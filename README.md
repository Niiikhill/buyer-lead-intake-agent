# Buyer Lead Intake Agent

## Overview

This project implements a Buyer Lead Intake Agent for real estate professionals. The system processes buyer inquiries, extracts structured requirements using a Large Language Model (LLM), matches buyer needs against MLS listings, and generates actionable Lead Briefs for realtors.

The objective is to help realtors quickly understand buyer intent, identify suitable properties, and prioritize follow-up actions.

---

## Features

- LLM-based lead parsing using Groq Llama
- Property matching and ranking
- Prompt injection detection
- Sensitive information protection
- Automated Lead Brief generation
- Realtor-focused recommendations and next actions

---

## Project Structure

```text
buyer-lead-intake-agent/
│
├── agents/
│   ├── lead_parser.py
│   ├── property_matcher.py
│   ├── validation_agent.py
│   └── brief_generator.py
│
├── data/
│   ├── miami_mls_listings.csv
│   └── sample_buyer_inquiries.json
│
├── outputs/
│   ├── LEAD-2026-001.md
│   ├── LEAD-2026-002.md
│   ├── ...
│   └── LEAD-2026-012.md
│
├── main.py
├── requirements.txt
├── README.md
└── explanation.md
```

---

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Running the Project

Generate Lead Briefs:

```bash
python3 main.py
```

Generated briefs will be saved in the `outputs/` directory.

---

## Tech Stack

- Python
- Pandas
- Groq API
- Llama 3
- python-dotenv

---

## Author

Nikhil Verma

Engineering Case Study Submission for AgentMira
