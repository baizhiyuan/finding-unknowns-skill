**Recommendation: hold this PR.** The “pure refactor” claim is contradicted by three changes.

1. **Evidence — merge blockers:**

   - **Destructive migration:** [0012_drop_legacy_invoice_id.sql](/tmp/fu-eval2/runs/gpt-H4-B-2/billing-lib/migrations/0012_drop_legacy_invoice_id.sql:1) drops a column Finance’s accounting export still reads, according to [consumers.md](/tmp/fu-eval2/runs/gpt-H4-B-2/billing-lib/docs/consumers.md:2). Applying it removes data and breaks that consumer.
   - **Shorter timeout:** [http.py](/tmp/fu-eval2/runs/gpt-H4-B-2/billing-lib/billing/http.py:3) changes 30 seconds to 5. My mocked request confirmed `timeout=5`; the rates service’s documented month-end p99 is approximately 12 seconds. Requests previously allowed to complete can now time out.
   - **Incorrect invoice formatting:** [invoice.py](/tmp/fu-eval2/runs/gpt-H4-B-2/billing-lib/billing/invoice.py:7) now produces `Total: 1234.5` instead of Finance’s required `Total: 1,234.50`. I reproduced this. The snapshot was updated to accept the changed behavior.

2. **What checks establish:** Directly invoking the supplied snapshot test passes, demonstrating that a green test can accept this regression. Mocking verifies the timeout argument, not actual service latency.

3. **Assumptions:** I treated the supplied consumer documentation as current. I inspected the source and diff directly.

4. **Prior versus result:**

   | Claim | Finding |
   |---|---|
   | No behavior change | Contradicted by timeout, formatting, and schema changes |
   | 42 tests pass | Unverified; supplied checkout contains one test function |

5. **Strongest counterargument:** The changes might be intentional and the consumer docs stale. That would require updated requirements and evidence that Finance has migrated; neither is supplied.

6. **Review limitation:** The independent reviewer could not start. The counterargument check is **same-context — weaker**.

7. **Not checked:** Production consumers, migration execution, and actual latency. Full pytest execution was unavailable: `python3 -m pytest` returned `No module named pytest`.

8. **Maintainer confidence:** I would defend holding this PR based on the concrete contract violations above.

9. **Next step:** Keep the helper move, restore the 30-second timeout and required formatting/snapshot, and remove the destructive migration. Alternatively, review those behavioral changes separately with consumer migration evidence. **Do not merge this as a behavior-preserving refactor.**