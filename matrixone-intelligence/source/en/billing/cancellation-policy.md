# Cancellation policy

Cancellation only applies to pre-paid (subscription / annual & monthly) instances. If your business no longer needs a subscription instance, you can cancel it. Read this policy carefully before you cancel — MOC refunds you according to the rules below. Pay-as-you-go (post-pay) instances are not subject to cancellation; you can stop billing on them by terminating the instance directly in the instance management console.

# Rules

You can cancel a Standard subscription instance at any time. After cancellation, instance data is retained for 7 days, then permanently deleted. Within those 7 days you can recover the instance by renewing it from the terminated-instance list.

When you cancel, the cash portion is refunded first: any unused cash is returned to your account balance. Any coupons used are not refundable. For example, if you used a coupon worth 100 RMB and 50 RMB of it was actually applied, none of the coupon balance is refunded or converted to cash on cancellation. In other words, once a coupon is applied to a payment it is consumed and has no cash value at refund time. Plan accordingly when paying with coupons.

# Refund amount

We handle refunds in two cases:

- Cash actually paid for the instance > amount already consumed: refund = cash actually paid - amount already consumed.

- Cash actually paid for the instance ≤ amount already consumed (i.e. coupons covered part of it): refund = 0.

The "amount already consumed" is calculated as:

**Amount consumed = (years used × 12 × monthly unit price × discount for the years used + months used × monthly unit price × discount for the months used + days used × daily unit price) × surcharge factor**

- Years used: 0 if less than a full year.
- Monthly unit price: the monthly list price of the current configuration.
- Months used: any whole months not making up a full year; 0 if less than a full month.
- Days used: any time not making up a full month; partial days count as full days.
- Daily unit price: monthly list price / 30.
- Surcharge factor:
    - Used time < 30 days: factor = 1.5.
    - Used time ≥ 30 days: factor = 1.

For example, if the annual discount is 0.51 and the monthly discount is 0.7, and the instance has been used for 1 year, 1 month, and 3 days:

amount consumed = (1 × 12 × monthly unit price × 0.51 + 3 × monthly unit price × 1 × 0.7 + 3 × daily unit price) × 1
