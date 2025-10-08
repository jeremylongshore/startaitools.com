<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "ac2459c0d5cc823922e3d9240a95028c",
  "translation_date": "2025-07-13T19:06:29+00:00",
  "source_file": "03-GettingStarted/03-llm-client/solution/java/README.md",
  "language_code": "ur"
}
-->
# Calculator LLM Client

ایک جاوا ایپلیکیشن جو LangChain4j کو استعمال کرتے ہوئے MCP (Model Context Protocol) کیلکولیٹر سروس سے GitHub Models انٹیگریشن کے ساتھ جڑنے کا طریقہ دکھاتی ہے۔

## ضروریات

- جاوا 21 یا اس سے اوپر
- Maven 3.6+ (یا شامل Maven wrapper استعمال کریں)
- ایک GitHub اکاؤنٹ جسے GitHub Models تک رسائی حاصل ہو
- ایک MCP کیلکولیٹر سروس جو `http://localhost:8080` پر چل رہی ہو

## GitHub ٹوکن حاصل کرنا

یہ ایپلیکیشن GitHub Models استعمال کرتی ہے جس کے لیے GitHub پرسنل ایکسیس ٹوکن کی ضرورت ہوتی ہے۔ اپنا ٹوکن حاصل کرنے کے لیے درج ذیل مراحل پر عمل کریں:

### 1. GitHub Models تک رسائی حاصل کریں
1. [GitHub Models](https://github.com/marketplace/models) پر جائیں
2. اپنے GitHub اکاؤنٹ سے سائن ان کریں
3. اگر پہلے سے رسائی نہیں ہے تو GitHub Models کے لیے درخواست دیں

### 2. پرسنل ایکسیس ٹوکن بنائیں
1. [GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)](https://github.com/settings/tokens) پر جائیں
2. "Generate new token" → "Generate new token (classic)" پر کلک کریں
3. اپنے ٹوکن کو ایک وضاحتی نام دیں (مثلاً "MCP Calculator Client")
4. میعاد ختم ہونے کی تاریخ مقرر کریں جیسا ضرورت ہو
5. درج ذیل اسکوپس منتخب کریں:
   - `repo` (اگر پرائیویٹ ریپوزٹریز تک رسائی چاہیے)
   - `user:email`
6. "Generate token" پر کلک کریں
7. **اہم**: ٹوکن کو فوراً کاپی کر لیں - آپ اسے دوبارہ نہیں دیکھ سکیں گے!

### 3. ماحول کا متغیر سیٹ کریں

#### ونڈوز (کمانڈ پرامپٹ) پر:
```cmd
set GITHUB_TOKEN=your_github_token_here
```

#### ونڈوز (پاور شیل) پر:
```powershell
$env:GITHUB_TOKEN="your_github_token_here"
```

#### میک او ایس/لینکس پر:
```bash
export GITHUB_TOKEN=your_github_token_here
```

## سیٹ اپ اور انسٹالیشن

1. **پروجیکٹ ڈائریکٹری کلون کریں یا وہاں جائیں**

2. **انحصارات انسٹال کریں**:
   ```cmd
   mvnw clean install
   ```
   یا اگر آپ کے پاس Maven عالمی طور پر انسٹال ہے:
   ```cmd
   mvn clean install
   ```

3. **ماحول کا متغیر سیٹ کریں** (اوپر "GitHub ٹوکن حاصل کرنا" سیکشن دیکھیں)

4. **MCP کیلکولیٹر سروس شروع کریں**:
   یقینی بنائیں کہ آپ کے پاس باب 1 کی MCP کیلکولیٹر سروس `http://localhost:8080/sse` پر چل رہی ہو۔ کلائنٹ شروع کرنے سے پہلے یہ سروس چل رہی ہونی چاہیے۔

## ایپلیکیشن چلانا

```cmd
mvnw clean package
java -jar target\calculator-llm-client-0.0.1-SNAPSHOT.jar
```

## ایپلیکیشن کیا کرتی ہے

یہ ایپلیکیشن کیلکولیٹر سروس کے ساتھ تین اہم تعاملات دکھاتی ہے:

1. **جمع**: 24.5 اور 17.3 کا مجموعہ نکالتی ہے
2. **اسکوائر روٹ**: 144 کا مربع جذر نکالتی ہے
3. **مدد**: دستیاب کیلکولیٹر فنکشنز دکھاتی ہے

## متوقع نتیجہ

کامیابی سے چلنے پر آپ کو درج ذیل جیسا نتیجہ نظر آئے گا:

```
The sum of 24.5 and 17.3 is 41.8.
The square root of 144 is 12.
The calculator service provides the following functions: add, subtract, multiply, divide, sqrt, power...
```

## مسائل کا حل

### عام مسائل

1. **"GITHUB_TOKEN ماحول کا متغیر سیٹ نہیں ہے"**
   - یقینی بنائیں کہ آپ نے `GITHUB_TOKEN` ماحول کا متغیر سیٹ کیا ہے
   - متغیر سیٹ کرنے کے بعد اپنا ٹرمینل/کمانڈ پرامپٹ دوبارہ شروع کریں

2. **"localhost:8080 سے کنکشن مسترد"**
   - چیک کریں کہ MCP کیلکولیٹر سروس پورٹ 8080 پر چل رہی ہے
   - دیکھیں کہ کوئی اور سروس پورٹ 8080 استعمال تو نہیں کر رہی

3. **"تصدیق ناکام"**
   - اپنے GitHub ٹوکن کی درستگی اور اجازتوں کی تصدیق کریں
   - چیک کریں کہ آپ کو GitHub Models تک رسائی حاصل ہے

4. **Maven بلڈ کی غلطیاں**
   - یقینی بنائیں کہ آپ جاوا 21 یا اس سے اوپر استعمال کر رہے ہیں: `java -version`
   - بلڈ صاف کرنے کی کوشش کریں: `mvnw clean`

### ڈیبگنگ

ڈیبگ لاگنگ فعال کرنے کے لیے، ایپلیکیشن چلانے کے دوران درج ذیل JVM آرگیومنٹ شامل کریں:
```cmd
java -Dlogging.level.dev.langchain4j=DEBUG -jar target\calculator-llm-client-0.0.1-SNAPSHOT.jar
```

## کنفیگریشن

ایپلیکیشن کی کنفیگریشن درج ذیل ہے:
- GitHub Models کو `gpt-4.1-nano` ماڈل کے ساتھ استعمال کرنا
- MCP سروس سے `http://localhost:8080/sse` پر کنکشن
- درخواستوں کے لیے 60 سیکنڈ کا ٹائم آؤٹ
- ڈیبگنگ کے لیے درخواست/جواب لاگنگ فعال کرنا

## انحصارات

اس پروجیکٹ میں استعمال ہونے والے اہم انحصارات:
- **LangChain4j**: AI انٹیگریشن اور ٹول مینجمنٹ کے لیے
- **LangChain4j MCP**: Model Context Protocol سپورٹ کے لیے
- **LangChain4j GitHub Models**: GitHub Models انٹیگریشن کے لیے
- **Spring Boot**: ایپلیکیشن فریم ورک اور انحصار انجیکشن کے لیے

## لائسنس

یہ پروجیکٹ Apache License 2.0 کے تحت لائسنس یافتہ ہے - تفصیلات کے لیے [LICENSE](../../../../../../03-GettingStarted/03-llm-client/solution/java/LICENSE) فائل دیکھیں۔

**دستخطی نوٹ**:  
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ اگرچہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنی مادری زبان میں ہی معتبر ماخذ سمجھی جانی چاہیے۔ اہم معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم پر عائد نہیں ہوتی۔