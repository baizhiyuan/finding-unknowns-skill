# Amount display
Amounts are stored as signed integer cents in USD.
A charge of 125 cents must render as $1.25.
A credit of -125 cents must render as -$1.25; the minus sign is required so customers can distinguish refunds from charges.
Zero renders as $0.00. No locale-specific formatting is used.
