---
url: "https://www.iso20022payments.com/miscellaneous/currency-and-amount/"
title: "Currency and Amount – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/miscellaneous/currency-and-amount/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## Miscellaneous

## Currency and Amount

In all payments, it is vital to define what is the amount of the payment. But the amount alone is not enough. It has to be accompanied by currency.

Especially in cross-border payments when we populate the amount in the payment message it is crucial to indicate in which currency this amount is expressed.

Let’s investigate how this information is depicted in ISO 20022.

Below there is an example of the CBPR+ User Guidelines presentation of the Interbank Settlement Amount in pacs.009.

![Interbank Settlement Amount](https://www.iso20022payments.com/wp-content/uploads/2023/01/Interbank-Settlement-Amount.jpg)

**(1)** When we look at the above screenshot we can see that the Currency is added as an attribute to the Interbank Settlement Amount element. This is stated explicitly in the second row: Xml **Attribute** Currency. In the Interbank Settlement Amountelement, there is also an indication of the two Algorithms applied.

We will get to them soon.

**(2)** On the right there is a description of “Type” that Interbank Settlement Amount has been assigned. This tells us that the Amount can have up to 14 digits with up to 5 fractionDigits. The decimal separator is a dot. So, according to this definition, the Amount of 21.1234 of any currency should be valid. Right?

Well, this is indeed valid when it comes only to this definition. However, this is not the only requirement that we have to take into account.

When we move down from the Interbank Settlement Amount and click on Xml Attribute Currency we see the following description:

![Xml Attribute Currency](https://www.iso20022payments.com/wp-content/uploads/2023/01/Xml-Attribute-Currency.jpg)

In the above picture, we see another restriction related to the ActiveCurrencyCode pattern. From this, we know that Currency Code must have exactly 3 Upper Case letters from A to Z. I described how to understand this part in [XSD pattern](https://iso20022payments.com/miscellaneous/xsd-pattern/) section.

But we are only in the middle of our journey.

When we go one step down further to Algorithm: ActiveCurrency we notice that the currency code has to be active and registered with ISO 4217.

![ActiveCurrency](https://www.iso20022payments.com/wp-content/uploads/2023/01/ActiveCurrency.jpg)

And there is one additional row in the Usage Guidelines, which we cannot omit.

Algorithm: CurrencyAmount reveals the following crucial information:

![CurrencyAmount](https://www.iso20022payments.com/wp-content/uploads/2023/01/CurrencyAmount.jpg)

Here the requirement says that not only the Currency Code has to comply with ISO 4217 but also the number of fractional digits must comply with ISO 4217.

So, what is ISO 4217? This is a standard that establishes internationally recognized codes for the representation of currencies. It also defines the maximum number of digits allowed after the decimal separator for a currency. You can get more information here: [ISO 4217 Currency codes.](https://www.iso.org/iso-4217-currency-codes.html)

**What is important to emphasize here it that the reference to ISO 4217 is not only included in the CBPR+ Usage Guidelines, but it is an international standard that should be followed. In the context of this article, I checked the TARGET Services Usage Guidelines and they also comply with ISO 4217.**

Let’s see how it works in practice.

If we take the exemplary amount that we provided at the beginning of this article which is 21.1234 and use it with CLF (currency in Chile) everything will be fine:

![CLF 4](https://www.iso20022payments.com/wp-content/uploads/2023/01/CLF-4-1024x434.jpg)

The above diagram shows how the Currency attribute is populated in the Interbank Settlement Amount element.

The CLF 21.1234 works fine as ISO 4217 allows CLF to have 4 decimal digits.

However, if we take the same amount expressed in USD and test it in the CBPR+ Readiness Portal we will get the error:

![USD 4](https://www.iso20022payments.com/wp-content/uploads/2023/01/USD-4-1024x196.jpg)

So what should we do, when the payment is in USD?

We have to express it in amount with a max of 2 decimal digits.

This is because ISO 4217 defines the maximum number of digits after the decimal separator for USD as 2.

As we can see below the amount of USD 21.12 (2 digits after the decimal separator) works fine:

![USD 2](https://www.iso20022payments.com/wp-content/uploads/2023/01/USD-2-1024x59.jpg)

But, are we always safe with two decimal digits?

Let’s take a look at what happens if we use the same amount for Yen:

![JPY 2](https://www.iso20022payments.com/wp-content/uploads/2023/01/JPY-2-1024x179.jpg)

If we use the same amount that was used for USD we got an error. In fact, Yen is not allowed to have any decimal digits.

It works fine only if we use whole numbers:

![JPY 0](https://www.iso20022payments.com/wp-content/uploads/2023/01/JPY-0-1024x56.jpg)

So, if you have any doubts you should always check ISO 4217 documentation.

In this article I used pacs.009 Interbank Settlement Amount as an example, but the same situation refers to other elements in CBPR+ Usage Guidelines in which we have to specify the Amount and Currency. And as I mentioned earlier it is not a CBPR+ characteristic, but an international standard.

|     |     |
| --- | --- |
| [<< XSD pattern](https://iso20022payments.com/miscellaneous/xsd-pattern/) | [UTC offset >>](https://www.iso20022payments.com/miscellaneous/utc-offset/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme