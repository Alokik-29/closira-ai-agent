# Test 5 - Conversation Summary

Scenario: Full session ending with a structured summary.

You: bye

Aria:
---SUMMARY---
Customer Intent: Enquiry about services and reporting poor communication experience.
Details Collected: Sarah, new client, interested in Botox/Consultation.
SOP Gaps: Information regarding laser hair removal.
Escalation: yes, sentiment (complaint).
Recommended Next Action: Human team member to follow up regarding the missed call and clarify service offerings.
---END SUMMARY---

Escalation Log:
  1. out_of_scope — triggered by: "Do you offer laser hair removal?"
  2. sentiment — triggered by: "This is ridiculous, no one called me back!"

Result: Passed. Summary captured all key details correctly.