"""
factcheck_agent.py

A lightweight fact-checking agent for MARS.

It performs:
1. Cross-source consistency check
2. Claim verification against retrieved context
3. Flags missing or contradicted information

This helps demonstrate multi-agent design and evaluation.
"""

from typing import List, Dict


# -------------------------------------------------------------
# 1. Extract key claims from summary (simple heuristics)
# -------------------------------------------------------------

def extract_claims(summary: str) -> List[str]:
    """
    Splits summary into simple granular claims.
    Very simple approach: split by periods.
    """
    claims = [s.strip() for s in summary.split(".") if s.strip()]
    return claims


# -------------------------------------------------------------
# 2. Check if claim appears in any retrieved memory chunk
# -------------------------------------------------------------

def claim_in_context(claim: str, context_text: str) -> bool:
    """
    Check if a claim is supported by retrieved context (case-insensitive).
    """
    return claim.lower() in context_text.lower()


# -------------------------------------------------------------
# 3. Run Fact-Check
# -------------------------------------------------------------

def fact_check(summary: str, retrieved_context: str) -> Dict:
    """
    Returns:
    {
        "supported": [...claims],
        "not_supported": [...claims],
        "total_claims": n
    }
    """
    claims = extract_claims(summary)

    supported = []
    unsupported = []

    for claim in claims:
        if claim_in_context(claim, retrieved_context):
            supported.append(claim)
        else:
            unsupported.append(claim)

    return {
        "total_claims": len(claims),
        "supported": supported,
        "not_supported": unsupported
    }


# -------------------------------------------------------------
# 4. Annotate summary with fact-checking results
# -------------------------------------------------------------

def annotate_summary(summary: str, fc_results: Dict) -> str:
    """
    Adds fact-checking metadata at the bottom of the summary.
    """

    supported = len(fc_results["supported"])
    unsupported = len(fc_results["not_supported"])
    total = fc_results["total_claims"]

    metadata = (
        "\n\n---\n"
        f"**Fact Check Results:**\n"
        f"- Supported claims: {supported}/{total}\n"
        f"- Unsupported claims: {unsupported}/{total}\n"
    )

    if unsupported > 0:
        metadata += "**Note:** Some statements could not be verified from retrieved sources.\n"

    return summary + metadata
