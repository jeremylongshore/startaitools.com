<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e378b47e0361b7a9b0dab7a0306878c8",
  "translation_date": "2025-08-26T20:00:36+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/README.md",
  "language_code": "bn"
}
-->
# MCP stdio সার্ভার সমাধানসমূহ

> **⚠️ গুরুত্বপূর্ণ**: এই সমাধানগুলো **stdio transport** ব্যবহার করার জন্য আপডেট করা হয়েছে, যা MCP স্পেসিফিকেশন ২০২৫-০৬-১৮ অনুযায়ী সুপারিশকৃত। পূর্বের SSE (Server-Sent Events) transport এখন আর ব্যবহারযোগ্য নয়।

এখানে প্রতিটি রানটাইমে stdio transport ব্যবহার করে MCP সার্ভার তৈরির সম্পূর্ণ সমাধান দেওয়া হয়েছে:

- [TypeScript](../../../../../03-GettingStarted/05-stdio-server/solution/typescript) - সম্পূর্ণ stdio সার্ভার ইমপ্লিমেন্টেশন
- [Python](../../../../../03-GettingStarted/05-stdio-server/solution/python) - asyncio সহ Python stdio সার্ভার
- [.NET](../../../../../03-GettingStarted/05-stdio-server/solution/dotnet) - ডিপেনডেন্সি ইনজেকশন সহ .NET stdio সার্ভার

প্রতিটি সমাধান প্রদর্শন করে:
- stdio transport সেটআপ করা
- সার্ভার টুল সংজ্ঞায়িত করা
- সঠিক JSON-RPC মেসেজ হ্যান্ডলিং
- Claude-এর মতো MCP ক্লায়েন্টের সাথে ইন্টিগ্রেশন

সমস্ত সমাধান বর্তমান MCP স্পেসিফিকেশন অনুসরণ করে এবং সর্বোত্তম পারফরম্যান্স ও নিরাপত্তার জন্য সুপারিশকৃত stdio transport ব্যবহার করে।

---

**অস্বীকৃতি**:  
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনুবাদ করা হয়েছে। আমরা যথাসম্ভব সঠিকতার জন্য চেষ্টা করি, তবে অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল ভাষায় থাকা নথিটিকে প্রামাণিক উৎস হিসেবে বিবেচনা করা উচিত। গুরুত্বপূর্ণ তথ্যের জন্য, পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদ ব্যবহারের ফলে কোনো ভুল বোঝাবুঝি বা ভুল ব্যাখ্যা হলে আমরা দায়ী থাকব না।