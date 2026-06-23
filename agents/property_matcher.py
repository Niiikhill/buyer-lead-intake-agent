import pandas as pd


class PropertyMatcher:

    def __init__(self):
        self.df = pd.read_csv("data/miami_mls_listings.csv")

    def calculate_match_score(self, row, requirements):

        score = 0
        reasons = []

        # ==================================
        # LOCATION MATCH (40 points)
        # ==================================

        locations = requirements.get("locations") or []

        if isinstance(locations, str):
            locations = [locations]

        if row["neighborhood"] in locations:
            score += 40
            reasons.append(
                f"Located in preferred neighborhood ({row['neighborhood']})"
            )

        # ==================================
        # BUDGET MATCH (25 points)
        # ==================================

        budget_max = requirements.get("budget_max")

        if budget_max:

            if row["price"] <= budget_max:
                score += 25
                reasons.append("Within stated budget")

            elif row["price"] <= budget_max * 1.15:
                score += 10
                reasons.append(
                    "Slightly above budget but potentially negotiable"
                )

        # ==================================
        # BEDROOM MATCH (15 points)
        # ==================================

        bedrooms = requirements.get("bedrooms")

        if isinstance(bedrooms, dict):
            bedrooms = bedrooms.get("min", 0)

        elif isinstance(bedrooms, list):
            bedrooms = min(bedrooms)

        elif bedrooms is None:
            bedrooms = 0

        if bedrooms and pd.notna(row["bedrooms"]):

            diff = abs(row["bedrooms"] - bedrooms)

            if diff == 0:
                score += 15
                reasons.append(
                    f"Exact bedroom match ({int(row['bedrooms'])} BR)"
                )

            elif diff == 1:
                score += 5
                reasons.append(
                    "Bedroom count closely matches requirement"
                )

            elif diff == 2:
                score += 2

        # ==================================
        # PROPERTY TYPE MATCH (10 points)
        # ==================================

        property_type = requirements.get("property_type")

        if property_type:

            row_type = str(row["property_type"]).lower()

            if isinstance(property_type, list):

                for pt in property_type:

                    if str(pt).lower() in row_type:
                        score += 10
                        reasons.append(
                            f"Matches desired property type ({row['property_type']})"
                        )
                        break

            else:

                if str(property_type).lower() in row_type:
                    score += 10
                    reasons.append(
                        f"Matches desired property type ({row['property_type']})"
                    )

        # ==================================
        # FEATURE MATCH (up to 20 points)
        # ==================================

        requested_features = requirements.get("features") or []

        feature_text = str(row["features"]).lower()

        feature_score = 0

        for feature in requested_features:

            if not feature:
                continue

            feature = str(feature).lower()

            if feature in feature_text:

                feature_score += 5

                reasons.append(
                    f"Includes requested feature: {feature}"
                )

        score += min(feature_score, 20)

        # ==================================
        # SCORE CAP
        # ==================================

        score = min(score, 100)

        return score, reasons

    def get_top_matches(self, requirements):

        matches = []

        for _, row in self.df.iterrows():

            score, reasons = self.calculate_match_score(
                row,
                requirements
            )

            matches.append({
                "listing_id": row["listing_id"],
                "address": row["address"],
                "neighborhood": row["neighborhood"],
                "price": row["price"],
                "bedrooms": row["bedrooms"],
                "property_type": row["property_type"],
                "match_score": score,
                "match_reasons": reasons
            })

        matches = sorted(
            matches,
            key=lambda x: x["match_score"],
            reverse=True
        )

        return matches[:5]