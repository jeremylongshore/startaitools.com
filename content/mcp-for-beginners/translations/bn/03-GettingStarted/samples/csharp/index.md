<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "882aae00f1d3f007e20d03b883f44afa",
  "translation_date": "2025-07-13T22:14:45+00:00",
  "source_file": "03-GettingStarted/samples/csharp/README.md",
  "language_code": "bn"
}
-->
# Basic Calculator MCP Service

এই সার্ভিসটি Model Context Protocol (MCP) এর মাধ্যমে বেসিক ক্যালকুলেটর অপারেশন প্রদান করে। এটি MCP ইমপ্লিমেন্টেশন শেখার জন্য নতুনদের জন্য একটি সহজ উদাহরণ হিসেবে ডিজাইন করা হয়েছে।

আরও তথ্যের জন্য দেখুন [C# SDK](https://github.com/modelcontextprotocol/csharp-sdk)

## বৈশিষ্ট্যসমূহ

এই ক্যালকুলেটর সার্ভিস নিম্নলিখিত ক্ষমতাগুলো প্রদান করে:

1. **বেসিক আরিথমেটিক অপারেশন**:
   - দুইটি সংখ্যার যোগফল
   - এক সংখ্যাকে অন্য সংখ্যার থেকে বিয়োগ
   - দুইটি সংখ্যার গুণফল
   - এক সংখ্যাকে অন্য সংখ্যার দ্বারা ভাগ (শূন্য ভাগ করার চেক সহ)

## `stdio` টাইপ ব্যবহার

## কনফিগারেশন

1. **MCP সার্ভার কনফিগার করুন**:
   - VS Code-এ আপনার ওয়ার্কস্পেস খুলুন।
   - আপনার ওয়ার্কস্পেস ফোল্ডারে `.vscode/mcp.json` ফাইল তৈরি করুন MCP সার্ভার কনফিগার করার জন্য। উদাহরণ কনফিগারেশন:

     ```jsonc
     {
       "inputs": [
         {
           "type": "promptString",
           "id": "repository-root",
           "description": "The absolute path to the repository root"
         }
       ],
       "servers": {
         "calculator-mcp-dotnet": {
           "type": "stdio",
           "command": "dotnet",
           "args": [
             "run",
             "--project",
             "${input:repository-root}/03-GettingStarted/samples/csharp/src/calculator.csproj"
           ]
         }
       }
     }
     ```

   - আপনাকে GitHub রিপোজিটরি রুট প্রবেশ করতে বলা হবে, যা কমান্ড `git rev-parse --show-toplevel` থেকে পাওয়া যাবে।

## সার্ভিস ব্যবহার

সার্ভিসটি MCP প্রোটোকলের মাধ্যমে নিম্নলিখিত API এন্ডপয়েন্টগুলো প্রকাশ করে:

- `add(a, b)`: দুইটি সংখ্যা যোগ করুন
- `subtract(a, b)`: দ্বিতীয় সংখ্যাটি প্রথম থেকে বিয়োগ করুন
- `multiply(a, b)`: দুইটি সংখ্যা গুণ করুন
- `divide(a, b)`: প্রথম সংখ্যাটি দ্বিতীয় দ্বারা ভাগ করুন (শূন্য চেক সহ)
- isPrime(n): একটি সংখ্যা মৌলিক কিনা পরীক্ষা করুন

## VS Code-এ Github Copilot Chat দিয়ে পরীক্ষা করুন

1. MCP প্রোটোকল ব্যবহার করে সার্ভিসে রিকোয়েস্ট পাঠানোর চেষ্টা করুন। উদাহরণস্বরূপ, আপনি বলতে পারেন:
   - "Add 5 and 3"
   - "Subtract 10 from 4"
   - "Multiply 6 and 7"
   - "Divide 8 by 2"
   - "Does 37854 prime?"
   - "What are the 3 prime numbers before after 4242?"
2. নিশ্চিত হতে যে এটি টুলস ব্যবহার করছে, প্রম্পটে #MyCalculator যোগ করুন। উদাহরণস্বরূপ:
   - "Add 5 and 3 #MyCalculator"
   - "Subtract 10 from 4 #MyCalculator"

## কন্টেইনারাইজড ভার্সন

আগের সমাধানটি খুব ভালো যখন আপনার কাছে .NET SDK ইনস্টল করা থাকে এবং সব ডিপেন্ডেন্সি ঠিকঠাক থাকে। তবে, যদি আপনি সমাধানটি শেয়ার করতে চান বা অন্য পরিবেশে চালাতে চান, তাহলে আপনি কন্টেইনারাইজড ভার্সন ব্যবহার করতে পারেন।

1. Docker চালু করুন এবং নিশ্চিত করুন এটি চলছে।
1. একটি টার্মিনাল থেকে `03-GettingStarted\samples\csharp\src` ফোল্ডারে যান
1. ক্যালকুলেটর সার্ভিসের জন্য Docker ইমেজ তৈরি করতে নিচের কমান্ডটি চালান (আপনার Docker Hub ইউজারনেম দিয়ে `<YOUR-DOCKER-USERNAME>` প্রতিস্থাপন করুন):
   ```bash
   docker build -t <YOUR-DOCKER-USERNAME>/mcp-calculator .
   ``` 
1. ইমেজ তৈরি হয়ে গেলে, এটিকে Docker Hub-এ আপলোড করুন। নিচের কমান্ডটি চালান:
   ```bash
    docker push <YOUR-DOCKER-USERNAME>/mcp-calculator
  ```

## Dockerized ভার্সন ব্যবহার

1. `.vscode/mcp.json` ফাইলে সার্ভার কনফিগারেশন নিম্নরূপ পরিবর্তন করুন:
   ```json
    "mcp-calc": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "<YOUR-DOCKER-USERNAME>/mcp-calc"
      ],
      "envFile": "",
      "env": {}
    }
   ```
   কনফিগারেশন দেখে বোঝা যায়, কমান্ডটি `docker` এবং আর্গুমেন্টগুলো `run --rm -i <YOUR-DOCKER-USERNAME>/mcp-calc`। `--rm` ফ্ল্যাগটি নিশ্চিত করে যে কন্টেইনার বন্ধ হওয়ার পর মুছে ফেলা হবে, এবং `-i` ফ্ল্যাগটি কন্টেইনারের স্ট্যান্ডার্ড ইনপুটের সাথে ইন্টারঅ্যাক্ট করার সুযোগ দেয়। শেষ আর্গুমেন্টটি হলো সেই ইমেজের নাম যা আমরা তৈরি করে Docker Hub-এ আপলোড করেছি।

## Dockerized ভার্সন পরীক্ষা করুন

`"mcp-calc": {` এর উপরে ছোট Start বাটনে ক্লিক করে MCP সার্ভার শুরু করুন, এবং আগের মতোই ক্যালকুলেটর সার্ভিসকে কিছু গণনা করতে বলুন।

**অস্বীকৃতি**:  
এই নথিটি AI অনুবাদ সেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। আমরা যথাসাধ্য সঠিকতার চেষ্টা করি, তবে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল নথিটি তার নিজস্ব ভাষায়ই কর্তৃত্বপূর্ণ উৎস হিসেবে বিবেচিত হওয়া উচিত। গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানব অনুবাদ গ্রহণ করার পরামর্শ দেওয়া হয়। এই অনুবাদের ব্যবহারে সৃষ্ট কোনো ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়ী নই।