FEATURE_MESSAGES = {
    'EXT_SOURCE_1_good': 'Your first external credit signal is strong',
    'EXT_SOURCE_1_bad': 'Your first external credit signal is weak',
    'EXT_SOURCE_2_good': 'Your second external credit signal is strong',
    'EXT_SOURCE_2_bad': 'Your second external credit signal is weak',
    'EXT_SOURCE_3_good': 'Your third external credit signal is strong',
    'EXT_SOURCE_3_bad': 'Your third external credit signal is weak',
    'DAYS_EMPLOYED_good': 'Your employment history is stable and long',
    'DAYS_EMPLOYED_bad': 'Your employment duration is relatively short',
    'DAYS_BIRTH_good': 'Your age profile shows maturity and reliability',
    'DAYS_BIRTH_bad': 'Your age profile suggests limited credit history',
    'AMT_INCOME_TOTAL_good': 'Your income level is a strong positive factor',
    'AMT_INCOME_TOTAL_bad': 'Your income level is lower than average applicants',
    'AMT_CREDIT_good': 'Your requested credit amount is appropriate',
    'AMT_CREDIT_bad': 'Your requested credit amount is high for your profile',
    'AMT_ANNUITY_good': 'Your loan repayment amount is manageable',
    'AMT_ANNUITY_bad': 'Your loan repayment burden is relatively high',
    'AMT_GOODS_PRICE_good': 'Your requested loan amount looks reasonable',
    'AMT_GOODS_PRICE_bad': 'Your requested loan amount is high for your profile',
    'DAYS_ID_PUBLISH_good': 'Your ID has been stable for a long time',
    'DAYS_ID_PUBLISH_bad': 'Your ID was recently issued which reduces trust signals',
    'DAYS_REGISTRATION_good': 'Your registration history is long and stable',
    'DAYS_REGISTRATION_bad': 'Your registration history is recent',
    'DAYS_LAST_PHONE_CHANGE_good': 'Your phone number has been stable',
    'DAYS_LAST_PHONE_CHANGE_bad': 'You changed your phone number recently',
    'AMT_REQ_CREDIT_BUREAU_YEAR_good': 'You have few credit enquiries this year',
    'AMT_REQ_CREDIT_BUREAU_YEAR_bad': 'You have had multiple credit enquiries this year',
    'REGION_RATING_CLIENT_good': 'Your region has a favorable credit rating',
    'REGION_RATING_CLIENT_bad': 'Your region has a higher than average risk rating',
    'FLAG_OWN_CAR_Y_good': 'Owning a car is a positive asset signal',
    'FLAG_OWN_CAR_Y_bad': 'Not owning a car slightly affects your asset profile',
    'FLAG_OWN_REALTY_Y_good': 'Owning property is a strong positive signal',
    'FLAG_OWN_REALTY_Y_bad': 'Not owning property affects your asset profile',
}

def get_feature_message(feature: str, context: str) -> str:
    key = f"{feature}_{context}"
    return FEATURE_MESSAGES.get(key, feature)


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
    },
    "DAYS_BIRTH": {
        "3_months": "Start building financial activity early.",
        "6_months": "Open a savings account and transact regularly.",
        "12_months": "Build a long-term financial track record."
    },
    "AMT_INCOME_TOTAL": {
        "3_months": "Explore additional income sources like freelancing.",
        "6_months": "Document all income sources formally.",
        "12_months": "Aim for a stable income increase through skill development."
    },
    "DAYS_REGISTRATION": {
        "3_months": "Ensure your address and ID documents are up to date.",
        "6_months": "Avoid changing residence frequently.",
        "12_months": "Maintain stable residential history."
    },
    "DAYS_LAST_PHONE_CHANGE": {
        "3_months": "Avoid changing your registered mobile number.",
        "6_months": "Keep your UPI-linked number consistent.",
        "12_months": "Maintain a stable digital identity."
    },
    "AMT_REQ_CREDIT_BUREAU_YEAR": {
        "3_months": "Avoid applying for multiple loans simultaneously.",
        "6_months": "Space out any credit applications.",
        "12_months": "Limit credit enquiries to once or twice a year."
    },
    "AMT_GOODS_PRICE": {
        "3_months": "Request only what you genuinely need.",
        "6_months": "Align loan amount with your repayment capacity.",
        "12_months": "Build a track record of responsible borrowing."
    },
    "REGION_RATING_CLIENT": {
        "3_months": "Ensure your registered address is accurate.",
        "6_months": "Maintain clean financial records in your region.",
        "12_months": "Build local financial credibility."
    },
    "CNT_CHILDREN": {
        "3_months": "Document family income accurately.",
        "6_months": "Demonstrate stable household finances.",
        "12_months": "Show consistent savings despite family obligations."
    },
    "CNT_FAM_MEMBERS": {
        "3_months": "Show stable household income coverage.",
        "6_months": "Reduce unnecessary expenditure.",
        "12_months": "Build family financial resilience."
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