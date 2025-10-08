<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "98bcd044860716da5819e31c152813b7",
  "translation_date": "2025-08-18T15:12:12+00:00",
  "source_file": "03-GettingStarted/07-aitk/README.md",
  "language_code": "bn"
}
-->
# Visual Studio Code-এর AI Toolkit এক্সটেনশন ব্যবহার করে সার্ভার কনজিউম করা

যখন আপনি একটি AI এজেন্ট তৈরি করছেন, তখন এটি শুধুমাত্র স্মার্ট উত্তর তৈরি করার বিষয় নয়; এটি এজেন্টকে কার্যকর পদক্ষেপ নেওয়ার ক্ষমতা দেওয়ার বিষয়ও। এখানেই Model Context Protocol (MCP) গুরুত্বপূর্ণ ভূমিকা পালন করে। MCP এজেন্টদের বাইরের টুল এবং সার্ভিসগুলোতে একটি সঙ্গতিপূর্ণ উপায়ে অ্যাক্সেস করতে সহজ করে তোলে। এটি এমন যেন আপনার এজেন্টকে একটি টুলবক্সে সংযুক্ত করা হচ্ছে যা সে *বাস্তবিকভাবে* ব্যবহার করতে পারে।

ধরুন আপনি আপনার এজেন্টকে একটি ক্যালকুলেটর MCP সার্ভারের সাথে সংযুক্ত করেছেন। হঠাৎ করেই আপনার এজেন্ট গণিতের কাজ করতে পারে, শুধুমাত্র একটি প্রম্পট পাওয়ার মাধ্যমে যেমন “৪৭ গুণ ৮৯ কত?”—কোনো লজিক হার্ডকোড করার বা কাস্টম API তৈরি করার প্রয়োজন নেই।

## ওভারভিউ

এই পাঠে আলোচনা করা হয়েছে কীভাবে Visual Studio Code-এর [AI Toolkit](https://aka.ms/AIToolkit) এক্সটেনশন ব্যবহার করে একটি ক্যালকুলেটর MCP সার্ভারকে একটি এজেন্টের সাথে সংযুক্ত করা যায়, যা এজেন্টকে প্রাকৃতিক ভাষার মাধ্যমে যোগ, বিয়োগ, গুণ এবং ভাগ করার মতো গণিতের কাজ সম্পাদন করতে সক্ষম করে।

AI Toolkit একটি শক্তিশালী এক্সটেনশন যা Visual Studio Code-এ এজেন্ট ডেভেলপমেন্টকে সহজ করে তোলে। AI ইঞ্জিনিয়াররা সহজেই জেনারেটিভ AI মডেল তৈরি এবং পরীক্ষা করতে পারেন—লোকাল বা ক্লাউডে। এই এক্সটেনশনটি আজকের বেশিরভাগ প্রধান জেনারেটিভ মডেলকে সমর্থন করে।

*নোট*: AI Toolkit বর্তমানে Python এবং TypeScript সমর্থন করে।

## শেখার লক্ষ্য

এই পাঠ শেষে, আপনি সক্ষম হবেন:

- AI Toolkit ব্যবহার করে MCP সার্ভার কনজিউম করতে।
- MCP সার্ভার দ্বারা প্রদত্ত টুলগুলো আবিষ্কার এবং ব্যবহার করার জন্য একটি এজেন্ট কনফিগারেশন সেটআপ করতে।
- প্রাকৃতিক ভাষার মাধ্যমে MCP টুল ব্যবহার করতে।

## পদ্ধতি

আমাদের উচ্চ-স্তরে এইভাবে এগোতে হবে:

- একটি এজেন্ট তৈরি করুন এবং তার সিস্টেম প্রম্পট নির্ধারণ করুন।
- ক্যালকুলেটর টুল সহ একটি MCP সার্ভার তৈরি করুন।
- Agent Builder-কে MCP সার্ভারের সাথে সংযুক্ত করুন।
- প্রাকৃতিক ভাষার মাধ্যমে এজেন্টের টুল ব্যবহারের পরীক্ষা করুন।

চমৎকার, এখন আমরা প্রবাহটি বুঝেছি। চলুন MCP-এর মাধ্যমে বাইরের টুল ব্যবহার করার জন্য একটি AI এজেন্ট কনফিগার করি এবং তার ক্ষমতা বাড়াই!

## পূর্বশর্ত

- [Visual Studio Code](https://code.visualstudio.com/)
- [Visual Studio Code-এর AI Toolkit](https://aka.ms/AIToolkit)

## অনুশীলন: সার্ভার কনজিউম করা

> [!WARNING]
> macOS ব্যবহারকারীদের জন্য নোট। আমরা বর্তমানে macOS-এ ডিপেনডেন্সি ইনস্টলেশনকে প্রভাবিত করা একটি সমস্যার তদন্ত করছি। এর ফলে, macOS ব্যবহারকারীরা এই টিউটোরিয়ালটি সম্পন্ন করতে পারবেন না। আমরা যত দ্রুত সম্ভব নির্দেশাবলী আপডেট করব। আপনার ধৈর্য এবং বোঝার জন্য ধন্যবাদ!

এই অনুশীলনে, আপনি Visual Studio Code-এর AI Toolkit ব্যবহার করে MCP সার্ভারের টুল সহ একটি AI এজেন্ট তৈরি, চালানো এবং উন্নত করবেন।

### -0- প্রাক-ধাপ, My Models-এ OpenAI GPT-4o মডেল যোগ করুন

এই অনুশীলনে **GPT-4o** মডেল ব্যবহার করা হয়েছে। এজেন্ট তৈরি করার আগে মডেলটি **My Models**-এ যোগ করা উচিত।

![Visual Studio Code-এর AI Toolkit এক্সটেনশনের মডেল সিলেকশন ইন্টারফেসের স্ক্রিনশট। হেডিংটি "Find the right model for your AI Solution" এবং সাবটাইটেলটি ব্যবহারকারীদের AI মডেল আবিষ্কার, পরীক্ষা এবং ডিপ্লয় করতে উৎসাহিত করে। নিচে, “Popular Models”-এর অধীনে ছয়টি মডেল কার্ড প্রদর্শিত হয়েছে: DeepSeek-R1 (GitHub-hosted), OpenAI GPT-4o, OpenAI GPT-4.1, OpenAI o1, Phi 4 Mini (CPU - Small, Fast), এবং DeepSeek-R1 (Ollama-hosted)। প্রতিটি কার্ডে “Add” বা “Try in Playground” অপশন রয়েছে।](../../../../translated_images/aitk-model-catalog.2acd38953bb9c119aa629fe74ef34cc56e4eed35e7f5acba7cd0a59e614ab335.bn.png)

1. **Activity Bar** থেকে **AI Toolkit** এক্সটেনশন খুলুন।
1. **Catalog** সেকশনে **Models** নির্বাচন করুন, যা **Model Catalog** খুলবে। **Models** নির্বাচন করলে **Model Catalog** একটি নতুন এডিটর ট্যাবে খুলবে।
1. **Model Catalog** সার্চ বারে **OpenAI GPT-4o** লিখুন।
1. **+ Add** ক্লিক করে মডেলটি আপনার **My Models** তালিকায় যোগ করুন। নিশ্চিত করুন যে আপনি **Hosted by GitHub** মডেলটি নির্বাচন করেছেন।
1. **Activity Bar**-এ নিশ্চিত করুন যে **OpenAI GPT-4o** মডেলটি তালিকায় প্রদর্শিত হচ্ছে।

### -1- একটি এজেন্ট তৈরি করুন

**Agent (Prompt) Builder** আপনাকে আপনার নিজস্ব AI-চালিত এজেন্ট তৈরি এবং কাস্টমাইজ করতে সক্ষম করে। এই সেকশনে, আপনি একটি নতুন এজেন্ট তৈরি করবেন এবং কথোপকথন চালানোর জন্য একটি মডেল বরাদ্দ করবেন।

![Visual Studio Code-এর AI Toolkit এক্সটেনশনের "Calculator Agent" বিল্ডার ইন্টারফেসের স্ক্রিনশট। বাম প্যানেলে, নির্বাচিত মডেলটি "OpenAI GPT-4o (via GitHub)"। একটি সিস্টেম প্রম্পট দেখায় "You are a professor in university teaching math," এবং একটি ইউজার প্রম্পট বলে, "Explain to me the Fourier equation in simple terms।" অতিরিক্ত অপশনগুলোর মধ্যে টুল যোগ করার, MCP সার্ভার সক্রিয় করার এবং স্ট্রাকচার্ড আউটপুট নির্বাচন করার বোতাম রয়েছে। নিচে একটি নীল “Run” বোতাম রয়েছে। ডান প্যানেলে, "Get Started with Examples" এর অধীনে তিনটি নমুনা এজেন্ট তালিকাভুক্ত রয়েছে: Web Developer (with MCP Server, Second-Grade Simplifier, এবং Dream Interpreter, প্রতিটির সংক্ষিপ্ত বিবরণ সহ।](../../../../translated_images/aitk-agent-builder.901e3a2960c3e4774b29a23024ff5bec2d4232f57fae2a418b2aaae80f81c05f.bn.png)

1. **Activity Bar** থেকে **AI Toolkit** এক্সটেনশন খুলুন।
1. **Tools** সেকশনে **Agent (Prompt) Builder** নির্বাচন করুন। **Agent (Prompt) Builder** নির্বাচন করলে এটি একটি নতুন এডিটর ট্যাবে খুলবে।
1. **+ New Agent** বোতাম ক্লিক করুন। এক্সটেনশনটি **Command Palette**-এর মাধ্যমে একটি সেটআপ উইজার্ড চালু করবে।
1. **Calculator Agent** নাম লিখুন এবং **Enter** চাপুন।
1. **Agent (Prompt) Builder**-এ, **Model** ফিল্ডে **OpenAI GPT-4o (via GitHub)** মডেলটি নির্বাচন করুন।

### -2- এজেন্টের জন্য একটি সিস্টেম প্রম্পট তৈরি করুন

এজেন্টের কাঠামো তৈরি করার পর, তার ব্যক্তিত্ব এবং উদ্দেশ্য নির্ধারণ করার সময় এসেছে। এই সেকশনে, আপনি **Generate system prompt** ফিচার ব্যবহার করে এজেন্টের উদ্দেশ্য বর্ণনা করবেন—এই ক্ষেত্রে একটি ক্যালকুলেটর এজেন্ট—এবং মডেলকে সিস্টেম প্রম্পট লিখতে বলবেন।

![Visual Studio Code-এর AI Toolkit-এর "Calculator Agent" ইন্টারফেসের স্ক্রিনশট যেখানে একটি মডাল উইন্ডো খোলা রয়েছে যার শিরোনাম "Generate a prompt।" মডালটি ব্যাখ্যা করে যে একটি প্রম্পট টেমপ্লেট তৈরি করা যেতে পারে মৌলিক বিবরণ শেয়ার করে এবং একটি টেক্সট বক্সে নমুনা সিস্টেম প্রম্পট দেখায়: "You are a helpful and efficient math assistant. When given a problem involving basic arithmetic, you respond with the correct result।" টেক্সট বক্সের নিচে "Close" এবং "Generate" বোতাম রয়েছে। ব্যাকগ্রাউন্ডে এজেন্ট কনফিগারেশনের অংশ দৃশ্যমান, যার মধ্যে নির্বাচিত মডেল "OpenAI GPT-4o (via GitHub)" এবং সিস্টেম এবং ইউজার প্রম্পটের জন্য ফিল্ড রয়েছে।](../../../../translated_images/aitk-generate-prompt.ba9e69d3d2bbe2a26444d0c78775540b14196061eee32c2054e9ee68c4f51f3a.bn.png)

1. **Prompts** সেকশনে, **Generate system prompt** বোতাম ক্লিক করুন। এই বোতামটি প্রম্পট বিল্ডার খুলবে যা AI ব্যবহার করে এজেন্টের জন্য একটি সিস্টেম প্রম্পট তৈরি করে।
1. **Generate a prompt** উইন্ডোতে, নিম্নলিখিত লিখুন: `You are a helpful and efficient math assistant. When given a problem involving basic arithmetic, you respond with the correct result।`
1. **Generate** বোতাম ক্লিক করুন। একটি নোটিফিকেশন নিচের ডান কোণে প্রদর্শিত হবে যা নিশ্চিত করবে যে সিস্টেম প্রম্পট তৈরি হচ্ছে। প্রম্পট তৈরি সম্পন্ন হলে, এটি **Agent (Prompt) Builder**-এর **System prompt** ফিল্ডে প্রদর্শিত হবে।
1. **System prompt** পর্যালোচনা করুন এবং প্রয়োজন হলে সংশোধন করুন।

### -3- একটি MCP সার্ভার তৈরি করুন

এখন আপনি এজেন্টের সিস্টেম প্রম্পট নির্ধারণ করেছেন—যা তার আচরণ এবং প্রতিক্রিয়া নির্দেশ করে—এটি এজেন্টকে বাস্তবিক ক্ষমতা দেওয়ার সময়। এই সেকশনে, আপনি একটি ক্যালকুলেটর MCP সার্ভার তৈরি করবেন যা যোগ, বিয়োগ, গুণ এবং ভাগ করার গণিতের কাজ সম্পাদন করতে সক্ষম টুল সরবরাহ করবে। এই সার্ভারটি এজেন্টকে প্রাকৃতিক ভাষার প্রম্পটের প্রতিক্রিয়ায় রিয়েল-টাইম গণিতের কাজ সম্পাদন করতে সক্ষম করবে।

!["Visual Studio Code-এর AI Toolkit এক্সটেনশনের Calculator Agent ইন্টারফেসের নিচের অংশের স্ক্রিনশট। এটি “Tools” এবং “Structure output” এর জন্য এক্সপ্যান্ডেবল মেনু দেখায়, একটি ড্রপডাউন মেনু সহ যার লেবেল “Choose output format” এবং সেট করা হয়েছে “text।” ডানদিকে, একটি বোতাম লেবেল করা হয়েছে “+ MCP Server” একটি Model Context Protocol সার্ভার যোগ করার জন্য। Tools সেকশনের উপরে একটি ইমেজ আইকন প্লেসহোল্ডার দেখানো হয়েছে।](../../../../translated_images/aitk-add-mcp-server.9742cfddfe808353c0caf9cc0a7ed3e80e13abf4d2ebde315c81c3cb02a2a449.bn.png)

AI Toolkit টেমপ্লেট দিয়ে সজ্জিত যা আপনার নিজস্ব MCP সার্ভার তৈরি করা সহজ করে তোলে। আমরা ক্যালকুলেটর MCP সার্ভার তৈরি করতে Python টেমপ্লেট ব্যবহার করব।

*নোট*: AI Toolkit বর্তমানে Python এবং TypeScript সমর্থন করে।

1. **Agent (Prompt) Builder**-এর **Tools** সেকশনে, **+ MCP Server** বোতাম ক্লিক করুন। এক্সটেনশনটি **Command Palette**-এর মাধ্যমে একটি সেটআপ উইজার্ড চালু করবে।
1. **+ Add Server** নির্বাচন করুন।
1. **Create a New MCP Server** নির্বাচন করুন।
1. **python-weather** টেমপ্লেট নির্বাচন করুন।
1. **Default folder** নির্বাচন করুন MCP সার্ভার টেমপ্লেট সংরক্ষণ করতে।
1. সার্ভারের জন্য নিম্নলিখিত নাম লিখুন: **Calculator**
1. একটি নতুন Visual Studio Code উইন্ডো খুলবে। **Yes, I trust the authors** নির্বাচন করুন।
1. **Terminal** ব্যবহার করে একটি ভার্চুয়াল এনভায়রনমেন্ট তৈরি করুন: `python -m venv .venv`
1. **Terminal** ব্যবহার করে ভার্চুয়াল এনভায়রনমেন্ট সক্রিয় করুন:
    1. Windows - `.venv\Scripts\activate`
    1. macOS/Linux - `source .venv/bin/activate`
1. **Terminal** ব্যবহার করে ডিপেনডেন্সি ইনস্টল করুন: `pip install -e .[dev]`
1. **Activity Bar**-এর **Explorer** ভিউতে **src** ডিরেক্টরি এক্সপ্যান্ড করুন এবং **server.py** নির্বাচন করুন ফাইলটি এডিটরে খুলতে।
1. **server.py** ফাইলের কোড নিম্নলিখিত দিয়ে প্রতিস্থাপন করুন এবং সংরক্ষণ করুন:

    ```python
    """
    Sample MCP Calculator Server implementation in Python.

    
    This module demonstrates how to create a simple MCP server with calculator tools
    that can perform basic arithmetic operations (add, subtract, multiply, divide).
    """
    
    from mcp.server.fastmcp import FastMCP
    
    server = FastMCP("calculator")
    
    @server.tool()
    def add(a: float, b: float) -> float:
        """Add two numbers together and return the result."""
        return a + b
    
    @server.tool()
    def subtract(a: float, b: float) -> float:
        """Subtract b from a and return the result."""
        return a - b
    
    @server.tool()
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers together and return the result."""
        return a * b
    
    @server.tool()
    def divide(a: float, b: float) -> float:
        """
        Divide a by b and return the result.
        
        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    ```

### -4- ক্যালকুলেটর MCP সার্ভার সহ এজেন্ট চালান

এখন আপনার এজেন্টের টুল রয়েছে, এটি ব্যবহার করার সময়! এই সেকশনে, আপনি এজেন্টে প্রম্পট জমা দেবেন এবং যাচাই করবেন যে এজেন্ট ক্যালকুলেটর MCP সার্ভার থেকে সঠিক টুল ব্যবহার করছে কিনা।

![Visual Studio Code-এর AI Toolkit এক্সটেনশনের Calculator Agent ইন্টারফেসের স্ক্রিনশট। বাম প্যানেলে, “Tools” এর অধীনে একটি MCP সার্ভার যোগ করা হয়েছে যার নাম local-server-calculator_server, যেখানে চারটি উপলব্ধ টুল দেখানো হয়েছে: add, subtract, multiply, এবং divide। একটি ব্যাজ দেখায় যে চারটি টুল সক্রিয়। নিচে একটি নীল “Run” বোতাম রয়েছে। ডান প্যানেলে, “Model Response” এর অধীনে, এজেন্ট multiply এবং subtract টুল invoke করে ইনপুট {"a": 3, "b": 25} এবং {"a": 75, "b": 20} সহ। চূড়ান্ত “Tool Response” 75.0 হিসাবে দেখানো হয়েছে। নিচে একটি “View Code” বোতাম রয়েছে।](../../../../translated_images/aitk-agent-response-with-tools.e7c781869dc8041a25f9903ed4f7e8e0c7e13d7d94f6786a6c51b1e172f56866.bn.png)

আপনি আপনার লোকাল ডেভ মেশিনে **Agent Builder** ব্যবহার করে ক্যালকুলেটর MCP সার্ভার চালাবেন MCP ক্লায়েন্ট হিসেবে।

1. MCP সার্ভার ডিবাগিং শুরু করতে `F5` চাপুন। **Agent (Prompt) Builder** একটি নতুন এডিটর ট্যাবে খুলবে। সার্ভারের স্ট্যাটাস টার্মিনালে দৃশ্যমান।
1. **Agent (Prompt) Builder**-এর **User prompt** ফিল্ডে নিম্নলিখিত প্রম্পট লিখুন: `I bought 3 items priced at $25 each, and then used a $20 discount. How much did I pay?`
1. **Run** বোতাম ক্লিক করুন এজেন্টের প্রতিক্রিয়া তৈরি করতে।
1. এজেন্টের আউটপুট পর্যালোচনা করুন। মডেলটি সিদ্ধান্তে পৌঁছানো উচিত যে আপনি **$55** পরিশোধ করেছেন।
1. এখানে কী ঘটবে তার একটি বিশ্লেষণ:
    - এজেন্ট **multiply** এবং **subtract** টুল নির্বাচন করে গণনার জন্য।
    - **multiply** টুলের জন্য যথাযথ `a` এবং `b` মান বরাদ্দ করা হয়।
    - **subtract** টুলের জন্য যথাযথ `a` এবং `b` মান বরাদ্দ করা হয়।
    - প্রতিটি টুলের প্রতিক্রিয়া **Tool Response**-এ প্রদান করা হয়।
    - মডেলের চূড়ান্ত আউটপুট **Model Response**-এ প্রদান করা হয়।
1. এজেন্ট পরীক্ষা করার জন্য অতিরিক্ত প্রম্পট জমা দিন। আপনি **User prompt** ফিল্ডে বিদ্যমান প্রম্পটটি পরিবর্তন করতে পারেন ফিল্ডে ক্লিক করে এবং বিদ্যমান প্রম্পটটি প্রতিস্থাপন করে।
1. একবার আপনি এজেন্ট পরীক্ষা শেষ করলে, **terminal** ব্যবহার করে সার্ভার বন্ধ করতে **CTRL/CMD+C** লিখুন।

## অ্যাসাইনমেন্ট

আপনার **server.py** ফাইলের একটি অতিরিক্ত টুল এন্ট্রি যোগ করার চেষ্টা করুন (যেমন: একটি সংখ্যার বর্গমূল ফেরত দিন)। এমন অতিরিক্ত প্রম্পট জমা দিন যা আপনার নতুন টুল (বা বিদ্যমান টুল) ব্যবহার করার প্রয়োজন হবে। নতুন টুল লোড করতে সার্ভার পুনরায় চালু করতে ভুলবেন না।

## সমাধান

[Solution](./solution/README.md)

## মূল বিষয়গুলো

এই অধ্যায়ের মূল বিষয়গুলো হলো:

- AI Toolkit এক্সটেনশন একটি চমৎকার ক্লায়েন্ট যা MCP সার্ভার এবং তাদের টুল কনজিউম করতে দেয়।
- আপনি MCP সার্ভারে নতুন টুল যোগ করতে পারেন, এজেন্টের ক্ষমতা প্রসারিত করে ক্রমবর্ধমান প্রয়োজনীয়তা পূরণ করতে।
- AI Toolkit টেমপ্লেট (যেমন: Python MCP সার্ভার টেমপ্লেট) অন্তর্ভুক্ত করে যা কাস্টম টুল তৈরি করা সহজ করে।

## অতিরিক্ত সম্পদ

- [AI Toolkit ডকস](https://aka.ms/AIToolkit/doc)

## পরবর্তী কী
- পরবর্তী: [Testing & Debugging](../08-testing/README.md)

**অস্বীকৃতি**:  
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনুবাদ করা হয়েছে। আমরা যথাসম্ভব সঠিকতার জন্য চেষ্টা করি, তবে অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। এর মূল ভাষায় থাকা নথিটিকে প্রামাণিক উৎস হিসেবে বিবেচনা করা উচিত। গুরুত্বপূর্ণ তথ্যের জন্য, পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদ ব্যবহারের ফলে কোনো ভুল বোঝাবুঝি বা ভুল ব্যাখ্যা হলে আমরা তার জন্য দায়ী থাকব না।