---
url: "https://www.iso20022payments.com/cbpr/pacs-008-serial-method/"
title: "pacs.008 SERIAL method – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/cbpr/pacs-008-serial-method/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## CBPR+

## pacs.008 SERIAL method

In the previous article, we discussed Customer Credit Transfer Initiation (pain.001).

Today we are going to explore FI to FI Customer Credit Transfer (pacs.008).

These two messages are closely related. We can notice it already from their names:

![](https://www.iso20022payments.com/wp-content/uploads/2023/03/pain.001-and-pacs.008-names.png)

As we can see both messages are related to the **Customer Credit Transfer.**

**Credit Transfer** means that we are talking about push payment, where the direction of the funds is the same as the direction of the message.

In other words, in **Credit Transfer** the Debtor is on the sending side and the Creditor on the receiving side.

Additionally, both messages are related to a specific kind of **Credit Transfer: Customer Credit Transfer.**

The word **Customer** means that either Debtor or Creditor has to be a non-FI party.

And what differences can we depict from the messages’ names?

As the first name tells us, pain.001 is ‘only’ the **Initiation** of the **Customer Credit Transfer.** The word **Initiation** means pain.001 ‘does not carry’ funds.

The funds are carried via pacs.008,which is initiated by pain.001.

The name of pacs.008 message is interesting. It may even cause confusion.

Let’s have a closer look.

Pacs.008 is **FI to FICustomer Credit Transfer.** So, it contains both ‘**FI to FI’** and ‘ **Customer’** references.

Isn’t it contradictory?

No, it is not.

I would explain it like that:

- Pacs.008 is a **Customer Credit Transfer** because either Debtor or Creditor has to be a non-FI party.
- Pacs.008 is an **FI to FICustomer Credit Transfer** because Sender and Receiver have to be Financial Institutions.

As we are going to see ‘**FI to FI’** means that pacs.008 is exchanged only in Bank-to-Bank space. This message cannot be sent by a Corporation to its bank.

If you are still confused I hope that investigating pain.001 and pacs.008 on the diagram below will make it clear.

But before we go there, let’s remind ourselves of another important notion for this article.

**SERIAL method**

As I indicated in the title of this article, today we are going to explore pacs.008 exchanged via SERIAL method.

What does it mean?

Let’s start the explanation by reminding ourselves that pacs.008 may be processed between:

- two banks or
- among several banks.

When there are only two banks involved, there is only one pacs.008 exchanged between them.

However, when there are many banks involved in customer payment the differentiation of the method used is needed.

There are two methods used while processing payments: **SERIAL** and **COVER**.

We already talked about them in the context of [pacs.009 (ADV)](https://www.iso20022payments.com/cbpr/pacs-009-adv/). As we could learn from this article, SERIAL and COVER methods are not only related to customer payment. However, we usually refer to this differentiation in the context of customer payments.

One thing to notice is that both methods are valid, and it is the decision of the bank which method is preferable depending on internal policies and correspondent agreements.

Both methods lead to the Creditor account being credited, but reach this goal via different paths.

In this article, I will focus on SERIAL method. The differences that apply to the COVER method will be explained in the next article.

What are the key features related to the SERIAL method?

This method is also called the American method. It is the prevailing settlement method in the USA.

The **SERIAL** method means that the payment is sent through a ‘series’ of banks before it reaches the Creditor Agent. Banks in the chain are chosen based on currency and account relationships.

Let’s illustrate this method with a simple example.

Let’s assume that Bank A is instructed to make a payment to the customer of Bank C. Bank A and Bank C do not have an account relationship in the currency of the transfer. Hence, Bank A has to use Bank B as an intermediary.

Bank A and Bank B need to have an account relationship in the currency of the transfer. Bank A sends pacs.008 to Bank B.

Similarly, Bank B and Bank C have to have an account relationship in the currency of the transfer. Bank B sends the second pacs.008 to Bank C.

The above scenario is precisely the pacs.008 processed via **SERIAL** method.

In this method, for each pair of banks in the payment chain, there is a need of a direct account relationship, which allows the funds to move along the messages.

In other words, in **SERIAL** method the payment is built by several pacs.008 messages processed by the banks in the payment chain until it reaches the Creditor Agent. Pacs.008 messages are sent from one financial institution to the next financial institution in the chain.

What is worth noting is that each of the pacs.008 messages exchanged in the payment chain:

- contains the necessary payment **information** for the next bank
- is also the **settlement instruction** that results in the bookings made in the involved banks.

Now, as we have a basic understanding of SERIAL method, let’s place pacs.008 in the diagram that includes different ISO 20022 implementations

( [ISO 20022 market implementations](https://www.iso20022payments.com/miscellaneous/iso-20022-market-implementations/)).

pacs.008 in the broader context

If we put the pain.008 in the diagram we can see that there are many scenarios where this message is used.

As this message is strongly related to pain.001 I decided to use similar scenarios from the previous article about [pain.001](https://www.iso20022payments.com/cbpr/pain-001-pain-002/).

![](https://www.iso20022payments.com/wp-content/uploads/2023/03/pacs.008-Serial..png)

Although, the above diagram shows both pain.001 as well as pacs.008, in the below description I tried to focus on pacs.008.

What can we learn from the above diagram?

Well, first of all, **FI to FICustomer Credit Transfer (pacs.008)** is sent by the Debtor Agent to the Creditor Agent:

- **directly**: scenarios **(** **3** **) , (4) , (5) –** one pacs.008 message
- **through other agents:** scenario **(** **2** **)**– more than one pacs.008 message
- **through a payment clearing and settlement system:** scenario **(** **6** **)**– more than one pacs.008 message

We can see in the above diagram that contrary to the pain.001, pacs.008 can be exchanged only in Bank-to-Bank space. We discussed it already in the article.

Let’s explore now the presented scenarios.

**(** **1** **)** To be honest, I was wondering whether I should include the first scenario in the article about pacs.008. What’s the point in presenting the scenario where pacs.008 is not even sent? But, I came to the conclusion, that it is important to clarify that not every successful pain.001 means that pacs.008 needs to be exchanged in the Bank-to-Bank space. When both Debtor’s and Creditor’s accounts are in the same bank there is no need to send any further payment messages. This kind of transaction is sometimes called an in-house payment or book transfer.

**(** **3** **) , (4) , (5)** These three scenarios show the pacs.008 sent as a result of the pain.001 exchanged in the Bank-to-Bank space. As we can see there can be several cases when it may happen. I won’t present these scenarios in depth here as they were described in the previous article. If you are interested please refer to the following page: [pain.001](https://www.iso20022payments.com/cbpr/pain-001-pain-002/).

In these examples, I depicted only one pacs.008. Needless to say, it may not always be the case. Depending on the business scenario, we might have not only one pacs.008 exchanged, but many. So, we could imagine that Bank C is not the Creditor Agent and has to send another pacs.008 to Bank D, and even Bank D might not be the last bank in the payment chain.

**(** **2** **)** The second scenario describes the most common business case, where upon receiving the pain.001, Bank A (as Debtor Agent) sends pacs.008 to Bank D (Creditor Agent) via Intermediaries (Bank B and Bank C).

For Bank A this payment is ‘from us’ (we hold the Debtor’s account) but is ‘not on us’ (we do not hold the account for the Creditor). In order to make the Creditor receive the funds, we have to send the Fi to Fi Customer Credit Transfer to the Bank that holds Creditor’s account.

Why Bank A does not send pacs.008 directly to Bank D, where the Creditor’s account is held? This is because these two banks do not have the necessary bilateral account relationship.

This scenario is a good example of SERIAL method as the message sent to Bank B is subsequently sent by Bank B to Bank C and in the end by Bank C to Bank D.

**(** **6** **)** The last example (at the bottom of the diagram) is similar to the second one we have just discussed. Here I just wanted to highlight that when Bank A sends pacs.008, this message may be further processed also by the Market Infrastructure. In the diagram, Bank B reaches Bank D via the Payment System. What is different in this scenario is that Bank B and Bank D do not need a direct account relationship in the currency of the transfer. When the settlement is done in the Payment System, the accounts are held centrally by the Market Infrastructure.

Of course, here as well we can imagine other variants of this scenario.

pacs.008

– business scenario –

Now, I would like to introduce you to our business scenario.

Here it is:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008-Business-scenario.png)

In our scenario, Corporation X has to pay Corporation Y USD 565000.

Corporation Y is the Creditor based in the UK. It holds a USD account with Bank C (Creditor Agent) based also in the UK.

As we explained above, for the SERIAL payment there is a need for account relationships between involved parties.

Since the payment is in USD, there is a need of USD correspondent for both Debtor Agent and Creditor Agent to be involved.

In our scenario, both Bank A and Bank C hold their Nostro USD accounts in Bank B.

Based on the correspondent arrangements they both offer USD accounts to their customers, Corporation X and Corporation Y respectively.

Payment is initiated by pain.001 sent by Corporation X (Debtor) to Bank A (Debtor Agent).

Let’s assume that Corporation X provided the following information in **pain.001** sent to Bank A:

- EndToEndId: CORPORATIONXENDTOENDID
- UETR: d0b7077f-49fb-42ed-b78d-af331c0e5012
- Requested Execution Date: 2023-04-21
- Instructed Amount: USD 565000
- Charge Bearer: DEBT
- Debtor: Corporation X
- Debtor Agent: BANKAUAAXXX
- Creditor Agent: BANKGBCCXXX
- Creditor: Corporation Y
- Remittance Information: Contract 123

Based on the above information we are now going to explore **pacs.008** sent by Bank A to Bank B.

The message comprises both BAH and pacs.008 message instance. Let’s start with **BAH**.

**Business Application Header**

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008BAH.png)

As you may remember, the BAH **From** element identifies the BIC of the party who created the Business Document (in our case pacs.008), and **To** element identifies the BIC of the party who will ultimately process the Business Document.

These two elements can also be understood as Sender and Receiver.

It’s worth highlighting that according to the CBPR+ rule BAH **From** BIC must match **Instructing Agent** BIC and BAH **To** BIC must match **Instructed Agent** BIC.

So, in our scenario **From** element contains BIC of Bank A ( **Instructing Agent**) and **To** element of BIC of Bank B ( **Instructed Agent**).

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/addressing.png)

**Business Message Identifier** has to be the same as Message Identification captured within the Business Document’s Group Header. It contains Bank A reference.

**Message Definition Identifier** is pacs.008.001.08.

**Business Service** for pacs.008 core is swift.cbprplus.02.

**Creation Date** captures the date and time when the Business Application Header was created.

You can learn more about the format of this element in [UTC offset](https://www.iso20022payments.com/miscellaneous/utc-offset/) article.

The BAH is attached to the pacs.008 message instance which contains further business information.

The first element in the pacs.008 is **Group Header**.

**Group Header**

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008-GH.png)

**Message Identification** element is a [point-to-point reference](https://www.iso20022payments.com/cbpr/point-to-point-end-to-end/) used to unambiguously identify the message.

Point-to-point means that this is an element created by Bank A (sender of the message). It has to be the same as **Business Message Identifier** from **BAH**.

**Creation Date** captures the date and time when the message was created. You can learn more about the format of this element in [UTC offset](https://www.iso20022payments.com/miscellaneous/utc-offset/) article.

**Number of Transactions** in CBPR+ payment usage guidelines is fixed to 1.

**Settlement Method** indicates how the payment leg is settled. INDA means that Instructed Agent (Bank B) will settle this payment leg (as the Account Servicing Institution). In our scenario, Bank B holds the USD account for Bank A.

You can learn more about this topic in [Settlement Method: INGA vs. INDA](https://iso20022payments.com/cbpr/settlement-method-inga-inda/) article.

After **Group Header** there is a **Credit Transfer Transaction Information** element in pacs.008.

It contains the remaining business information about the payment.

These are the first nested elements under **Credit Transfer Transaction Information:**

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008-1.png)

In **Payment Identification,** there are three references:

- **Instruction Identification**– a point-to-point reference restricted in CBPR+ to 16 characters. This is the reference of Bank A (sender of the message).

In our example, I used the same references that Bank A populated in **GrpHdr/MsgId** (BANKAREF), but this is not required. Bank A could populate in **Instruction Identification** other references which makes sense from their point of view.

aaaaaaaaaaaaaa
- **End to End Identification –** an end-to-end reference provided by the Debtor which must be passed unchanged throughout the payment chain and reported to the Creditor. This is the reference that Corporation X populated in the pain.001. It is now forwarded by Bank A in pacs.008. Later on, Bank B will provide this reference to Bank C, and Bank C will report it to Corporation Y.

aaaaaaaaaaa
- **UETR –** the end-to-end Transaction Reference created using the UUIDv4 standard. This reference must be passed unchanged throughout the payment chain. This is the reference that Corporation X populated in the pain.001. Similarly to **End to End Identification,** it is now forwarded by Bank A in pacs.008. Later on, Bank B will provide this reference to Bank C.

You can learn more about different kinds of references in [Point-to-point vs. End-to-end](https://iso20022payments.com/cbpr/point-to-point-end-to-end/) article.

**Interbank Settlement Amount** contains the amount that Bank A sends to Bank B. You can learn about the format of this element in [Currency and Amount](https://www.iso20022payments.com/miscellaneous/currency-and-amount/) article.

As in our example Instructed Amount in pain.001 was in the same currency and amount Bank A does not need to include Instructed Amount element in pacs.008.

**Charge Bearer** specifies which party would bear any charges. DEBT means that charges are paid by the Debtor. More information about [Charges](https://www.iso20022payments.com/cbpr/charges/) is available in a dedicated article.

With DEBT option the deduction of charges from the Interbank Settlement Amount is not allowed.

In our scenario, Bank C will receive the full amount, and the full amount should be credited to Corporation Y.

**Interbank Settlement Date** contains the date when the payment should be executed.

In the analyzed payment leg, Bank A is the **Instructing Agent** (Sender) and Bank B is the **Instructed Agent** (Receiver).

As it was explained above according to the CBPR+ rule BAH **From** BIC must match **Instructing Agent** BIC and BAH **To** BIC must match **Instructed Agent** BIC.

The next part of the message contains information about **Debtor**:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008-2.png)

Corporation X is our Debtor and Bank A is Debtor Agent. Debtor Agent (Bank A) services the USD account for the Debtor (Corporation X).

Here Debtor Account is provided in the proprietary format.

As you can see the Debtor is identified via Name and Postal Address. You can learn about it in the following article: [Debtor and Creditor data (FATF 16)](https://www.iso20022payments.com/miscellaneous/debtor-and-creditor-data-fatf-16/)

The same way of identification applies also to the **Creditor** which is included in the next part of the message:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008-3.png)

**Creditor Agent** (Bank C) services the USD account for the **Creditor** (Corporation Y).

Here **Creditor Account** is provided as an IBAN.

The last element of the message is **Remittance Information** which enables the reconciliation of the payment.

If you are interested, the file analyzed above can be accessed here: [pacs.008 SERIAL form Bank A to Bank B](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008-SERIAL-form-Bank-A-to-Bank-B.txt)

I checked this message in the CBPR+ Readiness Portal, and this file is a valid message.

The warnings in the Portal relate only to the Envelope and BIC & IBAN data, which, of course, arefictitious.

Comparison of two pacs.008 messages

In this part, I would like to take a brief look at the second pacs.008 message.

To begin with let’s just quickly remind ourselves of our scenario:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008-Business-scenario.png)

In the diagram, we can clearly see that apart from the pacs.008 sent by Bank A there is also the second pacs.008 sent by Bank B.

I think it’s a good idea to have a look at both of them and explore their similarities and in what elements they will differ.

This is the purpose of the below table:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008-SERIALcomparison.png)

We know that **Instructing Agent** and **Instructed Agent** represent the Agents involved in the pacs point-to-point message exchange.

As the payment moves along the chain, banks take turns playing the roles of **Instructing** and **Instructed** Agents. These roles, therefore, change on each payment leg.

We also know that **BAH/From** and **BAH/To** are respectively the same in CBPR+ as **Instructing** and **Instructed Agents**.

In the first pacs.008:

- Bank A sends the message ( **Instructing Agent** & **BAH/From**)

to
- Bank B ( **Instructed Agent** & **BAH/To**).

In the second pacs.008:

- Bank B sends the message ( **Instructing Agent** & **BAH/From**)

to
- Bank C ( **Instructed Agent** & **BAH/To**).

Contrary to the dynamic roles described above, **Debtor**, **Debtor Agent**, **Creditor** and **Creditor Agent** are static roles.

These roles are the same in the first and in the second pacs.008 sent in this payment chain.

You can learn more about different roles in the following articles:

[Static vs. Dynamic Roles (1)](https://www.iso20022payments.com/cbpr/static-vs-dynamic-roles-1/)

[Static vs. Dynamic Roles (2)](https://www.iso20022payments.com/cbpr/static-vs-dynamic-roles-2/)

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/Previous-Instructing-Agent-1.png)

In the second message **Settlement Method** INGA is used which reflects the account relationship between Bank B and Bank C. Bank B holds the USD account for Bank C, so the settlement takes place in the books of Bank B. I described this topic in the following article: [Settlement Method: INGA vs. INDA](https://www.iso20022payments.com/cbpr/settlement-method-inga-inda/)

As the **Charge Bearer** is DEBT the same **Interbank Settlement Amount** is forwarded in the second pacs.008 (no deduction).

Depending on the nature of the particular references, either the same are populated in the second pacs.008 ( **end-to-end references**) or Bank B populates its own references ( **point-to-point references**).

As **Remittance Information** enables the reconciliation of the payment, it is forwarded by Bank B to Bank C.

pacs.008 STP

At the end of this article, I would like to touch upon one more key issue related to pacs.008.

When we examine CBPR+ Usage Guidelines we can see that there are two Usage Guidelines related to pacs.008 message:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008-two-UG.png)

The second Usage Guideline refers to the **STP** variant.

What is it?

**STP** is the abbreviation for **Straight Through Processing**.

This means that payment is processed automatically (without human intervention) by all parties in the payment chain.

We can achieve **Straight Through Processing** by using pacs.008 **STP** variant.

This is because pacs.008 **STP** is based on a network-validated, restricted set of elements of the pacs.008 which make it straight-through processable.

In other words, some elements are not allowed in **STP** variant, which makes the message more easily processable by computers.

The differences between pacs.008 and pacs.008 **STP** are summarised in the CBPR+ UHB in the following way:

![](https://www.iso20022payments.com/wp-content/uploads/2023/05/pacs.008-STP.png)

Source: CBPR+ User Handbook, Q1 2023 (live implementation) Edition

The above picture shows what elements are restricted in the **STP** variant.

Additionally, there is one element that clearly shows that the particular message is pacs.008 **STP**.

This element is **Business Service** in **Business Application Header**.

For pacs.008 this element should contain the value: swift.cbprplus.02

but for pacs.008 STP the value should indicate the **STP** variant:  swift.cbprplus.stp.02

This concludes the article about pacs.008 processed via SERIAL method.

I hope it was interesting.

In the next article, we are going to discuss the COVER method.

|     |     |
| --- | --- |
| [<< pacs.008](https://www.iso20022payments.com/cbpr/pacs-008/) | [pacs.008 COVER method >>](https://www.iso20022payments.com/cbpr/pacs-008-cover-method/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme