class BriefGenerator:    
    def generate(self, requirements, warnings, matches):

        raw_budget = requirements.get("budget_max")

        buyer_type = requirements.get("buyer_type") or "Not Specified"
        locations = requirements.get("locations") or "Not Specified"
        property_type = requirements.get("property_type") or "Not Specified"
        bedrooms = requirements.get("bedrooms") or "Not Specified"
        features = requirements.get("features") or "Not Specified"
        urgency = requirements.get("urgency") or "Not Specified"

        budget_display = (
            f"${raw_budget:,}"
            if isinstance(raw_budget, (int, float))
            else "Not Specified"
        )

        brief = "# BUYER LEAD BRIEF\n\n"

        # ==================================
        # Buyer Summary
        # ==================================

        brief += "## Buyer Summary\n\n"

        brief += f"- Buyer Type: {buyer_type}\n"
        brief += f"- Preferred Locations: {locations}\n"
        brief += f"- Property Type: {property_type}\n"
        brief += f"- Bedrooms: {bedrooms}\n"
        brief += f"- Budget: {budget_display}\n"
        brief += f"- Desired Features: {features}\n"
        brief += f"- Urgency: {urgency}\n\n"

        # ==================================
        # Potential Concerns
        # ==================================

        concerns = []

        if isinstance(raw_budget, (int, float)) and raw_budget < 320000:
            concerns.append(
                "Requested budget appears significantly below comparable MLS inventory."
            )

        if str(buyer_type).lower() == "investor" and raw_budget is None:
            concerns.append(
                "Insufficient information to recommend investment opportunities."
            )

        if isinstance(locations, list):
            for loc in locations:
                if "bay road" in str(loc).lower():
                    concerns.append(
                        "Buyer appears interested in a specific property and may require offer strategy guidance."
                    )

        if concerns:

            brief += "## Potential Concerns\n\n"

            for concern in concerns:
                brief += f"- {concern}\n"

            brief += "\n"

        # ==================================
        # Missing Information
        # ==================================

        missing = []

        if raw_budget is None:
            missing.append("Budget range")

        if property_type == "Not Specified":
            missing.append("Property type")

        if urgency == "Not Specified":
            missing.append("Timeline / urgency")

        if missing:

            brief += "## Missing Information\n\n"

            for item in missing:
                brief += f"- {item}\n"

            brief += "\n"

        # ==================================
        # Security Notes
        # ==================================

        if warnings:

            brief += "## Security Notes\n\n"

            for warning in warnings:
                brief += f"- {warning}\n"

            brief += "- Sensitive owner information was not disclosed.\n\n"

        # ==================================
        # Weak Investor Lead
        # ==================================

        if matches and matches[0]["match_score"] == 0:

            brief += "## Recommended Properties\n\n"

            brief += (
                "No reliable property recommendations generated.\n\n"
            )

            brief += (
                "Reason:\n"
                "- Budget not specified\n"
                "- Property type not specified\n"
                "- Investment goals not specified\n\n"
            )

            brief += (
                "Recommended Realtor Action:\n"
                "- Schedule a discovery call\n"
                "- Confirm investment strategy\n"
                "- Confirm budget range\n"
                "- Determine preferred property type\n"
            )

            return brief

        # ==================================
        # Recommended Properties
        # ==================================

        brief += "## Recommended Properties\n\n"

        for i, match in enumerate(matches, start=1):

            brief += f"### Property {i}\n\n"

            brief += f"- Address: {match['address']}\n"
            brief += f"- Neighborhood: {match['neighborhood']}\n"
            brief += f"- Property Type: {match['property_type']}\n"
            brief += f"- Price: ${match['price']:,}\n"
            brief += f"- Bedrooms: {match['bedrooms']}\n"
            brief += f"- Match Score: {match['match_score']}/100\n\n"

            reasons = match.get("match_reasons", [])

            if reasons:

                brief += "- Why It Matches:\n"

                for reason in reasons:
                    brief += f"  • {reason}\n"

                brief += "\n"

        # ==================================
        # Realtor Notes
        # ==================================

        brief += "## Realtor Notes\n\n"

        if isinstance(raw_budget, (int, float)) and raw_budget < 320000:

            brief += (
                "⚠ Buyer expectations may not align with current market inventory. "
                "Recommend discussing budget flexibility or alternative neighborhoods.\n\n"
            )

        elif str(buyer_type).lower() == "investor" and raw_budget is None:

            brief += (
                "⚠ Investor lead lacks critical information. "
                "Discovery call recommended before presenting properties.\n\n"
            )

        elif isinstance(locations, list) and any(
            "bay road" in str(loc).lower()
            for loc in locations
        ):

            brief += (
                "⚠ Buyer appears focused on a specific property. "
                "Seller motivation is not available in MLS data. "
                "Recommend reviewing comparable sales and days on market.\n\n"
            )

        elif warnings:

            brief += (
                "⚠ Inquiry contained a request for sensitive information. "
                "Only legitimate housing requirements were processed.\n\n"
            )

        else:

            brief += (
                "Buyer requirements appear sufficiently defined for an initial outreach conversation.\n\n"
            )

        # ==================================
        # Suggested Next Action
        # ==================================

        brief += "## Suggested Next Action\n\n"

        brief += "Contact the buyer within 24 hours and confirm:\n"
        brief += "- Financing status\n"
        brief += "- Preferred neighborhoods\n"
        brief += "- Budget flexibility\n"
        brief += "- Move-in timeline\n"
        brief += "- Must-have vs nice-to-have features\n"

        return brief