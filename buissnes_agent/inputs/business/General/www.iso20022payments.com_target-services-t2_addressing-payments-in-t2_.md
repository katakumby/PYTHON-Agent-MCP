---
url: "https://www.iso20022payments.com/target-services-t2/addressing-payments-in-t2/"
title: "Addressing payments in T2 – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/target-services-t2/addressing-payments-in-t2/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## TARGET Services (T2)

## Addressing payments in T2

This article is related to addressing payments in T2.

T2 is the successor of TARGET2 system (the RTGS system for EUR payments).

It consists of two components:

- **Central Liquidity Management****(CLM)** dedicated to Liquidity management and Central Bank Operations,
- **RTGS** which provides the settlement for real-time interbank and customer payments and ancillary system transactions.

This article covers the addressing of payments in the **RTGS** component of T2.

To understand this topic it is necessary to analyze the following T2-related documents:

- T2 User Detailed Functional Specifications – Real-time Gross Settlement System (RTGS)  (available [here](https://www.ecb.europa.eu/paym/target/t2/t2-profuse/html/index.en.html))
- CRDM User Detailed Functional Specifications – Common Reference Data Management (CRDM) (available [here](https://www.ecb.europa.eu/paym/target/coco/profuse/html/index.en.html))

Needless to say, the detailed description of the T2 messages’ documentation is in MyStandards.

The document explaining how to access T2 documentation in MyStandards is available [here](https://www.ecb.europa.eu/paym/pdf/consultations/mystandards_readiness_portal_user_manual.pdf).

**RTGS Directory**

Addressing in the RTGS component of T2 is done based on RTGS Directory.

To put it simply,  RTGS Directory includes the list of parties that are reachable via T2.

The RTGS Directory is described in the CRDM UDFS.

The crucial fields in RTGS Directory are:

**BIC**– This is the BIC that uniquely identifies an RTGS Participant we want to reach via T2.

Let’s imagine that we receive an incoming **EUR** pacs.004/008/009/010 message or pain.001.

We are not the Creditor Agent, so the payment should have an outgoing leg.

What is the Agent that we should reach in the outgoing leg of this payment?

Well, it will be the Agent populated as Intermediary Agent 1 (if present) or Creditor Agent in the message we received.

How should we reach this Agent? Via CBPR+ or T2 payment?

To answer this question we check whether this Agent is present in RTGS Directory in BIC field.

If yes, we can reach this Agent via T2.

If not, it cannot be reached by T2 and we have to send CBPR+ payment.

While addressing the payment do we use this BIC we found in the ‘BIC’ field of RTGS Directory?

The ‘BIC’ field should not be used to address the T2 payment.

So, how should we address a T2 payment to this Agent?

We have to take into account two additional fields in RTGS Directory which are linked to BIC field.

These are:

**Addressee BIC**– this BIC is to be used in the message business header to address payments.

I like to think about the ‘Addressee BIC’ as a postal address where the message should be sent.

So, when we find the Agent that we want to reach in the RTGS Directory in the ‘BIC’ field, we take the ‘Addressee BIC’ linked to this ‘BIC’ field and we put ‘Addressee BIC’ in the **BAH/To** element of the message.

I know that it may sound complicated, but at the end of the article, there is a diagram that presents the whole process graphically, which I hope will make it more clear.

This is, however, not the end of the process, as we have a third important field in the RTGS Directory:

**Account BIC** – This is the BIC identifying the Account to be debited/credited in T2.

As we are going to discover, this BIC has to be placed in the **Instructing/Instructed Agent** elements of the message instance.

Going back to our example, when we find the Agent that we want to reach in the RTGS Directory in the ‘BIC’ field, we take the ‘Account BIC’ linked to this ‘BIC’ field and we put ‘Account BIC’ in the **Instructed Agent** element of the message.

You may ask at this stage what is the correlation between these 3 fields in RTGS Directory.

In other words: are values in ‘BIC’, ‘Addressee BIC’, ‘Account BIC’ fields always different? Are they sometimes the same? ect.

These are very important questions.

The correlation between these values depends on the participation types in T2.

I will describe this in-depth in the next article, but to signal it now briefly, it may be that:

- all three BICs are the same (Direct participation)
- only ‘Addressee BIC’ and ‘Account BIC’ are the same (Indirect/Addressable BIC participation)
- only ‘BIC’ and ‘Addressee BIC’ are the same (Multi addressee participation).

This third situation is a very interesting case where only ‘Account BIC’ is different!

It means that ‘Addressee BIC’ populated in BAH/To is different than ‘Account BIC’ populated in Instructed Agent.

In my opinion, this is one of the biggest differences between CBPR+ and T2. In CBPR+ Instructing and Instructed Agents identify Sender and Receiver.

In T2, however, they identify the accounts to be debited/credited in T2. As a result, BICs in BAH can be different from BICs in Instructing/Instructed Agents.

As I said I will address the participation types and these differences in the next article.

What is crucial to understand for the time being is that the description given in this article is true for all scenarios and participation types.

Ok. Now we are going to turn our attention to the important elements in the message itself and see how what we have just learned relates to the information provided in MyStandards.

**Important elements of the message**

In the first part of this article, we learned about RTGS Directory and explored how it should be used.

Now I would like to cross-check the information provided above.

Let’s see whether in MyStandards Portal and in the RTGS UDFS we have the same information.

I am going to begin this part with:

**Instructing/Instructed Agents****in the Message instance (e.g. pacs.009)**

From the RTGS Directory analysis, we learned that in these elements we should populate the ‘Account BIC’ field from RTGS Directory (BIC identifying the Account in T2).

The description in MyStandards confirms this understanding.

**Instructing Agent** identifies the RTGS account to be debited:

- **RTGS-Use**: BIC of the RTGS cash account to be debited.

![](https://www.iso20022payments.com/wp-content/uploads/2023/08/Instructing-Agent.png)

**Instructed Agent** identifies the RTGS account to be credited:

- **RTGS-Use**: BIC of the RTGS cash account to be credited.

![](https://www.iso20022payments.com/wp-content/uploads/2023/08/Instructed-Agent.png)

Is this a strict requirement or only a recommendation?

Let’s find out.

If we investigate further the above elements in MyStandards we can see that both point to the validation rule **VR00070**:

- **RTGS-BusinessRules**: VR00070

We can find it under **Instructing Agent** element:

![](https://www.iso20022payments.com/wp-content/uploads/2023/08/Instructing_Instructed-VR00070.png)

We can also notice it under **Instructed Agent** element:

![](https://www.iso20022payments.com/wp-content/uploads/2023/08/Instructed-Agent-VR00070.png)

Where can we find the description of the validation **VR00070**?

It is provided in RTGS UDFS.

If we search RTGS UDFS we can see the following explanation:

**VR00070:**‘Instructing Agent’ and ‘Instructed Agent’ must be known cash accounts in the addressed settlement service for the indicated currency.

![](https://www.iso20022payments.com/wp-content/uploads/2023/08/VR00070.png)

This means that this is more than a recommendation. It is validated in the system.

If the BIC populated in the **Instructing/Instructed Agent** elements is not the one linked to the RTGS account, the payment will be rejected via pacs.002 with E007 Error code.

……………………………………………………………………………

**ATTENTION:** Please notice that the usage of **Instructing/Instructed Agent** is reversed in the case of pacs.010 which is a Direct Debit payment.

For pacs.010:

Instructing Agent

**RTGS-Use**: BIC of the RTGS cash account to be credited.

Instructed Agent:

**RTGS-Use**: BIC of the RTGS cash account to be debited.

……………………………………………………………………………

As the accounting in T2 takes place based on **Instructing/Instructed Agent** elements I like to call it the **accounting layer in T2.**

Now let’s move to **the business layer** of the message, which is the **‘Business Application Header.’**

From the RTGS Directory analysis, we learned that in **BAH/From** and **BAH/To** elements we should populate the ‘Addressee BIC’ field from RTGS Directory (BIC identifying the Sender and Receiver in T2).

**BAH/From**

The description in MyStandard confirms this understanding:

- **RTGS-Use**: Business Sender of the message.

Inbound:

– payment orders sent by the party itself: An ‘Addressee BIC’ of the account given in ‘Instructing Agent’ element in the payload;

![](https://www.iso20022payments.com/wp-content/uploads/2023/08/From.png)

**BAH/To**

A similar description is in MyStandard for BAH/To:

- **RTGS-Use**: Business Receiver of the message.

Inbound:

– payment orders: An ‘Addressee BIC’ of the account given in ‘Instructed Agent’ element in the payload;

![](https://www.iso20022payments.com/wp-content/uploads/2023/08/To.png)

Also, this is a requirement that is validated in the system.

The validation Rule applicable here is **VR00120**.

We already know that we have to put in the **Instructed Agent** element ‘Account BIC’ from the RTGS Directory that identifies the Account to be credited.

Now we learn that in the **BIC/To** element, we have to put the ‘Addressee BIC’ from the RTGS Directory that is linked to the ‘Account BIC’ we populated in the **Instructed Agent** element.

If not, we will get the pacs.002 with E012 error code:

- **VR00120:** The business receiver ‘To’ in the BAH must specify for payment orders:

– An ‘Addressee BIC’ of the account given in ‘Instructed Agent’ element in the payload.


![](https://www.iso20022payments.com/wp-content/uploads/2023/08/BAH.png)

A similar situation is for **BAH/From** and **Instructing Agent**.

Here the validation rule is:

- **VR00100:** The business sender ‘From’ in the BAH must specify for payment orders:

– An ‘Addressee BIC’ of the account given in ‘Instructing Agent’ element in the payload


Up till now, we identified the relevant RTGS Actors based on BICs.

The last layer in the message I would like to mention is where BIC is no longer the direct party identifier.

Let’s talk about**Technical Header.**

Here, there is an important notion related to T2 which is crucial for our investigation. This is the fact that T2 uses a V-shaped model and not Y-copy mode as its predecessor (TARGET2) was using.

The consequence of this is that:

**At the technical layer any message sent to T2 has to be addressed to the system itself.**

This is described in UDFS RTGS, chapter 2.5:

![](https://www.iso20022payments.com/wp-content/uploads/2023/08/Technical-Header.png)

As we can see there are two business actors in this message. Let’s call them **Bank A** and **Bank B**. **Bank A** wants to send the message to **Bank B** via T2.

We explored above the BIC’s that should be populated in the Instructed Agent element and BAH/To elements.

However, at the technical layer, the message is addressed to the **RTGS system** and NOT to **Bank B**.

There are three interesting points in the above figure.

- **We can see that the parties are identified by DN. What is DN?**

DN stands for Distinguished Name. This identifier is not only relevant for T2. This is also how parties are identified in CBPR+. I provided some information about DNs in the CBPR+ context in this article: [CBPR+ message structure](https://www.iso20022payments.com/cbpr/cbpr-message-structure/)

The main difference in addressing between T2 and CBPR+ is that in CBPR+ **Bank A** addresses the Payment to **Bank B’s** DN, and in T2 **Bank A** addresses the payment to **RTGS’s DN**.

- **How does T2 know that this payment should go to Bank B?**

T2 identifies the party that should receive the message from **BAH/To** element, where **Bank’s B BIC** will be provided.

- **If Bank B is identified by BIC in BAH/To, how does T2 know Bank’s B DN which has to be placed in the technical layer of the outbound message?**

In the CRDM component of T2 containing reference data, there is a link between the Business Identifier Codes (BICs) and the DN’s. This is called the ‘DN-BIC Routing’ table. Thanks to this table T2 is able to identify the Distinguished Name (“DN”) to which RTGS should forward a payment message based on the BIC in the BAH/To element. In case there is no link defined in CRDM, the inbound message is rejected as it cannot be forwarded to the intended business receiver.

The last thing about the technical layer that I want to highlight is that there is not much information about the Technical Header in the TARGET documentation itself. This is because the TARGET system is Network Service Provider (NSP) agnostic. The detailed information about this header is in the NSP documentation. SWIFT is one of the two NSPs certified for TARGET. The second one is SIA-Colt.

If you are interested in how NSPs and T2 verify and authenticate the messages including DN and BIC provided, there is an interesting paper on this subject:

[Explainer on authentication of queries and instructions in T2](https://www.ecb.europa.eu/paym/target/consolidation/profuse/shared/pdf/explainer_on_distinguished_name_and_authentication.pdf)

**Diagram**

I know that this topic may not be easy for everybody.

This is why I prepared the diagram that visually presents the way payments should be addressed in T2.

For the purpose of this diagram let’s discuss the payment between two banks **Bank A** and **Bank B**.

The banks in question have the following data in RTGS Directory:

![](https://www.iso20022payments.com/wp-content/uploads/2023/08/Extract-of-RTGS-Directory.png)

I deliberately used colors instead of concrete values in the fields ‘Addressee BIC’ and ‘Account BIC’ as I wanted to present the generic approach, independent of the particular participation types of Bank A and Bank B.

The diagram below uses pacs.009 as an example, but the same principle applies for other pacs messages.

So, if we combine all the information provided in this article we can draw the below diagram summarizing the way payments should be addressed in T2:

![](https://www.iso20022payments.com/wp-content/uploads/2023/08/Digram.png)

**(1)****‘Addressee BIC’** from RTGS Directory for Bank A is populated in **BAH/From**. This value is the same in the message T2 sends to Bank B.

**(2)****‘Addressee BIC’** from RTGS Directory for Bank B is populated in **BAH/To**.

This value is the same in the message T2 sends to Bank B.

Additionally, the ‘DN-BIC routing’ derives – from a BIC (in the **BAH/To** element) – the **Distinguished Name** (technical address) to which RTGS should forward a message.

**(3)****‘Account BIC’** from RTGS Directory for Bank A is populated in **Instructing Agent**. This value is the same in the message T2 sends to Bank B.

**(4)****‘Account BIC’** from RTGS Directory for Bank B is populated in **Instructed Agent**. This value is the same in the message T2 sends to Bank B.

One last note about the approach taken by T2. If you are familiar with the addressing in the former TARGET2 system you could have noticed that the way payments need to be addressed in T2 is more complex.

In TARGET2 the SENDER and RECEIVER were taken from the ‘Addressee BIC’ in TARGET2 Directory and the system recognized based on the reference data the account to be debited and credited.

In T2 we need to include the ‘Account BIC’ when we send the payment.

This is particularly crucial for the Multi-addressee participation types when ‘Addressee BIC’ and ‘Account BIC’ differ.

**Debtor / Debtor Agent / Creditor Agent / Creditor**

You may be surprised that Debtor/Debtor Agent/Creditor Agent/Creditor are not mentioned in this article.

This is because they are not relevant for the settlement in T2.

Below are descriptions of these elements for pacs.009 from MyStandards:

**Debtor:****RTGS-Use**: Mandatory but not relevant for settlement of a payment in RTGS and forwarded within the outbound message.

**Debtor Agent:**

**RTGS-Use**: Not relevant for settlement in RTGS and forwarded within the outbound message.

**Creditor Agent:** **RTGS-Use**: Not relevant for settlement in RTGS and forwarded within the outbound message.

**Creditor:** **RTGS-Use**: Mandatory but not relevant for settlement of a payment in RTGS and forwarded within the outbound message.

**camt.056/camt.029**

This article is about pacs, that is payment messages.

Why do I want to talk about camt.056 and camt.029?

This is because these two messages share an essential feature with payment messages, meaning they can be forwarded by T2 to the Receiver Bank.

Because of that, they also share some characteristics related to the addressing of the messages.

Let’s have a look.

**Technical Level**

We know that at the technical level, camt.056 and camt.029, as all the other messages should be addressed to **DN RTGS**.

**Business level**

Similarly to the pacs messages, in **BAH/To** business receiver should be populated.

Additionally, as for pacs messages, the business receiver for camt.056 and camt.029 should be taken from the ‘BIC Addressee’ in RTGS Directory.

This is how it is presented in the RTGS UDFS:

![](https://www.iso20022payments.com/wp-content/uploads/2023/08/BAH_To.png)

Of course, there are also appropriate validations applied for camt.056:

**VR00100**:

- The business sender ‘From’ in the BAH must specify an ‘Addressee BIC’ of account given in ‘Assigner’ element in the payload;

**VR00120**:

- The business receiver ‘To’ in the BAH must specify an ‘Addressee BIC’ of the account given in ‘Assignee’ element in the payload.

The bove fragments shows that similarly to the pacs messages, in the payload of camt.056 the accounts should be populated.

So, it seems that in the pacs messages accounts are identified:

-  in **Instructing/Instructed Agent** elements

In camt.056 accounts are identified:

- in **Assigner/Assignee** elements

To double check, let’s have a look at the descriptions given in the camt.056 payload in MyStandards:

**Message instance (camt.056)**

From the descriptions available in MyStandards, indeed, we can learn that:

**Assigner** in camt.056 in T2 is treated as **Instructing Agent** in pacs messages:

- **RTGS-Use**: Equivalent to the Instructing Agent

![](https://www.iso20022payments.com/wp-content/uploads/2023/08/Assigner.png)

**Assignee** in camt.056 in T2 is treated as **Instructed Agent** in pacs messages:

- **RTGS-Use**: Equivalent to the Instructed Agent

![](https://www.iso20022payments.com/wp-content/uploads/2023/08/Assignee.png)

This concludes this article.

Hope it was interesting.

This article, however, does not cover all aspects of addressing payments in T2.

In the following posts, I will try to explain what impact the addressing has on the different types of T2 participants.

Also, I will analyze the flow of payments that include both CBPR+ as well as T2 legs.

|     |     |
| --- | --- |
| [<< TARGET Services Infrastructure](https://www.iso20022payments.com/target-services-t2/target-services-infrastructure/) | [Addressing payments in T2: Participation types >>](https://www.iso20022payments.com/target-services-t2/addressing-payments-in-t2-participation-types/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme