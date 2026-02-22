---
url: "https://www.iso20022payments.com/target-services-t2/addressing-payments-t2-with-cbpr-leg-multi-addressee/"
title: "Addressing payments: T2 with CBPR+ leg (Multi-Addressee) – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/target-services-t2/addressing-payments-t2-with-cbpr-leg-multi-addressee/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## TARGET Services (T2)

## Addressing payments: T2 with CBPR+ leg (Multi-Addressee)

In this article, I am going to continue the topic of addressing T2 payments.

The scenario discussed previously was about a payment to “Addressable BIC” (which from a technical perspective behaves as an Indirect participant).

My article was based on the examples published on the ECB website:

[Examples Multi-addressee and addressable BIC](https://www.ecb.europa.eu/paym/pdf/consultations/Examples_Multi_Addressee.xlsx)

Today I am using the same ECB excel file as the basis for my analysis.

I will focus, however, on the scenarios related to the Multi-addressee participation type.

**ECB 1st examples**

The first scenarios I am going to explore are the ones described in the ECB file under the following sheets:

- Scenario A Multi Addressee
- Scenario A-Reverse

Both scenarios are based on the following data in the RTGS Directory:

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/A-RTGS-Directory-1024x308.png)

Before we investigate this topic further, let’s remind ourselves what T2 Multi-addressee participation is.

This participation type relates to the situation in which a Direct participant authorizes, e.g. its Branch to submit and receive the payments directly to T2, without their involvement.

In the above extract from RTGS Directory, we can see that **COBAESMXXXX** is registered in T2 as a Multi-addressee.

**COBAESMXXXX** does not have an RTGS account (RTGS DCA) in T2.

The account debited/credited as a result of **COBAESMXXXX** payments is the account of **COBADEFFXXX**(Direct T2 participant).

However, even if Multi-addressee does not hold the account in T2, it sends and receives payments directly, from/to its own BIC.

In other words, Multi-addressee can channel payments through the RTGS account of the Direct participant by submitting/receiving payments without the involvement of the Direct participant.

So, this is the payment flow from the first ECB scenario

( **‘Scenario A Multi Addressee’** sheet from the ECB excel file)

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/A-Multi-addressee.png)

In this scenario, **DEUTDEFFXXX** receives the CBPR+ pacs.009.

From the message received, **DEUTDEFFXXX** learns that the next agent to be reached is the **COBAESMXXXX**(Creditor Agent) **.**

Because this is a EUR payment, and **DEUTDEFFXXX** is a T2 Direct participant it checks whether **COBAESMXXXX** is reachable via T2 **.**

As we already know, **COBAESMXXXX** is reachable via T2 using Multi-addressee participation type.

Based on the RTGS Directory **DEUTDEFFXXX**addresses the next payment leg in the following way:

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/COBA-Multi-addressee-1024x229.png)

An interesting thing to notice here is that in T2 leg the Instructed Agent is different than BAH/To.

The message will be sent by T2 to **COBAESMXXXX,** however, the credited account in T2 is the account of the Direct participant **COBADEFFXXX.**

As we know, in the CBPR+ this is not possible. In CBPR+:

- Instructing Agent has to be the same as the BAH/From and
- Instructed Agent has to be the same as BAH/To.

This is not the case for Multi-addressee participants in T2.

I think it is interesting to investigate the consequences of this different approach. This will be the main topic of this article.

Now, let’s have a look at the reverse payment flow.

( **‘Scenario A-reverse’** sheet from the ECB excel file)

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/Reverse-A-Multi-addressee.png)

Here, **COBAESMXXXX** is sending pacs.009 to T2.

**COBAESMXXXX** is in BAH/From.

However, **COBAESMXXXX** as a Multi-addressee populates the **COBADEFFXXX**(Direct participant) as Instructing Agent.

**DEUTDEFFXXX** receives the payment where BAH/From is different from Instructing Agent.

As indicated on the diagram with red arrow, **DEUTDEFFXXX** populates the value **COBADEFFXXX** as Previous Instructing Agent 1.

In the message sent by **DEUTDEFFXXX**, **COBAESMXXXX** is only present as Debtor Agent.

In this context, the following question arises:

In what way, may **COBADEFFXXX** being populated as Previous Instructing Agent 1, impact the processing of the pacs.004 if the payment has to be returned?

I will look into this at the end of this article.

Let’s have a look also at other examples of Multi-addressee.

**ECB 2nd example**

Below is the payment flow from the second ECB scenario.

( **‘Scenario B’** sheet from the ECB excel file)

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/B-Multi-addressee.png)

This scenario is based on the same RTGS Directory data as the previous one.

Here, **DEUTDEFFXXX** receives the CBPR+ pacs.009 where Intermediary Agent 1 is ****COBAESMXXXX.****

**DEUTDEFFXXX** addresses the next payment leg based on the RTGS Directory record for ****COBAESMXXXX.****

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/COBA-Multi-addressee-1024x229.png)

****COBAESMXXXX**** receives the pacs.009, but it is not the Creditor Agent.

There has to be one more payment leg.

In the message received by ****COBAESMXXXX**** we have another example of the scenario with BAH/To ( ****COBAESMXXXX****) being different from Instructed Agent ( **COBADEFFXXX**).

How is this situation reflected in the next payment leg?

****COBAESMXXXX**** populates:

- **DEUTDEFFXXX** as Previous Instructing Agent 1
- **COBADEFFXXX** as Previous Instructing Agent 2

What’s new here in comparison to the first example described above is that:

- Previous Instructing Agent 1 and Previous Instructing Agent 2 are added at the same time (in the same payment leg)
- **COBADEFFXXX** is mapped directly in the following way:

Instruct **ED** Agent -> Previous Instruct **ING** Agent 2

And one more example.

**ECB 3rd example**

The following is the payment flow from the third ECB scenario.

( **‘Scenario B-Reverse’** sheet from the ECB excel file)

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/B-Reverse-Multi-addressee.png)

In this scenario, the following RTGS Directory data apply:

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/Reverse-B-RTGS-Directory-1024x306.png)

Here, we have **BNPAJPJTXXX** as a Multi-addressee.

**BNPAJPJTXXX** receives the CBPR+ pacs.009 from **BNPAHKHHXXX.**

The next agent to be reached is **DEUTDEFFXXX.** As **DEUTDEFFXXX** is a Direct T2 participant, BAH/To euqals Instructed Agent.

However, on the sending side, **BNPAJPJTXXX** populates pacs.009 to T2 according to the RTGS Directory data:

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/Reverse-B-addressing-1024x219.png)

**DEUTDEFFXXX** receives pacs.009 with different BAH/From (**BNPAJPJTXXX**) and Instructing Agent ( **BNPAFRPPXXX).**

How is this situation reflected in the next payment leg?

****DEUTDEFFXXX**** populates:

- **BNPAJPJTXXX** as Previous Instructing Agent 1
- **BNPAFRPPXXX** as Previous Instructing Agent 2

I indicated this on the diagram with red arrows.

We have already seen in the second example that two Previous Instructing Agents were populated in the one payment leg.

The same behavior can be seen in this scenario.

What’s new here in comparison to the second example described above is that:

- **Previous Instructed 1** is mapped from **BAH/From**

**Note:**

Alternatively, according to the ECB comment in the excel file, **BNPAJPJTXXX**could already indicate itself as Previous Istructing Agent 1 in the payment leg sent to ****DEUTDEFFXXX.****

In that case, it might have been easier for **DEUTDEFFXXX** to populate both Previous Instructing Agents in the next payment leg.

**CBPR+ example**

It is crucial to understand that the above examples come from ECB and were prepared in the context of T2.

However, the issue here is not strictly related to the T2 leg of the payment, but to the CBPR+ leg following the T2 payment leg.

I think it is important to have a look at the CBPR+ documentation and try to find clues that will help us understand the above flows.

Of course, we will not find in the CBPR+ documentation flows with BAH/From being different than Instructing Agent or BAH/To different than Instructed Agent.

However, we can rephrase the problem and search for the CBPR+ scenario where there is a difference between the Agent sending the message and the Agent holding the account to be debited.

Additionally, we can check, how this scenario manifests itself in the specific usage of the Previous Instructed Agents elements.

Bearing that in mind, I have found one page in CBPR+ UHB which may shed some light on this problem.

This is what CBPR+ UHB says:

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/CBPR-account.png)

The situation here is the following:

- The branch of Agent A sends the CBPR+ message, however, the account to be debited belongs to HQ of Agent A.
- Agent A HQ’s BIC does not appear in the BAH or Instructing/Instructed Agents elements.
- For transparency purposes, Agent C populates Agent A HQ’s BIC (AAAAGB2L) as Previous Instructing Agent 1.

I am aware that this description is not exactly the same as the ECB examples described in this article.

In my opinion, however, it shows at least that according to the CBPR+ there are some situations in which the Previous Instructing Agents are populated from other than Instructing Agent elements according to the business scenario.

**Impact on pacs.004?**

In this article, we have seen different T2 scenarios for Multi-addressee participants where there is a difference in the BAH and Instructing/Instructed Agent elements.

These examples included also CBPR+ legs with the EBC examples of how these agents could be populated in the following payment legs.

In my opinion, the first challenge here is related to the automation of these processes in the payment engines used by banks.

The second challenge is about the impact this difference may have on the pacs.004 processing.

This may differ depending on how the pacs.004 is generated in the payment engine.

In other words, when we receive the pacs.004, is the following leg that we generate based on:

- the ‘Return chain’ in the received pacs.004
- the data kept from the original message that is now being returned?

Let’s revisit our first scenario from this article.

This is the message that **DEUTDEFFXXX** gets:

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/pacs.004-1.png)

As we already know, **COBAESMXXXX** is a Multi-addressee in T2, so **DEUTDEFFXXX** receives the pacs.009 with:

- BAH/From: **COBAESMXXXX**
- Instructing Agent: **COBADEFFXXX**

This time, though, let’s assume that **DEUTDEFFXXX** cannot process this payment further.

How should pacs.004 be addressed by **DEUTDEFFXXX**?

Should it be sent to **COBAESMXXXX** or **COBADEFFXXX**?

From the T2 perspective, these two BICs have separate records in the RTGS Directory.

In my opinion (maybe there will be some other views):

- as the pacs.009 is received by **DEUTDEFFXXX** from **COBAESMXXXX** as a Multi-addressee,
- pacs.004 should be sent also to **COBAESMXXXX** as a Multi-addressee.

To my mind, the pacs.004 sent by **DEUTDEFFXXX** should look like this:

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/pacs.004-2.png)

This would mirror the original flow.

**One note here:** According to the CBPR+ UHB, the initiator of the Payment Return becomes the mandatory Debtor in the Return Chain element (as they owe the money to the party the return is intended for). This is why I populated **DEUTDEFF** **XXX** (initiator of the Payment Return) as a Debtor.

However, if the payment engine checks Instructing Agent of the original payment to determine the Agent to which pacs.004 has to be addressed, it may be that pacs.004 is generated in the following way:

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/pacs.004-3.png)

Of course, this pacs.004 will be settled in T2 as **COBADEFFXXX** is a Direct T2 participant.

However, this pacs.004 does not follow exactly the same chain as the original payment.

In this particular example, it may not be a big issue, since **COBAESMXXXX** is present as a Creditor Agent in pacs.004.

Can there be, however, other flows where it may become more problematic?

Let’s now look at what may happen if **DEUTDEFFXXX** processes pacs.009, however, the payment cannot be processed by the next Agent.

This is the pacs.009 flow, from the first scenario in this article:

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/pacs.004-4.png)

An interesting question is: How may **SOGEFRPPXXX** interpret the received pacs.009?

**SOGEFRPPXXX** notices that **COBADEFFXXX** is populated as the Previous Instructing Agent 1, so it may think that **DEUTDEFFXXX**received the payment from **COBADEFFXXX (Direct participant)** and not from****COBAESMXXXX (Multi-addressee).****

In our scenario, **SOGEFRPPXXX** cannot process this payment further and has to send pacs.004.

If the **COBADEFFXXX** is populated as Previous Instructing Agent 1 in pacs.009, then it may be presentin pacs.004 as Intermediary Agent 1.

This would be the standard CBPR+ change of roles in pacs.004 Return chain.

In this scenario the pacs.004 would look like this:

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/pacs.004-5.png)

**COBADEFFXXX** (Previous Instructing Agent 1) in the original payment transition to Intermediary Agent 1 in the return chain.

The key issue here is how the **DEUTDEFFXXX** will forward the pacs.004.

If the payment engine checks only Intermediary Agent 1 in pacs.004 as the Agent where pacs.004 should be forwarded, it may end up sending the pacs.004:

- to **COBADEFFXXX** as a Direct T2 participant and
- not to **COBAESMXXXX** as a Multi-addressee participant.

As explained above, this would not be the ideal situation, in my opinion.

**Conclusion**

This brings us to the end of this article.

As we have seen, there are several scenarios where T2 Multi-addressee may be included in the payment chain including CBPR+ legs.

I would hazard a guess that T2 is not the only RTGS system where it is possible to have different BICs in BAH From/To and Instructing/Instructed Agent elements.

It would be interesting to analyze how the payment engines may automate these different business scenarios while populating Previous Instructing Agents.

Additionally, at different stages of the payment chain, the payment may have to be returned.

The way Previous Instructing Agents were populated may have an impact on the Return chain in pacs.004.

It’s good to keep in mind the challenges the above scenario may cause for the automatic processing of the payments in different payment engines.

|     |     |
| --- | --- |
| [<< Addressing payments: T2 with CBPR+ leg (Addressable BIC)](https://www.iso20022payments.com/target-services-t2/addressing-payments-t2-with-cbpr-leg-addressable-bic/) | next page >> |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme