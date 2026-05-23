# Closira AI Agent — Intern Assignment

A Python-based AI customer support workflow built for Bloom Aesthetics Clinic. The assistant handles inbound customer questions, qualifies leads, detects escalations, and summarises conversations.

---

## What It Does

- Answers customer questions using a business SOP file
- Asks 2-3 questions to qualify the lead
- Detects when to hand off to a human agent
- Produces a structured summary at the end of each session

---

## Project Structure

- main.py — main workflow
- sop.json — business SOP data
- prompt_design.md — prompt decisions and escalation logic
- requirements.txt — dependencies
- .env — API key (not uploaded to GitHub)
- test_transcripts/ — sample conversations for each scenario

---

## Install Dependencies

Run this in your terminal:

    pip install google-genai python-dotenv

---

## Add Your API Key

Create a .env file in the root folder and add:

    GOOGLE_API_KEY=your_key_here

---

## Run

    python main.py

Type bye or end session to finish the conversation and see the summary.

---

## Trade-offs and Limitations

- No memory between sessions, each run starts fresh
- Escalation relies on the model following prompt instructions consistently
- SOP is kept small for this demo but can be expanded
- No frontend, runs entirely in the terminal