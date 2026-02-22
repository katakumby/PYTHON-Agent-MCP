---
url: "https://www.iso20022payments.com/cbpr/static-vs-dynamic-roles-1/"
title: "Static vs. Dynamic Roles (1) – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/cbpr/static-vs-dynamic-roles-1/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## CBPR+

## Static vs. Dynamic Roles (1)

There is only one topic left before I will deep dive into CBPR+ example messages. This topic is related to Static and Dynamic Roles.

This is precisely the subject I am going to discuss in this article.

This article will be split into two parts. The **first part** aims to define what roles agents can play in the message. This is what we are going to discover below.

The **second part** will describe how these roles change in the subsequent messages during the payment chain processing.

Similarly to previous sections, in this one I also use pacs.009 as an example. However, the logic is the same for pacs.008.

The two main differences we should keep in mind are:

- in pacs.008 Debtor and/or Creditor are not Financial Institutions and
- in pacs.008 Debtor Agent and Creditor Agent are mandatory elements.

There are two remarks that I would like to make at the beginning of this article:

- as Debtor Agent and Creditor Agent are optional elements in pacs.009 they may not always be populated if the bank is also an Instructing or Instructed Agent for a particular payment leg. Let’s say that Bank X is a Debtor Agent. When Bank X sends the message it becomes Instructing Agent. As it plays already the role of Instructing Agent in this payment leg Bank X may not see the point of additionally identifying itself as Debtor Agent. However, in the below scenarios when there is Debtor Agent or Creditor Agent, I will always identify them in the message as such. Even if they play additionally the role of Instructing or Instructed Agent. To my mind, this approach makes the message more clear from a business point of view.

- in the scenarios below I assumed that Bank A which is the first bank in the payment chain knows all the payment intermediaries that should be populated in the message. This is usually done by consulting the Standing Settlement Instructions (SSI) where banks publish their correspondents for a particular currency.

So, let’s start with the first part of the Static vs. Dynamic Roles article.

**What roles can Agents have in the payment?**

The roles that actors play in the payment chain are populated in the **Credit Transfer Transaction Information** block of pacs.009.

To determine what roles can actors have we are going to look at the message from the first bank’s perspective.

The first bank in the payment chain will assign to each of the next banks their role by populating the appropriate elements in the first message. This will differ for each business case. The first bank will have to take into consideration how many banks will be involved in the payment chain based on their direct account relationship in the currency of the transfer. I discussed this topic earlier in [Cross-border payments](https://iso20022payments.com/cbpr/cross-border-payments/) article.

When we look at the message structure presented in the [CBPR+ message structure](https://www.iso20022payments.com/cbpr/cbpr-message-structure/) section, we can see the following mandatory roles agents have to play in the pacs.009:

- Instructing Agent
- Instructed Agent
- Debtor
- Creditor

In other words, the above 4 elements have to be populated in every business scenario of pacs.009.

But, is it possible to create a valid business scenario where only the above 4 elements are present? Indeed, it is.

So, let’s see what this basic scenario will look like.

Although we are going to use only 4 elements in this first scenario, I am going to already list all the elements of the pacs.009 that we will populate in this section. This, I hope, will allow us to easier spot the changes that each business case brings. Elements that are not present in the particular message analyzed are marked **in grey**.

**Scenario of pacs.009 exchanged between Bank A and Bank B.**

So, here is our scenario where only 4 mandatory elements are used.

There are only two banks involved. Bank A is a Debtor and Bank B is a Creditor.

Additionally, Bank A is an Agent that **instructs** the payment so it plays the role of **Instructing Agent**.

Bank B **is instructed** by Bank A. It plays the role of **Instructed Agent**.

Of course, to make this scenario possible there has to be a direct account relationship in the currency of the transfer between Bank A and Bank B.

![2 Banks](https://www.iso20022payments.com/wp-content/uploads/2023/01/2-Banks.jpg)

Now that we have seen the basic scenario, let’s try to extend the business case to include the third bank.

**Scenario of pacs.009 sent by Bank A (three banks involved in the payment).**

First of all, when we consider more than 2 banks involved in the payment it is important to highlight what payment method is used.

Here we are going to discuss the serial method, which means that messages are sent through a series of banks. Settlement of each payment leg is done on the Nostro/Vostro account that we talked about in [Settlement Method: INGA vs. INDA](https://iso20022payments.com/cbpr/settlement-method-inga-inda/) section. We are going to explore other payment methods in the future.

But, why there is a need to include the third bank in the first place?

It is necessary when Debtor and Creditor do not have a direct account relationship with each other in the currency of the transfer.

What will be the role of this third bank?

From the business perspective, this bank will have an account relationship with both Debtor and Creditor, so it will be Debtor Agent as well as Creditor Agent.

In other words, this bank will service the account for Debtor and for Creditor.

Additionally, this bank will be now instructed by Bank A, so it will take a role of Instructed Agent.

However, even if this bank is both Debtor Agent and Creditor Agent, CBPR+ User Handbook recommends in such a situation that in the message itself this bank is captured only in the Creditor Agent element.

So, when we form the message according to this CBPR+ recommendation it will look like that:

![3 Banks](https://www.iso20022payments.com/wp-content/uploads/2023/01/3-Banks.jpg)

The above diagram depicts a situation where Debtor and Creditor have the same correspondent. Of course, this is not always the case.

A more frequent scenario is with Bank A and Bank B having different correspondents. As you may guess, this will require the involvement of 4 banks in the payment chain. Debtor Agent and Creditor Agent will be populated separately in this message. Let’s have a look.

**Scenario of pacs.009 sent by Bank A (four banks involved in the payment).**

![4 Banks](https://www.iso20022payments.com/wp-content/uploads/2023/01/4-Banks.jpg)

As we already know the Debtor Agent services the account for the Debtor, and Creditor Agent services the account for the Creditor.

What’s important here is to emphasize that if the payment leg between Debtor Agent and Creditor Agent is done via CBPR+ message it requires that these Agents also maintain a direct account relationship in the currency of the transfer. In other scenarios, the settlement of that payment leg could be done via a Payment System, but in that case, it would not be a CBPR+ message. This was discussed in [Cross-border payments](https://iso20022payments.com/cbpr/cross-border-payments/).

As you certainly have guessed this is not the end.

Sometimes more than four banks may be involved in the transaction. In such a case we use the Intermediary Agent 1 role.

The Intermediary Agent 1 is an Agent that services account for both Debtor Agent and Creditor Agent.

**Scenario of pacs.009 sent by Bank A (five banks involved in the payment).**

![5 Banks](https://www.iso20022payments.com/wp-content/uploads/2023/01/5-Banks.jpg)

And yes, in cases where the Debtor Agent cannot reach the Creditor Agent through only one Intermediary Agent, two or even more Intermediary Agents may be involved, depending of course on the account relationship in the currency of the transfer among them.

As you may remember, the Intermediary Agents are classified in numeric order, so when there is a need for 6 banks to be involved in the payment we have to use Intermediary Agent 2 along with Intermediary Agent 1.

**Scenario of pacs.009 sent by Bank A (six banks involved in the payment).**

![6 Banks](https://www.iso20022payments.com/wp-content/uploads/2023/01/6-Banks.jpg)

In the end, I would like just to mention that even if our example looks quite complex, it does not exhaust all the possible scenarios. There is still room for additional Intermediary Agent 3.

In the table presenting the actors, we can see that Previous Instructing Agents 1 and 2 are still in**grey**. This means that they do not appear in the message sent by Bank A. However, let’s be patient. Maybe they will be populated in part 2 of this article?

The above example concludes the first part of this article.

In the second part, we are going to capitalize on this last example.

We are going to observe how the roles of the banks change on each payment leg.

|     |     |
| --- | --- |
| [<< Static vs. Dynamic Roles](https://www.iso20022payments.com/cbpr/static-vs-dynamic-roles/) | [Static vs. Dynamic Roles (2) >>](https://www.iso20022payments.com/cbpr/static-vs-dynamic-roles-2/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme