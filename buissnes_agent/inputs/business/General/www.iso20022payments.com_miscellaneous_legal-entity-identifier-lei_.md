---
url: "https://www.iso20022payments.com/miscellaneous/legal-entity-identifier-lei/"
title: "Legal Entity Identifier (LEI) – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/miscellaneous/legal-entity-identifier-lei/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## Miscellaneous

## Legal Entity Identifier (LEI)

This article is about Legal Entity Identifier (LEI).

**What is LEI?**

LEI is a unique global identifier for legal entities participating in financial transactions worldwide.

It is a 20-digit alphanumeric reference.

LEI contains information about an entity’s ownership and thus tells us ‘who is who’ and ‘who owns whom’.

Below are a few examples of how LEI is introduced in ISO 20022 implementations.

**PMPG documents about LEI**

PMPG stands for **Payment Market Practice Group.**

I introduced this group in the following article: [Payments Market Practice Group](https://www.iso20022payments.com/miscellaneous/payments-market-practice-group/)

This group published several papers about LEI, e.g.:

- [LEI in the Payments Market (2017)](https://www.swift.com/swift-resource/139861/download)
- [The Adoption of LEI in Payment Messages (2019)](https://www.swift.com/swift-resource/229631/download)

The last document published by PMPG about LEI is a White paper:

- [Global adoption of the LEI (Legal Entity Identifier) in ISO 20022 Payment Messages (2021)](https://www.swift.com/swift-resource/251371/download)

A key notion expressed in this paper is that in the MT world, the ability to utilize the LEI was limited, with the implementation of ISO 20022, however, the benefits of the LEI can be fully realized.

The aim of the above document is to provide Market Practices on the LEI in payments and to provide clear use cases for more transparent, efficient, and secure payments.

This paper provides also information about the uptake of the LEI in Payment Systems and across several institutions.

**LEI in CBPR+**

In CBPR+ UHB we can understand LEI as one of the ways an Agent is identified.

However, LEI does not replace the BIC which still is the best practice to identify the Financial Institution.

From the schema perspective, LEI is not mandatory in the context of CBPR+ messages. Even for Financial Institution identification it is an optional element.

Nevertheless, for some elements, LEI usage is indicated in the CBPR+ rules.

For example in pacs.009 in the context of identification of Debtor, Debtor Agent, Creditor, Creditor Agent, Previous Instructing Agents and Intermediary Agents there are the following Textual rules:

**Rule “CBPR\_Agent\_Option\_1\_TextualRule”**

_BICFI, complemented optionally with an **LEI**(preferred option)_

**Rule “CBPR\_Agent\_Option\_2\_TextualRule”**

_(Clearing Code OR **LEI)** AND (Name AND (Unstructured postal address OR \[Structured postal address with minimum Town Name and Country\]). It is recommended to also add the post code when available._

It is worth mentioning that Textual rules are not validated on the network. Despite that, they form an important part of CBPR+ requirements.

Above, I talked about LEI in the context of Financial Institutions. But, LEI can also be used not only for FI but also for the identification of other parties, such as for example Debtor and Creditor in pacs.008.

**LEI in TARGET system**

Similarly to CBPR+ Usage Guidelines, LEI is not mandatory in messages processed in TARGET system.

What is interesting here, though, is the fact that LEI is mandatory during the reference data registration in the system, for the participant that wants to access RTGS settlement:

![](https://www.iso20022payments.com/wp-content/uploads/2023/02/LEI-TARGET.jpg)

Source: CRDM UDFS v3.0, 1.3.2.3. Description of the entities

This requirement is further clarified by TARGET SERVICES REGISTRATION AND ONBOARDING GUIDE, 4.2. REFERENCE DATA FIELDS where it is stated that branches should insert the LEI of the Head Office.

**LEI in SEPA**

In November 2023 version of SEPA Implementations Guidelines Identification/Organisation Identification also includes the possibility of using LEI.

For example, the description of the Ultimate Debtor/Identification/Organisation Identification in pacs.008.001.08 is the following:

![](https://www.iso20022payments.com/wp-content/uploads/2023/02/LEI-SEPA.jpg)

Source: SEPA Credit Transfer Scheme, Inter-PSP Implementation Guidelines, 2023 Version 1.0, 2.1.1 Use of FI to FI Customer Credit Transfer (pacs.008.001.08)

This brings us to the end of this topic.

I wanted to write this article as I presume LEI will be more and more important in the payments world.

|     |     |
| --- | --- |
| [<< T-account and Wash account](https://www.iso20022payments.com/miscellaneous/t-account-and-wash-account/) | [Mandatory vs. optional elements >>](https://www.iso20022payments.com/miscellaneous/mandatory-vs-optional-elements/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme