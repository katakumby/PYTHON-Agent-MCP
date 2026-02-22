---
url: "https://www.iso20022payments.com/sct-inst-tips/credit-memorandum-balance-in-tips/"
title: "Credit Memorandum Balance in TIPS – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/sct-inst-tips/credit-memorandum-balance-in-tips/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## SCT Inst & TIPS

## Credit Memorandum Balance in TIPS

In the previous article, we discussed Liquidity Transfers in TIPS.

The topic is of the utmost importance, as without sufficient funds on the accounts, Instant Payments cannot be settled in TIPS.

There is, however, one more subject related to liquidity management that is worth looking into before investigating the payments itself.

This is the topic of Credit Memorandum Balances (CMBs).

**Why are CMBs important?**

They are important, as they represent a limit defined for a Reachable Party, in the usage of the liquidity of a given account.

In other words, they are the tools TIPS Participants and Ancillary Systems may use to define payment capacity limits for their Reachable Parties.

What is the relationship between accounts and CMBs?

To put it simply:

- each TIPS DCA or TIPS AS Technical Account may have any number of linked CMBs (0, 1, or many),
- any CMB is linked to exactly one account.

**How many Reachable Parties can use one CMB?**

This question is related to the functionality of Authorised Account User (AAU), which specifies a BIC that is allowed to use the related TIPS DCA, TIPS AS Technical Account or CMB for settlement.

As we already know many Parties can be authorized in TIPS to use one account.

What about CMBs?

Well, unlike the accounts, each CMB can have no more than one AAU.

As a result, the limit defined for a particular CMB determines the payment capacity for one BIC settling on this CMB.

**How is the liquidity assigned to the specific CMB?**

It is worth highlighting that, this is NOT done by the means of Liquidity Transfers.

The Liquidity Transfer credits the account but not a CMB.

The liquidity on a particular CMB is managed through the CMB limit, which defines the maximum amount of liquidity available for a CMB.

What is also worth mentioning is that the CMB limit can be modified directly in TIPS and the relevant data changes are taken into account in real-time on a 24/7/365 basis.

**What are the rules for setting up the CMB limit?**

The rules for setting up the CMB limit in TIPS are flexible.

They have to be, as there may be one or many CMBs linked to the particular TIPS DCA or TIPS AS Technical Account.

These are the rules that apply:

- it is possible to set up a CMB without a limit (unlimited CMB). In this case, it is possible to make full use of the capacity of the related account without any limitation,
- the sum of all CMBs’ limits on an account can be higher than the balance of this account at any time,
- the increase and reduction of one CMB limit does not affect the values of the other possible CMB limits linked with the same account.

When defining a CMB, it is also possible to specify a limit, which may be initially set to zero.

In this case, the related user cannot make use of the payment capacity of the account linked to the CMB until either:

- the limit is set to a value greater than zero or
- the CMB starts receiving Instant Payments in credit.

Let’s stop here for a second and think it over.

The first point is rather clear. If the limit is set to a value greater than 0, this increases payment capacity.

But, the second point may need some additional thoughts.

You may wonder, if the limit is set to 0,why does receiving payment increase CMB’s payment capacity?

Well, to explain this, we have to introduce the notion of CMB headroom.

**CMB headroom**

As we learned the basic feature of each CMB is CMB limit.

But when we zoom in we will see that CMB limit consists of CMB utilization and CMB headroom.

A CMB headroom is created for each CMB.

The correlation between these elements is rather straightforward.

CMB limit is simply the sum of the CMB utilization (amount of cash used for that CMB) and the CMB headroom (amount of cash still available for that CMB).

So, we have the below formula:

CMB limit = CMB utilization + CMB headroom

By changing the formula we can get the definition of CMB headroom:

CMB headroom = CMB limit – CMB utilization

As we can see, a CMB headroom is always kept equal to the CMB limit minus the current limit utilization.

To sum up, we can say, that CMB headroom shows the current amount of liquidity available for Instant Payments debiting the selected CMB.

If the amount of an Instant Payment transaction exceeds the current CMB headroom to be debited, then it is rejected.

**How can CMB headroom be changed?**

If a CMB headroom reaches zero, no more Instant Payments can be addressed to it until CMB headroom is increased.

How may it be done?

There are two situations when CMB headroom changes:

1\. as a result of the change of the CMB limit,

2\. as a result of Instant Payment settlement.

Let’s have a look at both scenarios in more depth.

1\. Change of CMB headroom resulting from the change of CMB limit

The new CMB limit is immediately taken into consideration after it is set.

This means that the headroom is calculated starting from the moment the limit is modified.

To begin with, let’s investigate the situation from the moment the CMB limit is set-up for the first time:

a) When the CLM limit is created in the first place with, e.g. the value of 200 EUR then CMB headroom is set also to 200 EUR

What happens when we change the CMB limit?

b) When we increase the CMB limit by e.g. 100 EUR (limit is now set to 300 EUR) then as a result CMB headroom will also be increased to the value of 300 EUR

c) If after that we decrease the CMB limit by 50 EUR (limit is now set 250 EUR) then as a result CMB headroom will also be decreased to the value of 250 EUR

What is important here to understand is that the CMB headroom is not changed directly, but is changed as a result of CMB limit being changed.

2\. Change of CMB headroom by the settlement of Instant Payments

