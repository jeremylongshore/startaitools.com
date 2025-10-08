<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "41f16dac486d2086a53bc644a01cbe42",
  "translation_date": "2025-08-19T16:51:18+00:00",
  "source_file": "07-LessonsfromEarlyAdoption/README.md",
  "language_code": "bg"
}
-->
# 🌟 Уроци от ранните потребители

[![Уроци от ранните потребители на MCP](../../../translated_images/08.980bb2babbaadd8a97739effc9b31e5f1abd8f4c4a3fbc90fb9f931a866674d0.bg.png)](https://youtu.be/jds7dSmNptE)

_(Кликнете върху изображението по-горе, за да гледате видеото към този урок)_

## 🎯 Какво обхваща този модул

Този модул разглежда как реални организации и разработчици използват Model Context Protocol (MCP), за да решават практически предизвикателства и да стимулират иновации. Чрез подробни казуси и практически примери ще откриете как MCP позволява сигурна и мащабируема интеграция на изкуствен интелект, която свързва езикови модели, инструменти и корпоративни данни.

### 📚 Вижте MCP в действие

Искате да видите как тези принципи се прилагат в готови за производство инструменти? Разгледайте нашето [**Ръководство за 10 Microsoft MCP сървъра, които трансформират продуктивността на разработчиците**](microsoft-mcp-servers.md), което представя реални Microsoft MCP сървъри, които можете да използвате още днес.

## Преглед

Този урок изследва как ранните потребители са използвали Model Context Protocol (MCP), за да решават реални предизвикателства и да стимулират иновации в различни индустрии. Чрез подробни казуси и практически проекти ще видите как MCP позволява стандартизирана, сигурна и мащабируема интеграция на изкуствен интелект—свързвайки големи езикови модели, инструменти и корпоративни данни в единна рамка. Ще придобиете практически опит в проектирането и изграждането на решения, базирани на MCP, ще научите от доказани модели за внедряване и ще откриете най-добрите практики за използване на MCP в производствени среди. Урокът също така подчертава нововъзникващи тенденции, бъдещи насоки и ресурси с отворен код, които ще ви помогнат да останете в крак с развитието на MCP технологията и нейната екосистема.

## Цели на обучението

- Анализирайте реални внедрявания на MCP в различни индустрии
- Проектирайте и изграждайте завършени приложения, базирани на MCP
- Изследвайте нововъзникващи тенденции и бъдещи насоки в MCP технологията
- Прилагайте най-добрите практики в реални сценарии за разработка

## Реални внедрявания на MCP

### Казус 1: Автоматизация на клиентската поддръжка в предприятия

Многонационална корпорация внедри решение, базирано на MCP, за стандартизиране на AI взаимодействията в системите за клиентска поддръжка. Това им позволи да:

- Създадат унифициран интерфейс за множество доставчици на LLM
- Поддържат последователно управление на подканите между отделите
- Въведат надеждни мерки за сигурност и съответствие
- Лесно превключват между различни AI модели според конкретните нужди

**Техническо внедряване:**

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

**Резултати:** 30% намаление на разходите за модели, 45% подобрение в последователността на отговорите и подобрено съответствие в глобалните операции.

### Казус 2: Асистент за диагностика в здравеопазването

Доставчик на здравни услуги разработи инфраструктура MCP за интеграция на множество специализирани медицински AI модели, като същевременно гарантира защита на чувствителните данни на пациентите:

- Безпроблемно превключване между общи и специализирани медицински модели
- Строг контрол на поверителността и одитни следи
- Интеграция със съществуващи системи за електронни здравни досиета (EHR)
- Последователно инженерство на подканите за медицинска терминология

**Техническо внедряване:**

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

**Резултати:** Подобрени диагностични предложения за лекари при пълно съответствие с HIPAA и значително намаляване на контекстното превключване между системите.

### Казус 3: Анализ на риска във финансовите услуги

Финансова институция внедри MCP за стандартизиране на процесите за анализ на риска в различни отдели:

- Създаде унифициран интерфейс за модели за кредитен риск, откриване на измами и инвестиционен риск
- Въведе строги контроли за достъп и версиониране на моделите
- Осигури одитируемост на всички AI препоръки
- Поддържа последователно форматиране на данни в различни системи

**Техническо внедряване:**

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

**Резултати:** Подобрено регулаторно съответствие, 40% по-бързи цикли на внедряване на модели и подобрена последователност в оценката на риска между отделите.

### Казус 4: Microsoft Playwright MCP сървър за автоматизация на браузъри

Microsoft разработи [Playwright MCP сървър](https://github.com/microsoft/playwright-mcp), за да позволи сигурна и стандартизирана автоматизация на браузъри чрез Model Context Protocol. Този готов за производство сървър позволява на AI агенти и LLM да взаимодействат с уеб браузъри по контролиран, одитируем и разширяем начин—позволявайки случаи на употреба като автоматизирано тестване на уеб, извличане на данни и крайни работни потоци.

> **🎯 Готов за производство инструмент**
> 
> Този казус представя реален MCP сървър, който можете да използвате още днес! Научете повече за Playwright MCP сървъра и още 9 готови за производство Microsoft MCP сървъра в нашето [**Ръководство за Microsoft MCP сървъри**](microsoft-mcp-servers.md#8--playwright-mcp-server).

**Ключови характеристики:**
- Предоставя възможности за автоматизация на браузъри (навигация, попълване на формуляри, заснемане на екрани и др.) като MCP инструменти
- Въвежда строги контроли за достъп и изолиране, за да предотврати неоторизирани действия
- Осигурява подробни одитни дневници за всички взаимодействия с браузъра
- Поддържа интеграция с Azure OpenAI и други доставчици на LLM за автоматизация, управлявана от агенти
- Захранва възможностите за уеб браузване на GitHub Copilot

**Техническо внедряване:**

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

**Резултати:**

- Позволи сигурна, програмируема автоматизация на браузъри за AI агенти и LLM
- Намали ръчните усилия за тестване и подобри покритието на тестовете за уеб приложения
- Осигури повторно използваема, разширяема рамка за интеграция на инструменти, базирани на браузъри, в корпоративни среди
- Захранва възможностите за уеб браузване на GitHub Copilot

**Референции:**

- [Playwright MCP Server GitHub Repository](https://github.com/microsoft/playwright-mcp)
- [Microsoft AI and Automation Solutions](https://azure.microsoft.com/en-us/products/ai-services/)

### Казус 5: Azure MCP – Model Context Protocol като услуга от корпоративен клас

Azure MCP Server ([https://aka.ms/azmcp](https://aka.ms/azmcp)) е управляваното от Microsoft внедряване на Model Context Protocol от корпоративен клас, проектирано да предоставя мащабируеми, сигурни и съвместими MCP сървърни възможности като облачна услуга. Azure MCP позволява на организациите бързо да внедряват, управляват и интегрират MCP сървъри с Azure AI, данни и услуги за сигурност, намалявайки оперативните разходи и ускорявайки приемането на AI.

> **🎯 Готов за производство инструмент**
> 
> Това е реален MCP сървър, който можете да използвате още днес! Научете повече за Azure AI Foundry MCP Server в нашето [**Ръководство за Microsoft MCP сървъри**](microsoft-mcp-servers.md).

- Напълно управляван хостинг на MCP сървъри с вградена мащабируемост, мониторинг и сигурност
- Нативна интеграция с Azure OpenAI, Azure AI Search и други Azure услуги
- Корпоративна автентикация и авторизация чрез Microsoft Entra ID
- Поддръжка за персонализирани инструменти, шаблони за подканяне и конектори за ресурси
- Съответствие с изискванията за корпоративна сигурност и регулации

**Техническо внедряване:**

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

**Резултати:**  
- Намалено време за реализация на проекти с AI чрез предоставяне на готова за използване, съвместима MCP сървърна платформа  
- Оптимизирана интеграция на LLM, инструменти и корпоративни източници на данни  
- Подобрена сигурност, наблюдаемост и оперативна ефективност за MCP натоварвания  
- Подобрено качество на кода с най-добрите практики на Azure SDK и актуални модели за автентикация  

**Референции:**  
- [Azure MCP Documentation](https://aka.ms/azmcp)  
- [Azure MCP Server GitHub Repository](https://github.com/Azure/azure-mcp)  
- [Azure AI Services](https://azure.microsoft.com/en-us/products/ai-services/)  
- [Microsoft MCP Center](https://mcp.azure.com)  

...
> **🎯 Инструмент, готов за производство**  
>  
> Това е истински MCP сървър, който можете да използвате още днес! Научете повече за MCP сървърите на Microsoft Learn Docs в нашето [**Ръководство за MCP сървъри на Microsoft**](microsoft-mcp-servers.md#1--microsoft-learn-docs-mcp-server).
**Основни характеристики:**
- Достъп в реално време до официална документация на Microsoft, Azure и Microsoft 365
- Разширени семантични възможности за търсене, които разбират контекста и намерението
- Винаги актуална информация, публикувана в Microsoft Learn
- Обхватна покривност на Microsoft Learn, документация за Azure и Microsoft 365
- Връща до 10 висококачествени съдържателни части с заглавия на статии и URL адреси

**Защо е важно:**
- Решава проблема с "остаряла AI информация" за технологиите на Microsoft
- Гарантира, че AI асистентите имат достъп до най-новите функции на .NET, C#, Azure и Microsoft 365
- Осигурява авторитетна, първостепенна информация за точно генериране на код
- Критично за разработчици, работещи с бързо развиващи се технологии на Microsoft

**Резултати:**
- Драстично подобрена точност на AI-генерирания код за технологии на Microsoft
- Намалено време за търсене на актуална документация и добри практики
- Повишена продуктивност на разработчиците чрез извличане на документация, съобразена с контекста
- Безпроблемна интеграция с работните процеси на разработка без напускане на IDE

**Референции:**
- [Microsoft Learn Docs MCP Server GitHub Repository](https://github.com/MicrosoftDocs/mcp)
- [Microsoft Learn Documentation](https://learn.microsoft.com/)

## Практически проекти

### Проект 1: Създаване на MCP сървър с множество доставчици

**Цел:** Създайте MCP сървър, който може да насочва заявки към множество доставчици на AI модели въз основа на специфични критерии.

**Изисквания:**

- Поддръжка на поне три различни доставчици на модели (например OpenAI, Anthropic, локални модели)
- Реализиране на механизъм за маршрутизация въз основа на метаданни на заявките
- Създаване на конфигурационна система за управление на идентификационни данни на доставчици
- Добавяне на кеширане за оптимизация на производителността и разходите
- Изграждане на прост табло за наблюдение на използването

**Стъпки за реализация:**

1. Настройте основната инфраструктура на MCP сървъра
2. Реализирайте адаптери за доставчици за всяка AI услуга
3. Създайте логика за маршрутизация въз основа на атрибути на заявките
4. Добавете механизми за кеширане за чести заявки
5. Разработете табло за наблюдение
6. Тествайте с различни модели на заявки

**Технологии:** Изберете между Python (.NET/Java/Python според предпочитанията ви), Redis за кеширане и прост уеб фреймуърк за таблото.

### Проект 2: Система за управление на шаблони за подсказки в предприятието

**Цел:** Разработете система, базирана на MCP, за управление, версиониране и внедряване на шаблони за подсказки в организацията.

**Изисквания:**

- Създаване на централизирано хранилище за шаблони за подсказки
- Реализиране на системи за версиониране и одобрение
- Изграждане на възможности за тестване на шаблони със примерни входни данни
- Разработване на контрол на достъпа, базиран на роли
- Създаване на API за извличане и внедряване на шаблони

**Стъпки за реализация:**

1. Проектирайте схемата на базата данни за съхранение на шаблони
2. Създайте основния API за CRUD операции на шаблони
3. Реализирайте система за версиониране
4. Изградете работен процес за одобрение
5. Разработете рамка за тестване
6. Създайте прост уеб интерфейс за управление
7. Интегрирайте с MCP сървър

**Технологии:** Ваш избор на бекенд фреймуърк, SQL или NoSQL база данни и фронтенд фреймуърк за интерфейса за управление.

### Проект 3: Платформа за генериране на съдържание, базирана на MCP

**Цел:** Създайте платформа за генериране на съдържание, която използва MCP за предоставяне на последователни резултати за различни типове съдържание.

**Изисквания:**

- Поддръжка на множество формати на съдържание (блог постове, социални медии, маркетингови текстове)
- Реализиране на генериране, базирано на шаблони, с опции за персонализация
- Създаване на система за преглед и обратна връзка за съдържание
- Проследяване на метрики за ефективност на съдържанието
- Поддръжка на версиониране и итерация на съдържание

**Стъпки за реализация:**

1. Настройте инфраструктурата на MCP клиента
2. Създайте шаблони за различни типове съдържание
3. Изградете тръбопровод за генериране на съдържание
4. Реализирайте система за преглед
5. Разработете система за проследяване на метрики
6. Създайте потребителски интерфейс за управление на шаблони и генериране на съдържание

**Технологии:** Ваш предпочитан програмен език, уеб фреймуърк и система за база данни.

## Бъдещи насоки за MCP технология

### Нови тенденции

1. **Мултимодален MCP**
   - Разширяване на MCP за стандартизиране на взаимодействията с модели за изображения, аудио и видео
   - Разработване на способности за кръстомодално разсъждение
   - Стандартизирани формати за подсказки за различни модалности

2. **Федеративна MCP инфраструктура**
   - Разпределени MCP мрежи, които могат да споделят ресурси между организации
   - Стандартизирани протоколи за сигурно споделяне на модели
   - Техники за запазване на поверителността при изчисления

3. **MCP пазари**
   - Екосистеми за споделяне и монетизиране на MCP шаблони и плъгини
   - Процеси за осигуряване на качество и сертификация
   - Интеграция с пазари за модели

4. **MCP за Edge Computing**
   - Адаптиране на MCP стандартите за устройства с ограничени ресурси
   - Оптимизирани протоколи за среди с ниска честотна лента
   - Специализирани MCP реализации за IoT екосистеми

5. **Регулаторни рамки**
   - Разработване на MCP разширения за съответствие с регулации
   - Стандартизирани следи за одит и интерфейси за обяснение
   - Интеграция с нововъзникващи рамки за управление на AI

### MCP решения от Microsoft

Microsoft и Azure са разработили няколко отворени хранилища, които помагат на разработчиците да внедрят MCP в различни сценарии:

#### Microsoft организация

1. [playwright-mcp](https://github.com/microsoft/playwright-mcp) - Playwright MCP сървър за автоматизация и тестване на браузъри
2. [files-mcp-server](https://github.com/microsoft/files-mcp-server) - OneDrive MCP сървър за локално тестване и принос от общността
3. [NLWeb](https://github.com/microsoft/NlWeb) - NLWeb е колекция от отворени протоколи и свързани инструменти с отворен код. Основният му фокус е създаването на основен слой за AI Web

#### Azure-Samples организация

1. [mcp](https://github.com/Azure-Samples/mcp) - Връзки към примери, инструменти и ресурси за изграждане и интеграция на MCP сървъри в Azure с множество езици
2. [mcp-auth-servers](https://github.com/Azure-Samples/mcp-auth-servers) - Референтни MCP сървъри, демонстриращи автентикация с текущата спецификация на Model Context Protocol
3. [remote-mcp-functions](https://github.com/Azure-Samples/remote-mcp-functions) - Страница за Remote MCP сървър реализации в Azure Functions с връзки към езиково-специфични хранилища
4. [remote-mcp-functions-python](https://github.com/Azure-Samples/remote-mcp-functions-python) - Шаблон за бърз старт за изграждане и внедряване на персонализирани Remote MCP сървъри с Azure Functions и Python
5. [remote-mcp-functions-dotnet](https://github.com/Azure-Samples/remote-mcp-functions-dotnet) - Шаблон за бърз старт за изграждане и внедряване на персонализирани Remote MCP сървъри с Azure Functions и .NET/C#
6. [remote-mcp-functions-typescript](https://github.com/Azure-Samples/remote-mcp-functions-typescript) - Шаблон за бърз старт за изграждане и внедряване на персонализирани Remote MCP сървъри с Azure Functions и TypeScript
7. [remote-mcp-apim-functions-python](https://github.com/Azure-Samples/remote-mcp-apim-functions-python) - Azure API Management като AI Gateway към Remote MCP сървъри с Python
8. [AI-Gateway](https://github.com/Azure-Samples/AI-Gateway) - Експерименти с APIM ❤️ AI, включително MCP възможности, интеграция с Azure OpenAI и AI Foundry

Тези хранилища предоставят различни реализации, шаблони и ресурси за работа с Model Context Protocol в различни програмни езици и Azure услуги. Те обхващат редица случаи на употреба от основни реализации на сървъри до автентикация, облачно внедряване и сценарии за интеграция в предприятието.

#### MCP Resources Directory

[Директорията MCP Resources](https://github.com/microsoft/mcp/tree/main/Resources) в официалното хранилище на Microsoft MCP предоставя курирана колекция от примерни ресурси, шаблони за подсказки и дефиниции на инструменти за използване с Model Context Protocol сървъри. Тази директория е предназначена да помогне на разработчиците бързо да започнат работа с MCP, като предлага повторно използваеми градивни блокове и примери за добри практики за:

- **Шаблони за подсказки:** Готови за използване шаблони за подсказки за често срещани AI задачи и сценарии, които могат да бъдат адаптирани за вашите собствени реализации на MCP сървъри.
- **Дефиниции на инструменти:** Примерни схеми на инструменти и метаданни за стандартизиране на интеграцията и извикването на инструменти в различни MCP сървъри.
- **Примерни ресурси:** Примерни дефиниции на ресурси за свързване към източници на данни, API и външни услуги в рамките на MCP.
- **Референтни реализации:** Практически примери, които демонстрират как да структурирате и организирате ресурси, подсказки и инструменти в реални MCP проекти.

Тези ресурси ускоряват разработката, насърчават стандартизацията и помагат за осигуряване на добри практики при изграждането и внедряването на решения, базирани на MCP.

#### MCP Resources Directory

- [MCP Resources (Sample Prompts, Tools, and Resource Definitions)](https://github.com/microsoft/mcp/tree/main/Resources)

### Възможности за изследване

- Ефективни техники за оптимизация на подсказки в рамките на MCP
- Модели за сигурност за многопотребителски MCP внедрения
- Бенчмаркинг на производителността между различни MCP реализации
- Методи за формална проверка на MCP сървъри

## Заключение

Model Context Protocol (MCP) бързо оформя бъдещето на стандартизирана, сигурна и съвместима AI интеграция в различни индустрии. Чрез казусите и практическите проекти в този урок видяхте как ранните потребители—включително Microsoft и Azure—използват MCP за решаване на реални предизвикателства, ускоряване на AI внедряването и осигуряване на съответствие, сигурност и мащабируемост. Модулният подход на MCP позволява на организациите да свързват големи езикови модели, инструменти и корпоративни данни в единна, проверима рамка. Докато MCP продължава да се развива, ангажирането с общността, изследването на ресурси с отворен код и прилагането на добри практики ще бъдат ключови за изграждането на устойчиви, готови за бъдещето AI решения.

## Допълнителни ресурси

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

## Упражнения

1. Анализирайте един от казусите и предложете алтернативен подход за реализация.
2. Изберете една от идеите за проект и създайте подробна техническа спецификация.
3. Изследвайте индустрия, която не е обхваната в казусите, и очертайте как MCP може да реши специфичните ѝ предизвикателства.
4. Разгледайте една от бъдещите насоки и създайте концепция за ново MCP разширение, което да я подкрепи.

Следва: [Microsoft MCP Server](../07-LessonsfromEarlyAdoption/microsoft-mcp-servers.md)

**Отказ от отговорност**:  
Този документ е преведен с помощта на AI услуга за превод [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля, имайте предвид, че автоматизираните преводи може да съдържат грешки или неточности. Оригиналният документ на неговия изходен език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Не носим отговорност за каквито и да е недоразумения или погрешни интерпретации, произтичащи от използването на този превод.