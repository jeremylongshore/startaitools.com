<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "706b9b075dc484b73a053e6e9c709b4b",
  "translation_date": "2025-07-13T23:35:37+00:00",
  "source_file": "04-PracticalImplementation/samples/python/README.md",
  "language_code": "my"
}
-->
# Model Context Protocol (MCP) Python အကောင်အထည်ဖော်ခြင်း

ဤ repository တွင် Model Context Protocol (MCP) ကို Python ဖြင့် အကောင်အထည်ဖော်ထားပြီး MCP စံသတ်မှတ်ချက်ကို အသုံးပြုကာ ဆာဗာနှင့် ကလိုင်ယင့် အပလီကေးရှင်းများကို ဖန်တီးပုံကို ပြသထားသည်။

## အနှစ်ချုပ်

MCP အကောင်အထည်ဖော်မှုတွင် အဓိက အစိတ်အပိုင်း ၂ ခု ပါဝင်သည်-

1. **MCP Server (`server.py`)** - ဆာဗာတစ်ခုဖြစ်ပြီး အောက်ပါအရာများကို ပေးဆောင်သည်-
   - **Tools**: ဝေးလံမှ ခေါ်ယူနိုင်သော function များ
   - **Resources**: ရယူနိုင်သော ဒေတာများ
   - **Prompts**: ဘာသာစကားမော်ဒယ်များအတွက် prompt များ ဖန်တီးရန် template များ

2. **MCP Client (`client.py`)** - ဆာဗာနှင့် ချိတ်ဆက်ပြီး ၎င်း၏ လုပ်ဆောင်ချက်များကို အသုံးပြုသော client application

## လုပ်ဆောင်ချက်များ

ဤအကောင်အထည်ဖော်မှုတွင် MCP ၏ အဓိက လုပ်ဆောင်ချက်များကို ပြသထားသည်-

### Tools
- `completion` - AI မော်ဒယ်များမှ စာသားဖြည့်စွက်မှုများ ဖန်တီးပေးသည် (အတု)
- `add` - နံပါတ် ၂ ခုကို ပေါင်းတွက်ပေးသော ရိုးရှင်းသော ကိန်းဂဏန်းကိရိယာ

### Resources
- `models://` - ရရှိနိုင်သော AI မော်ဒယ်များအကြောင်း အချက်အလက် ပြန်ပေးသည်
- `greeting://{name}` - ပေးထားသော နာမည်အတွက် ကိုယ်ပိုင် မင်္ဂလာပါ စကားပြန်ပေးသည်

### Prompts
- `review_code` - ကုဒ်စစ်ဆေးရန် prompt ဖန်တီးပုံ template

## တပ်ဆင်ခြင်း

ဤ MCP အကောင်အထည်ဖော်မှုကို အသုံးပြုရန် လိုအပ်သော package များကို တပ်ဆင်ပါ-

```powershell
pip install mcp-server mcp-client
```

## ဆာဗာနှင့် ကလိုင်ယင့် စတင်ပြေးဆွဲခြင်း

### ဆာဗာ စတင်ခြင်း

တစ်ခုသော terminal ပြတင်းပေါ်တွင် ဆာဗာကို ပြေးဆွဲပါ-

```powershell
python server.py
```

MCP CLI ကို အသုံးပြု၍ ဖွံ့ဖြိုးရေး mode ဖြင့်လည်း ဆာဗာကို ပြေးဆွဲနိုင်သည်-

```powershell
mcp dev server.py
```

သို့မဟုတ် Claude Desktop တွင် တပ်ဆင်ထားပါက အသုံးပြုနိုင်သည်-

```powershell
mcp install server.py
```

### ကလိုင်ယင့် ပြေးဆွဲခြင်း

အခြား terminal ပြတင်းပေါ်တွင် ကလိုင်ယင့်ကို ပြေးဆွဲပါ-

```powershell
python client.py
```

ဤကလိုင်ယင့်သည် ဆာဗာနှင့် ချိတ်ဆက်ကာ ရရှိနိုင်သည့် လုပ်ဆောင်ချက်များအားလုံးကို ပြသပေးမည်ဖြစ်သည်။

### ကလိုင်ယင့် အသုံးပြုမှု

ကလိုင်ယင့် (`client.py`) သည် MCP ၏ လုပ်ဆောင်ချက်များအားလုံးကို ပြသထားသည်-

```powershell
python client.py
```

ဤကလိုင်ယင့်သည် ဆာဗာနှင့် ချိတ်ဆက်ကာ tools, resources, prompts အပါအဝင် လုပ်ဆောင်ချက်များအားလုံးကို အသုံးပြုမည်ဖြစ်ပြီး အောက်ပါအရာများကို ပြသမည်-

1. ကိန်းဂဏန်းကိရိယာရလဒ် (5 + 7 = 12)
2. "What is the meaning of life?" ဆိုသော စာသားအတွက် completion tool ၏ တုံ့ပြန်ချက်
3. ရရှိနိုင်သော AI မော်ဒယ်များစာရင်း
4. "MCP Explorer" အတွက် ကိုယ်ပိုင် မင်္ဂလာပါ စကား
5. ကုဒ်စစ်ဆေးရန် prompt template

## အကောင်အထည်ဖော်မှု အသေးစိတ်

ဆာဗာကို `FastMCP` API ဖြင့် အကောင်အထည်ဖော်ထားပြီး MCP ဝန်ဆောင်မှုများ သတ်မှတ်ရာတွင် အဆင့်မြင့် abstraction များ ပေးသည်။ tools များ သတ်မှတ်ပုံကို ရိုးရှင်းစွာ ဖော်ပြထားသည်-

```python
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The sum of the two numbers
    """
    logger.info(f"Adding {a} and {b}")
    return a + b
```

ကလိုင်ယင့်သည် MCP client library ကို အသုံးပြုကာ ဆာဗာနှင့် ချိတ်ဆက်ပြီး ခေါ်ယူသည်-

```python
async with stdio_client(server_params) as (reader, writer):
    async with ClientSession(reader, writer) as session:
        await session.initialize()
        result = await session.call_tool("add", arguments={"a": 5, "b": 7})
```

## ပိုမိုသိရှိလိုပါက

MCP အကြောင်း ပိုမိုသိရှိလိုပါက အောက်ပါလင့်ခ်သို့ ဝင်ကြည့်ပါ- https://modelcontextprotocol.io/

**အကြောင်းကြားချက်**  
ဤစာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) ဖြင့် ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှန်ကန်မှုအတွက် ကြိုးစားသော်လည်း အလိုအလျောက် ဘာသာပြန်ခြင်းတွင် အမှားများ သို့မဟုတ် မှားယွင်းချက်များ ပါဝင်နိုင်ကြောင်း သတိပြုပါရန် မေတ္တာရပ်ခံအပ်ပါသည်။ မူရင်းစာတမ်းကို မိမိဘာသာစကားဖြင့်သာ တရားဝင်အချက်အလက်အဖြစ် ယူဆသင့်ပါသည်။ အရေးကြီးသော အချက်အလက်များအတွက် လူ့ဘာသာပြန်ပညာရှင်မှ ဘာသာပြန်ခြင်းကို အကြံပြုပါသည်။ ဤဘာသာပြန်ချက်ကို အသုံးပြုရာမှ ဖြစ်ပေါ်လာနိုင်သည့် နားလည်မှုမှားယွင်းမှုများအတွက် ကျွန်ုပ်တို့သည် တာဝန်မယူပါ။