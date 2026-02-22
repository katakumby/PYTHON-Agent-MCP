---
url: "https://www.iso20022payments.com/sct-inst-tips/instant-payment-between-two-tips-participants/"
title: "Instant Payment between two TIPS participants – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/sct-inst-tips/instant-payment-between-two-tips-participants/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## SCT Inst & TIPS

## Instant Payment between two TIPS participants

In this article we are going to explore the Instant Payment process in TIPS.

We have to be aware that TIPS supports different process flows, based on:

- SCT Inst scheme,
- Non-Euro settlement scheme,
- Single Instructing Party (SIP) settlement model.

In my articles, I mainly focus on payment transactions following the SCT Inst scheme.

Additionally, there are two types of payment transactions:

1\. Instant Payment

2\. Positive Recall Response

In this article I am going to focus on Instant Payments process flow (point 1).

Positive Recall Response (point 2) will be described in other article.

The messages used are:

- FItoFICustomerCreditTransfer (pacs.008.001.08) sent to instruct the Instant Payment transaction
- FIToFIPaymentStatusReport (pacs.002.001.10) sent:
  - to TIPS to either accept or reject the Instant Payment transaction
  - by TIPS to inform the actors about the result of the settlement

Below is the diagram with the basic scenario of a payment between two TIPS Participants: PSPAAAAAXXX and PSPBBBBBXXX.

This positive scenario depicts a successful payment transaction settled on TIPS DCAs.

Another assumption is that PSP A and PSP B connect to TIPS directely (no Instructing Party different from the TIPS Participants is involved).

![](https://www.iso20022payments.com/wp-content/uploads/2024/07/Between-two-participants-dobre.jpg)

The first thing to notice in the diagram is that there are no actual Originator and Beneficiary presented.

This is because the perimeter of TIPS is limited to the interactions with TIPS Parties or institutions acting on their behalf. The communication between the actual Originator and Beneficiary of a payment (i.e. the individuals or institutions transferring funds between each other, which may be customers of the Originator/Beneficiary Participants) is out of the TIPS scope and handled by each TIPS Participant/Reachable Party independently.

So, TIPS is interacting directly with PSP A and PSP B but not with their customers.

Below there is a description of the main points from the diagram.

Of course, this is not as detailed as the description in TIPS UDFS, but I hope it will allow to get a good understanding of the crucial steps.

To make the description more precise I added information about possible statuses for Instant Payment transaction.

Generally, in TIPS:

- there are three intermediary statuses: Received, Validated, Reserved
- there are three final unsuccessful statuses: Failed, Expired, Rejected
- there is one final successful status: Settled

Please bear in mind, that this is a description of a positive scenario.

However, I also included some information related to unsuccessful paths (marked in red).

**(1) Payment transaction (pacs.008)**

PSP A sends an SCT Inst payment transaction to TIPS.

PSP A is a TIPS Participants connected directly to TIPS.

Please find here the example of this message: [pacs.008](https://www.iso20022payments.com/wp-content/uploads/2024/07/pacs.008.txt)

The message contains the following elements:

- Debtor Agent BIC: PSPAAAAAXXX
- Creditor Agent BIC: PSPBBBBBXXX

Please bear in mind that according to the SEPA Instant Credit Transfer Rulebook:

- Debtor Agent BIC in pacs.008 is defined as the BIC code of the Originator PSP. Following this definition Debtor Agent BIC is called in TIPS: Originator BIC.
- Creditor Agent BIC in pacs.008 is defined as the BIC code of the Beneficiary PSP. Following this definition Creditor Agent BIC is called in TIPS: Beneficiary BIC

The most important thing about the above BICs is that:

- PSPAAAAAXXX has to be defined as Account Authorised BIC for PSP A’s TIPS DCA
- PSPBBBBBXXX has to be defined as Account Authorised BIC for PSP B’s TIPS DCA.

This is crucial as Authorised Account User specifies a BIC that is allowed to use the related TIPS DCA.

As we are going to see, TIPS uses these BICs to determine the accounts on which settlement should take place.

An Instant Payment transaction entering the system for the first time is temporarily in **Received**status while it undergoes the TIPS validations.

**(2) TIPS validates the transaction**

First TIPS validates the incoming message.

All the checks are described in Chapter 4.1 – Business Rules of TIPS UDFS.

In our example, Instant Payment transaction passes all validations successfully and becomes **Validated**.

**Unsuccessful scenario:**

If the Instant Payment transaction did not pass one of the validation checks, than pacs.002 would be sent to PSP A containing the proper error code.

Unsuccessful validation may set the transaction status to:

- **Expired** (if Originator timeout expired) or
- **Failed** (any other possible error).


**(3) TIPS reserves the relevant amount**

At this point the next step of the process begins with the attempt to reserve the required cash amount on the relevant debit account.

Bear in mind, that payments are always settled for the full amount; partial settlement is not foreseen in TIPS.

How TIPS determines the accounts involved?

- TIPS identifies the account to be debited as the account for which Originator BIC is defined as authorised user. In our example PSPAAAAAXXX is the AAU for PSP A’s TIPS DCA.
- TIPS identifies the account to be credited as the account for which Beneficiary BIC is defined as as authorised user. In our example PSPBBBBBXXX is the AAU for PSP B’s TIPS DCA.

In our example the amount on PSP A’s DCA is sufficient and reservation is successful.

The transaction is set to **Reserved** status.

A **Reserved** Instant Payment transaction may subsequently change its status into one of the four final statuses, depending on the outcome of the next steps.

While the cash amount is reserved, it cannot be used for settlement in a different payment or liquidity transfer.

**Unsuccessful scenario:**

If for any reason the reservation is unsuccessful (e.g. because either the cash balance on the account is insufficient or the account is blocked) its status changes to **Failed**.

**(4) TIPS forwards the transaction (pacs.008) to PSP B**

After the reservation of funds, TIPS forwards the payment transaction for acceptance to the receiving participant.

In our example PSP B is a TIPS Participant directly connected to TIPS.

PSP B does not outsource connectivity to the Instructing Party.

The DN of the PSP B is identified based on the “Outbound DN-BIC Routing” mapping table from the element Creditor Agent in pacs.008.

**(5) PSP B replies with pacs.002**

PSP B shall respond to TIPS with a beneficiary reply, either confirming or rejecting the payment.

The element Original Message Identification in pacs.002 should match with the Identification of the original message (pacs.008).

In our example, PSP B confirms the payment by sending pacs.002 with a positive answer – ACCP.

In the message either Group Status or Transaction Status element must be used. If incoming pacs.002 from Beneficiary Participant does not include any status or both are filled in, connected payment transaction will be rejected by TIPS.

As in our example PSP B replies with positive message, the settlement process starts.

**Here, several unsuccessful scenarios may occur:**

- If TIPS does not receive a reply from the Beneficiary Participant within a standard, configurable timeout period, the Instant Payment times out and the transaction moves to status **Expired**.
- If the Beneficiary Participant rejects the Instant Payment, the transaction moves to status **Rejected**.
- If the Beneficiary Participant confirms or rejects the Instant Payment but any kind of error occurs, the transaction moves to status **Failed**.


**(6) Settlement process**

Upon receiving Beneficiary Participant reply, TIPS identifies the transaction based on Original Message Identification element in pacs.002.

The transaction must be in status **Reserved**.

If the Beneficiary Participant confirms the Instant Payment and TIPS settles it successfully, the transaction moves to status **Settled**.

Additionally, the reserved amount of the Originator Account is decreased by the amount of the corresponding settled transaction.

This is exactly what happens in our example:

- PSP A’s TIPS DCA is debited
- Reserved funds on PSP A’s TIPS DCA are decreased with the same amount
- PSP B’s TIPS DCA is credited

The transaction status is turned into **Settled**. This makes the payment Irrevocable.

**Unsuccessful scenarios:**

When payment is moved to one of the unsuccessful statuses ( **Expired**, **Rejected**, **Failed**) then the reserved amount is automatically released and can then be once again used for settlement.

TIPS sends a negative status report to the Originator and Beneficiary Participants.

**(7) TIPS confirms settlement to the PSP A (pacs.002)**

TIPS confirms settlement to PSP A by forwarding the received pacs.002 to PSP A.

**Unsuccessful scenario:**

When payment is moved to one of the unsuccessful statuses ( **Expired**, **Rejected**, **Failed**) TIPS sends a negative status report to Originator Participant.

**(8) TIPS confirms settlement to the PSP B (pacs.002)**

TIPS generates a positive Payment status report and sends it to PSP B.

**Unsuccessful scenarios:**

When payment is moved to one of the unsuccessful statuses ( **Expired**, **Failed**) TIPS sends a negative status report to Beneficiary Participant.

|     |     |
| --- | --- |
| [<< Settlement options in TIPS](https://www.iso20022payments.com/sct-inst-tips/settlement-options-in-tips/) | [Instant Payment between two Reachable Parties >>](https://www.iso20022payments.com/sct-inst-tips/instant-payment-between-two-reachable-parties/)<br> >> |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme