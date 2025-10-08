<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "41f16dac486d2086a53bc644a01cbe42",
  "translation_date": "2025-08-18T14:01:36+00:00",
  "source_file": "07-LessonsfromEarlyAdoption/README.md",
  "language_code": "ur"
}
-->
# 🌟 ابتدائی صارفین سے سیکھے گئے اسباق

[![ابتدائی صارفین سے سیکھے گئے اسباق](../../../translated_images/08.980bb2babbaadd8a97739effc9b31e5f1abd8f4c4a3fbc90fb9f931a866674d0.ur.png)](https://youtu.be/jds7dSmNptE)

_(اوپر دی گئی تصویر پر کلک کریں تاکہ اس سبق کی ویڈیو دیکھ سکیں)_

## 🎯 اس ماڈیول میں کیا شامل ہے

یہ ماڈیول دریافت کرتا ہے کہ حقیقی تنظیمیں اور ڈویلپرز ماڈل کانٹیکسٹ پروٹوکول (MCP) کو کس طرح استعمال کر رہے ہیں تاکہ حقیقی چیلنجز کو حل کیا جا سکے اور جدت کو فروغ دیا جا سکے۔ تفصیلی کیس اسٹڈیز اور عملی منصوبوں کے ذریعے، آپ یہ جانیں گے کہ MCP کس طرح محفوظ، توسیع پذیر AI انضمام کو ممکن بناتا ہے جو زبان کے ماڈلز، ٹولز، اور انٹرپرائز ڈیٹا کو جوڑتا ہے۔

### 📚 MCP کو عملی طور پر دیکھیں

کیا آپ ان اصولوں کو پروڈکشن کے لیے تیار ٹولز پر لاگو ہوتا دیکھنا چاہتے ہیں؟ ہمارے [**10 مائیکروسافٹ MCP سرورز جو ڈویلپرز کی پیداواریت کو بدل رہے ہیں**](microsoft-mcp-servers.md) کو دیکھیں، جو حقیقی مائیکروسافٹ MCP سرورز کو پیش کرتے ہیں جنہیں آپ آج استعمال کر سکتے ہیں۔

## جائزہ

یہ سبق دریافت کرتا ہے کہ ابتدائی صارفین نے ماڈل کانٹیکسٹ پروٹوکول (MCP) کو حقیقی دنیا کے چیلنجز کو حل کرنے اور مختلف صنعتوں میں جدت کو فروغ دینے کے لیے کس طرح استعمال کیا۔ تفصیلی کیس اسٹڈیز اور عملی منصوبوں کے ذریعے، آپ دیکھیں گے کہ MCP کس طرح معیاری، محفوظ، اور توسیع پذیر AI انضمام کو ممکن بناتا ہے—بڑے زبان کے ماڈلز، ٹولز، اور انٹرپرائز ڈیٹا کو ایک متحد فریم ورک میں جوڑتا ہے۔ آپ MCP پر مبنی حل ڈیزائن اور بنانے کا عملی تجربہ حاصل کریں گے، ثابت شدہ نفاذ کے نمونوں سے سیکھیں گے، اور پروڈکشن ماحول میں MCP کو تعینات کرنے کے بہترین طریقوں کو دریافت کریں گے۔ سبق ابھرتے ہوئے رجحانات، مستقبل کی سمتوں، اور اوپن سورس وسائل کو بھی اجاگر کرتا ہے تاکہ آپ کو MCP ٹیکنالوجی اور اس کے ارتقاء پذیر ماحولیاتی نظام کے ساتھ آگے رہنے میں مدد ملے۔

## سیکھنے کے مقاصد

- مختلف صنعتوں میں حقیقی دنیا کے MCP نفاذ کا تجزیہ کریں  
- مکمل MCP پر مبنی ایپلیکیشنز ڈیزائن اور بنائیں  
- MCP ٹیکنالوجی میں ابھرتے ہوئے رجحانات اور مستقبل کی سمتوں کو دریافت کریں  
- حقیقی ترقیاتی منظرناموں میں بہترین طریقوں کا اطلاق کریں  

## حقیقی دنیا کے MCP نفاذ

### کیس اسٹڈی 1: انٹرپرائز کسٹمر سپورٹ آٹومیشن

ایک کثیر القومی کارپوریشن نے اپنے کسٹمر سپورٹ سسٹمز میں AI تعاملات کو معیاری بنانے کے لیے MCP پر مبنی حل نافذ کیا۔ اس سے انہیں یہ ممکن ہوا:

- متعدد LLM فراہم کنندگان کے لیے ایک متحد انٹرفیس بنانا  
- مختلف محکموں میں مستقل پرامپٹ مینجمنٹ کو برقرار رکھنا  
- مضبوط سیکیورٹی اور تعمیل کنٹرولز کو نافذ کرنا  
- مخصوص ضروریات کی بنیاد پر مختلف AI ماڈلز کے درمیان آسانی سے سوئچ کرنا  

**تکنیکی نفاذ:**

```python
# Python MCP server implementation for customer support
import logging
import asyncio
from modelcontextprotocol import create_server, ServerConfig
from modelcontextprotocol.server import MCPServer
from modelcontextprotocol.transports import create_http_transport
from modelcontextprotocol.resources import ResourceDefinition
from modelcontextprotocol.prompts import PromptDefinition
from modelcontextprotocol.tool import ToolDefinition

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    # Create server configuration
    config = ServerConfig(
        name="Enterprise Customer Support Server",
        version="1.0.0",
        description="MCP server for handling customer support inquiries"
    )
    
    # Initialize MCP server
    server = create_server(config)
    
    # Register knowledge base resources
    server.resources.register(
        ResourceDefinition(
            name="customer_kb",
            description="Customer knowledge base documentation"
        ),
        lambda params: get_customer_documentation(params)
    )
    
    # Register prompt templates
    server.prompts.register(
        PromptDefinition(
            name="support_template",
            description="Templates for customer support responses"
        ),
        lambda params: get_support_templates(params)
    )
    
    # Register support tools
    server.tools.register(
        ToolDefinition(
            name="ticketing",
            description="Create and update support tickets"
        ),
        handle_ticketing_operations
    )
    
    # Start server with HTTP transport
    transport = create_http_transport(port=8080)
    await server.run(transport)

if __name__ == "__main__":
    asyncio.run(main())
```

**نتائج:** ماڈل کے اخراجات میں 30% کمی، جواب کی مستقل مزاجی میں 45% بہتری، اور عالمی آپریشنز میں بہتر تعمیل۔

### کیس اسٹڈی 2: ہیلتھ کیئر ڈائیگنوسٹک اسسٹنٹ

ایک ہیلتھ کیئر فراہم کنندہ نے متعدد خصوصی طبی AI ماڈلز کو مربوط کرنے کے لیے MCP انفراسٹرکچر تیار کیا جبکہ حساس مریض کے ڈیٹا کو محفوظ رکھا:

- عمومی اور خصوصی طبی ماڈلز کے درمیان ہموار سوئچنگ  
- سخت پرائیویسی کنٹرولز اور آڈٹ ٹریلز  
- موجودہ الیکٹرانک ہیلتھ ریکارڈ (EHR) سسٹمز کے ساتھ انضمام  
- طبی اصطلاحات کے لیے مستقل پرامپٹ انجینئرنگ  

**تکنیکی نفاذ:**

```csharp
// C# MCP host application implementation in healthcare application
using Microsoft.Extensions.DependencyInjection;
using ModelContextProtocol.SDK.Client;
using ModelContextProtocol.SDK.Security;
using ModelContextProtocol.SDK.Resources;

public class DiagnosticAssistant
{
    private readonly MCPHostClient _mcpClient;
    private readonly PatientContext _patientContext;
    
    public DiagnosticAssistant(PatientContext patientContext)
    {
        _patientContext = patientContext;
        
        // Configure MCP client with healthcare-specific settings
        var clientOptions = new ClientOptions
        {
            Name = "Healthcare Diagnostic Assistant",
            Version = "1.0.0",
            Security = new SecurityOptions
            {
                Encryption = EncryptionLevel.Medical,
                AuditEnabled = true
            }
        };
        
        _mcpClient = new MCPHostClientBuilder()
            .WithOptions(clientOptions)
            .WithTransport(new HttpTransport("https://healthcare-mcp.example.org"))
            .WithAuthentication(new HIPAACompliantAuthProvider())
            .Build();
    }
    
    public async Task<DiagnosticSuggestion> GetDiagnosticAssistance(
        string symptoms, string patientHistory)
    {
        // Create request with appropriate resources and tool access
        var resourceRequest = new ResourceRequest
        {
            Name = "patient_records",
            Parameters = new Dictionary<string, object>
            {
                ["patientId"] = _patientContext.PatientId,
                ["requestingProvider"] = _patientContext.ProviderId
            }
        };
        
        // Request diagnostic assistance using appropriate prompt
        var response = await _mcpClient.SendPromptRequestAsync(
            promptName: "diagnostic_assistance",
            parameters: new Dictionary<string, object>
            {
                ["symptoms"] = symptoms,
                patientHistory = patientHistory,
                relevantGuidelines = _patientContext.GetRelevantGuidelines()
            });
            
        return DiagnosticSuggestion.FromMCPResponse(response);
    }
}
```

**نتائج:** HIPAA کی مکمل تعمیل کے ساتھ ڈاکٹروں کے لیے بہتر تشخیصی تجاویز اور سسٹمز کے درمیان سیاق و سباق کی تبدیلی میں نمایاں کمی۔

### کیس اسٹڈی 3: مالیاتی خدمات کے خطرے کا تجزیہ

ایک مالیاتی ادارے نے اپنے خطرے کے تجزیے کے عمل کو مختلف محکموں میں معیاری بنانے کے لیے MCP کو نافذ کیا:

- کریڈٹ رسک، دھوکہ دہی کا پتہ لگانے، اور سرمایہ کاری کے خطرے کے ماڈلز کے لیے ایک متحد انٹرفیس بنایا  
- سخت رسائی کنٹرولز اور ماڈل ورژننگ کو نافذ کیا  
- تمام AI سفارشات کی آڈٹ ایبلٹی کو یقینی بنایا  
- متنوع سسٹمز میں مستقل ڈیٹا فارمیٹنگ کو برقرار رکھا  

**تکنیکی نفاذ:**

```java
// Java MCP server for financial risk assessment
import org.mcp.server.*;
import org.mcp.security.*;

public class FinancialRiskMCPServer {
    public static void main(String[] args) {
        // Create MCP server with financial compliance features
        MCPServer server = new MCPServerBuilder()
            .withModelProviders(
                new ModelProvider("risk-assessment-primary", new AzureOpenAIProvider()),
                new ModelProvider("risk-assessment-audit", new LocalLlamaProvider())
            )
            .withPromptTemplateDirectory("./compliance/templates")
            .withAccessControls(new SOCCompliantAccessControl())
            .withDataEncryption(EncryptionStandard.FINANCIAL_GRADE)
            .withVersionControl(true)
            .withAuditLogging(new DatabaseAuditLogger())
            .build();
            
        server.addRequestValidator(new FinancialDataValidator());
        server.addResponseFilter(new PII_RedactionFilter());
        
        server.start(9000);
        
        System.out.println("Financial Risk MCP Server running on port 9000");
    }
}
```

**نتائج:** بہتر ریگولیٹری تعمیل، ماڈل کی تعیناتی کے چکروں میں 40% تیزی، اور محکموں میں خطرے کے تجزیے کی مستقل مزاجی میں بہتری۔

### کیس اسٹڈی 4: مائیکروسافٹ پلے رائٹ MCP سرور برائے براؤزر آٹومیشن

مائیکروسافٹ نے ماڈل کانٹیکسٹ پروٹوکول کے ذریعے محفوظ، معیاری براؤزر آٹومیشن کو فعال کرنے کے لیے [پلے رائٹ MCP سرور](https://github.com/microsoft/playwright-mcp) تیار کیا۔ یہ پروڈکشن کے لیے تیار سرور AI ایجنٹس اور LLMs کو ویب براؤزرز کے ساتھ ایک کنٹرولڈ، آڈٹ ایبل، اور توسیع پذیر طریقے سے تعامل کرنے کی اجازت دیتا ہے—جیسے کہ خودکار ویب ٹیسٹنگ، ڈیٹا نکالنا، اور اختتام سے اختتام تک ورک فلو۔

> **🎯 پروڈکشن کے لیے تیار ٹول**  
> 
> یہ کیس اسٹڈی ایک حقیقی MCP سرور کو پیش کرتی ہے جسے آپ آج استعمال کر سکتے ہیں! پلے رائٹ MCP سرور اور دیگر 9 پروڈکشن کے لیے تیار مائیکروسافٹ MCP سرورز کے بارے میں مزید جانیں ہمارے [**مائیکروسافٹ MCP سرورز گائیڈ**](microsoft-mcp-servers.md#8--playwright-mcp-server) میں۔

**اہم خصوصیات:**
- براؤزر آٹومیشن کی صلاحیتوں کو MCP ٹولز کے طور پر پیش کرتا ہے (نیویگیشن، فارم بھرنا، اسکرین شاٹ لینا وغیرہ)  
- غیر مجاز کارروائیوں کو روکنے کے لیے سخت رسائی کنٹرولز اور سینڈ باکسنگ کو نافذ کرتا ہے  
- تمام براؤزر تعاملات کے لیے تفصیلی آڈٹ لاگز فراہم کرتا ہے  
- ایجنٹ سے چلنے والی آٹومیشن کے لیے Azure OpenAI اور دیگر LLM فراہم کنندگان کے ساتھ انضمام کی حمایت کرتا ہے  
- GitHub Copilot کے کوڈنگ ایجنٹ کو ویب براؤزنگ کی صلاحیتوں کے ساتھ طاقت دیتا ہے  

**تکنیکی نفاذ:**

```typescript
// TypeScript: Registering Playwright browser automation tools in an MCP server
import { createServer, ToolDefinition } from 'modelcontextprotocol';
import { launch } from 'playwright';

const server = createServer({
  name: 'Playwright MCP Server',
  version: '1.0.0',
  description: 'MCP server for browser automation using Playwright'
});

// Register a tool for navigating to a URL and capturing a screenshot
server.tools.register(
  new ToolDefinition({
    name: 'navigate_and_screenshot',
    description: 'Navigate to a URL and capture a screenshot',
    parameters: {
      url: { type: 'string', description: 'The URL to visit' }
    }
  }),
  async ({ url }) => {
    const browser = await launch();
    const page = await browser.newPage();
    await page.goto(url);
    const screenshot = await page.screenshot();
    await browser.close();
    return { screenshot };
  }
);

// Start the MCP server
server.listen(8080);
```

**نتائج:**

- AI ایجنٹس اور LLMs کے لیے محفوظ، پروگراماتی براؤزر آٹومیشن کو فعال کیا  
- ویب ایپلیکیشنز کے لیے دستی ٹیسٹنگ کی کوشش کو کم کیا اور ٹیسٹ کوریج کو بہتر بنایا  
- انٹرپرائز ماحول میں براؤزر پر مبنی ٹول انضمام کے لیے ایک دوبارہ قابل استعمال، توسیع پذیر فریم ورک فراہم کیا  
- GitHub Copilot کے ویب براؤزنگ کی صلاحیتوں کو طاقت دی  

**حوالہ جات:**

- [پلے رائٹ MCP سرور GitHub ریپوزٹری](https://github.com/microsoft/playwright-mcp)  
- [مائیکروسافٹ AI اور آٹومیشن حل](https://azure.microsoft.com/en-us/products/ai-services/)  

### کیس اسٹڈی 5: Azure MCP – انٹرپرائز-گریڈ ماڈل کانٹیکسٹ پروٹوکول بطور سروس

Azure MCP سرور ([https://aka.ms/azmcp](https://aka.ms/azmcp)) مائیکروسافٹ کا منظم، انٹرپرائز-گریڈ ماڈل کانٹیکسٹ پروٹوکول کا نفاذ ہے، جو ایک کلاؤڈ سروس کے طور پر توسیع پذیر، محفوظ، اور تعمیل شدہ MCP سرور کی صلاحیتیں فراہم کرنے کے لیے ڈیزائن کیا گیا ہے۔ Azure MCP تنظیموں کو MCP سرورز کو تیزی سے تعینات، منظم، اور Azure AI، ڈیٹا، اور سیکیورٹی خدمات کے ساتھ مربوط کرنے کے قابل بناتا ہے، آپریشنل اوور ہیڈ کو کم کرتا ہے اور AI اپنانے کو تیز کرتا ہے۔

> **🎯 پروڈکشن کے لیے تیار ٹول**  
> 
> یہ ایک حقیقی MCP سرور ہے جسے آپ آج استعمال کر سکتے ہیں! Azure AI Foundry MCP سرور کے بارے میں مزید جانیں ہمارے [**مائیکروسافٹ MCP سرورز گائیڈ**](microsoft-mcp-servers.md) میں۔

- بلٹ ان اسکیلنگ، مانیٹرنگ، اور سیکیورٹی کے ساتھ مکمل طور پر منظم MCP سرور ہوسٹنگ  
- Azure OpenAI، Azure AI Search، اور دیگر Azure خدمات کے ساتھ مقامی انضمام  
- Microsoft Entra ID کے ذریعے انٹرپرائز تصدیق اور اجازت  
- حسب ضرورت ٹولز، پرامپٹ ٹیمپلیٹس، اور وسائل کنیکٹرز کے لیے معاونت  
- انٹرپرائز سیکیورٹی اور ریگولیٹری تقاضوں کے ساتھ تعمیل  

**تکنیکی نفاذ:**

```yaml
# Example: Azure MCP server deployment configuration (YAML)
apiVersion: mcp.microsoft.com/v1
kind: McpServer
metadata:
  name: enterprise-mcp-server
spec:
  modelProviders:
    - name: azure-openai
      type: AzureOpenAI
      endpoint: https://<your-openai-resource>.openai.azure.com/
      apiKeySecret: <your-azure-keyvault-secret>
  tools:
    - name: document_search
      type: AzureAISearch
      endpoint: https://<your-search-resource>.search.windows.net/
      apiKeySecret: <your-azure-keyvault-secret>
  authentication:
    type: EntraID
    tenantId: <your-tenant-id>
  monitoring:
    enabled: true
    logAnalyticsWorkspace: <your-log-analytics-id>
```

**نتائج:**  
- انٹرپرائز AI منصوبوں کے لیے وقت کی قدر کو کم کیا، ایک تیار استعمال، تعمیل شدہ MCP سرور پلیٹ فارم فراہم کر کے  
- LLMs، ٹولز، اور انٹرپرائز ڈیٹا ذرائع کے انضمام کو آسان بنایا  
- MCP ورک لوڈز کے لیے سیکیورٹی، مشاہدہ، اور آپریشنل کارکردگی کو بہتر بنایا  
- Azure SDK کے بہترین طریقوں اور موجودہ تصدیقی نمونوں کے ساتھ کوڈ کے معیار کو بہتر بنایا  

**حوالہ جات:**  
- [Azure MCP دستاویزات](https://aka.ms/azmcp)  
- [Azure MCP سرور GitHub ریپوزٹری](https://github.com/Azure/azure-mcp)  
- [Azure AI خدمات](https://azure.microsoft.com/en-us/products/ai-services/)  
- [مائیکروسافٹ MCP سینٹر](https://mcp.azure.com)  
> **🎯 پروڈکشن کے لیے تیار ٹول**

> یہ ایک حقیقی MCP سرور ہے جسے آپ آج ہی استعمال کر سکتے ہیں! Microsoft Learn Docs MCP سرور کے بارے میں مزید جاننے کے لیے ہمارے [**Microsoft MCP Servers Guide**](microsoft-mcp-servers.md#1--microsoft-learn-docs-mcp-server) کو دیکھیں۔
**اہم خصوصیات:**
- مائیکروسافٹ کی آفیشل دستاویزات، Azure ڈاکس، اور Microsoft 365 دستاویزات تک حقیقی وقت میں رسائی
- جدید سیمینٹک سرچ کی صلاحیتیں جو سیاق و سباق اور ارادے کو سمجھتی ہیں
- ہمیشہ تازہ ترین معلومات کیونکہ Microsoft Learn کا مواد شائع ہوتا ہے
- Microsoft Learn، Azure دستاویزات، اور Microsoft 365 ذرائع کے درمیان جامع کوریج
- 10 اعلی معیار کے مواد کے حصے، آرٹیکل کے عنوانات اور URLs کے ساتھ واپس کرتا ہے

**یہ کیوں اہم ہے:**
- مائیکروسافٹ ٹیکنالوجیز کے لیے "پرانے AI علم" کے مسئلے کو حل کرتا ہے
- یقینی بناتا ہے کہ AI اسسٹنٹس کو .NET، C#, Azure، اور Microsoft 365 کی تازہ ترین خصوصیات تک رسائی حاصل ہو
- درست کوڈ جنریشن کے لیے مستند، فرسٹ پارٹی معلومات فراہم کرتا ہے
- مائیکروسافٹ ٹیکنالوجیز کے ساتھ کام کرنے والے ڈویلپرز کے لیے ضروری ہے جو تیزی سے ترقی کر رہی ہیں

**نتائج:**
- مائیکروسافٹ ٹیکنالوجیز کے لیے AI کے ذریعے تیار کردہ کوڈ کی درستگی میں نمایاں بہتری
- موجودہ دستاویزات اور بہترین طریقوں کی تلاش میں کم وقت صرف ہوتا ہے
- سیاق و سباق سے آگاہ دستاویزات کی بازیافت کے ساتھ ڈویلپرز کی پیداواری صلاحیت میں اضافہ
- IDE چھوڑے بغیر ترقیاتی ورک فلو کے ساتھ ہموار انضمام

**حوالہ جات:**
- [Microsoft Learn Docs MCP Server GitHub Repository](https://github.com/MicrosoftDocs/mcp)
- [Microsoft Learn Documentation](https://learn.microsoft.com/)

## عملی منصوبے

### منصوبہ 1: ملٹی پرووائیڈر MCP سرور بنائیں

**مقصد:** ایک MCP سرور بنائیں جو مخصوص معیار کی بنیاد پر متعدد AI ماڈل پرووائیڈرز کو درخواستیں بھیج سکے۔

**ضروریات:**

- کم از کم تین مختلف ماڈل پرووائیڈرز کی حمایت کریں (جیسے OpenAI، Anthropic، لوکل ماڈلز)
- درخواست میٹا ڈیٹا کی بنیاد پر روٹنگ میکانزم نافذ کریں
- پرووائیڈر کی اسناد کو منظم کرنے کے لیے کنفیگریشن سسٹم بنائیں
- کارکردگی اور اخراجات کو بہتر بنانے کے لیے کیشنگ شامل کریں
- استعمال کی نگرانی کے لیے ایک سادہ ڈیش بورڈ بنائیں

**عمل درآمد کے مراحل:**

1. بنیادی MCP سرور انفراسٹرکچر قائم کریں
2. ہر AI ماڈل سروس کے لیے پرووائیڈر ایڈاپٹر نافذ کریں
3. درخواست کی خصوصیات کی بنیاد پر روٹنگ منطق بنائیں
4. بار بار درخواستوں کے لیے کیشنگ میکانزم شامل کریں
5. نگرانی کے ڈیش بورڈ کو تیار کریں
6. مختلف درخواست کے نمونوں کے ساتھ ٹیسٹ کریں

**ٹیکنالوجیز:** Python (.NET/Java/Python آپ کی ترجیح کے مطابق)، Redis کیشنگ کے لیے، اور ڈیش بورڈ کے لیے ایک سادہ ویب فریم ورک۔

### منصوبہ 2: انٹرپرائز پرامپٹ مینجمنٹ سسٹم

**مقصد:** ایک MCP پر مبنی نظام تیار کریں جو تنظیم بھر میں پرامپٹ ٹیمپلیٹس کو منظم، ورژننگ، اور تعینات کرے۔

**ضروریات:**

- پرامپٹ ٹیمپلیٹس کے لیے ایک مرکزی ذخیرہ بنائیں
- ورژننگ اور منظوری کے ورک فلو نافذ کریں
- نمونہ ان پٹس کے ساتھ ٹیمپلیٹ ٹیسٹنگ کی صلاحیتیں بنائیں
- رول پر مبنی رسائی کنٹرول تیار کریں
- ٹیمپلیٹ بازیافت اور تعیناتی کے لیے API بنائیں

**عمل درآمد کے مراحل:**

1. ٹیمپلیٹ اسٹوریج کے لیے ڈیٹا بیس اسکیمہ ڈیزائن کریں
2. ٹیمپلیٹ CRUD آپریشنز کے لیے بنیادی API بنائیں
3. ورژننگ سسٹم نافذ کریں
4. منظوری کے ورک فلو کو تیار کریں
5. ٹیسٹنگ فریم ورک تیار کریں
6. انتظام کے لیے ایک سادہ ویب انٹرفیس بنائیں
7. MCP سرور کے ساتھ انضمام کریں

**ٹیکنالوجیز:** بیک اینڈ فریم ورک، SQL یا NoSQL ڈیٹا بیس، اور فرنٹ اینڈ فریم ورک آپ کی پسند کے مطابق۔

### منصوبہ 3: MCP پر مبنی مواد تخلیق پلیٹ فارم

**مقصد:** ایک مواد تخلیق پلیٹ فارم بنائیں جو مختلف مواد کی اقسام میں مستقل نتائج فراہم کرنے کے لیے MCP کا فائدہ اٹھائے۔

**ضروریات:**

- متعدد مواد فارمیٹس کی حمایت کریں (بلاگ پوسٹس، سوشل میڈیا، مارکیٹنگ کاپی)
- حسب ضرورت اختیارات کے ساتھ ٹیمپلیٹ پر مبنی تخلیق نافذ کریں
- مواد کا جائزہ اور تاثرات کا نظام بنائیں
- مواد کی کارکردگی کے میٹرکس کو ٹریک کریں
- مواد کے ورژننگ اور تکرار کی حمایت کریں

**عمل درآمد کے مراحل:**

1. MCP کلائنٹ انفراسٹرکچر قائم کریں
2. مختلف مواد کی اقسام کے لیے ٹیمپلیٹس بنائیں
3. مواد تخلیق پائپ لائن بنائیں
4. جائزہ نظام نافذ کریں
5. میٹرکس ٹریکنگ سسٹم تیار کریں
6. ٹیمپلیٹ مینجمنٹ اور مواد تخلیق کے لیے صارف انٹرفیس بنائیں

**ٹیکنالوجیز:** آپ کی پسند کی پروگرامنگ زبان، ویب فریم ورک، اور ڈیٹا بیس سسٹم۔

## MCP ٹیکنالوجی کے لیے مستقبل کے رجحانات

### ابھرتے ہوئے رجحانات

1. **ملٹی موڈل MCP**
   - تصویر، آڈیو، اور ویڈیو ماڈلز کے ساتھ تعامل کو معیاری بنانے کے لیے MCP کی توسیع
   - کراس موڈل استدلال کی صلاحیتوں کی ترقی
   - مختلف موڈالٹیز کے لیے معیاری پرامپٹ فارمیٹس

2. **فیڈریٹڈ MCP انفراسٹرکچر**
   - تقسیم شدہ MCP نیٹ ورکس جو تنظیموں کے درمیان وسائل کا اشتراک کر سکتے ہیں
   - محفوظ ماڈل شیئرنگ کے لیے معیاری پروٹوکولز
   - پرائیویسی کو محفوظ رکھنے والی کمپیوٹیشن تکنیکیں

3. **MCP مارکیٹ پلیسز**
   - MCP ٹیمپلیٹس اور پلگ انز کے اشتراک اور منیٹائز کرنے کے لیے ایکو سسٹمز
   - معیار کی یقین دہانی اور سرٹیفیکیشن کے عمل
   - ماڈل مارکیٹ پلیسز کے ساتھ انضمام

4. **ایج کمپیوٹنگ کے لیے MCP**
   - وسائل کی کمی والے ایج ڈیوائسز کے لیے MCP معیارات کی موافقت
   - کم بینڈوڈتھ ماحول کے لیے بہتر پروٹوکولز
   - IoT ایکو سسٹمز کے لیے خصوصی MCP نفاذ

5. **ریگولیٹری فریم ورک**
   - ریگولیٹری تعمیل کے لیے MCP ایکسٹینشنز کی ترقی
   - معیاری آڈٹ ٹریلز اور وضاحت کے انٹرفیس
   - ابھرتے ہوئے AI گورننس فریم ورک کے ساتھ انضمام

### مائیکروسافٹ کی طرف سے MCP حل

مائیکروسافٹ اور Azure نے مختلف منظرناموں میں MCP کو نافذ کرنے میں مدد کے لیے کئی اوپن سورس ریپوزٹریز تیار کی ہیں:

#### مائیکروسافٹ آرگنائزیشن

1. [playwright-mcp](https://github.com/microsoft/playwright-mcp) - براؤزر آٹومیشن اور ٹیسٹنگ کے لیے Playwright MCP سرور
2. [files-mcp-server](https://github.com/microsoft/files-mcp-server) - لوکل ٹیسٹنگ اور کمیونٹی تعاون کے لیے OneDrive MCP سرور نفاذ
3. [NLWeb](https://github.com/microsoft/NlWeb) - NLWeb اوپن پروٹوکولز اور اوپن سورس ٹولز کا مجموعہ ہے، جس کا بنیادی مقصد AI ویب کے لیے ایک بنیاد قائم کرنا ہے

#### Azure-Samples آرگنائزیشن

1. [mcp](https://github.com/Azure-Samples/mcp) - Azure پر متعدد زبانوں کا استعمال کرتے ہوئے MCP سرورز بنانے اور انضمام کے لیے نمونے، ٹولز، اور وسائل کے لنکس
2. [mcp-auth-servers](https://github.com/Azure-Samples/mcp-auth-servers) - موجودہ ماڈل کانٹیکسٹ پروٹوکول وضاحت کے ساتھ تصدیق کا مظاہرہ کرنے والے حوالہ MCP سرورز
3. [remote-mcp-functions](https://github.com/Azure-Samples/remote-mcp-functions) - Azure Functions میں ریموٹ MCP سرور نفاذ کے لیے لینڈنگ پیج، زبان کے مخصوص ریپوزٹریز کے لنکس کے ساتھ
4. [remote-mcp-functions-python](https://github.com/Azure-Samples/remote-mcp-functions-python) - Azure Functions کے ساتھ Python کا استعمال کرتے ہوئے کسٹم ریموٹ MCP سرورز بنانے اور تعینات کرنے کے لیے کوئیک اسٹارٹ ٹیمپلیٹ
5. [remote-mcp-functions-dotnet](https://github.com/Azure-Samples/remote-mcp-functions-dotnet) - Azure Functions کے ساتھ .NET/C# کا استعمال کرتے ہوئے کسٹم ریموٹ MCP سرورز بنانے اور تعینات کرنے کے لیے کوئیک اسٹارٹ ٹیمپلیٹ
6. [remote-mcp-functions-typescript](https://github.com/Azure-Samples/remote-mcp-functions-typescript) - Azure Functions کے ساتھ TypeScript کا استعمال کرتے ہوئے کسٹم ریموٹ MCP سرورز بنانے اور تعینات کرنے کے لیے کوئیک اسٹارٹ ٹیمپلیٹ
7. [remote-mcp-apim-functions-python](https://github.com/Azure-Samples/remote-mcp-apim-functions-python) - Python کا استعمال کرتے ہوئے Azure API Management کو AI Gateway کے طور پر ریموٹ MCP سرورز کے ساتھ انضمام
8. [AI-Gateway](https://github.com/Azure-Samples/AI-Gateway) - APIM ❤️ AI تجربات بشمول MCP صلاحیتیں، Azure OpenAI اور AI Foundry کے ساتھ انضمام

یہ ریپوزٹریز مختلف نفاذ، ٹیمپلیٹس، اور وسائل فراہم کرتی ہیں جو مختلف پروگرامنگ زبانوں اور Azure سروسز کے ساتھ ماڈل کانٹیکسٹ پروٹوکول کے ساتھ کام کرنے کے لیے ہیں۔ یہ بنیادی سرور نفاذ سے لے کر تصدیق، کلاؤڈ تعیناتی، اور انٹرپرائز انضمام کے منظرناموں تک کے استعمال کے معاملات کا احاطہ کرتی ہیں۔

#### MCP وسائل ڈائریکٹری

[MCP وسائل ڈائریکٹری](https://github.com/microsoft/mcp/tree/main/Resources) مائیکروسافٹ کے آفیشل MCP ریپوزٹری میں نمونہ وسائل، پرامپٹ ٹیمپلیٹس، اور ٹول تعریفوں کا ایک منتخب مجموعہ فراہم کرتی ہے جو ماڈل کانٹیکسٹ پروٹوکول سرورز کے ساتھ استعمال کے لیے ہیں۔ یہ ڈائریکٹری ڈویلپرز کو MCP کے ساتھ جلدی شروع کرنے میں مدد دینے کے لیے دوبارہ قابل استعمال بلڈنگ بلاکس اور بہترین عملی مثالیں پیش کرتی ہے:

- **پرامپٹ ٹیمپلیٹس:** عام AI کاموں اور منظرناموں کے لیے تیار استعمال پرامپٹ ٹیمپلیٹس، جنہیں آپ کے اپنے MCP سرور نفاذ کے لیے اپنایا جا سکتا ہے۔
- **ٹول تعریفیں:** مختلف MCP سرورز کے درمیان ٹول انضمام اور کال کو معیاری بنانے کے لیے مثال ٹول اسکیمہ اور میٹا ڈیٹا۔
- **وسائل کے نمونے:** MCP فریم ورک کے اندر ڈیٹا ذرائع، APIs، اور بیرونی سروسز سے جڑنے کے لیے مثال وسائل کی تعریفیں۔
- **حوالہ نفاذ:** عملی نمونے جو حقیقی دنیا کے MCP منصوبوں میں وسائل، پرامپٹس، اور ٹولز کو کیسے ترتیب دیں اور منظم کریں دکھاتے ہیں۔

یہ وسائل ترقی کو تیز کرتے ہیں، معیاری بنانے کو فروغ دیتے ہیں، اور MCP پر مبنی حل تیار کرنے اور تعینات کرنے میں بہترین طریقوں کو یقینی بنانے میں مدد کرتے ہیں۔

#### MCP وسائل ڈائریکٹری

- [MCP وسائل (نمونہ پرامپٹس، ٹولز، اور وسائل کی تعریفیں)](https://github.com/microsoft/mcp/tree/main/Resources)

### تحقیق کے مواقع

- MCP فریم ورک کے اندر مؤثر پرامپٹ آپٹیمائزیشن تکنیک
- ملٹی ٹیننٹ MCP تعیناتیوں کے لیے سیکیورٹی ماڈلز
- مختلف MCP نفاذ کے درمیان کارکردگی کا بینچ مارکنگ
- MCP سرورز کے لیے رسمی تصدیق کے طریقے

## نتیجہ

ماڈل کانٹیکسٹ پروٹوکول (MCP) صنعتوں میں معیاری، محفوظ، اور انٹرآپریبل AI انضمام کے مستقبل کو تیزی سے تشکیل دے رہا ہے۔ اس سبق میں کیس اسٹڈیز اور عملی منصوبوں کے ذریعے، آپ نے دیکھا کہ ابتدائی اپنانے والے—بشمول مائیکروسافٹ اور Azure—MCP کو حقیقی دنیا کے چیلنجز حل کرنے، AI اپنانے کو تیز کرنے، اور تعمیل، سیکیورٹی، اور اسکیل ایبلٹی کو یقینی بنانے کے لیے کیسے استعمال کر رہے ہیں۔ MCP کا ماڈیولر نقطہ نظر تنظیموں کو بڑے زبان کے ماڈلز، ٹولز، اور انٹرپرائز ڈیٹا کو ایک متحد، آڈٹ ایبل فریم ورک میں جوڑنے کے قابل بناتا ہے۔ جیسے جیسے MCP ترقی کرتا ہے، کمیونٹی کے ساتھ مشغول رہنا، اوپن سورس وسائل کو دریافت کرنا، اور بہترین طریقوں کو اپنانا مضبوط، مستقبل کے لیے تیار AI حل بنانے کی کلید ہوگی۔

## اضافی وسائل

- [MCP Foundry GitHub Repository](https://github.com/azure-ai-foundry/mcp-foundry)
- [Foundry MCP Playground](https://github.com/azure-ai-foundry/foundry-mcp-playground)
- [Integrating Azure AI Agents with MCP (Microsoft Foundry Blog)](https://devblogs.microsoft.com/foundry/integrating-azure-ai-agents-mcp/)
- [MCP GitHub Repository (Microsoft)](https://github.com/microsoft/mcp)
- [MCP Resources Directory (Sample Prompts, Tools, and Resource Definitions)](https://github.com/microsoft/mcp/tree/main/Resources)
- [MCP Community & Documentation](https://modelcontextprotocol.io/introduction)
- [Azure MCP Documentation](https://aka.ms/azmcp)
- [Playwright MCP Server GitHub Repository](https://github.com/microsoft/playwright-mcp)
- [Files MCP Server (OneDrive)](https://github.com/microsoft/files-mcp-server)
- [Azure-Samples MCP](https://github.com/Azure-Samples/mcp)
- [MCP Auth Servers (Azure-Samples)](https://github.com/Azure-Samples/mcp-auth-servers)
- [Remote MCP Functions (Azure-Samples)](https://github.com/Azure-Samples/remote-mcp-functions)
- [Remote MCP Functions Python (Azure-Samples)](https://github.com/Azure-Samples/remote-mcp-functions-python)
- [Remote MCP Functions .NET (Azure-Samples)](https://github.com/Azure-Samples/remote-mcp-functions-dotnet)
- [Remote MCP Functions TypeScript (Azure-Samples)](https://github.com/Azure-Samples/remote-mcp-functions-typescript)
- [Remote MCP APIM Functions Python (Azure-Samples)](https://github.com/Azure-Samples/remote-mcp-apim-functions-python)
- [AI-Gateway (Azure-Samples)](https://github.com/Azure-Samples/AI-Gateway)
- [Microsoft AI and Automation Solutions](https://azure.microsoft.com/en-us/products/ai-services/)

## مشقیں

1. کسی ایک کیس اسٹڈی کا تجزیہ کریں اور متبادل نفاذ کا طریقہ تجویز کریں۔
2. کسی ایک منصوبے کے خیال کا انتخاب کریں اور تفصیلی تکنیکی وضاحت تیار کریں۔
3. کسی ایسی صنعت پر تحقیق کریں جو کیس اسٹڈیز میں شامل نہیں ہے اور اس کے مخصوص چیلنجز کو حل کرنے کے لیے MCP کا خاکہ پیش کریں۔
4. مستقبل کے رجحانات میں سے کسی ایک کو دریافت کریں اور اسے سپورٹ کرنے کے لیے ایک نئے MCP ایکسٹینشن کا تصور تیار کریں۔

اگلا: [Microsoft MCP Server](../07-LessonsfromEarlyAdoption/microsoft-mcp-servers.md)

**ڈس کلیمر**:  
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کا استعمال کرتے ہوئے ترجمہ کی گئی ہے۔ ہم درستگی کے لیے کوشش کرتے ہیں، لیکن براہ کرم آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا خامیاں ہو سکتی ہیں۔ اصل دستاویز کو اس کی اصل زبان میں مستند ذریعہ سمجھا جانا چاہیے۔ اہم معلومات کے لیے، پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کے لیے ہم ذمہ دار نہیں ہیں۔