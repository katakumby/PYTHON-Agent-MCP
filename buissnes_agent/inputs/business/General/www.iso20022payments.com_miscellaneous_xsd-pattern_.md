---
url: "https://www.iso20022payments.com/miscellaneous/xsd-pattern/"
title: "XSD pattern – ISO 20022 payments"
---

[Skip to content](https://www.iso20022payments.com/miscellaneous/xsd-pattern/#content)

### [ISO 20022 payments](https://www.iso20022payments.com/)

## Miscellaneous

## XSD pattern

In this article I would like to write a few words about XSD pattern. It will not be a comprehensive, technical article about it. I would rather focus on the practical interpretation of the information we can encounter during our work with XML documents.

What is XSD pattern and where can we deal with it?

If we open for example pacs.009 CBPR+ Usage Guideline in MyStandards, we can see the following information about BICFI as an Agent identifier:

![XSD pattern](https://iso20022payments.com/wp-content/uploads/2023/01/XSD-pattern.jpg)

When we export the pacs.009 XSD from MyStandards we can see the same information there:

![XSD pattern in XSD](https://iso20022payments.com/wp-content/uploads/2023/01/XSD-pattern-in-XSD.jpg)

Let’s try to understand what this means.

XSD pattern constraint is used to limit the content of an XML element and to define a series of numbers or letters that can be used.

In the square brackets there is information about characters that may be used. Let’s have a look at some examples:

**\[xyz\]** means that ONE of the listed letters has to be used: x, y or z.

**\[a-z\]** means that ONE of the LOWERCASE letters from a to z has to be used

**\[a-zA-Z\]\[a-zA-Z\]\[a-zA-Z\]** means that THREE of the LOWERCASE OR UPPERCASE letters from a to z have to be used.

**\[0-9\]\[0-9\]\[0-9\]** means that THREE digits have to be used, and each digit must be in a range from 0 to 9.

But what if we have a lot of characters with the same restriction? Let’s say we have min 4 up to 8 characters and each of them should be either LOWERCASE or UPPERCASE letters from a to z or a digit from 0 to 9.

We will write it like that:

**\[a-zA-Z0-9\]{4,8}**

**\[a-zA-Z0-9\]**– determines what are possible characters

**{4,8}** –  curly brackets allow determining how many characters must be used. The first letter describes the **minimum number** of characters and the second one the **maximum number**. The exact 8 characters would be {8,8}.

Here is an example combining what we have learned so far:

**\[A-Z\]{6,6}(\[0-9\]{3,3}){0,1}**

To easily analyze it, let’s break it down into smaller pieces:

**\[A-Z\]{6,6}** – this means that exactly six capital letters must be used

**(\[0-9\]{3,3}){0,1}** – this is more tricky. It forms one expression. Let’s have a look at it from the end. We can see that the minimum occurrence for this expression is 0 and the maximum is 1 – **{0,1}**. Because the minimum is 0, this second part of the expression is optional. However, if this second part is to be filled, there are restrictions provided in round brackets **(\[0-9\]{3,3})**. This means that exactly 3 digits \[0-9\] have to be used.

So, with this pattern **\[A-Z\]{6,6}(\[0-9\]{3,3}){0,1}** the following exemplary values will comply:

- ABCDEF
- CDEBGT111

To conclude let’s have a look at the BICFI pattern that we saw at the beginning:

**\[A-Z0-9\]{4,4}\[A-Z\]{2,2}\[A-Z0-9\]{2,2}(\[A-Z0-9\]{3,3}){0,1}**

We can break it down into the following parts:

**\[A-Z0-9\]{4,4}** – exactly 4 characters of UPPERCASE letters from A to Z or digits from 0 to 9

**\[A-Z\]{2,2}** – exactly 2 characters of UPPERCASE letters from A to Z

**\[A-Z0-9\]{2,2}** – exactly 2 characters of UPPERCASE letters from A to Z or digits from 0 to 9

**(\[A-Z0-9\]{3,3}){0,1}**– optionally, exactly 3 characters of UPPERCASE letters from A to Z or digits from 0 to 9

|     |     |
| --- | --- |
| [<< Miscellaneous](https://iso20022payments.com/miscellaneous/) | [Currency and Amount >>](https://www.iso20022payments.com/miscellaneous/currency-and-amount/) |

### [ISO 20022 PAYMENTS](https://iso20022payments.com/?customize_changeset_uuid=614f2986-6599-4c3a-809b-286cbe33ab94&customize_messenger_channel=preview-0)

WordPress [Di Blog](https://dithemes.com/di-blog-free-wordpress-theme/) Theme