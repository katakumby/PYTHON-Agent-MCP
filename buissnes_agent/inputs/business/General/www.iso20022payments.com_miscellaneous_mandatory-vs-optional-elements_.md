---
url: "https://www.iso20022payments.com/miscellaneous/mandatory-vs-optional-elements/"
title: "Mandatory vs. optional elements – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/miscellaneous/mandatory-vs-optional-elements/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## Miscellaneous

## Mandatory vs. optional elements

In this article, I am going to investigate how to determine whether a particular element in ISO 20022 message is mandatory or optional.

Our analysis will be based on the way the elements are visible in the Usage Guidelines on MyStandards portal.

**Basic information**

In XML world the cardinality of the message element is defined using minimum ( **Min**) & maximum ( **Max**).

**Min** and **Max** describe the occurrences of each element.

At first sight, it seems to be very straightforward:

- If **Min** is **0** then the element is optional
- If **Min** is **1** then the element is mandatory
- If **Max** is **1** then no more than 1 occurrence is possible
- If **Max** is **\*** then unlimited occurrences are possible

Every element has both **Min** and **Max** assigned.

When we join together both pieces of information we get the following cardinality options:

**Min** **Max**

**0         1**     – an optional element that may be present once

**0         \***     – an optional element with unlimited repetitions

**1         1**     – a mandatory element that must be present exactly once

**1         \***     – a mandatory element with unlimited repetitions

So, for example, we can see in the pacs.008 Usage Guidelines that for the Group Header **Min** is set to **1** and **Max** is also set to **1**:

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/Group-Header-UG.png)

It means that CBPR+ pacs.008 **Group Header** element is mandatory but only one occurrence is possible.

It seems that this topic is relatively easy, isn’t it?

Before jumping to such conclusion let’s have a look at cardinality more closely.

**Hierarchical structure**

You may have noticed in MyStandards that in front of the tag name drop-down arrows are presented.

We can see an example of such symbol in the below picture (on the left-hand side):

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/Settlement-Information.png)

The arrow before **Settlement Information** tag is pointing down which means that the embedded elements are visible.

**Settlement Information** is a complex element that contains other, nested child elements.

**Settlement Information** tag has **Min 1** and **Max 1** which means that it has to appear in the message.

However, child elements may be mandatory or may be optional.

The above picture shows that **Settlement Method** is mandatory, but **Settlement Account** is not.

What can we learn from the above picture?

First of all, it is crucial to understand that XML messages have a hierarchical structure.

Consequently, it is crucial to look at the whole XML path to learn whether a particular element has to appear in the message or not.

The above notion will surely become clearer when we consider an example.

Let’s imagine that we have to determine if the pacs.008 element identified by the following path is mandatory or optional:

**/Document/FIToFICstmrCdtTrf/GrpHdr/SttlmInf/SttlmAcct/Id/Othr/Id**

This element in Usage Guideline has **Min 1** and **Max 1**.

Nevertheless, this does not necessarily mean that this element has to appear in every pacs.008 message!

When we consider the whole XML path of this element we can observe that Settlement Account (marked below in yellow) is not mandatory.

So, if the Settlement Account is not present, consequently our element will not appear either.

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/Settlement-Account.png)

Alla

**Choice element**

There is one more issue that is worth looking into.

To discover it we are going to investigate another XML element.

The question, however, remains the same:

Is the pacs.004 element identified by the following path

**/Document/PmtRtr/TxInf/RtrChain/Cdtr/Agt/FinInstnId**

mandatory?

In other words, does it always have to appear in pacs.004 message?

When we repeat the same exercise from the previous example, we can see that all the elements in the XML path are marked with **Min 1** and **Max 1**:

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/Creditor-pacs.004.png)

If all the elements in the path have **Min 1** and **Max 1** the element in question has to appear in the message. Correct?

Well, before answering this question we have to take into account another symbol presented in the picture.

Just before **Creditor** element, we can see the following symbol:

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/Creditor.png)

This symbol indicates that **Creditor** is a choice element.

It means that one of the tags defined underneath must be chosen.

What’s crucial, only one of the values under this element may be picked. Both cannot be used together.

**Creditor** element has two child elements: **Party** and **Agent**.

One of the two child elements must be present. However, there are mutually exclusive. So, either **Party** or **Agent** is used.

If **Party** element is chosen, then our element will not appear in the message.

I tested the following **Debtor** element (with **Party** instead of **Agent**) and CBPR+ Readiness Portal confirmed that it is a valid message:

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/Creditor-1.png)

In this message, the element we were investigating: **/Document/PmtRtr/TxInf/RtrChain/Cdtr/Agt/FinInstnId**is not present.

**Other examples**

It sometimes happens that the **optional element** has **child elements** which are **all mandatory**.

For example, **Charges Information** in pacs.008 is an optional and repetitive element.

If used, both elements **Amount** and **Agent** are mandatory with each repetition:

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/Charges-Information.png)

On the other hand, a **mandatory element** can have several **child elements** that are **all optional**.

For example, **Debtor** in pacs.008 is a mandatory element, with all child elements being optional:

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/Debtor.png)

From the **Min** and **Max** information in the above picture, we could guess that if none of the **Debtor** child elements is mandatory then any **Debtor** identification will be sufficient. Correct?

So, let’s test it by populating only the last element under **Debtor,** which is **Country Of Residence**.

If I test the message with **Debtor** identified in this way…

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/Debtor-1.png)

… I get an error.

Why is that?

This is because the **Min** and **Max** are not the only indicators of whether the particular element is sufficient in the message or not.

**Min** and **Max** define cardinality based on XSD.

These indicators do not include, however, other requirements stemming from the CBPR+ business rules.

Testing the above **Debtor** element I got the following error description:

**If AnyBIC is absent then Name is mandatory and it is recommended to also provide the Postal Address.**

When I replaced the **Country Of Residence** with **Name …**

![](https://www.iso20022payments.com/wp-content/uploads/2023/04/Debtor-Name.png)

… CBPR+ Readiness Portal informed me, that the message is valid.

To sum up, from the XSD perspective both **Country Of Residence** and **Name** are similar when it comes to cardinality.

What makes one of them sufficient and the second one not sufficient are the CBPR+ business rules.

There are several types of CBPR+ rules, that we should consider: Formal Rules, Textual Rules, Guideline Rules, Cross Element Rules.

But this is a subject for another article.

|     |     |
| --- | --- |
| [<< Legal Entity Identifier (LEI)](https://www.iso20022payments.com/miscellaneous/legal-entity-identifier-lei/) | [Debtor and Creditor data (FATF 16) >>](https://www.iso20022payments.com/miscellaneous/debtor-and-creditor-data-fatf-16/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme