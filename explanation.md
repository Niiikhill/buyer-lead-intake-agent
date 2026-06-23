# Buyer Lead Intake Agent – Design Explanation

## 1. Overall Approach and Design Decisions

The goal of this project was to build a Buyer Lead Intake Agent that can help realtors quickly understand buyer requirements, identify suitable properties from an MLS dataset, and prepare for an informed follow-up conversation.

I approached the problem as a multi-stage pipeline consisting of four components:

1. Lead Parser Agent
2. Validation Agent
3. Property Matching Agent
4. Brief Generator

I chose to use a Large Language Model (Groq Llama 3) for requirement extraction because buyer inquiries are unstructured and may contain varying levels of detail. An LLM is well suited for converting free-text inquiries into a structured representation containing location preferences, budget, bedroom requirements, property type, desired features, and urgency.

For property matching, I used a rule-based scoring engine instead of relying entirely on an LLM. This approach provides transparency, predictable behavior, lower cost, and easier debugging. Realtors need to understand why a property was recommended, so explainable scoring was prioritized.

I also added a Validation Agent to handle prompt injection attempts and requests for sensitive information. Since the MLS dataset contains owner information, protecting that data is critical.

Finally, the Brief Generator converts extracted requirements and matching results into a realtor-friendly Lead Brief containing recommendations, warnings, missing information, and suggested next actions.

---

## 2. System Architecture

The system follows the workflow below:

Buyer Inquiry

↓

Lead Parser Agent

↓

Validation Agent

↓

Property Matching Agent

↓

Brief Generator

↓

Lead Brief

### Lead Parser Agent

The Lead Parser uses Groq Llama 3 to convert unstructured buyer messages into structured JSON fields such as:

- Buyer type
- Preferred locations
- Property type
- Budget
- Bedroom requirements
- Desired features
- Urgency

### Validation Agent

The Validation Agent analyzes inquiries for:

- Prompt injection attempts
- Requests for owner phone numbers
- Requests for owner names
- Attempts to override system behavior

If such behavior is detected, warnings are added to the Lead Brief and sensitive information is never exposed.

### Property Matching Agent

The Property Matching Agent compares buyer requirements against MLS listings and assigns a match score.

The score considers:

- Neighborhood match
- Budget compatibility
- Bedroom compatibility
- Property type compatibility
- Requested feature matches

Each recommended property includes an explanation describing why it was selected.

### Brief Generator

The Brief Generator produces a realtor-ready document that includes:

- Buyer Summary
- Potential Concerns
- Missing Information
- Recommended Properties
- Match Explanations
- Security Notes
- Realtor Notes
- Suggested Next Actions

---

## 3. Walkthrough of the 12 Lead Briefs

### Lead 001

Relocating buyer seeking a condo in Brickell or Downtown Miami with a budget below $700k. The system identified matching condos and prioritized neighborhood and budget compatibility.

### Lead 002

Family buyer looking for a larger home in Coral Gables or Pinecrest. The matching process emphasized bedroom count, neighborhood preference, and pool requirements.

### Lead 003

Buyer requested a four-bedroom property with a very low budget relative to available inventory. The system highlighted the budget mismatch and recommended discussing alternative neighborhoods or increased budget flexibility.

### Lead 004

Investor lead with insufficient information. Since no budget, property type, or investment goals were provided, the system avoided making unreliable recommendations and instead suggested a discovery conversation.

### Lead 005

Buyer appeared interested in a specific address. The system flagged this as a targeted property inquiry and advised the realtor to focus on comparable sales and offer strategy.

### Lead 006

Buyer included a prompt injection attempt requesting owner information. The system detected the request, blocked disclosure of sensitive information, and continued processing legitimate housing requirements.

### Lead 007

Buyer was searching for a property suitable for elderly parents. The system prioritized affordability, accessibility-related features, and preferred neighborhoods.

### Lead 008

Family buyer searching for a larger home with space for remote work. Matching emphasized bedroom count, budget, neighborhood preferences, and requested features.

### Lead 009

Cash buyer looking for a townhouse in Brickell. The matching engine prioritized location, property type, and bedroom requirements.

### Lead 010

Luxury waterfront buyer seeking high-end inventory with boat dock access. Matching focused on luxury neighborhoods, waterfront-related features, and budget compatibility.

### Lead 011

First-time homebuyer seeking an affordable condo. The system highlighted the closest matches and identified properties slightly above budget that may still be negotiable.

### Lead 012

Investor searching for multi-family or rental-oriented opportunities. The system prioritized properties matching the requested investment-oriented property types and budget range.

---

## 4. Security Considerations

A key requirement of any AI-powered real estate system is protecting sensitive information.

The MLS dataset contains owner information, including names and phone numbers. These fields should never be exposed simply because a user requests them.

To address this, the Validation Agent detects:

- Prompt injection attempts
- Requests for owner names
- Requests for owner phone numbers
- Attempts to override instructions

Lead 006 demonstrates this behavior. The buyer attempted to obtain owner information, but the system rejected the request and continued processing only legitimate housing requirements.

This design ensures that sensitive information remains protected while still providing value to the realtor.

---

## 5. AI Coding Tools Used

I used ChatGPT during development to accelerate implementation, generate boilerplate code, assist with debugging, and improve documentation.

All architecture decisions, matching logic, testing, and final output validation were reviewed manually. Several generated solutions were modified to better align with the requirements of the case study and the realities of a realtor workflow.

---

## 6. Tradeoffs and Future Improvements

The current implementation uses rule-based matching because it is transparent and easy to explain. However, there are several improvements I would make with additional time.

### Retrieval Improvements

- Semantic property search using embeddings
- Vector database retrieval
- Hybrid keyword and semantic matching

### Real Estate Intelligence

- School district analysis
- Walkability scores
- Commute-time estimates
- Neighborhood quality metrics
- Market trend analysis

### Agent Improvements

- Multi-agent orchestration using LangGraph
- Property research agents
- Buyer follow-up agents
- Automated realtor task generation

### Learning System

- Realtor feedback loop
- Conversion-based ranking optimization
- Personalized recommendation strategies

These additions would improve recommendation quality, personalization, and real-world usability while keeping the system secure and explainable.

---

## Conclusion

This project demonstrates an end-to-end Buyer Lead Intake workflow that converts unstructured buyer inquiries into structured realtor-ready Lead Briefs. The solution combines LLM-based understanding, explainable property matching, security validation, and actionable recommendations to help realtors respond more effectively to incoming buyer leads.