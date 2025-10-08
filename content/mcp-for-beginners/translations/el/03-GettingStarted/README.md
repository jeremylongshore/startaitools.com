<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "f400d87053221363769113c24f117248",
  "translation_date": "2025-10-06T23:08:41+00:00",
  "source_file": "03-GettingStarted/README.md",
  "language_code": "el"
}
-->
## Ξεκινώντας  

[![Δημιουργήστε τον πρώτο σας MCP Server](../../../translated_images/04.0ea920069efd979a0b2dad51e72c1df7ead9c57b3305796068a6cee1f0dd6674.el.png)](https://youtu.be/sNDZO9N4m9Y)

_(Κάντε κλικ στην εικόνα παραπάνω για να δείτε το βίντεο αυτού του μαθήματος)_

Αυτή η ενότητα αποτελείται από αρκετά μαθήματα:

- **1 Ο πρώτος σας server**, σε αυτό το πρώτο μάθημα, θα μάθετε πώς να δημιουργήσετε τον πρώτο σας server και να τον εξετάσετε με το εργαλείο επιθεώρησης, έναν πολύτιμο τρόπο για να δοκιμάσετε και να διορθώσετε τον server σας, [στο μάθημα](01-first-server/README.md)

- **2 Πελάτης**, σε αυτό το μάθημα, θα μάθετε πώς να γράψετε έναν πελάτη που μπορεί να συνδεθεί στον server σας, [στο μάθημα](02-client/README.md)

- **3 Πελάτης με LLM**, ένας ακόμα καλύτερος τρόπος για να γράψετε έναν πελάτη είναι προσθέτοντας ένα LLM ώστε να μπορεί να "διαπραγματευτεί" με τον server σας για το τι να κάνει, [στο μάθημα](03-llm-client/README.md)

- **4 Χρήση του GitHub Copilot Agent mode σε Visual Studio Code**. Εδώ, εξετάζουμε την εκτέλεση του MCP Server μας μέσα από το Visual Studio Code, [στο μάθημα](04-vscode/README.md)

- **5 stdio Transport Server**. Το stdio transport είναι το προτεινόμενο πρότυπο για την επικοινωνία server-to-client MCP στην τρέχουσα προδιαγραφή, παρέχοντας ασφαλή επικοινωνία βασισμένη σε υποδιαδικασίες, [στο μάθημα](05-stdio-server/README.md)

- **6 HTTP Streaming με MCP (Streamable HTTP)**. Μάθετε για το σύγχρονο HTTP streaming, ειδοποιήσεις προόδου και πώς να υλοποιήσετε κλιμακούμενους, πραγματικού χρόνου MCP servers και πελάτες χρησιμοποιώντας Streamable HTTP, [στο μάθημα](06-http-streaming/README.md)

- **7 Χρήση του AI Toolkit για VSCode** για την κατανάλωση και δοκιμή των MCP Clients και Servers σας, [στο μάθημα](07-aitk/README.md)

- **8 Δοκιμές**. Εδώ θα επικεντρωθούμε ειδικά στο πώς μπορούμε να δοκιμάσουμε τον server και τον πελάτη μας με διάφορους τρόπους, [στο μάθημα](08-testing/README.md)

- **9 Ανάπτυξη**. Αυτό το κεφάλαιο θα εξετάσει διαφορετικούς τρόπους ανάπτυξης των λύσεων MCP σας, [στο μάθημα](09-deployment/README.md)

- **10 Προχωρημένη χρήση server**. Αυτό το κεφάλαιο καλύπτει προχωρημένη χρήση server, [στο μάθημα](./10-advanced/README.md)

- **11 Αυθεντικοποίηση**. Αυτό το κεφάλαιο καλύπτει πώς να προσθέσετε απλή αυθεντικοποίηση, από Basic Auth έως τη χρήση JWT και RBAC. Ενθαρρύνεστε να ξεκινήσετε εδώ και στη συνέχεια να εξετάσετε Προχωρημένα Θέματα στο Κεφάλαιο 5 και να πραγματοποιήσετε πρόσθετη ενίσχυση ασφάλειας μέσω των συστάσεων στο Κεφάλαιο 2, [στο μάθημα](./11-simple-auth/README.md)

Το Model Context Protocol (MCP) είναι ένα ανοιχτό πρωτόκολλο που τυποποιεί τον τρόπο με τον οποίο οι εφαρμογές παρέχουν περιεχόμενο στα LLMs. Σκεφτείτε το MCP σαν μια θύρα USB-C για εφαρμογές AI - παρέχει έναν τυποποιημένο τρόπο σύνδεσης μοντέλων AI με διαφορετικές πηγές δεδομένων και εργαλεία.

## Στόχοι Μάθησης

Μέχρι το τέλος αυτού του μαθήματος, θα μπορείτε:

- Να ρυθμίσετε περιβάλλοντα ανάπτυξης για MCP σε C#, Java, Python, TypeScript και JavaScript
- Να δημιουργήσετε και να αναπτύξετε βασικούς MCP servers με προσαρμοσμένα χαρακτηριστικά (πόρους, προτροπές και εργαλεία)
- Να δημιουργήσετε εφαρμογές υποδοχής που συνδέονται με MCP servers
- Να δοκιμάσετε και να διορθώσετε υλοποιήσεις MCP
- Να κατανοήσετε κοινές προκλήσεις ρύθμισης και τις λύσεις τους
- Να συνδέσετε τις υλοποιήσεις MCP σας με δημοφιλείς υπηρεσίες LLM

## Ρύθμιση του Περιβάλλοντος MCP

Πριν ξεκινήσετε να εργάζεστε με MCP, είναι σημαντικό να προετοιμάσετε το περιβάλλον ανάπτυξης σας και να κατανοήσετε τη βασική ροή εργασίας. Αυτή η ενότητα θα σας καθοδηγήσει στα αρχικά βήματα ρύθμισης για να εξασφαλίσετε μια ομαλή αρχή με το MCP.

### Προαπαιτούμενα

Πριν εμβαθύνετε στην ανάπτυξη MCP, βεβαιωθείτε ότι έχετε:

- **Περιβάλλον Ανάπτυξης**: Για τη γλώσσα που επιλέξατε (C#, Java, Python, TypeScript ή JavaScript)
- **IDE/Επεξεργαστή**: Visual Studio, Visual Studio Code, IntelliJ, Eclipse, PyCharm ή οποιονδήποτε σύγχρονο επεξεργαστή κώδικα
- **Διαχειριστές Πακέτων**: NuGet, Maven/Gradle, pip ή npm/yarn
- **API Keys**: Για οποιεσδήποτε υπηρεσίες AI σκοπεύετε να χρησιμοποιήσετε στις εφαρμογές υποδοχής σας

### Επίσημα SDKs

Στα επόμενα κεφάλαια θα δείτε λύσεις που έχουν υλοποιηθεί χρησιμοποιώντας Python, TypeScript, Java και .NET. Εδώ είναι όλα τα επίσημα υποστηριζόμενα SDKs.

Το MCP παρέχει επίσημα SDKs για πολλές γλώσσες:
- [C# SDK](https://github.com/modelcontextprotocol/csharp-sdk) - Διατηρείται σε συνεργασία με τη Microsoft
- [Java SDK](https://github.com/modelcontextprotocol/java-sdk) - Διατηρείται σε συνεργασία με το Spring AI
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) - Η επίσημη υλοποίηση TypeScript
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Η επίσημη υλοποίηση Python
- [Kotlin SDK](https://github.com/modelcontextprotocol/kotlin-sdk) - Η επίσημη υλοποίηση Kotlin
- [Swift SDK](https://github.com/modelcontextprotocol/swift-sdk) - Διατηρείται σε συνεργασία με το Loopwork AI
- [Rust SDK](https://github.com/modelcontextprotocol/rust-sdk) - Η επίσημη υλοποίηση Rust

## Βασικά Σημεία

- Η ρύθμιση ενός περιβάλλοντος ανάπτυξης MCP είναι απλή με SDKs ειδικά για κάθε γλώσσα
- Η δημιουργία MCP servers περιλαμβάνει τη δημιουργία και την καταχώρηση εργαλείων με σαφή σχήματα
- Οι MCP πελάτες συνδέονται με servers και μοντέλα για να αξιοποιήσουν επεκταμένες δυνατότητες
- Οι δοκιμές και η διόρθωση είναι απαραίτητες για αξιόπιστες υλοποιήσεις MCP
- Οι επιλογές ανάπτυξης κυμαίνονται από τοπική ανάπτυξη έως λύσεις βασισμένες στο cloud

## Εξάσκηση

Διαθέτουμε ένα σύνολο δειγμάτων που συμπληρώνουν τις ασκήσεις που θα δείτε σε όλα τα κεφάλαια αυτής της ενότητας. Επιπλέον, κάθε κεφάλαιο έχει επίσης τις δικές του ασκήσεις και εργασίες.

- [Java Calculator](./samples/java/calculator/README.md)
- [.Net Calculator](../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](./samples/javascript/README.md)
- [TypeScript Calculator](./samples/typescript/README.md)
- [Python Calculator](../../../03-GettingStarted/samples/python)

## Πρόσθετοι Πόροι

- [Δημιουργία Agents χρησιμοποιώντας το Model Context Protocol στο Azure](https://learn.microsoft.com/azure/developer/ai/intro-agents-mcp)
- [Απομακρυσμένο MCP με Azure Container Apps (Node.js/TypeScript/JavaScript)](https://learn.microsoft.com/samples/azure-samples/mcp-container-ts/mcp-container-ts/)
- [.NET OpenAI MCP Agent](https://learn.microsoft.com/samples/azure-samples/openai-mcp-agent-dotnet/openai-mcp-agent-dotnet/)

## Τι ακολουθεί

Επόμενο: [Δημιουργία του πρώτου σας MCP Server](01-first-server/README.md)

---

**Αποποίηση ευθύνης**:  
Αυτό το έγγραφο έχει μεταφραστεί χρησιμοποιώντας την υπηρεσία αυτόματης μετάφρασης [Co-op Translator](https://github.com/Azure/co-op-translator). Παρόλο που καταβάλλουμε προσπάθειες για ακρίβεια, παρακαλούμε να έχετε υπόψη ότι οι αυτόματες μεταφράσεις ενδέχεται να περιέχουν σφάλματα ή ανακρίβειες. Το πρωτότυπο έγγραφο στη μητρική του γλώσσα θα πρέπει να θεωρείται η αυθεντική πηγή. Για κρίσιμες πληροφορίες, συνιστάται επαγγελματική ανθρώπινη μετάφραση. Δεν φέρουμε ευθύνη για τυχόν παρεξηγήσεις ή εσφαλμένες ερμηνείες που προκύπτουν από τη χρήση αυτής της μετάφρασης.