# Configuration change

If a Standard Instance is over- or under-provisioned for your workload, you can resize it by changing the number and size of compute nodes.

# Rules

Click **Resize** on the instance page to start. When the resize starts, the system generates a new bill: the cash portion of the previous bill is deducted first; if there is a refund, the remainder is returned to your account balance. Coupons that have already been used are not refundable. After you submit, the instance shows a "Resizing" badge — typically a few minutes to complete.

# Billing

For pay-as-you-go (post-pay) instances there is no refund or extra payment on resize: the next hour's charge is calculated by the second based on when the resize happened. The rest of this section explains billing for resizes on subscription (annual / monthly) instances.

The billing rules cover these cases:

|  Case  | Billing rule |
|  ----  | ----  |
| Increase node spec only / increase node count only / increase both | Top-up = (new monthly list price - old monthly list price) / 30 / 24 × remaining subscription time |
| Decrease node spec only / decrease node count only / decrease both | <ol><li>Cash actually paid for the instance > amount already consumed: refund = (cash actually paid - amount already consumed) × old/new spec ratio</li><li>Cash actually paid for the instance ≤ amount already consumed (i.e. coupons covered part of it): refund = 0</li></ol><li>Old/new spec ratio = (old list price - new list price) / old list price</li> |
| Increase node spec and decrease node count | Compute the top-up using rule 1, compute the refund using rule 2, and net the two to get the final amount. |
| Decrease node spec and increase node count | Compute the refund using rule 2, compute the top-up using rule 1, and net the two to get the final amount. |

For the meaning of "amount already consumed" and the surcharge factor, see the refund-amount calculation in the [Cancellation policy](cancellation-policy.md).
