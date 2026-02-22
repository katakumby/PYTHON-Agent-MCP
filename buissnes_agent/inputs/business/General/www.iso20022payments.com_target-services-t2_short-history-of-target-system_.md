---
url: "https://www.iso20022payments.com/target-services-t2/short-history-of-target-system/"
title: "Short history of TARGET system – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/target-services-t2/short-history-of-target-system/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## TARGET Services

## Short history of TARGET system

This is a short introduction to the TARGET system.

In this article, I would like to walk you through the main phases of the evolution of the TARGET system. This, I hope, will be a good preparation for the next article where I am going to present the high-level architecture of the current, quite complex infrastructure, and will allow us to place the particular service of this infrastructure in the larger context.

So, what is TARGET?

**TARGET** stands for:

**T** rans-European

**A** utomated

**R** eal-time

**G** ross settlement

**E** xpress

**T** ransfer

It is one of the largest payment systems in the world.

Its beginnings are linked to the introduction of the EUR currency.

**TARGET(1)**

TARGET commenced operations on 4 January 1999 following the launch of the euro on 1 January 1999.

It was an RTGS system for the euro payments.

What is an RTGS system?

**Real-time gross settlement (RTGS)** system is a system where the processing and settlement of a transaction takes place on:

- a **“gross” basis** (transaction-by-transaction, individually, without bunching or netting with any other transaction)
- in **real-time** (transactions are not subjected to any waiting period)
- in **central bank money** (settlement takes place on accounts held at the central bank. Settlement is immediate, final, and irrevocable)

At the first stage of its existence, TARGET was simply a “system of systems”,  consisting of national RTGS systems (one per Member State) and the ECB Payment Mechanism.

All the systems were connected via Interlinking based on SWIFT network.

Its architecture can be presented in the following way:

![](https://www.iso20022payments.com/wp-content/uploads/2024/01/interlinking-300x252.png)

_Source: ECB_

We can say, that TARGET was decentralized both from the legal as well as technical point of view. It did not replace the national RTGS systems but linked them, which formed a technical framework for the processing of cross-border payments.

Although TARGET served well its purpose, its decentralized structure caused some challenges to adapt cost-effectively to the new needs of the market. As a consequence, the Governing Council of the ECB decided in October 2002 to develop a second-generation system.

**TARGET2**

TARGET2 was launched in November 2007 and fully replaced the previous system in May 2008, when the latter ceased operating.

The biggest change was related to the technical infrastructure of the system.

With TARGET2, the decentralized structure of the first-generation TARGET system was replaced by a **single technical platform** („SSP – Single Shared Platform”).

From the communication point of view, SWIFT network and messages were used.

The shift to TARGET2 can be illustrated with the following diagram:

![](https://www.iso20022payments.com/wp-content/uploads/2023/12/TARGET2.png)

Source: [https://nbs.sk/en/payments/payment-systems/target-services/basic-informations-about-target2/history-t2/](https://nbs.sk/en/payments/payment-systems/target-services/basic-informations-about-target2/history-t2/)

The new system provided a harmonized service, where all participants were offered the same high-quality functionalities and interfaces, as well as a single price structure.

SSP was developed and operated (on behalf of the Eurosystem) by 3CB:

- the Banca d’Italia,
- the Banque de France, and
- the Deutsche Bundesbank.

What is important to note is that, despite its technical centralization, TARGET2 remained a decentralized system in legal terms.

It meant that TARGET2 was still legally structured as a multiplicity of payment systems (called TARGET2 components).

We may illustrate this with the below diagram:

![](https://www.iso20022payments.com/wp-content/uploads/2024/01/TARGET2.png)

The next big milestone was the launch of the T2S platform.

**TARGET2 (including T2S)**

What is T2S?

**TARGET2-Securities (T2S)** offers centralized delivery-versus-payment (DvP) settlement in central bank money.

The fundamental objective of the T2S project was to integrate and harmonize the highly fragmented securities settlement infrastructure in Europe.

T2S platform became operational on 22 June 2015.

We can distinguish two areas in T2S: securities one and a cash one.

Consequently, T2S accommodates:

- market participants’ securities accounts (opened by central securities depositories (CSDs) for their customers), and
- cash accounts (opened by central banks for the credit instututions)

The cash accounts in T2S were called T2S DCAs (T2S Dedicated Cash Accounts).

This is because these accounts were dedicated exclusively to the settlement of the cash leg of a securities transactions in T2S.

Securities accounts and cash accounts were integrated into one single IT platform, making settlement fast, highly efficient, and low risk.

Because the T2S was not a payment system, legally, euro-denominated DCAs (cash accounts) were placed within the perimeter of TARGET2.

On the other hand, securities accounts remained under the CSDs competence, and as such were not covered by TARGET2 legal perimeter.

This is illustrated by this diagram:

![](https://www.iso20022payments.com/wp-content/uploads/2024/01/TARGET2-and-T2S-1024x709.png)

As we can see, with the introduction of the T2S, the business scope of the TARGET2 transactions as well as technical infrastructure was extended.

Moreover, some interesting things happened in T2S:

- from the communication perspective, apart from SWIFT also the SIA-Colt was established as a Network Service Provider (NSP) for participants
- the messages used were ISO 20022-compliant
- T2S was a multicurrency platform, enabling the interested non-euro area central banks to connect to T2S with their currencies. Currently (February 2024), apart from EUR, the settlement in T2S is done in Danish krone (DKK).

The above features highly impacted the future evolution of the TARGET2 system.

The same approach was taken during the next stage: the launch of TIPS platform.

**TARGET2 (including T2S and TIPS)**

TIPS was launched in 2018.

**TIPS** stands for **TARGET instant payment settlement.**

As its name suggests, it is a service where the settlement of instant payments takes place.

Payments are settled in TIPS:

- within seconds
- in Central Bank money
- with around-the-clock availability (on a 24/7/365 basis).

Many features that were implemented previously for T2S, were also applied for TIPS. These include i.a. two Network Service Providers (NSP), or developing TIPS as a multicurrency platform.

TIPS is based on the SEPA Instant Credit Transfer (SCT Inst) and it uses ISO 20022-compliant messages.

The cash accounts in TIPS were called TIPS DCA (TIPS Dedicated Cash Accounts).

This is because these accounts were dedicated to the settlement of instant payments in TIPS.

When we add TIPS to our diagram we get the following picture:

![](https://www.iso20022payments.com/wp-content/uploads/2024/01/TARGET2-T2S-and-TIPS-1.png)

**Interesting Note:**

When we go to the European Payments Council website and look for Clearing and Settlement Mechanisms (CSMs) that are compliant with the particular payment scheme ( [here](https://www.europeanpaymentscouncil.eu/what-we-do/sepa-payment-scheme-management/clearing-and-settlement-mechanisms)) we can see that there are a lot of Central Banks that are indicated as SCT Inst compliant CSM with the note: **through TIPS**.

On the other hand, TIPS is not listed there.

Why is that?

This is because TIPS falls under the legal perimeter of the TARGET2 and as I explained above, despite all the technical changes, this system is still formally comprised of many national systems operated by Central Banks.

So, from the legal point of view, there is no one TIPS system, but each central bank that owns its TARGET2 national component also runs a “national part” of TIPS and should be described as a CSM compliant with SCT Inst.

Of course, since TIPS is a centralized platform, this formal arrangement is fully transparent for the participants when settling the payments.

Ok. Back to our main topic.

As we can imagine, after the implementation of the T2S and TIPS platforms, the whole TARGET2 infrastructure became quite complicated and challenging from the functional and technical points of view.

As a response, the Eurosystem launched the T2-T2S Consolidation project to improve efficiency and optimize the provision of its services.

This project resulted in the introduction of the new TARGET infrastructure which I will describe in the next article.

I hope that the above basic historical information, will allow us to understand the new architecture with ease.

|     |     |
| --- | --- |
| [<< TARGET Services (T2)](https://www.iso20022payments.com/target-services-t2/) | [TARGET Services Infrastructure >>](https://www.iso20022payments.com/target-services-t2/target-services-infrastructure/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme