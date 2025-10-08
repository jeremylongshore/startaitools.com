<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T16:44:40+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "pa"
}
-->
# MCP ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣ - ਅਗਸਤ 2025 ਅੱਪਡੇਟ

> **ਮੌਜੂਦਾ ਮਿਆਰ**: ਇਹ ਦਸਤਾਵੇਜ਼ [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) ਸੁਰੱਖਿਆ ਦੀਆਂ ਲੋੜਾਂ ਅਤੇ ਅਧਿਕਾਰਤ [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) ਨੂੰ ਦਰਸਾਉਂਦਾ ਹੈ।

Model Context Protocol (MCP) ਨੇ ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣਾਂ ਵਿੱਚ ਮਹੱਤਵਪੂਰਨ ਸੁਧਾਰ ਕੀਤੇ ਹਨ ਜੋ ਰਵਾਇਤੀ ਸੌਫਟਵੇਅਰ ਸੁਰੱਖਿਆ ਅਤੇ AI-ਵਿਸ਼ੇਸ਼ ਖਤਰੇ ਦੋਵਾਂ ਨੂੰ ਪਤਾ ਲਗਾਉਂਦੇ ਹਨ। ਇਹ ਦਸਤਾਵੇਜ਼ ਅਗਸਤ 2025 ਤੱਕ ਸੁਰੱਖਿਅਤ MCP ਲਾਗੂ ਕਰਨ ਲਈ ਵਿਸਤ੍ਰਿਤ ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ।

## **ਲਾਜ਼ਮੀ ਸੁਰੱਖਿਆ ਲੋੜਾਂ**

### **MCP Specification ਤੋਂ ਮਹੱਤਵਪੂਰਨ ਪਾਬੰਦੀਆਂ:**

> **ਪਾਬੰਦੀ**: MCP ਸਰਵਰ **ਕਦੇ ਵੀ** ਉਹ ਟੋਕਨ ਸਵੀਕਾਰ ਨਹੀਂ ਕਰ ਸਕਦੇ ਜੋ MCP ਸਰਵਰ ਲਈ ਸਪਸ਼ਟ ਤੌਰ 'ਤੇ ਜਾਰੀ ਨਹੀਂ ਕੀਤੇ ਗਏ  
>
> **ਪ੍ਰਤੀਬੰਧਿਤ**: MCP ਸਰਵਰ **ਕਦੇ ਵੀ** ਪ੍ਰਮਾਣਿਕਤਾ ਲਈ ਸੈਸ਼ਨ ਵਰਤ ਨਹੀਂ ਸਕਦੇ  
>
> **ਲੋੜੀਂਦਾ**: ਅਧਿਕਾਰ ਲਾਗੂ ਕਰਨ ਵਾਲੇ MCP ਸਰਵਰ **ਹਰ** ਆਉਣ ਵਾਲੀ ਬੇਨਤੀ ਦੀ ਜਾਂਚ ਕਰਨ  
>
> **ਲਾਜ਼ਮੀ**: ਸਥਿਰ ਕਲਾਇੰਟ IDs ਵਰਤਣ ਵਾਲੇ MCP ਪ੍ਰਾਕਸੀ ਸਰਵਰ **ਹਰ** ਗਤੀਸ਼ੀ ਤੌਰ 'ਤੇ ਰਜਿਸਟਰ ਕੀਤੇ ਕਲਾਇੰਟ ਲਈ ਉਪਭੋਗਤਾ ਦੀ ਸਹਿਮਤੀ ਪ੍ਰਾਪਤ ਕਰਨ

---

## 1. **ਪ੍ਰਮਾਣਿਕਤਾ ਅਤੇ ਅਧਿਕਾਰ ਨਿਯੰਤਰਣ**

### **ਬਾਹਰੀ ਪਛਾਣ ਪ੍ਰਦਾਤਾ ਇੰਟੀਗ੍ਰੇਸ਼ਨ**

**ਮੌਜੂਦਾ MCP ਮਿਆਰ (2025-06-18)** MCP ਸਰਵਰਾਂ ਨੂੰ ਬਾਹਰੀ ਪਛਾਣ ਪ੍ਰਦਾਤਾਵਾਂ ਨੂੰ ਪ੍ਰਮਾਣਿਕਤਾ ਸੌਂਪਣ ਦੀ ਆਗਿਆ ਦਿੰਦਾ ਹੈ, ਜੋ ਇੱਕ ਮਹੱਤਵਪੂਰਨ ਸੁਰੱਖਿਆ ਸੁਧਾਰ ਹੈ:

**ਸੁਰੱਖਿਆ ਫਾਇਦੇ:**
1. **ਕਸਟਮ ਪ੍ਰਮਾਣਿਕਤਾ ਖਤਰੇ ਖਤਮ ਕਰਦਾ ਹੈ**: ਕਸਟਮ ਪ੍ਰਮਾਣਿਕਤਾ ਲਾਗੂ ਕਰਨ ਦੇ ਨਾਲ ਜੁੜੇ ਖਤਰੇ ਘਟਾਉਂਦਾ ਹੈ
2. **ਐਨਟਰਪ੍ਰਾਈਜ਼-ਗਰੇਡ ਸੁਰੱਖਿਆ**: Microsoft Entra ID ਵਰਗੇ ਸਥਾਪਿਤ ਪਛਾਣ ਪ੍ਰਦਾਤਾਵਾਂ ਦੇ ਉੱਚ-ਤਕਨੀਕੀ ਸੁਰੱਖਿਆ ਵਿਸ਼ੇਸ਼ਤਾਵਾਂ ਦਾ ਲਾਭ ਲੈਂਦਾ ਹੈ
3. **ਕੇਂਦਰੀਕ੍ਰਿਤ ਪਛਾਣ ਪ੍ਰਬੰਧਨ**: ਉਪਭੋਗਤਾ ਜੀਵਨਚੱਕਰ ਪ੍ਰਬੰਧਨ, ਪਹੁੰਚ ਨਿਯੰਤਰਣ, ਅਤੇ ਅਨੁਕੂਲਤਾ ਆਡਿਟਿੰਗ ਨੂੰ ਸਧਾਰਦਾ ਹੈ
4. **ਮਲਟੀ-ਫੈਕਟਰ ਪ੍ਰਮਾਣਿਕਤਾ**: ਐਨਟਰਪ੍ਰਾਈਜ਼ ਪਛਾਣ ਪ੍ਰਦਾਤਾਵਾਂ ਤੋਂ MFA ਸਮਰੱਥਾ ਪ੍ਰਾਪਤ ਕਰਦਾ ਹੈ
5. **ਸ਼ਰਤਮੁਲਕ ਪਹੁੰਚ ਨੀਤੀਆਂ**: ਖਤਰੇ-ਅਧਾਰਿਤ ਪਹੁੰਚ ਨਿਯੰਤਰਣ ਅਤੇ ਅਨੁਕੂਲ ਪ੍ਰਮਾਣਿਕਤਾ ਦਾ ਲਾਭ ਲੈਂਦਾ ਹੈ

**ਲਾਗੂ ਕਰਨ ਦੀਆਂ ਲੋੜਾਂ:**
- **ਟੋਕਨ ਦਰਸ਼ਕ ਦੀ ਜਾਂਚ**: ਸਾਰੇ ਟੋਕਨ ਦੀ ਜਾਂਚ ਕਰੋ ਕਿ ਉਹ MCP ਸਰਵਰ ਲਈ ਸਪਸ਼ਟ ਤੌਰ 'ਤੇ ਜਾਰੀ ਕੀਤੇ ਗਏ ਹਨ
- **ਜਾਰੀ ਕਰਨ ਵਾਲੇ ਦੀ ਜਾਂਚ**: ਟੋਕਨ ਜਾਰੀ ਕਰਨ ਵਾਲੇ ਨੂੰ ਉਮੀਦ ਕੀਤੇ ਪਛਾਣ ਪ੍ਰਦਾਤਾ ਨਾਲ ਮਿਲਾਉਣਾ
- **ਦਸਤਖਤ ਦੀ ਜਾਂਚ**: ਟੋਕਨ ਦੀ ਅਖੰਡਤਾ ਦੀ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫਿਕ ਜਾਂਚ
- **ਮਿਆਦ ਦੀ ਪਾਬੰਦੀ**: ਟੋਕਨ ਦੀ ਮਿਆਦ ਦੀਆਂ ਸੀਮਾਵਾਂ ਦੀ ਸਖਤ ਪਾਬੰਦੀ
- **ਸਕੋਪ ਦੀ ਜਾਂਚ**: ਯਕੀਨੀ ਬਣਾਓ ਕਿ ਟੋਕਨ ਵਿੱਚ ਬੇਨਤੀ ਕੀਤੇ ਕਾਰਵਾਈਆਂ ਲਈ ਉਚਿਤ ਅਧਿਕਾਰ ਹਨ

### **ਅਧਿਕਾਰ ਲਾਜ਼ਮੀ ਸੁਰੱਖਿਆ**

**ਮਹੱਤਵਪੂਰਨ ਨਿਯੰਤਰਣ:**
- **ਵਿਆਪਕ ਅਧਿਕਾਰ ਆਡਿਟ**: ਸਾਰੇ ਅਧਿਕਾਰ ਫੈਸਲੇ ਦੇ ਬਿੰਦੂਆਂ ਦੀ ਨਿਯਮਿਤ ਸੁਰੱਖਿਆ ਸਮੀਖਿਆ
- **ਫੇਲ-ਸੇਫ ਡਿਫਾਲਟ**: ਜਦੋਂ ਅਧਿਕਾਰ ਲਾਜ਼ਮੀਆਂ ਫੈਸਲਾ ਨਹੀਂ ਕਰ ਸਕਦੀਆਂ, ਪਹੁੰਚ ਨੂੰ ਰੋਕੋ
- **ਅਧਿਕਾਰ ਦੀਆਂ ਸੀਮਾਵਾਂ**: ਵੱਖ-ਵੱਖ ਸਵੈਧਿਕ ਪੱਧਰਾਂ ਅਤੇ ਸਰੋਤ ਪਹੁੰਚ ਦੇ ਵਿਚਕਾਰ ਸਪਸ਼ਟ ਵੱਖਰਾ
- **ਆਡਿਟ ਲੌਗਿੰਗ**: ਸੁਰੱਖਿਆ ਨਿਗਰਾਨੀ ਲਈ ਸਾਰੇ ਅਧਿਕਾਰ ਫੈਸਲਿਆਂ ਦੀ ਪੂਰੀ ਲੌਗਿੰਗ
- **ਨਿਯਮਿਤ ਪਹੁੰਚ ਸਮੀਖਿਆ**: ਉਪਭੋਗਤਾ ਅਧਿਕਾਰਾਂ ਅਤੇ ਸਵੈਧਿਕ ਅਸਾਈਨਮੈਂਟ ਦੀ ਮਿਆਦਿਕ ਜਾਂਚ

## 2. **ਟੋਕਨ ਸੁਰੱਖਿਆ ਅਤੇ ਐਂਟੀ-ਪਾਸਥਰੂ ਨਿਯੰਤਰਣ**

### **ਟੋਕਨ ਪਾਸਥਰੂ ਰੋਕਥਾਮ**

**MCP ਅਧਿਕਾਰ ਨਿਰਧਾਰਨ ਵਿੱਚ ਟੋਕਨ ਪਾਸਥਰੂ ਸਖ਼ਤ ਤੌਰ 'ਤੇ ਮਨਾਹੀ ਹੈ** ਕਿਉਂਕਿ ਇਹ ਮਹੱਤਵਪੂਰਨ ਸੁਰੱਖਿਆ ਖਤਰੇ ਪੈਦਾ ਕਰਦਾ ਹੈ:

**ਸੁਰੱਖਿਆ ਖਤਰੇ ਹੱਲ ਕੀਤੇ:**
- **ਨਿਯੰਤਰਣ ਦਾ ਉਲੰਘਨ**: ਦਰਜਾ ਸੀਮਿਤ ਕਰਨ, ਬੇਨਤੀ ਦੀ ਜਾਂਚ, ਅਤੇ ਟ੍ਰੈਫਿਕ ਨਿਗਰਾਨੀ ਵਰਗੇ ਜ਼ਰੂਰੀ ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣਾਂ ਨੂੰ ਬਾਈਪਾਸ ਕਰਦਾ ਹੈ
- **ਜਵਾਬਦੇਹੀ ਦਾ ਟੁੱਟਣਾ**: ਕਲਾਇੰਟ ਪਛਾਣ ਨੂੰ ਅਸੰਭਵ ਬਣਾਉਂਦਾ ਹੈ, ਆਡਿਟ ਟ੍ਰੇਲਾਂ ਅਤੇ ਘਟਨਾ ਦੀ ਜਾਂਚ ਨੂੰ ਖਰਾਬ ਕਰਦਾ ਹੈ
- **ਪ੍ਰਾਕਸੀ-ਅਧਾਰਿਤ ਡਾਟਾ ਚੋਰੀ**: ਦੁਰਾਸ਼ਾ ਵਾਲੇ ਅਭਿਨੇਤਾਵਾਂ ਨੂੰ ਅਣਅਧਿਕਾਰਤ ਡਾਟਾ ਪਹੁੰਚ ਲਈ ਸਰਵਰਾਂ ਨੂੰ ਪ੍ਰਾਕਸੀ ਵਜੋਂ ਵਰਤਣ ਦੀ ਆਗਿਆ ਦਿੰਦਾ ਹੈ
- **ਭਰੋਸੇ ਦੀ ਸੀਮਾ ਦਾ ਉਲੰਘਨ**: ਟੋਕਨ ਮੂਲਾਂ ਬਾਰੇ ਡਾਊਨਸਟ੍ਰੀਮ ਸੇਵਾ ਭਰੋਸੇ ਦੇ ਅਨੁਮਾਨਾਂ ਨੂੰ ਤੋੜਦਾ ਹੈ
- **ਪਾਸੇ ਦੀ ਚਲਣਸ਼ੀਲਤਾ**: ਕਈ ਸੇਵਾਵਾਂ ਵਿੱਚ ਸਮਝੌਤਾ ਕੀਤੇ ਟੋਕਨ ਵਿਆਪਕ ਹਮਲੇ ਦੇ ਵਧਾਏ ਗਏ ਖੇਤਰ ਨੂੰ ਯਕੀਨੀ ਬਣਾਉਂਦੇ ਹਨ

**ਲਾਗੂ ਕਰਨ ਦੇ ਨਿਯੰਤਰਣ:**
```yaml
Token Validation Requirements:
  audience_validation: MANDATORY
  issuer_verification: MANDATORY  
  signature_check: MANDATORY
  expiration_enforcement: MANDATORY
  scope_validation: MANDATORY
  
Token Lifecycle Management:
  rotation_frequency: "Short-lived tokens preferred"
  secure_storage: "Azure Key Vault or equivalent"
  transmission_security: "TLS 1.3 minimum"
  replay_protection: "Implemented via nonce/timestamp"
```

### **ਸੁਰੱਖਿਅਤ ਟੋਕਨ ਪ੍ਰਬੰਧਨ ਪੈਟਰਨ**

**ਸਰਵੋਤਮ ਅਭਿਆਸ:**
- **ਛੋਟੇ ਸਮੇਂ ਦੇ ਟੋਕਨ**: ਵਾਰੰ-ਵਾਰ ਟੋਕਨ ਰੋਟੇਸ਼ਨ ਨਾਲ ਖਤਰੇ ਦੀ ਵਿੰਡੋ ਘਟਾਓ
- **ਸਿਰਫ਼-ਜ਼ਰੂਰਤ ਦੇ ਅਧਾਰ 'ਤੇ ਜਾਰੀ ਕਰਨਾ**: ਟੋਕਨ ਸਿਰਫ਼ ਵਿਸ਼ੇਸ਼ ਕਾਰਵਾਈਆਂ ਲਈ ਜ਼ਰੂਰਤ ਦੇ ਸਮੇਂ ਜਾਰੀ ਕਰੋ
- **ਸੁਰੱਖਿਅਤ ਸਟੋਰੇਜ**: ਹਾਰਡਵੇਅਰ ਸੁਰੱਖਿਆ ਮੋਡੀਊਲ (HSMs) ਜਾਂ ਸੁਰੱਖਿਅਤ ਕੁੰਜੀ ਵਾਲਟ ਵਰਤੋ
- **ਟੋਕਨ ਬਾਈਂਡਿੰਗ**: ਟੋਕਨ ਨੂੰ ਵਿਸ਼ੇਸ਼ ਕਲਾਇੰਟ, ਸੈਸ਼ਨ, ਜਾਂ ਕਾਰਵਾਈਆਂ ਨਾਲ ਜੁੜੋ ਜਿੱਥੇ ਸੰਭਵ ਹੋਵੇ
- **ਨਿਗਰਾਨੀ ਅਤੇ ਚੇਤਾਵਨੀ**: ਟੋਕਨ ਦੇ ਦੁਰਵਰਤੋਂ ਜਾਂ ਅਣਅਧਿਕਾਰਤ ਪਹੁੰਚ ਪੈਟਰਨ ਦੀ ਰੀਅਲ-ਟਾਈਮ ਪਛਾਣ

## 3. **ਸੈਸ਼ਨ ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣ**

### **ਸੈਸ਼ਨ ਹਾਈਜੈਕਿੰਗ ਰੋਕਥਾਮ**

**ਹਮਲੇ ਦੇ ਰਸਤੇ ਹੱਲ ਕੀਤੇ:**
- **ਸੈਸ਼ਨ ਹਾਈਜੈਕ ਪ੍ਰੰਪਟ ਇੰਜੈਕਸ਼ਨ**: ਸਾਂਝੇ ਸੈਸ਼ਨ ਸਥਿਤੀ ਵਿੱਚ ਦੁਰਾਸ਼ਾ ਵਾਲੇ ਘਟਨਾਵਾਂ ਨੂੰ ਇੰਜੈਕਟ ਕੀਤਾ ਜਾਂਦਾ ਹੈ
- **ਸੈਸ਼ਨ ਨਕਲ**: ਚੋਰੀ ਕੀਤੇ ਸੈਸ਼ਨ IDs ਦੀ ਅਣਅਧਿਕਾਰਤ ਵਰਤੋਂ ਨਾਲ ਪ੍ਰਮਾਣਿਕਤਾ ਨੂੰ ਬਾਈਪਾਸ ਕਰਨਾ
- **ਰਿਜ਼ਯੂਮਬਲ ਸਟ੍ਰੀਮ ਹਮਲੇ**: ਸਰਵਰ-ਭੇਜੇ ਘਟਨਾ ਰਿਜ਼ਯੂਮਸ਼ਨ ਦਾ ਦੁਰਵਰਤੋਂ ਕਰਕੇ ਦੁਰਾਸ਼ਾ ਵਾਲੇ ਸਮੱਗਰੀ ਇੰਜੈਕਸ਼ਨ

**ਲਾਜ਼ਮੀ ਸੈਸ਼ਨ ਨਿਯੰਤਰਣ:**
```yaml
Session ID Generation:
  randomness_source: "Cryptographically secure RNG"
  entropy_bits: 128 # Minimum recommended
  format: "Base64url encoded"
  predictability: "MUST be non-deterministic"

Session Binding:
  user_binding: "REQUIRED - <user_id>:<session_id>"
  additional_identifiers: "Device fingerprint, IP validation"
  context_binding: "Request origin, user agent validation"
  
Session Lifecycle:
  expiration: "Configurable timeout policies"
  rotation: "After privilege escalation events"
  invalidation: "Immediate on security events"
  cleanup: "Automated expired session removal"
```

**ਟ੍ਰਾਂਸਪੋਰਟ ਸੁਰੱਖਿਆ:**
- **HTTPS ਲਾਗੂ ਕਰਨਾ**: TLS 1.3 ਦੇ ਜ਼ਰੀਏ ਸਾਰੇ ਸੈਸ਼ਨ ਸੰਚਾਰ
- **ਸੁਰੱਖਿਅਤ ਕੁਕੀ ਗੁਣ**: HttpOnly, Secure, SameSite=Strict
- **ਸਰਟੀਫਿਕੇਟ ਪਿਨਿੰਗ**: ਮਹੱਤਵਪੂਰਨ ਕਨੈਕਸ਼ਨਾਂ ਲਈ MITM ਹਮਲਿਆਂ ਨੂੰ ਰੋਕਣ ਲਈ

### **ਸਥਿਤੀਵਾਨ ਅਤੇ ਸਥਿਤੀਹੀਨ ਵਿਚਾਰ**

**ਸਥਿਤੀਵਾਨ ਲਾਗੂ ਕਰਨ ਲਈ:**
- ਸਾਂਝੇ ਸੈਸ਼ਨ ਸਥਿਤੀ ਨੂੰ ਇੰਜੈਕਸ਼ਨ ਹਮਲਿਆਂ ਤੋਂ ਵਧੇਰੇ ਸੁਰੱਖਿਆ ਦੀ ਲੋੜ ਹੈ
- ਕਤਾਰ-ਅਧਾਰਿਤ ਸੈਸ਼ਨ ਪ੍ਰਬੰਧਨ ਨੂੰ ਅਖੰਡਤਾ ਦੀ ਜਾਂਚ ਦੀ ਲੋੜ ਹੈ
- ਕਈ ਸਰਵਰ ਇੰਸਟੈਂਸਾਂ ਨੂੰ ਸੁਰੱਖਿਅਤ ਸੈਸ਼ਨ ਸਥਿਤੀ ਸਮਰੂਪਤਾ ਦੀ ਲੋੜ ਹੈ

**ਸਥਿਤੀਹੀਨ ਲਾਗੂ ਕਰਨ ਲਈ:**
- JWT ਜਾਂ ਇਸੇ ਟੋਕਨ-ਅਧਾਰਿਤ ਸੈਸ਼ਨ ਪ੍ਰਬੰਧਨ
- ਸੈਸ਼ਨ ਸਥਿਤੀ ਦੀ ਅਖੰਡਤਾ ਦੀ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫਿਕ ਜਾਂਚ
- ਘਟਾਏ ਗਏ ਹਮਲੇ ਦਾ ਰਸਤਾ ਪਰ ਮਜ਼ਬੂਤ ਟੋਕਨ ਜਾਂਚ ਦੀ ਲੋੜ

## 4. **AI-ਵਿਸ਼ੇਸ਼ ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣ**

### **ਪ੍ਰੰਪਟ ਇੰਜੈਕਸ਼ਨ ਰੱਖਿਆ**

**Microsoft Prompt Shields ਇੰਟੀਗ੍ਰੇਸ਼ਨ:**
```yaml
Detection Mechanisms:
  - "Advanced ML-based instruction detection"
  - "Contextual analysis of external content"
  - "Real-time threat pattern recognition"
  
Protection Techniques:
  - "Spotlighting trusted vs untrusted content"
  - "Delimiter systems for content boundaries"  
  - "Data marking for content source identification"
  
Integration Points:
  - "Azure Content Safety service"
  - "Real-time content filtering"
  - "Threat intelligence updates"
```

**ਲਾਗੂ ਕਰਨ ਦੇ ਨਿਯੰਤਰਣ:**
- **ਇਨਪੁਟ ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ**: ਸਾਰੇ ਉਪਭੋਗਤਾ ਇਨਪੁਟ ਦੀ ਵਿਸ਼ਤ੍ਰਿਤ ਜਾਂਚ ਅਤੇ ਫਿਲਟਰੇਸ਼ਨ
- **ਸਮੱਗਰੀ ਸੀਮਾ ਦੀ ਪਰਿਭਾਸ਼ਾ**: ਸਿਸਟਮ ਹਦਾਇਤਾਂ ਅਤੇ ਉਪਭੋਗਤਾ ਸਮੱਗਰੀ ਦੇ ਵਿਚਕਾਰ ਸਪਸ਼ਟ ਵੱਖਰਾ
- **ਹਦਾਇਤ ਅਨੁਕ੍ਰਮ**: ਵਿਰੋਧੀ ਹਦਾਇਤਾਂ ਲਈ ਸਹੀ ਅਗਰਤਾ ਨਿਯਮ
- **ਆਉਟਪੁੱਟ ਨਿਗਰਾਨੀ**: ਸੰਭਾਵਿਤ ਤੌਰ 'ਤੇ ਹਾਨੀਕਾਰਕ ਜਾਂ ਚੇੜ-ਛਾੜ ਕੀਤੇ ਆਉਟਪੁੱਟ ਦੀ ਪਛਾਣ

### **ਟੂਲ ਪੌਇਜ਼ਨਿੰਗ ਰੋਕਥਾਮ**

**ਟੂਲ ਸੁਰੱਖਿਆ ਫਰੇਮਵਰਕ:**
```yaml
Tool Definition Protection:
  validation:
    - "Schema validation against expected formats"
    - "Content analysis for malicious instructions" 
    - "Parameter injection detection"
    - "Hidden instruction identification"
  
  integrity_verification:
    - "Cryptographic hashing of tool definitions"
    - "Digital signatures for tool packages"
    - "Version control with change auditing"
    - "Tamper detection mechanisms"
  
  monitoring:
    - "Real-time change detection"
    - "Behavioral analysis of tool usage"
    - "Anomaly detection for execution patterns"
    - "Automated alerting for suspicious modifications"
```

**ਗਤੀਸ਼ੀ ਟੂਲ ਪ੍ਰਬੰਧਨ:**
- **ਮਨਜ਼ੂਰੀ ਵਰਕਫਲੋਜ਼**: ਟੂਲ ਵਿੱਚ ਤਬਦੀਲੀਆਂ ਲਈ ਸਪਸ਼ਟ ਉਪਭੋਗਤਾ ਸਹਿਮਤੀ
- **ਰੋਲਬੈਕ ਸਮਰੱਥਾ**: ਪਿਛਲੇ ਟੂਲ ਵਰਜਨ ਵਿੱਚ ਵਾਪਸ ਜਾਣ ਦੀ ਯੋਗਤਾ
- **ਤਬਦੀਲੀ ਆਡਿਟਿੰਗ**: ਟੂਲ ਪਰਿਭਾਸ਼ਾ ਤਬਦੀਲੀਆਂ ਦਾ ਪੂਰਾ ਇਤਿਹਾਸ
- **ਖਤਰੇ ਦਾ ਮੁਲਾਂਕਣ**: ਟੂਲ ਸੁਰੱਖਿਆ ਸਥਿਤੀ ਦਾ ਸਵੈਚਾਲਿਤ ਮੁਲਾਂਕਣ

## 5. **Confused Deputy ਹਮਲੇ ਰੋਕਥਾਮ**

### **OAuth ਪ੍ਰਾਕਸੀ ਸੁਰੱਖਿਆ**

**ਹਮਲੇ ਰੋਕਥਾਮ ਨਿਯੰਤਰਣ:**
```yaml
Client Registration:
  static_client_protection:
    - "Explicit user consent for dynamic registration"
    - "Consent bypass prevention mechanisms"  
    - "Cookie-based consent validation"
    - "Redirect URI strict validation"
    
  authorization_flow:
    - "PKCE implementation (OAuth 2.1)"
    - "State parameter validation"
    - "Authorization code binding"
    - "Nonce verification for ID tokens"
```

**ਲਾਗੂ ਕਰਨ ਦੀਆਂ ਲੋੜਾਂ:**
- **ਉਪਭੋਗਤਾ ਸਹਿਮਤੀ ਦੀ ਜਾਂਚ**: ਗਤੀਸ਼ੀ ਕਲਾਇੰਟ ਰਜਿਸਟਰੇਸ਼ਨ ਲਈ ਕਦੇ ਵੀ ਸਹਿਮਤੀ ਸਕ੍ਰੀਨ ਨੂੰ ਛੱਡੋ ਨਹੀਂ
- **ਰੀਡਾਇਰੈਕਟ URI ਦੀ ਜਾਂਚ**: ਰੀਡਾਇਰੈਕਟ ਮੰਜ਼ਿਲਾਂ ਦੀ ਸਖ਼ਤ ਵ੍ਹਾਈਟਲਿਸਟ-ਅਧਾਰਿਤ ਜਾਂਚ
- **ਅਧਿਕਾਰ ਕੋਡ ਸੁਰੱਖਿਆ**: ਛੋਟੇ ਸਮੇਂ ਦੇ ਕੋਡਾਂ ਨਾਲ ਸਿੰਗਲ-ਯੂਜ਼ ਪਾਬੰਦੀ
- **ਕਲਾਇੰਟ ਪਛਾਣ ਦੀ ਜਾਂਚ**: ਕਲਾਇੰਟ ਪ੍ਰਮਾਣਿਕਤਾ ਅਤੇ ਮੈਟਾਡੇਟਾ ਦੀ ਮਜ਼ਬੂਤ ਜਾਂਚ

## 6. **ਟੂਲ ਕਾਰਵਾਈ ਸੁਰੱਖਿਆ**

### **Sandboxing ਅਤੇ Isolation**

**ਕੰਟੇਨਰ-ਅਧਾਰਿਤ Isolation:**
```yaml
Execution Environment:
  containerization: "Docker/Podman with security profiles"
  resource_limits:
    cpu: "Configurable CPU quotas"
    memory: "Memory usage restrictions"
    disk: "Storage access limitations"
    network: "Network policy enforcement"
  
  privilege_restrictions:
    user_context: "Non-root execution mandatory"
    capability_dropping: "Remove unnecessary Linux capabilities"
    syscall_filtering: "Seccomp profiles for syscall restriction"
    filesystem: "Read-only root with minimal writable areas"
```

**ਪ੍ਰਕਿਰਿਆ Isolation:**
- **ਵੱਖਰੀ ਪ੍ਰਕਿਰਿਆ ਸੰਦਰਭ**: ਹਰ ਟੂਲ ਕਾਰਵਾਈ ਨੂੰ ਵੱਖਰੇ ਪ੍ਰਕਿਰਿਆ ਸਥਾਨ ਵਿੱਚ
- **ਇੰਟਰ-ਪ੍ਰਕਿਰਿਆ ਸੰਚਾਰ**: ਸੁਰੱਖਿਅਤ IPC ਮਕੈਨਿਜ਼ਮਾਂ ਨਾਲ ਜਾਂਚ
- **ਪ੍ਰਕਿਰਿਆ ਨਿਗਰਾਨੀ**: ਰਨਟਾਈਮ ਵਿਹਾਰ ਵਿਸ਼ਲੇਸ਼ਣ ਅਤੇ ਅਸਧਾਰਨਤਾ ਦੀ ਪਛਾਣ
- **ਸਰੋਤ ਪਾਬੰਦੀ**: CPU, ਮੈਮੋਰੀ, ਅਤੇ I/O ਕਾਰਵਾਈਆਂ 'ਤੇ ਸਖ਼ਤ ਸੀਮਾਵਾਂ

### **ਘੱਟ ਤੋਂ ਘੱਟ ਅਧਿਕਾਰ ਲਾਗੂ ਕਰਨਾ**

**ਅਧਿਕਾਰ ਪ੍ਰਬੰਧਨ:**
```yaml
Access Control:
  file_system:
    - "Minimal required directory access"
    - "Read-only access where possible"
    - "Temporary file cleanup automation"
    
  network_access:
    - "Explicit allowlist for external connections"
    - "DNS resolution restrictions" 
    - "Port access limitations"
    - "SSL/TLS certificate validation"
  
  system_resources:
    - "No administrative privilege elevation"
    - "Limited system call access"
    - "No hardware device access"
    - "Restricted environment variable access"
```

## 7. **ਸਪਲਾਈ ਚੇਨ ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣ**

### **ਨਿਰਭਰਤਾ ਦੀ ਜਾਂਚ**

**ਵਿਆਪਕ ਕੰਪੋਨੈਂਟ ਸੁਰੱਖਿਆ:**
```yaml
Software Dependencies:
  scanning: 
    - "Automated vulnerability scanning (GitHub Advanced Security)"
    - "License compliance verification"
    - "Known vulnerability database checks"
    - "Malware detection and analysis"
  
  verification:
    - "Package signature verification"
    - "Checksum validation"
    - "Provenance attestation"
    - "Software Bill of Materials (SBOM)"

AI Components:
  model_verification:
    - "Model provenance validation"
    - "Training data source verification" 
    - "Model behavior testing"
    - "Adversarial robustness assessment"
  
  service_validation:
    - "Third-party API security assessment"
    - "Service level agreement review"
    - "Data handling compliance verification"
    - "Incident response capability evaluation"
```

### **ਨਿਰੰਤਰ ਨਿਗਰਾਨੀ**

**ਸਪਲਾਈ ਚੇਨ ਖਤਰੇ ਦੀ ਪਛਾਣ:**
- **ਨਿਰਭਰਤਾ ਸਿਹਤ ਨਿਗਰਾਨੀ**: ਸੁਰੱਖਿਆ ਸਮੱਸਿਆਵਾਂ ਲਈ ਸਾਰੀਆਂ ਨਿਰਭਰਤਾਵਾਂ ਦਾ ਨਿਰੰਤਰ ਮੁਲਾਂਕਣ
- **ਖਤਰੇ ਦੀ ਜਾਣਕਾਰੀ ਇੰਟੀਗ੍ਰੇਸ਼ਨ**: ਉਭਰਦੇ ਸਪਲਾਈ ਚੇਨ ਖਤਰੇ 'ਤੇ ਰੀਅਲ-ਟਾਈਮ ਅੱਪਡੇਟ
- **ਵਿਹਾਰਕ ਵਿਸ਼ਲੇਸ਼ਣ**: ਬਾਹਰੀ ਕੰਪੋਨੈਂਟਾਂ ਵਿੱਚ ਅਸਧਾਰਨ ਵਿਹਾਰ ਦੀ ਪਛਾਣ
- **ਸਵੈਚਾਲਿਤ ਜਵਾਬ**: ਸਮਝੌਤਾ ਕੀਤੇ ਕੰਪੋਨੈਂਟਾਂ ਦੀ ਤੁਰੰਤ ਰੋਕਥਾਮ

## 8. **ਨਿਗਰਾਨੀ ਅਤੇ ਪਛਾਣ ਨਿਯੰਤਰਣ**

### **ਸੁਰੱਖਿਆ ਜਾਣਕਾਰੀ ਅਤੇ ਘਟਨਾ ਪ੍ਰਬੰਧਨ (SIEM)**

**ਵਿਆਪਕ ਲੌਗਿੰਗ ਰਣਨੀਤੀ:**
```yaml
Authentication Events:
  - "All authentication attempts (success/failure)"
  - "Token issuance and validation events"
  - "Session creation, modification, termination"
  - "Authorization decisions and policy evaluations"

Tool Execution:
  - "Tool invocation details and parameters"
  - "Execution duration and resource usage"
  - "Output generation and content analysis"
  - "Error conditions and exception handling"

Security Events:
  - "Potential prompt injection attempts"
  - "Tool poisoning detection events"
  - "Session hijacking indicators"
  - "Unusual access patterns and anomalies"
```

### **ਰੀਅਲ-ਟਾਈਮ ਖਤਰੇ ਦੀ ਪਛਾਣ**

**ਵਿਹਾਰਕ ਵਿਸ਼ਲੇਸ਼ਣ:**
- **ਉਪਭੋਗਤਾ ਵਿਹਾਰ ਵਿਸ਼ਲੇਸ਼ਣ (UBA)**: ਅਸਧਾਰਨ ਉਪਭੋਗਤਾ ਪਹੁੰਚ ਪੈਟਰਨ ਦੀ ਪਛਾਣ
- **ਇਕਾਈ ਵਿਹਾਰ ਵਿਸ਼ਲੇਸ਼ਣ (EBA)**: MCP ਸਰਵਰ ਅਤੇ ਟੂਲ ਵਿਹਾਰ ਦੀ ਨਿਗਰਾਨੀ
- **ਮਸ਼ੀਨ ਲਰਨਿੰਗ ਅ

**ਅਸਵੀਕਾਰਨ**:  
ਇਹ ਦਸਤਾਵੇਜ਼ AI ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਅਨੁਵਾਦ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀ ਹੋਣ ਦਾ ਯਤਨ ਕਰਦੇ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਦਿਓ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸੁਚੱਜੇਪਣ ਹੋ ਸਕਦੇ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼, ਜੋ ਇਸਦੀ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਹੈ, ਨੂੰ ਅਧਿਕਾਰਤ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਮਹੱਤਵਪੂਰਨ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਇਸ ਅਨੁਵਾਦ ਦੀ ਵਰਤੋਂ ਤੋਂ ਪੈਦਾ ਹੋਣ ਵਾਲੇ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆ ਲਈ ਅਸੀਂ ਜ਼ਿੰਮੇਵਾਰ ਨਹੀਂ ਹਾਂ।