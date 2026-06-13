ROADMAP_RULES = {
    "DAYS_EMPLOYED": {
        "3_months": "Avoid switching jobs frequently.",
        "6_months": "Stay employed continuously for at least 6 months.",
        "12_months": "Build a strong employment history."
    },

    "EXT_SOURCE_2": {
        "3_months": "Pay utility bills on time.",
        "6_months": "Maintain regular digital transactions.",
        "12_months": "Build consistent repayment behaviour."
    },

    "EXT_SOURCE_3": {
        "3_months": "Avoid missed payments.",
        "6_months": "Maintain healthy financial activity.",
        "12_months": "Improve overall creditworthiness."
    },

    "AMT_CREDIT": {
        "3_months": "Avoid taking additional loans.",
        "6_months": "Reduce outstanding liabilities.",
        "12_months": "Keep debt levels low."
    },

    "AMT_ANNUITY": {
        "3_months": "Reduce EMI burden if possible.",
        "6_months": "Avoid unnecessary borrowing.",
        "12_months": "Maintain manageable repayment obligations."
    }
}


def generate_roadmap(hurting_features):
    roadmap = {
        "3_months": [],
        "6_months": [],
        "12_months": []
    }

    for item in hurting_features:
        feature = item["feature"]

        if feature in ROADMAP_RULES:
            roadmap["3_months"].append(
                ROADMAP_RULES[feature]["3_months"]
            )

            roadmap["6_months"].append(
                ROADMAP_RULES[feature]["6_months"]
            )

            roadmap["12_months"].append(
                ROADMAP_RULES[feature]["12_months"]
            )

    return roadmap