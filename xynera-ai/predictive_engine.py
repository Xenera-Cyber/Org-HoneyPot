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
