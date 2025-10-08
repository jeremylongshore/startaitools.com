<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:44:22+00:00",
  "source_file": "changelog.md",
  "language_code": "sw"
}
-->
# Rekodi ya Mabadiliko: Mtaala wa MCP kwa Kompyuta

Hati hii ni rekodi ya mabadiliko muhimu yaliyofanywa kwenye mtaala wa Model Context Protocol (MCP) kwa Kompyuta. Mabadiliko yameandikwa kwa mpangilio wa kinyume wa tarehe (mabadiliko mapya kwanza).

## Oktoba 6, 2025

### Upanuzi wa Sehemu ya Kuanza – Matumizi ya Juu ya Seva & Uthibitishaji Rahisi

#### Matumizi ya Juu ya Seva (03-GettingStarted/10-advanced)
- **Sura Mpya Imeongezwa**: Mwongozo wa kina wa matumizi ya juu ya seva za MCP, ukijumuisha usanifu wa kawaida na wa kiwango cha chini.
  - **Kawaida vs. Usanifu wa Kiwango cha Chini**: Ulinganisho wa kina na mifano ya msimbo katika Python na TypeScript kwa mbinu zote mbili.
  - **Ubunifu wa Kulingana na Wahandisi**: Maelezo ya usimamizi wa zana/rasilimali/mwongozo kwa utekelezaji wa seva unaoweza kupanuka na kubadilika.
  - **Mifumo ya Kivitendo**: Matukio halisi ambapo mifumo ya seva ya kiwango cha chini ni muhimu kwa vipengele vya juu na usanifu.

#### Uthibitishaji Rahisi (03-GettingStarted/11-simple-auth)
- **Sura Mpya Imeongezwa**: Mwongozo wa hatua kwa hatua wa kutekeleza uthibitishaji rahisi kwenye seva za MCP.
  - **Mafunzo ya Uthibitishaji**: Maelezo wazi ya tofauti kati ya uthibitishaji na idhini, na usimamizi wa hati za kuingia.
  - **Utekelezaji wa Uthibitishaji wa Msingi**: Mifumo ya uthibitishaji inayotegemea middleware katika Python (Starlette) na TypeScript (Express), pamoja na mifano ya msimbo.
  - **Kuendelea na Usalama wa Juu**: Mwongozo wa kuanza na uthibitishaji rahisi na kuendelea na OAuth 2.1 na RBAC, pamoja na marejeleo ya moduli za usalama wa juu.

Nyongeza hizi zinatoa mwongozo wa vitendo kwa kujenga utekelezaji wa seva za MCP zilizo imara, salama, na zinazoweza kubadilika, zikichanganya dhana za msingi na mifumo ya uzalishaji ya juu.

## Septemba 29, 2025

### Maabara ya Ushirikiano wa Hifadhidata ya Seva ya MCP - Njia Kamili ya Kujifunza kwa Vitendo

#### 11-MCPServerHandsOnLabs - Mtaala Mpya wa Ushirikiano wa Hifadhidata
- **Njia Kamili ya Kujifunza Maabara 13**: Imeongezwa mtaala wa kina wa kujifunza kwa vitendo kwa kujenga seva za MCP zilizo tayari kwa uzalishaji na ushirikiano wa hifadhidata ya PostgreSQL.
  - **Utekelezaji wa Dunia Halisi**: Kesi ya matumizi ya uchanganuzi wa Zava Retail inayoonyesha mifumo ya kiwango cha biashara.
  - **Maendeleo ya Kujifunza kwa Muundo**:
    - **Maabara 00-03: Misingi** - Utangulizi, Usanifu wa Msingi, Usalama & Multi-Tenancy, Usanidi wa Mazingira.
    - **Maabara 04-06: Kujenga Seva ya MCP** - Ubunifu wa Hifadhidata & Schema, Utekelezaji wa Seva ya MCP, Maendeleo ya Zana.
    - **Maabara 07-09: Vipengele vya Juu** - Ushirikiano wa Utafutaji wa Semantic, Upimaji & Urekebishaji, Ushirikiano wa VS Code.
    - **Maabara 10-12: Uzalishaji & Mifumo Bora** - Mikakati ya Utekelezaji, Ufuatiliaji & Uangalizi, Mifumo Bora & Uboreshaji.
  - **Teknolojia za Biashara**: Mfumo wa FastMCP, PostgreSQL na pgvector, embeddings za Azure OpenAI, Azure Container Apps, Application Insights.
  - **Vipengele vya Juu**: Usalama wa Kiwango cha Safu (RLS), utafutaji wa semantic, ufikiaji wa data wa multi-tenant, embeddings za vector, ufuatiliaji wa wakati halisi.

#### Uboreshaji wa Istilahi - Kubadilisha Moduli kuwa Maabara
- **Sasisho la Kina la Nyaraka**: Zote README zimesasishwa katika 11-MCPServerHandsOnLabs kutumia istilahi ya "Maabara" badala ya "Moduli".
  - **Vichwa vya Sehemu**: "Kile Moduli Hii Inashughulikia" imebadilishwa kuwa "Kile Maabara Hii Inashughulikia" katika maabara yote 13.
  - **Maelezo ya Yaliyomo**: "Moduli hii inatoa..." imebadilishwa kuwa "Maabara hii inatoa..." katika nyaraka zote.
  - **Malengo ya Kujifunza**: "Mwisho wa moduli hii..." imebadilishwa kuwa "Mwisho wa maabara hii..."
  - **Viungo vya Uelekezaji**: Marejeleo yote ya "Moduli XX:" yamebadilishwa kuwa "Maabara XX:" katika marejeleo ya msalaba na uelekezaji.
  - **Ufuatiliaji wa Kukamilisha**: "Baada ya kukamilisha moduli hii..." imebadilishwa kuwa "Baada ya kukamilisha maabara hii..."
  - **Marejeleo ya Kiufundi Yaliyohifadhiwa**: Marejeleo ya moduli za Python yamehifadhiwa katika faili za usanidi (mfano, `"module": "mcp_server.main"`).

#### Uboreshaji wa Mwongozo wa Kujifunza (study_guide.md)
- **Ramani ya Mtaala wa Kielelezo**: Sehemu mpya ya "11. Maabara ya Ushirikiano wa Hifadhidata" imeongezwa na muundo wa maabara wa kina.
- **Muundo wa Hifadhi**: Imeboreshwa kutoka sehemu kumi hadi kumi na moja na maelezo ya kina ya 11-MCPServerHandsOnLabs.
- **Mwongozo wa Njia ya Kujifunza**: Maelekezo ya uelekezaji yameimarishwa kufunika sehemu 00-11.
- **Ushirikiano wa Teknolojia**: Maelezo ya FastMCP, PostgreSQL, na huduma za Azure yameongezwa.
- **Matokeo ya Kujifunza**: Utekelezaji wa seva zilizo tayari kwa uzalishaji, mifumo ya ushirikiano wa hifadhidata, na usalama wa kiwango cha biashara vimeangaziwa.

#### Uboreshaji wa Muundo wa README Kuu
- **Istilahi ya Kulingana na Maabara**: README.md kuu katika 11-MCPServerHandsOnLabs imesasishwa kutumia muundo wa "Maabara" kwa uthabiti.
- **Muundo wa Njia ya Kujifunza**: Maendeleo wazi kutoka dhana za msingi hadi utekelezaji wa juu hadi utekelezaji wa uzalishaji.
- **Mtazamo wa Dunia Halisi**: Msisitizo juu ya kujifunza kwa vitendo na mifumo ya kiwango cha biashara na teknolojia.

### Uboreshaji wa Ubora wa Nyaraka & Uthabiti
- **Msisitizo wa Kujifunza kwa Vitendo**: Njia ya maabara ya vitendo imeimarishwa katika nyaraka zote.
- **Mtazamo wa Mifumo ya Biashara**: Utekelezaji ulio tayari kwa uzalishaji na masuala ya usalama wa kiwango cha biashara vimeangaziwa.
- **Ushirikiano wa Teknolojia**: Ushirikiano wa kina wa huduma za kisasa za Azure na mifumo ya AI.
- **Maendeleo ya Kujifunza**: Njia wazi na iliyopangwa kutoka dhana za msingi hadi utekelezaji wa uzalishaji.

## Septemba 26, 2025

### Uboreshaji wa Kesi za Matumizi - Ushirikiano wa Usajili wa MCP wa GitHub

#### Kesi za Matumizi (09-CaseStudy/) - Mtazamo wa Maendeleo ya Mfumo
- **README.md**: Upanuzi mkubwa na kesi ya matumizi ya Usajili wa MCP wa GitHub.
  - **Kesi ya Matumizi ya Usajili wa MCP wa GitHub**: Kesi mpya ya matumizi ya kina inayochunguza uzinduzi wa Usajili wa MCP wa GitHub mnamo Septemba 2025.
    - **Uchambuzi wa Tatizo**: Uchunguzi wa kina wa changamoto za ugunduzi wa seva za MCP zilizogawanyika na utekelezaji.
    - **Usanifu wa Suluhisho**: Mbinu ya usajili wa kati ya GitHub na usakinishaji wa VS Code kwa kubofya mara moja.
    - **Athari za Biashara**: Uboreshaji unaoweza kupimwa katika kuanza kwa watengenezaji na tija.
    - **Thamani ya Kistratejia**: Mtazamo wa utekelezaji wa wakala wa modular na ushirikiano wa zana mbalimbali.
    - **Maendeleo ya Mfumo**: Kuweka msingi kama jukwaa la ushirikiano wa wakala.
  - **Muundo wa Kesi za Matumizi Ulioboreshwa**: Kesi zote saba za matumizi zimesasishwa na muundo thabiti na maelezo ya kina.
    - Mawakala wa Safari za AI za Azure: Msisitizo wa orchestration ya wakala mbalimbali.
    - Ushirikiano wa Azure DevOps: Mtazamo wa kiotomatiki wa mtiririko wa kazi.
    - Urejeshaji wa Nyaraka wa Wakati Halisi: Utekelezaji wa mteja wa console ya Python.
    - Jenereta ya Mpango wa Kujifunza wa Maingiliano: Programu ya wavuti ya mazungumzo ya Chainlit.
    - Nyaraka Ndani ya Mhariri: Ushirikiano wa VS Code na GitHub Copilot.
    - Usimamizi wa API ya Azure: Mifumo ya ushirikiano wa API ya biashara.
    - Usajili wa MCP wa GitHub: Maendeleo ya mfumo na jukwaa la jamii.
  - **Hitimisho la Kina**: Sehemu ya hitimisho imeandikwa upya ikionyesha kesi saba za matumizi zinazojumuisha vipengele mbalimbali vya utekelezaji wa MCP.
    - Ushirikiano wa Biashara, Orchestration ya Wakala Mbalimbali, Tija ya Watengenezaji.
    - Maendeleo ya Mfumo, Matumizi ya Kielimu.
    - Uboreshaji wa maarifa kuhusu mifumo ya usanifu, mikakati ya utekelezaji, na mifumo bora.
    - Msisitizo wa MCP kama itifaki iliyopevuka, tayari kwa uzalishaji.

#### Sasisho za Mwongozo wa Kujifunza (study_guide.md)
- **Ramani ya Mtaala wa Kielelezo**: Mindmap imesasishwa kujumuisha Usajili wa MCP wa GitHub katika sehemu ya Kesi za Matumizi.
- **Maelezo ya Kesi za Matumizi**: Maelezo ya jumla yameimarishwa kuwa muhtasari wa kina wa kesi saba za matumizi.
- **Muundo wa Hifadhi**: Sehemu ya 10 imesasishwa kuonyesha chanjo ya kina ya kesi za matumizi na maelezo maalum ya utekelezaji.
- **Ujumuishaji wa Rekodi ya Mabadiliko**: Kuingizwa kwa tarehe ya Septemba 26, 2025 ikiorodhesha nyongeza ya Usajili wa MCP wa GitHub na uboreshaji wa kesi za matumizi.
- **Sasisho za Tarehe**: Timestamp ya footer imesasishwa kuonyesha marekebisho ya hivi karibuni (Septemba 26, 2025).

### Uboreshaji wa Ubora wa Nyaraka
- **Uthabiti Ulioboreshwa**: Muundo wa kesi za matumizi na muundo thabiti katika mifano yote saba.
- **Chanjo ya Kina**: Kesi za matumizi sasa zinajumuisha matukio ya biashara, tija ya watengenezaji, na maendeleo ya mfumo.
- **Kuweka Kistratejia**: Mtazamo ulioimarishwa wa MCP kama jukwaa la msingi kwa utekelezaji wa mifumo ya wakala.
- **Ujumuishaji wa Rasilimali**: Rasilimali za ziada zimesasishwa kujumuisha kiungo cha Usajili wa MCP wa GitHub.

## Septemba 15, 2025

### Upanuzi wa Mada za Juu - Usafirishaji Maalum & Uhandisi wa Muktadha

#### Usafirishaji Maalum wa MCP (05-AdvancedTopics/mcp-transport/) - Mwongozo Mpya wa Utekelezaji wa Juu
- **README.md**: Mwongozo kamili wa utekelezaji wa mifumo maalum ya usafirishaji wa MCP.
  - **Usafirishaji wa Azure Event Grid**: Utekelezaji wa usafirishaji wa matukio unaotegemea seva.
    - Mifano ya C#, TypeScript, na Python na ushirikiano wa Azure Functions.
    - Mifumo ya usanifu wa matukio kwa suluhisho za MCP zinazoweza kupanuka.
    - Wapokeaji wa webhook na usimamizi wa ujumbe unaotegemea msukumo.
  - **Usafirishaji wa Azure Event Hubs**: Utekelezaji wa usafirishaji wa utiririshaji wa kiwango cha juu.
    - Uwezo wa utiririshaji wa wakati halisi kwa matukio ya ucheleweshaji wa chini.
    - Mikakati ya kugawanya na usimamizi wa alama za ukaguzi.
    - Uboreshaji wa utendaji na usimamizi wa ujumbe wa kundi.
  - **Mifumo ya Ushirikiano wa Biashara**: Mifano ya usanifu iliyo tayari kwa uzalishaji.
    - Usindikaji wa MCP uliosambazwa katika Azure Functions nyingi.
    - Usanifu wa usafirishaji mseto unaochanganya aina nyingi za usafirishaji.
    - Mikakati ya kudumu kwa ujumbe, uaminifu, na usimamizi wa makosa.
  - **Usalama & Ufuatiliaji**: Ushirikiano wa Azure Key Vault na mifumo ya uangalizi.
    - Uthibitishaji wa utambulisho uliosimamiwa na ufikiaji wa kiwango cha chini.
    - Telemetry ya Application Insights na ufuatiliaji wa utendaji.
    - Mifumo ya kuvunja mzunguko na mikakati ya uvumilivu wa makosa.
  - **Mifumo ya Upimaji**: Mikakati ya upimaji wa kina kwa usafirishaji maalum.
    - Upimaji wa vitengo kwa mifumo ya bandia na mifumo ya kuiga.
    - Upimaji wa ushirikiano na Azure Test Containers.
    - Mazingatio ya upimaji wa utendaji na mzigo.

#### Uhandisi wa Muktadha (05-AdvancedTopics/mcp-contextengineering/) - Taaluma Inayochipuka ya AI
- **README.md**: Uchunguzi wa kina wa uhandisi wa muktadha kama uwanja unaochipuka.
  - **Kanuni za Msingi**: Kushiriki muktadha kikamilifu, ufahamu wa maamuzi ya hatua, na usimamizi wa dirisha la muktadha.
  - **Ulinganifu wa Itifaki ya MCP**: Jinsi muundo wa MCP unavyoshughulikia changamoto za uhandisi wa muktadha.
    - Vikwazo vya dirisha la muktadha na mikakati ya upakiaji wa maendeleo.
    - Uamuzi wa umuhimu na urejeshaji wa muktadha wa nguvu.
    - Ushughulikiaji wa muktadha wa njia nyingi na masuala ya usalama.
  - **Mbinu za Utekelezaji**: Usanifu wa nyuzi moja vs. wakala mbalimbali.
    - Mbinu za kugawanya muktadha na kipaumbele.
    - Upakiaji wa maendeleo wa muktadha na mikakati ya ukandamizaji.
    - Mbinu za muktadha zilizowekwa tabaka na uboreshaji wa urejeshaji.
  - **Mfumo wa Upimaji**: Vipimo vinavyochipuka vya tathmini ya ufanisi wa muktadha.
    - Ufanisi wa pembejeo, utendaji, ubora, na mazingatio ya uzoefu wa mtumiaji.
    - Mbinu za majaribio za uboreshaji wa muktadha.
    - Uchambuzi wa kushindwa na mbinu za kuboresha.

#### Sasisho za Uelekezaji wa Mtaala (README.md)
- **Muundo wa Moduli Ulioboreshwa**: Jedwali la mtaala limesasishwa kujumuisha mada mpya za juu.
  - Sehemu za Uhandisi wa Muktadha (5.14) na Usafirishaji Maalum (5.15) zimeongezwa.
  - Muundo thabiti na viungo vya uelekezaji katika moduli zote.
  - Maelezo yamesasishwa kuonyesha wigo wa yaliyomo ya sasa.

### Uboreshaji wa Muundo wa Hifadhi
- **Uthabiti wa Majina**: "mcp transport" imebadilishwa kuwa "mcp-transport" kwa uthabiti na folda nyingine za mada za juu.
- **Muundo wa Yaliyomo**: Folda zote za 05-AdvancedTopics sasa zinafuata muundo wa majina thabiti (mcp-[mada]).

### Uboreshaji wa Ubora wa Nyaraka
- **Ulinganifu wa Maelezo ya MCP**: Yaliyomo yote mapya yanarejelea Maelezo ya MCP ya sasa ya 2025-06-18.
- **Mifano ya Lugha Nyingi**: Mifano ya msimbo ya kina katika C#, TypeScript, na Python.
- **Mtazamo wa Biashara**: Mifumo iliyo tayari
#### Mada ya Juu Usalama (05-AdvancedTopics/mcp-security/) - Utekelezaji Tayari kwa Uzalishaji
- **README.md**: Kuandikwa upya kabisa kwa utekelezaji wa usalama wa kiwango cha biashara
  - **Ulinganifu wa Maelezo ya Sasa**: Imesasishwa kwa Maelezo ya MCP 2025-06-18 na mahitaji ya lazima ya usalama
  - **Uthibitishaji Ulioboreshwa**: Ujumuishaji wa Microsoft Entra ID na mifano kamili ya usalama ya .NET na Java Spring
  - **Ujumuishaji wa Usalama wa AI**: Utekelezaji wa Microsoft Prompt Shields na Azure Content Safety na mifano ya kina ya Python
  - **Kupunguza Vitisho vya Juu**: Mifano kamili ya utekelezaji kwa:
    - Kuzuia Mashambulizi ya Confused Deputy kwa PKCE na uthibitishaji wa ridhaa ya mtumiaji
    - Kuzuia Uhamishaji wa Tokeni kwa uthibitishaji wa hadhira na usimamizi salama wa tokeni
    - Kuzuia Utekaji wa Kikao kwa kufunga kwa njia ya kriptografia na uchambuzi wa tabia
  - **Ujumuishaji wa Usalama wa Biashara**: Ufuatiliaji wa Azure Application Insights, mifumo ya kugundua vitisho, na usalama wa mnyororo wa ugavi
  - **Orodha ya Utekelezaji**: Udhibiti wa usalama wa lazima dhidi ya unaopendekezwa na faida za mfumo wa usalama wa Microsoft

### Ubora wa Nyaraka na Ulinganifu wa Viwango
- **Marejeleo ya Maelezo**: Imesasishwa marejeleo yote kwa Maelezo ya MCP ya sasa 2025-06-18
- **Mfumo wa Usalama wa Microsoft**: Mwongozo ulioboreshwa wa ujumuishaji katika nyaraka zote za usalama
- **Utekelezaji wa Kivitendo**: Mifano ya kina ya msimbo katika .NET, Java, na Python na mifumo ya biashara
- **Mpangilio wa Rasilimali**: Uainishaji kamili wa nyaraka rasmi, viwango vya usalama, na miongozo ya utekelezaji
- **Viashiria vya Kielezo**: Alama wazi za mahitaji ya lazima dhidi ya mazoea yanayopendekezwa

#### Dhana za Msingi (01-CoreConcepts/) - Kisasa Kamili
- **Sasisho la Toleo la Itifaki**: Imesasishwa kurejelea Maelezo ya MCP ya sasa 2025-06-18 na muundo wa tarehe (YYYY-MM-DD)
- **Uboreshaji wa Usanifu**: Maelezo yaliyoboreshwa ya Wenyeji, Wateja, na Seva ili kuonyesha mifumo ya usanifu ya sasa ya MCP
  - Wenyeji sasa wamefafanuliwa wazi kama programu za AI zinazoratibu miunganisho mingi ya wateja wa MCP
  - Wateja wameelezwa kama viunganishi vya itifaki vinavyodumisha uhusiano wa moja kwa moja na seva
  - Seva zimeboreshwa na hali za usanidi wa ndani dhidi ya wa mbali
- **Urekebishaji wa Primitives**: Marekebisho kamili ya primitives za seva na wateja
  - Primitives za Seva: Rasilimali (vyanzo vya data), Maelezo (templates), Zana (kazi zinazoweza kutekelezwa) na maelezo ya kina na mifano
  - Primitives za Wateja: Sampuli (ukamilishaji wa LLM), Uchochezi (maingizo ya mtumiaji), Kumbukumbu (upelelezi/ufuatiliaji)
  - Imesasishwa na mifumo ya sasa ya ugunduzi (`*/list`), upatikanaji (`*/get`), na utekelezaji (`*/call`)
- **Usanifu wa Itifaki**: Mfano wa usanifu wa tabaka mbili ulianzishwa
  - Tabaka la Data: Msingi wa JSON-RPC 2.0 na usimamizi wa mzunguko wa maisha na primitives
  - Tabaka la Usafirishaji: STDIO (ndani) na HTTP inayoweza kutiririka na SSE (mbali) kama mifumo ya usafirishaji
- **Mfumo wa Usalama**: Kanuni za usalama za kina ikiwa ni pamoja na ridhaa ya wazi ya mtumiaji, ulinzi wa faragha ya data, usalama wa utekelezaji wa zana, na usalama wa tabaka la usafirishaji
- **Mifumo ya Mawasiliano**: Imesasishwa ujumbe wa itifaki kuonyesha mchakato wa kuanzisha, kugundua, kutekeleza, na kutoa taarifa
- **Mifano ya Msimbo**: Mifano ya lugha nyingi (.NET, Java, Python, JavaScript) imesasishwa ili kuonyesha mifumo ya sasa ya MCP SDK

#### Usalama (02-Security/) - Marekebisho Kamili ya Usalama  
- **Ulinganifu wa Viwango**: Ulinganifu kamili na mahitaji ya usalama ya Maelezo ya MCP 2025-06-18
- **Mageuzi ya Uthibitishaji**: Mageuzi kutoka kwa seva za OAuth za kawaida hadi ugawaji wa mtoa huduma wa kitambulisho wa nje (Microsoft Entra ID)
- **Uchambuzi wa Vitisho vya AI**: Uboreshaji wa chanjo ya vectors za mashambulizi ya AI ya kisasa
  - Hali za mashambulizi ya sindano ya maelezo na mifano halisi
  - Mbinu za sumu za zana na mifumo ya mashambulizi ya "rug pull"
  - Sumu ya dirisha la muktadha na mashambulizi ya mkanganyiko wa modeli
- **Suluhisho za Usalama za AI za Microsoft**: Chanjo kamili ya mfumo wa usalama wa Microsoft
  - Prompt Shields za AI na mbinu za kugundua, kuonyesha, na mipaka ya juu
  - Mifumo ya ujumuishaji wa Azure Content Safety
  - Usalama wa Juu wa GitHub kwa ulinzi wa mnyororo wa ugavi
- **Kupunguza Vitisho vya Juu**: Udhibiti wa usalama wa kina kwa:
  - Utekaji wa kikao na hali maalum za mashambulizi ya MCP na mahitaji ya ID ya kikao ya kriptografia
  - Matatizo ya Confused Deputy katika hali za wakala wa MCP na mahitaji ya ridhaa ya wazi
  - Udhaifu wa uhamishaji wa tokeni na udhibiti wa uthibitishaji wa lazima
- **Usalama wa Mnyororo wa Ugavi**: Chanjo ya mnyororo wa ugavi wa AI iliyopanuliwa ikiwa ni pamoja na modeli za msingi, huduma za embeddings, watoa muktadha, na API za wahusika wa tatu
- **Usalama wa Msingi**: Ujumuishaji ulioboreshwa na mifumo ya usalama wa biashara ikiwa ni pamoja na usanifu wa zero trust na mfumo wa usalama wa Microsoft
- **Mpangilio wa Rasilimali**: Viungo vya rasilimali vilivyopangwa kwa aina (Nyaraka Rasmi, Viwango, Utafiti, Suluhisho za Microsoft, Miongozo ya Utekelezaji)

### Uboreshaji wa Ubora wa Nyaraka
- **Malengo ya Kujifunza Yaliyopangwa**: Malengo ya kujifunza yaliyoboreshwa na matokeo maalum, yanayoweza kutekelezwa
- **Marejeleo ya Msalaba**: Viungo vilivyoongezwa kati ya mada zinazohusiana za usalama na dhana za msingi
- **Taarifa za Sasa**: Imesasishwa marejeleo yote ya tarehe na viungo vya maelezo kwa viwango vya sasa
- **Mwongozo wa Utekelezaji**: Miongozo maalum, inayoweza kutekelezwa ya utekelezaji imeongezwa katika sehemu zote mbili

## Julai 16, 2025

### README na Uboreshaji wa Uabiri
- Muundo wa uabiri wa mtaala katika README.md umerekebishwa kabisa
- Lebo za `<details>` zimebadilishwa na muundo wa meza unaoweza kufikiwa zaidi
- Chaguo mbadala za mpangilio zimeundwa katika folda mpya ya "alternative_layouts"
- Mifano ya uabiri wa mtindo wa kadi, tabbed-style, na accordion-style imeongezwa
- Sehemu ya muundo wa hifadhi ya jalada imesasishwa ili kujumuisha faili zote za hivi karibuni
- Sehemu ya "Jinsi ya Kutumia Mtaala Huu" imeboreshwa na mapendekezo wazi
- Viungo vya maelezo ya MCP vimesasishwa kuelekeza kwenye URL sahihi
- Sehemu ya Uhandisi wa Muktadha (5.14) imeongezwa kwenye muundo wa mtaala

### Sasisho za Mwongozo wa Kujifunza
- Mwongozo wa kujifunza umerekebishwa kabisa ili kuendana na muundo wa hifadhi ya jalada ya sasa
- Sehemu mpya zimeongezwa kwa Wateja wa MCP na Zana, na Seva Maarufu za MCP
- Ramani ya Mtaala wa Kielezo imesasishwa ili kuonyesha mada zote kwa usahihi
- Maelezo ya Mada za Juu yameboreshwa ili kufunika maeneo yote maalum
- Sehemu ya Masomo ya Kesi imesasishwa ili kuonyesha mifano halisi
- Changelog hii kamili imeongezwa

### Michango ya Jamii (06-CommunityContributions/)
- Taarifa za kina kuhusu seva za MCP kwa kizazi cha picha zimeongezwa
- Sehemu kamili ya kutumia Claude katika VSCode imeongezwa
- Maelekezo ya usanidi wa mteja wa terminal wa Cline na matumizi yameongezwa
- Sehemu ya wateja wa MCP imesasishwa ili kujumuisha chaguo zote maarufu za wateja
- Mifano ya michango imeboreshwa na sampuli sahihi zaidi za msimbo

### Mada za Juu (05-AdvancedTopics/)
- Folda zote za mada maalum zimepangwa kwa majina yanayolingana
- Vifaa na mifano ya uhandisi wa muktadha imeongezwa
- Nyaraka za ujumuishaji wa wakala wa Foundry zimeongezwa
- Nyaraka za ujumuishaji wa usalama wa Entra ID zimeboreshwa

## Juni 11, 2025

### Uundaji wa Awali
- Toleo la kwanza la mtaala wa MCP kwa Kompyuta lilitolewa
- Muundo wa msingi wa sehemu zote 10 kuu uliundwa
- Ramani ya Mtaala wa Kielezo ilitekelezwa kwa uabiri
- Miradi ya sampuli ya awali katika lugha nyingi za programu iliongezwa

### Kuanza (03-GettingStarted/)
- Mifano ya utekelezaji wa seva ya kwanza iliundwa
- Mwongozo wa maendeleo ya mteja umeongezwa
- Maelekezo ya ujumuishaji wa mteja wa LLM yamejumuishwa
- Nyaraka za ujumuishaji wa VS Code zimeongezwa
- Mifano ya seva ya Server-Sent Events (SSE) ilitekelezwa

### Dhana za Msingi (01-CoreConcepts/)
- Maelezo ya kina ya usanifu wa mteja-seva yameongezwa
- Nyaraka za vipengele muhimu vya itifaki ziliundwa
- Mifumo ya ujumbe katika MCP iliorodheshwa

## Mei 23, 2025

### Muundo wa Hifadhi ya Jalada
- Hifadhi ya jalada ilianzishwa na muundo wa folda wa msingi
- Faili za README kwa kila sehemu kuu ziliundwa
- Miundombinu ya tafsiri ilianzishwa
- Picha na michoro ziliongezwa

### Nyaraka
- README.md ya awali iliyo na muhtasari wa mtaala iliundwa
- CODE_OF_CONDUCT.md na SECURITY.md ziliundwa
- SUPPORT.md iliyo na mwongozo wa kupata msaada iliundwa
- Muundo wa awali wa mwongozo wa kujifunza uliundwa

## Aprili 15, 2025

### Mipango na Mfumo
- Mipango ya awali ya mtaala wa MCP kwa Kompyuta ilianza
- Malengo ya kujifunza na hadhira lengwa yalifafanuliwa
- Muundo wa sehemu 10 za mtaala ulielezwa
- Mfumo wa dhana kwa mifano na masomo ya kesi ulitengenezwa
- Mifano ya awali ya prototype kwa dhana muhimu iliundwa

---

**Kanusho**:  
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kuhakikisha usahihi, tafadhali fahamu kuwa tafsiri za kiotomatiki zinaweza kuwa na makosa au kutokuwa sahihi. Hati ya asili katika lugha yake ya awali inapaswa kuzingatiwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu ya binadamu inapendekezwa. Hatutawajibika kwa kutoelewana au tafsiri zisizo sahihi zinazotokana na matumizi ya tafsiri hii.