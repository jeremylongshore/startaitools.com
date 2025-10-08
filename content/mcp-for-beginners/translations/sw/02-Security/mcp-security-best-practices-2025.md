<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-19T14:33:44+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "sw"
}
-->
# MCP Mbinu Bora za Usalama - Sasisho la Agosti 2025

> **Muhimu**: Hati hii inaonyesha mahitaji ya usalama ya hivi karibuni kulingana na [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) na [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Daima rejelea toleo la sasa la maelezo haya kwa mwongozo wa kisasa zaidi.

## Mbinu Muhimu za Usalama kwa Utekelezaji wa MCP

Model Context Protocol inaleta changamoto za kipekee za usalama zinazozidi zile za programu za kawaida. Mbinu hizi zinashughulikia mahitaji ya msingi ya usalama na vitisho maalum vya MCP kama vile prompt injection, tool poisoning, session hijacking, matatizo ya confused deputy, na udhaifu wa token passthrough.

### **MAHITAJI YA LAZIMA YA USALAMA**

**Mahitaji Muhimu kutoka kwa MCP Specification:**

> **MUST NOT**: MCP servers **MUST NOT** kukubali token zozote ambazo hazijatolewa mahsusi kwa MCP server  
> 
> **MUST**: MCP servers zinazotekeleza authorization **MUST** kuthibitisha maombi yote yanayoingia  
>  
> **MUST NOT**: MCP servers **MUST NOT** kutumia sessions kwa ajili ya authentication  
>
> **MUST**: MCP proxy servers zinazotumia static client IDs **MUST** kupata ridhaa ya mtumiaji kwa kila mteja aliyesajiliwa kwa njia ya nguvu  

---

## 1. **Usalama wa Token & Uthibitishaji**

**Udhibiti wa Uthibitishaji na Uidhinishaji:**
   - **Ukaguzi Mkali wa Uidhinishaji**: Fanya ukaguzi wa kina wa mantiki ya uidhinishaji wa MCP server ili kuhakikisha kuwa ni watumiaji na wateja waliokusudiwa pekee wanaweza kufikia rasilimali  
   - **Ujumuishaji wa Mtoa Utambulisho wa Nje**: Tumia watoa utambulisho waliothibitishwa kama Microsoft Entra ID badala ya kutekeleza uthibitishaji wa kawaida  
   - **Uthibitishaji wa Token Audience**: Daima hakikisha kuwa token zilitolewa mahsusi kwa MCP server yako - usikubali token za upstream  
   - **Mzunguko Sahihi wa Token**: Tekeleza mzunguko salama wa token, sera za kumalizika muda, na zuia mashambulizi ya token replay  

**Hifadhi Salama ya Token:**
   - Tumia Azure Key Vault au hifadhi salama za siri zinazofanana kwa siri zote  
   - Tekeleza usimbaji wa token wakati wa kuhifadhi na kusafirisha  
   - Fanya mzunguko wa mara kwa mara wa siri na ufuatiliaji wa ufikiaji usioidhinishwa  

## 2. **Usimamizi wa Session & Usalama wa Usafirishaji**

**Mbinu Salama za Session:**
   - **Session IDs Zenye Usimbaji wa Kificho**: Tumia session IDs salama, zisizotabirika zinazozalishwa kwa jenereta za namba za bahati nasibu salama  
   - **Ufungaji wa Mtumiaji Maalum**: Funga session IDs kwa utambulisho wa watumiaji kwa kutumia fomati kama `<user_id>:<session_id>` ili kuzuia matumizi mabaya ya session kati ya watumiaji  
   - **Usimamizi wa Mzunguko wa Session**: Tekeleza kumalizika muda, mzunguko, na kubatilisha ipasavyo ili kupunguza madirisha ya udhaifu  
   - **Utekelezaji wa HTTPS/TLS**: HTTPS ni lazima kwa mawasiliano yote ili kuzuia kuingiliwa kwa session ID  

**Usalama wa Safu ya Usafirishaji:**
   - Sanidi TLS 1.3 inapowezekana na usimamizi sahihi wa vyeti  
   - Tekeleza certificate pinning kwa miunganisho muhimu  
   - Fanya mzunguko wa mara kwa mara wa vyeti na uhakiki wa uhalali  

## 3. **Ulinzi Dhidi ya Vitisho Maalum vya AI** 🤖

**Ulinzi Dhidi ya Prompt Injection:**
   - **Microsoft Prompt Shields**: Tumia AI Prompt Shields kwa ajili ya kugundua na kuchuja maagizo mabaya  
   - **Usafishaji wa Ingizo**: Thibitisha na safisha maingizo yote ili kuzuia mashambulizi ya injection na matatizo ya confused deputy  
   - **Mipaka ya Maudhui**: Tumia mifumo ya delimiter na datamarking kutofautisha kati ya maagizo yanayoaminika na maudhui ya nje  

**Kuzuia Tool Poisoning:**
   - **Uthibitishaji wa Metadata ya Zana**: Tekeleza ukaguzi wa uadilifu wa ufafanuzi wa zana na ufuatilie mabadiliko yasiyotarajiwa  
   - **Ufuatiliaji wa Zana kwa Wakati Halisi**: Fuatilia tabia ya wakati wa utekelezaji na weka tahadhari kwa mifumo isiyotarajiwa ya utekelezaji  
   - **Mtiririko wa Idhini**: Hitaji idhini ya wazi ya mtumiaji kwa mabadiliko ya zana na uwezo  

## 4. **Udhibiti wa Ufikiaji & Ruhusa**

**Kanuni ya Upendeleo wa Chini Kabisa:**
   - Toa MCP servers ruhusa za chini kabisa zinazohitajika kwa utendaji uliokusudiwa  
   - Tekeleza udhibiti wa ufikiaji kulingana na majukumu (RBAC) na ruhusa za kina  
   - Fanya mapitio ya mara kwa mara ya ruhusa na ufuatiliaji wa kuendelea wa kupandishwa kwa ruhusa  

**Udhibiti wa Ruhusa Wakati wa Utekelezaji:**
   - Tumia mipaka ya rasilimali ili kuzuia mashambulizi ya uchovu wa rasilimali  
   - Tumia kutengwa kwa kontena kwa mazingira ya utekelezaji wa zana  
   - Tekeleza ufikiaji wa muda mfupi kwa kazi za kiutawala  

## 5. **Usalama wa Maudhui & Ufuatiliaji**

**Utekelezaji wa Usalama wa Maudhui:**
   - **Ujumuishaji wa Azure Content Safety**: Tumia Azure Content Safety kugundua maudhui hatari, majaribio ya jailbreak, na ukiukaji wa sera  
   - **Uchambuzi wa Tabia**: Tekeleza ufuatiliaji wa tabia ya wakati wa utekelezaji ili kugundua hali zisizo za kawaida katika MCP server na utekelezaji wa zana  
   - **Kumbukumbu Kamili**: Rekodi majaribio yote ya uthibitishaji, miito ya zana, na matukio ya usalama kwa hifadhi salama isiyoweza kubadilishwa  

**Ufuatiliaji Endelevu:**
   - Tahadhari za wakati halisi kwa mifumo ya kutiliwa shaka na majaribio ya ufikiaji usioidhinishwa  
   - Ujumuishaji na mifumo ya SIEM kwa usimamizi wa kati wa matukio ya usalama  
   - Ukaguzi wa mara kwa mara wa usalama na majaribio ya kupenya kwa utekelezaji wa MCP  

## 6. **Usalama wa Mnyororo wa Ugavi**

**Uthibitishaji wa Vipengele:**
   - **Uchambuzi wa Utegemezi**: Tumia uchambuzi wa kiotomatiki wa udhaifu kwa utegemezi wote wa programu na vipengele vya AI  
   - **Uthibitishaji wa Asili**: Thibitisha asili, leseni, na uadilifu wa mifano, vyanzo vya data, na huduma za nje  
   - **Paket Zilizotiwa Saini**: Tumia paket zilizotiwa saini kwa njia ya kificho na thibitisha saini kabla ya kupeleka  

**Mchakato Salama wa Maendeleo:**
   - **GitHub Advanced Security**: Tekeleza uchambuzi wa siri, uchambuzi wa utegemezi, na uchambuzi tuli wa CodeQL  
   - **Usalama wa CI/CD**: Jumuisha uthibitishaji wa usalama katika mchakato wa kiotomatiki wa kupeleka  
   - **Uadilifu wa Vifaa**: Tekeleza uthibitishaji wa kificho kwa vifaa vilivyotumwa na usanidi  

## 7. **Usalama wa OAuth & Kuzuia Confused Deputy**

**Utekelezaji wa OAuth 2.1:**
   - **Utekelezaji wa PKCE**: Tumia Proof Key for Code Exchange (PKCE) kwa maombi yote ya uidhinishaji  
   - **Ridhaa ya Wazi**: Pata ridhaa ya mtumiaji kwa kila mteja aliyesajiliwa kwa nguvu ili kuzuia mashambulizi ya confused deputy  
   - **Uthibitishaji wa Redirect URI**: Tekeleza uthibitishaji mkali wa redirect URIs na vitambulisho vya mteja  

**Usalama wa Proxy:**
   - Zuia kupitishwa kwa uidhinishaji kupitia unyonyaji wa static client ID  
   - Tekeleza mtiririko sahihi wa ridhaa kwa ufikiaji wa API za wahusika wa tatu  
   - Fuatilia wizi wa authorization code na ufikiaji usioidhinishwa wa API  

## 8. **Majibu ya Matukio & Urejeshaji**

**Uwezo wa Kujibu Haraka:**
   - **Majibu ya Kiotomatiki**: Tekeleza mifumo ya kiotomatiki kwa mzunguko wa siri na kudhibiti vitisho  
   - **Taratibu za Kurudisha**: Uwezo wa kurudi haraka kwenye usanidi na vipengele vilivyo salama  
   - **Uwezo wa Uchunguzi**: Njia za ukaguzi wa kina na kumbukumbu kwa uchunguzi wa matukio  

**Mawasiliano & Uratibu:**
   - Taratibu wazi za kupandisha matukio ya usalama  
   - Ujumuishaji na timu za shirika za majibu ya matukio  
   - Mazoezi ya mara kwa mara ya matukio ya usalama na mazoezi ya kinadharia  

## 9. **Uzingatiaji wa Sheria & Utawala**

**Uzingatiaji wa Kanuni:**
   - Hakikisha utekelezaji wa MCP unakidhi mahitaji maalum ya sekta (GDPR, HIPAA, SOC 2)  
   - Tekeleza udhibiti wa uainishaji wa data na faragha kwa usindikaji wa data ya AI  
   - Dumisha nyaraka kamili kwa ukaguzi wa uzingatiaji  

**Usimamizi wa Mabadiliko:**
   - Michakato rasmi ya ukaguzi wa usalama kwa mabadiliko yote ya mfumo wa MCP  
   - Udhibiti wa toleo na mtiririko wa idhini kwa mabadiliko ya usanidi  
   - Tathmini za mara kwa mara za uzingatiaji na uchambuzi wa mapengo  

## 10. **Udhibiti wa Juu wa Usalama**

**Zero Trust Architecture:**
   - **Usiamini Kamwe, Thibitisha Daima**: Uthibitishaji wa kuendelea wa watumiaji, vifaa, na miunganisho  
   - **Micro-segmentation**: Udhibiti wa kina wa mtandao unaotenga vipengele vya MCP binafsi  
   - **Ufikiaji wa Masharti**: Udhibiti wa ufikiaji unaotegemea hatari unaobadilika kulingana na muktadha wa sasa na tabia  

**Ulinzi wa Programu Wakati wa Utekelezaji:**
   - **Runtime Application Self-Protection (RASP)**: Tekeleza mbinu za RASP kwa kugundua vitisho kwa wakati halisi  
   - **Ufuatiliaji wa Utendaji wa Programu**: Fuatilia hali zisizo za kawaida za utendaji ambazo zinaweza kuashiria mashambulizi  
   - **Sera za Usalama Zinazobadilika**: Tekeleza sera za usalama zinazobadilika kulingana na mazingira ya sasa ya vitisho  

## 11. **Ujumuishaji wa Mfumo wa Usalama wa Microsoft**

**Usalama Kamili wa Microsoft:**
   - **Microsoft Defender for Cloud**: Usimamizi wa hali ya usalama wa wingu kwa mzigo wa kazi wa MCP  
   - **Azure Sentinel**: Uwezo wa SIEM na SOAR wa asili ya wingu kwa kugundua vitisho vya hali ya juu  
   - **Microsoft Purview**: Utawala wa data na uzingatiaji kwa mtiririko wa kazi wa AI na vyanzo vya data  

**Usimamizi wa Utambulisho & Ufikiaji:**
   - **Microsoft Entra ID**: Usimamizi wa utambulisho wa biashara na sera za ufikiaji wa masharti  
   - **Privileged Identity Management (PIM)**: Ufikiaji wa muda mfupi na mtiririko wa idhini kwa kazi za kiutawala  
   - **Identity Protection**: Udhibiti wa ufikiaji unaotegemea hatari na majibu ya kiotomatiki ya vitisho  

## 12. **Mageuzi Endelevu ya Usalama**

**Kukaa Kwenye Mstari wa Mbele:**
   - **Ufuatiliaji wa Maelezo**: Mapitio ya mara kwa mara ya masasisho ya MCP specification na mabadiliko ya mwongozo wa usalama  
   - **Ujasusi wa Vitisho**: Ujumuishaji wa vyanzo vya vitisho maalum vya AI na viashiria vya kuathirika  
   - **Ushirikiano wa Jamii ya Usalama**: Ushiriki wa kazi katika jamii ya usalama ya MCP na programu za kufichua udhaifu  

**Usalama Unaobadilika:**
   - **Usalama wa Kujifunza kwa Mashine**: Tumia kugundua hali zisizo za kawaida kwa msingi wa ML ili kutambua mifumo mipya ya mashambulizi  
   - **Uchambuzi wa Usalama wa Kutabiri**: Tekeleza mifano ya kutabiri kwa utambulisho wa vitisho kwa njia ya proaktif  
   - **Kiotomatiki cha Usalama**: Sasisho za sera za usalama za kiotomatiki kulingana na ujasusi wa vitisho na mabadiliko ya maelezo  

---

## **Rasilimali Muhimu za Usalama**

### **Hati Rasmi za MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Suluhisho za Usalama za Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Security](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Viwango vya Usalama**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Miongozo ya Utekelezaji**
- [Azure API Management MCP Authentication Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Tahadhari ya Usalama**: Mbinu za usalama za MCP hubadilika haraka. Daima hakikisha dhidi ya [MCP specification](https://spec.modelcontextprotocol.io/) ya sasa na [hati rasmi za usalama](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) kabla ya utekelezaji.

**Kanusho**:  
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kuhakikisha usahihi, tafadhali fahamu kuwa tafsiri za kiotomatiki zinaweza kuwa na makosa au kutokuwa sahihi. Hati ya asili katika lugha yake ya awali inapaswa kuzingatiwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu ya binadamu inapendekezwa. Hatutawajibika kwa kutoelewana au tafsiri zisizo sahihi zinazotokana na matumizi ya tafsiri hii.