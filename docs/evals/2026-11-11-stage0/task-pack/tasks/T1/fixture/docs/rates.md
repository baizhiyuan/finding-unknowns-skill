# Carrier rates
Billable kilograms are the greater of scale weight and volume in cm³ divided by 5000.
The published service table in shipping.py is authoritative for prices, transit days and zones.
For a 2 kg parcel measuring 50 × 40 × 40 cm the billable weight is 16 kg.
Costs use currency units with two decimal places, without tax.
If no service qualifies, emit an entry with status "unavailable" and a reason; never drop that parcel.
Output has a top-level "parcels" array, with one object per source id and status "selected" or "unavailable".
A selected object includes id, service, days and cost. Preserve input order.
The business may impose a transit limit or a preference between equally priced services; neither is set here.
