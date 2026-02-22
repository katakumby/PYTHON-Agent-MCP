---
url: "https://www.iso20022payments.com/miscellaneous/t-account-and-wash-account/"
title: "T-account and Wash account – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/miscellaneous/t-account-and-wash-account/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## Miscellaneous

## T-account and Wash account

In this article, I would like to briefly present the bookings on T-accounts and Wash accounts.

**T-accounts**

As not all of the readers may be familiar with double-entry accounting represented on T-accounts, in many sections of my website I use the simplified illustration of booking entries. It still seems important, however, to illustrate how bookings would look on T-accounts. This is the purpose of this section.

What is a T-account?

A T-account is a term used in the context of double-entry bookkeeping.

It is called a T-account because the bookkeeping entries are laid out in a way that resembles a T-shape.

This is what the T-account looks like:

![](https://www.iso20022payments.com/wp-content/uploads/2023/01/T-account-300x244.jpg)

As you can seedebits are listed on the left and credits are recorded on the right.

But we can still ask what a debit or a credit mean in the context of the account that banks hold.

So, when the account is debited it means that the balance on the account decreases. As a consequence, if you are Debtor funds are taken from your account.

On the other hand, when the account is credited it means that the balance on the account increases. If you are Creditor, you receive funds on your account.

Additionally, a very important notion is the rule according to which to record every transaction, there will be two accounting entries needed:

- one account will get a debit entry and
- the second one will get a credit entry.

This is to ensure that the total sum of debits is equal to the total sum of credits.

How about having a look at an example?

Let’s say that Bank A sends the Credit transfer to Bank B.

We can illustrate the bookings with T-accounts in the following way:

![](https://www.iso20022payments.com/wp-content/uploads/2023/01/T-account-transfer-1.jpg)

Needless to say, in the above example, we do not consider any currencies, charges, etc.

What we can see, however, is that in both banks there is one entry on the debit side and one entry on the credit side. In both banks amount debited is equal to the amount credited.

What is additionally worth noticing is that, if the Mirror Nostro is credited then the actual Nostro in a correspondent bank is debited and vice versa. Mirror Nostro is used to reflect the status/balance of the Nostro account.

Between Bank A and Bank B, we can see an arrow symbolizing a payment message. And what is written above the arrow may be easily overlooked, but in fact, is very important.

The above example refers to **Credit transfer**.

In Credit transfer, the direction of the message is the same as the direction of the funds: from Debtor to Creditor.

We can see that message arrow points from the left to the right.

The same is the direction of the bookings in Bank A and in Bank B.

Bank A sends the message as Debtor Agent to Bank B which is Creditor Agent.

Why Bank A sends this message?

It does so on behalf of its customer. The Debtor initiates the transfer and Debtor Agent pushes funds toward Creditor Agent.

This is why Credit transfer is an example of **push transfer**.

The opposite situation we are going to have in the case of **Direct debit**.

In the case of Direct debit, it is Creditor that initiates the transfer. It’s a **pull transfer**. The Creditor Agent pulls the funds.

The direction of the message is from Creditor to Debtor, but the direction of the funds will be from Debtor toward Creditor.

Of course in the case of Direct debit, the bookings will look different, however, the logic still is the same: debits on the left, credits on the right.

**Wash accounts**

As you certainly know, accounting rules differ among banks.

One of the differences is that some banks may use additional temporary accounts, like **W** **ash accounts** during the processing flow.

Temporary accounts are zero-balance accounts. It means that after all the transactions are finalized these accounts should not have any debit or credit balance. You always take out the same amount that you put in.

There are many benefits of using Wash accounts.

In this section, I would like to complement the above example with only one scenario.

What I have in mind is a Customer payment sent with Cover method.

As you may know, Cover method decouples the settlement from the payment information. There are two messages sent:

- one is an announcement with information concerning payment details
- second is the cover payment which moves the funds

So, let’s say that Bank B from the example above is going to receive the payment sent with Cover method.

When should Bank B perform bookings?

Of course, it may be that when Bank B receives an announcement it decides to wait for the arrival of the respective funds before doing any bookings.

But sometimes Bank B may decide that it will book the Creditor without waiting for the funds. The bookings will be carried out upon receiving the announcement. This may be because Bank B trusts the banks involved in the transfer.

What will these first bookings based on the announcement look like?

In such a case Bank B will credit the Creditor.

But, what account will be debited?

Bank B will not want to debit Bank A’s Nostro Account because the funds have not arrived yet.

We can see already, that Bank B will need a temporary account to perform the bookings.

Bank B is going to use a dedicated Wash account.

This will be done as follows:

![](https://www.iso20022payments.com/wp-content/uploads/2023/01/Announcement.jpg)

We can see that in that case the credit side of the transaction is decoupled from the debit side.

To perform bookings only on the Credit side of the transaction a temporary account is needed.

And what will happen when the funds finally arrive?

When the Cover payment arrives the second booking will be conducted:

![](https://www.iso20022payments.com/wp-content/uploads/2023/01/cover.jpg)

This second booking takes care of the debit side of the transaction.

Nostro account of Bank A is debited, and Wash account is credited.

After this second booking, the Wash account is correctly balanced.

As a temporary account, the Wash account is a 0-balance account.

And precisely, after this second booking, there is no debit or credit balance on this account.

|     |     |
| --- | --- |
| [<< ISO 20022 market implementations](https://www.iso20022payments.com/miscellaneous/iso-20022-market-implementations/) | [Legal Entity Identifier (LEI) >>](https://www.iso20022payments.com/miscellaneous/legal-entity-identifier-lei/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme