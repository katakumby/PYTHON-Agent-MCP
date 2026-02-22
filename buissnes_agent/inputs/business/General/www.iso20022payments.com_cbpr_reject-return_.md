---
url: "https://www.iso20022payments.com/cbpr/reject-return/"
title: "Reject & Return – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/cbpr/reject-return/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## CBPR+

## Reject & Return

This article is related to Reject (pacs.002) & Return (pacs.004) messages in CBPR+.

Although I am going to give some basic information about the messages it is not the goal of this article to investigate the messages’ structure in detail.

What I want to do is explore the different flows of messages and see how they may result in pacs.002 and pacs.004 being sent.

Here we are also going to observe what is the role of Nostro/Vostro account relationship and INDA/INGA settlement method.

Let’s start with the basic information about messages.

**pacs.002**

Pacs.002 is a Payment Status Report message.

As a ‘Report’ message it always relates to the previously sent payment.

It is sent by an instructed agent of the original message to the previous party in the payment chain.

So, let’s imagine that Bank A (Instructing Agent) sends pacs.008 to Bank B (Instructed Agent).

Pacs.002 is sent by Bank B to Bank A. In pacs.002 Bank B becomes Instructing Agent and Bank A becomes Instructed Agent.

This is because Instructing Agent and Instructed Agent represent the Agents involved in the pacs point-to-point message exchange. These roles therefore change on each payment leg.

Now, let’s have a look at two questions related to pacs.002:

**How the original message is identified in pacs.002?**

If pacs.002 always relates to a previously sent message, there has to be a way to identify the previous message in pacs.002.

Well, if we have a look at the pacs.002 structure, we will notice that there are a lot of elements that begin with word “Orginal”. These refer to the original message that pacs.002 is linked to.

Below I listed only 4 mandatory elements:

- **Original Message Identification:** _Message Identification of the underlying payment (eg. pacs.008/pacs.009/pacs.004)._
- **Original Message Name Identification:** _message name of the underlying payment (e.g. pacs.008.001.08 or pacs.009.001.08)_
- **Original End To End Identification:** _EndToEnd Identification of the underlying payment message_
- **Original UETR:** _UETR of the underlying_ _payment message_

And the second question is:

**What is the purpose of pacs.002?**

In fact, pacs.002 is not only used for the Rejects scenarios.

Generally, this message is used to inform about:

- final positive status of an instruction
- final negative status of an instruction
- status of the pending instruction

What is important to understand is that pacs.002 becomes mandatory only in the scenario of final negative status of an instruction. In other words, when payment is Rejected, pacs.002 must be sent to inform the previous agent in the chain.

There are two elements in pacs.002 that transport the ‘status’ information:

- **Transaction Status** – utilizes the externalized [ISO Payment Transaction Status code](https://www.iso20022.org/catalogue-messages/additional-content-messages/external-code-sets) (ExternalPaymentTransactionStatus1Code) list to provide a status update on a pacs message previously received. In this article, we refer to the scenarios linked to RJCT (Reject) Transaction Status.
- **Status Reason Information** with additional nested elements:
  - Reason – which utilizes either an [ISO external Status Reason code](https://www.iso20022.org/catalogue-messages/additional-content-messages/external-code-sets) (ExternalStatusReason1Code) or a proprietary reason.

    For example, AC04 ‘Closed Account Number’ may complement an RJCT (Reject) Transaction Status.
  - Additional Information – a text element to provide further status reason information.

As I said, in this article we are going to focus on the situation when an agent has to REJECT the payment, and as a result, it sends pacs.002 with the final negative status code RJCT (Rejected). Let’s not forget that when the payment is rejected it is mandatory to send pacs.002. Additionally, if the Transaction Status RJCT (Reject) code is used, Status Reason Information/Reason is mandatory.

- This is how it may look in the pacs.002:

![](https://www.iso20022payments.com/wp-content/uploads/2023/07/RJCT.png)


**pacs.004**

Pacs.004 is a Payment Return message.

Let’s look at some similarities and differences between pacs.002 and pacs.004.

**Similarities between pacs.002 and pacs.004**

- What is similar between pacs.002 and pacs.004 is that both messages relate to the original message that was sent before.
- Both messages are sent by an instructed agent of the original message to the previous party in the payment chain.
- Return Reason Information/Reason element in pacs.004 also uses [ISO 20022 external code list](https://www.iso20022.org/catalogue-messages/additional-content-messages/external-code-sets) (ExternalReturnReason1Code) to provide the Reason information for the Return.
- If we have a look at the pacs.004 structure, we will notice that similarily to pacs.002 there are a lot of elements that begin with word “Orginal”. These refer to the original message.

Below I listed 4 mandatory elements, which are also present in pacs.002:

**– Original Message Identification**: _Message Identification of the underlying payment (eg. pacs.008/pacs.009)._**– Original Message Name Identification**: _message name of the underlying payment (e.g._ _pacs.008.001.08 or pacs.009.001.08)_

**– Original End To End Identification**: _EndToEnd Identification of the underlying payment message_**– Original UETR**: _UETR of the underlying pacs.008/pacs.009_


**Key differences between pacs.002 and pacs.004**

What are the differences between these two messages?

Certainly, there are a lot of them, however, there is one which I would like to highlight the most:

- As we have seen pacs.002 informs about the status of the payment. It’s a ‘Report’ message.
- On the other hand, pacs.004 is something ‘more’. Pacs.004 is a settlement instruction itself.

The fact that pacs.004 is a separate settlement instruction from the original payment has various important implications, i.a.:

- Returned Interbank Settlement Amount may be different than the Original Interbank Settlement Amount.
- Pacs.004 has charges-related elements in the message.
- There is a Settlement Method element in pacs.004. In the correspondent banking space, INDA/INGA is used in this element. We will come back to this notion later in this article.
- Return Chain element from pacs.004 captures all the parties involved in the return transaction. In this element, however, the roles of the various parties change. For example, the Creditor Agent of the original payment may become the Debtor Agent of the Payment Return.
- As with any other settlement instruction (like pacs.008, pacs.009) the outcome of the pacs.004 settlement can be positive or negative.

When the outcome is negative pacs.004 should be Rejected by pacs.002.

This is shown in the below diagram from CBPR+ UHB:

![](https://www.iso20022payments.com/wp-content/uploads/2023/07/Reject-of-pacs.004-1024x442.png)

In the diagram, we can see that Bank C Rejects pacs.008 with pacs.002.

Bank B does not forward pacs.002 to Bank A but instead, it sends pacs.004.

Bank A, however, can’t settle this pacs.004 so pacs.004 is rejected via pacs.002.

I hope after this article we will be able to understand why banks involved in this scenario send the described messages.

This is, however, quite a complex subject, so let’s begin this journey by reminding ourselves about INDA/INGA settlement methods and Nostro/Vostro account relationship.

**-INDA vs. INGA-**

**Which settlement method should be used?**

First of all, I think it is important to remember that each payment leg has its own settlement component.

Moreover:

- In each settlement leg, two banks are involved.
- There is an account relationship in the currency of the transfer between these banks.
- The settlement of the particular payments leg is done by the bank that holds the account in the currency of the transfer for the other one.

This notion was already described in the previous articles:

- ## [Cross-border payments](https://www.iso20022payments.com/cbpr/cross-border-payments/)

- ## [Settlement Method: INGA vs. INDA](https://www.iso20022payments.com/cbpr/settlement-method-inga-inda/)


In the context of this article, I would like to present it with the below diagram:

![](https://www.iso20022payments.com/wp-content/uploads/2023/06/introductions.png)

In the diagram, we can see 3 payment legs.

Each payment leg has its own settlement component.

At the message level, this is reflected by Settlement Method (INDA/INGA).

To correctly populate this element (INDA/INGA) we should ask ourselves the following questions:

- **FIRST QUESTION:** Which bank holds the account (is Account Servicing Institution) for the other one? To determine this we can also ask which bank provides Account Statement for the other one in the currency of the transfer.
- **SECOND QUESTION:** Is this Account Servicing Institution the Instructing or Instructed Agent?

Let’s investigate the 3 payment legs from the above diagram:

**(1)** In the first payment leg we can see that Bank B holds the account in the currency of the transfer for Bank A. Bank B is the Account Servicing Institution. Bank B is responsible for the settlement. In the above diagram, the payment message is from Bank A to Bank B, so Bank B is **IN** structe **D A** gent. The settlement Method should be **INDA**.

**(2)** In the second payment leg we can see that Bank B holds the account in the currency of the transfer for Bank C. Bank B is the Account Servicing Institution. Bank B is responsible for the settlement. In the above diagram, the payment message is from Bank B to Bank C, so Bank B is **IN** structin **G A** gent. The settlement Method should be **INGA**.

**(3)** In the third payment leg we can see that Bank C holds the account in the currency of the transfer for Bank D. Bank C is the Account Servicing Institution. Bank C is responsible for the settlement. In the above diagram, the payment message is from Bank C to Bank D, so Bank C is **IN** structin **G A** gent. The settlement Method should be **INGA**.

As we have seen, the crucial factor here is to determine which bank holds the account for the other one.

This account is referred to as Vostro/Nostro account.

**-Nostro vs. Vostro-**

Below I prepared some exemplary data of Bank A, which we will use in the further part of the article.

Firstly, we are going to see what are the account relationship between Bank A and Bank B and Bank C in currency X.

Secondly, we are going to explore how this may be reflected in Bank A’s reference data.

**Bank A’s account relationship in currency X**

![](https://www.iso20022payments.com/wp-content/uploads/2023/07/Settlement-account.png)

As we can see Bank A has a correspondent account relationship in currency X with Bank B and Bank C.

Currency X is not the local currency for Bank A.

This is the base currency for Bank C.

Bank C is Bank A’s correspondent that holds an account in currency X for Bank A. This is the account on which the settlement will take place in currency X between Bank A and Bank C.

From Bank A’s perspective, this account is called a NOSTRO account.

Bank A holds in its books a mirror NOSTRO account.

On the other hand, the account relationship in currency X with Bank C, allows Bank A to offer the settlement service in currency X for Bank B.

To do so, Bank A holds the account in currency X for Bank B. This is an account on which the settlement will take place in currency X between Bank A and Bank B.

From Bank A’s perspective, this account is called a VOSTRO account.

Bank B holds in its books a mirror account.

How these account relationships are presented in Bank A’s reference data?

**Example of Bank A’s reference data**

Of course, each bank may have a different way of presenting the data in their own system, however, to my knowledge this is very often done in a similar fashion as in the diagram below.

![](https://www.iso20022payments.com/wp-content/uploads/2023/06/Reference-data-in-Bank-A.png)

**(1)** **Bank A** holds a **VOSTRO** account for **Bank B** in Currency X.

In Bank A’s reference data, the account type for Bank B is **VOSTRO**.

**Bank A** is Account Servicing Institution

(provides Account Statement to **Bank B**).

As a result, settlement in Currency X isperformed at **Bank A**.

If **Bank A** is **IN** structe **D** **A** gent, the settlement method is **INDA**.

If **Bank A** is **IN** structin **G** **A** gent, the settlement method is **INGA**.

**(2)** The second part is about **NOSTRO** account.

In Bank A’s reference data, the account type for Bank C is **NOSTRO**.

It means that the “real” account in X currency is in the books of **Bank C**.

**Bank C** holds a **NOSTRO** account for **Bank A** in Currency X.

**Bank C** is Account Servicing Institution

(provides Account Statement to **Bank A** ).

As a result, settlement in Currency X isperformedat**Bank C**.

If **Bank C** is **IN** structin **G** **A** gent, the settlement method is **INGA**.

If **Bank C** is **IN** structe **D** **A** gent, the settlement method is **INDA**.

**-pacs.002 (Reject) vs. pacs.004 (Return) –**

**Which message should be used?**

We have seen that in each payment leg, one of the two banks involved performs the settlement, and this is the one who holds the account for the other one in the currency of the transfer.

Now we have to add one more element to our equation.

we have to understand which message should be used (pacs.002 or pacs.004) based on whether the settlement took place or not.

Let’s put it simply:

**pacs.002:** is used to **REJECT** the payment leg. It is sent **BEFORE** the payment leg has been settled.

**pacs.004:** is used to **RETURN** the payment leg. It is sent **AFTER** the payment leg has been settled.

With all the above information we are ready to have a look at various scenarios.

**Note:** The idea with the below examples is not to present the whole payment chain. In the diagrams, I show only the payment legs that are necessary to understand the scenario.

**Scenario 1a – no settlement at Bank A**

![](https://www.iso20022payments.com/wp-content/uploads/2023/06/1a-no-settlement-at-Bank-A.png)

**(1)** **Bank A** holds a **VOSTRO** account in X currency for **Bank B**.

**Bank A** is responsible for the settlement.

**Bank B** sends pacs.009 to **Bank A** with **INDA** settlement method.

**(2)** Pacs.009 was NOT settled in the books of **Bank B**.

**Bank A** should settle this payment leg.

If **Bank A** cannot settle (book) this payment it has to reject it.

In our example, **Bank A** cannot book this payment.

**Bank A** sends pacs.002 with **RJCT** status.

Pacs.002 is sent because there was no settlement of pacs.009.

**Scenario 1b – settlement at Bank A**

![](https://www.iso20022payments.com/wp-content/uploads/2023/06/1b-settlement-at-Bank-A.png)

**(1)** **Bank A** holds a **VOSTRO** account in X currency for **Bank B**.

**Bank A** is responsible for the settlement.

**Bank B** sends pacs.008 to **Bank A** with INDA settlement method.

**(2)** **Bank A** settles the payment (credits the Creditor and sends the credit confirmation to the Creditor)

**(3)** Creditor requests the return of funds. Please note that it is possible to return the funds partially (if e.g. Creditor determines that they were overpaid).

**(4)** Pacs.008 (point 1) was settled in the books of **Bank A**.

**Bank A** CANNOT send pacs.002 (reject).

**Bank A** sends pacs.004 with **INGA** settlement method because **Bank A** holds the account for **Bank B** and is **IN** struting **G A** gent in pacs.004.

**Scenario 2 – settlement at Bank C**

![](https://www.iso20022payments.com/wp-content/uploads/2023/06/2-settlement-at-Bank-C.png)

**(1)** **Bank C** holds **Bank A’s NOSTRO** account in X currency.

**Bank C** sends pacs.009 to **Bank A** with INGA settlement method.

**Bank C** performs the settlement (credits NOSTRO account).

What is important to understand here, is that the settlement of this payment leg is done before **Bank A** receives pacs.009.

**(2)** Pacs.009 was already settled in the books of **Bank C**.

**Bank A** CANNOT reject this payment (pacs.002).

If **Bank A** cannot process this payment it has to send pacs.004 – Payment Return.

**Bank A** puts the **INDA** in pacs.004 settlement method because **Bank C** (INstructeD Agent) will settle this Payment Return.

**Scenario 3a – no settlement at Bank C**

![](https://www.iso20022payments.com/wp-content/uploads/2023/06/3a-no-settlement-at-Bank-C.png)

**(1)** **Bank A** holds a **VOSTRO** account in currency X for **Bank B**.

**Bank A** is responsible for the settlement.

**Bank B** sends pacs.009 to **Bank A** with **INDA** settlement method.

**(2)** **Bank A** sends pacs.009 further.

**INDA** is used as **Bank C** is responsible for the settlement (holds **NOSTRO** account for Bank A).

**(3)** Pacs.009 was NOT settled in the books of **Bank A**.

If **Bank C** cannot settle this payment it has to reject it.

**Bank C** sends pacs.002 with **RJCT** status.

**(4)** Pacs.009 from **Bank B** to **Bank A** was already settled (point 1).

**Bank A** CANNOT reject it (forward pacs.002).

**Bank A** has to send pacs.004 – Payment Return.

**Bank A** puts the **INGA** settlement method because **Bank A** settles this Payment Return.

**Scenario 3b – settlement at Bank C**

![](https://www.iso20022payments.com/wp-content/uploads/2023/06/3b-settlement-at-Bank-C.png)

**(1)** **Bank A** holds a **VOSTRO** account in currency X for **Bank B**.

**Bank A** is responsible for the settlement.

**Bank B** sends pacs.008 to **Bank A** with **INDA** settlement method.

**(2)** **Bank A** sends pacs.008 further.

**INDA** is used as **Bank C** is responsible for performing settlement (holds **NOSTRO** account for **Bank A**).

**(3)** **Bank C** settles the payment (credits the Creditor and sends the credit confirmation to the Creditor).

**(4)** Creditor requests the return of funds.

**(5)** Pacs.008 (point 2) was settled in the books of **Bank C**.

**Bank C** CANNOT send pacs.002 (reject).

**Bank C** sends pacs.004 with **INGA** settlement method because **Bank C** holds the account for **Bank A** and is **IN** struting **G A** gent in pacs.004.

**(6)** Pacs.008 (point 1) was settled in the books of **Bank A**.

**Bank A** CANNOT send pacs.002 (reject).

**Bank A** sends pacs.004 with **INGA** settlement method because **Bank A** holds the account for **Bank B** and is **IN** struting **G A** gent in pacs.004.

**Scenario 4 – settlement at Bank C and Bank A**

![](https://www.iso20022payments.com/wp-content/uploads/2023/07/4-settlement-at-Bank-C-and-Bank-A.png)

**(1)** **Bank C** holds **Bank A’s NOSTRO** account in currency X.

**Bank C** performs the settlement.

**Bank C** sends pacs.009 to **Bank A** with **INGA** settlement method.

**(2)** **Bank A** sends pacs.009 further.

**INGA** is used as **Bank A** performs settlement (holds **VOSTRO** account for **Bank B**).

**(3)** Pacs.009 (point 2) was settled in the books of **Bank A**.

**Bank B** CANNOT reject this payment (pacs.002).

If **Bank B** cannot process this payment further it has to send pacs.004 – Payment Return.

**Bank B** puts **INDA** settlement method because **Bank A** (INstructeD Agent) will settle this Payment Return.

**(4)** Pacs.009 (point 1) was already settled in the books of **Bank C**.

**Bank A** CANNOT reject this payment (pacs.002).

**Bank A** has to send pacs.004 – Payment Return.

**Bank A** puts the **INDA** settlement method because **Bank C** (INstructeD Agent) will settle this Payment Return.

**Scenario 5 – settlement in Market Infrastructure (MI)**

![](https://www.iso20022payments.com/wp-content/uploads/2023/06/5-Settlement-in-MI.png)

Generally, this article is related to the CBPR+ settlement, however, I thought that it would be a good idea to include one scenario with MI settlement.

The crucial difference between CBPR+ and MI settlement is that MI holds the accounts centrally for both Bank C and Bank B.

As MI holds the accounts centrally, it is responsible for the settlement.

Let’s investigate the diagram provided.

**(1)** **Bank C** holds an RTGS account in currency X in **MI**.

**MI** is responsible for the settlement.

**Bank C** sends pacs.009 to MI with **CLRG** settlement method.

**CLRG** settlement method is not part of CBPR+ specifications but instead is used in [HVPS+](https://www.iso20022payments.com/miscellaneous/iso-20022-market-implementations/).

**(2)** **NOTE:** If **MI** is unable to perform the settlement it sends pacs.002 (reject) to **Bank C**. This is because the settlement has not been performed.

In our scenario **, MI** performs the settlement and sends pacs.009 to Bank B with **C** **LRG** settlement method.

**(3)** Pacs.009 was settled in **MI**.

**Bank B** CANNOT reject this payment (pacs.002).

NOTE: Banks cannot send pacs.002 to MI.

If **Bank B** cannot process this payment it has to send pacs.004 – Payment Return.

**Bank B** puts **CLRG** settlement method because **MI** will settle this Payment Return.

**(4)** **NOTE:** If **MI** is unable to perform the settlement of this Payment Return it sends pacs.002 to **Bank B**. This is because the settlement has not been performed.

In our scenario **, MI** settles pacs.004 and sends pacs.004 to **Bank C** with **CLRG** settlement method.

**Scenario 6a – COVER settlement at Bank B**

![](https://www.iso20022payments.com/wp-content/uploads/2023/06/6a-COVER-settlement-at-Bank-B.png)

In this COVER scenario, I would like to focus on the last part of the payment chain.

Detailed information about COVER scenario was described in the dedicated article: [pacs.008 COVER method](https://www.iso20022payments.com/cbpr/pacs-008-cover-method/)

**(1)** **Bank A** holds a **VOSTRO** account for **Bank B**.

In the pacs.009 (COV) flow **Bank A** is the Creditor Agent and **Bank B** is the Creditor.

**Bank A** credits **VOSTRO** account of **Bank B**.

**Bank A** sends Account Statement (camt.053) and potentially Credit Notification (camt.054) to Bank B.

**(2)** **Bank B** reconciles pacs.008 with the camt. messages (notifications about covering funds being received) from **Bank A**.

**Bank B** credits the Creditor and sends the credit confirmation to the Creditor.

**(3)** Creditor requests the return of funds.

**(4)** **Bank B** already received funds on its account held at **Bank A**.

**Bank B** CANNOT send pacs.002 (reject) to **Bank A**.

**Bank B** sends pacs.004 with **INDA** settlement method because **Bank A** holds the account for **Bank B** and is **IN** strute **D A** gent in pacs.004.

**Please note that in the above scenario, I have not presented pacs.002 sent by Bank B to Bank X to reject pacs.008.**

This is because the settlement is completed by Bank B and only later, a return is initiated. Bank B does not send pacs.002 for the pacs.008 as this has been matched and completed on their side. In other words, pacs.008 is not an active pending message as far as Bank X is concerned.

Note that upon receipt of the Return Bank X should see within the tracker that the direct and cover message was completed, and the final beneficiary was credited. Therefore, no pacs.002 is needed for this pacs.008 flow and no Enquiry and Investigation message needed to enquire upon the status of the pacs.008.

**Scenario 6b – COVER no settlement at Bank B**

![](https://www.iso20022payments.com/wp-content/uploads/2023/06/6b-COVER-no-settlement-at-Bank-B.png)

This is the second scenario related to COVER payment.

Detailed information about COVER scenario was described in the dedicated article: [pacs.008 COVER method](https://www.iso20022payments.com/cbpr/pacs-008-cover-method/)

**(1)** **Bank A** holds a **VOSTRO** account for **Bank B**.

In the pacs.009 (COV) flow **Bank A** is the Creditor Agent and **Bank B** is the Creditor.

**Bank A** credits **VOSTRO** account of **Bank B**.

**Bank A** sends Account Statement (camt.053) and potentially Credit Notification (camt.054) to **Bank B**.

**(2) (3)** In this scenario there are no points 2 and 3, as **Bank B** cannot process this payment (e.g. Creditor Account is closed).

**(4)** **Bank B** already received funds on its account held at Bank A.

**Bank B** CANNOT send pacs.002 (reject) to **Bank A**.

**Bank B** reconciles pacs.008 with the camt. messages (notification about covering funds being received) from **Bank A**.

**Bank B** sends pacs.004 with **INDA** settlement method because **Bank A** holds the account for **Bank B** and is **IN** strute **D A** gent in pacs.004.

**Please note that in the 6b scenario I have not presented pacs.002 sent by Bank B to Bank X to reject pacs.008.**

In 6b scenario, the settlement by Bank B is not completed.

In such situations, we need to take into account some additional aspects.

For example, if Bank B received pacs.008 announcement earlier and already recognized (before the settlement of pacs.009 COV) that the payment cannot be completed as requested (e.g. Creditor Account is closed) it may also Reject pacs.008 with the pacs.002 message sent to Bank X. Nevertheless, also in this scenario, Bank B should arrange a Return of funds when they arrive.

Additionally, the pacs.002 may be needed when there is no tracker update to confirm the final credit and therefore it is not always possible for Bank X to know that Bank B has initiated the return and the pacs.008 can be assumed as null and void. Is such situations, it may be a good practice for Bank B to also send a pacs.002 Rejection message for the pacs.008 so that Bank X knows that the pacs.008 instruction is no longer active. This may avoid the need for an Enquiry and Investigation message to be sent.

For additional explanation, I would like to invite you to check the [PMPG](https://www.iso20022payments.com/miscellaneous/payments-market-practice-group/) document related to this topic: [Best Practice Guidance for the Return of Funds and Rejects of Payments.](https://www.swift.com/swift-resource/252097/download)

This is a very helpful document that contains many additional scenarios in the context of COVER payments. I highly recommend reading it.

This concludes the article. I am aware that it was quite complex and long but I hope it was also a bit interesting.

|     |     |
| --- | --- |
| [<< pacs.008 COVER method](https://www.iso20022payments.com/cbpr/pacs-008-cover-method/) | next page >> |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme