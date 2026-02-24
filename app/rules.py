"""
Deterministic, explainable and rule-based regulatory triage engine
Its purpose is to:
- Provide a predictable first-pass triage for all complaints.
- Detect obvious high-risk/regulatory-triggering signals.
- Keep logic transparent for auditability.
- Flags when human review is compulsory

"""

from dataclasses import dataclass
from typing import List

@dataclass
class RuleResult:
    risk_level: str      #overall severity used by downstream systems: Low, Medium or High
    obligation: str      #checks if regularory escalation should activate: INTERNAL_ONLY or REQULATORY_REVIEW_REQUIRED  
    deadline_hours: int  # recommended SLA in hours
    human_review_required: bool   #safety gate, if true must be reviewed by human
    matched_rules: List[str]    #for auditability - shows which rule was fired


#Keyword rules definition
RULES = [
    ("REGULATOR_MENTION", ["fcac", "obsi", "ombudsman", "regulator"]),
    ("FRAUD_UNAUTHORIZED", ["unauthorized", "fraud", "identity theft", "stolen", "scam"]),
    ("PRIVACY_BREACH", ["privacy", "data breach", "leak", "personal information", "pii"]),
    ("LEGAL_THREAT", ["lawsuit", "legal action", "sue", "lawyer", "court"]),
]


def evaluate_rules(raw_text: str)-> RuleResult:
    """
Evaluates raw complaint text against deterministic rules
Its purpose is to:
- Scan for high-risk regulatory signal.
- Assign triage severity.
- Determine if human review is compulsory.

"""
    text = raw_text.lower()
    matched: List[str] = []

    #scan text for rule keyword matches
    for rule_name, keywords in RULES:
        if any (k in text for k in keywords):
            matched.append(rule_name)

    #regulatory escalatory signal
    regulatory_trigger = "REGULATOR_MENTION" in matched
    #high risk indicator for urgency
    high_risk = any(r in matched for r in ["FRAUD_UNAUTHORIZED", "PRIVACY_BREACH", "LEGAL_THREAT"])


    #if regulator is mentioned, route for human review
    if regulatory_trigger:
        return RuleResult(
            risk_level="HIGH",
            obligation="REQULATORY_REVIEW_REQUIRED",
            deadline_hours=24,
            human_review_required=True,
            matched_rules=matched,
        )
    
    #if other high risk, route to internal teams
    if high_risk:
        return RuleResult(
            risk_level="HIGH",
            obligation="INTERNAL_ONLY",
            deadline_hours=24,
            human_review_required=False,
            matched_rules=matched,
        )
        
    #if not critical, route to internal
    if matched:
        return RuleResult(
            risk_level="MEDIUM",
            obligation="INTERNAL_ONLY",
            deadline_hours=72,
            human_review_required=True,
            matched_rules=matched,
        )
        
    #low urgency
    return RuleResult(
            risk_level="LOW",
            obligation="INTERNAL_ONLY",
            deadline_hours=120,
            human_review_required=True,
            matched_rules=[],
         )