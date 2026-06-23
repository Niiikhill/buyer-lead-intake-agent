import json
from groq import Groq


class LeadParser:

    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def parse_lead(self, inquiry):

        prompt = f"""
Extract the buyer requirements from this real estate inquiry.

Return ONLY valid JSON.

Fields:
- buyer_type
- locations
- property_type
- bedrooms
- budget_max
- features
- urgency

Inquiry:
{inquiry}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        try:
            parsed_json = json.loads(content)
            return parsed_json

        except Exception as e:

            print("Parser failed. Returning fallback structure.")

            return {
                "buyer_type": None,
                "locations": [],
                "property_type": None,
                "bedrooms": None,
                "budget_max": None,
                "features": [],
                "urgency": None
            }