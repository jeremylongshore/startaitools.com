<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T17:56:51+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "tr"
}
-->
# MCP Güvenlik Kontrolleri - Ağustos 2025 Güncellemesi

> **Mevcut Standart**: Bu belge, [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) güvenlik gereksinimlerini ve resmi [MCP Güvenlik En İyi Uygulamaları](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) belgelerini yansıtmaktadır.

Model Context Protocol (MCP), hem geleneksel yazılım güvenliği hem de yapay zeka odaklı tehditlere yönelik gelişmiş güvenlik kontrolleriyle önemli ölçüde olgunlaşmıştır. Bu belge, Ağustos 2025 itibarıyla güvenli MCP uygulamaları için kapsamlı güvenlik kontrolleri sunmaktadır.

## **ZORUNLU Güvenlik Gereksinimleri**

### **MCP Spesifikasyonundan Kritik Yasaklar:**

> **YASAK**: MCP sunucuları, MCP sunucusu için açıkça verilmemiş hiçbir token'ı **KABUL ETMEMELİDİR**  
>
> **YASAK**: MCP sunucuları, kimlik doğrulama için oturumları **KULLANMAMALIDIR**  
>
> **GEREKLİ**: Yetkilendirme uygulayan MCP sunucuları, TÜM gelen istekleri **DOĞRULAMALIDIR**  
>
> **ZORUNLU**: Statik istemci kimlikleri kullanan MCP proxy sunucuları, her dinamik olarak kaydedilen istemci için kullanıcı onayı **ALMALIDIR**

---

## 1. **Kimlik Doğrulama ve Yetkilendirme Kontrolleri**

### **Harici Kimlik Sağlayıcı Entegrasyonu**

**Mevcut MCP Standardı (2025-06-18)**, MCP sunucularının kimlik doğrulamayı harici kimlik sağlayıcılara devretmesine olanak tanır ve bu, önemli bir güvenlik iyileştirmesidir:

**Güvenlik Avantajları:**
1. **Özel Kimlik Doğrulama Risklerini Ortadan Kaldırır**: Özel kimlik doğrulama uygulamalarından kaynaklanan güvenlik açıklarını azaltır  
2. **Kurumsal Düzeyde Güvenlik**: Microsoft Entra ID gibi gelişmiş güvenlik özelliklerine sahip kimlik sağlayıcılarından yararlanır  
3. **Merkezi Kimlik Yönetimi**: Kullanıcı yaşam döngüsü yönetimini, erişim kontrolünü ve uyumluluk denetimlerini basitleştirir  
4. **Çok Faktörlü Kimlik Doğrulama**: Kurumsal kimlik sağlayıcılardan MFA yeteneklerini devralır  
5. **Koşullu Erişim Politikaları**: Risk tabanlı erişim kontrolleri ve uyarlanabilir kimlik doğrulama avantajları sağlar  

**Uygulama Gereksinimleri:**
- **Token Hedef Doğrulama**: Tüm token'ların MCP sunucusu için açıkça verildiğini doğrulayın  
- **Yayımlayıcı Doğrulama**: Token yayımlayıcısının beklenen kimlik sağlayıcıyla eşleştiğini doğrulayın  
- **İmza Doğrulama**: Token bütünlüğünün kriptografik doğrulaması  
- **Süre Sona Erme Uygulaması**: Token ömrü sınırlarının sıkı bir şekilde uygulanması  
- **Kapsam Doğrulama**: Token'ların istenen işlemler için uygun izinler içerdiğinden emin olun  

### **Yetkilendirme Mantığı Güvenliği**

**Kritik Kontroller:**
- **Kapsamlı Yetkilendirme Denetimleri**: Tüm yetkilendirme karar noktalarının düzenli güvenlik incelemeleri  
- **Güvenli Varsayılanlar**: Yetkilendirme mantığı kesin bir karar veremediğinde erişimi reddet  
- **İzin Sınırları**: Farklı ayrıcalık seviyeleri ve kaynak erişimi arasında net ayrım  
- **Denetim Kaydı**: Güvenlik izleme için tüm yetkilendirme kararlarının eksiksiz kaydı  
- **Düzenli Erişim İncelemeleri**: Kullanıcı izinlerinin ve ayrıcalık atamalarının periyodik doğrulaması  

## 2. **Token Güvenliği ve Geçiş Önleme Kontrolleri**

### **Token Geçişinin Önlenmesi**

**Token geçişi**, MCP Yetkilendirme Spesifikasyonunda kritik güvenlik riskleri nedeniyle açıkça yasaklanmıştır:

**Ele Alınan Güvenlik Riskleri:**
- **Kontrol Atlatma**: Oran sınırlama, istek doğrulama ve trafik izleme gibi temel güvenlik kontrollerini atlar  
- **Hesap Verebilirlik Bozulması**: Müşteri kimliğini imkansız hale getirir, denetim izlerini ve olay incelemesini bozar  
- **Proxy Tabanlı Veri Sızdırma**: Kötü niyetli aktörlerin sunucuları yetkisiz veri erişimi için proxy olarak kullanmasına olanak tanır  
- **Güven Sınırı İhlalleri**: Token kaynakları hakkında aşağı akış hizmet güven varsayımlarını bozar  
- **Yatay Hareket**: Birden fazla hizmetteki ele geçirilmiş token'lar daha geniş saldırı genişlemesine olanak tanır  

**Uygulama Kontrolleri:**
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

### **Güvenli Token Yönetim Modelleri**

**En İyi Uygulamalar:**
- **Kısa Ömürlü Token'lar**: Sık token yenileme ile maruz kalma süresini en aza indirin  
- **Tam Zamanında Verme**: Token'ları yalnızca belirli işlemler için gerektiğinde verin  
- **Güvenli Depolama**: Donanım güvenlik modülleri (HSM'ler) veya güvenli anahtar kasaları kullanın  
- **Token Bağlama**: Token'ları mümkün olduğunda belirli istemcilere, oturumlara veya işlemlere bağlayın  
- **İzleme ve Uyarı**: Token kötüye kullanımını veya yetkisiz erişim modellerini gerçek zamanlı olarak tespit edin  

## 3. **Oturum Güvenliği Kontrolleri**

### **Oturum Ele Geçirme Önleme**

**Ele Alınan Saldırı Vektörleri:**
- **Oturum Ele Geçirme Komut Enjeksiyonu**: Paylaşılan oturum durumuna kötü niyetli olayların eklenmesi  
- **Oturum Taklidi**: Çalınan oturum kimliklerinin yetkilendirmeyi atlamak için yetkisiz kullanımı  
- **Devam Ettirilebilir Akış Saldırıları**: Sunucu tarafından gönderilen olayların yeniden başlatılmasının kötü niyetli içerik enjeksiyonu için kullanılması  

**Zorunlu Oturum Kontrolleri:**
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

**Taşıma Güvenliği:**
- **HTTPS Zorunluluğu**: Tüm oturum iletişimi TLS 1.3 üzerinden  
- **Güvenli Çerez Nitelikleri**: HttpOnly, Secure, SameSite=Strict  
- **Sertifika Sabitleme**: Ortadaki adam (MITM) saldırılarını önlemek için kritik bağlantılarda  

### **Durumlu ve Durumsuz Uygulamalar**

**Durumlu Uygulamalar İçin:**
- Paylaşılan oturum durumu, enjeksiyon saldırılarına karşı ek koruma gerektirir  
- Kuyruk tabanlı oturum yönetimi, bütünlük doğrulaması gerektirir  
- Birden fazla sunucu örneği, güvenli oturum durumu senkronizasyonu gerektirir  

**Durumsuz Uygulamalar İçin:**
- JWT veya benzeri token tabanlı oturum yönetimi  
- Oturum durumu bütünlüğünün kriptografik doğrulaması  
- Azaltılmış saldırı yüzeyi ancak sağlam token doğrulama gerektirir  

## 4. **Yapay Zeka Özelinde Güvenlik Kontrolleri**

### **Komut Enjeksiyonu Savunması**

**Microsoft Prompt Shields Entegrasyonu:**
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

**Uygulama Kontrolleri:**
- **Girdi Temizleme**: Tüm kullanıcı girdilerinin kapsamlı doğrulaması ve filtrelenmesi  
- **İçerik Sınırı Tanımı**: Sistem talimatları ve kullanıcı içeriği arasında net ayrım  
- **Talimat Hiyerarşisi**: Çelişen talimatlar için uygun öncelik kuralları  
- **Çıktı İzleme**: Potansiyel olarak zararlı veya manipüle edilmiş çıktıları tespit etme  

### **Araç Zehirlenmesini Önleme**

**Araç Güvenlik Çerçevesi:**
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

**Dinamik Araç Yönetimi:**
- **Onay İş Akışları**: Araç değişiklikleri için açık kullanıcı onayı  
- **Geri Alma Yetenekleri**: Önceki araç sürümlerine geri dönme yeteneği  
- **Değişiklik Denetimi**: Araç tanımı değişikliklerinin tam geçmişi  
- **Risk Değerlendirmesi**: Araç güvenlik duruşunun otomatik değerlendirmesi  

## 5. **Karmaşık Vekil Saldırılarını Önleme**

### **OAuth Proxy Güvenliği**

**Saldırı Önleme Kontrolleri:**
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

**Uygulama Gereksinimleri:**
- **Kullanıcı Onayı Doğrulama**: Dinamik istemci kaydı için onay ekranlarını asla atlamayın  
- **Yönlendirme URI Doğrulama**: Yönlendirme hedeflerinin sıkı beyaz liste tabanlı doğrulaması  
- **Yetkilendirme Kodu Koruması**: Tek kullanımlık ve kısa ömürlü kodlar  
- **İstemci Kimliği Doğrulama**: İstemci kimlik bilgileri ve meta verilerinin sağlam doğrulaması  

## 6. **Araç Çalıştırma Güvenliği**

### **Sandboxing ve İzolasyon**

**Konteyner Tabanlı İzolasyon:**
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

**Süreç İzolasyonu:**
- **Ayrı Süreç Bağlamları**: Her araç çalıştırması izole edilmiş süreç alanında  
- **Süreçler Arası İletişim**: Doğrulama ile güvenli IPC mekanizmaları  
- **Süreç İzleme**: Çalışma zamanı davranış analizi ve anomali tespiti  
- **Kaynak Uygulaması**: CPU, bellek ve I/O işlemleri için sıkı sınırlar  

### **En Az Ayrıcalık Uygulaması**

**İzin Yönetimi:**
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

## 7. **Tedarik Zinciri Güvenlik Kontrolleri**

### **Bağımlılık Doğrulama**

**Kapsamlı Bileşen Güvenliği:**
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

### **Sürekli İzleme**

**Tedarik Zinciri Tehdit Algılama:**
- **Bağımlılık Sağlık İzleme**: Tüm bağımlılıkların güvenlik sorunları için sürekli değerlendirilmesi  
- **Tehdit İstihbaratı Entegrasyonu**: Ortaya çıkan tedarik zinciri tehditleri hakkında gerçek zamanlı güncellemeler  
- **Davranış Analizi**: Harici bileşenlerdeki olağandışı davranışların tespiti  
- **Otomatik Yanıt**: Tehlikeye atılmış bileşenlerin anında kontrol altına alınması  

## 8. **İzleme ve Algılama Kontrolleri**

### **Güvenlik Bilgileri ve Olay Yönetimi (SIEM)**

**Kapsamlı Günlükleme Stratejisi:**
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

### **Gerçek Zamanlı Tehdit Algılama**

**Davranış Analitiği:**
- **Kullanıcı Davranışı Analitiği (UBA)**: Olağandışı kullanıcı erişim modellerinin tespiti  
- **Varlık Davranışı Analitiği (EBA)**: MCP sunucusu ve araç davranışlarının izlenmesi  
- **Makine Öğrenimi Anomali Tespiti**: Güvenlik tehditlerinin yapay zeka destekli tespiti  
- **Tehdit İstihbaratı Korelasyonu**: Gözlemlenen etkinliklerin bilinen saldırı modelleriyle eşleştirilmesi  

## 9. **Olay Müdahale ve Kurtarma**

### **Otomatik Yanıt Yetkinlikleri**

**Anında Yanıt Eylemleri:**
```yaml
Threat Containment:
  session_management:
    - "Immediate session termination"
    - "Account lockout procedures"
    - "Access privilege revocation"
  
  system_isolation:
    - "Network segmentation activation"
    - "Service isolation protocols"
    - "Communication channel restriction"

Recovery Procedures:
  credential_rotation:
    - "Automated token refresh"
    - "API key regeneration"
    - "Certificate renewal"
  
  system_restoration:
    - "Clean state restoration"
    - "Configuration rollback"
    - "Service restart procedures"
```

### **Adli Yetkinlikler**

**Soruşturma Desteği:**
- **Denetim İzinin Korunması**: Kriptografik bütünlükle değiştirilemez günlükleme  
- **Kanıt Toplama**: İlgili güvenlik eserlerinin otomatik toplanması  
- **Zaman Çizelgesi Yeniden Yapılandırma**: Güvenlik olaylarına yol açan olayların ayrıntılı sıralaması  
- **Etkilenen Alanın Değerlendirilmesi**: İhlal kapsamının ve veri maruziyetinin değerlendirilmesi  

## **Temel Güvenlik Mimarisi İlkeleri**

### **Derinlemesine Savunma**
- **Birden Fazla Güvenlik Katmanı**: Güvenlik mimarisinde tek bir hata noktası olmaması  
- **Yedekleyici Kontroller**: Kritik işlevler için örtüşen güvenlik önlemleri  
- **Güvenli Varsayılan Mekanizmalar**: Sistemler hata veya saldırılarla karşılaştığında güvenli varsayılanlar  

### **Sıfır Güven Uygulaması**
- **Asla Güvenme, Her Zaman Doğrula**: Tüm varlıkların ve isteklerin sürekli doğrulanması  
- **En Az Ayrıcalık İlkesi**: Tüm bileşenler için minimum erişim hakları  
- **Mikro Segmentasyon**: Ayrıntılı ağ ve erişim kontrolleri  

### **Sürekli Güvenlik Evrimi**
- **Tehdit Ortamına Uyum**: Ortaya çıkan tehditlere yönelik düzenli güncellemeler  
- **Güvenlik Kontrol Etkinliği**: Kontrollerin sürekli değerlendirilmesi ve iyileştirilmesi  
- **Spesifikasyon Uyumluluğu**: Gelişen MCP güvenlik standartlarıyla uyum  

---

## **Uygulama Kaynakları**

### **Resmi MCP Belgeleri**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Güvenlik En İyi Uygulamaları](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Yetkilendirme Spesifikasyonu](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft Güvenlik Çözümleri**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure İçerik Güvenliği](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Gelişmiş Güvenlik](https://github.com/security/advanced-security)  
- [Azure Anahtar Kasası](https://learn.microsoft.com/azure/key-vault/)  

### **Güvenlik Standartları**
- [OAuth 2.0 Güvenlik En İyi Uygulamaları (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Büyük Dil Modelleri için İlk 10](https://genai.owasp.org/)  
- [NIST Siber Güvenlik Çerçevesi](https://www.nist.gov/cyberframework)  

---

> **Önemli**: Bu güvenlik kontrolleri, mevcut MCP spesifikasyonunu (2025-06-18) yansıtmaktadır. Standartlar hızla gelişmeye devam ettiğinden, her zaman en son [resmi belgeleri](https://spec.modelcontextprotocol.io/) kontrol edin.

**Feragatname**:  
Bu belge, [Co-op Translator](https://github.com/Azure/co-op-translator) adlı yapay zeka çeviri hizmeti kullanılarak çevrilmiştir. Doğruluk için çaba göstersek de, otomatik çevirilerin hata veya yanlışlıklar içerebileceğini lütfen unutmayın. Orijinal belgenin kendi dilindeki hali yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımından kaynaklanan yanlış anlamalar veya yanlış yorumlamalar için sorumluluk kabul etmiyoruz.