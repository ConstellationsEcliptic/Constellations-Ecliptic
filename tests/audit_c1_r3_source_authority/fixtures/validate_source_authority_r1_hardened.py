#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys,zipfile,os,stat
from pathlib import Path

EXPECTED_H8='4077b60b120c6415e633b5fdaa88b9dd7f52ba55a5a0c5a556640a62f884c587'
EXPECTED_LOCK='fffb23655dd91c3d672207f05be6d3af9141b8254b603af3d2c46882a27b6fbd'
EXPECTED_AGG='0cfc76a9dc51296f2241492e3376f1e71d13dd4f36b476253d4b82df57dfc990'
EXPECTED={
 'seas_18.se1':'a2cd8fc33807c78ca9a700c91c2e042258b12fc4796519e00781440b5ad8b2e2',
 'semo_18.se1':'1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7',
 'sepl_18.se1':'ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66',
}
BLOBS={
 'seas_18.se1':'8f900cab7e557e4c41f758a6bf3a3c3967e7e3db',
 'semo_18.se1':'5427d9f885fd6cb9489584ade37e52c6abb4d407',
 'sepl_18.se1':'786702cd04506371ee6223af1ebac02d54c848b8',
}

def fail(msg): raise RuntimeError(msg)
def req(cond,msg):
    if not cond: fail(msg)
def sha(p):
    h=hashlib.sha256();
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def regular(p): return p.exists() and p.is_file() and not p.is_symlink()
def safe_tree(root):
    req(root.is_dir() and not root.is_symlink(),'root missing/not-regular')
    for p in root.rglob('*'):
        rel=p.relative_to(root).as_posix(); q=Path(rel)
        req(not q.is_absolute() and '..' not in q.parts and '\\' not in rel,'unsafe relative path')
        req(not p.is_symlink(),f'symlink: {rel}')

def verify(root:Path):
    safe_tree(root)
    record=json.loads((root/'CE_SOURCE_AUTHORITY_RECORD_R1.json').read_bytes())
    req(record.get('resolution_status')=='PARTIAL_RESOLUTION_NOT_ESTABLISHED','resolution status mismatch')
    req(record.get('sealed') is False,'sealed overclaim')
    req(record.get('authorized') is False,'authorized overclaim')
    req(record.get('fail_closed') is True,'fail-closed flag missing')
    parent=record['parent']; req(parent['h8_package_sha256']==EXPECTED_H8,'H8 parent mismatch'); req(parent['expected_h8_package_sha256']==EXPECTED_H8,'expected H8 mismatch'); req(parent['frozen_master_sha256']=='b46c52ab9a767fd2a5765f7e56e8e45f4d8404bf9c68121f3a92189f4add6542','master mismatch')
    lock=record['canonical_lock']; req(lock=={'id':'CE-V1-CANONICAL-DATA-2026D-SE-V2.10.3BFINAL','revision':4,'sha256':EXPECTED_LOCK,'expected_sha256':EXPECTED_LOCK,'status':'SEAL_CANDIDATE'},'canonical lock identity mismatch')
    i=record['upstream_authority']['iana']; req(i['release']=='2026d','IANA release'); req(i['release_date']=='2026-09-11','IANA release date'); req(i['commit']=='d633fe7ed3de8e00ce7cac991376a064a1373bb1','IANA commit'); req(i['archive_sha256']=='0cb2aa8e333c3dc049badc42a0c61f21987b8cd44e107fa900bad764aacc7767','IANA SHA256'); req(i['signing_primary_fingerprint'].upper()=='7E3792A9D8ACF7D633BC1588ED97E90E62AA7E34','IANA signer')
    sw=record['upstream_authority']['swisseph']; req(sw['repository']=='https://github.com/aloistr/swisseph.git','Swiss repo'); req(sw['release_tag']=='v2.10.3bfinal','Swiss release'); req(sw['commit']=='f4dcd18e8005dde95fd8a8d2312ed12f9accd1b0','Swiss commit'); req(sw['upstream_basis']=='JPL_DE441','Swiss upstream basis')
    h8=root/'evidence/parent/CE_V1_H8_FULL_CHAIN_REHARDENED_R2-2026-09-23.zip'; lk=root/'evidence/canonical-data/canonical-data-lock.rev4-h3-truth-repaired.yaml'; ep=root/'evidence/canonical-data/ephemeris'
    req(regular(h8),'H8 missing'); req(sha(h8)==EXPECTED_H8,'H8 byte mismatch'); req(regular(lk),'lock missing'); req(sha(lk)==EXPECTED_LOCK,'lock byte mismatch'); req(ep.is_dir() and not ep.is_symlink(),'ephemeris dir invalid')
    actual_names=sorted(p.name for p in ep.iterdir())
    req(actual_names==sorted(EXPECTED),'ephemeris file-set mismatch')
    rows=[]
    for n,h in EXPECTED.items():
        p=ep/n; req(regular(p),f'{n} not regular'); b=p.read_bytes(); actual=hashlib.sha256(b).hexdigest(); req(actual==h,f'{n} hash mismatch'); oid=hashlib.sha1(b'blob %d\0'%len(b)+b).hexdigest(); req(oid==BLOBS[n],f'{n} git blob mismatch'); rec=sw['artifact_files'][n]; req(rec['sha256']==h and rec['git_blob_oid_sha1']==oid and rec['object_type_required']=='blob',f'{n} record binding mismatch'); rows.append((n,h))
    agg=hashlib.sha256(('\n'.join(f'{n} {h}' for n,h in sorted(rows))+'\n').encode()).hexdigest(); req(agg==EXPECTED_AGG,'aggregate mismatch'); req(sw['canonical_aggregate_sha256']==EXPECTED_AGG,'record aggregate mismatch'); req(sw['expected_canonical_aggregate_sha256']==EXPECTED_AGG,'expected aggregate mismatch')
    ce=record['ce_production_source_authority']; req(ce['status']=='NOT_ESTABLISHED','production status overclaim')
    for k in ['repository_locator','exact_commit','source_tree_sha256','approved_signer_fingerprint','approved_keyring_sha256','signed_source_statement']:
        req(ce[k] is None,f'production field unexpectedly populated: {k}')

def main():
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'subject'
    try:
        verify(root); print('C1_R3_HARDENED_SOURCE_AUTHORITY_VALIDATOR_PASS'); return 0
    except Exception as e:
        print('C1_R3_HARDENED_SOURCE_AUTHORITY_VALIDATOR_FAIL: '+str(e)); return 20
if __name__=='__main__': raise SystemExit(main())
