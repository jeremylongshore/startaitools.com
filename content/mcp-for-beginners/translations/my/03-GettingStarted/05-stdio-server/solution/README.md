<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e378b47e0361b7a9b0dab7a0306878c8",
  "translation_date": "2025-08-26T20:04:11+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/README.md",
  "language_code": "my"
}
-->
# MCP stdio Server Solutions

> **⚠️ အရေးကြီး**: ဒီဖြေရှင်းနည်းတွေကို MCP Specification 2025-06-18 မှအကြံပြုထားတဲ့ **stdio transport** ကိုအသုံးပြုဖို့အတွက် အပ်ဒိတ်လုပ်ထားပါတယ်။ မူရင်း SSE (Server-Sent Events) transport ကိုတော့ အသုံးမပြုတော့ပါဘူး။

ဒီမှာ stdio transport ကိုအသုံးပြုပြီး MCP server တွေကို တည်ဆောက်ဖို့အတွက် runtime တစ်ခုချင်းစီအတွက် ပြည့်စုံတဲ့ဖြေရှင်းနည်းတွေကို ဖော်ပြထားပါတယ် -

- [TypeScript](../../../../../03-GettingStarted/05-stdio-server/solution/typescript) - stdio server ကို အပြည့်အစုံတည်ဆောက်ထားတဲ့ TypeScript
- [Python](../../../../../03-GettingStarted/05-stdio-server/solution/python) - asyncio နဲ့အတူ Python stdio server
- [.NET](../../../../../03-GettingStarted/05-stdio-server/solution/dotnet) - dependency injection နဲ့အတူ .NET stdio server

ဖြေရှင်းနည်းတစ်ခုချင်းစီမှာ ဖော်ပြထားတာတွေကတော့:
- stdio transport ကို စတင်တပ်ဆင်ခြင်း
- server tools တွေကို သတ်မှတ်ခြင်း
- JSON-RPC message တွေကို မှန်ကန်စွာ ကိုင်တွယ်ခြင်း
- Claude လို MCP client တွေနဲ့ ပေါင်းစည်းခြင်း

ဖြေရှင်းနည်းအားလုံးဟာ လက်ရှိ MCP specification ကိုလိုက်နာပြီး stdio transport ကို အသုံးပြုထားတာကြောင့် အကောင်းဆုံး performance နဲ့ security ရရှိစေပါတယ်။

---

**အကြောင်းကြားချက်**:  
ဤစာရွက်စာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) ကို အသုံးပြု၍ ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှုအတွက် ကြိုးစားနေသော်လည်း၊ အလိုအလျောက် ဘာသာပြန်မှုများတွင် အမှားများ သို့မဟုတ် မတိကျမှုများ ပါဝင်နိုင်သည်ကို သတိပြုပါ။ မူရင်းဘာသာစကားဖြင့် ရေးသားထားသော စာရွက်စာတမ်းကို အာဏာတရ အရင်းအမြစ်အဖြစ် ရှုလေ့လာသင့်ပါသည်။ အရေးကြီးသော အချက်အလက်များအတွက် လူ့ဘာသာပြန်ပညာရှင်များမှ ပရော်ဖက်ရှင်နယ် ဘာသာပြန်မှုကို အကြံပြုပါသည်။ ဤဘာသာပြန်မှုကို အသုံးပြုခြင်းမှ ဖြစ်ပေါ်လာသော အလွဲအလွတ်များ သို့မဟုတ် အနားယူမှုများအတွက် ကျွန်ုပ်တို့သည် တာဝန်မယူပါ။