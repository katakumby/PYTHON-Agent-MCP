---
url: "https://www.iso20022payments.com/cbpr/settlement-method-inga-inda/"
title: "Settlement Method: INGA vs. INDA – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/cbpr/settlement-method-inga-inda/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## CBPR+

## Settlement Method: INGA vs. INDA

In the previous section, we discussed cross-border payments, and we especially focused on the notion of settlement.

We identified the bank which in particular cross-border payment leg is responsible for settlement of the payment.

It was not a theoretical exercise because in ISO 20022 pacs messages there is precisely an element related to this notion. This element is called **Settlement Method**.

In this section, we are going to look at two possible values that this element may hold: **INGA** and **INDA**.

There are two aspects which are important for us in this respect. These are:

**1.** What is the direction of the payment message? In other words which bank is the Sender and which bank is Receiver. However, from a business perspective in ISO 20022 terminology Sender is called **Instructing Agent** and Receiver is called **Instructed Agent**.

**2\.**Which bank holds the account in the currency of the transfer for the other one? This aspect we precisely analyzed in the previous section. If it is difficult for you to identify the bank which holds an account for the other bank there is an additional question that may help to determine that. This question is: Which bank provides the Account Statement? The bank that provides the Account Statement is an Account Servicing Institution, and thus holds an account for the other bank in the payment leg.

So, what is the meaning of the INGA and INDA Settlement Method?

**INGA** stands for **IN**structin**G A**gent, and it means that the Instructing Agent performs the settlement of the payment leg.

**INDA** stands for **IN**structe**D A**gent, and it means that the Instructed Agent performs the settlement of the payment leg.

Now, as we already know the theory behind Settlement Method element we are ready to have a look at a practical application of this idea.

**INGA and INDA examples**

Our examples will relate to the scenario discussed in the previous section: [Cross-border payments](https://iso20022payments.com/cbpr/cross-border-payments/)

As the analyzed notion is more related to interbank settlement, in the below examples I want to focus just on two types of accounts: Nostro and Mirror Nostro. The customers’ accounts are just presented for accounting purposes.

There are two banks involved in the below examples: Bank A in France and Bank C in the USA. They established the bilateral account relationship.

It means that Bank A in France holds a EUR account for Bank C (for Bank C it is a Nostro Account).

Symmetrically, Bank C holds a USD account for Bank A (for Bank A it is a Nostro Account).

Let’s have a look at 4 scenarios depending on the currency and the direction of the transfer.

**INGA – EUR payment**

![INGA - EUR payment](https://iso20022payments.com/wp-content/uploads/2022/12/INGA-EUR-payment.jpg)

Which bank holds an account for the other one in the currency of the payment?

Payment is in EUR, and **Bank A** holds a EUR account for Bank C. Bank A will provide here an Account Statement. In other words, Bank A services the account of Bank C and is responsible for settling this payment leg.

Is Bank A and Instructed or Instructing Agent?

Bank A is **IN** structin **G A** gent. The direction of the payment is from Bank A to Bank C.

Settlement Method is **INGA**.

**INDA – EUR payment**

![INDA - EUR payment](https://iso20022payments.com/wp-content/uploads/2022/12/INDA-EUR-payment.jpg)

Which bank holds an account for the other one in the currency of the payment?

Payment is in EUR, and **Bank A** holds a EUR account for Bank C. Bank A will provide here an Account Statement. In other words, Bank A services the account of Bank C and is responsible for settling this payment leg.

Is Bank A and Instructed or Instructing Agent?

Bank A is **IN** structe **D A** gent. The direction of the payment is from Bank C to Bank A.

Settlement Method is **INDA**.

**INGA – USD payment**

![INGA - USD payment](https://iso20022payments.com/wp-content/uploads/2022/12/INGA-USD-payment.jpg)

Which bank holds an account for the other one in the currency of the payment?

Payment is in USD, and **Bank C** holds a USD account for Bank A. Bank C will provide here an Account Statement. In other words, Bank C services the account of Bank A and is responsible for settling this payment leg.

Is Bank C and Instructed or Instructing Agent?

Bank C is **IN** structin **G A** gent. The direction of the payment is from Bank C to Bank A.

Settlement Method is **INGA**.

**INDA – USD payment**

![INDA - USD payment](https://iso20022payments.com/wp-content/uploads/2022/12/INDA-USD-payment.jpg)

Which bank holds an account for the other one in the currency of the payment?

Payment is in USD, and **Bank C** holds a USD account for Bank A. Bank C will provide here an Account Statement. In other words, Bank C services the account of Bank A and is responsible for settling this payment leg.

Is Bank C an Instructed or Instructing Agent?

Bank C is **IN** structe **D A** gent. The direction of the payment is from Bank A to Bank C.

Settlement Method is **INDA**.

**When the settlement takes place?**

There is one more important aspect of Settlement Method that I would like to mention here.

If the Settlement Method is **INGA** it means the settlement is done by the bank sending the payment message. It means that settlement is already done at the moment the **IN** structin **G A** gent sends the payment message.

If Settlement Method is **INDA** it means the settlement is not done by the bank sending the payment message. In other words, settlement is not done at the moment the Instructing Agent sends the payment message. It will only be done when **IN** structe **D A** gent processes the payment.

This aspect will also come back in our analysis at the time when the return or reject messages will be investigated.

I hope this section was helpful when it comes to understanding the notion of INGA and INDA Settlement Method.

However, our adventure with Settlement Method is far from over.

We have not covered all possible Settlement Methods. But with this, let’s wait for the appropriate business scenario.

|     |     |
| --- | --- |
| [<< Cross-border payments](https://iso20022payments.com/cbpr/cross-border-payments/) | [Point-to-point vs. End-to-end >>](https://iso20022payments.com/cbpr/point-to-point-end-to-end/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme