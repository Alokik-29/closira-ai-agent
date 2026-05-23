import json
from anthropic import Anthropic

client = Anthropic()

# load SOP from file
def load_sop(path="sop.json"):
    with open(path) as f:
        return json.load(f)

SOP = load_sop()
SOP_TEXT = json.dumps(SOP, indent=2)

SYSTEM_PROMPT = f"""You are Aria, a friendly customer support assistant for {SOP["business_name"]}.

You handle conversations in four stages:
  Stage 1 - FAQ: Answer questions using only the SOP data below.
  Stage 2 - Lead Qualification: Ask 2-3 questions to learn about the customer.
  Stage 3 - Escalation: Hand off to a human when needed.
  Stage 4 - Summary: Summarise the session when it ends.

SOP DATA:
{SOP_TEXT}

RULES:
1. Only answer from the SOP. Never make up prices, services, or policies.
2. If something is not in the SOP, say: "I don't have that information — let me connect you with our team." Then write: [ESCALATE: out_of_scope]
3. If the customer is angry or complaining, empathise briefly then write: [ESCALATE: sentiment]
4. If the customer asks for a human, write: [ESCALATE: customer_request]
5. If you are not confident in your answer, write: [ESCALATE: low_confidence]
6. If 2 questions in a row go unanswered, write: [ESCALATE: too_many_unanswered]
7. Never negotiate prices. Say prices are fixed, then write: [ESCALATE: pricing_negotiation]
8. Keep replies short, warm and professional.

LEAD QUALIFICATION:
After answering initial questions, collect these naturally:
  - Customer name
  - New or returning client
  - Which service they are interested in

ESCALATION TAG FORMAT:
Always write the tag on its own line: [ESCALATE: reason]
Valid reasons: out_of_scope | sentiment | customer_request | low_confidence | too_many_unanswered | pricing_negotiation | medical_question

SESSION SUMMARY:
When the user says bye, done, or end session, output this exact format:
---SUMMARY---
Customer Intent: ...
Details Collected: ...
SOP Gaps: ...
Escalation: yes/no and reason
Recommended Next Action: ...
---END SUMMARY---
"""

# track conversation and escalations
conversation_history = []
escalation_log = []

def check_escalation(text):
    if "[ESCALATE:" not in text:
        return None
    start = text.index("[ESCALATE:") + len("[ESCALATE:")
    end = text.index("]", start)
    return text[start:end].strip()

def log_escalation(reason, user_msg):
    escalation_log.append({"reason": reason, "triggered_by": user_msg})
    print(f"\n[ESCALATION] Reason: {reason}")
    print("Handing off to human agent...\n")

def chat(user_message):
    conversation_history.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=conversation_history,
    )

    reply = response.content[0].text
    conversation_history.append({"role": "assistant", "content": reply})

    # check if AI flagged an escalation
    reason = check_escalation(reply)
    if reason:
        log_escalation(reason, user_message)

    return reply

END_PHRASES = {"bye", "done", "end session", "goodbye", "exit", "quit"}

def main():
    print("Bloom Aesthetics Clinic - AI Support")
    print("Type 'bye' or 'end session' to finish.\n")

    # send a silent opening message to get the greeting
    greeting = chat("Hello, I'd like some information please.")
    print(f"Aria: {greeting}\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() in END_PHRASES:
            summary = chat("end session")
            print(f"\nAria: {summary}\n")
            break

        reply = chat(user_input)

        # strip the escalation tag before showing to customer
        display = reply.replace("[ESCALATE:", "").replace("]", "") if "[ESCALATE:" in reply else reply
        print(f"\nAria: {display}\n")

    # print escalation log at the end
    if escalation_log:
        print("\nEscalation Log:")
        for i, entry in enumerate(escalation_log, 1):
            print(f"  {i}. {entry['reason']} — triggered by: \"{entry['triggered_by']}\"")
    else:
        print("No escalations this session.")

if __name__ == "__main__":
    main()
