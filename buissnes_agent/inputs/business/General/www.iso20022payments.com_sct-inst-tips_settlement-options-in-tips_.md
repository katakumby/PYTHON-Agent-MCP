---
url: "https://www.iso20022payments.com/sct-inst-tips/settlement-options-in-tips/"
title: "Settlement options in TIPS – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/sct-inst-tips/settlement-options-in-tips/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## SCT Inst & TIPS

## Settlement options in TIPS

Some time ago I was wondering about settlement options in TIPS for Instant Payment transactions following the SCT Inst scheme.

This article was created as a result of my thought process.

I started investigating this topic by looking at the two important elements of pacs.008:

- Debtor Agent BIC (Originator BIC) (/Document/FIToFICstmrCdtTrf/CdtTrfTxInf/DbtrAgt/FinInstnId/BICFI)
- Creditor Agent BIC (Beneficiary BIC) (/Document/FIToFICstmrCdtTrf/CdtTrfTxInf/CdtrAgt/FinInstnId/BICFI)

These elements are mandatory in pacs.008 sent to TIPS.

When TIPS receives pacs.008 it compares two BICs from the above elements with reference data kept in the system.

One of the important checks is to verify whether these BICs are defined as so-called Authorized Account Users (AAUs) in TIPS, which is necessary for the settlement to take place.

So, let’s imagine that TIPS receives pacs.008 with:

- Debtor Agent BIC (Originator BIC) = **PSPAAAAAXXX**
- Creditor Agent BIC (Beneficiary BIC) = **PSPBBBBBXXX**

We already know, that to successfully process this payment both BICs ( **PSPAAAAAXXX**, **PSPBBBBBXXX**) should be defined as Authorized Account Users (AAU) in TIPS.

The situation so far can be illustrated in the following way:

![](https://www.iso20022payments.com/wp-content/uploads/2024/09/Debtor-and-Creditor-Agent.png)

To explore further the possible settlement options in TIPS we have to look closer at the functionality of AAU.

Each AAU specifies a BIC which is allowed to use the related account or CMB for settlement.

AAU can be linked:

- directly to an account (“TIPS Account” or “TIPS AS Technical Account”), or
- to CMB that is linked to an account (“TIPS Account” or “TIPS AS Technical Account”)

TIPS does not only check whether BICs are defined as AAUs, but it also checks to what account or CMBs the AAUs are linked.

Based on this information, the settlement is performed on a specific account or CMB.

If we add to the above diagram, the possible options of accounts or CMBs that AAU can be linked to, we get the following picture:

![](https://www.iso20022payments.com/wp-content/uploads/2024/09/AAUs-configuraton.png)

How to read this diagram?

On the top, we can see two elements in the pacs.008:

- Debtor Agent BIC
- Creditor Agent BIC

TIPS checks what values are populated in these elements.

Debtor Agent BIC contains value ‘ **PSPAAAAAXXX**‘

Creditor Agent BIC contains value ‘ **PSPBBBBBXXX**‘

As we know these BICs have to be defined as AAUs in TIPS.

TIPS checks whether they are registered as AAUs and to what account or CMB they are linked.

In the middle we can see the possible links for AAUs.

On the debit side (left-hand side of the diagram) **PSPAAAAAXXX** as a AAU can be linked to:

**(A)** TIPS DCA

**(B)** TIPS AS Technical Account

**(C)** CMB that is linked to TIPS DCA

**(D)** CMB that is linked to TIPS AS Technical Account

The same situation is on the credit side (right-hand side of the diagram). **PSPBBBBBXXX** as a AAU can be linked to:

**(E)**TIPS DCA

**(F)**TIPS AS Technical Account

**(G)**CMB that is linked to TIPS DCA

**(H)** CMB that is linked to TIPS AS Technical Account

Depending on the account/CMB that each of these BICs is linked to, it seems that we can have 16 options of settlement in TIPS.

I think it is unnecessary to describe all the options presented above.

What seems to be important, though, is to understand what is the main difference when AAU is linked to an account and when it is linked to a CMB.

In short:

- If the AAU is linked to an account that account is simply debited or credited.
- If the AAU is linked to a CMB:
  - the account that the CMB is linked to is debited or credited.
  - additionally, when the settlement occurs, CMB headroom is decreased or increased respectively. For more information about CMBs you can check my previous article: [Credit Memorandum Balance in TIPS](https://www.iso20022payments.com/sct-inst-tips/credit-memorandum-balance-in-tips/).

In other words, when AAU is linked to CMB, apart from posting on the account, the CMB headroom is also adjusted.

To make sure that we have a good understanding, let’s just have a look at three scenarios from the above diagram:

**1\. Scenario**

- **Debtor Agent BIC is linked to TIPS DCA (A)**
- **Creditor Agent BIC is linked to TIPS DCA (E)**

This scenario can be illustrated in the following way:

![](https://www.iso20022payments.com/wp-content/uploads/2024/09/1-scenario.png)

While settling a payment:

**(a)** TIPS debits TIPS DCA to which **PSPAAAAAXXX** is linked to.

**(b)**TIPS credits TIPS DCA to which **PSPBBBBBXXX** is linked to.

**2\. Scenario**

- **Debtor Agent BIC is linked to TIPS DCA (A)**
- **Creditor Agent BIC is linked to TIPS AS Technical Account (F)**

This scenario can be illustrated in the following way:

![](https://www.iso20022payments.com/wp-content/uploads/2024/09/2-scenario.png)

While settling a payment:

**(a)**TIPS debits TIPS DCA to which **PSPAAAAAXXX** is linked to

**(b)**TIPS credits TIPS AS Technical Account to which **PSPBBBBBXXX** is linked to

**3\. Scenario**

- **Debtor Agent BIC is linked to CMB linked to TIPS DCA (C)**
- **Creditor Agent BIC is linked to CMB linked to TIPS AS Technical Account (H)**

This scenario be illustrated in the following way:

![](https://www.iso20022payments.com/wp-content/uploads/2024/09/Scenario-3.png)

While settling a payment:

**(a)** TIPS debits TIPS DCA to which CMB is linked to

**(b)** TIPS decreases the CMB headroom to which **PSPAAAAAXXX** is linked to

**(c)**TIPS credits TIPS AS Technical Account to which CMB is linked to

**(d)** TIPS increases the CMB headroom to which **PSPBBBBBXXX** is linked to

I hope that the above information will allow us to see the settlement logic in every of the possible scenarios.

At the end of this article, I would like to touch upon another issue, which is the possibilities that PSPs have when deciding how to settle payments in TIPS.

It seems that our findings from this article can also shed some light on this subject.

We have to remember that in the context of measures set by ECB’s Governing Council in 2020 ( [here](https://www.ecb.europa.eu/press/intro/news/html/ecb.mipnews200724.en.html)) PSPs have two possibilities:

- become a TIPS Participant with its own TIPS DCA, or
- become a Reachable Party and settle payments via TIPS DCA of another TIPS Participant

These two options, however, do not cover all the options.

In addition to being reachable via TIPS DCA, a PSP can decide to also settle via TIPS AS Technical Account. It is important to remember that, when a PSP wants to settle both via TIPS DCA and via TIPS AS Technical Account, it will need to use a different BIC11 for each option. This is because every TIPS Party and every AAU must be identified with a unique BIC11.

Then, depending on the BIC used in Instant payment either TIPS DCA or TIPS AS Technical Account will be used for settlement.

This brings us to the end of this article.

|     |     |
| --- | --- |
| [<< Credit Memorandum Balance in TIPS](https://www.iso20022payments.com/sct-inst-tips/credit-memorandum-balance-in-tips/) | [Instant Payment between two TIPS participants >>](https://www.iso20022payments.com/sct-inst-tips/instant-payment-between-two-tips-participants/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme