<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-19T17:48:06+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "hr"
}
-->
# MCP Sigurnosne Najbolje Prakse - Ažuriranje za kolovoz 2025.

> **Važno**: Ovaj dokument odražava najnovije sigurnosne zahtjeve prema [MCP Specifikaciji 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) i službene [MCP Sigurnosne Najbolje Prakse](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Uvijek se oslonite na trenutnu specifikaciju za najnovije smjernice.

## Osnovne Sigurnosne Prakse za MCP Implementacije

Model Context Protocol donosi jedinstvene sigurnosne izazove koji nadilaze tradicionalnu softversku sigurnost. Ove prakse pokrivaju temeljne sigurnosne zahtjeve i MCP-specifične prijetnje, uključujući ubrizgavanje prompta, trovanje alata, otmicu sesije, probleme zbunjenog zamjenika i ranjivosti prijenosa tokena.

### **OBAVEZNI Sigurnosni Zahtjevi**

**Ključni Zahtjevi iz MCP Specifikacije:**

> **NE SMIJE**: MCP serveri **NE SMIJU** prihvatiti bilo koje tokene koji nisu izričito izdani za MCP server  
> 
> **MORA**: MCP serveri koji implementiraju autorizaciju **MORAJU** provjeriti SVE dolazne zahtjeve  
>  
> **NE SMIJE**: MCP serveri **NE SMIJU** koristiti sesije za autentifikaciju  
>
> **MORA**: MCP proxy serveri koji koriste statične ID-ove klijenata **MORAJU** dobiti korisnički pristanak za svakog dinamički registriranog klijenta  

---

## 1. **Sigurnost Tokena i Autentifikacija**

**Kontrole Autentifikacije i Autorizacije:**  
   - **Temeljita Revizija Autorizacije**: Provedite sveobuhvatne revizije logike autorizacije MCP servera kako biste osigurali da samo namijenjeni korisnici i klijenti mogu pristupiti resursima  
   - **Integracija Vanjskih Pružatelja Identiteta**: Koristite etablirane pružatelje identiteta poput Microsoft Entra ID umjesto implementacije prilagođene autentifikacije  
   - **Validacija Publike Tokena**: Uvijek provjerite da su tokeni izričito izdani za vaš MCP server - nikada ne prihvaćajte tokene iz drugih izvora  
   - **Pravilno Upravljanje Životnim Ciklusom Tokena**: Implementirajte sigurnu rotaciju tokena, politike isteka i spriječite napade ponovnog korištenja tokena  

**Zaštićeno Pohranjivanje Tokena:**  
   - Koristite Azure Key Vault ili slične sigurne spremnike za sve tajne  
   - Implementirajte enkripciju tokena u mirovanju i tijekom prijenosa  
   - Redovita rotacija vjerodajnica i praćenje neovlaštenog pristupa  

## 2. **Upravljanje Sesijama i Sigurnost Prijenosa**

**Sigurne Prakse za Sesije:**  
   - **Kriptografski Sigurni ID-ovi Sesija**: Koristite sigurne, nedeterminističke ID-ove sesija generirane pomoću sigurnih generatora slučajnih brojeva  
   - **Veza Specifična za Korisnika**: Povežite ID-ove sesija s identitetima korisnika koristeći formate poput `<user_id>:<session_id>` kako biste spriječili zloupotrebu sesija između korisnika  
   - **Upravljanje Životnim Ciklusom Sesija**: Implementirajte pravilno isteka, rotaciju i poništavanje kako biste ograničili ranjivost  
   - **Obavezno HTTPS/TLS**: Obavezni HTTPS za svu komunikaciju kako biste spriječili presretanje ID-ova sesija  

**Sigurnost Transportnog Sloja:**  
   - Konfigurirajte TLS 1.3 gdje je moguće uz pravilno upravljanje certifikatima  
   - Implementirajte pinning certifikata za ključne veze  
   - Redovita rotacija certifikata i provjera valjanosti  

## 3. **Zaštita od AI-Specifičnih Prijetnji** 🤖

**Obrana od Ubrizgavanja Promptova:**  
   - **Microsoft Prompt Shields**: Koristite AI Prompt Shields za naprednu detekciju i filtriranje zlonamjernih uputa  
   - **Sanitizacija Ulaza**: Validirajte i sanitizirajte sve ulaze kako biste spriječili napade ubrizgavanja i probleme zbunjenog zamjenika  
   - **Granice Sadržaja**: Koristite sustave za označavanje i razgraničenje sadržaja kako biste razlikovali pouzdane upute od vanjskog sadržaja  

**Prevencija Trovanja Alata:**  
   - **Validacija Metapodataka Alata**: Implementirajte provjere integriteta za definicije alata i pratite neočekivane promjene  
   - **Dinamičko Praćenje Alata**: Pratite ponašanje tijekom izvođenja i postavite upozorenja za neočekivane obrasce izvršavanja  
   - **Radni Tokovi Odobrenja**: Zahtijevajte izričito korisničko odobrenje za izmjene alata i promjene sposobnosti  

## 4. **Kontrola Pristupa i Dozvole**

**Načelo Najmanjih Privilegija:**  
   - Dodijelite MCP serverima samo minimalne dozvole potrebne za predviđenu funkcionalnost  
   - Implementirajte kontrolu pristupa temeljenog na ulogama (RBAC) s detaljnim dozvolama  
   - Redovite revizije dozvola i kontinuirano praćenje eskalacije privilegija  

**Kontrole Dozvola Tijekom Izvršavanja:**  
   - Primijenite ograničenja resursa kako biste spriječili napade iscrpljivanja resursa  
   - Koristite izolaciju kontejnera za okruženja izvršavanja alata  
   - Implementirajte pristup "na zahtjev" za administrativne funkcije  

## 5. **Sigurnost Sadržaja i Praćenje**

**Implementacija Sigurnosti Sadržaja:**  
   - **Integracija Azure Content Safety**: Koristite Azure Content Safety za detekciju štetnog sadržaja, pokušaja jailbreaka i kršenja politika  
   - **Analiza Ponašanja**: Implementirajte praćenje ponašanja tijekom izvođenja kako biste otkrili anomalije u MCP serveru i izvršavanju alata  
   - **Sveobuhvatno Logiranje**: Zabilježite sve pokušaje autentifikacije, pozive alata i sigurnosne događaje uz sigurno, nepromjenjivo pohranjivanje  

**Kontinuirano Praćenje:**  
   - Upozorenja u stvarnom vremenu za sumnjive obrasce i pokušaje neovlaštenog pristupa  
   - Integracija sa SIEM sustavima za centralizirano upravljanje sigurnosnim događajima  
   - Redovite sigurnosne revizije i testiranje penetracije MCP implementacija  

## 6. **Sigurnost Opskrbnog Lanca**

**Verifikacija Komponenti:**  
   - **Skeniranje Ovisnosti**: Koristite automatizirano skeniranje ranjivosti za sve softverske ovisnosti i AI komponente  
   - **Validacija Porijekla**: Provjerite porijeklo, licenciranje i integritet modela, izvora podataka i vanjskih usluga  
   - **Potpisani Paketi**: Koristite kriptografski potpisane pakete i provjerite potpise prije implementacije  

**Sigurni Razvojni Procesi:**  
   - **GitHub Advanced Security**: Implementirajte skeniranje tajni, analizu ovisnosti i CodeQL statičku analizu  
   - **Sigurnost CI/CD**: Integrirajte sigurnosnu validaciju kroz automatizirane procese implementacije  
   - **Integritet Artefakata**: Implementirajte kriptografsku verifikaciju za implementirane artefakte i konfiguracije  

## 7. **Sigurnost OAuth-a i Prevencija Zbunjenog Zamjenika**

**Implementacija OAuth 2.1:**  
   - **Implementacija PKCE**: Koristite Proof Key for Code Exchange (PKCE) za sve zahtjeve za autorizaciju  
   - **Izričiti Pristanak**: Dobijte korisnički pristanak za svakog dinamički registriranog klijenta kako biste spriječili napade zbunjenog zamjenika  
   - **Validacija URI Preusmjeravanja**: Implementirajte strogu validaciju URI-ja preusmjeravanja i identifikatora klijenata  

**Sigurnost Proxyja:**  
   - Spriječite zaobilaženje autorizacije kroz iskorištavanje statičnih ID-ova klijenata  
   - Implementirajte pravilne radne tokove pristanka za pristup API-ju trećih strana  
   - Pratite krađu autorizacijskih kodova i neovlašteni pristup API-ju  

## 8. **Odgovor na Incidente i Oporavak**

**Sposobnosti Brzog Odgovora:**  
   - **Automatizirani Odgovor**: Implementirajte automatizirane sustave za rotaciju vjerodajnica i suzbijanje prijetnji  
   - **Postupci Povratka**: Sposobnost brzog vraćanja na poznate dobre konfiguracije i komponente  
   - **Forenzičke Sposobnosti**: Detaljni tragovi revizije i logiranje za istraživanje incidenata  

**Komunikacija i Koordinacija:**  
   - Jasni postupci eskalacije za sigurnosne incidente  
   - Integracija s organizacijskim timovima za odgovor na incidente  
   - Redovite simulacije sigurnosnih incidenata i vježbe na stolu  

## 9. **Usklađenost i Upravljanje**

**Regulatorna Usklađenost:**  
   - Osigurajte da MCP implementacije zadovoljavaju zahtjeve specifične za industriju (GDPR, HIPAA, SOC 2)  
   - Implementirajte kontrole klasifikacije podataka i privatnosti za obradu AI podataka  
   - Održavajte sveobuhvatnu dokumentaciju za reviziju usklađenosti  

**Upravljanje Promjenama:**  
   - Formalni procesi sigurnosne revizije za sve izmjene MCP sustava  
   - Kontrola verzija i radni tokovi odobrenja za promjene konfiguracije  
   - Redovite procjene usklađenosti i analize praznina  

## 10. **Napredne Sigurnosne Kontrole**

**Arhitektura Zero Trust:**  
   - **Nikad Ne Vjeruj, Uvijek Provjeravaj**: Kontinuirana provjera korisnika, uređaja i veza  
   - **Mikro-segmentacija**: Granularne mrežne kontrole koje izoliraju pojedine MCP komponente  
   - **Uvjetni Pristup**: Kontrole pristupa temeljene na riziku koje se prilagođavaju trenutnom kontekstu i ponašanju  

**Zaštita Aplikacija Tijekom Izvršavanja:**  
   - **Runtime Application Self-Protection (RASP)**: Implementirajte RASP tehnike za detekciju prijetnji u stvarnom vremenu  
   - **Praćenje Performansi Aplikacija**: Pratite anomalije u performansama koje mogu ukazivati na napade  
   - **Dinamičke Sigurnosne Politike**: Implementirajte sigurnosne politike koje se prilagođavaju trenutnom sigurnosnom okruženju  

## 11. **Integracija Microsoft Sigurnosnog Ekosustava**

**Sveobuhvatna Microsoft Sigurnost:**  
   - **Microsoft Defender for Cloud**: Upravljanje sigurnosnim položajem oblaka za MCP radna opterećenja  
   - **Azure Sentinel**: Cloud-native SIEM i SOAR sposobnosti za naprednu detekciju prijetnji  
   - **Microsoft Purview**: Upravljanje podacima i usklađenost za AI radne tokove i izvore podataka  

**Upravljanje Identitetom i Pristupom:**  
   - **Microsoft Entra ID**: Upravljanje identitetom u poduzeću s politikama uvjetnog pristupa  
   - **Privileged Identity Management (PIM)**: Pristup "na zahtjev" i radni tokovi odobrenja za administrativne funkcije  
   - **Zaštita Identiteta**: Uvjetni pristup temeljen na riziku i automatizirani odgovor na prijetnje  

## 12. **Kontinuirana Evolucija Sigurnosti**

**Ostati u Korak:**  
   - **Praćenje Specifikacija**: Redoviti pregled ažuriranja MCP specifikacija i promjena sigurnosnih smjernica  
   - **Obavještavanje o Prijetnjama**: Integracija AI-specifičnih izvora prijetnji i indikatora kompromitacije  
   - **Sudjelovanje u Sigurnosnoj Zajednici**: Aktivno sudjelovanje u MCP sigurnosnoj zajednici i programima za prijavu ranjivosti  

**Adaptivna Sigurnost:**  
   - **Sigurnost Temeljena na Strojnim Učenju**: Koristite modele za detekciju anomalija za identifikaciju novih obrazaca napada  
   - **Prediktivna Sigurnosna Analitika**: Implementirajte prediktivne modele za proaktivnu identifikaciju prijetnji  
   - **Automatizacija Sigurnosti**: Automatizirano ažuriranje sigurnosnih politika na temelju obavještavanja o prijetnjama i promjena specifikacija  

---

## **Ključni Sigurnosni Resursi**

### **Službena MCP Dokumentacija**  
- [MCP Specifikacija (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Sigurnosne Najbolje Prakse](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Specifikacija Autorizacije](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft Sigurnosna Rješenja**  
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Sigurnost](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Sigurnosni Standardi**  
- [OAuth 2.0 Sigurnosne Najbolje Prakse (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 za Velike Jezične Modele](https://genai.owasp.org/)  
- [NIST AI Okvir Upravljanja Rizicima](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Vodiči za Implementaciju**  
- [Azure API Management MCP Gateway za Autentifikaciju](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID s MCP Serverima](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Sigurnosna Napomena**: MCP sigurnosne prakse brzo se razvijaju. Uvijek provjerite trenutnu [MCP specifikaciju](https://spec.modelcontextprotocol.io/) i [službenu sigurnosnu dokumentaciju](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) prije implementacije.

**Odricanje od odgovornosti**:  
Ovaj dokument je preveden korištenjem AI usluge za prevođenje [Co-op Translator](https://github.com/Azure/co-op-translator). Iako nastojimo osigurati točnost, imajte na umu da automatski prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati mjerodavnim izvorom. Za ključne informacije preporučuje se profesionalni prijevod od strane stručnjaka. Ne preuzimamo odgovornost za bilo kakve nesporazume ili pogrešne interpretacije proizašle iz korištenja ovog prijevoda.