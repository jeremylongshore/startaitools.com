<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "6d6315e03f591fb5a39be91da88585dc",
  "translation_date": "2025-07-13T19:19:55+00:00",
  "source_file": "03-GettingStarted/03-llm-client/solution/typescript/README.md",
  "language_code": "el"
}
-->
# Εκτέλεση αυτού του παραδείγματος

Αυτό το παράδειγμα περιλαμβάνει τη χρήση ενός LLM στον πελάτη. Το LLM χρειάζεται είτε να το εκτελέσετε σε Codespaces είτε να ρυθμίσετε ένα προσωπικό access token στο GitHub για να λειτουργήσει.

## -1- Εγκατάσταση των εξαρτήσεων

```bash
npm install
```

## -3- Εκτέλεση του διακομιστή

```bash
npm run build
```

## -4- Εκτέλεση του πελάτη

```sh
npm run client
```

Θα πρέπει να δείτε ένα αποτέλεσμα παρόμοιο με:

```text
Asking server for available tools
MCPClient started on stdin/stdout
Querying LLM:  What is the sum of 2 and 3?
Making tool call
Calling tool add with args "{\"a\":2,\"b\":3}"
Tool result:  { content: [ { type: 'text', text: '5' } ] }
```

**Αποποίηση ευθυνών**:  
Αυτό το έγγραφο έχει μεταφραστεί χρησιμοποιώντας την υπηρεσία αυτόματης μετάφρασης AI [Co-op Translator](https://github.com/Azure/co-op-translator). Παρόλο που επιδιώκουμε την ακρίβεια, παρακαλούμε να γνωρίζετε ότι οι αυτόματες μεταφράσεις ενδέχεται να περιέχουν λάθη ή ανακρίβειες. Το πρωτότυπο έγγραφο στη μητρική του γλώσσα πρέπει να θεωρείται η αυθεντική πηγή. Για κρίσιμες πληροφορίες, συνιστάται επαγγελματική ανθρώπινη μετάφραση. Δεν φέρουμε ευθύνη για τυχόν παρεξηγήσεις ή λανθασμένες ερμηνείες που προκύπτουν από τη χρήση αυτής της μετάφρασης.