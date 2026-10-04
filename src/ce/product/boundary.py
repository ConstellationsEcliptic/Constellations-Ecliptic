from __future__ import annotations

from dataclasses import dataclass

from ce.foundation.status import CalculationStatus


@dataclass(frozen=True)
class ProductBoundaryDecision:
    status: CalculationStatus
    signal_processing_allowed: bool
    canon_claim_allowed: bool
    ai_release_allowed: bool
    quiet_sky_allowed: bool
    reason: str


def preserve_calculation_truth(status: CalculationStatus) -> ProductBoundaryDecision:
    """Preserve non-VALID calculation states across product boundaries.

    This is a guard, not a production authorization mechanism. A VALID
    calculation still requires downstream qualification before any claim.
    """
    if not isinstance(status, CalculationStatus):
        raise ValueError("product_boundary_status_invalid")

    if status is not CalculationStatus.VALID:
        return ProductBoundaryDecision(
            status=status,
            signal_processing_allowed=False,
            canon_claim_allowed=False,
            ai_release_allowed=False,
            quiet_sky_allowed=False,
            reason="non_valid_calculation_state_preserved",
        )

    return ProductBoundaryDecision(
        status=status,
        signal_processing_allowed=True,
        canon_claim_allowed=True,
        ai_release_allowed=True,
        quiet_sky_allowed=False,
        reason="valid_state_requires_downstream_qualification",
    )
