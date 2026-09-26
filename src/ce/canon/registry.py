from __future__ import annotations


class CanonRegistryNotEstablished(RuntimeError):
    pass


def get_rule(rule_id: str) -> None:
    raise CanonRegistryNotEstablished(
        f"Canon rule registry is not materialized: {rule_id}"
    )
