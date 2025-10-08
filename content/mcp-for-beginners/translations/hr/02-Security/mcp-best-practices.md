<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-19T17:51:31+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "hr"
}
-->
# MCP Sigurnosne Najbolje Prakse 2025

Ovaj sveobuhvatni vodič opisuje ključne sigurnosne najbolje prakse za implementaciju sustava Model Context Protocol (MCP) temeljenih na najnovijoj **MCP Specifikaciji 2025-06-18** i trenutnim industrijskim standardima. Prakse se bave tradicionalnim sigurnosnim izazovima, kao i prijetnjama specifičnim za AI koje su jedinstvene za MCP implementacije.

## Ključni Sigurnosni Zahtjevi

### Obavezne Sigurnosne Kontrole (MUST Zahtjevi)

1. **Validacija Tokena**: MCP serveri **NE SMIJU** prihvatiti tokene koji nisu izričito izdani za MCP server
2. **Provjera Autorizacije**: MCP serveri koji implementiraju autorizaciju **MORAJU** provjeriti SVE dolazne zahtjeve i **NE SMIJU** koristiti sesije za autentifikaciju  
3. **Korisnički Pristanak**: MCP proxy serveri koji koriste statične ID-ove klijenata **MORAJU** dobiti izričit pristanak korisnika za svakog dinamički registriranog klijenta
4. **Sigurni ID-ovi Sesije**: MCP serveri **MORAJU** koristiti kriptografski sigurne, nedeterminističke ID-ove sesije generirane pomoću sigurnih generatora slučajnih brojeva

## Osnovne Sigurnosne Prakse

### 1. Validacija i Sanitizacija Unosa
- **Sveobuhvatna Validacija Unosa**: Validirajte i sanitizirajte sve unose kako biste spriječili napade injekcijom, probleme s zamjenom identiteta i ranjivosti prompt injekcije
- **Provedba Sheme Parametara**: Implementirajte strogu JSON validaciju sheme za sve parametre alata i API unose
- **Filtriranje Sadržaja**: Koristite Microsoft Prompt Shields i Azure Content Safety za filtriranje zlonamjernog sadržaja u promptovima i odgovorima
- **Sanitizacija Izlaza**: Validirajte i sanitizirajte sve izlaze modela prije nego što ih predstavite korisnicima ili sustavima nizvodno

### 2. Izvrsnost u Autentifikaciji i Autorizaciji  
- **Vanjski Pružatelji Identiteta**: Delegirajte autentifikaciju etabliranim pružateljima identiteta (Microsoft Entra ID, OAuth 2.1 pružatelji) umjesto implementacije prilagođene autentifikacije
- **Fino-granularne Dozvole**: Implementirajte granularne, alat-specifične dozvole slijedeći princip najmanjeg privilegija
- **Upravljanje Životnim Ciklusom Tokena**: Koristite kratkotrajne tokene za pristup s sigurnom rotacijom i pravilnom validacijom publike
- **Višefaktorska Autentifikacija**: Zahtijevajte MFA za sav administrativni pristup i osjetljive operacije

### 3. Sigurni Komunikacijski Protokoli
- **Sigurnost Transportnog Sloja**: Koristite HTTPS/TLS 1.3 za sve MCP komunikacije uz pravilnu validaciju certifikata
- **End-to-End Enkripcija**: Implementirajte dodatne slojeve enkripcije za vrlo osjetljive podatke u prijenosu i mirovanju
- **Upravljanje Certifikatima**: Održavajte pravilno upravljanje životnim ciklusom certifikata uz automatizirane procese obnove
- **Provedba Verzije Protokola**: Koristite trenutnu verziju MCP protokola (2025-06-18) uz pravilnu pregovaranje verzije

### 4. Napredno Ograničavanje Brzine i Zaštita Resursa
- **Višeslojno Ograničavanje Brzine**: Implementirajte ograničavanje brzine na razini korisnika, sesije, alata i resursa kako biste spriječili zloupotrebu
- **Adaptivno Ograničavanje Brzine**: Koristite ograničavanje brzine temeljeno na strojnom učenju koje se prilagođava obrascima korištenja i indikatorima prijetnji
- **Upravljanje Kvotama Resursa**: Postavite odgovarajuće limite za računalne resurse, korištenje memorije i vrijeme izvršenja
- **Zaštita od DDoS Napada**: Implementirajte sveobuhvatnu zaštitu od DDoS napada i sustave analize prometa

### 5. Sveobuhvatno Logiranje i Praćenje
- **Strukturirano Logiranje Revizije**: Implementirajte detaljne, pretražive logove za sve MCP operacije, izvršenja alata i sigurnosne događaje
- **Praćenje Sigurnosti u Stvarnom Vremenu**: Koristite SIEM sustave s AI-pogonom za otkrivanje anomalija u MCP radnim opterećenjima
- **Logiranje u Skladu s Privatnošću**: Logirajte sigurnosne događaje uz poštivanje zahtjeva i regulacija privatnosti podataka
- **Integracija Odgovora na Incidente**: Povežite sustave logiranja s automatiziranim tijekovima rada za odgovor na incidente

### 6. Poboljšane Prakse Sigurnog Pohranjivanja
- **Moduli Sigurnosti Hardvera**: Koristite HSM-podržano pohranjivanje ključeva (Azure Key Vault, AWS CloudHSM) za kritične kriptografske operacije
- **Upravljanje Ključevima za Enkripciju**: Implementirajte pravilnu rotaciju, segregaciju i kontrolu pristupa za ključeve enkripcije
- **Upravljanje Tajnama**: Pohranite sve API ključeve, tokene i vjerodajnice u namjenske sustave za upravljanje tajnama
- **Klasifikacija Podataka**: Klasificirajte podatke prema razinama osjetljivosti i primijenite odgovarajuće mjere zaštite

### 7. Napredno Upravljanje Tokenima
- **Prevencija Prolaska Tokena**: Izričito zabranite obrasce prolaska tokena koji zaobilaze sigurnosne kontrole
- **Validacija Publike**: Uvijek provjerite tvrdnje o publici tokena kako bi odgovarale identitetu MCP servera
- **Autorizacija Temeljena na Tvrdnjama**: Implementirajte fino-granularnu autorizaciju temeljenu na tvrdnjama tokena i atributima korisnika
- **Vezivanje Tokena**: Vežite tokene za specifične sesije, korisnike ili uređaje gdje je to prikladno

### 8. Sigurno Upravljanje Sesijama
- **Kriptografski ID-ovi Sesije**: Generirajte ID-ove sesije pomoću kriptografski sigurnih generatora slučajnih brojeva (ne predvidivih sekvenci)
- **Vezivanje Specifično za Korisnika**: Vežite ID-ove sesije za informacije specifične za korisnika koristeći sigurne formate poput `<user_id>:<session_id>`
- **Kontrole Životnog Ciklusa Sesije**: Implementirajte pravilno isteknuće, rotaciju i poništavanje sesija
- **Sigurnosni Zaglavlja Sesije**: Koristite odgovarajuća HTTP sigurnosna zaglavlja za zaštitu sesija

### 9. Sigurnosne Kontrole Specifične za AI
- **Obrana od Prompt Injekcije**: Koristite Microsoft Prompt Shields s tehnikama osvjetljavanja, razdjelnika i označavanja podataka
- **Prevencija Trovanja Alata**: Validirajte metapodatke alata, pratite dinamičke promjene i provjerite integritet alata
- **Validacija Izlaza Modela**: Skenirajte izlaze modela za potencijalno curenje podataka, štetan sadržaj ili kršenje sigurnosnih politika
- **Zaštita Kontekstnog Prozora**: Implementirajte kontrole za sprječavanje trovanja kontekstnog prozora i manipulacijskih napada

### 10. Sigurnost Izvršenja Alata
- **Izolacija Izvršenja**: Pokrenite izvršenja alata u kontejneriziranim, izoliranim okruženjima s ograničenjima resursa
- **Razdvajanje Privilegija**: Izvršavajte alate s minimalno potrebnim privilegijama i odvojenim korisničkim računima
- **Izolacija Mreže**: Implementirajte segmentaciju mreže za okruženja izvršenja alata
- **Praćenje Izvršenja**: Pratite izvršenje alata za anomalno ponašanje, korištenje resursa i sigurnosne povrede

### 11. Kontinuirana Validacija Sigurnosti
- **Automatizirano Sigurnosno Testiranje**: Integrirajte sigurnosno testiranje u CI/CD procese pomoću alata poput GitHub Advanced Security
- **Upravljanje Ranjivostima**: Redovito skenirajte sve ovisnosti, uključujući AI modele i vanjske usluge
- **Penetracijsko Testiranje**: Provodite redovite sigurnosne procjene usmjerene na MCP implementacije
- **Pregledi Sigurnosnog Koda**: Implementirajte obavezne sigurnosne preglede za sve promjene koda povezane s MCP-om

### 12. Sigurnost Opskrbnog Lanca za AI
- **Verifikacija Komponenti**: Provjerite porijeklo, integritet i sigurnost svih AI komponenti (modeli, ugrađivanja, API-ji)
- **Upravljanje Ovisnostima**: Održavajte trenutne inventare svih softverskih i AI ovisnosti uz praćenje ranjivosti
- **Pouzdani Repozitoriji**: Koristite verificirane, pouzdane izvore za sve AI modele, biblioteke i alate
- **Praćenje Opskrbnog Lanca**: Kontinuirano pratite kompromise kod AI pružatelja usluga i repozitorija modela

## Napredni Sigurnosni Obrasci

### Zero Trust Arhitektura za MCP
- **Nikad Ne Vjeruj, Uvijek Provjeri**: Implementirajte kontinuiranu verifikaciju za sve MCP sudionike
- **Mikro-segmentacija**: Izolirajte MCP komponente uz granularne mrežne i identitetske kontrole
- **Uvjetni Pristup**: Implementirajte kontrole pristupa temeljene na riziku koje se prilagođavaju kontekstu i ponašanju
- **Kontinuirana Procjena Rizika**: Dinamički procjenjujte sigurnosni položaj na temelju trenutnih indikatora prijetnji

### Implementacija AI-a uz Očuvanje Privatnosti
- **Minimizacija Podataka**: Izlažite samo minimalno potrebne podatke za svaku MCP operaciju
- **Diferencijalna Privatnost**: Implementirajte tehnike očuvanja privatnosti za obradu osjetljivih podataka
- **Homomorfna Enkripcija**: Koristite napredne tehnike enkripcije za sigurnu obradu na enkriptiranim podacima
- **Federativno Učenje**: Implementirajte distribuirane pristupe učenju koji čuvaju lokalitet podataka i privatnost

### Odgovor na Incidente za AI Sustave
- **Postupci Specifični za AI Incidente**: Razvijte postupke odgovora na incidente prilagođene prijetnjama specifičnim za AI i MCP
- **Automatizirani Odgovor**: Implementirajte automatizirano ograničavanje i sanaciju za uobičajene AI sigurnosne incidente  
- **Forenzičke Sposobnosti**: Održavajte spremnost za forenzičku analizu kompromisa AI sustava i curenja podataka
- **Postupci Oporavka**: Uspostavite postupke za oporavak od trovanja AI modela, napada prompt injekcije i kompromisa usluga

## Resursi za Implementaciju i Standardi

### Službena MCP Dokumentacija
- [MCP Specifikacija 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Trenutna MCP specifikacija protokola
- [MCP Sigurnosne Najbolje Prakse](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Službene sigurnosne smjernice
- [MCP Specifikacija Autorizacije](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Obrasci autentifikacije i autorizacije
- [MCP Sigurnost Transporta](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Zahtjevi sigurnosti transportnog sloja

### Microsoft Sigurnosna Rješenja
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Napredna zaštita od prompt injekcije
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Sveobuhvatno filtriranje AI sadržaja
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Upravljanje identitetom i pristupom za poduzeća
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Sigurno upravljanje tajnama i vjerodajnicama
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Sigurnosno skeniranje opskrbnog lanca i koda

### Sigurnosni Standardi i Okviri
- [OAuth 2.1 Sigurnosne Najbolje Prakse](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Trenutne smjernice za OAuth sigurnost
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Sigurnosni rizici web aplikacija
- [OWASP Top 10 za LLM](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Sigurnosni rizici specifični za AI
- [NIST AI Okvir Upravljanja Rizicima](https://www.nist.gov/itl/ai-risk-management-framework) - Sveobuhvatno upravljanje rizicima za AI
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Sustavi upravljanja informacijskom sigurnošću

### Vodiči za Implementaciju i Tutorijali
- [Azure API Management kao MCP Auth Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Obrasci autentifikacije za poduzeća
- [Microsoft Entra ID s MCP Serverima](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integracija pružatelja identiteta
- [Implementacija Sigurnog Pohranjivanja Tokena](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Najbolje prakse upravljanja tokenima
- [End-to-End Enkripcija za AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Napredni obrasci enkripcije

### Napredni Sigurnosni Resursi
- [Microsoft Sigurnosni Razvojni Ciklus](https://www.microsoft.com/sdl) - Prakse sigurnog razvoja
- [AI Red Team Smjernice](https://learn.microsoft.com/security/ai-red-team/) - Sigurnosno testiranje specifično za AI
- [Modeliranje Prijetnji za AI Sustave](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Metodologija modeliranja prijetnji za AI
- [Inženjering Privatnosti za AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Tehnike očuvanja privatnosti za AI

### Usklađenost i Upravljanje
- [GDPR Usklađenost za AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Usklađenost privatnosti u AI sustavima
- [Okvir Upravljanja AI](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Implementacija odgovornog AI-a
- [SOC 2 za AI Usluge](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Sigurnosne kontrole za pružatelje AI usluga
- [HIPAA Usklađenost za AI](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Zahtjevi usklađenosti za AI u zdravstvu

### DevSecOps i Automatizacija
- [DevSecOps Cjevovod za AI](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Sigurni razvojni cjevovodi za AI
- [Automatizirano Sigurnosno Testiranje](https://learn.microsoft.com/security/engineering/devsecops) - Kontinuirana validacija sigurnosti
- [Sigurnost Infrastrukture kao Koda](https://learn.microsoft.com/security/engineering/infrastructure-security) - Sigurno postavljanje infrastrukture
- [Sigurnost Kontejnera za AI](https
- **Razvoj alata**: Razvijajte i dijelite sigurnosne alate i biblioteke za MCP ekosustav

---

*Ovaj dokument odražava najbolje sigurnosne prakse MCP-a od 18. kolovoza 2025., temeljene na MCP specifikaciji 2025-06-18. Sigurnosne prakse trebaju se redovito pregledavati i ažurirati kako se protokol i prijetnje razvijaju.*

**Odricanje od odgovornosti**:  
Ovaj dokument je preveden korištenjem AI usluge za prijevod [Co-op Translator](https://github.com/Azure/co-op-translator). Iako nastojimo osigurati točnost, imajte na umu da automatski prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati mjerodavnim izvorom. Za ključne informacije preporučuje se profesionalni prijevod od strane ljudskog prevoditelja. Ne preuzimamo odgovornost za bilo kakva nesporazuma ili pogrešna tumačenja koja mogu proizaći iz korištenja ovog prijevoda.