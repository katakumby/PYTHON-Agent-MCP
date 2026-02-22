---
url: "https://www.iso20022payments.com/miscellaneous/debtor-and-creditor-data-fatf-16/"
title: "Debtor and Creditor data (FATF 16) – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/miscellaneous/debtor-and-creditor-data-fatf-16/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## Miscellaneous

## Debtor and Creditor data (FATF 16)

This will be a brief article about Debtor and Creditor data in the context of FATF 16.

To begin with, let’s check what the CBPR+ pacs.008 rules for the identification of the **Debtor** and **Creditor** are.

The previous article about mandatory and optional elements available [here](https://www.iso20022payments.com/miscellaneous/mandatory-vs-optional-elements/) may be good background information for this part.

**Debtor and Creditor data (CBPR+)**

In the context of **Debtor** and **Creditor** data, it is important to investigate both:

- party elements ( **Debtor** and **Creditor**) as well as
- account elements ( **Debtor Account/Creditor Account**).

The first thing to notice is thatin CBPR+ pacs.008 **Debtor Account/****Creditor Account** are not mandatory elements.

And what about **Debtor** and **Creditor**?

Let’s take a look.

CBPR+ pacs.008 Usage Guidelines show requirements for **Debtor** element ( **Creditor** is similar) in the following way:

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/Debtor-2.png)

As we can see, from the pure schema perspective, **Debtor** and **Creditor** elements are mandatory (Min 1, Max 1).

However, each of their 4 child elements ( **Name, Postal Address, Identification, Country Of Residence**) is optional.

In other words, pure schema requirements do not tell us which child elements should be used to identify **Debtor**.

Does this mean that we can simply choose one of the child elements and it will work fine?

I am afraid not.

Which child elements should we use (and also in which configuration they may be used) is determined by CBPR+ business rules.

There are several business rules related to the **Debtor** and **Creditor**.

Below I present 3 of them (numbers have been assigned by me, not SWIFT), which are the most important for our analysis:

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/1.png)

**(** **1****)**Rule number 1 is a textual rule, so it is not validated by SWIFT.

It shows the relation between the usage of **Any BIC** and **Name** with **Postal Address**.

According to the description, **Any BIC** and **Name** with **Postal Address** are mutually exclusive.

So, either we identify Debtor:

- by **Any BIC** or
- by **Name** with **Postal Address**.

Here I would like to remind ourselves that the above refers to CBPR+ business rule. If we investigate rules which apply to high-value payment systems the situation may be different. For example, TARGET system points to the rule, according to which **BIC**, **Name** and **Address** are not mutually exclusive, and can be present together:

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/HVPS.png)

In this context, it is worth noticing the following comment in CBPR+ Usage Guidelines:

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/comment.png)

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/2.png)

**(** **2****)**When we analyze rule number 2, we see that the presence of the **Postal Address** makes **Name** mandatory.

In other words, we cannot provide only **Postal Address** without **Name**.

But, does it also work vice versa? We can learn about this from rule 3 below.

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/3.png)

**(** **3****)**What we can see is that rule number 3 is not symmetrical to rule number 2. In the absence of **Any BIC**, indeed **Name** becomes mandatory, however, **Postal Address** is only recommended.

So, it is possible to provide **Name** without **Postal Address.**

As a result, the pacs.008 message with the following **Creditor** information passes SWIFT validation:

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/Creditor-2.png)

We can imagine that the above is not a precise **Creditor** identification (“Pawel” means simply “Paul”).

Such **Creditor** identification will make it impossible to process the payment STP (without further investigation).

Additionally, precise **Debtor/Creditor** identification is important in the context of sanctions screening, compliance, AML, and so on…

And this is where FATF 16 comes into play to ensure that **Debtor** and **Creditor** data in payment messages are precise and accurate.

**FATF 16**

FATF stands for Financial Action Task Force (official website: [FATF](https://www.fatf-gafi.org/en/home.html)).

FATF is the global money laundering and terrorist financing watchdog.

It sets international standards that aim to prevent these illegal activities and the harm they cause to society.

In February 2012, FATF published revisions to its Recommendations.

You can access the updated document [here](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Fatf-recommendations.html). While reading it, it is important to look also at the Interpretive Notes, which include more detailed information.

For us important is Recommendation 16.

Recommendation 16 extends the scope of the former SRVII by applying the requirements to cross-border and domestic wire transfers, including serial payments and cover payments.

It aims to ensure that the necessary information on the **Debtor** and **Creditor** of wire transfers is immediately available to all the agents involved in the payment, in order to facilitate the identification of both customers as well as the reporting of suspicious transactions.

So, what is, according to FATF 16 the required information about **Debtor** and **Creditor** that has to be populated in the message?

I will not go into much detail in this article, but, in a nutshell, for cross-border payments, the recommendation stipulates the need for:

- Debtor’s name, address, account number and
- Creditor’s name and account number (even if the Creditor’s address is not required by FATF Recommendation 16 it is best practice to include it)

What is crucial to highlight is that FATF 16 is only the starting point.

The FATF 16 recommendation has been/can be implemented in national regulations with some variations. These can be related to different requirements for domestic vs. cross-border payments or the threshold for the payment to which a particular requirement applies.

In the **European Union**, for example, Regulation (EU) 2015/847 was introduced to implement Recommendation 16 (document available [here](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A32015R0847)).

Also, **PMPG** (more about this group [here](https://www.iso20022payments.com/miscellaneous/payments-market-practice-group/)) published the following document:

“Market Practice Guidelines for use of fields 50a Ordering Customer and 59a Beneficiary Customer to comply with FATF Recommendation 16”.

You can find this document [here.](https://www.swift.com/swift-resource/202336/download)

**PMPG** document is based on the FATF Recommendation 16 so it does not take into account regional regulators that may have additional or other requirements once the FATF Recommendation has been applied in their respective legal frameworks.

One thing to notice is that **PMPG** document is based on MT messages and not on ISO 20022, but it is still a valuable source of information.

There is also a document prepared by **Wolfsberg Group** related to Payment Transparency Standards (document available [here](https://www.wolfsberg-principles.com/sites/default/files/wb/pdfs/wolfsberg-standards/1.%20Wolfsberg-Payment-Transparency-Standards-October-2017.pdf)), which also points to **Name**, **Address**and **Account number** as the preferred option to comply with FATF 16.

This concludes this article.

I hope it will give you some basic knowledge about the way **Debtor** and **Creditor** can be identified and about FATF Recommendation 16.

In case more detailed information is needed, we can always consult the appropriate document linked in this article.

Another topic related to this one is structured vs. unstructured customer data. This, however, is for another time.

|     |     |
| --- | --- |
| [<< Mandatory vs. optional elements](https://www.iso20022payments.com/miscellaneous/mandatory-vs-optional-elements/) | next page >> |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme