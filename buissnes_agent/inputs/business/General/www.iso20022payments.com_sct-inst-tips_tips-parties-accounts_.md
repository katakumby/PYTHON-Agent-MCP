---
url: "https://www.iso20022payments.com/sct-inst-tips/tips-parties-accounts/"
title: "TIPS Parties & Accounts – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/sct-inst-tips/tips-parties-accounts/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## SCT Inst & TIPS

## TIPS Parties & Accounts

TARGET Instant Payment Settlement (TIPS) is a market infrastructure service launched by the Eurosystem in November 2018.

TIPS settles instant payments in central bank money, in real-time and around the clock, every day of the year (24/7/365).

In my previous article, I provided main aspects of TIPS ( [here](https://www.iso20022payments.com/sct-inst-tips/intoduction-to-tips/)).

In this article, I am going to focus on Parties and Accounts in TIPS.

What is also important to hignlight is that in my articles I look at TIPS mainly from EUR settlement perspective.

Let’s start with Parties.

**Parties**

First thing to notice is that each party in TIPS is univocally identified with a BIC11.

For the sake of this article let’s focus on the following party types:

• Participant

• Ancillary System

• Reachable Party

The most basic Party in TIPS is a **Participant**.

Participant owns one or more **TIPS DCAs** (TIPS Dedicated Cash Accounts).

In functional documentation this account is called TIPS account, but I will use term “TIPS DCA”, which is used in legal documentation.

So, a **Participant** is a **TIPS DCA holder**.

An **Ancillary System** also holds an account in TIPS, but this is a different type of account.

An Ancillary System is a party that holds one **TIPS AS Technical Account**.

What is a **Reachable Party**?

The crucial thing to remember is that Reachable parties do not hold accounts in TIPS.

They rely on a **TIPS DCA** account or a **TIPS AS Technical Account** to settle instant payment orders in TIPS.

These payments are booked on a **Participant’s** or **Ancillary System’s** account with whom **Reachable Party** entered into agreement.

If they wish **Reachable Parties** may instruct payments themselves or outsource it to the third party via **Instructing Party** functionality (more about it below).

**Adherence to SCT Inst**

**Reachable parties** and **TIPS DCA holders** settling in EUR should adhere to the SCT Inst scheme by signing the SEPA Instant Credit Transfer Adherence Agreement.

For the list of SEPA Inst participants you can check this EPC page: [https://www.europeanpaymentscouncil.eu/what-we-do/be-involved/register-participants/registers-participants-sepa-payment-schemes](https://www.europeanpaymentscouncil.eu/what-we-do/be-involved/register-participants/registers-participants-sepa-payment-schemes)

**TIPS AS technical account holders** settling in EUR should be an SCT Inst compliant Clearing and Settlement Mechanism (CSM).

For the list of SCT Inst compliant CMSs, you can check this EPC page: [https://www.europeanpaymentscouncil.eu/what-we-do/sepa-payment-scheme-management/clearing-and-settlement-mechanisms](https://www.europeanpaymentscouncil.eu/what-we-do/sepa-payment-scheme-management/clearing-and-settlement-mechanisms)

**List of TIPS direct Participants and Reachable Parties**

The list of TIPS participants and Reachable Parties is available on the following ECB page: [https://www.ecb.europa.eu/paym/target/tips/facts/html/index.en.html](https://www.ecb.europa.eu/paym/target/tips/facts/html/index.en.html)

**Instructing Party**

There is one more role that we have to mention here which is not formally a party in TIPS, but plays an important function in the overall TIPS architecture.

This is an **Instructing Party**.

What is **Instructing Party**?

The role of **Instructing Party** allows to send (or receive) Instant Payments to (or from) TIPS by interacting directly with TIPS.

From the technical point of view **Instructing Parties** are defined as Distinguished Names that **TIPS DCA holders**, **TIPS AS technical account holders** or **Reachable Parties** define and authorize (via a specific DN-BIC configuration) to act on their behalf.

The above-listed parties in TIPS ( **Participant**, **Ancillary System**, **Reachable Party**) can play the role of **Instructing Party** for themselves or for other Parties.

Additionally, third parties can also act as **Instructing Parties**.

There is a lot of flexibility in the possible set-ups.

**Accounts & CMBs**

As we already know:

• A **Participant** holds one or many **TIPS DCAs**

• An **Ancillary System** holds one **TIPS AS Technical Account**

On the other hand, a **Reachable Party** does not hold an account in TIPS.

The settlement of **Reachable Party** payments is booked on the **TIPS DCA** or **TIPS AS Technical Accounts**.

The challenge here is to correctly manage the liquidity and payment flows.

Sure, to separate the liquidity and payments flow for a particular **Reachable Party**, a **Participant** can dedicate one of its **TIPS DCAs** for each **Reachable Party**.

It is not, however, the only solution available for **Participants** having many **Reachable Parties**.

As we already know, TIPS allows many **Reachable Partie** s to be authorized to settle on one account.

If so, the question may arise:

• How is the liquidity on one account managed for all **Reachable Parties** settling on this account?

Let’s say a **Participant** wants to offer services to three **Reachable Parties** on its **TIPS DCA**. Additionally, this **Participant** also settles its own payments on this account.

• How is this **Participant** able to control its own liquidity and liquidity of the **Reachable Parties**?

Well, this is where a **Credit Memorandum Balance (CMB)** comes into play.

A **Credit Memorandum Balance** represents a limit defined for a **Reachable Party**, in the usage of the liquidity of a given account.

In other words, TIPS **Participants** and **Ancillary Systems** may define **CMBs** linked to their accounts, to define payment capacity limits for their **Reachable Parties**.

Each **TIPS DCA** or **TIPS AS Technical Account** may have any number of linked **CMBs** (0, 1 or many), each **CMB** representing a credit line for a **Reachable Party** in TIPS.

Although accounts may have any number of **CMBs**, each **CMB** is linked to exactly one account (either one **TIPS Account** or one **TIPS AS Technical Account**).

**Authorised Account User**

We already know that Instant Payments in TIPS settles on **TIPS DCAs** or **TIPS AS Technical Accounts** and may use **CMB** limit.

The next important question is:

• How does TIPS control which Party can settle on which account and use which **CMBs**?

There is a functionality of **Authorised Account User (AAU)** in TIPS.

Each **Authorised Account User** specifies a BIC that is allowed to use the related **TIPS DCA**, **TIPS AS Technical Account** or **CMB** for settlement.

The BIC of an **Ancillary System** cannot be authorised to settle on a **TIPS DCA** nor on a **TIPS AS Technical Account**.

Additionally, the following rules apply:

• Several BICs can be authorized to settle on the same **TIPS DCA**/ **TIPS AS Technical Account**

( **TIPS DCAs** and **TIPS AS Technical Accounts** may have one or many **AAUs**)

• Each **CMB** can have no more than one **AAU**

• Each **AAU** BIC can be linked to one and only one **TIPS DCA**, **TIPS AS Technical Account** or **CMB**

**Pan-European reachability**

Below are the measures set by ECB’s Governing Council in 2020: [https://www.ecb.europa.eu/press/intro/news/html/ecb.mipnews200724.en.html](https://www.ecb.europa.eu/press/intro/news/html/ecb.mipnews200724.en.html)

According to the measures taken:

1) **If a PSP**:

• adhered to the SCT Inst scheme, and

• is reachable in T2

then it must also be reachable in TIPS either as:

- a **TIPS DCA holder** or as
- a **Reachable Party** via a **TIPS DCA holder**

2) **If ACH** offers instant payment services, it should hold its **AS Technical Account** in TIPS.

Previously ACHs kept their technical account in TARGET2. Because of this requirement, all ACHs that offered instant payment services moved their accounts to TIPS.

This brings us to the end of this article.

In the next one, we are going to discuss liqudity transfers.

|     |     |
| --- | --- |
| [<< Introduction to TIPS](https://www.iso20022payments.com/sct-inst-tips/intoduction-to-tips/) | [Liquidity Transfers in TIPS >>](https://www.iso20022payments.com/sct-inst-tips/liquidity-transfers-in-tips/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme