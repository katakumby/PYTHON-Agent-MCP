---
url: "https://www.iso20022payments.com/target-services-t2/target-services-infrastructure/"
title: "TARGET Services Infrastructure – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/target-services-t2/target-services-infrastructure/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## TARGET Services

## TARGET Services Infrastructure

This is a second introductory article about TARGET system.

In the previous one, I walked you through the main phases of the evolution of the TARGET system.

Today I am going to present the high-level architecture of the current system (March 2024).

A quick reminder: **TARGET** stands for:

**T** rans-European

**A** utomated

**R** eal-time

**G** ross settlement

**E** xpress

**T** ransfer

It is one of the largest payment systems in the world.

The TARGET2 migration to the new system took place in March 2023.

**TARGET vs. TARGET Services**

When we talk with payment professionals we still often hear the name: TARGET2.

Over the years people have become much accustomed to it.

The problem is that TARGET2 does not exist anymore.

On 20 March 2023, a new system went live.

What do we call the new system?

Below I described three terms you may encounter:

**TARGET:** Interestingly enough this is the formal name of a new system. The Eurosystem removed the suffix “2” but left the well-recognised name.

The legal framework for TARGET is defined in:

[Guideline (EU) of the European Central Bank on a new generation Trans-European Automated Real-time Gross Settlement Express Transfer system (TARGET) and repealing Guideline ECB/2012/27](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022O0912&qid=1669803866580)

From the legal pespective, TARGET is a payment system that provides the settlement in euro in central bank money on several kinds of cash accounts.

These accounts are held in different **TARGET Services**.

**TARGET Services:**This is a more functional term related to the whole infrastructure. I will describe it in more detail further on in this article.

At this point, you may ask whether **TARGET** and **TARGET Services** are just different names for the same thing.

Is **TARGET** the legal term and does **TARGET Services** cover a more functional perspective?

To some extent, this is the correct way of looking at this issue.

However, I would also argue that the term **TARGET Services** is a bit larger in scope.

As I said above **TARGET** covers only cash accounts and EUR settlement.

T2S on the other hand, one of the **TARGET Services**, incorporate also securities accounts (securities accounts are not cash accounts).

Also, **TARGET Services** are implemented as multi-currency services not only dedicated to EUR settlement.

Another term often used is **T2**.

This is simply one of the **TARGET Services**.  I am going to describe it in more detail below.

**4CB**

When you open TARGET Services documentation,

for example the most important functional document related to RTGS: RTGS User Detailed Functional Specifications ( [here](https://www.ecb.europa.eu/paym/target/consolidation/profuse/shared/pdf/RTGS_UDFS_R2024_JUN_revised_20240112.pdf)),

you may notice that at the top, on the right-hand side, there are logos of the 4 CBs:

- Deutsche Bundesbank,
- Banque de France,
- Banca d’Italia and
- Banco de España

Why are these 4CBs listed on the functional documentation?

This is because these 4 CBs developed and operate (on behalf of the Eurosystem) the TARGET Services infrastructure.

**One payment system or a multiplicity of payment systems?**

TARGET Services form a centralized and harmonized technical infrastructure.

However, the legal perspective differs here from the technical one.

From the legal point of view TARGET is structured as a multiplicity of payment systems, where each Central Bank operates its own TARGET component system.

This approach is not new and has not changed with the migration to the new system.

This means that current TARGET national components constitute the legal successors of the corresponding, previous TARGET2 national components.

Also ECB operates its own TARGET component.

It’s worth noting, that not only Eurozone Central Banks have their TARGET components. Under the additional agreement, Central Banks outside the Eurozone, may also connect to TARGET system and operate their own TARGET components.

This is precisely the case for Poland, where Narodowy Bank Polski operates the Polish component of TARGET, called TARGET-NBP.

**What does the new TARGET infrastructure look like?**

When we talk about TARGET infrastructure we have to start with the term that we are already familiar with: TARGET Services.

**TARGET Services** are:

- **T2** (comprised of **CLM** and **RTGS**)
- **TARGET2-Securities** (T2S)
- **TARGET Instant Payment Settlement** (TIPS).

_\\* ECMS is also defined as a TARGET Service but let’s skip it in this article_

Each service is dedicated to a particular business area.

However, they are not independent.

This is because, all **TARGET Services** use so-called **common components**, which allows the harmonization across services.

Below I present two common components, which in my opinion are the most important:

- **Eurosystem Single Market Infrastructure Gateway****(ESMIG).**

It is a network service provider (NSP) agnostic component, using ISO 20022-compliant messages as the standard format for communication with all TARGET Services.

There are two certified NSPs that participants may use for connectivity purposes: SWIFT and SIA-COLT.

ESMIG allows users to connect to TARGET settlement services and common components via both A2A\* and U2A\*\* modes.


  - _\* **A2A** connection allows the software of TARGET participants to communicate with TARGET by sending/receiving single messages and files. A2A communication relies on ISO 20022 XML messages._
  - _\*\***U2A** connection allows TARGET users to access TARGET via the graphical user interfaces (GUIs)._

- **Common Reference Data Management (CRDM)**

It is a component where reference data are maintained.

CRDM allows for the creation, maintenance, and deletion of common reference datarelating to parties, cash accounts, rules, and parameters across TARGET services.

This is how the infrastructure comprising of TARGET Services and common components is presented in the document:

T2-T2S CONSOLIDATION BUSINESS DESCRIPTION DOCUMENT ( [here](https://www.ecb.europa.eu/paym/target/consolidation/profuse/shared/pdf/Business_Description_Document.en.pdf)):

![](https://www.iso20022payments.com/wp-content/uploads/2024/01/Target-Services-Architecture-1024x751.png)

In this diagram, I indicated TARGET Services **in red**.

We can see **T2S** on the left and **TIPS** on the right.

Where is **T2**, though?

**T2** is presented by **CLM** and **RTGS**. This is because **CLM** and **RTGS** form together one service: **T2**.

**In orange**, both **ESMIG** and **CRDM** are highligted.

Now, you may wonder: What are the most practical benefits of knowing the architecture of the above infrastructure?

In my opinion, the most useful aspect of this is the fact, that the TARGET documentation is organized in the same way as the whole infrastructure.

This means that, e.g. in RTGS documentation you will not find all the details related to connectivity, as these are in the ESMIG documentation.

What is even more crucial, in the RTGS documentation you will not find the RTGS Directory description, because RTGS Directory is the reference data, so it is described in CRDM documentation.

Needless to say, the same goes for TIPS Directory.

This is the way the TARGET Services documentation is presented on the ECB website:

![](https://www.iso20022payments.com/wp-content/uploads/2024/01/ECB-website-1024x582.png)

You can recognize the T2, T2S, TIPS.

The “Shared features” section contains the common components documentation, i.a. ESMIG and CRDM.

**Accounts and business areas in the TARGET infrastructure**

We already know the TARGET Services.

Now, let’s see what business areas each of them covers.

This may be presented by the below diagram:

![](https://www.iso20022payments.com/wp-content/uploads/2024/01/TARGET-from-business-and-acounting-perspective.png)

On the left, we can see **T2S Service** dedicated to Securities settlement.

On the right, there is **TIPS Service** used for Instant Payments settlement.

In the middle, we have **T2 Service**, consisting of **CLM** and **RTGS**.

The green arrows denote the Liquidity transfers that participants may use to shift funds from one service to another, depending on business needs.

Because the changes introduced in March 2023 were mainly dedicated to T2 Service, I will skip the detailed description of T2S and TIPS and will focus on explaining the new T2 Service.

As we already know, T2 Service is formed by CLM and RTGS.

Let’s present them one by one.

We are going to begin with CLM.

**T2 Service: CLM**

Central Liquidity Management (CLM) is a new feature of the TARGET infrastructure. There was no equivalent module in the TARGET2 system.

The account that participants hold in CLM is called the main cash account (MCA).

If a participant holds at least one dedicated cash account in any of the TARGET Services, that is: RTGS DCA, TIPS DCA, or T2S DCA, this participant is required to also open an MCA with the same central bank.

There are two main functionalities that CLM offers:

- settlement of Central Bank Operations (CBOs)
- efficient liquidity management

Let’s look at them more in detail.

In TARGET2 CBOs were conducted on the same accounts as other payments. This is not the case anymore.

With the introduction of CLM Eurosystem segregated all interactions of the credit institutions with their Central Bank from the settlement of other transactions.

One of the indicators that CLM is mainly dedicated to the CBOs is the fact that participants cannot send any pacs. messages to CLM.

Pacs.009 and pacs.010 can be sent to CLM only by Central Banks.

One of the most important CBOs is the provision of the Intraday credit.

Participants can be granted Intraday credit on their MCA, which is a central source of liquidity in TARGET system.

However, obtained liquidity can be distributed to other cash accounts in RTGS, TIPS, and T2S through liquidity transfers.

And this is where we approach the second aspect of CLM: a centralized mechanism for the monitoring and management of liquidity.

In this context, CLM offers a wide range of instruments for liquidity management and information tools for liquidity monitoring purposes.

When it comes to generating liquidity transfers, participants may send them ad-hoc depending on current business needs or trigger them automatically based on defined events (e.g. a queued payment order, breaching of floor/ceiling amount).

**T2 Service: RTGS**

Last but not least we are going to discuss the RTGS component of T2 Service.

What transactions are processed in RTGS?

Let’s have a look at this table:

![](https://www.iso20022payments.com/wp-content/uploads/2024/02/Cash-transfer-orders-1024x483.png)

Source: [Information Guide for TARGET participants. Part 1 – Fundamentals](https://www.ecb.europa.eu/paym/target/consolidation/profuse/shared/pdf/R2023.NOV_p1_fundamentals.en.pdf)

We can distinguish 3 types of cash orders based on this table:

- payments between TARGET participants (pacs.004, pacs.008, pacs.009, pacs.010)
- AS settlement (pain.998)
- Liquidity transfers (camt.050)

We have already talked about liqudity transfers, so let’s focus now on the settlement of payments and ancillary system transactions.

- **Settlement of payments in RTGS**

RTGS is designed for the real-time gross settlement of interbank and customer payments.

These transactions are settled on dedicated cash accounts (RTGS DCAs).

This is the area where there have been a lot of changes in comparison to TARGET2.

First, FIN messages were replaced by ISO 20022-compliant messages.

In this context, a fully-fledged (no “like-for-like”) approach was chosen.

This meant, that the ISO 20022 message standard was implemented fully.

Second, SWIFT Y-copy mode was switched to V-shape mode.

The shift to the V-shape communication model meant that:

- At the technical level the payment message is now addressed to the RTGS component and not to the receiving counterparty
- After the settlement, RTGS generates and sends out the message to the receiver.

The V-shape model is illustrated by this diagram:

![](https://www.iso20022payments.com/wp-content/uploads/2024/02/V-shaped.png)

Source: [T2-T2S CONSOLIDATION BUSINESS DESCRIPTION DOCUMENT](https://www.ecb.europa.eu/paym/target/consolidation/profuse/shared/pdf/Business_Description_Document.en.pdf)

It is worth highlighting that in V-shape mode, one payment from Bank A to Bank B means that two pacs messages are generated:

- first, sent by Bank A to the RTGS
- second, sent by RTGS to Bank B

More information about the processing of payments in RTGS is available in the following articles on my website:

- [Addressing payments in T2](https://www.iso20022payments.com/target-services-t2/addressing-payments-in-t2/)
- [Addressing payments in T2: Participation types](https://www.iso20022payments.com/target-services-t2/addressing-payments-in-t2-participation-types/)
- [Addressing payments: T2 with CBPR+ leg (Addressable BIC)](https://www.iso20022payments.com/target-services-t2/addressing-payments-t2-with-cbpr-leg-addressable-bic/)
- [Addressing payments: T2 with CBPR+ leg (Multi-Addressee)](https://www.iso20022payments.com/target-services-t2/addressing-payments-t2-with-cbpr-leg-multi-addressee/%20)

- **Settlement of ancillary systems transactions**

What are ancillary systems?

Simply put, ancillary systems (AS)are systems in which payments/financial instruments are exchanged/cleared, and as a consequence, the resulting obligations are settled in TARGET.

Examples of AS include retail payment systems (RPS), large-value payment systems (LVPS), foreign exchange systems, money market systems (MMS), automated clearing houses (ACH), central counterparties (CCP) and securities settlement systems (SSS).

The RTGS offers 5 AS settlement procedures for the settlement of AS transfer orders (procedures A, B, C, D, and E).

The list od AS and the procedures which are used in available [here.](https://www.ecb.europa.eu/paym/target/consolidation/profuse/shared/pdf/ancillary_systems_procedures_for_T2.xlsx)

One of the most well-known AS is [STEP2-T](https://www.ebaclearing.eu/services/step2-t-system/settlement/) which uses procedure D in RTGS.

|     |     |
| --- | --- |
| [<< Short history of TARGET system](https://www.iso20022payments.com/target-services-t2/short-history-of-target-system/) | [Addressing payments in T2 >>](https://www.iso20022payments.com/target-services-t2/addressing-payments-in-t2/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme