---
url: "https://www.iso20022payments.com/cbpr/charges/"
title: "Charges – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/cbpr/charges/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## CBPR+

## Charges

In this section, I would like to talk about charges. This is a complex issue.

First of all, it should be explained that what we call transaction charges is different from the SWIFT charges, that banks have to pay for SWIFT services.

Transaction charges are the charges that banks apply for the processing of customer payments.

Interbank transfers do not have associated charges, only customer payments do.

Each bank can decide at its discretion about its own price policy.

**pacs.008 elements related to charges**

How the charges-related information is presented in customer payment?

To answer this question, we have to consider the following elements of pacs.008:

**Interbank Settlement Amount** – this is the point-to-point currency amount that is settled between banks in one payment leg. This element may change throughout payment chain.

**Instructed Amount** – this is a conditional element that captures currency and amount instructed by the Debtor.

The Instructed Amount is present when Interbank Settlement Amount is in a different currency or amount. This may happen because of charges deduction or currency conversion. Instructed Amount cannot be changed in the payment chain.

**Exchange Rate** – this is a rate used for currency conversion. It must be present when currencies in Interbank Settlement Amount and Instructed Amount differ.

How the Exchange Rate is presented?

Instructed Amount currency is a base currency referred to as a whole unit to perform the exchange and the Interbank Settlement Amount currency is the quote currency.

If for example the Instructed Amount is in USD and the Interbank Settlement Amount is in EUR, USD 1 will be taken to show the exchange rate: 0.93998, because USD 1equals EUR 0.93998.

**Charge Bearer** – this element specifies which party would bear the charges. Possible values in CBPR+ are:

CRED – Creditor

DEBT – Debtor

SHAR – Shared

**Charges Information** – this field provides information on the charges to be paid by the Charge Bearer. The meaning of this element is twofold. It shows either:

- The amount of charges and the bank for whom the charges are due. This is a pre-paid scenario. In this scenario, the BIC of the bank for whom the charges are due is populated by the previous bank in the payment chain. The next bank upon receiving the message identifies its BIC and knows that the charges were pre-paid.
- The amount of charges and the bank that has deducted the charges. In this scenario, charges were not pre-paid. Bank deducts its charges from the Interbank Settlement Amount and provides its BIC and amount deducted to inform the next banks in the payment chain.

This is a repetitive field and it may be added at each payment leg. As this element may show both charges pre-paid for Bank X, and in other business case charges deducted by Bank X, it is crucial that other charges-related information in the message (e.g. Interbank Settlement Amount and Instructed Amount) are used correctly.

Additionally it is important to note, that even that CBPR+ does not prevent Charges from being booked in different currency, for transparency the Charges in the message should be represented in the Interbank Settlement Amount Currency.

So, now, let’s have a look at how the information analyzed above is provided in the message itself:

