---
url: "https://www.iso20022payments.com/target-services-t2/addressing-payments-in-t2-participation-types/"
title: "Addressing payments in T2: participation types – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/target-services-t2/addressing-payments-in-t2-participation-types/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## TARGET Services (T2)

## Addressing payments in T2: Participation types

This is the second article related to addressing payments in T2.

In the previous one, I described the general rules in this context.

Here I would like to show the application of these general rules for different participation types in T2.

In this article, I will focus on the payment legs that are processed in T2.

The payment chain comprising both T2 and CBPR+ legs will be addressed in the next articles in this series.

To understand the participation types in T2 let’s start with the description of the RTGS Directory, that we analyzed in the previous article.

Please note that I will not focus in this article on the legal aspects of participation in the T2, but present this topic from a functional point of view.

**RTGS Directory**

In the previous article, I introduced three fields in the RTGS Directory that are essential for addressing payments in T2.

Below is their description from CRDM UDFS:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/RTGS-Directory-structure.png)

In this article, we are going to add one more field to the equation.

The field we are interested in is the last field in the RTGS Directory.

It contains two characters defining one of the participation types available in T2.

This is how it is presented in the CRDM UDFS:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/RTGS-Directory_Participation-Types.png)

As we can see there are four main participation types:

- Direct
- Indirect
- Multi-addressee
- Addressable BIC

Moreover, Multi-addressee is broken down into two separate participation types (03 and 04) and Addressable BIC is broken down into four separate participation types (05, 06, 07, 08). These reflect in more detail the kind of business relationship between engaged parties. They are not, however, important from the addressing perspective. In other words, both participation types 03 and 04 reflect the general Multi-addressee participation and behave in the same way in the system. Similarly, participation types 05, 06, 07, and 08 reflect all Addressable BIC participation and behave in the same way in the system.

Because of that, I won’t focus on these differences in this article.

I am going to focus on the 4 main categories listed above.

**Note**: TARGET infrastructure is also prepared for the settlement in other currencies than EUR. However, for EUR settlement the **Indirect** participation type is not relevant and is not covered in the legal documentation. As its behavior in the system is the same as **Addressable BIC** (which is used in EUR settlement) I will show the examples based on **Addressable BIC**. It’s important to understand, however, that from a technical point of view, the system treats both **Indirect** and **Addressable BIC** in the same way.

**Example records in RTGS Directory**

For the purpose of this article, I created the following examples of the participation types in T2.

Let’s imagine that we have two **Direct** T2 participants:

- Bank A ( **BANKAAAAXXX**)
- Bank B ( **BANKBBBBXXX**).

Both of these banks have their branches:

- Bank A registered its Branch ( **BANKAAAA100**) as **Addressable BIC**
- Bank B registered its branch ( **BANKBBBB200**) as **Multi-addressee**.

This setup would look like in the RTGS Directory in the following way:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/RTGS-Directory-1.png)

Before we go further I would like to make some observations regarding the BIC constalations we have here.

- **As only Bank A and Bank B are Direct participants (RTGS DCA account holders) in all scenarios only their accounts can be debited/credited. This is represented by BICs in the Account BIC column.**

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/RTGS-Directory-3.png)

- **There shouldn’t be a scenario in which all 3 BICs in an RTGS record are different. At least two BICs should always be the same.**

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/RTGS-Directory-4.png)

For **Direct** participants, all three BICs should be the same.

For **Addressable BIC**: ‘Addressee BIC’ and ‘Account BIC’ should be the same populated with the BIC of the Direct participant.

The field ‘BIC’ should represent Addressable BIC.

For **Multi-addressee**:  ‘BIC’ and ‘Addressee BIC’ should be the same with the BIC of Multi-addressee.

‘Account BIC’ should represent a Direct participant.

- **Only in the case of the Multi-addressee participation ‘Addressee BIC’ and ‘Account BIC’ differ.**

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/RTGS-Directory-2.png)

Multi-addressee is a very interesting case which I will explore further in this article and in the following ones.

Now I would like to present some basic payment flows that are based on the above examples of RTGS Directory.

Additionally, I am going to show the message elements in which the BICs should appear. I explained the logic behind this in the previous article, where I investigated the general addressing of the messages in T2 ( [here](https://www.iso20022payments.com/target-services-t2/addressing-payments-in-t2/)).

Needless to say, the below are my examples. In the T2 documentation, there are not many examples where Debtor, Debtor Agent, Creditor and Creditor Agent elements are present, as these elements are not relevant for the processing in RTGS. Additionally, there is no simple mapping of the RTGS Directory fields to the Debtor, Debtor Agent, Creditor and Creditor Agent elements. The addressing of these elements is also not validated in the T2. Because of that, I want to highlight that the below examples are based on my understanding of the payments and are not based on the official T2 ones.

**Direct participation**

Let’s start with the Direct participation.

This is a key one because other participation types rely on Direct participants.

While discussing each participation type we are going to ask two questions related to:

- the **account**

(I will use the term RTGS DCA to refer to the account held in the RTGS Component of the T2. RTGS DCA stands for RTGS Dedicated Cash Account)
- the **connection** to the system.

Here are the two questions for the Direct participant:

1. **Does the Direct participant have an RTGS DCA in T2?**

**Yes.** This is the main characteristic of the Direct participant.

All RTGS DCA holders are Direct RTGS participants and all Direct RTGS participants hold the RTGS DCAs.
2. **How does the Direct RTGS participant send/receive payments?**

Direct RTGS Participant sends and receives payments **directly**.


Let’s now explore the basic flow from **Bank A** to **Bank B**.

Both banks are Direct participants.

Below is the record of **Bank A** in the RTGS Directory with the mapping to the message elements:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/Bank-A-From.png)

As the message is sent from **Bank A**, the BICs from RTGS Directory will be presented on the sending side in the message: **BAH/From** and **Instructing Agent**.

The record for **Bank B** in the RTGS Directory is the following:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/Bank-B-To.png)

As the message is sent to **Bank B**, the BICs from RTGS Directory will be presented on the receiving side in the message: **BAH/To** and **Instructed Agent**.

So, here is the **pacs.009** flow from Bank A to Bank B.

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/A-to-B-pacs.009.png)

The message elements presented in the diagram are the same in the message from Bank A to T2 and in the message from T2 to Bank B.

In pacs.009 Debtor Agent and Creditor Agent are optional.

**Note:** In this example the Creditor is BANKBEBBXXX. But we can also imagine the scenario where Bank A holds an account with Bank B. It may be that Bank A wants to shift liquidity from its RTGS DCA to its account with Bank B. In this scenario, Bank A would populate its own BIC also as the Creditor: **BANKAAAAXXX**

And here is **pacs.008** from Bank A to Bank B:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/A-to-B-pacs.008.png)

In pacs.008 Debtor Agent and Creditor Agent are mandatory. These elements represent the Agents that hold accounts for Debtor and Creditor respectively.

In this first part, we saw the flows between Direct participants.

Direct Participants can provide access to RTGS for their branches and other Credit Institutions.

In the following part, we are going to investigate the flows including the Branches of Bank A and Bank B.

**Addressable BIC (Indirect) participation**

As I explained earlier Addressable BIC and Indirect both behave in the same way in the system. From the system’s point of view, there is no difference here. The difference is related to the legal nature.

However, the current TARGET documentation does not cover Indirect participation, so the Indirect participation type is not relevant for EUR settlement.

Because of that, I would like to focus on the Addressable BIC.

So, let’s explore two questions in the context of **Addressable BIC:**

1. **Does the Addressable BIC have an RTGS DCA in T2?**

**No.** The payments sent in favor of/on behalf of the Addressable BIC are booked on the RTGS DCA of the Direct participant.
2. **How does the Addressable BIC send/receive payments?**

**Addressable BIC CANNOT send and receive payments directly.**

They can only send and receive payment orders indirectly via a Direct participant. In other words, the Direct participant is an intermediary between Addressable BICs and T2.

As an example, we are going to investigate the payment flow from the **Branch of Bank A** (**Addressable BIC**) to **Bank B** ( **Direct participant**).

Below is the record of the **Branch of Bank A** in RTGS Directory:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/Branch-A-From.png)

On the right-hand side, we have mappings of the RTGS Directory fields to the message elements.

As the message is sent from **the Branch of Bank A**, the BICs from RTGS Directory will be presented on the sending side in the message: **BAH/From** and **Instructing Agent**.

The record for **Bank B** in the RTGS Directory is the following:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/Bank-B-To.png)

As the message is sent to **Bank B**, the BICs from RTGS Directory will be presented on the receiving side in the message: **BAH/To** and **Instructed Agent**.

So, here is the **pacs.009** flow from Branch of Bank A to Bank B.

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/Branch-A-to-B-pacs.009.png)

Communication between Bank A and its branch is outside of the T2.

In this flow Debtor points to the Branch of Bank A, to indicate that the message is sent on behalf of **BANKAAAA100**.

Debtor Agent element in pacs.009 is not mandatory, but I wanted to make it explicit that Bank A holds the account for its Branch (Debtor).

And here is **pacs.008** from the Branch of Bank A to Bank B:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/Branch-of-Bank-A-to-B-pacs.008.png)

In pacs.008 Debtor Agent and Creditor Agent are mandatory. These elements represent the Agents that hold accounts for Debtor and Creditor respectively.

**Multi-addressee participation**

Last but not least: **Multi-addressee participation.**

This participation type relates to the situation in which a Direct participant authorizes, for example, its Branch to submit and receive the payments directly to T2, without their involvement.

Two questions in the context of **Multi-addressee participation****:**

1. **Does the Multi-addressee have an RTGS DCA in T2?**

**No.**

The payments sent by/to **Multi-addressee**are booked on the RTGS DCA of the Direct participant.

2. **How does the Multi-addressee send/receive payments?**

Multi-addressee **sends and receives payments directly, from/to its own BIC.** In other words, it can channel payments through the RTGS DCA of the Direct participant by submitting/receiving payments without the involvement of the Direct participant.

As an example let’s explore the pacs.009 flow from **Bank A** ( **Direct participant**) to the **Branch of Bank B** ( **Multi-addressee**).

Below is the record of **Bank A** in RTGS Directory:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/Bank-A-From.png)

On the right-hand side, we have mappings of the RTGS Directory fields to the message elements.

As the message is sent from **Bank A**, the BICs from RTGS Directory will be presented on the sending side in the message: **BAH/From** and **Instructing Agent**.

The record for **the Branch of Bank B** in the RTGS Directory is the following:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/Branch-B-To.png)

As the message is sent to **the Branch of Bank B**, the BICs from RTGS Directory will be presented on the receiving side in the message: **BAH/To** and **Instructed Agent**.

So, here is the **pacs.009** flow from Bank A to the Branch of Bank B.

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/A-to-Branch-B-pacs.009.png)

What is interesting here is that **BAH/To** and **Instructed Agent** differ.

**BAH/To** contains BIC of the Branch of Bank B which is addressed directly in T2. **BANKBBBB200** receives the message without the involvement of Bank B.

**Instructed Agent** contains the Account BIC of Bank B, which is credited in T2 as a result of the pacs.009 settlement.

As the last flow, I would like to show the **pacs.008** from the Branch of Bank A to the Branch of Bank B.

The RTGS records for these branches are the following:

The Branch of Bank A:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/Branch-A-From.png)

The Branch of Bank B:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/Branch-B-To.png)

Here is the flow of **pacs.008** from Branch of the Bank A to the Branch of the Bank B:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/Branch-A-to-Branch-B-pacs.008.png)

In pacs.008 Debtor Agent and Creditor Agent are mandatory. These elements represent the Agents that hold accounts for Debtor and Creditor respectively.

**Summary**

As a summary, I would like to point to the following table from the RTGS UDFS that nicely summarises the features of the participation types:

![](https://www.iso20022payments.com/wp-content/uploads/2023/09/Participation-types-table.png)

This concludes this article.

In the next one, I am going to present flows containing both T2 and CBPR+ legs.

[<< Addressing payments in T2](https://www.iso20022payments.com/target-services-t2/addressing-payments-in-t2/)

[Addressing payments: T2 with CBPR+ leg (Addressable BIC) >>](https://www.iso20022payments.com/target-services-t2/addressing-payments-t2-with-cbpr-leg-addressable-bic/)

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme