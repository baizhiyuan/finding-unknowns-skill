# Invoice totals
The ledger rounds each extended line to cents with Decimal ROUND_HALF_UP, then sums the rounded lines.
Three separate lines at 0.335 each total 1.02 under the ledger rule; rounding only the final sum gives 1.01.
Negative quantities represent credits, and must retain their sign in every calculation.
All source amounts are net values; this exporter does not calculate or add tax.
The export is JSON containing "invoices", each with id, total and a "lines" array.
Each exported line includes item and amount; tax_class may also be shown. Currency formatting is a caller choice.
Group by invoice id, preserve source line order, and sort invoices by id.
The existing total(rows) API returns Decimal and must remain compatible.
