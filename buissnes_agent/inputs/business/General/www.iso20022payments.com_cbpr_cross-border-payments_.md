---
url: "https://www.iso20022payments.com/cbpr/cross-border-payments/"
title: "Cross-border payments – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/cbpr/cross-border-payments/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## CBPR+

## Cross-border payments

In this section, I would like to remind us of some basic notions related to cross-border payments. It will not be a comprehensive introduction to this topic as I assume you have experience in the payments industry.

What I would like to do is to highlight the most important rules based on which cross-border payments are processed.

**O** **ne of the crucial aspects related to payments is settlement.**

Usually, this term is explained in the context of net or gross settlement and is placed as the next step in the process of netting and clearing. However, these are not so important for CBPR+ payments. I will get back to the above aspects when investigating TARGET system (gross settlement) and SEPA payments (netting and clearing). For the time being, I would like to stick to the meaning of settlement for CBPR+ payments.

First of all, it’s key to understand that settlement of payment is not related to the customer’s perspective. So, we cannot say, that the settlement is achieved when the creditor receives funds. It rather determines the payment’s status from an interbank perspective.**The settlement marks the completion of a transaction between banks\*. In other words, in the interbank space, settlement means that the aim of the payment is achieved. The obligation between banks is discharged.** If you are not familiar with this term, you can simply understand it as **the moment the payment between banks is done.**

And why do I start by focusing on interbank relations?

I do so because the CBPR+ rules regulate precisely the bank-to-bank space with customer-to-bank space being out of the scope of CBPR+.

\\* I could use here the term ‘Financial Institution (FI)’ which is a broader one, but I think using the term ‘Bank’ will make the article easier to digest.

**Mystery of settlement**

To investigate this topic further we may ask who is responsible for settlement?

To begin with, let us clarify that it is not SWIFT that is responsible for settlement. When we are talking about payments, SWIFT is mainly responsible for the communication layer. However, SWIFT is not a payment system. It does not hold any accounts for banks nor perform any bookings.

SWIFT conveysmessages from one party to another. So consequently, if we already know that SWIFT does not perform settlement, we can guess that the moment of settlement is not related to the payment message itself. In other words, settlement cannot be defined as a moment when a payment message from one bank arrives at another bank.

Let’s explore this issue further by answering the below question.

**Where the settlement is done?**

**The settlement is done on the accounts.** When the payment message is exchanged between two banks, the settlement is not done somewhere in the middle. No, the settlement is done by bookings on the accounts.

And this information helps to finally identify institutions responsible for settlement.

**So, who performs settlement?**

If the settlement is done on the accounts, it is performed by banks.

It may be done between two commercial banks as a result of the payment message exchanged between them, or it may be done in the books of a Central Bank, for example in an RTGS system operated by a Central Bank.

Let’s carry on our analysis by investigating this second scenario first.

**Settlement in the RTGS system**

While investigating settlement in an RTGS system, I will use an example of TARGET system.

In a nutshell, TARGET is an RTGS System in Europe. I will provide more details about TARGET in a dedicated section of my website.

So, how the settlement in an RTGS system looks like?

Below is a diagram from [TARGET documentation](https://www.ecb.europa.eu/paym/target/consolidation/profuse/shared/pdf/RTGS_UDFS_v3.0_clean_221014.en.pdf "RTGS UDFS").

![](https://iso20022payments.com/wp-content/uploads/2022/12/TARGET_Settlement.jpg)

Based on: T2 User Detailed Functional Specifications v3.0 – Real-time Gross Settlement System (RTGS), Figure 21

As we can see, there are two TARGET participants in the picture: Bank A and Bank B. They both hold accounts in TARGET system.

The payment is done from Bank A to Bank B.

So, the first thing we can notice is that **the settlement is done in RTGS system on the accounts that participants hold in this system.**These accounts are maintained by Central Banks. In other words, to open such accounts banks sign agreements with their Central Banks.

What countries are these participants from?

The original figure from TARGET documentation does not determine that. They may be both from one country, or they may be from two different countries. If the banks were from the same country we can easily understand that it would be a domestic payment.

But what if Bank A and Bank B were from different countries, for example, France and Germany? I added two flags in the diagram to indicate these two countries.

**Is the above payment between participants in France and Germany a cross-border payment?**

In the context of TARGET system it may be regarded as cross-border as it involves two counties. You may read about TARGET perspective in section 1.12 Share of inter-Member State traffic of [TARGET Annual Report 2021](https://www.ecb.europa.eu/pub/pdf/targetar/ecb.targetar2021.en.pdf). This chapter contains very interesting Box 3: Cross-border payments in TARGET2: an international perspective.

However, the above payment still does not fall into the category of cross-border payment as it is understood in the context of CBPR+. Why is that?

To understand this better we have to highlight that settlement in TARGET between banks located in the same country or different countries takes place in the same way. Why? Because we have here a system that uses centralized technical infrastructure that is the same for each participating country. For the processing of the above payment, Bank A does not need to have any bilateral relationship with Bank B. All the banks participating in the TARGET system are reachable to each other without a need for any bilateral business relationship between them.

Let’s repeat once more: even if a TARGET payment is between two banks in two countries, we would not consider this as a cross-border payment in the sense in which this word is used in the context of CBPR+. Such payment falls under TARGET rules and not CBPR+ rules.

**So, what is needed to consider a payment as cross-border?**

The key aspect of the above payment between banks in France and Germany that would not allow us to understand this payment as a cross-border payment is the fact, that the payment was **in the currency in which their Payment System operates, and because of that they did not need to have bilateral account relationship to process the payment**.

But the situation would be different if these two banks were to process a non-EUR payment, which cannot be settled in TARGET.

And this brings us to the following conclusion:

**To fully understand a payment as a cross-border payment in the context of CBPR+:**

- **not only should** **the banks be located in different countries,**
- **but also the payment should be denominated in a foreign currency, in which their local Payment System does not operate.**

We are going to explore this topic further in the below section.

**Cross-border payment**

So, let us investigate this topic of currency a bit further by asking the following question:

What is necessary for Bank A in France to process payments in USD?

We know that Bank A’s local Payment Systems do not settle in USD. For example, Bank A does not have a USD account in TARGET.

The settlement of USD is done in the USA. This leads us to the conclusion, that **if Bank A wants to settle in USD it has to get access to the payment infrastructure in the USA.**

How can Bank A access the payment infrastructure in the USA?

**It can open an account in one of the banks in the USA.**

And this type of arrangement we call a **correspondent account relationship**.

When Bank A opens a USD account in Bank C in the USA, Bank C is called the USD correspondent of Bank A.

How do we call this account that Bank A opens in Bank C?

We can look at this account from various perspectives, and the chosen perspective determines what this account is called. This is illustrated in the below diagram.

![Nostro.Vostro](https://iso20022payments.com/wp-content/uploads/2022/12/Nostro.Vostro.jpg)

As we can see Vostro and Nostro accounts are the same accounts but considered from different perspectives.

Bank A will call its account in Bank C a Nostro account, but Bank C will call it a Vostro account. In the below examples, I will stick to Bank A’s perspective and call it a Nostro account.

This Nostro account of Bank A in Bank C will be used for USD payments from/to Bank A in France.

To provide an example, let’s assume that Marc in France, a customer of Bank A is expecting a 100 USD payment from his friend, John, a customer of Bank C in the USA.

We know that in each bank or in each system the bookings have to be done on both the debit and credit side. The total sum of debits should be equal to the total sum of credits. We saw above an example of such debiting and crediting of the accounts in TARGET system.

What will the situation be here when the payment from John to Mark is processed?

Let’s begin with identifying accounts involved in the payment processing in Bank C. Here, we can guess that John’s account will be debited and Bank A’s Nostro account in Bank C will be credited.

And what about the bookings on the Bank A site?

As Marc is supposed to receive the payment, Marc’s account in Bank A will be credited. To make things simple let’s assume that Marc’s account is in USD. If it were in EUR Bank A would have to apply a currency conversion to be able to book the received amount on an EUR account.

But, which account will be debited in Bank A? The answer is that Bank A will debit a special, internal account, opened in its own books. This account is called a Mirror Nostro account and is opened for accounting and reconciliation purposes. The purpose of this account is to reflect what is happening on the account in Bank C.

Now, as we identified all the accounts involved in this scenario, we can illustrate them in the following way:

![Mirror Nostro](https://iso20022payments.com/wp-content/uploads/2022/12/Mirror-Nostro-.jpg)

Because Bank A and Bank C have a direct account relationship in the currency of the transfer we are ready to make a payment.

John pays Marc 100 USD.

For the readability of this example, I will illustrate the bookings in a simplistic way and we will not consider the charges.

So, the payment will look like that:

![Cross-border payment 1](https://iso20022payments.com/wp-content/uploads/2022/12/Cross-border-payment-1.jpg)A couple of remarks:

- As not all of the readers may be familiar with double-entry accounting represented on T-accounts, for the purpose of this section I use the simplified illustration of booking entries.
- I know that according to the English notation, I should probably write ‘USD 100’, however, in these examples where signs ‘+’ and ‘-‘ are added, I found that ‘100 USD’ is more straightforward.
- Please note, that accounting rules differ among banks. For example, some banks may use additional temporary accounts, like Wash accounts during the processing flow.

**I described the T-accounts as well as Wash accounts in the following section: [T-account and Wash account](https://www.iso20022payments.com/miscellaneous/t-account-and-wash-account/)**

And finally, the above example is an example of cross-border payment which falls into the CBPR+ rules. In other words, the payment message sent over SWIFT by Bank C to Bank A is validated against CBPR+ rules.

This is however a simple scenario. There is only one direct account relationship and one payment leg. And this is not always the case. Especially in the context of less popular currencies banks often do not have direct account relationships with the Creditor Bank, so they need to convey the transaction via intermediaries.

In other CBPR+ sections, we will explore such transactions in detail. However,the logic is the same even in more complex scenarios.

What’s important to highlight here is that each payment leg of a transaction in the CBPR+ space has to rely on account relationships between the two banks exchanging the message. In other words, to process such transactions there is a need for an account relationship chain between every pair of banks involved in the processing of the payment.

**With this example of cross-border payment, we can return to the question of the settlement.**

Here, we do not have a Payment System that processes the payment.

We know that settlement is performed by the bank. But here we have two banks.

**So, which bank performs settlement in the above scenario?**

We know that the above payment is in USD.

And which bank holds the account for the other one in USD? Of course, Bank C holds the account in USD for Bank A.

So, for the above example, the settlement is done in Bank C.

And for the payments in USD between Bank A and Bank C, this will be always the case. No matter what the direction of the payment is, from Bank C to Bank A or vice versa, the settlement will be done in Bank C, as Bank C holds the USD account for Bank A. What’s interesting, for payments from Bank C to Bank A the settlement is done even before the payment message arrives at Bank A in France!

Let’s however notice, that in the above example, we considered only the USD accounts and payments. For the time being, we have discussed only the situation where one bank has a Nostro account in the other bank. This is a unilateral account relationship. However, very often banks have bilateral account relationships.

If Bank C in the USA wants to process EUR payments it may also open an account in Bank A. The situation will be symmetrical to the one considered above. Bank A will service an account for Bank C in EUR. This account will be a Nostro account for Bank C and it will be a Vostro account for Bank A . Bank C will open in its own books a Mirror Nostro account. Every transfer in EUR will be settled in Bank A in France, no matter what the direction of the transfer is. This is because Bank A will hold the account for Bank C in the currency of the transfer.

To conclude this account setup, let’s remember that if two banks have a bilateral direct account relationship in both currencies, it means that both of them hold the accounts for the other one. **W** **hich bank settles the payment will depend on the currency of the particular payment.**

The notion described here may not be completely clear for now, and especially the following question may arise:

Why is it important which bank settles the payment?

As we will see in the future sections this notion is crucial when determining whether the message should be rejected or returned (if there is a need for such action). This aspect we are going to cover while investigating pacs.002 and pacs.004 messages.

And please bear with me, we will also come back to this idea in the next section of the CBPR+ series which is related to the [INDA and INGA Settlement Method](https://iso20022payments.com/cbpr/settlement-method-inga-inda/).

If this topic is not fully clear to you, hopefully, the next article will allow you to connect the dots.

For the time being let’s have a look at more complex examples of cross-border payments.

**More complex cross-border payments**

Now, we can go back to the situation where we have two banks from Europe: Bank A from France and Bank B from Germany. We know that Bank A has a USD account in Bank C in the USA.

Now Marc from France wants to send 50 USD to his friend Frank who has an account in Bank B in Germany.

Frank’s account is also in USD.

Let’s consider two scenarios here.

Similarly to the situation described earlier for Bank A, if Bank B wants to process payments in USD it has to open a Nostro account with a chosen bank in the USA.

Our two scenarios described below differ depending on whether Bank A and Bank B will have the same USD correspondent or not.

**Scenario 1. Bank B holds its USD Nostro Account in Bank C**

In this scenario Bank A and Bank B have the same USD correspondent.

Here is the diagram that shows what such a payment from Marc to Frank will look like.

![Cross-border payment 2](https://iso20022payments.com/wp-content/uploads/2022/12/Cross-border-payment-2.jpg)

The logic applied for bookings on the accounts is the same as the one described earlier.

Both messages exchanged in this example**(1)** and **(2)** are treated as cross-border payments and fall under the CBPR+ rules.

We could go even further here and depict the scenario where two banks from the same country, for example, France, have to process the USD payment.

Would it be a domestic payment? No. As this scenario will still require the inclusion of their USD correspondents, this would be still a cross-border payment processed according to CBPR+ rules.

**Scenario 2. Bank  B holds its USD Nostro Account in Bank D**

If Bank A and Bank B had different USD correspondents, the payment leg in the USA would be processed either via a payment system in the USA, for example Fedwire (RTGS system in the USA), or by direct payment message based on a bilateral relationship between Bank C and Bank D. The below diagram depicts the scenario of the settlement done via Fedwire.

![Fedwire](https://iso20022payments.com/wp-content/uploads/2022/12/Fedwire.jpg)

The above payment chain consists of 4 messages.

In this flow messages **(1)** and **(4)**are the CBPR+ messages but messages **(2)** and **(3)**are processed according to Fedwire rules.

Messages **(** **2)** and **(3)** denote a similar situation that we investigated at the beginning of this section in the context of TARGET system. Generally, if payment legs are processed by Market Infrastructure, i.e. payment systems like TARGET or Fedwire, they are not CBPR+ payments. We are going to explore this topic further with some meaningful examples in the section dedicated to the TARGET system.

**Conclusion**

I know that cross-border payments are quite challenging. I hope that this article was of a little help in understanding this subject. If it is still unclear, perhaps walking through the message examples that I am going to prepare will help connect this knowledge with practical application.

In the payment industry, we define cross-border payments usually by taking into account the **currency zone** and **currency of the payment**.

Following this approach, it is commonly understood that:

- **domestic payment** is between banks located in one currency zone with the payment in local currency ( _e.g._ _EUR payment between banks in France and Germany_)
- **cross-border payment** is in any other scenario:
  - between banks located in the same currency zone with the payment in foreign currency ( _e.g._ _USD payment between banks in France and Germany_)
  - between banks in the two currency zones with the payment in:
    - the local currency of one of the banks ( _e.g._ _USD payment between banks in France and the USA_)
    - foreign currency for both banks ( _e.g._ _GBP payment between banks in France and the USA_).

To conclude, I would like just to say that in the payment world, there are many nuances. Although the above approach is of key importance, when we take it out of the business context we may not always get the answer to whether a particular payment has to be processed via CBPR+ messages or not.

I will give you an example concerning my own country:

In Poland our local currency is PLN. France, where the local currency is EUR, is in a different currency zone. How will the high-value payment from the bank in Poland to the bank in France be settled?

According to the above definitions, this payment falls into the category of cross-border payment. Hence, it should be processed based on correspondent banking arrangements via CBPR+ message. And indeed there are banks in Poland that may send such payments that way.

However, this is not the only way.

As the National Bank of Poland joined TARGET2 system in 2008, several polish banks are direct TARGET participants. These banks can send payments to a bank in France in EUR without any correspondent account relationship. This payment will be processed the same way the payment between banks in France and Germany takes place. As this will be a TARGET payment it will not fall into CBPR+ rules.

What I am trying to say here, is that while discussing such a complex topic as cross-border payments, it is always good to have a full business context in mind.

The next topic to investigate in our journey is closely related to this one. I will talk about INDA and INGA Settlement Methods.

|     |     |
| --- | --- |
| [<< CBPR+ documentation](https://iso20022payments.com/cbpr/cbpr-documentation/) | [Settlement Method: INGA vs. INDA >>](https://iso20022payments.com/cbpr/settlement-method-inga-inda/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme