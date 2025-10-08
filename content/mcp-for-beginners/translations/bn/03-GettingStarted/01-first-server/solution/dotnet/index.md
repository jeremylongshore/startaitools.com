<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "92af35e8c34923031f3d228dffad9ebb",
  "translation_date": "2025-09-03T16:03:08+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/dotnet/README.md",
  "language_code": "bn"
}
-->
# এই নমুনা চালানো

## -1- নির্ভরশীলতাগুলি ইনস্টল করুন

```bash
dotnet restore
```

## -3- নমুনাটি চালান

```bash
dotnet run
```

## -4- নমুনাটি পরীক্ষা করুন

একটি টার্মিনালে সার্ভার চালু রেখে, আরেকটি টার্মিনাল খুলুন এবং নিচের কমান্ডটি চালান:

```bash
npx @modelcontextprotocol/inspector dotnet run
```

এটি একটি ভিজ্যুয়াল ইন্টারফেস সহ একটি ওয়েব সার্ভার চালু করবে, যা আপনাকে নমুনাটি পরীক্ষা করার সুযোগ দেবে।

সার্ভার সংযুক্ত হওয়ার পর: 

- টুলগুলির তালিকা দেখুন এবং `add` চালান, আর্গুমেন্ট হিসেবে 2 এবং 4 দিন, ফলাফলে 6 দেখতে পাবেন।
- রিসোর্স এবং রিসোর্স টেমপ্লেটে যান এবং "greeting" কল করুন, একটি নাম টাইপ করুন এবং আপনি যে নামটি দিয়েছেন তার সাথে একটি শুভেচ্ছা বার্তা দেখতে পাবেন।

### CLI মোডে পরীক্ষা করা

আপনি সরাসরি CLI মোডে এটি চালু করতে পারেন নিচের কমান্ডটি চালিয়ে:

```bash
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/list
```

এটি সার্ভারে উপলব্ধ সমস্ত টুলের তালিকা দেখাবে। আপনি নিচের আউটপুটটি দেখতে পাবেন:

```text
{
  "tools": [
    {
      "name": "Add",
      "description": "Adds two numbers",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "type": "integer"
          },
          "b": {
            "type": "integer"
          }
        },
        "title": "Add",
        "description": "Adds two numbers",
        "required": [
          "a",
          "b"
        ]
      }
    }
  ]
}
```

কোনো টুল চালানোর জন্য টাইপ করুন:

```bash
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/call --tool-name Add --tool-arg a=1 --tool-arg b=2
```

আপনি নিচের আউটপুটটি দেখতে পাবেন:

```text
{
  "content": [
    {
      "type": "text",
      "text": "Sum 3"
    }
  ],
  "isError": false
}
```

> [!TIP]
> সাধারণত ব্রাউজারের তুলনায় CLI মোডে ইনস্পেক্টর চালানো অনেক দ্রুত হয়।
> ইনস্পেক্টর সম্পর্কে আরও পড়ুন [এখানে](https://github.com/modelcontextprotocol/inspector)।

---

**অস্বীকৃতি**:  
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনুবাদ করা হয়েছে। আমরা যথাসম্ভব সঠিক অনুবাদের চেষ্টা করি, তবে অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। নথিটির মূল ভাষায় থাকা সংস্করণটিকেই প্রামাণিক উৎস হিসেবে বিবেচনা করা উচিত। গুরুত্বপূর্ণ তথ্যের জন্য, পেশাদার মানব অনুবাদ ব্যবহার করার পরামর্শ দেওয়া হয়। এই অনুবাদ ব্যবহারের ফলে সৃষ্ট কোনো ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়ী নই।