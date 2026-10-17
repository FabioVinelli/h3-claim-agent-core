from __future__ import annotations


class H3IdrrAdapter:
    @staticmethod
    def emit_cypher_upsert(case_id: str, payer: str, underpayment: float) -> str:
        return (
            f"MERGE (c:ClaimCase:H3 {{caseId: '{case_id}'}}) "
            f"MERGE (p:Payer:H3 {{name: '{payer}'}}) "
            f"MERGE (c)-[:ADJUDICATED_BY]->(p) "
            f"SET c.underpayment = {underpayment}, c.updatedAt = datetime();"
        )
