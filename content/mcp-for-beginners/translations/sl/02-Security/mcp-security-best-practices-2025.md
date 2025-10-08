<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-19T18:13:12+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "sl"
}
-->
# MCP Varnostne najboljše prakse - Posodobitev avgust 2025

> **Pomembno**: Ta dokument odraža najnovejše varnostne zahteve [MCP Specifikacije 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) in uradne [MCP Varnostne najboljše prakse](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Vedno se sklicujte na trenutno specifikacijo za najnovejše smernice.

## Ključne varnostne prakse za implementacije MCP

Model Context Protocol prinaša edinstvene varnostne izzive, ki presegajo tradicionalno programsko varnost. Te prakse obravnavajo tako osnovne varnostne zahteve kot tudi MCP-specifične grožnje, vključno z vbrizgavanjem ukazov, zastrupljanjem orodij, ugrabitvijo sej, težavami z zmedenim namestnikom in ranljivostmi pri posredovanju žetonov.

### **OBVEZNE varnostne zahteve**

**Ključne zahteve iz MCP specifikacije:**

> **NE SME**: MCP strežniki **NE SMEJO** sprejemati žetonov, ki niso bili izrecno izdani za MCP strežnik  
> 
> **MORA**: MCP strežniki, ki izvajajo avtorizacijo, **MORAJO** preveriti VSE dohodne zahteve  
>  
> **NE SME**: MCP strežniki **NE SMEJO** uporabljati sej za avtentikacijo  
>
> **MORA**: MCP posredniški strežniki, ki uporabljajo statične ID-je strank, **MORAJO** pridobiti soglasje uporabnika za vsako dinamično registrirano stranko  

---

## 1. **Varnost žetonov in avtentikacija**

**Kontrole avtentikacije in avtorizacije:**
   - **Temeljit pregled avtorizacije**: Izvedite celovite preglede avtorizacijske logike MCP strežnika, da zagotovite, da lahko vire dostopajo le predvideni uporabniki in stranke  
   - **Integracija zunanjih ponudnikov identitete**: Uporabljajte uveljavljene ponudnike identitete, kot je Microsoft Entra ID, namesto lastne implementacije avtentikacije  
   - **Preverjanje občinstva žetonov**: Vedno preverite, da so bili žetoni izrecno izdani za vaš MCP strežnik - nikoli ne sprejemajte žetonov iz drugih virov  
   - **Pravilno upravljanje življenjskega cikla žetonov**: Implementirajte varno rotacijo žetonov, politike poteka veljavnosti in preprečite napade z ponovnim predvajanjem žetonov  

**Zaščitena hramba žetonov:**
   - Uporabljajte Azure Key Vault ali podobne varne shrambe poverilnic za vse skrivnosti  
   - Implementirajte šifriranje žetonov tako v mirovanju kot med prenosom  
   - Redna rotacija poverilnic in spremljanje nepooblaščenega dostopa  

## 2. **Upravljanje sej in varnost prenosa**

**Varne prakse sej:**
   - **Kriptografsko varni ID-ji sej**: Uporabljajte varne, nedeterministične ID-je sej, ustvarjene z varnimi generatorji naključnih števil  
   - **Vezava na uporabnika**: Povežite ID-je sej z identitetami uporabnikov z uporabo formatov, kot je `<user_id>:<session_id>`, da preprečite zlorabo sej med uporabniki  
   - **Upravljanje življenjskega cikla sej**: Implementirajte pravilno potekanje, rotacijo in razveljavitev sej za omejitev ranljivostnih oken  
   - **Uveljavljanje HTTPS/TLS**: Obvezna uporaba HTTPS za vso komunikacijo, da preprečite prestrezanje ID-jev sej  

**Varnost transportne plasti:**
   - Konfigurirajte TLS 1.3, kjer je mogoče, z ustreznim upravljanjem certifikatov  
   - Implementirajte pripenjanje certifikatov za kritične povezave  
   - Redna rotacija certifikatov in preverjanje veljavnosti  

## 3. **Zaščita pred AI-specifičnimi grožnjami** 🤖

**Obramba pred vbrizgavanjem ukazov:**
   - **Microsoft Prompt Shields**: Uporabljajte AI Prompt Shields za napredno zaznavanje in filtriranje zlonamernih navodil  
   - **Sanitizacija vhodov**: Preverjajte in čistite vse vnose, da preprečite napade z vbrizgavanjem in težave z zmedenim namestnikom  
   - **Meje vsebine**: Uporabljajte sisteme za ločevanje in označevanje podatkov, da ločite zaupanja vredna navodila od zunanje vsebine  

**Preprečevanje zastrupljanja orodij:**
   - **Preverjanje metapodatkov orodij**: Implementirajte preverjanje celovitosti definicij orodij in spremljajte nepričakovane spremembe  
   - **Dinamično spremljanje orodij**: Spremljajte vedenje med izvajanjem in nastavite opozarjanje za nepričakovane vzorce izvajanja  
   - **Delovni tokovi odobritve**: Zahtevajte izrecno odobritev uporabnika za spremembe orodij in njihovih zmožnosti  

## 4. **Nadzor dostopa in dovoljenja**

**Načelo najmanjših privilegijev:**
   - MCP strežnikom dodelite le minimalna dovoljenja, potrebna za predvideno funkcionalnost  
   - Implementirajte nadzor dostopa na podlagi vlog (RBAC) z natančno določenimi dovoljenji  
   - Redni pregledi dovoljenj in stalno spremljanje za eskalacijo privilegijev  

**Kontrole dovoljenj med izvajanjem:**
   - Uporabljajte omejitve virov za preprečevanje napadov z izčrpavanjem virov  
   - Uporabljajte izolacijo vsebnikov za okolja izvajanja orodij  
   - Implementirajte dostop "just-in-time" za administrativne funkcije  

## 5. **Varnost vsebine in spremljanje**

**Implementacija varnosti vsebine:**
   - **Integracija Azure Content Safety**: Uporabljajte Azure Content Safety za zaznavanje škodljive vsebine, poskusov izogibanja pravilom in kršitev politik  
   - **Vedenjska analiza**: Implementirajte spremljanje vedenja med izvajanjem za zaznavanje anomalij v MCP strežniku in izvajanju orodij  
   - **Celovito beleženje**: Beležite vse poskuse avtentikacije, klice orodij in varnostne dogodke z varno, nepoškodljivo hrambo  

**Neprekinjeno spremljanje:**
   - Opozorila v realnem času za sumljive vzorce in poskuse nepooblaščenega dostopa  
   - Integracija s sistemi SIEM za centralizirano upravljanje varnostnih dogodkov  
   - Redni varnostni pregledi in penetracijsko testiranje implementacij MCP  

## 6. **Varnost dobavne verige**

**Preverjanje komponent:**
   - **Skeniranje odvisnosti**: Uporabljajte avtomatizirano skeniranje ranljivosti za vse programske odvisnosti in AI komponente  
   - **Preverjanje izvora**: Preverite izvor, licenciranje in celovitost modelov, virov podatkov in zunanjih storitev  
   - **Podpisani paketi**: Uporabljajte kriptografsko podpisane pakete in preverite podpise pred uvajanjem  

**Varna razvojna cevovoda:**
   - **GitHub Advanced Security**: Implementirajte skeniranje skrivnosti, analizo odvisnosti in statično analizo CodeQL  
   - **Varnost CI/CD**: Integrirajte varnostno preverjanje skozi avtomatizirane cevovode uvajanja  
   - **Celovitost artefaktov**: Implementirajte kriptografsko preverjanje za uvedene artefakte in konfiguracije  

## 7. **OAuth varnost in preprečevanje zmedenega namestnika**

**Implementacija OAuth 2.1:**
   - **Implementacija PKCE**: Uporabljajte Proof Key for Code Exchange (PKCE) za vse avtorizacijske zahteve  
   - **Izrecno soglasje**: Pridobite soglasje uporabnika za vsako dinamično registrirano stranko, da preprečite napade zmedenega namestnika  
   - **Preverjanje preusmeritvenih URI-jev**: Implementirajte strogo preverjanje preusmeritvenih URI-jev in identifikatorjev strank  

**Varnost posrednikov:**
   - Preprečite obvode avtorizacije z izkoriščanjem statičnih ID-jev strank  
   - Implementirajte ustrezne delovne tokove soglasja za dostop do API-jev tretjih oseb  
   - Spremljajte krajo avtorizacijskih kod in nepooblaščen dostop do API-jev  

## 8. **Odziv na incidente in okrevanje**

**Sposobnosti hitrega odziva:**
   - **Avtomatiziran odziv**: Implementirajte avtomatizirane sisteme za rotacijo poverilnic in zajezitev groženj  
   - **Postopki povrnitve**: Sposobnost hitrega vračanja na znane dobre konfiguracije in komponente  
   - **Forenzične sposobnosti**: Podrobne revizijske sledi in beleženje za preiskavo incidentov  

**Komunikacija in koordinacija:**
   - Jasni postopki za eskalacijo varnostnih incidentov  
   - Integracija z organizacijskimi ekipami za odziv na incidente  
   - Redne simulacije varnostnih incidentov in vaje na papirju  

## 9. **Skladnost in upravljanje**

**Regulativna skladnost:**
   - Zagotovite, da implementacije MCP izpolnjujejo zahteve specifične za industrijo (GDPR, HIPAA, SOC 2)  
   - Implementirajte klasifikacijo podatkov in nadzore zasebnosti za obdelavo AI podatkov  
   - Vzdržujte celovito dokumentacijo za revizije skladnosti  

**Upravljanje sprememb:**
   - Formalni varnostni pregledi za vse spremembe MCP sistema  
   - Nadzor različic in delovni tokovi odobritve za spremembe konfiguracije  
   - Redne ocene skladnosti in analize vrzeli  

## 10. **Napredni varnostni nadzori**

**Arhitektura Zero Trust:**
   - **Nikoli ne zaupaj, vedno preveri**: Nenehno preverjanje uporabnikov, naprav in povezav  
   - **Mikrosegmentacija**: Granularni omrežni nadzori za izolacijo posameznih komponent MCP  
   - **Pogojni dostop**: Nadzori dostopa na podlagi tveganja, prilagojeni trenutnemu kontekstu in vedenju  

**Zaščita aplikacij med izvajanjem:**
   - **Runtime Application Self-Protection (RASP)**: Uporabljajte tehnike RASP za zaznavanje groženj v realnem času  
   - **Spremljanje zmogljivosti aplikacij**: Spremljajte zmogljivostne anomalije, ki lahko nakazujejo napade  
   - **Dinamične varnostne politike**: Implementirajte varnostne politike, ki se prilagajajo trenutni grožnji  

## 11. **Integracija z Microsoftovim varnostnim ekosistemom**

**Celovita Microsoftova varnost:**
   - **Microsoft Defender for Cloud**: Upravljanje varnostne drže v oblaku za delovne obremenitve MCP  
   - **Azure Sentinel**: Cloud-native SIEM in SOAR zmogljivosti za napredno zaznavanje groženj  
   - **Microsoft Purview**: Upravljanje podatkov in skladnost za AI delovne tokove in vire podatkov  

**Upravljanje identitete in dostopa:**
   - **Microsoft Entra ID**: Upravljanje identitete podjetja s politikami pogojnega dostopa  
   - **Privileged Identity Management (PIM)**: Dostop "just-in-time" in delovni tokovi odobritve za administrativne funkcije  
   - **Zaščita identitete**: Pogojni dostop na podlagi tveganja in avtomatiziran odziv na grožnje  

## 12. **Neprekinjen razvoj varnosti**

**Ostajanje na tekočem:**
   - **Spremljanje specifikacij**: Redni pregledi posodobitev MCP specifikacij in sprememb varnostnih smernic  
   - **Obveščanje o grožnjah**: Integracija AI-specifičnih virov groženj in indikatorjev kompromisa  
   - **Sodelovanje v varnostni skupnosti**: Aktivno sodelovanje v MCP varnostni skupnosti in programih za razkritje ranljivosti  

**Prilagodljiva varnost:**
   - **Varnost strojnega učenja**: Uporabljajte zaznavanje anomalij na osnovi strojnega učenja za prepoznavanje novih vzorcev napadov  
   - **Prediktivna varnostna analitika**: Implementirajte prediktivne modele za proaktivno prepoznavanje groženj  
   - **Avtomatizacija varnosti**: Avtomatizirane posodobitve varnostnih politik na podlagi obveščanja o grožnjah in sprememb specifikacij  

---

## **Ključni varnostni viri**

### **Uradna dokumentacija MCP**
- [MCP Specifikacija (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Varnostne najboljše prakse](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Specifikacija avtorizacije](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoftove varnostne rešitve**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Varnost](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Varnostni standardi**
- [OAuth 2.0 Varnostne najboljše prakse (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 za velike jezikovne modele](https://genai.owasp.org/)  
- [NIST Okvir za upravljanje tveganj AI](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Vodiči za implementacijo**
- [Azure API Management MCP Avtentikacijski prehod](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID z MCP strežniki](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Varnostno obvestilo**: Varnostne prakse MCP se hitro razvijajo. Vedno preverite trenutno [MCP specifikacijo](https://spec.modelcontextprotocol.io/) in [uradno varnostno dokumentacijo](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) pred implementacijo.

**Omejitev odgovornosti**:  
Ta dokument je bil preveden z uporabo storitve za strojno prevajanje [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas opozarjamo, da lahko avtomatizirani prevodi vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za ključne informacije priporočamo strokovno človeško prevajanje. Ne prevzemamo odgovornosti za morebitna nesporazumevanja ali napačne razlage, ki izhajajo iz uporabe tega prevoda.