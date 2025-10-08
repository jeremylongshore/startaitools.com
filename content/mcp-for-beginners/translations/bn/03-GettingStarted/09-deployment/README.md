<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1d9dc83260576b76f272d330ed93c51f",
  "translation_date": "2025-07-13T22:07:28+00:00",
  "source_file": "03-GettingStarted/09-deployment/README.md",
  "language_code": "bn"
}
-->
# MCP সার্ভার ডিপ্লয়মেন্ট

আপনার MCP সার্ভার ডিপ্লয় করলে অন্যরা আপনার স্থানীয় পরিবেশের বাইরে এর টুলস এবং রিসোর্স ব্যবহার করতে পারবে। স্কেলেবিলিটি, নির্ভরযোগ্যতা এবং ব্যবস্থাপনার সহজতার উপর নির্ভর করে বিভিন্ন ডিপ্লয়মেন্ট কৌশল বিবেচনা করা যেতে পারে। নিচে MCP সার্ভারগুলো লোকালি, কন্টেইনারে এবং ক্লাউডে ডিপ্লয় করার নির্দেশনা দেওয়া হয়েছে।

## ওভারভিউ

এই পাঠে আপনি শিখবেন কিভাবে আপনার MCP Server অ্যাপ ডিপ্লয় করবেন।

## শেখার উদ্দেশ্য

এই পাঠ শেষ করার পর, আপনি সক্ষম হবেন:

- বিভিন্ন ডিপ্লয়মেন্ট পদ্ধতি মূল্যায়ন করতে।
- আপনার অ্যাপ ডিপ্লয় করতে।

## লোকাল ডেভেলপমেন্ট এবং ডিপ্লয়মেন্ট

যদি আপনার সার্ভার ব্যবহারকারীর মেশিনে রান করার জন্য হয়, তাহলে নিচের ধাপগুলো অনুসরণ করুন:

1. **সার্ভার ডাউনলোড করুন**। যদি আপনি সার্ভারটি না লিখে থাকেন, তাহলে প্রথমে সেটি আপনার মেশিনে ডাউনলোড করুন।  
1. **সার্ভার প্রসেস শুরু করুন**: আপনার MCP সার্ভার অ্যাপ্লিকেশন চালু করুন।

SSE এর জন্য (stdio টাইপ সার্ভারের জন্য প্রয়োজন নেই)

1. **নেটওয়ার্কিং কনফিগার করুন**: নিশ্চিত করুন সার্ভার প্রত্যাশিত পোর্টে অ্যাক্সেসযোগ্য।  
1. **ক্লায়েন্ট সংযোগ করুন**: `http://localhost:3000` এর মতো লোকাল কানেকশন URL ব্যবহার করুন।

## ক্লাউড ডিপ্লয়মেন্ট

MCP সার্ভার বিভিন্ন ক্লাউড প্ল্যাটফর্মে ডিপ্লয় করা যায়:

- **সার্ভারলেস ফাংশনস**: হালকা MCP সার্ভার সার্ভারলেস ফাংশন হিসেবে ডিপ্লয় করুন।  
- **কন্টেইনার সার্ভিসেস**: Azure Container Apps, AWS ECS, বা Google Cloud Run এর মতো সার্ভিস ব্যবহার করুন।  
- **কুবেরনেটিস**: উচ্চ উপলব্ধতার জন্য MCP সার্ভার কুবেরনেটিস ক্লাস্টারে ডিপ্লয় এবং পরিচালনা করুন।

### উদাহরণ: Azure Container Apps

Azure Container Apps MCP সার্ভার ডিপ্লয়মেন্ট সাপোর্ট করে। এটি এখনও উন্নয়নের পর্যায়ে এবং বর্তমানে SSE সার্ভার সাপোর্ট করে।

এটি করার ধাপগুলো:

1. একটি রিপো ক্লোন করুন:

  ```sh
  git clone https://github.com/anthonychu/azure-container-apps-mcp-sample.git
  ```

1. লোকালি রান করে পরীক্ষা করুন:

  ```sh
  uv venv
  uv sync

  # linux/macOS
  export API_KEYS=<AN_API_KEY>
  # windows
  set API_KEYS=<AN_API_KEY>

  uv run fastapi dev main.py
  ```

1. লোকালি চেষ্টা করার জন্য, *.vscode* ডিরেক্টরিতে *mcp.json* ফাইল তৈরি করুন এবং নিচের বিষয়বস্তু যোগ করুন:

  ```json
  {
      "inputs": [
          {
              "type": "promptString",
              "id": "weather-api-key",
              "description": "Weather API Key",
              "password": true
          }
      ],
      "servers": {
          "weather-sse": {
              "type": "sse",
              "url": "http://localhost:8000/sse",
              "headers": {
                  "x-api-key": "${input:weather-api-key}"
              }
          }
      }
  }
  ```

  SSE সার্ভার শুরু হলে, JSON ফাইলে প্লে আইকনে ক্লিক করুন, এখন আপনি GitHub Copilot দ্বারা সার্ভারের টুলস সনাক্ত হতে দেখবেন, টুল আইকন দেখুন।

1. ডিপ্লয় করতে, নিচের কমান্ড রান করুন:

  ```sh
  az containerapp up -g <RESOURCE_GROUP_NAME> -n weather-mcp --environment mcp -l westus --env-vars API_KEYS=<AN_API_KEY> --source .
  ```

এইভাবেই আপনি লোকালি ডিপ্লয় করতে পারেন, অথবা Azure এ এই ধাপগুলো অনুসরণ করে ডিপ্লয় করতে পারেন।

## অতিরিক্ত রিসোর্স

- [Azure Functions + MCP](https://learn.microsoft.com/en-us/samples/azure-samples/remote-mcp-functions-dotnet/remote-mcp-functions-dotnet/)  
- [Azure Container Apps আর্টিকেল](https://techcommunity.microsoft.com/blog/appsonazureblog/host-remote-mcp-servers-in-azure-container-apps/4403550)  
- [Azure Container Apps MCP রিপো](https://github.com/anthonychu/azure-container-apps-mcp-sample)  

## পরবর্তী ধাপ

- পরবর্তী: [প্র্যাকটিক্যাল ইমপ্লিমেন্টেশন](../../04-PracticalImplementation/README.md)

**অস্বীকৃতি**:  
এই নথিটি AI অনুবাদ সেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। আমরা যথাসাধ্য সঠিকতার চেষ্টা করি, তবে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল নথিটি তার নিজস্ব ভাষায়ই কর্তৃত্বপূর্ণ উৎস হিসেবে বিবেচিত হওয়া উচিত। গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানব অনুবাদ গ্রহণ করার পরামর্শ দেওয়া হয়। এই অনুবাদের ব্যবহারে সৃষ্ট কোনো ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়ী নই।