![Charges](https://iso20022payments.com/wp-content/uploads/2022/12/Charges.jpg)

I hope that you can identify each element we discussed above.

However, I know that the business usage of these elements may not be clear for the time being. The theoretical explanation is not enough. But, I am sure it will become more understandable if we put it in the business context. And this is precisely the aim of the below examples.

The examples show the 3 charges options: DEBT, SHAR, and CRED.

While investigating them we are going to see how in practice banks levy their charges.

**DEBT**

In this scenario, Bank A received the request for payment in EUR. The Amount is the EUR equivalent of USD 100.

The Instructed Amount is in USD, but the Interbank Settlement Amount is going to be in EUR.

The Debtor’s account with Bank A is in USD.

Debtor informed Bank A that he will bear all the charges – DEBT option.

Three banks are involved in the payment. All of them have their own charges.

The below diagram depicts how the messages are structured.

![](https://iso20022payments.com/wp-content/uploads/2022/12/DEBT..jpg)

**(1) pacs.008 sent by Bank A**

In our scenario, **the Instructed Amount is USD 100.**

The Instructed Amount is in USD and the Interbank Settlement Amount is in EUR. Instructed currency is used as the whole unit to perform the exchange, that is  USD 1 equals EUR **0.9401**. This is our **Exchange Rate.**

EUR equivalent of the USD 100 is EUR 94.01.

Bank A knows, however, Bank B’s charges for such a payment. They equal 10 EUR. In the message, Bank A adds EUR 10 to the EUR 94.01. So, the **Interbank Settlement Amount is EUR 104, 01** (EUR equivalent of USD 100 + Bank B’s EUR 10 charges).

Additionally, Bank A signals to Bank B that the charges have been prepaid. How?

In Charges Information Bank A adds the BIC of BANK B (**Agent – BANKFRBBXXX**). This will indicate to Bank B that the charges have been pre-paid. Additionally Bank A populates the Amount that has been pre-paid (**EUR 10**).

What is not presented in the pacs.008 is what are the charges of Bank A for this payment. Let’s assume they equal USD 5.

In accordance with Debtor’s banking agreement Bank A will debit Debtor’s account for:

- USD 100 that the Debtor instructed
- USD 5 of Bank A’s charges
- USD equivalent for Bank B’s EUR 10 charges that have been pre-paid. As the Debtor’s account is in USD, any bookings on this account have to be reflected in USD.

**(2) pacs.008 sent by Bank B**

Bank B recognizes the pre-payment of charges by the inclusion of its BIC in the Charge Information Agent element.

What is characteristic about the pre-paid scenario is also the fact that Interbank Settlement Amount is higher than Instructed Amount.

Bank B deducts its charges from the Interbank Settlement Amount. In the outgoing pacs.008 the **Interbank Settlement Amount equals EUR 94.01**(EUR 104.01 – EUR 10). Now, the Interbank Settlement Amount is precisely the EUR equivalent of instructed USD 100.

Bank B removes the Charges Information as it is not needed for Bank C. If bank B left the Charges Information with Bank B’s BIC the information could be misleading for Bank C. The amounts presented would not add up.

**(3) pacs.008 at Bank C**

Bank C receives the payment and notices that the Charge Bearer code is DEBT. Bank C identifies that its charges have not been pre-paid. There is no its BIC in the Charges Information.

With DEBT option Bank C cannot deduct its charges from the amount it credits to the Creditor. In other words, Creditor receives EUR 94, 01 which is the EUR equivalent of USD 100 as instructed by Debtor.

Bank C may in such a situation claim the charges. Sometimes it is also possible to debit the Nostro account of Bank B that Bank C may hold for Bank B. This is subject to a bilateral agreement between banks.

Before we move on I would like to make one remark about the above scenario.

You may have noticed that Bank B is located in France. In European Union, there is PSD2 legislation (you can access this document [here](https://www.eba.europa.eu/regulation-and-policy/single-rulebook/interactive-single-rulebook/5402)) that regulates that for certain payments only **SHAR** option is allowed (Article 62 (2)). Additionally, there is a so-called **full amount principle** introduced (Article 81). However, let’s assume that this scenario is a one-leg payment (both Bank A and Bank C are outside EEA). In this case, according to the _Guidance for implementation of the revised Payment Services Directive_ (available [here](https://www.ebf.eu/wp-content/uploads/2019/12/EBF-PSD2-guidance-Final-December-2019.pdf)), these PSD2 articles are not applicable.

**SHAR**

In this scenario, Bank A received the request for payment of USD 100. To avoid making this example too complex this time the currency of the Instructed Amount and Interbank Settlement Amount is going to be USD. Additionally, all four banks involved in the payment are located in the USA. All of them have their own charges expressed in USD. Debtor’s and Creditor’s accounts are also in USD.

I am aware that this may not be very probable business scenario, as such payment would be processed via the Payment system in the USD, however, for educational purposes I think is still valuable and will allow us to understand how the charges are processed.

Debtor informed Bank A that the charges will be shared – SHAR option.

The below diagram depicts how the messages are structured.

![SHAR](https://iso20022payments.com/wp-content/uploads/2022/12/SHAR.jpg)

**(1) pacs.008 sent by Bank A**

As the Interbank Settlement Account is in the same currency as the Instructed Amount, and there is no Charges Information, Bank A does not include Instructed Amount element in pacs.008.

In SHAR option Bank A’s charges are borne by Debtor, so Bank A will debit Debtor’s account for:

- USD 100 that the Debtor instructed
- USD 5 of Bank A’s charges

**(2) pacs.008 sent by Bank** **B**

In SHAR option, except the charges of the Debtor’s Agent (Bank A), all other banks’ charges are borne by Creditor. So, in practice, beginning of Bank B the way SHAR charges are processed is the same as for CRED option.

How do banks levy their charges in such a scenario? Banks deduct their charges from the Interbank Settlement Amount.

Following this logic, Bank B reduces the Interbank Settlement Amount by the amount of its charges (USD 10), so that the Interbank Settlement Amount in pacs.008 sent to Bank C equals USD 90.

Additionally, Bank B adds also the Charges Information to inform the next banks in the chain that it has deducted its charges.

Because, the Charges Information has been added and Interbank Settlement Amount is now different from the amount that Debtor instructed, Bank B adds also the Instructed Amount to pacs.008. This way, the whole picture becomes clear for the next banks.

**(3) pacs.008 sent by Bank** **C**

Following the same logic, Bank C reduces further the Interbank Settlement Amount by the amount of its charges (USD 7), so that the Interbank Settlement Amount in pacs.008 sent to Bank D equals USD 83.

Additionally, Bank C adds also the Charges Information to inform the next bank in the chain that it has deducted its charges.

Here we have an example of the repetitive nature of Charges Information. We have two occurrences of this element.

What we can observe is that there is a very straightforward relationship between the following elements:

Instructed Amount – Charges = Interbank Settlement Amount.

**(4) pacs.008 at Bank D**

Bank D receives the payment and notices that the Charge Bearer code is SHAR so its charges will be borne by Creditor.

Bank D decreases Interbank Settlement Amount (USD 83) with the amount of its charges (USD 5) and credits the Creditor (USD 78).

**CRED**

This scenario is a simpler version of the previous one. We have only 3 banks located in the USA.

Bank A received the request for payment of USD 100. Again, to avoid making this example too complex the currency of the Instructed Amount and Interbank Settlement Amount is going to be USD. All of the banks have their own charges expressed in USD. Debtor’s and Creditor’s accounts are also in USD.

Debtor informed Bank A that the charges will be borne by Creditor – CRED option.

The below diagram depicts how the messages are structured.

![CRED](https://iso20022payments.com/wp-content/uploads/2022/12/CRED..jpg)

**(1) pacs.008 sent by Bank A**

As the Interbank Settlement Amount is in the same currency as the Instructed Amount we could expect that the Instructed Amount will not be populated by Bank A. However, in this scenario Bank A’s charges are paid by Creditor. Bank A makes Creditor pay its charges by reducing the Interbank Settlement Amount by its charges (USD 5). Also, Bank A adds the relevant information in Charges Information indicating that it has deducted its charges by including its BIC (BANKUSAAXXX) and providing the amount (USD 5).

In CRED option Bank A’s charges are borne by Creditor, so Bank A will debit Debtor’s account only for:

- USD 100 that the Debtor instructed

**(2) pacs.008 sent by Bank** **B**

In CRED option charges are borne by Creditor. Banks deduct their charges from the Interbank Settlement Amount.

Following this logic, Bank B reduces the Interbank Settlement Amount by the amount of its charges (USD 10), so that the Interbank Settlement Amount in pacs.008 sent to Bank C equals USD 85.

Additionally, Bank B adds also the Charges Information, to inform the next bank in the chain that it has deducted its charges.

**(3) pacs.008 at Bank C**

Bank C receives the payment and notices that the Charge Bearer code is CRED so its charges will be borne by Creditor.

Bank C decreases Interbank Settlement Amount (USD 85) with the amount of its charges (USD 5) and credits the Creditor (USD 80).

This is the end of the charges part. In my opinion, this is one of the most difficult aspects of payment processing. It would be great if the information I provided were of some help. In CBPR+ pacs.008 usage Guidelines there are many detailed rules that show cross-element dependencies in this context. I advise you to consult them in case of any questions.

|     |     |
| --- | --- |
| [<< Point-to-point vs. End-to-end](https://iso20022payments.com/cbpr/point-to-point-end-to-end/) | [CBPR+ message structure >>](https://iso20022payments.com/cbpr/cbpr-message-structure/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme