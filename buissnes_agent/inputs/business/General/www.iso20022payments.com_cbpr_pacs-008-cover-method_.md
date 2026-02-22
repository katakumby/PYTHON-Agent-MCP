---
url: "https://www.iso20022payments.com/cbpr/pacs-008-cover-method/"
title: "pacs.008 COVER method – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/cbpr/pacs-008-cover-method/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## CBPR+

## pacs.008 COVER method

In the previous article, we discussed pacs.008 processed via **SERIAL** method.

Today we are going to talk about **COVER** method.

**COVER method**

To begin with, let’s recap the basic features of **SERIAL** method to be able to see in what aspects they differ.

The **SERIAL** method means that the payment is sent through a ‘series’ of banks before it reaches the Creditor Agent.

In this method, for each pair of banks in the payment chain, there is a need for a direct account relationship, which allows the funds to move along the messages.

In other words, in **SERIAL** method **pacs.008** messages are sent from one financial institution to the next financial institution in the chain.

Each of the **pacs.008** messages exchanged in the payment chain:

- contains the necessary payment **information** for the next bank and for the Creditor Agent
- is also the **settlement instruction** that results in the bookings made in the involved banks

And this is where the key difference between **SERIAL** and **COVER** methods lies.

In **SERIAL** method one message ( **pacs.008**) is both the information as well as settlement instruction, however, **C****OVER** method decouples the settlement instruction from the payment information.

How is it done?

Well, in the first place it is worth noting that in the **COVER** method, there is only one **pacs.008** message exchanged.

This message is called an **Announcement.** It is usually sent to Creditor Agent and contains payment information.

It is crucial to understand that this **pacs.008** does not carry the funds (it is not a settlement instruction).

What is the role of **pacs.008 announcement**?

It advises the Creditor Agent:

- that funds are coming
- who the Creditor is
- from which reimbursement bank the funds will arrive

If **pacs.008 announcement** is not a settlement instruction, how does the settlement take place in **COVER** scenario?

Settlement is done via another message, which is **pacs.009 (COV)**.

The cover payment ( **pacs.009 COV**) is sent by the Debtor Agent to its correspondent and potentially goes through other agents until the funds reach the Creditor Agent.

So, in **COVER** method we have two types of messages:

- **pacs.008** – announcement (also called ‘direct’ message)
- **pacs.009 (COV)** – settlement instruction

Most often, the announcement is sent before the COVER payment. But this does not always have to be the case. It is possible that funds arrive at Creditor Agent before the announcement.

Here is the simple diagram that presents **COVER** method:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/COVER1.png)

As we can see two messages are initiated by **Bank A (Debtor Agent)** for this payment:

- **pacs.008 (announcement)** sent directly to **Bank B (Creditor Agent)**
- **pacs.009 (COV)** sent to **Bank C** (Bank A’s correspondent). This message starts the settlement process.

With **pacs.009 (COV)** funds start to move.

In the second step, **pacs.009 (COV)** is sent by **Bank C** (Bank A’s correspondent) to **Bank D** (Bank B’s correspondent).

It is worth noting that **pacs.009 (COV)** must only be used to order the movement of funds related to an underlying customer credit transfer **(pacs.008)**sent with the cover method. The **pacs.009 (COV)**must not be used for any other interbank transfer.

Now, here is an important question: What can we learn about the relationship between **Bank A** and **Bank B**?

There are two main things we should understand:

1. **Bank A** and **Bank B** do not have an account relationship in the currency of the transfer. If they had such a relationship Bank A would have sent pacs.008 without COVER method.
2. **Bank A** and **Bank B** can exchange SWIFT messages directly.

The proper RMA authorization must be in place which allows Bank A to send pacs.008 to Bank B.

These two points can be also viewed as the basic criteria for **Bank A** to choose the **COVER** method:

- The usage of **COVER** method makes sense for **Bank A** because there is no direct account relationship in the currency of the transfer with **Bank B**
- The usage of **COVER** method is only possible if **Bank A** has an RMA authorization to send pacs.008 directly to **Bank B**

There are also additional aspects that **Bank A** may take into account, while deciding about the method to be used.

- As negative criteria, **COVER** method may be excluded for certain currencies, countries or banks.
- As positive criteria, **COVER** method is usually perceived as faster and cheaper.

Let’s investigate further these two positive criteria.

Why is the **COVER** method considered a faster one?

Well, first of all, it is important to realize that in the above example, Creditor Agent ( **Bank B**) knows about the incoming payment from the start.

In the **SERIAL** method, this is not the case. **Bank B** would only know about the payment when the last **pacs.008** reaches Creditor Agent.

It is a crucial observation because, in the **COVER** method, **Bank B** may credit **Corporation Y** without waiting for the **COVER** payment.

Of course, it may be risky.

However, some banks may decide on such an approach if, for example:

- they trust the banks in the payment chain,
- the value of the payment is below a certain level, ect.

This makes the **COVER** payment faster, as the Creditor may receive the funds before the **COVER** message goes through all the intermediaries.

* * *

**Note:** In this context, it is worth mentioning that on path /Document/FIToFICstmrCdtTrf/CdtTrfTxInf/PmtTpInf/SvcLvl/Cd

there is a possibility to include the ExternalServiceLevel1Code. This code comes from the list published on the ISO official website (available **[here](https://www.iso20022.org/catalogue-messages/additional-content-messages/external-code-sets)**).

One of the codes is WFSM (WaitForSettlement) which means that the pacs.008 which contains this code is to be treated as advice only and funds should be applied to the account of the creditor or next agent only after settlement of the cover has been confirmed.

This code word was registered by the PMPG. More about this group you can find **[here](https://www.iso20022payments.com/miscellaneous/payments-market-practice-group/)**.

PMPG refers to this code stating that this codeword should be bilaterally agreed upon.

An interesting PMPG paper about Cover Payments (where WFSM is also discussed) is available **[here.](https://www.swift.com/swift-resource/251596/download)**

* * *

Why is the COVER method considered a cheaper one?

This aspect relates to charges.

As you may remember, charges are only associated with the **pacs.008** messages. There is no charges for **pacs.009 (COV)** messages.

In the **COVER** scenario there is only one **pacs.008** exchanged.

In the **SERIAL** method there may be several **pacs.008** messages exchanged between many banks, where each bank applies its own charges.

Because of that, **COVER** method is considered to be the cheapest option for customers.

**other COVER scenarios**

In this section, I would like to show the richness of the payment flows that include **COVER** method.

To begin with, let’s remind ourselves of the **‘basic’ COVER** scenario.

Each of the next scenarios in this section will differ in some aspect from this one.

I will highlight in the diagrams what is different and explain why.

- **Basic scenario**

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/COVER1.png)

As we already know, in this basic scenario **Bank A** decides to process the payments via **COVER** method which means that it sends:

- **pacs.008 announcement** to **Bank B**
- **pacs.009 (COV)** to **Bank C**

The funds from **Bank A** to **Bank B** travel through **Bank C** and **Bank D**.

**Bank C** and **Bank D** are called **Reimbursement Agents**.

**Bank C** is the **Instructing Reimbursement Agent**. Instructing Reimbursement Agent captures the Agent who will execute a covering payment ( **pacs.009 COV**) and is often referred to as the currency correspondent.

**Bank D** is the **Instructed Reimbursement Agent**. Instructed Reimbursement Agent captures the Agent who will receive the covering payment ( **pacs.009 COV**) and credit the account of **Bank B**.

Is it possible that there are more than two Reimbursement Agents in the payment chain?

Let’s see the next scenario.

- **3 reimbursement banks**

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/other3banks.png)

As we can see the number of Reimbursement Agents can differ depending on the scenario.

In certain scenarios, it is possible to use one Reimbursement Agent.

But it is also possible to use three Reimbursement Agents.

This scenario is depicted in the diagram above.

According to the CBPR+ UHB, the **Third Reimbursement Agent**captures an additional Agent who will receive the covering payment, where this is not the Agent detailed in the **Instructed Reimbursement Agent**.

In this scenario, **Bank E** will play the role of the **Third Reimbursement Agent**.

It is worth noting that in CBPR+ there is a CrossElementComplexRule stating that if ThirdReimbursementAgent is present, then InstructingReimbursementAgent and InstructedReimbursementAgent must both be present.

As for now, we have analyzed the scenarios where settlement is done based on the correspondent banking relationship.

This, however, does not have to be the case, as we will see in the next example.

- **COVER via Payment System**

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/othersMI.png)

This is an example where **Bank C** processes payment via **Payment Market Infrastructure**, for example, an RTGS system.

What is different in this scenario is that **Bank C** and **Bank D** do not need to have a direct account relationship in the currency of the transfer.

**Bank C** reaches **Bank D** via the **Payment System** which holds the account for both **Bank C** and **Bank D**.

If there is no account relationship, what **Settlement Method** will **Bank C** use for the **pacs.009 (COV)**:

INGA or INDA? (see [Settlement Method: INGA vs. INDA](https://www.iso20022payments.com/cbpr/settlement-method-inga-inda/))

Neither of them.

**Bank C** sends the **pacs.009 (COV)** with Settlement Method **CLRG**.

**Settlement Method** code **CLRG** is not part of CBPR+ specifications but instead, it is used in Market Infrastructure specification ( [HVPS+](https://www.iso20022payments.com/miscellaneous/iso-20022-market-implementations/)).

What is also important to note is that the messages sent from **Bank C** to **MI** and from **MI** to **Bank D** are not CBPR+ messages, but follow the specifications of MI.

In the above example, we see that **pacs.009 (COV)** is sent via **Payment System**.

We can ask: Is it possible that **pacs.008 announcement** is sent by **Payment System**?

The answer is NO.

**Pacs.008 announcement** is never sent via **Payment System**.

Why?

Well, when **pacs.008** is processed via **Payment System** (it is possible in **SERIAL** method) it means that **pacs.008** is a settlement instruction and is settled in **Payment System**.

And as we discussed earlier **pacs.008 announcement** is not supposed to be the settlement instruction, meaning it does not carry funds.

**Pacs.008 announcement** should be settled via **pacs.009 (COV)**.

And **pacs.009 (COV)** can be settled via a correspondent banking relationship as well as via Payment System.

There is another important aspect that we should investigate in this scenario:

As we can see **Bank D** does not send **pacs.009 (COV)** to **Bank B**.

Why is that?

This is because **Bank D** holds an account for **Bank B**. In other words, **Bank D** is Account Servicing Institution.

It credits the account of **Bank B** and sends **camt.054** (Debit Credit Notification) and **camt.053** (Account Statement).

Upon receiving funds in its account with **Bank D**, **Bank B** can reconcile **pacs.008 announcement** with the **camt** messages it receives from **Bank D**.

This is an important aspect of **COVER** processing chain.

But, are there any scenarios where **Bank B** receives **pacs.009 (COV)** instead of **camt** messages?

One of such scenario is described below.

- **pacs.009 (COV) sent to Creditor Agent**

So, when is it possible that **Bank B** receives **pacs.009 (COV)**?

It is possible if the **Market Infrastructure** is involved in the payment chain.

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/others-pacs.009COV-to-Debtor-Agent.png)

As we can see in the above diagram **Bank C** reaches **Bank B** via a **Payment System**.

**Pacs.009 (COV)** is settled in the **Payment System**.

The **pacs.009 (COV)** is sent from the **Payment System** to **Bank B** to inform **Bank B** about the settlement.

To understand this flow I would propose to look at this issue in the following way.

The goal of the payment is that **Bank B** credits the account of **Corporation Y**.

Crediting of **Corporation Y** is possible if **Bank B** receives the funds in its account.

**Bank B** account to be credited can be held either:

- centrally in the Payment System:

This is depicted in this scenario.

**Bank C** initiates the settlement in the **Payment System** via **pacs.009 (COV)**. **Bank B** receives funds in its account in the **Payment System**.

**Pacs.009 (COV)** is forwarded to **Bank B** after the settlement takes place in the **Payment System**.

aaaaaaaaaa
- in another Bank.

This option was depicted in the previous scenarios.

If **Bank B** receives funds on its Nostro account held in another bank, this bank will not send the **pacs.009 (COV)** to **Bank B**.

Instead, **camt** messages will be sent to **Bank B** to report the credit done to **Bank’s B** account.

- **SERIAL with COVER**

The last scenario describes the situation where both **SERIAL** and **COVER** methods are used together in the payment chain.

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/others-with-Serial.png)

Some scenarios include both methods. This depends mainly on the account relationships and RMA authorizations.

In the diagram, we can see that:

- the payment initiated by **Bank E** to **Bank A** is sent via **SERIAL** method.

aaa
- **Bank A** sends the payment to **Bank B** via **COVER** method.

Why **Bank A** does not send the **pacs.008 announcement** directly to **Bank F**?

It’s an important question. When using **COVER** method an announcement should be sent as close to the Creditor Agent as possible.

Sometimes, however, it may not be possible to reach Creditor Agent.

For example, **Bank A** may not have RMA authorization to send **pacs.008** to **Bank F**.

aaa
- **Bank B** processes the payment further to **Bank F** via **SERIAL** method.

The above diagram presents the situation where **COVER** method has both legs (leg-in and leg-out) sent as **SERIAL** payments.

Of course, it does not have to be the case. Sometimes, only one leg can be present.

Additionally, the **SERIAL** leg can be longer and include several agents before/after the payment is processed via **COVER** method.

**pacs.008 and pacs.009 (COV)**

**– relation between messages –**

In this section of the article, I am going to investigate the relationship between the two messages that form **COVER** payment.

Let’s start with the following question:

**How to identify that the particular message is part of the COVER scenario?**

Let’s imagine that the message arrived at our bank. How to recognize that this message is part of the COVER method?

Well, the key indicators are the following:

- **in pacs.008:**


  - The settlement method **COVE** is used.

    **COVE**indicates that this Customer Credit Transfer will be settled using a covering **pacs.009 (COV)**.
  - The presence of **Reimbursement Agents** elements in the Group Header also indicates that **pacs.008** is sent via **COVER** method.

    In fact, there is a CrossElementComplexRule stating that if SettlementMethod is equal to **COVE**, then **InstructedReimbursementAgent** or **InstructingReimbursementAgent** must be present.
- **in pacs.009 (COV)**:


  - in the BAH the Business Service element contains value: **swift.cbprplus.cov.02**
  - there is an **Underlying Customer Credit Transfer** element present in the **pacs.009 (COV)** message instance.

    This element differentiates a **pacs.009 (COV)** from **pacs.009 CORE**.

The second interesting question is:

**How can we link both messages as being part of the same payment?**

The main elements that link the **pacs.008 announcement** and **pacs.009 (COV)** are references.

Even if two types of messages are used in **COVER** method, for SWIFT all the messages in the **COVER** method form the same transaction.

Because of that **pacs.008** and **pacs.009 (COV)** should have **the same UETR**.

Another interlinking is that, in the **pacs.009 (COV)** the **End to End Identification** should contain the **Instruction Identification** from the underlying **pacs.008**.

These requirements both form TextualRules in CBPR+ Usage Guidelines:

## **Rule “CBPR\_E2E\_COV\_TextualRule**“

_In the pacs.009 COV, the E2E identification should transport the instruction identification of the underlying pacs.008._

## **Rule “CBPR\_UETR\_COV\_TextualRule”**

_In the pacs.009 COV, the UETR should transport the UETR of the underlying pacs.008._

The last question relates to the parties’ roles in the messages:

**What are the changes in the parties’ roles between the messages:**

**Pacs.008** is a Customer Credit Transfer, which means that **either Debtor or Creditor is Non-Fi.**

**Pacs.009 (COV)** is a Financial Institution Credit Transfer Cover message sent by a **Debtor Financial Institution to a Creditor Financial Institution**.

It is important to recognize that some roles change between these parallel messages.

Below I present what roles banks play in the **pacs.008** and what roles they play in **pacs.009 (COV)**.

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/Parties-1.png)

**Bank A** is **Debtor Agent** in **pacs.008** but in **pacs.009 (COV)** it is **Debtor**.

**Bank B** is **Creditor Agent** in **pacs.008** but in **pacs.009 (COV)** it is **Creditor**.

**Bank C** is **Instructing Reimbursement Agent** in **pacs.008** but in **pacs.009 (COV)** it is **Debtor Agent**.

**Bank D** is **Instructed Reimbursement Agent** in **pacs.008** but in **pacs.009 (COV)** it is **Creditor Agent**.

The change in the roles comes from the fact that the chain of parties involved in **pacs.008** is different that the chain of parties involved in **pacs.009 (COV)**.

**pacs.008 COVER method**

**– our business scenario –**

Now, I would like to introduce you to our business scenario.

Here it is:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008-COVER-our-business-scenario.png)

In our scenario, **Corporation X** (Singapore) has to pay **Corporation Y** JPY 1000000.

**Corporation X** is the **Debtor** and holds its account with **Bank A** ( **Debtor Agent**).

**Corporation Y** is the **Creditor** based in the UK. It holds an account with **Bank B** ( **Creditor Agent**) based also in the UK.

Since the payment is in JPY, there is a need for both Bank A’s JPY correspondent ( **Bank C**) and Bank B’s JPY correspondent ( **Bank D**) to be involved.

Based on the correspondent arrangements both **Bank A** and **Bank B** offer JPY accounts to their customers, **Corporation X** and **Corporation Y** respectively.

Payment is initiated by **pain.001** sent by **Corporation X** ( **Debtor**) to **Bank A** ( **Debtor Agent**).

Let’s assume that **Corporation X** provided the following information in **pain.001** sent to **Bank A**:

- EndToEndId: **CORPORATIONXENDTOENDID**
- UETR: **d0b7077f-49fb-42ed-b78d-af331c0e5012**
- Requested Execution Date: **2023-04-21**
- Instructed Amount: **JPY 1000000**
- Charge Bearer: **SHAR**
- Debtor: **Corporation X**
- Debtor Agent: **BANKSGAAXXX**
- Creditor Agent: **BANKGBBBXXX**
- Creditor: **Corporation Y**
- Remittance Information: **Contract 123**

Based on the above information we are now going to explore **pacs.008** sent by **Bank A** to **Bank B**.

The message comprises both **BAH** and **pacs.008 message instance**.

Let’s start with **BAH**.

**Business Application Header**

![](https://www.iso20022payments.com/wp-content/uploads/2023/06/pacs.008COVER-BAH3.png)

As you may remember, the BAH **From** element identifies the BIC of the party who created the Business Document (in our case **pacs.008**), and **To** element identifies the BIC of the party who will ultimately process the Business Document.

These two elements can also be understood as Sender and Receiver.

It’s worth highlighting that according to the CBPR+ rule BAH **From** BIC must match **Instructing Agent** BIC and BAH **To** BIC must match **Instructed Agent** BIC.

So, in our scenario **From** element contains BIC of **Bank A** ( **Instructing Agent**) and **To** element contains BIC of **Bank B** ( **Instructed Agent**).

**Business Message Identifier** has to be the same as **Message Identification** captured within the Business Document’s Group Header. It contains **Bank A’s** reference.

**Message Definition Identifier** is pacs.008.001.08.

**Business Service** for pacs.008 is swift.cbprplus.02.

**Creation Date** captures the date and time when the Business Application Header was created.

You can learn more about the format of this element in [UTC offset](https://www.iso20022payments.com/miscellaneous/utc-offset/) article.

The **BAH** is attached to the **pacs.008 message instance** which contains further business information.

The first element in the **pacs.008** is **Group Header**.

**Group Header**

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008COVERGrH2.png)

**Message Identification** element is a [point-to-point reference](https://www.iso20022payments.com/cbpr/point-to-point-end-to-end/) used to unambiguously identify the message.

Point-to-point means that this is an element created by **Bank A** (sender of the message).

It has to be the same as **Business Message Identifier** from **BAH**.

**Creation Date** captures the date and time when the message was created. You can learn more about the format of this element in [UTC offset](https://www.iso20022payments.com/miscellaneous/utc-offset/) article.

**Number of Transactions** in CBPR+ payment usage guidelines is fixed to 1.

**Settlement Method** indicates how the payment leg is settled.

**COVE** means that **pacs.008** is an announcement, that will be settled via **pacs.009 (COV)**.

The **Instructing Reimbursement Agent** captures the Agent who will execute a covering payment ( **pacs.009 COV**).

In our scenario, it is **Bank C** (Bank A’s JPY correspondent).

The **Instructed Reimbursement Agent** captures the Agent who will receive the covering payment ( **pacs.009 COV**).

In our scenario, it is **Bank D** (Bank B’s JPY correspondent).

After **Group Header** there is a **Credit Transfer Transaction Information** element in **pacs.008**.

It contains the remaining business information about the payment.

These are the first nested elements under **Credit Transfer Transaction Information:**

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008COVERInstrA.png)

In **Payment Identification,** there are three references:

- **Instruction Identification**– a point-to-point reference restricted in CBPR+ to 16 characters. This is the reference of **Bank A** (sender of the message).

In our example, I used the same references that **Bank A** populated in **GrpHdr/MsgId** (pacs008BANKAREF), but this is not required. **Bank A** can populate in **Instruction Identification** other references which make sense from their point of view.

aaaaaaaaaaaaaa
- **End to End Identification –** an end-to-end reference provided by the Debtor which must be passed unchanged throughout the payment chain and reported to the Creditor. This is the reference that **Corporation X** populated in the **pain.001**. It is now forwarded by **Bank A** in **pacs.008**.

Later on, **Bank B** will report it to **Corporation Y**.

**Note:** If Debtor has not provided an end-to-end identifier, Debtor Agent may populate “NOTPROVIDED” to comply with the mandatory need of this element.

aaaaaaaaaaa
- **UETR –** the end-to-end Transaction Reference created using the UUIDv4 standard. This reference must be passed unchanged throughout the payment chain. This is the reference that **Corporation X** populated in the **pain.001**.

Similarly to **End to End Identification,** it is now forwarded by **Bank A** in **pacs.008**.

**Note:** If UETR is not provided by Debtor, Debtor Agent creates the UETR.

You can learn more about different kinds of references in [Point-to-point vs. End-to-end](https://iso20022payments.com/cbpr/point-to-point-end-to-end/) article.

**Interbank Settlement Amount** contains the amount that **Bank A** sends to **Bank B**. You can learn about the format of this element in [Currency and Amount](https://www.iso20022payments.com/miscellaneous/currency-and-amount/) article.

As in our example **Instructed Amount** in **pain.001** was in the same currency and amount (JPY 1000000) as **Interbank Settlement Amount** in **pacs.008**, **Bank A** does not need to include **Instructed Amount** element in **pacs.008**.

**Charge Bearer** specifies which party would bear charges. **SHAR** means that charges are shared. More information about [Charges](https://www.iso20022payments.com/cbpr/charges/) is available in a dedicated article.

**Interbank Settlement Date** contains the date when the payment should be executed.

In the **pacs.008**, **Bank A** is the **Instructing Agent** (Sender) and **Bank B** is the **Instructed Agent** (Receiver).

As it was explained above according to the CBPR+ rule BAH **From** BIC must match **Instructing Agent** BIC and BAH **To** BIC must match **Instructed Agent** BIC.

The next part of the message contains information about **Debtor**:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008COVERdebtor.png)

**Corporation X** is our **Debtor** and **Bank A** is **Debtor Agent**. **Debtor Agent** ( **Bank A**) services the JPY account for the **Debtor** ( **Corporation X**).

**Debtor Account** is provided in the proprietary format.

As you can see the **Debtor** is identified via **Name** and **Postal Address**. You can learn about it in the following article: [Debtor and Creditor data (FATF 16)](https://www.iso20022payments.com/miscellaneous/debtor-and-creditor-data-fatf-16/)

The same way of identification applies also to the **Creditor** which is included in the next part of the message:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008COVERcreditor2.png)

**Creditor Agent** ( **Bank B**) services the JPY account for the **Creditor** ( **Corporation Y**).

Here **Creditor Account** is provided as an IBAN.

The last element of the message is **Remittance Information** which enables the reconciliation of the payment.

If you are interested, the file analyzed above can be accessed here: [pacs.008 COVER A to B](https://www.iso20022payments.com/wp-content/uploads/2023/06/pacs.008COVER-A-to-B.txt)

I checked this message in the CBPR+ Readiness Portal, and this file is a valid message.

The warnings in the Portal relate only to the Envelope and BIC & IBAN data, which, of course, are fictitious.

**pacs.009 (COV)**

**– our business scenario –**

In the last part of this article, we are going to explore **pacs.009 (COV)** message.

As we know **pacs.009 (COV)** is used as the cover payment for **pacs.008 announcement**.

Is there any difference in the structure between **pacs.009 (core)** and **pacs.009 (COV)**?

Yes, it is.

We analyzed **pacs.009 (core)** in the earlier article ( [here](https://www.iso20022payments.com/cbpr/pacs-009-core/)).

As we have seen **pacs.009 (core)** comprises the following parts:

- **Group Header**
- **Credit Transfer Transaction Information**

**Pacs.009 (COV)** contains these two parts but also includes information on the **Underlying Customer Credit Transfer** ( **pacs.008**):

- **Group Header**
- **Credit Transfer Transaction Information**


  - **Underlying Customer Credit Transfer**

So, what is this **Underlying Customer Credit Transfer**element?

To put is simply, this element contains information about the corresponding **pacs.008 announcement**.

Thanks to this element the business part of the **pacs.008 announcement** can be also included in the **pacs.009 (COV)**.

It is presented in CBPR+ UHB in the following way:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/Underlying-Customer-Creditr-Transfer.png)

Ok. Let’s now explore the details of **pacs.009 (COV)**.

As we know, **pacs.009 (COV)** is sent by a Debtor Financial Institution to a Creditor Financial Institution. Both **Debtor** and **Creditor** are Financial Institutions.

Below we are going to investigate the **pacs.009 (COV)** sent by **Bank A** to **Bank C**.

As always let’s start with the **BAH**.

**Business Application Header**

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.009COVERBAH2.png)

As you may remember, the BAH **From** element identifies the BIC of the party who created the Business Document (in our case **pacs.009 (COV)**), and **To** element identifies the BIC of the party who will ultimately process the Business Document.

These two elements can also be understood as Sender and Receiver.

It’s worth highlighting that according to the CBPR+ rule BAH **From** BIC must match **Instructing Agent** BIC and BAH **To** BIC must match **Instructed Agent** BIC.

So, in our scenario **From** element contains BIC of **Bank A** ( **Instructing Agent**) and **To** element contains BIC of **Bank C** ( **Instructed Agent**).

**Business Message Identifier** has to be the same as **Message Identification** captured within the Business Document’s Group Header. It contains **Bank A’s** reference for **pacs.009 (COV)**.

**Message Definition Identifier** is pacs.009.001.08.

**Business Service** for pacs.009 (COV) is swift.cbprplus.cov.02.

**Creation Date** captures the date and time when the Business Application Header was created.

You can learn more about the format of this element in [UTC offset](https://www.iso20022payments.com/miscellaneous/utc-offset/) article.

The **BAH** is attached to the **pacs.009 (COV)message instance** which contains further business information.

The first element in the **pacs.009 (COV)** is **Group Header**.

**Group Header**

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.009COVERGrH2.png)

**Message Identification** is a point-to-point reference used to unambiguously identify the message.

Point-to-point means that this is an element created by **Bank A** (sender of the message). It has to be the same as **Business Message Identifier** from **BAH**.

**Number of Transactions** in CBPR+ payment usage guidelines is fixed to 1.

The **pacs.009 (COV)** **Settlement Method**element includes one of the embedded codes to indicate how the payment message will be settled.

**INDA** indicates that this payment leg will be settled by the **Instructed Agent** – **Bank C** (as the Account Servicing Institution). **Bank C** is **Bank A’s correspondent** and it holds **Bank A’s JPY account**.

After **Group Header** there is a **Credit Transfer Transaction  Information**element in **pacs.009 (COV)**.

These are the nested elements under **Credit Transfer Transaction Information:**

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.009COVERCdtTRfTxInf.png)

In **Payment Identification,** there are three references.

To make it very clear what the relationship between the references in both messages is, I have prepared this diagram:

![](https://www.iso20022payments.com/wp-content/uploads/2023/06/references.png)

As we can see:

- **Instruction Identification** in **pacs.009 (COV)** is not related to **pacs.008**. It is a point-to-point reference restricted in CBPR+ to 16 characters.

This is the reference of **Bank A** (sender of the message).

In our example, I used the same references that **Bank A** populated in **GrpHdr/MsgId** (pacs009BANKAREF), but this is not required.

**Bank A** could populate in **Instruction Identification** other references which make sense from their point of view.

aaaaaaaaaaaaaa
- **End to End Identification –** for **pacs.009 (COV)** the **end-to-end ID** is the same as **Instruction ID** used in **pacs.008 announcement**(pacs008BANKAREF).

aaaaaaaaaaa
- **UETR –** for **pacs.009 (COV)** the **UETR** is the same as **UETR** used in **pacs.008 announcement**.

**Interbank Settlement Amount** is present in the **pacs.009 (COV)** as it was in **pacs.008**.

**Interbank Settlement Date** contains the date when the payment should be executed.

At the start of the transaction flow, the **Instructing Agent** in **pacs.009 (COV)** is the same as in the **pacs.008**.

**Bank A** sends both announcement as well as COVER message.

The **Instructed Agent** is however different. The **Instructed Agent** in **pacs.009 (COV)** is **Bank C**.

As we discussed earlier in the article the roles of the banks in **pacs.009 (COV)** are different from the roles in **pacs.008 anouncement**.

**Debtor** in the **pacs.009 (COV)** is the **Debtor Agent** from the **pacs.008 – Bank A**.

**Creditor** in the **pacs.009 (COV)** is the **Creditor Agent** from the **pacs.008 – Bank B**.

**Debtor Agent** in the **pacs.009 (COV)** is the **Instructing Reimbursement Agent** from the **pacs.008 – Bank C**.

**Creditor Agent** in the **pacs.009 (COV)** is the **Instructed Reimbursement Agent** from the **pacs.008 – Bank D**.

The last element in **pacs.009 (COV)** is **Underlying Customer Credit Transfer.**

It contains the information from **pacs.008 announcement**.

This is the debit side:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.009COVERdebtor.png)

And this is the credit side:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.009COVERCreditor2.png)

In **Underlying Customer Credit****Transfer:**

- Debtor
- Debtor Agent
- Creditor Agent
- Creditor

are mandatory elements.

These four elements are always required as a strict minimum.

They are copied from the **pacs.008**.

Also other relevant information, for example, **Remittance Information** from the **pacs.008** should be copied into the **Underlying Customer Credit** **Transfer****Remittance Information**element in the **pacs.009 (COV)**.

According to the CBPR+ UHB only **Instruction for Creditor Agent**from the **pacs.008** does not need to be included in the **pacs.009 (COV)**.

If you are interested, the file analyzed above can be accessed here: [pacs.009 COVER A to C](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.009-COVER-A-to-C.txt)

I checked this message in the CBPR+ Readiness Portal, and this file is a valid message.

This concludes this article. I hope it was interesting.

|     |     |
| --- | --- |
| [<< pacs.008 SERIAL method](https://www.iso20022payments.com/cbpr/pacs-008-serial-method/) | [Reject & Return >>](https://www.iso20022payments.com/cbpr/reject-return/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme