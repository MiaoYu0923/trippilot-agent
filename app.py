import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

try:
    from google import genai
except Exception:
    genai = None


st.set_page_config(
    page_title="TripPilot",
    page_icon="🧳",
    layout="wide"
)


def estimate_budget(budget_level: str) -> str:
    budget_map = {
        "Low": "Focus on free attractions, public transport, casual meals, and walking-friendly routes.",
        "Medium": "Balance paid attractions with free stops, include one comfortable meal, and use public transport.",
        "High": "Include premium experiences, flexible transport, reservations, and more comfortable food options."
    }
    return budget_map.get(
        budget_level,
        "Use a balanced travel budget with a mix of free and paid activities."
    )


def detect_schedule_risk(must_visit: str) -> str:
    places = [p.strip() for p in must_visit.split(",") if p.strip()]

    if len(places) >= 5:
        return "High risk: The schedule may be too packed. Add buffers and prioritize the top 3 places."
    elif len(places) >= 3:
        return "Medium risk: The plan is manageable, but transport and rest buffers are recommended."
    else:
        return "Low risk: The plan appears realistic for a one-day itinerary."


def generate_packing_checklist(constraints: str) -> list:
    base_items = [
        "Comfortable walking shoes",
        "Portable charger",
        "Reusable water bottle",
        "Light jacket or layer",
        "Digital or printed booking confirmations",
        "Bank card and small amount of cash",
        "Phone with offline map downloaded"
    ]

    lower_constraints = constraints.lower()

    if "rain" in lower_constraints or "weather" in lower_constraints:
        base_items.append("Compact umbrella or waterproof jacket")

    if "walk" in lower_constraints or "walking" in lower_constraints:
        base_items.append("Plan rest stops and avoid overloading the route")

    if "diet" in lower_constraints or "vegetarian" in lower_constraints or "halal" in lower_constraints:
        base_items.append("Pre-check food options that match dietary needs")

    return base_items


def create_rule_based_plan(
    destination,
    travel_date,
    start_time,
    end_time,
    budget,
    style,
    must_visit,
    constraints
):
    budget_note = estimate_budget(budget)
    risk_note = detect_schedule_risk(must_visit)
    packing_items = generate_packing_checklist(constraints)

    must_visit_list = [p.strip() for p in must_visit.split(",") if p.strip()]
    first_place = must_visit_list[0] if len(must_visit_list) > 0 else "main city landmark"
    second_place = must_visit_list[1] if len(must_visit_list) > 1 else "local cultural area"
    third_place = must_visit_list[2] if len(must_visit_list) > 2 else "scenic viewpoint or relaxed neighbourhood"

    plan = f"""
## 1. Trip Overview

**Destination:** {destination}  
**Date:** {travel_date}  
**Travel window:** {start_time} - {end_time}  
**Travel style:** {style}  
**Budget level:** {budget}  

TripPilot creates a structured one-day plan for organized travelers who want a realistic schedule, useful buffers, backup options, and clear reminders.

---

## 2. Hour-by-Hour Itinerary

**{start_time} - 10:00 | Arrival and breakfast / coffee buffer**  
Start calmly. Check transport, weather, tickets, and route before the main plan begins.

**10:00 - 11:30 | Visit: {first_place}**  
Make this the first major stop while your energy is high.

**11:30 - 12:00 | Transport and buffer time**  
Leave space for walking, queues, public transport, or navigation.

**12:00 - 13:30 | Visit: {second_place}**  
Choose a cultural, scenic, or local experience based on your travel style.

**13:30 - 14:30 | Lunch break**  
Pick somewhere close to the second stop to reduce unnecessary travel time.

**14:30 - 16:00 | Visit: {third_place}**  
Keep the afternoon flexible. If you feel tired, shorten this stop.

**16:00 - 16:30 | Rest / coffee / shopping buffer**  
A J-Mode pause to prevent the day from becoming too packed.

**16:30 - 18:00 | Flexible local experience**  
Choose one: museum, market, riverside walk, bookstore, gallery, or neighbourhood stroll.

**18:00 - {end_time} | Dinner and slow evening close**  
End with a relaxed dinner and check transport back to your accommodation.

---

## 3. Food and Break Suggestions

- Add a coffee break in the morning.
- Keep lunch close to the second stop.
- Avoid booking dinner too far from your final location.
- If the day involves lots of walking, add at least one seated break in the afternoon.

---

## 4. Estimated Budget Guidance

{budget_note}

Suggested categories:
- Transport
- Food and drinks
- Attractions
- Emergency buffer of 10-15%

---

## 5. Rainy Day / Disruption Backup Plan

If the weather is bad:
- Replace outdoor viewpoints with museums, galleries, covered markets, cafés, or bookstores.
- Keep indoor or pre-booked attractions.
- Reduce walking distance.
- Group nearby stops together.
- Add more transport buffer.

---

## 6. J-Mode Reservation and Risk Checklist

- Check whether tickets are needed for: {first_place}
- Add transport buffer before every major stop.
- Do not schedule more than 3 major attractions in one day.
- Save offline maps before leaving.
- Screenshot bookings and addresses.
- Check the last train or bus time before dinner.
- Schedule risk: {risk_note}

---

## 7. Packing Checklist

{chr(10).join([f"- {item}" for item in packing_items])}

---

## 8. Final Recommendation

Prioritize the top 2-3 must-visit places and treat everything else as optional. The best travel day is not the fullest one, but the one you can actually enjoy.
"""
    return plan


def generate_with_gemini(
    destination,
    travel_date,
    start_time,
    end_time,
    budget,
    style,
    must_visit,
    constraints
):
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key or genai is None:
        return create_rule_based_plan(
            destination,
            travel_date,
            start_time,
            end_time,
            budget,
            style,
            must_visit,
            constraints
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are TripPilot, an AI concierge travel planning agent for organized travelers.

Use four internal agent roles:
1. Preference Collector Agent
2. Itinerary Planner Agent
3. Risk and Backup Agent
4. Checklist Agent

User inputs:
- Destination: {destination}
- Travel date: {travel_date}
- Start time: {start_time}
- End time: {end_time}
- Budget level: {budget}
- Travel style: {style}
- Must-visit places: {must_visit}
- Constraints: {constraints}

Return the answer in this exact structure:

## 1. Trip Overview
## 2. Hour-by-Hour Itinerary
## 3. Food and Break Suggestions
## 4. Estimated Budget Guidance
## 5. Rainy Day / Disruption Backup Plan
## 6. J-Mode Reservation and Risk Checklist
## 7. Packing Checklist
## 8. Final Recommendation

Rules:
- Make the plan realistic.
- Include buffers.
- Do not overpack the schedule.
- Avoid asking for sensitive personal data.
- Do not make fake claims about live prices, opening hours, or availability.
- If exact live information is needed, tell the user to verify it before travel.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


st.title("🧳 TripPilot")
st.subheader("An AI Concierge Agent for Structured Travel Planning")

st.markdown(
    """
TripPilot helps organized travelers turn messy travel preferences into a structured one-day itinerary,
with time blocks, budget guidance, packing checklist, backup plans, and **J-Mode risk reminders**.
"""
)

with st.sidebar:
    st.header("About this project")
    st.markdown(
        """
**Capstone Track:** Concierge Agents

**Agent roles:**
- Preference Collector Agent
- Itinerary Planner Agent
- Risk & Backup Agent
- Checklist Agent

**Key concepts shown:**
- Multi-agent workflow
- Tool-style helper functions
- Security-conscious design
- Deployable Streamlit prototype
"""
    )

st.divider()

col1, col2 = st.columns(2)

with col1:
    destination = st.text_input("Destination", value="Edinburgh")
    travel_date = st.text_input("Travel date / season", value="October 2026")
    start_time = st.text_input("Start time", value="09:00")
    end_time = st.text_input("End time", value="20:00")

with col2:
    budget = st.selectbox("Budget level", ["Low", "Medium", "High"], index=1)
    style = st.multiselect(
        "Travel style",
        ["Relaxed", "Cultural", "Food-focused", "Nature", "Packed", "Scenic", "Shopping"],
        default=["Cultural", "Scenic", "Relaxed"]
    )
    must_visit = st.text_area(
        "Must-visit places",
        value="Edinburgh Castle, Victoria Street, Calton Hill"
    )
    constraints = st.text_area(
        "Constraints or preferences",
        value="Prefer not to walk too much, need coffee breaks, want a rainy day backup plan"
    )

style_text = ", ".join(style)

if st.button("Generate Travel Plan", type="primary"):
    if not destination.strip():
        st.warning("Please enter a destination.")
    else:
        with st.spinner("TripPilot agents are planning your day..."):
            result = generate_with_gemini(
                destination=destination,
                travel_date=travel_date,
                start_time=start_time,
                end_time=end_time,
                budget=budget,
                style=style_text,
                must_visit=must_visit,
                constraints=constraints
            )

        st.success("Your structured trip plan is ready.")
        st.markdown(result)

        st.download_button(
            label="Download travel plan as Markdown",
            data=result,
            file_name=f"trippilot_{destination.lower().replace(' ', '_')}_plan.md",
            mime="text/markdown"
        )
else:
    st.info("Fill in your travel preferences and click **Generate Travel Plan**.")