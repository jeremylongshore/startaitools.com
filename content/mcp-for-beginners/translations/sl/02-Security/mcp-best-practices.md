<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-19T18:17:20+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "sl"
}
-->
# MCP Varnostne Najboljše Prakse 2025

Ta obsežen vodnik opisuje ključne varnostne najboljše prakse za implementacijo sistemov Model Context Protocol (MCP) na podlagi najnovejše **MCP Specifikacije 2025-06-18** in trenutnih industrijskih standardov. Prakse obravnavajo tako tradicionalne varnostne izzive kot tudi grožnje, specifične za umetno inteligenco, ki so edinstvene za MCP implementacije.

## Ključne Varnostne Zahteve

### Obvezni Varnostni Nadzori (Zahteve MUST)

1. **Validacija žetonov**: MCP strežniki **NE SMEJO** sprejemati žetonov, ki niso bili izrecno izdani za sam MCP strežnik.
2. **Preverjanje avtorizacije**: MCP strežniki, ki izvajajo avtorizacijo, **MORAJO** preveriti VSE dohodne zahteve in **NE SMEJO** uporabljati sej za avtentikacijo.  
3. **Uporabniško soglasje**: MCP proxy strežniki, ki uporabljajo statične ID-je odjemalcev, **MORAJO** pridobiti izrecno soglasje uporabnika za vsakega dinamično registriranega odjemalca.
4. **Varni ID-ji sej**: MCP strežniki **MORAJO** uporabljati kriptografsko varne, nedeterministične ID-je sej, ustvarjene z varnimi generatorji naključnih števil.

## Osnovne Varnostne Prakse

### 1. Validacija in Sanitizacija Vnosov
- **Celovita validacija vnosov**: Validirajte in sanitizirajte vse vnose, da preprečite napade z vnosom, težave z zmedenimi pooblaščenci in ranljivosti zaradi vnosov v pozive.
- **Uveljavljanje sheme parametrov**: Uporabite strogo validacijo JSON shem za vse parametre orodij in API vnose.
- **Filtriranje vsebine**: Uporabite Microsoft Prompt Shields in Azure Content Safety za filtriranje zlonamerne vsebine v pozivih in odgovorih.
- **Sanitizacija izhodov**: Validirajte in sanitizirajte vse izhode modela, preden jih predstavite uporabnikom ali sistemom navzdol.

### 2. Odličnost v Avtentikaciji in Avtorizaciji  
- **Zunanji ponudniki identitete**: Avtentikacijo delegirajte uveljavljenim ponudnikom identitete (Microsoft Entra ID, ponudniki OAuth 2.1) namesto implementacije lastne avtentikacije.
- **Drobnozrnata dovoljenja**: Implementirajte granularna, orodju specifična dovoljenja po načelu najmanjših privilegijev.
- **Upravljanje življenjskega cikla žetonov**: Uporabljajte kratkožive dostopne žetone z varno rotacijo in pravilno validacijo občinstva.
- **Večfaktorska avtentikacija**: Zahtevajte MFA za ves administrativni dostop in občutljive operacije.

### 3. Varni Komunikacijski Protokoli
- **Transportna plastna varnost**: Uporabljajte HTTPS/TLS 1.3 za vse MCP komunikacije z ustrezno validacijo certifikatov.
- **Šifriranje od konca do konca**: Implementirajte dodatne sloje šifriranja za zelo občutljive podatke v prenosu in mirovanju.
- **Upravljanje certifikatov**: Vzdržujte pravilno upravljanje življenjskega cikla certifikatov z avtomatiziranimi postopki obnove.
- **Uveljavljanje različice protokola**: Uporabljajte trenutno različico MCP protokola (2025-06-18) z ustreznim pogajanjem o različici.

### 4. Napredno Omejevanje Hitrosti in Zaščita Virov
- **Večplastno omejevanje hitrosti**: Implementirajte omejevanje hitrosti na ravni uporabnika, seje, orodja in virov za preprečevanje zlorab.
- **Prilagodljivo omejevanje hitrosti**: Uporabljajte omejevanje hitrosti, ki temelji na strojni inteligenci in se prilagaja vzorcem uporabe ter indikatorjem groženj.
- **Upravljanje kvot virov**: Nastavite ustrezne omejitve za računske vire, porabo pomnilnika in čas izvajanja.
- **Zaščita pred DDoS**: Uvedite celovite sisteme za zaščito pred DDoS in analizo prometa.

### 5. Celovito Beleženje in Spremljanje
- **Strukturirano beleženje revizij**: Implementirajte podrobne, iskalne dnevnike za vse MCP operacije, izvajanja orodij in varnostne dogodke.
- **Spremljanje varnosti v realnem času**: Uvedite SIEM sisteme z AI-podprtim zaznavanjem anomalij za MCP delovne obremenitve.
- **Beleženje skladno z zasebnostjo**: Beležite varnostne dogodke ob spoštovanju zahtev in predpisov o zasebnosti podatkov.
- **Integracija odziva na incidente**: Povežite sisteme beleženja z avtomatiziranimi poteki dela za odziv na incidente.

### 6. Izboljšane Prakse Varnega Shranjevanja
- **Strojne varnostne module**: Uporabljajte HSM-podprto shranjevanje ključev (Azure Key Vault, AWS CloudHSM) za ključne kriptografske operacije.
- **Upravljanje šifrirnih ključev**: Implementirajte pravilno rotacijo ključev, ločevanje in nadzor dostopa za šifrirne ključe.
- **Upravljanje skrivnosti**: Shranjujte vse API ključe, žetone in poverilnice v namenskih sistemih za upravljanje skrivnosti.
- **Razvrščanje podatkov**: Razvrstite podatke glede na stopnjo občutljivosti in uporabite ustrezne zaščitne ukrepe.

### 7. Napredno Upravljanje Žetonov
- **Preprečevanje posredovanja žetonov**: Izrecno prepovejte vzorce posredovanja žetonov, ki obidejo varnostne nadzore.
- **Validacija občinstva**: Vedno preverite, ali trditve o občinstvu žetona ustrezajo identiteti predvidenega MCP strežnika.
- **Avtorizacija na podlagi trditev**: Implementirajte drobnozrnato avtorizacijo na podlagi trditev žetonov in atributov uporabnikov.
- **Vezava žetonov**: Žetone vežite na specifične seje, uporabnike ali naprave, kjer je to primerno.

### 8. Varno Upravljanje Sej
- **Kriptografski ID-ji sej**: Ustvarjajte ID-je sej z uporabo kriptografsko varnih generatorjev naključnih števil (nepredvidljivih zaporedij).
- **Vezava na uporabnika**: ID-je sej vežite na uporabniško specifične informacije z uporabo varnih formatov, kot je `<user_id>:<session_id>`.
- **Nadzor življenjskega cikla sej**: Implementirajte pravilno potekanje, rotacijo in razveljavitev sej.
- **Varnostni glavi sej**: Uporabljajte ustrezne HTTP varnostne glave za zaščito sej.

### 9. Varnostni Nadzori Specifični za AI
- **Obramba pred vnosom v pozive**: Uvedite Microsoft Prompt Shields z osvetljevanjem, ločili in tehnikami označevanja podatkov.
- **Preprečevanje zastrupitve orodij**: Validirajte metapodatke orodij, spremljajte dinamične spremembe in preverjajte integriteto orodij.
- **Validacija izhodov modela**: Preverjajte izhode modela za morebitno uhajanje podatkov, škodljivo vsebino ali kršitve varnostnih politik.
- **Zaščita kontekstnega okna**: Implementirajte nadzore za preprečevanje zastrupitve in manipulacije kontekstnega okna.

### 10. Varnost Izvajanja Orodij
- **Izolacija izvajanja**: Izvajajte orodja v vsebniških, izoliranih okoljih z omejitvami virov.
- **Ločevanje privilegijev**: Izvajajte orodja z minimalno potrebnimi privilegiji in ločenimi uporabniškimi računi.
- **Omrežna izolacija**: Implementirajte segmentacijo omrežja za okolja izvajanja orodij.
- **Spremljanje izvajanja**: Spremljajte izvajanje orodij za nenavadno vedenje, porabo virov in varnostne kršitve.

### 11. Nenehna Varnostna Validacija
- **Avtomatizirano varnostno testiranje**: Integrirajte varnostno testiranje v CI/CD procese z orodji, kot je GitHub Advanced Security.
- **Upravljanje ranljivosti**: Redno pregledujte vse odvisnosti, vključno z AI modeli in zunanjimi storitvami.
- **Penetracijsko testiranje**: Redno izvajajte varnostne ocene, posebej usmerjene na MCP implementacije.
- **Pregledi varnostne kode**: Implementirajte obvezne varnostne preglede za vse spremembe kode, povezane z MCP.

### 12. Varnost Dobavne Verige za AI
- **Preverjanje komponent**: Preverjajte izvor, integriteto in varnost vseh AI komponent (modelov, vdelav, API-jev).
- **Upravljanje odvisnosti**: Vzdržujte trenutne inventarje vseh programske opreme in AI odvisnosti z sledenjem ranljivostim.
- **Zaupanja vredni repozitoriji**: Uporabljajte preverjene, zaupanja vredne vire za vse AI modele, knjižnice in orodja.
- **Spremljanje dobavne verige**: Nenehno spremljajte morebitne kompromise pri ponudnikih AI storitev in repozitorijih modelov.

## Napredni Varnostni Vzorci

### Arhitektura Zero Trust za MCP
- **Nikoli ne zaupaj, vedno preveri**: Implementirajte stalno preverjanje za vse MCP udeležence.
- **Mikrosegmentacija**: Izolirajte MCP komponente z granularnimi omrežnimi in identitetnimi nadzori.
- **Pogojni dostop**: Implementirajte nadzore dostopa, ki temeljijo na tveganju in se prilagajajo kontekstu ter vedenju.
- **Nenehna ocena tveganja**: Dinamično ocenjujte varnostno stanje na podlagi trenutnih indikatorjev groženj.

### Implementacija AI z Ohranjanjem Zasebnosti
- **Minimizacija podatkov**: Razkrijte le minimalno potrebne podatke za vsako MCP operacijo.
- **Diferencialna zasebnost**: Implementirajte tehnike za ohranjanje zasebnosti pri obdelavi občutljivih podatkov.
- **Homomorfno šifriranje**: Uporabljajte napredne šifrirne tehnike za varno računanje na šifriranih podatkih.
- **Federativno učenje**: Implementirajte porazdeljene pristope učenja, ki ohranjajo lokalnost in zasebnost podatkov.

### Odziv na Incidente za AI Sisteme
- **Postopki za incidente specifične za AI**: Razvijte postopke za odziv na incidente, prilagojene grožnjam, specifičnim za AI in MCP.
- **Avtomatiziran odziv**: Implementirajte avtomatizirano zadrževanje in sanacijo za pogoste AI varnostne incidente.  
- **Forenzične zmogljivosti**: Vzdržujte pripravljenost na forenzične preiskave za kompromise AI sistemov in kršitve podatkov.
- **Postopki za obnovitev**: Ustanovite postopke za obnovitev po zastrupitvi AI modelov, napadih z vnosom v pozive in kompromisih storitev.

## Viri za Implementacijo in Standardi

### Uradna MCP Dokumentacija
- [MCP Specifikacija 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Trenutna MCP specifikacija protokola
- [MCP Varnostne Najboljše Prakse](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Uradna varnostna navodila
- [MCP Specifikacija Avtorizacije](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Vzorci avtentikacije in avtorizacije
- [MCP Transportna Varnost](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Zahteve za varnost transportne plasti

### Microsoft Varnostne Rešitve
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Napredna zaščita pred vnosom v pozive
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Celovito filtriranje vsebine AI
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Upravljanje identitete in dostopa za podjetja
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Varno upravljanje skrivnosti in poverilnic
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Pregledovanje varnosti kode in dobavne verige

### Standardi in Okviri za Varnost
- [OAuth 2.1 Varnostne Najboljše Prakse](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Trenutna navodila za varnost OAuth
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Tveganja za spletne aplikacije
- [OWASP Top 10 za LLM-je](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Tveganja specifična za AI
- [NIST Okvir za Upravljanje Tveganj AI](https://www.nist.gov/itl/ai-risk-management-framework) - Celovito upravljanje tveganj AI
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Sistemi za upravljanje informacijske varnosti

### Vodniki za Implementacijo in Vadnice
- [Azure API Management kot MCP Avtorizacijski Prehod](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Vzorci avtentikacije za podjetja
- [Microsoft Entra ID z MCP Strežniki](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integracija ponudnika identitete
- [Implementacija Varnega Shranjevanja Žetonov](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Najboljše prakse za upravljanje žetonov
- [Šifriranje od Konca do Konca za AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Napredni vzorci šifriranja

### Napredni Varnostni Viri
- [Microsoftov Varnostni Razvojni Ciklus](https://www.microsoft.com/sdl) - Prakse za varen razvoj
- [Vodnik za AI Rdeče Ekipe](https://learn.microsoft.com/security/ai-red-team/) - Testiranje varnosti specifično za AI
- [Modeliranje Groženj za AI Sisteme](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Metodologija za modeliranje groženj AI
- [Inženiring Zasebnosti za AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Tehnike za ohranjanje zasebnosti AI

### Skladnost in Upravljanje
- [Skladnost z GDPR za AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Skladnost zasebnosti v AI sistemih
- [Okvir za Upravljanje AI](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Implementacija odgovorne AI
- [SOC 2 za AI Storitve](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Varnostni nadzori za ponudnike AI storitev
- [Skladnost z HIPAA za AI](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Zahteve za skladnost AI v zdravstvu

### DevSecOps in Avtomatizacija
- [DevSecOps Cevovod za AI](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Varni razvojni cevovodi za AI
- [Avtomatizirano Varnostno Testiranje](https://learn.microsoft.com/security/engineering/devsecops) - Nene
- **Razvoj orodij**: Razvijajte in delite varnostna orodja ter knjižnice za ekosistem MCP

---

*Ta dokument odraža najboljše prakse za varnost MCP na dan 18. avgust 2025, skladno s specifikacijo MCP 2025-06-18. Varnostne prakse je treba redno pregledovati in posodabljati, saj se protokol in grožnje nenehno razvijajo.*

**Omejitev odgovornosti**:  
Ta dokument je bil preveden z uporabo storitve za strojno prevajanje [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas opozarjamo, da lahko avtomatizirani prevodi vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za ključne informacije priporočamo strokovno človeško prevajanje. Ne prevzemamo odgovornosti za morebitna nesporazumevanja ali napačne razlage, ki izhajajo iz uporabe tega prevoda.