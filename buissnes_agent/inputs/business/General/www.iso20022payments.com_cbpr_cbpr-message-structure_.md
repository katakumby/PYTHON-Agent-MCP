---
url: "https://www.iso20022payments.com/cbpr/cbpr-message-structure/"
title: "CBPR+ message structure – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/cbpr/cbpr-message-structure/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## CBPR+

## CBPR+ message structure

Before we dive deep into the examples of CBPR+ messages, it is vital to understand the CBPR+ message structure.

This is the topic of this section.

We are going to begin with the high-level diagram which I prepared based on a similar one published in CBPR+ UHB.

Please find below the picture presenting the generic CBPR+ message structure.

**CBPR+ message structure**

![CBPR+ Message Structure 1](https://iso20022payments.com/wp-content/uploads/2022/12/CBPR-Message-Structure-1.jpg)

Based on: CBPR+ User Hnadbook, Q4 2022 Edition, p.12 SWIFT FINplus Message structure

As you can see there are two main parts of the CRBR+ message. The first is related to the technical aspect of the message and the second refers to the business information. In the picture, we can see that point **(1)** depicts the Request Header and point **(2)** refers to the business message. Generally, we will focus our analysis on point **(2)** that is on the business message. However, I thought that it might be useful to provide some key information on the **(1)**Request Header as well.

**Request Header**

Request Header is also known as **Technical Header**. What is this header about?

The CBPR+ messages are exchanged over SWIFT via FINplus service.

FINplus is built on another SWIFT service – InterAct service.

This information may not be necessarily crucial to everybody, because it is quite technical, however, it explains the source of the Request Header. Request Header is simply the header used in InterAct service, and as FINplus is built on InterAct, it also uses this header.

**The most important aspect of this header is the fact that banks are not identified here by Business Identifiers Codes (BICs), but by so-called Distinguished Names (DN).**This is not as complicated as it may sound, though, as there is a very straightforward way to map the BIC to DN.

In CBPR+ live environment 3 layer DN is used. As I said it is mapped from BIC in a simple way. As we know BIC11 composes of BIC8 and a 3-character Branch identifier. If there is no Branch identifier we put ‘XXX’ at the end of BIC8 to get BIC11.

Here is the way DN is formatted:

ou=live branch or xxx,o=live bic8,o=swift

What is also important, there is a specific terminology used in Request Header:

**Sender of the message is called Requestor**

**Receiver of the message is called Responder**

So, let’s bring all the above information together.

If we have **Bank A** identified with BIC **BANKFRAAXXX** sending the CBPR+ message to **Bank B** identified with BIC **BANKDEBBXXX** these two actors will be identified in the Request Header in the following way:

**Bank A** will be **Requestor** identified with the following DN: ou= **XXX**,o= **BANKFRAA**,o=swift

**Bank B** will be **Responder** identified with the following DN: ou= **XXX**,o= **BANKDEBB**,o=swift

I would like to stress here one more thing. You may have noticed that the description for DN refers to the Live BIC8, which is not only valid for the live environment. Also for test environments banks are identified with DN based on their live BIC8.

If so, we may ask, how arethe test messages identified?

**The different environments are identified in the Request Header not by DNs but based on Service name element.**

For example, for live environment Service name element will be populated with **swift.finplus** but for the pilot current environment Service name element will be populated with **swift.finplus!pc**.

This is how SWIFT distinguishes whether a particular message is a live or test message.

**In Request Header there is also an indication of what business message is included inside.** **For this, the** **RequestType element is used.**

In other words, RequestType element identifies the name of the ISO 20022 message processed. For example, for **pacs.009.001.08** the value of the RequestType element will be … precisely **pacs.009.001.08**.

I have provided here only the most important elements of RequestHeader.

More details about FINplus, InterAct and RequestHeader can be found in SWIFT documentation.

Now, let’s focus on point **(2)** from the above diagram, which is the business message.

**Business Message**

The business part of the message is also called Message Payload.

As we have seen in the diagram aboveit consists of two main elements: **Business Application Header** **(BAH)** and **ISO Message Instance**.

Let’s investigate how the Business Message will look if we zoom in a little.

This is the picture we get:

![Business Message](https://iso20022payments.com/wp-content/uploads/2022/12/Business-Message.jpg)

In the above diagram, we can already see some XML elements that form the generic structure of the Business Message.

One thing that I need to highlight here is that **Business Application Header** is a mandatory element in all CBPR+ messages.

On the other hand, the **Message Instance** structure depends on the message type used.

The above structure is presented with an example of pacs.009. This message apart from **Group Header** comprises **Credit Transfer Transaction Information**. The same general structure has pacs.008. However, this is not always the case. We are going to encounter messages that apart from Group Header have different blocks. Some messages (like camt.029 or camt.056) do not even have a Group Header element.

Let’s try now to dive even deeper into the message structure.

First, we are going to focus on the BAH.

**Business Application Header**

In this part, I am going to describe the BAH.

The elements marked with this symbol:

![Red dot](https://iso20022payments.com/wp-content/uploads/2023/01/Red-dot.png)

– are mandatory.

Please find below the most important elements of BAH (head.001).

![BAH](https://iso20022payments.com/wp-content/uploads/2023/01/BAH.jpg)

Apart from the elements that are described above, there are additional two in BAH that I would like to mention now:

- **Related** – this element allows capturing the BAH from the related message. We are going to describe this element while talking about Payment Return, where it will be used to point to the BAH from the original message.
- **Copy Duplicate** – as this element is associated with reporting messages, I will describe it while investigating camt messages.

**pacs.009**

Now it’s time for the Message Instance.

I would like to present the structure of this second part of the business message based on the pacs.009 example.

As other messages have different structures, it will not be a comprehensive description.

Nevertheless, I think that the below description may still be helpful, especially in the context of other pacs messages that share many characteristics.

As we have seen, even pacs.009 comprises two main parts:

- Group Header

- Credit Transfer Transaction Information


Let’s start with the description of the Group Header.

- **Group Header**

Please find below the most important elements of Group Header.

![Group Header](https://iso20022payments.com/wp-content/uploads/2023/01/Group-Header.jpg)

And now we move to the second part of pacs.009.

- **Credit Transfer Transaction Information**

Below are presented the most important elements of Credit Transfer Transaction Information.

This part is the largest one, so I have split the description into smaller pieces.

To begin with, there is an element **Payment Identification <PmtId>**, where a set of elements is provided to identify a payment.

To know more about point-to-point vs. end-to-end references please refer to this [section of my website](https://iso20022payments.com/cbpr/point-to-point-end-to-end/) where there is more information provided.

![Payment Identification](https://iso20022payments.com/wp-content/uploads/2023/01/Payment-Identification.jpg)

Now, let’s a have look at **Payment Type Information** **<PmtTpInf** \> element.

![Payment Type Information](https://iso20022payments.com/wp-content/uploads/2023/01/Payment-Type-Information.jpg)

After that we have several elements related to settlement:

![Settlement](https://iso20022payments.com/wp-content/uploads/2023/01/Settlement.jpg)

The following part is related to the (Previous) Instructing and Instructed Agents:

![Instructing Instructed Agents](https://iso20022payments.com/wp-content/uploads/2023/01/Instructing-Instructed.jpg)

If there is a business need for an Intermediary between Debtor Agent and Creditor Agent the following elements are used:

![Intermediary Agent 1](https://iso20022payments.com/wp-content/uploads/2023/01/Intermediary-Agent-1.jpg)

Then several elements on debit side are populated:

![Debtor](https://iso20022payments.com/wp-content/uploads/2023/01/Debtor_.jpg)

The similar elements are available on Creditor side:

![Creditor](https://iso20022payments.com/wp-content/uploads/2023/01/Creditor.jpg)

And the message finishes with a few elements containing additional information:

![Additional information](https://iso20022payments.com/wp-content/uploads/2023/01/Additional-information.jpg)

I hope the above presentation of the CBPR+ message structure will be useful.

**Additional information**

At the end, I would like to just turn your attention to the fact that for several elements many options may be used.

This is only to show how rich the ISO 20022 standard is.

The below examples present briefly how two basic elements (**an account** and **a party**) may be identified in the message.

- **An account**

Here are the options to identify the Debtor Account in the Usage Guidelines for pacs.009:

![Account](https://iso20022payments.com/wp-content/uploads/2023/01/Account.jpg)

As we can see on the left, **an account** may be identified by **IBAN** or by **another identification**.

Also, some additional information like **Type** or **Currency** may be added.

Additionally, **Type** can be populated as **Code** or **Proprietary information**.

What is important to highlight here is the fact that if we want to populate **Type** of the account with the **Code** the documentation directs us to the **ExternalCashAccountType1Code.**

We can see this in the picture above on the right.

But, where can we find codes that are allowed as **ExternalCashAccountType1Code?**

For that, we have to go to the ISO 20022 website.

There is a dedicated list available on the ISO 20022 website that consists of external codes. It is called **External code sets** and is available [here](https://www.iso20022.org/catalogue-messages/additional-content-messages/external-code-sets "External code sets").

When you search for the **ExternalCashAccountType1Code** in this file you will find that the following codes may be used:

![Account codes](https://iso20022payments.com/wp-content/uploads/2023/01/Account-codes.jpg)

If you need to determine **Type** but the **External code sets** list does not contain the code which fulfills your needs, you can use **Proprietary** format to forward this information.

- **A party**

Similarly to an account, a party in the payment message may be identified by several elements.

Here are possible identification elements for Debtor Agent:

![Party Identification](https://iso20022payments.com/wp-content/uploads/2023/01/Party.jpg)

Although there are many possibilities, as we can see BIC remains the most popular and recommended option for cross-border scenarios.

There is also an interesting identifier called LEI. If you want to know more about it you can visit the dedicated article on my website about [LEI](https://www.iso20022payments.com/miscellaneous/legal-entity-identifier-lei/).

|     |     |
| --- | --- |
| [<< Charges](https://iso20022payments.com/cbpr/charges/) | [Static vs. Dynamic Roles >>](https://www.iso20022payments.com/cbpr/static-vs-dynamic-roles/ "Static vs. Dynamic Roles (1) >>") |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme