---
url: "https://www.iso20022payments.com/cbpr/static-vs-dynamic-roles-2/"
title: "Static vs. Dynamic Roles (2) – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/cbpr/static-vs-dynamic-roles-2/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## CBPR+

## Static vs. Dynamic Roles (2)

In the first part of this article we explored how Bank A should address pacs.009 depending on the number of banks involved in the payment chain and the direct account relationship in the currency of the transfer.

Now we are going to complement our analysis with information on how the roles of the banks will change during the subsequent steps of payment processing.

Let’s start where we finished the first part.

Below is the pacs.009 that Bank A addressed taking into account that there are 6 banks involved in the payment chain.

**pacs.009 from Bank A**

![From A](https://www.iso20022payments.com/wp-content/uploads/2023/01/From-A.jpg)

We built this message in the previous part.

You may have noticed, however, that I introduced some additional information to the above diagram. These are directly linked to the subject of this article.

First of all, you can see that I assigned to some roles the padlock symbol.

This is to highlight that:

**![](https://www.iso20022payments.com/wp-content/uploads/2023/01/padlock.png)Debtor**

**![](https://www.iso20022payments.com/wp-content/uploads/2023/01/padlock.png)**

**Debtor** **Agent**

**![](https://www.iso20022payments.com/wp-content/uploads/2023/01/padlock.png)Creditor** **Agent**

**![](https://www.iso20022payments.com/wp-content/uploads/2023/01/padlock.png)Creditor**

are **Static roles** in the message.

This means that once a particular bank is assigned any of these roles it keeps it for each payment leg. These roles do not change.

On the other hand, you may have noticed that I colored the **Instructing Agent** and **Instructed Agent** in pink. As you may remember the Instructing Agent may be understood as the Sender of the message. It instructs the Instructed Agent, that may be understood as the Receiver of the message. In other words, Instructed Agent is the next party in the payment chain after Instructing Agent. We may say that these Agents play [point-to-point](https://iso20022payments.com/cbpr/point-to-point-end-to-end/) roles in the message.

I used pink color to emphasize that these two roles change for each payment leg. They represent **Dynamic roles** in the message.

And what about Intermediary Agents?

Bank E is the first Intermediary Agent and Bank F is the second one. They are classified in numeric order. But, are these static or dynamic roles?

Let’s find out by setting this pacs.009 in motion.

**pacs.009 from Bank C**

![From C](https://www.iso20022payments.com/wp-content/uploads/2023/01/From-C.jpg)

The above diagram depicts the second message in the payment chain.

We know that Debtor, Debtor Agent, Creditor Agent and Creditor remain the same. These are static roles. There is no change there.

This message is sent by Bank C (Instructing Agent) to Bank E (Instructed Agents). As Bank E plays the role of Instructed Agent there is no need for an additional role for this bank.

And Bank F’s role reveals to us what is the nature of Intermediary Agents. Bank F in the previous message was Intermediary Agent 2 and now it becomes Intermediary Agent 1. We learned earlier that Intermediary Agents are classified in numeric order, now we additionally know that their numbers change with each payment leg. In other words, Intermediary Agents are another example of a **Dynamic role**.

**pacs.009 from Bank E**

![From E](https://www.iso20022payments.com/wp-content/uploads/2023/01/From-E.jpg)

The next message is from Bank E.

Here Bank E plays the role of Instructing Agent and Bank F plays the role of Instructed Agent. There is no need for additional roles for these banks.

You may have noticed that at this stage Intermediary Agents disappear from the message.

Static Roles with assigned padlock icons remain the same.

**pacs.009 from Bank F**

![From F](https://www.iso20022payments.com/wp-content/uploads/2023/01/From-F.jpg)

And this is the last pacs.009.

You may wonder why I say so. Why there is no pacs.009 sent by Bank D to Bank B? There is, after all, an arrow pointing from Bank D to Bank B.

It’s a very good and important question.

To understand this let’s ask ourselves which bank holds the account that has to be credited with this payment.

We know that Bank B is the Creditor so Bank B owns the account to be credited. But this information still does not answer our question.

Is the account to be credited opened in Bank B? No.

This is indeed Bank’s B account but it is Bank D (as Creditor Agent and Account Servicing Institution) that holds this account for Bank B.

From the Bank B perspective this is a Nostro account. This is explained in the following section [Cross-border payments](https://iso20022payments.com/cbpr/cross-border-payments/).

Instead of sending another pacs.009 what Bank D does is to report to Bank B the credit entry on Bank’s B account. There are two messages usually used in this context. For end-of-the reporting, this is done by camt.053 Bank to Customer Statement. Additionally Bank B may be notified by camt.054 Bank to Customer Debit Credit Notification. We are going to explore both messages in the CBPR+ section.

Ok, so now we know why this is the last pacs.009. But is there something interesting going on in this message?

By this time we know that static roles remain the same during the payment processing, and we understand the behaviors of Instructing and Instructed Agent.

What is interesting though in this last message is the appearance of Previous Instructing Agent 1. It’s the first time, the Previous Instructing Agent 1 role has been used.

How to understand this role? It’s in fact quite simple.

One message earlier Bank E was **Instructing Agent**. So in this message, it plays the role of **Previous Instructing Agent 1**. In other words, Bank E **previously** was **Instructing Agent**.

As you can see, I also added the padlock icon to this role. This is to indicate that this is another static role. If there were further pacs.009 messages in this payment chain, Bank E would still play in them the role of Previous Instructing Agent 1.

But, you may ask, why didn’t we use this role earlier for Bank A or Bank C.

Bank A was Instructing Agent in the first message and Bank B was Instructing Agent in the second message. Right? Shouldn’t they have been indicated as Previous Instructing Agents as well?

The answer is: no. We are not expected to populate Debtor and Debtor Agent with Previous Instructing Agent role.

This is because Debtor and Debtor Agent are already important static roles themselves so there is no need to additionally assign them another role.

On the contrary, for Bank E, Previous Instructing Agent 1 is the only role it plays in this message. In this case, it is necessary to use this role to show the participation of Bank E in the payment chain.

Similarly to Intermediary Agents, Previous Instructing Agents are also classified in numeric order. If there were additional pacs.009 sent in this payment chain, Bank F would become Previous Instructing Agent 2.

This brings us to the end of this article.

The topic investigated here was an important one.

An insight into the roles that agents play in the payment chain will certainly help to deepen our understanding of the message content.

|     |     |
| --- | --- |
| [<< Static vs. Dynamic Roles (1)](https://www.iso20022payments.com/cbpr/static-vs-dynamic-roles-1/) | [pacs.009 >>](https://www.iso20022payments.com/cbpr/pacs-009/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme