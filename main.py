import os
import json

from dotenv import load_dotenv

from agents.lead_parser import LeadParser
from agents.validation_agent import ValidationAgent
from agents.property_matcher import PropertyMatcher
from agents.brief_generator import BriefGenerator

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# Initialize agents
parser = LeadParser(api_key)
validator = ValidationAgent()
matcher = PropertyMatcher()
generator = BriefGenerator()

# Load all buyer inquiries
with open("data/sample_buyer_inquiries.json", "r") as f:
    leads = json.load(f)

print(f"\nProcessing {len(leads)} buyer leads...\n")

# Process each lead
for lead in leads:

    lead_id = lead["lead_id"]
    inquiry = lead["message"]

    print(f"Processing {lead_id}...")

    try:
        # Step 1: Parse Lead
        requirements = parser.parse_lead(inquiry)
        print("Requirements:")
        print(requirements)

        # Step 2: Validate Lead
        warnings = validator.validate(inquiry)

        # Step 3: Match Properties
        matches = matcher.get_top_matches(requirements)

        # Step 4: Generate Brief
        brief = generator.generate(
            requirements,
            warnings,
            matches
        )

        # Step 5: Save Brief
        output_file = f"outputs/{lead_id}.md"

        with open(output_file, "w") as f:
            f.write(brief)

        print(f" Saved: {output_file}")

    except Exception as e:
        print(f" Error processing {lead_id}: {e}")

print("\n All leads processed!")