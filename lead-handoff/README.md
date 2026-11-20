# Lead handoff playbook

A print shop receives an inquiry at 16:50 on Friday. The person who usually handles it is away. Before you connect any automation, see whether two teammates using your rules independently assign the same owner and reply deadline.

## Set the rules

1. Copy the [worksheet](worksheet.csv). Choose your team’s time zone, working hours, holidays, primary owner, backup and the queue owner who handles exceptions.
2. For this fictional shop, coverage is Monday through Friday, 09:00 to 17:00 local time. Acknowledge ownership within 30 working minutes. Send a first reply within two working hours of receipt. Pause both clocks outside coverage.
3. Assign the available primary or backup. If neither is available, alert the queue owner. At the acknowledgment deadline, an unclaimed item goes to the backup or queue owner. Carry the original reply deadline through reassignment.
4. Record one item per source event ID. On exact replay, log receipt against the existing item. If different event IDs look like the same person, send them to a human for review before merging anything.

## Rehearse the handoff

Assume an ordinary week with no closures. Use one copy of the worksheet per run.

| Input | Expected result |
| --- | --- |
| Event P41 arrives Friday at 16:50. Primary away, backup on duty. | Backup owns it. Ten working minutes elapse Friday. Acknowledgment is due Monday at 09:20 and first reply at 10:50. |
| Event P41 arrives again at 16:52. | Record the replay on P41. One inquiry, one owner and the original deadlines. |
| Event P42 arrives with a similar name and a different request. | Retain both event IDs. A person decides whether the requests belong together. |
| Event P43 arrives Monday at 10:00. Primary receives it but has not acknowledged at 10:30. | Route to the backup or queue owner at 10:30. First reply is still due at 12:00. |

Record the actual owner and due time beside each expected result. If the two teammates disagree, revise the rule that allowed both interpretations and repeat that case. In a CRM, rehearse with fictional records and outbound messaging switched off.
