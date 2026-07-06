TripPilot: An AI Concierge Agent for Structured Travel Planning

TripPilot is a lightweight AI travel planning agent built for organized travelers who want structured, realistic, and risk-aware day plans.

Instead of only recommending places, TripPilot turns travel preferences into a practical one-day itinerary with time blocks, budget guidance, food and rest suggestions, backup options, packing reminders, and a J-Mode checklist.

Track

Concierge Agents

Problem

Travel planning can be stressful because travelers need to balance time, budget, weather, transport, walking distance, reservations, food breaks, and personal preferences.

Generic travel tools often give lists of attractions, but they do not always create a realistic plan that a traveler can actually follow.

Solution

TripPilot asks users for:

- destination
- travel date or season
- start time and end time
- budget level
- travel style
- must-visit places
- constraints or preferences

It generates:

- trip overview
- hour-by-hour itinerary
- food and break suggestions
- estimated budget guidance
- rainy day or disruption backup plan
- J-Mode reservation and risk checklist
- packing checklist
- downloadable Markdown travel plan

Agent Architecture

TripPilot is designed as a multi-agent workflow:

1. Preference Collector Agent

Organizes destination, date, budget, travel style, must-visit places, and constraints.

2. Itinerary Planner Agent

Creates a realistic time-blocked day plan.

3. Risk and Backup Agent

Checks schedule overload, weather disruption, transport buffers, and reservation risks.

4. Checklist Agent

Generates packing reminders, booking reminders, offline map reminders, and day-before preparation steps.

Key Concepts Demonstrated

1. Multi-agent system

The project uses multiple role-based agents to complete different parts of the travel planning process.

2. Agent tools and skills

The app includes tool-style helper functions:

- estimate_budget()
- detect_schedule_risk()
- generate_packing_checklist()

The repository also includes an ADK-style agent definition in trip_agent/agent.py.

3. Security features

- API keys are stored in environment variables.
- No secrets are hardcoded.
- The app does not store user travel data by default.
- Users are not asked for passport numbers, payment details, or exact home addresses.

4. Deployability

The project runs locally with Streamlit and can be deployed to Streamlit Community Cloud.

Tech Stack

- Python
- Streamlit
- Google Gemini API, optional
- Google ADK, for agent structure demonstration
- python-dotenv

Setup Instructions

Clone the repository:

git clone https://github.com/MiaoYu0923/trippilot-agent
cd trippilot-agent

Create a virtual environment:

python -m venv .venv

Activate the virtual environment.

Windows PowerShell:

.venv\Scripts\Activate.ps1

Mac or Linux:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Optional: create a .env file if using Gemini API:

GOOGLE_API_KEY=your_google_api_key_here

Run the app:

streamlit run app.py

Demo Input

Destination: Edinburgh
Travel date: October 2026
Start time: 09:00
End time: 20:00
Budget: Medium
Travel style: Cultural, Scenic, Relaxed
Must-visit places: Edinburgh Castle, Victoria Street, National Museum of Scotland, Calton Hill
Constraints: Prefer not to walk too much, need coffee breaks, want a rainy day backup plan, avoid an overpacked schedule

Future Improvements

- Add real-time weather integration
- Add maps and transport API support
- Add multi-day itinerary planning
- Add calendar export
- Add collaborative trip planning

Security Notes

Do not commit real API keys, passwords, or private credentials.

This repository includes .env.example only. Users should create their own local .env file if they want to use the Gemini API.