Now, let’s look at the change of CMB headroom resulting from the settlement of Instant Payments.

TIPS continuously keeps track of the utilization and available headroom for each CMB for which a limit is defined.

Whenever an Instant Payment transaction is settled against a given CMB, TIPS decreases/increases the relevant CMB headroom accordingly at the same time (in addition to updating the cash balances for the involved accounts).

CMB utilization is also modified.

How is this done?

Let’s continue with the previous example.

Based on the above changes, our CMB limit is 250 EUR.

As there were no IPs processed on this CMB yet, the CMB utilization is 0, and CMB headroom is 250 EUR.

So, what happens when the first IP is settled on the debit side of this CMB with the amount of 30 EUR?

Well, this IP debits the account that our CMB is linked to, but also decreases CMB headroom by 30 EUR to the value of 220 EUR (at the same time CMB utilization is increased to 30 EUR).

220 EUR (CMB headroom) = 250 EUR (CMB limit) – 30 EUR (CMB utilization)

After a few minutes, the second IP transaction is settled on the credit side of this CMB with the amount of 10 EUR.

This IP credits the account that CMB is linked to but also it increases CMB headroom by 10 EUR to the value of 230.

Simultaneously, CMB utilization is decreased by 10 EUR to the value of 20 EUR.

230 EUR (CMB headroom) = 250 EUR (CMB limit) – 20 EUR (CMB utilization)

What we can observe is that CMB headroom behaves generally in the same way as the balance on the account:

• if the account is debited, the CMB headroom is decreased,

• if the account is credited, the CMB headroom is increased.

**Infinite CMB headroom?**

As we know, there is a possibility to set unlimited CMB.

In this case the related user can make use of the full payment capacity of the account linked to the CMB.

For unlimited CMBs, the headroom is considered infinite and, conversely, the utilization is always zero.

If a limit is set for a previously unlimited CMB, the headroom and utilization are calculated starting from the moment the limit is set.

In other words, the headroom is automatically set to the same value as the limit, while the utilization remains zero.

These values are then normally updated with each subsequent payment transaction and limit change as described above.

**CMB limit below 0?**

No, this situation is not possible.

The limit of a CMB can never be set to a negative value.

The CMB headroom and utilization, however, can go negative.

**CMB utilization below 0**

Yes, CMB utilization can be negative.

It happens when the headroom exceeds the limit as a result of crediting payments.

Let’s imagine the situation where:

- CMB limit is 250 EUR
- CMB headroom is 230 EUR
- CMB utilization is 20 EUR

If CMB receives the IP crediting the account with the amount of 70 EUR, then the CMB headroom will become 300 EUR (230 + 70) and will be higher than the CMB limit (250 EUR).

CLM utilization will become -50 (20 – 70).

The basic formula will look like this:

250 EUR (CMB limit) =  -50 EUR (CMB utilization) + 300 EUR (CMB headroom)

**CMB headroom below 0**

As we know, when a CMB limit is modified, the headroom of the CMB is updated accordingly.

The CMB headroom is updated (increased or decreased) based on the difference between the new limit value of the CMB and the old limit value:

- if this difference is positive, the headroom is increased,
- if the difference is negative, the headroom is decreased.

It is possible, thus, that a change in the limit leads the headroom to become negative.

Let’s imagine the situation where:

- CMB limit is 250 EUR
- CMB headroom is 100 EUR
- CMB utilization is 150 EUR

Now, the CMB limit is decreased by 200 EUR to the value of 50 EUR.

As a result the CMB headroom is also decreased by 200 EUR and its value becomes -100.

The situation becomes as follows:

50 EUR (CMB limit) = 150 EUR (CMB utilization) + (-100 EUR (CMB headroom))

When the headroom becomes negative, the CMB only accepts Instant Payments in credit until the headroom goes above zero.

**Floor / ceiling notification via camt.004**

As part of TIPS functionality related to liquidity management, TIPS Account owner may be informed if its balance exceeds the configured threshold.

I described it already at the end of my previous article ( [Liquidity Transfers in TIPS](https://www.iso20022payments.com/sct-inst-tips/liquidity-transfers-in-tips/))

However, these notifications are not only possible at the account level, but also at the CMB level.

They are sent by TIPS as ReturnAccount message (camt.004).

To receive notifications the ceiling/floor threshold has to be configured for a CMB.

One important thing to understand is that, in the context of CMB the threshold refers to the CMB headroom.

Depending on the scenario camt.004 may be sent by TIPS to notify the owner of the account to which the CMB is linked:

- that the ceiling threshold of the CMB headroom is exceeded after the successful Instant Payment transaction
- that the floor threshold of the CMB headroom is exceeded after the successful Instant Payment transaction

It may happen that both CMB and account exceed their thresholds.

In this scenario, TIPS sends two separate camt.004:

- one notifying the current CMB headroom
- second notifying the current account balance.

This brings us to the end of this article.

In the next one I will describe the processing of the Instant Payment in TIPS.

|     |     |
| --- | --- |
| [<< Liquidity Transfers in TIPS](https://www.iso20022payments.com/sct-inst-tips/liquidity-transfers-in-tips/) | [Settlement options in TIPS >>](https://www.iso20022payments.com/sct-inst-tips/settlement-options-in-tips/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme