---
url: "https://www.iso20022payments.com/cbpr/point-to-point-end-to-end/"
title: "Point-to-point vs. End-to-end – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/cbpr/point-to-point-end-to-end/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## CBPR+

## Point-to-point vs. End-to-end

In this section, we are going to explore the idea of point-to-point and end-to-end data exchanged in payment messages.

This is an important notion for transactions in which several subsequent messages are processed.

**Point-to-point** describes the data that is exchanged only in one payment leg. Because the data is meaningful for this one particular payment leg, it does not need to be present in subsequent messages.

**End-to-end** describes the data that has to be passed unchanged throughout the whole payment chain.

This aspect is of paramount importance in the context of references.

Let’s have a look at some examples.

**Point-to-point**

An example of point-to-point reference is **Instruction Identification**.

This is a reference meaningful to the party sending the message.

Banks can have their own reference structure that is understood within the bank and used for a particular payment processing.

In CBPR+ Instruction Identification is restricted to 16 characters to make it directly comparable to field 20 of an MT message.

Our business scenario comprises the interbank transaction in USD, which consist of two pacs.009 messages sent on the first of April 2023 (in the American format it will be: 040123).

Bank A and Bank B have the following method to generate the Instruction Identification:

**(** **1** **)** Bank A has in its reference: **message type**, **date**, and **message number** per day. – **0090401230000001**(for Bank A it will be its first pacs.009 on that day)

**(2** **)** Bank B has in its reference: **date**, **currency**, and **message number** per day – **0** **40123USD0000005**(for Bank B it will be its fifth pacs.009 on that day)

The Instruction Identification in that payment chain will look the following way:

![Point to point](https://iso20022payments.com/wp-content/uploads/2022/12/Point-to-point.jpg)

Bank A generates the payment message with Instruction Identification created according to its own rules.

Bank B receives the pacs.009 with the Instruction Identification created by Bank A, but it sends the pacs.009 to Bank C with the newly created Instruction Identification.

**End-to-end**

In contrast to Point-to-point references, End-to-end references have their meaning for the whole transaction cycle.

There are two particularly important end-to-end references we should consider: **End to End Identification** and **UETR.**

**End to End Identification** – This reference is provided by the Debtor.

It may happen that Debtor does not provide End to End Identification. As this reference is obligatory, the Debtor Agent may in such scenario populate “NOTPROVIDED”.

In our example, Bank A sends the pacs.009 on its own behalf, so Bank A is a Debtor.

Bank A can still generate the End to End Identification that will be meaningful or generate random references created by their system.

Let’s assume that Bank A took the first option, and it creates End to End Identification by just adding to the Instruction Identification the 6-character identification of the back-office application that generated the payment.

In our scenario pacs.009 was generated in Bank A by the system called **FOREX1**. So, End to End Identification will be: **0090401230000001**FOREX1****

The above reference will have to be passed by Bank B to Bank C and if Bank C is not a Creditor, it will have to be reported by Bank C to the Creditor.

**UETR –** UETR stands for **Unique End-to-end Transaction Reference.**

According to the CBPR+ Usage Guidelines, it is a ‘Universally unique identifier to provide an end-to-end reference of a payment transaction’.

What is the difference when compared to the **End to End Identification**?

The key word here is ‘ **Universally**‘. UETR is a ‘ **Universally unique identifier** …’. It means that this reference should be understood in an even wider context than only this particular payment chain.

The UETR is used by SWIFT gpi service and SWIFT Transaction Manager.

To ensure the uniqueness of this reference, it has to be generated according to the UUIDv4 standard and it has a particular pattern.

Let’s assume that UETR used by Bank A is the following:

**d0b7077f-49fb-42ed-b78d-af331c0e5012**

When we include the end-to-end references in our example, we get the following result:

![End to end](https://iso20022payments.com/wp-content/uploads/2022/12/End-to-end.jpg)

And this is how the above references look like in the pacs message sent by **Bank B**:

![References in message](https://iso20022payments.com/wp-content/uploads/2022/12/References-in-message.jpg)

This brings us to the end of this article.

Of course, needless to say, the examples above are fictitious. Every bank has its own policy when generating references.

I hope, however, that this article was useful to understand the logic of point-to-point and end-to-end data in the payment chain.

|     |     |
| --- | --- |
| [<< Settlement Method: INGA vs. INDA](https://iso20022payments.com/cbpr/settlement-method-inga-inda/) | [Charges >>](https://iso20022payments.com/cbpr/charges/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme