# Prompt Design

## System Prompt

The full system prompt is in `main.py` inside the `SYSTEM_PROMPT` variable. It tells the AI to act as Aria, a support assistant for Bloom Aesthetics Clinic.

---

## Why I Made These Choices

### Persona and Tone
I gave the assistant a name (Aria) and kept the tone short and warm. The replies are written for WhatsApp-style chat, so no long paragraphs.

### SOP Grounding
I pasted the full SOP as a JSON block inside the system prompt. The model has one source of truth and is told not to answer anything outside it.

### Hallucination Prevention
The prompt has two explicit rules:
- Never make up prices, services, or policies
- If a question is not in the SOP, admit it and escalate instead of guessing

This way the model fails safely rather than inventing answers.

### Escalation Detection
I used output tags like `[ESCALATE: reason]` instead of confidence scores. This is simpler to parse and the reason is logged automatically. The tag is stripped before the customer sees the reply.

### Lead Qualification
After the first question is answered, Aria collects three things naturally in conversation: customer name, new or returning, and which service they want. It feels like a chat, not a form.

### Session Summary
The summary has fixed headings so it can be read or parsed easily. It covers what the customer wanted, what was collected, any gaps in the SOP, whether there was an escalation, and what to do next.

---

## Escalation Triggers

| Trigger | Reason Tag |
|---|---|
| Question not in SOP | out_of_scope |
| Customer is angry or complaining | sentiment |
| Customer asks for a human | customer_request |
| Model is not confident | low_confidence |
| Two questions unanswered in a row | too_many_unanswered |
| Customer tries to negotiate price | pricing_negotiation |
| Medical question asked | medical_question |

---

## Limitations

- No memory between sessions, each run starts fresh
- Escalation depends on the model following instructions, it may miss subtle tone sometimes
- The SOP is small and would need expanding for a real business