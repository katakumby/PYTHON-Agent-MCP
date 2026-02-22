---
url: "https://www.iso20022payments.com/cbpr/pain-001-pain-002/"
title: "pain.001 & pain.002 – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/cbpr/pain-001-pain-002/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## CBPR+

## pain.001 & pain.002

In the previous articles, we discussed interbank payments. In interbank payments, both Debtor and Creditor are Financial Institutions.

Now we are shifting our attention. We are going to include in our analysis also non-FI parties. Two main categories of messages that include non-FI parties are Customer Credit Transfer Initiation (pain.001) and Customer Credit Transfer (pacs.008).

From the names, we can already see that pain.001 is the message that initiates pacs.008.

In this article, I will describe pain.001 which I hope will give us a good background for the pacs.008 exploration in the next article.

So, as I said pain.001.001.09 is a Customer Credit Transfer Initiation message. The response to this message is pain.002.001.10 – Customer Payment Status Report.

In this article, I am going to investigate both of these messages.

But let’s start with pain.001.

Traditionally I would like to begin with placing the pain.001 in the diagram that includes different ISO 20022 implementations: [ISO 20022 market implementations](https://www.iso20022payments.com/miscellaneous/iso-20022-market-implementations/)

**pain.001 in the broader context**

If we put the pain.001 in the diagram we can see that there are many scenarios where this message is used.

![](https://www.iso20022payments.com/wp-content/uploads/2023/03/pain.001-diagram.png)

As we already said, pain.001 is a message that initiates the customer payment. In other words, it’s sent to request the movement of funds.

We can see in the above diagram that this message can be exchanged in both Customer-to-Bank as well as Bank-to-Bank space.

I will start off by explaining the scenarios with pain.001 processed in the Customer-to-Bank space.

As the name suggests Customer-to-Bank space cover messages that are initiated by the customers. But, who is a customer?

This term may relate to any client of the bank. So, as customers, we can understand both big corporations as well as natural persons.

In the above diagram, we see Corporation X as an example of a bank’s customer. We can easily understand that big corporation can have SWIFT interface and the ability to send pain.001 message to its bank.

But, what about me and you? Do we send pain.001 messages?

If I would like to initiate the cross-border payment I could use the online banking portal to submit the order.

I do not see what happens next, but my bank may format my order into the pain.001 and send it to its payment engine.

In this way, banks are able to automatically process any payment initiation regardless of the channel where it was initiated.

But of course, this depends on the bank’s agreement with their customers as well as the interfaces that the bank’s channel has with the bank’s payment engine.

Instead of pain.001 also other agreed proprietary messages for instructing a payment initiation request can be used.

**So, let’s get back to our scenarios of pain.001 exchanged in Customer-to-Bank space:**

**(** **1** **)**First scenario comprises only one pain.001 sent by Corporation X to Bank A. Why there is no other messages in this scenario? It is because both Debtor’s and Creditor’s accounts are in the same bank – in our case Bank A. We can say that for Bank Athis transaction can be categorized both as from us (we hold the Debtor’s account) as well as on us (we hold the account for the Creditor). This is an example of intrabank payment. There is no need to send any further payment messages. This kind of transaction is sometimes called an in-house payment or book transfer.

**(** **2** **)**In the second scenario we can see that upon receiving pain.001 from Corporation X Bank A sends pacs.008 to Bank B, and Bank B subsequently sends another pacs.008 to Bank C.

If Bank A sends pacs.008 it means that the payment is from us (we hold the Debtor’s account) but is not on us (we do not hold the account for the Creditor). In order to make the Creditor receive the funds, we have to send the Customer Credit Transfer to the Bank that holds Creditor’s account.

Bank A does not send pain.001 but it sends pacs.008. This is because Bank A is Debtor Agent. When the Debtor’s account is debited, the next message in the chain is no longer a payment initiation. Pain.001 becomes pacs.008 – Customer Credit Transfer. We are going to discuss this payment in the next article.

And why Bank A does not send pacs.008 directly to Bank C, where the Creditor’s account is held? This is because these two banks do not have the necessary bilateral account relationship.

**(** **6** **)**The last example, at the bottom of the diagram is similar to the second one we have just discussed. Here I just wanted to highlight that when Bank A sends pacs.008 it may be further processed also by the Market Infrastructure. In the diagram Bank B reaches Bank D via the Payment System.

**In the above scenarios, pain.001 was only processed in the Customer-to-Bank space and not in the Bank-to-Bank space.**

**As we are discussing CBPR+, let’s now focus on the scenarios where pain.001 may be processed according to the CBPR+ rules in the Bank-to-Bank space.**

**CBPR+ UHB describes three such scenarios:**

**(** **3** **)**In the third scenario Corporation X sends pain.001 to Bank A but Bank A forwards pain.001 to Bank B. In other words, Bank A does not start the payment but needs to forward the payment initiation request to Bank B. Why is that?

This is because Bank A does not hold the account for Corporation X. If Bank does not hold the Debtor’s account it cannot start Customer Credit Transfer (pacs.008), but has to forward Payment Initiation request (pain.001) to the Debtor bank – in our case Bank B. And Bank B upon receipt of the pain.001, debits the Debtor’s account (Corporation X) and sends the pacs.008 message to Creditor Agent – Bank C.

In CBPR+ UHB this scenario is called **Relay**scenario. In this scenario Bank A plays the role of Forwarding Agent – it forwards the pain.001 message to the Debtor Agent.

But, you may wonder why relayed scenarios even exist.

Why a corporate does not want to send the pain.001 always to the Bank where the account to be debited is held?

In other words, why Corporation X does not send pain.001 directly to Bank B?

This is indeed an interesting question.

We are going to investigate this use case further in this article (while discussing pain.001 business scenario below), so I hope it will then become more evident.

**(4** **)**This scenario is called in CBPR+ UHB **Authorised Party Initiation.**

Here there is no pain.001 sent from Corporation X to Bank A. In this scenario, it is Bank A that initiates the payment. So, Bank A plays the role of theInitiating Party in the message.

However, Bank A does not act on its behalf.

In this payment, the Debtor is still Corporation X.

Bank A has, however, authorization to initiate payment on behalf of Corporation X.

Bank A sends the pain.001 to Bank B – Debtor Agent.

To process the payment Bank B has to know that Bank A is authorized to execute payments from Corporation X’s account held by Bank B. In other words, as a pre-requisite Corporation X provides Debit Authorisation to Bank B, which allows Bank A to initiate payment from their account.

As Bank B does not hold the Creditor’s account, after having debited Corporation X’s account it sends pacs.008 to Bank C – Creditor Agent.

This scenario may be relevant for example for a multi-bank liquidity sweep (sweep excess of funds from the corporation subsidiary’s account in Bank B to the master account with Bank C).

**(5** **)**When we look at the diagram this scenario looks almost the same as the previous one. Bank A sends pain.001 to Bank B, and Bank B sends pacs.008 to Bank C.

The difference is that in the previous example, Bank A sent the pain.001 on behalf of Corporation X and now Bank A has initiated the payment on its own behalf.

This scenario is called **Financial Institution Payment Initiation**.

Bank A is here both the Debtor and Initiating Party.

But, you may ask: Didn’t we say that Customer Payment involves non-FI parties?

Bank A is a Debtor and is certainly a Financial Institution.

Good point. Let’s clarify it further.

Customer Payment Initiation has to involve a non-FI party, but it does not mean that both Debtor and Creditor have to be non-FI parties. It means that either Debtor or Creditor has to be a non-FI party.

In this scenario Bank A as a Debtor is FI but the Creditor will be a non-FI party.

So, Bank A wants to initiate the payment from their account in Bank B towards non-FI Creditor, which holds an account in Bank C.

**Remark:** Please note that there is one big difference between messages exchanged in the Customer-to-Bank space and the Bank-to-Bank space.

Pain.001 and pacs.008 sent via CBPR+ have to transport only one transaction.

This is however not the case for Customer-to-Bank space.

In CGI documentation on MyStandards, there are two pain.001 Usage Guidelines, shown below.

![](https://www.iso20022payments.com/wp-content/uploads/2023/03/pain.001-Number-of-Transactions.png)

In the picture, we can see two Usage Guidelines: one for **Relay** scenario and the second one for **Urgent Wires & International** payments.

As the **Relay** pain.001 payment initiation is sent into the interbank messaging network, CGI indicates that it must contain single payment.

However, the second pain.001 Usage Guidelines for **Urgent Wires & International** does not have this restriction. Nevertheless, when CBPR+ or HVPS+ pacs.008 is built based on this pain.001 it has to be a message with one single transaction. In other words, if one CGI pain.001 has more than one transaction it will result in more than one CBPR+ or HVPS+ pacs.008 messages.

**pain.001**

**– parties –**

Now I would like to recap the different parties that can appear in the pain.001. I hope this will complement well the scenarios that I described above:

**Initiating Party:** Party that initiates the payment, which may be:

- the Debtor or
- an authorized Party acting on behalf of the Debtor (for example, the Head Office which has the authority to debit the account of its subsidiary)

**Forwarding Agent:** Financial Institution that receives the instruction from the Initiating Party and forwards it to the next agent in the payment chain for execution. This element is mandatory in CBPR+ only for **Relay** scenario. For the Authorised Party Initiation and FI Payment Initiation use cases, Forwarding Agent is not required.

**Ultimate Debtor:** The Ultimate Debtor element should not be confused with an Initiating Party who may send a payment initiation request on behalf of the Debtor. Ultimate Debtor has no financially regulated direct account relationship with the corresponding Debtor. An example of an Ultimate Debtor is an Individual that requests payment in a Money Transfer Bureau. Money Transfer Bureau will execute this payment as a Debtor in their bank (Debtor Agent).

**Debtor:** Party that owes an amount of money to the (ultimate) creditor. It is the party whose account is debited for a transaction.

**Debtor Agent:** Financial Institution servicing an account for the Debtor. Debtor Agent is a static role in the pain.001 Customer Credit Transfer Initiation. This agent maintains a relationship with their customer (Debtor).

**Intermediary Agent (1,2 and 3):** These agents represent the agent(s) that exist between the Debtor Agent and the Creditor Agent.

**Creditor Agent:** Financial Institution servicing an account for the Creditor.

**Creditor:** Party to which an amount of money is due. The ISO 20022 pain messages describe the Creditor as the party whose account was credited for a transaction.

**Ultimate Creditor:** Similar logicto the Ultimate Debtor. Ultimate Creditor has no financially regulated account relationship with the corresponding Creditor.

**pain.001**

**– business scenario –**

Now, I think is high time we dived into a business scenario.

Here is a diagram presenting the scenario I chose for pain.001.

![](https://www.iso20022payments.com/wp-content/uploads/2023/03/pain.001-business-scenario.png)

There are two corporations and three banks in this scenario.

Corporation X in the UK wants to make a EUR payment to Corporation Y in Belgium. Bank C in Belgium holds an account for Corporation Y. It is the Creditor Agent.

Bank C holds also a EUR Nostro account for Bank B.

As Bank B has its EUR correspondent (Bank C) it offers its clients the possibility to have EUR accounts. Corporation X is one of Bank B’s customers that have EUR account with Bank B.

Now is the time for the crucial question we raised above while discussing scenario **(** **3** **)**:

Why does Corporation X not send pain.001 directly to Bank B where its EUR account is held?

It may be that Corporation X has many different currency accounts with various banks. Corporation X is also a customer of Bank A.

Bank A offers a service to concentrate payment initiation from corporate customers. As Corporation X has many accounts in various banks it may be easier for it to maintain only one channel for all the payments they initiate. So, Bank A becomes a concentrating financial institution for Corporation X.

It means that if for the particular payment initiation, Bank A is not the Debtor Agent (it does not hold the Corporation X account to be debited) it plays the role of the Forwarding Agent. It will forward the pain.001 message to the Debtor Agentfor execution. For this particular payment initiation, Bank A plays a more technical than business role. It just forwards the messages without performing any bookings on the accounts.

In the above diagram, I placed the parties from both pain.001 messages:

- pain.001 from Corporation X and
- pain.001 from Bank A.

When we take a closer look we may notice that all the parties in both messages are the same. Pain.001 from Bank A is indeed the relay message! The only place where the parties differ is the BAH (in fact head.001 in CGI pain.001 is optional, so it may not even be present).

I think we are ready now to explore in depth pain.001 that Bank A sends to Bank B.

In the CBPR+ space, we always begin with Business Application Header (BAH).

![](https://www.iso20022payments.com/wp-content/uploads/2023/03/pain.001-BAH.png)

As we can see from **From** and **To** elements, this message is sent From Bank A to Bank B.

**Business Message Identifier** element contains the **Message Identification** captured within the pain.001 Group Header. We will come back to this reference.

**Message Definition Identifier** points to **pain.001.001.09.**

**Business Service** for pain.001.001.09 is swift.cbprplus.02.

The next element – **Creation Date** captures the date and time when the Business Application Header was created. You can learn about the CBPR+ DateTime format in this article: [UTC offset](https://www.iso20022payments.com/miscellaneous/utc-offset/)

The next comes the pain.001 message, which is composed of three blocks.

The first block is **Group Header.**

![](https://www.iso20022payments.com/wp-content/uploads/2023/03/pain.001-GH.png)

**Group Header** contains a set of characteristics that relates to all individual transactions.

However, as we already explained, in CBPR+ space **Number of Transactions** is fixed to 1.

When it comes to the **Message Identification** we see that the value is CORPORATIONXREF. This is because, for a relay scenario, Forwarding Agent should respect the Message ID provided by the Initiating Party of the pain.001 (Corporation X).

The **I** **nitiating Party** in the message is Corporation X and **Forwarding Agent** is Bank A.

In the Group Header, there is also **Creation Date Time** element. CBPR+ pain.001 message is more flexible in defining the date and time elements than other CBPR+ messages. More information is in CBPR+ UHB.

The next block is **Payment Information.**

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/pain.001-PmtInf.png)

**Payment Information** contains a set of characteristics that relates to the debit side of the transaction, such as Debtor and Debtor Agent.

At the top, there is **Payment Information Identification.** For single transactions in the CBPR+ pain.001 Usage Guideline, the value in **Payment Information Identification** is the same as the **Message Identification** of the Group Header.

The value TRF in **Payment Method** element means that the payment will be processed as Credit Transfer (and not as Cheque which is identified by CHK code).

**Requested Execution Date** element captures the date and time at which the Initiating Party requests the payment to be executed. Based on this element, Bank B will send pacs.008 on the 21st of April, 2023.

Corporation X is a **Debtor.** It holds a EUR account with Bank B which is the **Debtor Agent.**

As you can see I identified the **Debtor** with Name and Postal Address instead of BIC.

This is because in both CGI and CBPR+ pain.001 Usage Guidelines, there are rules which make the **Debtor Name** required.

I also included **Debtor Account**.

You can learn more about **Debtor** and **Creditor** data (FATF 16) [here](https://www.iso20022payments.com/miscellaneous/debtor-and-creditor-data-fatf-16/).

The last block is **Credit Transfer Transaction Information.**

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/pain.001-CTTI.png)

**Credit Transfer Transaction Information** contains, among others, elements related to the credit side of the transaction, such as Creditor and Creditor Agent.

**Instruction Identification** is not mandatory in CBPR+ pain.001. However, for transparency reasons, I put here the same reference as already used (CORPORATIONXREF) in the message.

**End to End Identification** and **UETR** are passed on unchanged by Bank A to Bank B. You can learn more about the Point-to-point vs. End-to-end references in the following article: [Point-to-point vs. End-to-end](https://iso20022payments.com/cbpr/point-to-point-end-to-end/)

The pain.001 nested **Amount** element has a choice of either **Instructed Amount** or **Equivalent Amount** to capture the amount and currency of the Customer Credit Transfer Initiation. In our business case the **Instructed Amount** is used.

Please find in the **green** box below an additional explanation related to **Instructed Amount/Equivalent Amount**.

![](https://www.iso20022payments.com/wp-content/uploads/2023/03/EquivalentAmount..png)

**Charge Bearer** uses an embedded code to specify which party/parties would bear any charges associated with processing the payment transaction.

SHAR means that the charges are shared between Debtor and Creditor.

More information is available [here](https://www.iso20022payments.com/cbpr/charges/).

The **Creditor Agent (Bank C)** is a static role in the pain.001 Customer Credit Transfer Initiation.

Bank C maintains a relationship with **Creditor** (Corporation Y).

Similarly to the **Debtor**, I identified the **Creditor** with Name and Postal Address instead of BIC.

This is because in both CGI and CBPR+ pain.001 Usage Guidelines, there are rules which make the **Creditor Name** required.

I also included **Creditor Account**.

You can learn more about **Debtor** and **Creditor** data (FATF 16) [here](https://www.iso20022payments.com/miscellaneous/debtor-and-creditor-data-fatf-16/).

**Remittance Information**enables the matching/reconciliation of an entry that the payment is intended to settle. In our scenario, **Unstructured** format is used, which is free format information restricted to 140 characters.

If you are interested, the file analyzed above can be accessed here: [pain.001 Relay from Bank A to Bank B](https://www.iso20022payments.com/wp-content/uploads/2023/04/pain.001-Relay-from-Bank-A-to-Bank-B.txt)

I checked this message in the CBPR+ Readiness Portal, and this file is a valid message.

The Warnings in the Portal relate only to the Envelope and BIC/IBAN formats.

**pain.002**

**– business scenario –**

Now, it’s time for pain.002.001.10 Customer Payment Status Report.

This message is used to inform the previous party in the payment chain about the positive or negative status of an instruction.

It is also used to report on pending instructions.

Negative status with reject code RJCT is mandatory in CBPR+.

The provision of a positive status or other statuses is determined by a bilateral agreement between the agents.

In our business scenario, we have two pain.001 messages: one from Corporation X to Bank A and the second one from Bank A to Bank B.

Accordingly, we have two pain.002 messages: one from Bank B to Bank A and the second one from Bank A to Corporation X.

Below I would like to present the roles in these two Status Report messages.

If we assign the roles in pain.002 messages we get the following picture:

![](https://www.iso20022payments.com/wp-content/uploads/2023/03/pain.002-business-scenario.png)

BAH **From** and **To** elements show in both messages who is the Sender and who is the Receiver.

Pain.002 is sent to the previous party in the payment chain. In other words, to the party that sent pain.001.

The first pain.002 is sent by the Debtor Agent (Bank B) to the previous agent in the payment chain (Bank A).

Bank B plays the role of the Initiating Party in pain.002. As we are discussing Relay scenario, Bank A plays the role of the Forwarding Agent.

In the second message, Bank A forwards pain.002 to Corporation X.

In this article, I will analyze in-depth the first of these two messages.

As always we begin with BAH.

![](https://www.iso20022payments.com/wp-content/uploads/2023/03/pain.002-BAH.png)

As we can see from **From** and **To** elements, this message is sent From Bank B to Bank A.

**Business Message Identifier** element contains the **Message Identification** captured within the pain.002 Group Header. We will come back to this reference.

**Message Definition Identifier** points to **pain.002.001.10.**

**Business Service** for pain.002.001.10 is swift.cbprplus.02.

The next element – **Creation Date** captures the date and time when the Business Application Header was created. You can learn about the CBPR+ DateTime format in this article: [UTC offset](https://www.iso20022payments.com/miscellaneous/utc-offset/)

The pain.002 message is composed of four building blocks.

The first block is **Group Header**.

![](https://www.iso20022payments.com/wp-content/uploads/2023/03/pain.002-GH.png)

**Group Header** contains a set of characteristics shared by all individual transactions in the message.

However, as we already explained, in CBPR+ space **Number of Transactions** is fixed to 1.

When it comes to the **Message Identification** we see that the value is BANKBREF. Bank B as Initiating Party assigns its own **Message Identification** in pain.002. What is important to note here is that in the second pain.002 Bank A should respect the Message ID provided by Bank B (Initiating Party) in the first pain.002.

As we can also see the **I** **nitiating Party** in pain.002 is Bank B. Bank B as the Debtor Agent was the last party that received pain.001 and now is the **Initiating Party** of the Status Report message.

Bank A is in Relay scenario a concentrating financial institution, so it plays the role of the **Forwarding Agent** both in pain.001 and pain.002. The **Forwarding Agent** is mandatory in a Relay scenario whereby the Receiver of the pain.002 message is not the original Debtor.

In the Group Header there is also **Creation Date Time** element. CBPR+ pain.002 message is more flexible in defining the date and time elements than other CBPR+ messages. More information is in CBPR+ UHB.

The next block is **Original Group Information and Status**

![](https://www.iso20022payments.com/wp-content/uploads/2023/03/pain.002-OGIS.png)

**Original Group Information and Status** contains the group of transactions, to which the status report message refers to.

However, since according to CBPR+ rules pain.001 can only contain one transaction, in pain.002 we can also refer to only one transaction.

The **Original Message Identification** in pain.002 contains the **Message Identification** from pain.001 (CORPORATIONXREF). This is the reference created by Corporation X and not Bank A, as Forwarding Agent should respect the Message ID provided by the Initiating Party of the pain.001 and pain.002. In other words, Bank A forwarded in pain.001 to Bank B the same Message ID (CORPORATIONXREF) it received from Corporation X.

**Original Message Name Identification**(pain.001.001.09) confirms that Status Report is related to pain.001 Customer Credit Transfer Initiation.

Optionally the **Original Creation Date Time** can also be captured.

The last two blocks are:

- **Original Payment Information And Status** (contains information about the original payment information, to which the status report message refers)
- **Transaction Information And Status**(contains information about the original transactions to which the status report message refers).

![](https://www.iso20022payments.com/wp-content/uploads/2023/03/pain.002-OPI.png)

In the **Original Payment Information and Status** block of pain.002 there is **Original Payment Information Identification** located.

Since CBPR+ pain.001 and pain.002 usage guidelines are restricted to one single transaction, this value is the same as the **Original Message ID** (CORPORATIONXREF) of the **Original Group Information And Status**.

**Transaction Information And Status** is a nested element used to capture further information from the pain.001.

**Original End to End Identification** and **Original UETR** are mandatory elements, containing the references from pain.001.

**Original Instruction Identification** is optional. However, for transparency reasons, I also populated this element in our example.

These Original elements enable the Initiating Party to associate the Payment Status with the payment they originally sent.

And now we reach the crucial element in pain.002: **Transaction Status.**

Transaction Status utilizes the externalized ISO Payment Transaction Status code list ( [ISO 20022 External Code Lists](https://www.iso20022.org/catalogue-messages/additional-content-messages/external-code-sets)) to provide a status update on a pain.001 message previously received.

The code used in our example ( **ACSP** -AcceptedSettlementInProcess) is sent to confirm that the payment is accepted for execution. It is important to highlight that this code does not indicate the final payment processing stage. So, in our scenario, there may be other pain.002 messages sent with further status codes. The last one would be pain.002 with the code ACCC – AcceptedSettlementCompleted, indicating that Settlement on the creditor’s account has been completed.

Such Status Information messages (pain.002) are bilaterally agreed.

The exception is reject code **RJCT**which is mandatory in CBPR+.

**Remark:** What is worth noting is that in the second pain.002 forwarded by Bank A to Corporation X the CGI rules apply. It will be a message outside the Bank-to-Bank space (outside CBPR+). Similarly to the pain.001, CGI created two Usage Guidelines for pain.002. One of them is related to the Relay scenario.

If you are interested, the file analyzed above can be accessed here: [pain.002 from Bank B to Bank A](https://www.iso20022payments.com/wp-content/uploads/2023/03/pain.002-from-Bank-B-to-Bank-A.txt)

I checked this message in the CBPR+ Readiness Portal, and this file is a valid message.

The warnings in the Portal relate only to the Envelope and BIC formats. Of course, the BICs used by me are not registered and published BICs.

The next article will be about pacs.008. Hopefully, this will allow us to connect all the dots when it comes to customer payments.

|     |     |
| --- | --- |
| [<< pacs.009 (ADV)](https://www.iso20022payments.com/cbpr/pacs-009-adv/) | [pacs.008 >>](https://www.iso20022payments.com/cbpr/pacs-008/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme