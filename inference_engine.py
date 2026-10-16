from knowledge_base import RULES


def analyze_threat(symptom, firewall):
    """
    CyberShield inference engine.
    Matches the user's selected threat indicator
    with the rules in the knowledge base.
    """

    selected_rule = None

    # Search knowledge base
    for rule in RULES:
        if rule["symptom"] == symptom:
            selected_rule = rule.copy()
            selected_rule["actions"] = rule["actions"].copy()
            break

    # No matching rule
    if selected_rule is None:
        selected_rule = {
            "threat": "UNKNOWN ANOMALY",
            "severity": "UNKNOWN",
            "diagnosis": "No matching rule found in local knowledge base.",
            "actions": [
                "Perform manual packet capture and system log inspection."
            ]
        }

    # Firewall disabled → critical override
    if firewall == "disabled":
        selected_rule["severity"] = "CRITICAL HAZARD"

        selected_rule["actions"].insert(
            0,
            "URGENT OVERRIDE: Re-enable firewall rules immediately to contain breach!"
        )

    return selected_rule