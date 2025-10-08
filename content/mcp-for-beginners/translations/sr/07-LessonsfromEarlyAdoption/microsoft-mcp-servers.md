<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c8f283730b5421082ddd26cc85c07831",
  "translation_date": "2025-07-18T12:09:55+00:00",
  "source_file": "07-LessonsfromEarlyAdoption/microsoft-mcp-servers.md",
  "language_code": "sr"
}
-->
# 🚀 10 Microsoft MCP сервера који трансформишу продуктивност програмера

## 🎯 Шта ћете научити у овом водичу

Овај практични водич представља десет Microsoft MCP сервера који активно мењају начин на који програмери раде са AI асистентима. Уместо да само објашњавамо шта MCP сервери *могу* да ураде, показаћемо вам сервере који већ праве стварну разлику у свакодневним развојним процесима у Microsoft-у и шире.

Сваки сервер у овом водичу изабран је на основу стварне употребе и повратних информација програмера. Открићете не само шта сваки сервер ради, већ и зашто је важан и како да га најбоље искористите у својим пројектима. Без обзира да ли сте потпуно нови у MCP-у или желите да проширите своју постојећу конфигурацију, ови сервери представљају неке од најпрактичнијих и најкориснијих алата у Microsoft екосистему.

> **💡 Брзи савет за почетак**
> 
> Нови сте у MCP-у? Не брините! Овај водич је прилагођен почетницима. Објаснићемо појмове како идемо, а увек можете да се вратите на наше модуле [Увод у MCP](../00-Introduction/README.md) и [Основни појмови](../01-CoreConcepts/README.md) за детаљније информације.

## Преглед

Овај свеобухватни водич истражује десет Microsoft MCP сервера који револуционишу начин на који програмери комуницирају са AI асистентима и спољним алатима. Од управљања Azure ресурсима до обраде докумената, ови сервери показују снагу Model Context Protocol-а у креирању беспрекорних и продуктивних развојних токова рада.

## Циљеви учења

До краја овог водича ћете:
- Разумети како MCP сервери повећавају продуктивност програмера
- Упознати се са најзначајнијим Microsoft MCP сервер имплементацијама
- Открити практичне примере коришћења сваког сервера
- Знати како да подесите и конфигуришете ове сервере у VS Code и Visual Studio-у
- Истражити шири MCP екосистем и будуће правце развоја

## 🔧 Разумевање MCP сервера: Водич за почетнике

### Шта су MCP сервери?

Као почетник у Model Context Protocol-у (MCP), можда се питате: „Шта је MCP сервер и зашто ми је то важно?“ Почнимо једноставном аналогом.

Замислите MCP сервере као специјализоване помоћнике који вашем AI кодирајућем сапутнику (као што је GitHub Copilot) омогућавају повезивање са спољним алатима и сервисима. Баш као што користите различите апликације на телефону за различите задатке — једну за време, другу за навигацију, трећу за банкарство — MCP сервери дају вашем AI асистенту могућност да комуницира са различитим развојним алатима и сервисима.

### Проблем који MCP сервери решавају

Пре MCP сервера, ако сте хтели да:
- Проверите своје Azure ресурсе
- Креирате GitHub issue
- Питате базу података
- Претражите документацију

Морали сте да прекинете кодирање, отворите прегледач, одете на одговарајући сајт и ручно обавите те задатке. Овај стални прелазак између контекста ремети ваш ток рада и смањује продуктивност.

### Како MCP сервери трансформишу ваше искуство развоја

Са MCP серверима, можете остати у свом развојном окружењу (VS Code, Visual Studio и сл.) и једноставно замолити свог AI асистента да обави те задатке. На пример:

**Уместо овог традиционалног тока рада:**
1. Прекини кодирање
2. Отвори прегледач
3. Иди на Azure портал
4. Потражи детаље о складишном налогу
5. Врати се у VS Code
6. Настави са кодирањем

**Сада можете ово:**
1. Питај AI: „Који је статус мојих Azure складишних налога?“
2. Настави са кодирањем са добијеним информацијама

### Кључне предности за почетнике

#### 1. 🔄 **Останите у свом току рада**
- Нема више пребацивања између више апликација
- Фокусирајте се на код који пишете
- Смањите ментални напор управљања различитим алатима

#### 2. 🤖 **Користите природан језик уместо сложених команди**
- Уместо да памтите SQL синтаксу, опишите које податке желите
- Уместо да памтите Azure CLI команде, објасните шта желите да постигнете
- Нека AI решава техничке детаље док ви размишљате о логици

#### 3. 🔗 **Повежите више алата заједно**
- Креирајте моћне токове рада комбинујући различите сервисе
- Пример: „Добиј све нове GitHub issue-је и направи одговарајуће Azure DevOps радне ставке“
- Аутоматизујте без писања сложених скрипти

#### 4. 🌐 **Приступајте растућем екосистему**
- Искористите сервере које су направили Microsoft, GitHub и друге компаније
- Комбинујте алате различитих добављача без проблема
- Придружите се стандардизованом екосистему који ради са различитим AI асистентима

#### 5. 🛠️ **Учите кроз праксу**
- Почните са унапред направљеним серверима да разумете концепте
- Постепено градите своје сервере како будете стицали више искуства
- Користите доступне SDK-ове и документацију као водич

### Пример из стварног света за почетнике

Рецимо да сте нови у веб развоју и радите на свом првом пројекту. Ево како MCP сервери могу помоћи:

**Традиционални приступ:**
```
1. Code a feature
2. Open browser → Navigate to GitHub
3. Create an issue for testing
4. Open another tab → Check Azure docs for deployment
5. Open third tab → Look up database connection examples
6. Return to VS Code
7. Try to remember what you were doing
```

**Са MCP серверима:**
```
1. Code a feature
2. Ask AI: "Create a GitHub issue for testing this login feature"
3. Ask AI: "How do I deploy this to Azure according to the docs?"
4. Ask AI: "Show me the best way to connect to my database"
5. Continue coding with all the information you need
```

### Предност стандарда за предузећа

MCP постаје индустријски стандард, што значи:
- **Конзистентност**: Слично искуство на различитим алатима и код различитих компанија
- **Интероперабилност**: Сервери различитих добављача раде заједно
- **Припрема за будућност**: Вештине и конфигурације се преносе између различитих AI асистената
- **Заједница**: Велики екосистем заједничког знања и ресурса

### Почетак рада: Шта ћете научити

У овом водичу истражићемо 10 Microsoft MCP сервера који су посебно корисни програмерима свих нивоа. Сваки сервер је дизајниран да:
- Решава уобичајене изазове у развоју
- Смањи понављајуће задатке
- Побољша квалитет кода
- Повећа могућности учења

> **💡 Савет за учење**
> 
> Ако сте потпуно нови у MCP-у, почните са нашим модулима [Увод у MCP](../00-Introduction/README.md) и [Основни појмови](../01-CoreConcepts/README.md). Затим се вратите овде да видите како се ти концепти примењују у пракси са стварним Microsoft алатима.
>
> За додатни контекст о значају MCP-а, погледајте пост Марије Наггага: [Connect Once, Integrate Anywhere with MCP](https://devblogs.microsoft.com/blog/connect-once-integrate-anywhere-with-mcps).

## Почетак рада са MCP у VS Code и Visual Studio-у 🚀

Подешавање ових MCP сервера је једноставно ако користите Visual Studio Code или Visual Studio 2022 са GitHub Copilot-ом.

### Подешавање у VS Code-у

Основни процес за VS Code:

1. **Омогућите Agent Mode**: У VS Code-у пребаците се на Agent mode у Copilot Chat прозору
2. **Конфигуришите MCP сервере**: Додајте конфигурације сервера у ваш settings.json фајл
3. **Покрените сервере**: Кликните на дугме „Start“ за сваки сервер који желите да користите
4. **Изаберите алате**: Одаберите које MCP сервере желите да омогућите у тренутној сесији

За детаљна упутства о подешавању, погледајте [VS Code MCP документацију](https://code.visualstudio.com/docs/copilot/copilot-mcp).

> **💡 Професионални савет: Управљајте MCP серверима као стручњак!**
> 
> Преглед екстензија у VS Code-у сада укључује [практичан нови интерфејс за управљање инсталираним MCP серверима](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode)! Имаш брз приступ за покретање, заустављање и управљање било којим MCP сервером преко јасног и једноставног интерфејса. Испробајте!

### Подешавање у Visual Studio 2022

За Visual Studio 2022 (верзија 17.14 или новија):

1. **Омогућите Agent Mode**: Кликните на „Ask“ падајући мени у GitHub Copilot Chat прозору и изаберите „Agent“
2. **Креирајте конфигурациони фајл**: Направите `.mcp.json` фајл у директоријуму решења (препоручена локација: `<SOLUTIONDIR>\.mcp.json`)
3. **Конфигуришите сервере**: Додајте конфигурације MCP сервера користећи стандардни MCP формат
4. **Одобрење алата**: Када се затражи, одобрите алате које желите да користите са одговарајућим дозволама

За детаљна упутства о подешавању у Visual Studio-у, погледајте [Visual Studio MCP документацију](https://learn.microsoft.com/visualstudio/ide/mcp-servers).

Сваки MCP сервер има своје захтеве за конфигурацију (конекцијске низове, аутентификацију итд.), али образац подешавања је сличан у оба IDE-а.

## Учење из Microsoft MCP сервера 🛠️

### 1. 📚 Microsoft Learn Docs MCP сервер

[![Инсталирај у VS Code](https://img.shields.io/badge/VS_Code-Install_Microsoft_Docs_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D) [![Инсталирај у VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Microsoft_Docs_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**Шта ради**: Microsoft Learn Docs MCP сервер је сервис у облаку који омогућава AI асистентима приступ званичној Microsoft документацији у реалном времену преко Model Context Protocol-а. Повезује се на `https://learn.microsoft.com/api/mcp` и омогућава семантичко претраживање кроз Microsoft Learn, Azure документацију, Microsoft 365 документацију и друге званичне Microsoft изворе.

**Зашто је користан**: Иако може изгледати као „само документација“, овај сервер је кључан за сваког програмера који користи Microsoft технологије. Једна од најчешћих примедби .NET програмера на AI кодирајуће асистенте је да нису у току са најновијим .NET и C# издањима. Microsoft Learn Docs MCP сервер то решава тако што пружа приступ најсвежијој документацији, API референцама и најбољим праксама у реалном времену. Без обзира да ли радите са најновијим Azure SDK-овима, истражујете нове C# 13 функције или имплементирате најсавременије .NET Aspire шаблоне, овај сервер осигурава да ваш AI асистент има приступ ауторитетним и ажурним информацијама потребним за генерисање тачног и модерног кода.

**Примена у пракси**: „Које су az cli команде за креирање Azure container апликације према званичној Microsoft Learn документацији?“ или „Како да конфигуришем Entity Framework са dependency injection у ASP.NET Core?“ Или „Прегледај овај код да провериш да ли одговара препорукама за перформансе из Microsoft Learn документације.“ Сервер пружа свеобухватно покриће Microsoft Learn, Azure и Microsoft 365 документације користећи напредно семантичко претраживање да пронађе најрелевантније информације у контексту. Враћа до 10 висококвалитетних делова садржаја са насловима чланака и URL адресама, увек приступајући најновијој Microsoft документацији чим је објављена.

**Илустративни пример**: Сервер излаже алат `microsoft_docs_search` који изводи семантичко претраживање званичне Microsoft техничке документације. Када је конфигурисан, можете постављати питања као што су „Како да имплементирам JWT аутентификацију у ASP.NET Core?“ и добијати детаљне, званичне одговоре са линковима ка изворима. Квалитет претраге је изузетан јер разуме контекст – питање о „контейнерима“ у Azure контексту враћа документацију о Azure Container Instances, док исти термин у .NET контексту враћа релевантне информације о C# колекцијама.

Ово је посебно корисно за брзо мењајуће или недавно ажуриране библиотеке и случајеве коришћења. На пример, у неким недавним пројектима желео сам да искористим функције из најновијих издања .NET Aspire и Microsoft.Extensions.AI. Укључивањем Microsoft Learn Docs MCP сервера, могао сам да користим не само API документацију, већ и водиче и упутства која су тек објављена.
> **💡 Koristan savet**
> 
> Čak i modeli prilagođeni alatima treba da budu podstaknuti da koriste MCP alate! Razmislite o dodavanju sistemske poruke ili [copilot-instructions.md](https://docs.github.com/copilot/how-tos/custom-instructions/adding-repository-custom-instructions-for-github-copilot) poput: "Imaš pristup `microsoft.docs.mcp` – koristi ovaj alat za pretragu najnovije zvanične Microsoft dokumentacije kada rešavaš pitanja vezana za Microsoft tehnologije kao što su C#, Azure, ASP.NET Core ili Entity Framework."
>
> Za odličan primer kako ovo funkcioniše, pogledaj [C# .NET Janitor chat mode](https://github.com/awesome-copilot/chatmodes/blob/main/csharp-dotnet-janitor.chatmode.md) iz Awesome GitHub Copilot repozitorijuma. Ovaj režim posebno koristi Microsoft Learn Docs MCP server da pomogne u čišćenju i modernizaciji C# koda koristeći najnovije obrasce i najbolje prakse.
### 2. ☁️ Azure MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**Шта ради**: Azure MCP Server је свеобухватан скуп од преко 15 специјализованих конектора за Azure сервисе који уносе цео Azure екосистем у ваш AI радни ток. Ово није само један сервер – то је моћна колекција која укључује управљање ресурсима, повезивање са базама података (PostgreSQL, SQL Server), анализу логова Azure Monitor-а помоћу KQL-а, интеграцију са Cosmos DB и још много тога.

**Зашто је користан**: Поред управљања Azure ресурсима, овај сервер значајно побољшава квалитет кода када радите са Azure SDK-овима. Када користите Azure MCP у Agent режиму, он вам не помаже само да пишете код – помаже вам да пишете *бољи* Azure код који прати актуелне обрасце аутентификације, најбоље праксе за руковање грешкама и користи најновије функције SDK-а. Уместо да добијете општи код који можда ради, добијате код који прати препоручене Azure обрасце за продукцијске радне задатке.

**Кључни модули укључују**:
- **🗄️ Конектори за базе података**: Директан приступ Azure Database за PostgreSQL и SQL Server на природном језику
- **📊 Azure Monitor**: Анализа логова и оперативни увиди покретани KQL-ом
- **🌐 Управљање ресурсима**: Потпуна контрола животног циклуса Azure ресурса
- **🔐 Аутентификација**: Обрасци DefaultAzureCredential и managed identity
- **📦 Сервис складиштења**: Операције над Blob Storage, Queue Storage и Table Storage
- **🚀 Сервис контејнера**: Управљање Azure Container Apps, Container Instances и AKS
- **И још много специјализованих конектора**

**Примена у пракси**: „Наброј ми моје Azure storage налоге“, „Питај мој Log Analytics workspace за грешке у последњем сату“ или „Помози ми да направим Azure апликацију користећи Node.js са исправном аутентификацијом“

**Цео демонстрациони сценарио**: Ево комплетног прегледа који показује снагу комбиновања Azure MCP-а са GitHub Copilot for Azure екстензијом у VS Code-у. Када имате оба инсталирана и унесете:

> „Направи Python скрипту која отпрема фајл у Azure Blob Storage користећи DefaultAzureCredential аутентификацију. Скрипта треба да се повеже на мој Azure storage налог под именом 'mycompanystorage', отпреми у контејнер 'documents', креира тест фајл са тренутним временским печатом за отпремање, лепо обради грешке и пружи информативан излаз, прати најбоље Azure праксе за аутентификацију и руковање грешкама, укључи коментаре који објашњавају како DefaultAzureCredential аутентификација функционише и направи скрипту добро структуираном са одговарајућим функцијама и документацијом.“

Azure MCP Server ће генерисати комплетну, продукцијски спремну Python скрипту која:
- Користи најновији Azure Blob Storage SDK са исправним async обрасцима
- Имплементира DefaultAzureCredential са детаљним објашњењем fallback ланца
- Укључује робусно руковање грешкама са специфичним Azure типовима изузетака
- Прати најбоље праксе Azure SDK-а за управљање ресурсима и везама
- Пружа детаљно логовање и информативан излаз у конзоли
- Креира правилно структуирану скрипту са функцијама, документацијом и типским наговештајима

Оно што је посебно је да без Azure MCP-а можда добијете општи код за blob storage који ради, али не прати актуелне Azure обрасце. Са Azure MCP-ом добијате код који користи најновије методе аутентификације, обрађује Azure-специфичне грешке и прати Microsoft-ове препоруке за продукцијске апликације.

**Илустративни пример**: Често ми је тешко да се сетим специфичних команди за `az` и `azd` CLI алате за повремено коришћење. За мене је то увек двостепени процес: прво потражим синтаксу, па онда извршим команду. Често само уђем у портал и кликам да завршим посао јер не желим да признам да не могу да се сетим CLI синтаксе. Могућност да једноставно опишем шта желим је невероватна, а још боље је што то могу да урадим без напуштања IDE-а!

Постоји одлична листа примера употребе у [Azure MCP репозиторијуму](https://github.com/Azure/azure-mcp?tab=readme-ov-file#-what-can-you-do-with-the-azure-mcp-server) која ће вам помоћи да почнете. За детаљне водиче за подешавање и напредне опције конфигурације, погледајте [званичну Azure MCP документацију](https://learn.microsoft.com/azure/developer/azure-mcp-server/).

### 3. 🐙 GitHub MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Server-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/github/github-mcp-server)

**Шта ради**: Званични GitHub MCP Server пружа беспрекорну интеграцију са целим GitHub екосистемом, нудећи и хостовани удаљени приступ и опције локалног покретања преко Docker-а. Ово није само основна операција са репозиторијумима – то је свеобухватан алатски скуп који укључује управљање GitHub Actions, радне токове pull request-ова, праћење проблема, скенирање безбедности, обавештења и напредне могућности аутоматизације.

**Зашто је користан**: Овај сервер мења начин на који комуницирате са GitHub-ом тако што вам доноси пуну платформу директно у развојно окружење. Уместо сталног пребацивања између VS Code-а и GitHub.com за управљање пројектима, преглед кода и праћење CI/CD-а, све то можете обављати преко команди на природном језику док сте фокусирани на свој код.

> **ℹ️ Напомена: Различите врсте 'агената'**
> 
> Не мешајте овај GitHub MCP Server са GitHub Coding Agent-ом (AI агентом коме можете доделити проблеме за аутоматизоване задатке кодирања). GitHub MCP Server ради у Agent режиму VS Code-а и пружа интеграцију са GitHub API-јем, док је GitHub Coding Agent посебна функција која креира pull request-ове када је додељен GitHub проблемима.

**Кључне могућности укључују**:
- **⚙️ GitHub Actions**: Потпуно управљање CI/CD пипелинама, праћење радних токова и руковање артефактима
- **🔀 Pull Requests**: Креирање, преглед, спајање и управљање PR-овима са детаљним праћењем статуса
- **🐛 Issues**: Потпуна контрола животног циклуса проблема, коментарисање, означавање и додељивање
- **🔒 Безбедност**: Упозорења за скенирање кода, детекција тајни и интеграција са Dependabot-ом
- **🔔 Обавештења**: Паметно управљање обавештењима и контролом претплата на репозиторијуме
- **📁 Управљање репозиторијумима**: Операције са фајловима, управљање гранама и администрација репозиторијума
- **👥 Сарадња**: Претрага корисника и организација, управљање тимовима и контролa приступа

**Примена у пракси**: „Направи pull request са моје feature гране“, „Покажи ми све неуспеле CI покрете ове недеље“, „Наброј ми отворена безбедносна упозорења за моје репозиторијуме“ или „Пронађи све проблеме додељене мени у оквиру мојих организација“

**Цео демонстрациони сценарио**: Ево моћног радног тока који показује могућности GitHub MCP Server-а:

> „Морам да се припремим за преглед спринта. Покажи ми све pull request-ове које сам направио ове недеље, провери статус наших CI/CD пипелина, направи резиме безбедносних упозорења која треба да решимо и помогни ми да саставим белешке о издању на основу спојених PR-ова са ознаком 'feature'.“

GitHub MCP Server ће:
- Питање ваше недавне pull request-ове са детаљним информацијама о статусу
- Анализирати покрете радних токова и истакнути све неуспехе или проблеме у перформансама
- Саставити резултате скенирања безбедности и приоритетизовати критична упозорења
- Генерисати свеобухватне белешке о издању извлачењем информација из спојених PR-ова
- Пружити конкретне следеће кораке за планирање спринта и припрему издања

**Илустративни пример**: Веома волим да користим ово за преглед кода. Уместо да скачем између VS Code-а, GitHub обавештења и страница pull request-ова, могу рећи „Покажи ми све PR-ове који чекају мој преглед“ а затим „Додај коментар на PR #123 питајући о руковању грешкама у методу аутентификације.“ Сервер обрађује GitHub API позиве, одржава контекст дискусије и чак ми помаже да саставим конструктивније коментаре за преглед.

**Опције аутентификације**: Сервер подржава и OAuth (гладко у VS Code-у) и Personal Access Tokens, са конфигурисаним алаткама које омогућавају само GitHub функционалност која вам је потребна. Можете га покренути као удаљени хостовани сервис за тренутно подешавање или локално преко Docker-а за потпуну контролу.

> **💡 Савет за професионалце**
> 
> Омогућите само оне алатке које су вам потребне конфигурисањем параметра `--toolsets` у подешавањима MCP сервера да бисте смањили величину контекста и побољшали избор AI алата. На пример, додајте `"--toolsets", "repos,issues,pull_requests,actions"` у аргументе MCP конфигурације за основне развојне радне токове, или користите `"--toolsets", "notifications, security"` ако вам углавном требају GitHub могућности праћења.

### 4. 🔄 Azure DevOps MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_DevOps_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_DevOps_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/azure-devops-mcp)

**Шта ради**: Повезује се са Azure DevOps сервисима за свеобухватно управљање пројектима, праћење радних ставки, управљање build пипелинама и операције са репозиторијумима.

**Зашто је користан**: За тимове који користе Azure DevOps као своју примарну DevOps платформу, овај MCP сервер елиминише потребу за сталним пребацивањем између развојног окружења и Azure DevOps веб интерфејса. Можете управљати радним ставкама, проверавати статус build-ова, претраживати репозиторијуме и обављати задатке управљања пројектом директно преко вашег AI асистента.

**Примена у пракси**: „Покажи ми све активне радне ставке у текућем спринту за пројекат WebApp“, „Направи извештај о грешци за проблем са пријавом који сам управо пронашао“ или „Провери статус наших build пипелина и прикажи ми све недавне неуспехе“

**Илустративни пример**: Лако можете проверити статус текућег спринта вашег тима једноставним упитом као што је „Покажи ми све активне радне ставке у текућем спринту за пројекат WebApp“ или „Направи извештај о грешци за проблем
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_MarkItDown_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_MarkItDown_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/markitdown)

**Шта ради**: MarkItDown је свеобухватан сервер за конверзију докумената који претвара разне формате фајлова у квалитетан Markdown, оптимизован за коришћење у LLM и токовима за анализу текста.

**Зашто је користан**: Неопходан за модерне токове рада са документацијом! MarkItDown подржава широк спектар формата фајлова уз очување важне структуре документа као што су наслови, листе, табеле и линкови. За разлику од једноставних алата за извлачење текста, фокусира се на очување семантичког значења и форматирања које је вредно и за обраду вештачке интелигенције и за лако читање људима.

**Подржани формати фајлова**:
- **Office документи**: PDF, PowerPoint (PPTX), Word (DOCX), Excel (XLSX/XLS)
- **Медијски фајлови**: Слике (са EXIF метаподацима и OCR), Аудио (са EXIF метаподацима и транскрипцијом говора)
- **Веб садржај**: HTML, RSS фидови, YouTube URL-ови, Wikipedia странице
- **Формати података**: CSV, JSON, XML, ZIP фајлови (рекурзивно обрађује садржај)
- **Формати за издаваштво**: EPub, Jupyter нотебоок (.ipynb)
- **Е-пошта**: Outlook поруке (.msg)
- **Напредно**: Интеграција Azure Document Intelligence за побољшану обраду PDF-ова

**Напредне могућности**: MarkItDown подржава описе слика покретане LLM-ом (када је обезбеђен OpenAI клијент), Azure Document Intelligence за напредну обраду PDF-ова, транскрипцију аудио садржаја, као и систем плагина за проширење подршке на додатне формате фајлова.

**Примена у пракси**: „Претвори ову PowerPoint презентацију у Markdown за наш сајт документације“, „Извучи текст из овог PDF-а са исправном структуром наслова“ или „Трансформиши ову Excel табелу у читљиви табеларни формат“

**Илустративан пример**: Да цитирамо [MarkItDown документацију](https://github.com/microsoft/markitdown#why-markdown):

> Markdown је изузетно близу обичном тексту, са минималним ознакама или форматирањем, али ипак пружа начин да се представи важна структура документа. Главни LLM модели, као што је OpenAI GPT-4o, природно „говоре“ Markdown и често га укључују у своје одговоре без посебног подстицаја. Ово указује да су тренирани на огромним количинама текста форматираног у Markdown-у и да га добро разумеју. Као додатна предност, Markdown конвенције су и веома ефикасне у коришћењу токена.

MarkItDown одлично чува структуру документа, што је важно за AI токове рада. На пример, при конверзији PowerPoint презентације, задржава организацију слајдова са одговарајућим насловима, извлачи табеле као Markdown табеле, укључује алтернативни текст за слике и чак обрађује белешке говорника. Графикони се претварају у читљиве табеле података, а добијени Markdown одржава логички ток оригиналне презентације. Ово га чини идеалним за уношење садржаја презентација у AI системе или креирање документације из постојећих слајдова.

### 6. 🗃️ SQL Server MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_SQL_Database-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SQL_Database-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**Шта ради**: Омогућава разговорни приступ SQL Server базама података (локално, Azure SQL или Fabric)

**Зашто је користан**: Слично као PostgreSQL сервер, али за Microsoft SQL екосистем. Повежите се једноставним конекционим низом и почните да упитујете природним језиком – без потребе за пребацивањем контекста!

**Примена у пракси**: „Пронађи све поруџбине које нису испуњене у последњих 30 дана“ се преводи у одговарајуће SQL упите и враћа форматиране резултате

**Илустративан пример**: Када подесите конекцију са базом, можете одмах почети да комуницирате са својим подацима. Блог пост приказује ово кроз једноставно питање: „На коју базу си повезан?“ MCP сервер одговара позивањем одговарајућег алата за базу, повезује се на ваш SQL Server и враћа детаље о тренутној конекцији – све без писања иједне линије SQL-а. Сервер подржава свеобухватне операције са базом, од управљања шемом до манипулације подацима, све кроз природне језичке упите. За комплетна упутства и примере конфигурације са VS Code и Claude Desktop, погледајте: [Introducing MSSQL MCP Server (Preview)](https://devblogs.microsoft.com/azure-sql/introducing-mssql-mcp-server/).

### 7. 🎭 Playwright MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Playwright_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Playwright_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/playwright-mcp)

**Шта ради**: Омогућава AI агентима да интерагују са веб страницама ради тестирања и аутоматизације

> **ℹ️ Покреће GitHub Copilot**
> 
> Playwright MCP Server покреће GitHub Copilot-ов Coding Agent, пружајући му могућност претраживања веба! [Сазнајте више о овој функцији](https://github.blog/changelog/2025-07-02-copilot-coding-agent-now-has-its-own-web-browser/).

**Зашто је користан**: Савршен за аутоматизовано тестирање вођено описима на природном језику. AI може да прегледа веб сајтове, попуњава формуларе и извлачи податке кроз структуиране снимке приступачности – ово је изузетно моћна функција!

**Примена у пракси**: „Тестирај процес пријаве и провери да ли се контролна табла исправно учитава“ или „Генериши тест који претражује производе и верификује страницу са резултатима“ – све без потребе за приступом изворном коду апликације

**Илустративан пример**: Моја колегиница Debbie O'Brien је недавно радила сјајан посао са Playwright MCP Server-ом! На пример, показала је како можете генерисати комплетне Playwright тестове без икаквог приступа изворном коду апликације. У свом примеру, замолила је Copilot да направи тест за апликацију за претрагу филмова: отвори сајт, претражи „Garfield“ и провери да ли се филм појављује у резултатима. MCP је покренуо сесију прегледача, анализирао структуру странице користећи DOM снимке, пронашао одговарајуће селекторе и генерисао потпуно функционалан TypeScript тест који је прошао из првог покретања.

Оно што ово чини заиста моћним је што повезује упутства на природном језику са извршним тест кодом. Традиционални приступи захтевају ручно писање тестова или приступ кодној бази ради контекста. Али са Playwright MCP-ом можете тестирати спољне сајтове, клијентске апликације или радити у сценаријима црне кутије где приступ коду није доступан.

### 8. 💻 Dev Box MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Dev_Box_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Dev_Box_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**Шта ради**: Управља Microsoft Dev Box окружењима кроз природни језик

**Зашто је користан**: Знатно поједностављује управљање развојним окружењима! Креирајте, конфигуришите и управљајте окружењима без потребе да памтите специфичне команде.

**Примена у пракси**: „Подеси нови Dev Box са најновијим .NET SDK и конфигуриши га за наш пројекат“, „Провери статус свих мојих развојних окружења“ или „Креирај стандардизовано демо окружење за тимске презентације“

**Илустративан пример**: Ја сам велики фан коришћења Dev Box-а за лични развој. Мој „ахаа“ моменат је био када ми је James Montemagno објаснио колико је Dev Box сјајан за демо презентације на конференцијама, јер има супер брзу ethernet везу без обзира на WiFi у хотелу, авиону или конференцији. Заправо, недавно сам вежбао демо док ми је лаптоп био повезан на телефонски хотрспот у аутобусу између Бржа и Антверпена! Следећи корак ми је да истражим како да управљам више развојних окружења у тиму и стандардизованим демо окружењима. Још једна велика примена коју чујем од корисника и колега је коришћење Dev Box-а за претходно конфигурисана развојна окружења. У оба случаја, коришћење MCP-а за конфигурисање и управљање Dev Box-овима омогућава интеракцију на природном језику, све док сте у свом развојном окружењу.

### 9. 🤖 Azure AI Foundry MCP Server
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_AI_Foundry_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_AI_Foundry_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/azure-ai-foundry/mcp-foundry)

**Шта ради**: Azure AI Foundry MCP Server пружа програмерима свеобухватан приступ Azure AI екосистему, укључујући каталоге модела, управљање имплементацијом, индексирање знања помоћу Azure AI Search и алате за процену. Овај експериментални сервер повезује развој вештачке интелигенције са моћном Azure AI инфраструктуром, олакшавајући креирање, имплементацију и процену AI апликација.

**Зашто је користан**: Овај сервер мења начин рада са Azure AI услугама тако што доноси корпоративне AI могућности директно у ваш развојни ток. Уместо да прелазите између Azure портала, документације и IDE-а, можете откривати моделе, имплементирати услуге, управљати базама знања и процењивати перформансе AI помоћу природних језичких команди. Посебно је користан за програмере који праве RAG (Retrieval-Augmented Generation) апликације, управљају мулти-модел имплементацијама или спроводе свеобухватне AI процене.

**Кључне могућности за програмере**:
- **🔍 Откривање и имплементација модела**: Истражите каталог модела Azure AI Foundry, добијте детаљне информације о моделима са примерима кода и имплементирајте моделе у Azure AI Services
- **📚 Управљање знањем**: Креирајте и управљајте Azure AI Search индексима, додајте документе, конфигуришите индексере и градите сложене RAG системе
- **⚡ Интеграција AI агената**: Повежите се са Azure AI агентима, упитујте постојеће агенте и процењујте њихове перформансе у продукцијским сценаријима
- **📊 Оквир за процену**: Покрените свеобухватне процене текста и агената, генеришите извештаје у markdown формату и спроводите контролу квалитета AI апликација
- **🚀 Алати за прототиповање**: Добијте упутства за подешавање GitHub базираног прототиповања и приступите Azure AI Foundry Labs за најсавременије истраживачке моделе

**Примена у стварном свету**: „Имплементирај Phi-4 модел у Azure AI Services за моју апликацију“, „Креирај нови индекс претраге за мој RAG систем документације“, „Процени одговоре мог агента према метрикама квалитета“ или „Пронађи најбољи модел резоновања за моје сложене анализе“.

**Цео демонстрациони сценарио**: Ево моћног развојног тока за AI:


> „Правим агента за корисничку подршку. Помози ми да пронађем добар модел резоновања из каталога, имплементирам га у Azure AI Services, креирам базу знања из наше документације, подесим оквир за процену квалитета одговора и затим ми помогни да прототипујем интеграцију са GitHub токеном за тестирање.“

Azure AI Foundry MCP Server ће:
- Упитати каталог модела и препоручити оптималне моделе резоновања на основу твојих захтева
- Обезбедити команде за имплементацију и информације о квотама за изабрани Azure регион
- Подесити Azure AI Search индексе са одговарајућом шемом за твоју документацију
- Конфигурисати проценске токове са метрикама квалитета и безбедносним проверама
- Генерисати код за прототиповање са GitHub аутентификацијом за тренутно тестирање
- Обезбедити свеобухватна упутства прилагођена твом технолошком стеку

**Илустративни пример**: Као програмер, имао сам проблема да пратим различите LLM моделе који су доступни. Познајем неке главне, али сам имао осећај да пропуштам неке могућности за повећање продуктивности и ефикасности. Токени и квоте су стресни и тешки за управљање – никад нисам сигуран да ли сам изабрао прави модел за одређени задатак или неефикасно трошим буџет. Чуо сам за овај MCP Server од James Montemagno-а док сам тражио препоруке од колега, и узбуђен сам да га испробам! Могућности откривања модела делују посебно импресивно за некога као што сам ја, ко жели да истражи више од уобичајених опција и пронађе моделе оптимизоване за специфичне задатке. Оквир за процену ће ми помоћи да проверим да ли заиста добијам боље резултате, а не само да испробавам нешто ново без разлога.

> **ℹ️ Експериментални статус**
> 
> Овај MCP сервер је експерименталан и активно се развија. Функције и API-ји могу се мењати. Идеалан је за истраживање Azure AI могућности и прављење прототипова, али проверите стабилност пре коришћења у продукцији.

### 10. 🏢 Microsoft 365 Agents Toolkit MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_M365_Agents_Toolkit-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_M365_Agents_Toolkit-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/OfficeDev/microsoft-365-agents-toolkit)

**Шта ради**: Пружа програмерима основне алате за креирање AI агената и апликација које се интегришу са Microsoft 365 и Microsoft 365 Copilot-ом, укључујући валидацију шема, приступ примерима кода и помоћ при решавању проблема.

**Зашто је користан**: Развој за Microsoft 365 и Copilot укључује сложене манифест шеме и специфичне развојне обрасце. Овај MCP сервер доноси кључне ресурсе директно у ваше развојно окружење, помажући вам да валидацију шема, пронађете пример кода и решите уобичајене проблеме без сталног прегледања документације.

**Примена у стварном свету**: „Валидирај манифест мог декларативног агента и исправи грешке у шеми“, „Покажи ми пример кода за имплементацију Microsoft Graph API плагина“ или „Помози ми да решим проблеме са аутентификацијом у мојој Teams апликацији“.

**Илустративни пример**: Обратио сам се пријатељу John Miller-у након разговора на Build конференцији о M365 Agents, и он ми је препоручио овај MCP. Ово може бити одлично за програмере који су нови у M365 Agents јер пружа шаблоне, примере кода и основну структуру за брз почетак без преплављивања документацијом. Функције за валидацију шеме делују посебно корисно за избегавање грешака у структури манифеста које могу изазвати сате дебаговања.

> **💡 Корисни савет**
> 
> Користите овај сервер заједно са Microsoft Learn Docs MCP Server-ом за свеобухватну подршку развоју M365 – један пружа званичну документацију, а овај практичне алате и помоћ при решавању проблема.

## Шта следи? 🔮

## 📋 Закључак

Model Context Protocol (MCP) мења начин на који програмери комуницирају са AI асистентима и спољним алатима. Ових 10 Microsoft MCP сервера показују снагу стандардизоване AI интеграције, омогућавајући беспрекорне токове рада који програмерима омогућавају да остану у свом фокусу док користе моћне спољне могућности.

Од свеобухватне интеграције Azure екосистема до специјализованих алата као што су Playwright за аутоматизацију прегледача и MarkItDown за обраду докумената, ови сервери показују како MCP може повећати продуктивност у разним развојним сценаријима. Стандардизовани протокол осигурава да ови алати раде заједно без проблема, стварајући кохерентно развојно искуство.

Како MCP екосистем наставља да се развија, ангажовање у заједници, истраживање нових сервера и креирање прилагођених решења биће кључни за максималну продуктивност развоја. Отворена природа MCP стандарда значи да можете комбиновати алате различитих добављача и створити савршен ток рада за своје специфичне потребе.

## 🔗 Додатни ресурси

- [Званични Microsoft MCP репозиторијум](https://github.com/microsoft/mcp)
- [MCP заједница и документација](https://modelcontextprotocol.io/introduction)
- [VS Code MCP документација](https://code.visualstudio.com/docs/copilot/copilot-mcp)
- [Visual Studio MCP документација](https://learn.microsoft.com/visualstudio/ide/mcp-servers)
- [Azure MCP документација](https://learn.microsoft.com/azure/developer/azure-mcp-server/)
- [Let's Learn – MCP догађаји](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/lets-learn---mcp-events-a-beginners-guide-to-the-model-context-protocol/4429023)
- [Awesome GitHub Copilot Customizations](https://github.com/awesome-copilot)
- [C# MCP SDK](https://developer.microsoft.com/blog/microsoft-partners-with-anthropic-to-create-official-c-sdk-for-model-context-protocol)
- [MCP Dev Days Live 29th/30th July or watch on Demand](https://aka.ms/mcpdevdays)

## 🎯 Вежбе

1. **Инсталирај и конфигуриши**: Подеси један од MCP сервера у свом VS Code окружењу и тестирам основне функције.
2. **Интеграција тока рада**: Осмисли развојни ток који комбинује најмање три различита MCP сервера.
3. **Планирање прилагођеног сервера**: Идентификуј задатак у свакодневном развоју који би могао имати користи од прилагођеног MCP сервера и направи спецификацију за њега.
4. **Анализа перформанси**: Упореди ефикасност коришћења MCP сервера са традиционалним приступима за уобичајене развојне задатке.
5. **Процена безбедности**: Процени безбедносне импликације коришћења MCP сервера у свом развојном окружењу и предложи најбоље праксе.

Next:[Best Practices](../08-BestPractices/README.md)

**Одрицање од одговорности**:  
Овај документ је преведен коришћењем AI сервиса за превођење [Co-op Translator](https://github.com/Azure/co-op-translator). Иако се трудимо да превод буде тачан, молимо вас да имате у виду да аутоматски преводи могу садржати грешке или нетачности. Оригинални документ на његовом изворном језику треба сматрати ауторитетним извором. За критичне информације препоручује се професионални људски превод. Нисмо одговорни за било каква неспоразума или погрешна тумачења настала коришћењем овог превода.