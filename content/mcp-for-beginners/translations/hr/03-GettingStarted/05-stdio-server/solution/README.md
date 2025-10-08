<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e378b47e0361b7a9b0dab7a0306878c8",
  "translation_date": "2025-08-26T20:03:57+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/README.md",
  "language_code": "hr"
}
-->
# MCP stdio Server Rješenja

> **⚠️ Važno**: Ova rješenja su ažurirana kako bi koristila **stdio transport** prema preporuci MCP Specifikacije 2025-06-18. Izvorni SSE (Server-Sent Events) transport je ukinut.

Ovdje su potpuna rješenja za izgradnju MCP servera koristeći stdio transport u svakom runtimeu:

- [TypeScript](../../../../../03-GettingStarted/05-stdio-server/solution/typescript) - Potpuna implementacija stdio servera
- [Python](../../../../../03-GettingStarted/05-stdio-server/solution/python) - Python stdio server s asyncio
- [.NET](../../../../../03-GettingStarted/05-stdio-server/solution/dotnet) - .NET stdio server s dependency injection

Svako rješenje prikazuje:
- Postavljanje stdio transporta
- Definiranje alata za server
- Ispravno rukovanje JSON-RPC porukama
- Integraciju s MCP klijentima poput Claudea

Sva rješenja slijede trenutnu MCP specifikaciju i koriste preporučeni stdio transport za optimalne performanse i sigurnost.

---

**Odricanje od odgovornosti**:  
Ovaj dokument je preveden pomoću AI usluge za prevođenje [Co-op Translator](https://github.com/Azure/co-op-translator). Iako nastojimo osigurati točnost, imajte na umu da automatski prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za ključne informacije preporučuje se profesionalni prijevod od strane čovjeka. Ne preuzimamo odgovornost za bilo kakva nesporazuma ili pogrešna tumačenja koja proizlaze iz korištenja ovog prijevoda.