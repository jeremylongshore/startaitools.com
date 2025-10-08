<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "fd28e690667b8ad84bb153cb025cfd73",
  "translation_date": "2025-10-07T01:16:22+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/solution/python/README.md",
  "language_code": "bn"
}
-->
# নমুনা চালান

## পরিবেশ তৈরি করুন

```sh
python -m venv venv
source ./venv/bin/activate
```

## নির্ভরতা ইনস্টল করুন

```sh
pip install "mcp[cli]" dotenv PyJWT requeests
```

## টোকেন তৈরি করুন

আপনাকে একটি টোকেন তৈরি করতে হবে যা ক্লায়েন্ট সার্ভারের সাথে যোগাযোগ করতে ব্যবহার করবে।

কল করুন:

```sh
python util.py
```

## কোড চালান

কোড চালানোর জন্য:

```sh
python server.py
```

একটি আলাদা টার্মিনালে টাইপ করুন:

```sh
python client.py
```

সার্ভার টার্মিনালে, আপনি এরকম কিছু দেখতে পাবেন:

```text
Valid token, proceeding...
User exists, proceeding...
User has required scope, proceeding...
```

ক্লায়েন্ট উইন্ডোতে, আপনি এরকম টেক্সট দেখতে পাবেন:

```text
Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-10-06T17:37:39.847457",\n  "timezone": "UTC",\n  "timestamp": 1759772259.847457,\n  "formatted": "2025-10-06 17:37:39"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-10-06T17:37:39.847457', 'timezone': 'UTC', 'timestamp': 1759772259.847457, 'formatted': '2025-10-06 17:37:39'} isError=False
```

এর মানে সবকিছু ঠিকঠাক কাজ করছে।

### তথ্য পরিবর্তন করুন, এটি ব্যর্থ হতে দেখুন

*server.py* ফাইলের এই কোডটি খুঁজুন:

```python
 if not has_scope(has_header, "Admin.Write"):
```

এটি পরিবর্তন করুন যাতে এটি "User.Write" বলে। আপনার বর্তমান টোকেনের এই অনুমতি স্তর নেই, তাই যদি আপনি সার্ভারটি পুনরায় চালু করেন এবং ক্লায়েন্টটি আবার চালানোর চেষ্টা করেন তবে আপনি সার্ভার টার্মিনালে নিম্নলিখিত ধরনের একটি ত্রুটি দেখতে পাবেন:

```text
Valid token, proceeding...
User exists, proceeding...
-> Missing required scope!
```

আপনি হয় আপনার সার্ভার কোডটি পূর্বাবস্থায় ফিরিয়ে আনতে পারেন অথবা এই অতিরিক্ত স্কোপটি অন্তর্ভুক্ত করে একটি নতুন টোকেন তৈরি করতে পারেন, এটি আপনার উপর নির্ভর করছে।

---

**অস্বীকৃতি**:  
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনুবাদ করা হয়েছে। আমরা যথাসাধ্য সঠিকতা নিশ্চিত করার চেষ্টা করি, তবে অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল ভাষায় থাকা নথিটিকে প্রামাণিক উৎস হিসেবে বিবেচনা করা উচিত। গুরুত্বপূর্ণ তথ্যের জন্য, পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদ ব্যবহারের ফলে কোনো ভুল বোঝাবুঝি বা ভুল ব্যাখ্যা হলে আমরা দায়বদ্ধ থাকব না।