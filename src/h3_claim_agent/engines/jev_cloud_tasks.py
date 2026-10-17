from __future__ import annotations

from typing import Any


class JevModelTierRouter:
    FLASH_CARCS = {"16", "252", "45", "B7", "29"}
    PRO_CARCS = {"197", "198", "50", "51", "97", "4", "59"}

    @classmethod
    def route_model_tier(cls, denial_codes: list[str]) -> str:
        clean_carcs = {c.upper().replace("CARC", "").strip() for c in denial_codes}
        if clean_carcs.intersection(cls.PRO_CARCS):
            return "gemini-2.5-pro"
        return "gemini-2.5-flash"

    @classmethod
    def enqueue_shadow_evaluation(cls, run_id: str, payload: dict[str, Any], queue_name: str = "jev-shadow-queue") -> dict[str, str]:
        return {
            "status": "ENQUEUED",
            "queue": queue_name,
            "run_id": run_id,
            "target_model": cls.route_model_tier(payload.get("denial_codes", [])),
        }
