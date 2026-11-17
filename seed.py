# from core import register_agent

# # Simulated company profiles for the demo (not real company data).
# COMPANIES = [
#     {
#         "company_name": "Swiggy",
#         "industry_category": "Food delivery and quick commerce",
#         "aliases": ["swiggy", "instamart"],
#         "interest_manifesto": (
#             "Food delivery and quick commerce platform. Interested in festival and "
#             "seasonal campaigns, delivery offers, restaurant partnerships, and payment "
#             "or card tie-ups that increase order volume."
#         ),
#     },
#     {
#         "company_name": "PhonePe",
#         "industry_category": "Payments and fintech",
#         "aliases": ["phonepe", "phonepay", "phone pe"],
#         "interest_manifesto": (
#             "UPI payments app. Interested in e-commerce and food delivery promotions, "
#             "merchant cashback campaigns, festive offers, and payment partnerships "
#             "with consumer brands."
#         ),
#     },
#     {
#         "company_name": "HDFC Bank",
#         "industry_category": "Banking and cards",
#         "aliases": ["hdfc", "hdfc bank"],
#         "interest_manifesto": (
#             "Bank offering credit cards, debit cards, loans and EMI. Interested in "
#             "card-linked offers with retailers and delivery platforms, no-cost EMI "
#             "campaigns, vehicle financing, and festive spending promotions."
#         ),
#     },
#     {
#         "company_name": "Flipkart",
#         "industry_category": "E-commerce",
#         "aliases": ["flipkart"],
#          "interest_manifesto": (
#             "Online retail marketplace for electronics, fashion, and home goods. "
#             "Interested in bank credit card and EMI offers, UPI checkout cashback, "
#             "and B2B warehouse or parcel shipping logistics. Not interested in "
#             "restaurant food delivery or hyperlocal meal discounts."
#         ),
#     },
#     {
#         "company_name": "Bajaj Auto",
#         "industry_category": "Two-wheeler and three-wheeler manufacturing",
#         "aliases": ["bajaj", "bajaj auto"],
#         "interest_manifesto": (
#             "Motorcycle and three-wheeler manufacturer. Interested in vehicle launches, "
#             "vehicle financing and low down-payment schemes, dealer network expansion, "
#             "and auto loan partnerships."
#         ),
#     },
# ]

# if __name__ == "__main__":
#     for company in COMPANIES:
#         agent_id, api_key = register_agent(**company)
#         print(f"{company['company_name']}: id={agent_id}")
#     print("Seeded", len(COMPANIES), "agents.")

from core import register_agent

# Simulated company profiles for the demo (not real company data).
#
# interest_manifesto : POSITIVE only. Never write "not interested in" here,
#                      because embeddings don't understand negation.
# offers_text        : what this agent can concretely contribute to another
#                      agent's post (the key field for relevance).
# excludes_text      : topics this agent does NOT want. Embedded separately
#                      and used as a penalty in scoring.

COMPANIES = [
    {
        "company_name": "Swiggy",
        "industry_category": "Food delivery and quick commerce",
        "aliases": ["swiggy", "instamart"],
        "interest_manifesto": (
            "Food delivery and quick commerce platform. Interested in festival and "
            "seasonal campaigns, delivery offers, restaurant partnerships, and payment "
            "or card tie-ups that increase order volume."
        ),
        "offers_text": (
            "Food and grocery delivery offers, restaurant and cloud kitchen "
            "partnerships, delivery fee discounts, festive order campaigns."
        ),
        "excludes_text": (
            "Vehicle manufacturing, dealership promotions, auto loans, "
            "warehouse and parcel logistics."
        ),
    },
    {
        "company_name": "PhonePe",
        "industry_category": "Payments and fintech",
        "aliases": ["phonepe", "phonepay", "phone pe"],
        "interest_manifesto": (
            "UPI payments app. Interested in e-commerce and food delivery promotions, "
            "merchant cashback campaigns, festive offers, and payment partnerships "
            "with consumer brands."
        ),
        "offers_text": (
            "UPI payment offers, merchant cashback, scratch cards and rewards "
            "on partner purchases, checkout payment integrations."
        ),
        "excludes_text": (
            "Vehicle manufacturing and dealer network expansion, "
            "restaurant menu or recipe announcements."
        ),
    },
    {
        "company_name": "HDFC Bank",
        "industry_category": "Banking and cards",
        "aliases": ["hdfc", "hdfc bank"],
        "interest_manifesto": (
            "Bank offering credit cards, debit cards, loans and EMI. Interested in "
            "card-linked offers with retailers and delivery platforms, no-cost EMI "
            "campaigns, vehicle financing, and festive spending promotions."
        ),
        "offers_text": (
            "Credit and debit card discounts, no-cost EMI, bank cashback offers, "
            "vehicle and consumer loans on partner purchases."
        ),
        "excludes_text": (
            "Restaurant menus, food recipes, warehouse logistics, "
            "product catalogue listings."
        ),
    },
    {
        "company_name": "Flipkart",
        "industry_category": "E-commerce",
        "aliases": ["flipkart"],
        "interest_manifesto": (
            "Online retail marketplace for electronics, fashion, and home goods. "
            "Interested in seller and brand partnerships, big sale events, "
            "and warehouse or parcel shipping logistics."
        ),
        "offers_text": (
            "Marketplace sale events, electronics and fashion discounts, "
            "seller onboarding, parcel shipping and fulfilment partnerships."
        ),
        "excludes_text": (
            "Restaurant food delivery, hyperlocal meal discounts, "
            "grocery delivery offers, vehicle manufacturing."
        ),
    },
    {
        "company_name": "Bajaj Auto",
        "industry_category": "Two-wheeler and three-wheeler manufacturing",
        "aliases": ["bajaj", "bajaj auto"],
        "interest_manifesto": (
            "Motorcycle and three-wheeler manufacturer. Interested in vehicle launches, "
            "vehicle financing and low down-payment schemes, dealer network expansion, "
            "and auto loan partnerships."
        ),
        "offers_text": (
            "Motorcycle and three-wheeler launches, test rides, dealership "
            "promotions, low down-payment financing schemes."
        ),
        "excludes_text": (
            "Food delivery offers, online shopping discounts, "
            "payment cashback campaigns."
        ),
    },
]

if __name__ == "__main__":
    for company in COMPANIES:
        agent_id, api_key = register_agent(**company)
        print(f"{company['company_name']}: id={agent_id}")
    print("Seeded", len(COMPANIES), "agents.")