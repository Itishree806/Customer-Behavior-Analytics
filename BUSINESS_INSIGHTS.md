# Business Insights — Customer Behavior Analytics

## 1. Revenue is heavily concentrated in 3 categories
Clothing, Shoes, and Technology together generate ₺238.2M of the
₺251.5M total revenue (~95%), while the remaining 5 categories
(Cosmetics, Toys, Food & Beverage, Books, Souvenir) barely register.
Recommendation: inventory and marketing budget should weight
heavily toward these 3 categories.

## 2. Technology customers are low-volume but high-value
Average transaction value for Technology is ₺11,582, over 3x
Clothing's ₺3,306, despite having the fewest transactions (4,996)
of the top 3 categories. This customer group is a strong candidate
for premium loyalty programs rather than volume discounting.

## 3. Gender predicts transaction volume, not spend per visit
Female customers generated more total revenue (₺150M vs ₺101M), but
average spend per transaction is nearly identical (₺2,525 vs ₺2,534).
The revenue gap is driven entirely by more transactions from female
customers (59,482 vs 39,975), not by higher spending per visit.

## 4. The middle segment drives the most total revenue
K-Means segmentation into 4 value tiers shows "Regular Spenders"
(19,707 customers) generate ₺128.4M, 51% of total revenue more
than the "High-Value Shoppers" tier, despite lower average spend per
person. This is because total revenue depends on both spend level
and population size, and this middle tier has enough of both.
Recommendation: retention efforts for this segment may have the
largest overall revenue impact, not just the top-tier segment.

## 5. Two malls account for ~40% of all revenue
Mall of Istanbul and Kanyon each generate ~₺50M, while the bottom 5
malls each contribute under ₺13M. Useful for prioritizing
location-based marketing or inventory allocation.

## Methodology note: why K-Means instead of RFM
This dataset has exactly one transaction per customer_id (verified:
99,457 unique customers across 99,457 rows), so Frequency which is a core
RFM dimension cannot be computed. Segmentation was instead built
on total_amount, quantity, and age via K-Means clustering, which
answers the same underlying business question (customer value) using
signals this dataset actually supports.