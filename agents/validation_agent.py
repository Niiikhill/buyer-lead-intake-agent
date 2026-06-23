class ValidationAgent:

    def validate(self, inquiry_text):

        warnings = []

        text = inquiry_text.lower()

        # Prompt Injection
        if "ignore all previous instructions" in text:
            warnings.append(
                "Prompt injection attempt detected."
            )

        # Privacy Request
        if "owner names" in text or "phone numbers" in text:
            warnings.append(
                "Request for sensitive owner information rejected."
            )

        # Seller Motivation
        if "seller motivation" in text:
            warnings.append(
                "Seller motivation information unavailable in MLS data."
            )

        return warnings