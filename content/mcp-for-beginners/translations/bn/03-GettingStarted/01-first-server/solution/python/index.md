<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "d4c162484df410632550a4a357d40341",
  "translation_date": "2025-09-03T16:02:46+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/python/README.md",
  "language_code": "bn"
}
-->
# এই নমুনাটি চালানো

আপনাকে `uv` ইনস্টল করার পরামর্শ দেওয়া হচ্ছে, তবে এটি বাধ্যতামূলক নয়। বিস্তারিত দেখুন [নির্দেশনা](https://docs.astral.sh/uv/#highlights)

## -0- একটি ভার্চুয়াল পরিবেশ তৈরি করুন

```bash
python -m venv venv
```

## -1- ভার্চুয়াল পরিবেশ সক্রিয় করুন

```bash
venv\Scripts\activate
```

## -2- নির্ভরশীলতাগুলি ইনস্টল করুন

```bash
pip install "mcp[cli]"
```

## -3- নমুনাটি চালান

```bash
mcp run server.py
```

## -4- নমুনাটি পরীক্ষা করুন

একটি টার্মিনালে সার্ভার চালু রেখে, অন্য একটি টার্মিনাল খুলুন এবং নিচের কমান্ডটি চালান:

```bash
mcp dev server.py
```

এটি একটি ওয়েব সার্ভার চালু করবে যেখানে একটি ভিজ্যুয়াল ইন্টারফেস থাকবে যা আপনাকে নমুনাটি পরীক্ষা করতে দেবে।

সার্ভার সংযুক্ত হওয়ার পর: 

- টুলগুলির তালিকা দেখুন এবং `add` চালান, যেখানে আর্গুমেন্ট হবে ২ এবং ৪। আপনি ফলাফলে ৬ দেখতে পাবেন।

- রিসোর্স এবং রিসোর্স টেমপ্লেটে যান এবং `get_greeting` কল করুন। একটি নাম টাইপ করুন এবং আপনি প্রদত্ত নাম সহ একটি অভিবাদন দেখতে পাবেন।

### CLI মোডে পরীক্ষা করা

আপনি যে ইন্সপেক্টর চালিয়েছেন তা আসলে একটি Node.js অ্যাপ এবং `mcp dev` এটি চালানোর একটি র‍্যাপার। 

আপনি এটি সরাসরি CLI মোডে চালু করতে পারেন নিচের কমান্ডটি চালিয়ে:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/list
```

এটি সার্ভারে উপলব্ধ সমস্ত টুলের তালিকা দেখাবে। আপনি নিম্নলিখিত আউটপুট দেখতে পাবেন:

```text
{
  "tools": [
    {
      "name": "add",
      "description": "Add two numbers",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "title": "A",
            "type": "integer"
          },
          "b": {
            "title": "B",
            "type": "integer"
          }
        },
        "required": [
          "a",
          "b"
        ],
        "title": "addArguments"
      }
    }
  ]
}
```

কোনো টুল চালানোর জন্য টাইপ করুন:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/call --tool-name add --tool-arg a=1 --tool-arg b=2
```

আপনি নিম্নলিখিত আউটপুট দেখতে পাবেন:

```text
{
  "content": [
    {
      "type": "text",
      "text": "3"
    }
  ],
  "isError": false
}
```

> [!TIP]
> ব্রাউজারে ইন্সপেক্টর চালানোর চেয়ে CLI মোডে চালানো সাধারণত অনেক দ্রুত হয়।
> ইন্সপেক্টর সম্পর্কে আরও পড়ুন [এখানে](https://github.com/modelcontextprotocol/inspector)।

---

**অস্বীকৃতি**:  
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনুবাদ করা হয়েছে। আমরা যথাসাধ্য সঠিকতা নিশ্চিত করার চেষ্টা করি, তবে অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল ভাষায় থাকা নথিটিকে প্রামাণিক উৎস হিসেবে বিবেচনা করা উচিত। গুরুত্বপূর্ণ তথ্যের জন্য, পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদ ব্যবহারের ফলে কোনো ভুল বোঝাবুঝি বা ভুল ব্যাখ্যা হলে আমরা দায়বদ্ধ থাকব না।