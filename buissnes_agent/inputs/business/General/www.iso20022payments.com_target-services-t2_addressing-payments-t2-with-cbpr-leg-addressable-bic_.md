---
url: "https://www.iso20022payments.com/target-services-t2/addressing-payments-t2-with-cbpr-leg-addressable-bic/"
title: "Addressing payments: T2 with CBPR+ leg (Addressable BIC) – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/target-services-t2/addressing-payments-t2-with-cbpr-leg-addressable-bic/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## TARGET Services (T2)

## Addressing payments: T2 with CBPR+ leg (Addressable BIC)

In this article, I am going to continue the topic of addressing T2 payments.

This time, however, I would like to add CBPR+ leg to the equation.

The scenario described in this article is based on the examples published on the ECB website:

[Examples Multi-addressee and addressable BIC](https://www.ecb.europa.eu/paym/pdf/consultations/Examples_Multi_Addressee.xlsx)

Today I will analyze a payment to “Addressable BIC”, which from a technical perspective behaves as an Indirect participant.

This is presented in the “Scenario A Addressable BIC” sheet of the above Excel file.

The data shown below are taken from the ECB example.

What I tried to do is only to present them in a different way.

**ECB example**

The scenario is as follows:

Deutsche Bank, as an intermediary agent, receives a pacs.009 via CBPR+ from SOGEFRPP on behalf of SOGEFRPPLYP in favor of Commerzbank Madrid for further credit to Commerzbank Barcelona COBAESMXBAR.

Let’s have a look at the diagram illustrating this payment chain:

![](https://www.iso20022payments.com/wp-content/uploads/2023/10/Chain-Addressee-BIC.png)

As we can see after having received CBPR+ pacs.009 Deutsche Bank forwards it further via T2.

What can we say about this scenario?

**(1)** It’s always good to look first at the 4 static roles in the payment chain.

Here we have:

**SOGEFRPPXXX** – **Debtor Agent** who holds the account for **SOGEFRPPLYP** – **Debtor**.

**SOGEFRPPXXX** sends pacs.009 on behalf of the **SOGEFRPPLYP**.

On the other hand, **COBAESMXXXX** **– Creditor Agent** holds the account for **COBAESMXBAR – Creditor.**

This payment chain is about **SOGEFRPPXXX** reaching **COBAESMXXXX.**

How **SOGEFRPPXXX** will reach**COBAESMXXXX?**

**(2)**Firstly, **SOGEFRPPXXX** sends CBPR+ pacs.009 to **DEUTDEFFXXX.**

From the ECB example, we do not know why **SOGEFRPPXXX**sent CBPR+ pacs.009 to **DEUTDEFFXXX.**

I will come back to this question in the second part of the article.

For now, let’s assume that there is a business justification for **SOGEFRPPXXX**to address ****DEUTDEFFXXX****in the first place.

What addressing information does **SOGEFRPPXXX**include in this CBPR+ pacs.009?

We can see that **COBADEFFXXX**is depicted as Intermediary Agent 1, which means that **COBAESMXXXX** will be reached via **COBADEFFXXX.**

Why is that?

Well, this reflects the addressing rules included in the RTGS Directory which will be followed in the T2 leg of this payment chain.

**(3)** This is the extract from RTGS Directory, ECB attached with this scenario:

![](https://www.iso20022payments.com/wp-content/uploads/2023/10/RTGS-Directory-Addressee-BIC-1024x306.png)

**Note:** **COBAESMXBAR** is not in the RTGS Directory

As we can see, **COBAESMXXXX** is registered as “Addressable BIC” in RTGS Directory.

This means it cannot be reached directly in T2, because “Addressable BIC” CANNOT send and receive payments directly.

“Addressable BIC” is like an Indirect participant.

This direct participant for **COBAESMXXXX**is **COBADEFFXXX,**and as a result in the T2 payment leg:

- **COBADEFFXXX**(**Addressee BIC** in RTGS Directory) will be present in **BAH/To** element.
- **COBADEFFXXX**(**Account BIC** in RTGS Directory) will also be present in **Instructed Agent** element.

What we can’t see in the ECB example is the 3rd payment leg of this transaction.

I think it would be interesting to see what this pacs.009 would look like.

**Next payment leg**

We are in the moment where **COBADEFFXXX**as a Direct participant receives the pacs.009 via T2 from **DEUTDEFFXXX.**

In the next payment leg **COBADEFFXXX**sends the CBPR+ pacs.009 to **COBAESMXXXX.**

Let’s add this message to our diagram:

![](https://www.iso20022payments.com/wp-content/uploads/2023/10/3-leg-BIC-Addressee.png)

What can we see in this payment leg?

**(1)**First of all, the 4 static roles remain unchanged: Debtor, Debtor Agent, Creditor Agent, and Creditor.

**(2)** This pacs.009 is from**COBADEFFXXX** to **COBAESMXXXX.**

So, **COBADEFFXXX** is both in the BAH/From and Instructing Agent elements.

**COBAESMXXXX** is in both BAH/To and Instructed Agent elements.

**(3)**DEUTDEFFXXX**** is depicted in the message as Previous Instructing Agent 1.

Ok, earlier in the article I mentioned that I would come back to the role of the ****DEUTDEFFXXX**** in this payment chain.

Of course, there may be some business reasons for **SOGEFRPPXXX** to address the first message to****DEUTDEFFXXX****.

However, based on the excerpt from the RTGS Directory we have, can we think of another, alternative flow for this payment?

**Alternative example**

Let’s imagine that **SOGEFRPPLYP** instructs **SOGEFRPPXXX** to make an EUR payment to **COBAESMXBAR’s** account held at **COBAESMXXXX.**

This is the only routing information **SOGEFRPPXXX**gets.

When we translate this information into the message elements we get:

- **COBAESMXXXX** is the **Creditor Agent** and
- **COBAESMXBAR** is the **Creditor.**

**SOGEFRPPXXX** knows that the agent it has to reach is **COBAESMXXXX.**

What does**SOGEFRPPXXX**do?

Bacause this is an EUR payment, and **SOGEFRPPXXX** is a Direct T2 participant it checks whether **COBAESMXXXX** is reachable via T2 **.**

Let’s remind ourselves of the RTGS Directory:

![](https://www.iso20022payments.com/wp-content/uploads/2023/10/RTGS-Directory-Addressee-BIC-1024x306.png)

**SOGEFRPPXXX** looks for a BIC **COBAESMXXXX** in the first column of RTGS Directory.

It finds this BIC, meaning **COBAESMXXXX** can be addressed in T2.

Additionally, **SOGEFRPPXXX** knows from the RTGS Directory, what BICs should be populated in the BAH/To and Instructed Agent elements:

![](https://www.iso20022payments.com/wp-content/uploads/2023/11/BIC-Addressee-element-1024x219.png)

Based on the RTGS Directory, this is the pacs.009 **SOGEFRPPXXX** sends via T2 together with the next CBPR+ payment leg:

![](https://www.iso20022payments.com/wp-content/uploads/2023/10/Alt.-flow-BIC-Addressee.png)

**(1)** As we can see, since **SOGEFRPPXXX** is a Direct participant it can directly send a payment message to any other Bank reachable via T2.

In this alternative example, ****DEUTDEFFXXX**** does not appear in the payment chain.

**(2)** Because **COBAESMXXXX**is an “Addressable BIC” in T2 and is reachable via a **COBADEFFXXX, COBADEFFXXX** appears in both BAH/To and Instructed Agent elements.

**(3)** The 4 main static roles remain unchanged in comparison to the previously discussed ECB example:

Debtor – **SOGEFRPPLYP**

Debtor Agent – **SOGEFRPPXXX**

Creditor Agent – **COBAESMXXXX**

Creditor – **COBAESMXBAR**

(4) Having received the T2 payment from SOGEFRPPXXX, COBADEFFXXX learns from the message that the next agent to be reached is **COBAESMXXXX**(Creditor Agent).

(5) COBADEFFXXX sends CBPR+ pacs.009 to **COBAESMXXXX.**

This brings us to the end of this article.

In the next one, I will also explore the T2 and CBPR+ payment legs, however in the context of the “Multi-addressee” participant.

|     |     |
| --- | --- |
| [<< Addressing payments in T2: Participation types](https://www.iso20022payments.com/target-services-t2/addressing-payments-in-t2-participation-types/) | [Addressing payments: T2 with CBPR+ leg (Multi-Addressee) >>](https://www.iso20022payments.com/target-services-t2/addressing-payments-t2-with-cbpr-leg-multi-addressee/%20) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme