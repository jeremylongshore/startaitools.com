<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "706b9b075dc484b73a053e6e9c709b4b",
  "translation_date": "2025-07-13T23:30:24+00:00",
  "source_file": "04-PracticalImplementation/samples/python/README.md",
  "language_code": "ur"
}
-->
# ماڈل کانٹیکسٹ پروٹوکول (MCP) پائتھن امپلیمنٹیشن

یہ ریپوزیٹری ماڈل کانٹیکسٹ پروٹوکول (MCP) کی پائتھن امپلیمنٹیشن پر مشتمل ہے، جو دکھاتی ہے کہ کس طرح ایک سرور اور کلائنٹ ایپلیکیشن بنائی جاتی ہے جو MCP اسٹینڈرڈ کے ذریعے بات چیت کرتی ہیں۔

## جائزہ

MCP امپلیمنٹیشن دو اہم اجزاء پر مشتمل ہے:

1. **MCP سرور (`server.py`)** - ایک سرور جو فراہم کرتا ہے:
   - **Tools**: وہ فنکشنز جو دور سے کال کیے جا سکتے ہیں
   - **Resources**: وہ ڈیٹا جو حاصل کیا جا سکتا ہے
   - **Prompts**: زبان کے ماڈلز کے لیے پرامپٹ بنانے کے ٹیمپلیٹس

2. **MCP کلائنٹ (`client.py`)** - ایک کلائنٹ ایپلیکیشن جو سرور سے جڑتی ہے اور اس کی خصوصیات استعمال کرتی ہے

## خصوصیات

یہ امپلیمنٹیشن MCP کی کئی اہم خصوصیات دکھاتی ہے:

### Tools
- `completion` - AI ماڈلز سے متن کی تکمیل پیدا کرتا ہے (نقلی)
- `add` - ایک سادہ کیلکولیٹر جو دو نمبروں کو جمع کرتا ہے

### Resources
- `models://` - دستیاب AI ماڈلز کی معلومات واپس کرتا ہے
- `greeting://{name}` - دیے گئے نام کے لیے ذاتی نوعیت کا سلام واپس کرتا ہے

### Prompts
- `review_code` - کوڈ کا جائزہ لینے کے لیے پرامپٹ تیار کرتا ہے

## تنصیب

اس MCP امپلیمنٹیشن کو استعمال کرنے کے لیے، مطلوبہ پیکجز انسٹال کریں:

```powershell
pip install mcp-server mcp-client
```

## سرور اور کلائنٹ چلانا

### سرور شروع کرنا

سرور کو ایک ٹرمینل ونڈو میں چلائیں:

```powershell
python server.py
```

سرور کو MCP CLI کے ذریعے ڈیولپمنٹ موڈ میں بھی چلایا جا سکتا ہے:

```powershell
mcp dev server.py
```

یا Claude Desktop میں انسٹال کیا جا سکتا ہے (اگر دستیاب ہو):

```powershell
mcp install server.py
```

### کلائنٹ چلانا

کلائنٹ کو دوسری ٹرمینل ونڈو میں چلائیں:

```powershell
python client.py
```

یہ سرور سے جڑ جائے گا اور تمام دستیاب خصوصیات کا مظاہرہ کرے گا۔

### کلائنٹ کا استعمال

کلائنٹ (`client.py`) MCP کی تمام صلاحیتوں کا مظاہرہ کرتا ہے:

```powershell
python client.py
```

یہ سرور سے جڑ کر تمام خصوصیات بشمول tools، resources، اور prompts کو استعمال کرے گا۔ آؤٹ پٹ میں دکھایا جائے گا:

1. کیلکولیٹر ٹول کا نتیجہ (5 + 7 = 12)
2. "What is the meaning of life?" کے جواب میں completion ٹول کی آؤٹ پٹ
3. دستیاب AI ماڈلز کی فہرست
4. "MCP Explorer" کے لیے ذاتی سلام
5. کوڈ ریویو پرامپٹ ٹیمپلیٹ

## امپلیمنٹیشن کی تفصیلات

سرور `FastMCP` API استعمال کرتے ہوئے بنایا گیا ہے، جو MCP سروسز کی تعریف کے لیے اعلیٰ سطح کی تجریدات فراہم کرتا ہے۔ یہاں ایک سادہ مثال ہے کہ tools کیسے تعریف کیے جاتے ہیں:

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

کلائنٹ MCP کلائنٹ لائبریری استعمال کرتا ہے تاکہ سرور سے جڑ سکے اور کال کر سکے:

```python
async with stdio_client(server_params) as (reader, writer):
    async with ClientSession(reader, writer) as session:
        await session.initialize()
        result = await session.call_tool("add", arguments={"a": 5, "b": 7})
```

## مزید جانیں

MCP کے بارے میں مزید معلومات کے لیے ملاحظہ کریں: https://modelcontextprotocol.io/

**دستخطی نوٹ**:  
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ اگرچہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنی مادری زبان میں معتبر ماخذ سمجھی جانی چاہیے۔ اہم معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم پر عائد نہیں ہوتی۔