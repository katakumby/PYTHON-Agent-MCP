---
url: "https://www.iso20022payments.com/miscellaneous/utc-offset/"
title: "UTC offset – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/miscellaneous/utc-offset/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## Miscellaneous

## UTC offset

This article will be a brief one.

I am going to write a few words about the format of **CBPR+ DateTime** element.

In the CBPR+ UHB we can see that in DateTime elements time has to be represented as an **offset against UTC**.

How to understand this?

First of all. What is UTC?

**UTC** stands for **Universal Time Coordinated** which defines the time at zero degrees longitude.

It is used as a global time standard to regulate time and time zones.

And what is a UTC offset?

A **UTC offset** is the **difference in hours and minutes between a particular time zone and UTC**.

You may think of the local time of a country as a deviation from UTC.

Let’s get back to the CBPR+ requirements in this regard.

The structure of DateTime element is as follows:

**YYYY-MM-DDThh:mm:ss.sss+/-hh:mm**

We can distinguish here two parts:

**YYYY-MM-DDThh:mm:ss**.sss – this is local time. At the end we see milliseconds. They are however optional.

**+/-hh:mm**  – this is UTC offset

CBPR+ UHB gives the following example of DateTime element:

**2002-10-10T12:00:00-05:00**

This is based on the example provided in the XML Schema documentation:  [https://www.w3.org/TR/xmlschema-2/#dateTime](https://www.w3.org/TR/xmlschema-2/#dateTime)

Let’s have a closer look:

**2002-10-10T12:00:00** – first part indicates noon on 10 October 2002

**-05:00**   –  this shows a UTC offset.

Such offset is valid for example for Washington DC (USA).

We can see that that time difference is 5 hours.

But, how to understand „**–**“ sign?

This sign does not mean that to calculate the UTC you should subtract 5 hours from the local time in Washington DC.

In fact, on the contrary, it means that 5 hours were subtracted from UTC to get the noon in Washington DC.

**UTC in this example is 17:00 but in Washington DC is noon.**

In other words, a negative offset „**–**“ indicates that the time zone is west of UTC.

Let’s have a look at another example.

On the same day, also at noon, somebody in Kigali (Rwanda) wants to populate the DateTime according to the same requirements. It would look like that:

**2002-10-10T12:00:00+02:00**

**2002-10-10T12:00:00 –** the first part is the same as in the previous example. This is because from the local perspective in Washinton DC as well as in Kigali it is noon on the 10 October 2002.

However, this time the UTC offset is positive:

**+02:00 –**a positive offset indicates that the timezone is east of UTC.

UTC will be at this moment: 10:00. So two hours were added to UTC to get noon in Kigali.

This can be presented visually on the map in the following way:

![](https://www.iso20022payments.com/wp-content/uploads/2023/01/UTC-offset.jpg)

So, today is **20th January 2023**. I’m in Poland. The current local time is **18:09:24**.

How should I write DateTime according to the CBPR+ requirements?

It should be like that:

**2023-01-23T18:09:24+01:00**

Poland is to the east of UTC so I use positive offset.

Currently, UTC is 17:09:24. So I have to add one hour to get my local time.

Just a quick remark at the end. If I were to write these words in May, I will have to use offset +02:00, instead of +01:00. This is because currently in Poland we have CET (Central European Time) which has a UTC offset of +01:00 and in May we are going to use CEST (Central European Summer Time) which has a UTC offset of +02:00.

You will spot the above-presented structure across all CBPR+ messages.

Only in pain.001 and pain.002 there is a possibility to populate Date and Time in another way.

|     |     |
| --- | --- |
| [<< Currency and Amount](https://www.iso20022payments.com/miscellaneous/currency-and-amount/) | [Payments Market Practice Group >>](https://www.iso20022payments.com/miscellaneous/payments-market-practice-group/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme