import json

def bait_recommendation(asset_access):

    most_attractive = max(asset_access, key=asset_access.get)

    total_access = sum(asset_access.values())

    analytics = {
        "asset_statistics": asset_access,
        "most_attractive_asset": most_attractive,
        "access_count": asset_access[most_attractive],
        "total_asset_access": total_access
    }

    return analytics
def deception_effectiveness_report():

    report = {

        "most_successful_trap": "admin_credentials.txt",

        "most_visited_asset": "passwords.txt",

        "highest_engagement_session": {

            "session_id": "SESSION_001",

            "engagement_score": 94
        },

        "ai_performance": {

            "total_predictions": 125,

            "correct_predictions": 118,

            "accuracy": "94.4%"

        }

    }

    return report
def predictive_intelligence(
    curiosity_score,
    risk_score,
    engagement_level
):
    """
    Predict attacker behaviour and session outcome
    """

    # Predict next attacker action
    if curiosity_score >= 80:
        next_action = "Privilege Escalation"
    elif curiosity_score >= 50:
        next_action = "Credential Access"
    else:
        next_action = "Reconnaissance"

    # Predict high-value target
    if risk_score >= 80:
        target = "Admin Credentials"
    elif risk_score >= 50:
        target = "Sensitive Files"
    else:
        target = "Public Directories"

    # Deception success probability
    if engagement_level == "HIGH":
        deception_probability = "92%"
    elif engagement_level == "MEDIUM":
        deception_probability = "74%"
    else:
        deception_probability = "51%"

    # Session outcome
    if risk_score >= 80:
        outcome = "High Risk Session"
    elif risk_score >= 50:
        outcome = "Medium Risk Session"
    else:
        outcome = "Low Risk Session"

    return {
        "next_probable_action": next_action,
        "high_value_target": target,
        "deception_success_probability": deception_probability,
        "session_outcome": outcome
    }
if __name__ == "__main__":

    assets = {

        "passwords.txt":27,

        "database_backup.sql":18,

        "finance.xlsx":9,

        "ssh_keys":14,

        "admin_credentials.txt":31

    }

    result = bait_recommendation(assets)

    print(json.dumps(result, indent=4))

    print("\n========== Deception Effectiveness Report ==========\n")

    report = deception_effectiveness_report()

    print(json.dumps(report, indent=4))
    print("\n========== Predictive Intelligence ==========\n")

    prediction = predictive_intelligence(

    curiosity_score=91,

    risk_score=88,

    engagement_level="HIGH"

    )

    print(json.dumps(prediction, indent=4))
