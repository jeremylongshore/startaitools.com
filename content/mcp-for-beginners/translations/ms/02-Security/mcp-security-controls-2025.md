<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T17:59:09+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "ms"
}
-->
# Kawalan Keselamatan MCP - Kemas Kini Ogos 2025

> **Standard Semasa**: Dokumen ini mencerminkan keperluan keselamatan [Spesifikasi MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) dan [Amalan Terbaik Keselamatan MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) rasmi.

Model Context Protocol (MCP) telah berkembang dengan ketara dengan kawalan keselamatan yang dipertingkatkan untuk menangani ancaman keselamatan perisian tradisional dan ancaman khusus AI. Dokumen ini menyediakan kawalan keselamatan yang komprehensif untuk pelaksanaan MCP yang selamat sehingga Ogos 2025.

## **Keperluan Keselamatan WAJIB**

### **Larangan Kritikal dari Spesifikasi MCP:**

> **DILARANG**: Pelayan MCP **TIDAK BOLEH** menerima sebarang token yang tidak dikeluarkan secara eksplisit untuk pelayan MCP  
>
> **DILARANG**: Pelayan MCP **TIDAK BOLEH** menggunakan sesi untuk pengesahan  
>
> **WAJIB**: Pelayan MCP yang melaksanakan kebenaran **HARUS** mengesahkan SEMUA permintaan masuk  
>
> **WAJIB**: Pelayan proksi MCP yang menggunakan ID pelanggan statik **HARUS** mendapatkan persetujuan pengguna untuk setiap pelanggan yang didaftarkan secara dinamik  

---

## 1. **Kawalan Pengesahan & Kebenaran**

### **Integrasi Penyedia Identiti Luaran**

**Standard MCP Semasa (2025-06-18)** membenarkan pelayan MCP untuk mendelegasikan pengesahan kepada penyedia identiti luaran, mewakili peningkatan keselamatan yang ketara:

**Manfaat Keselamatan:**
1. **Menghapuskan Risiko Pengesahan Tersuai**: Mengurangkan permukaan kerentanan dengan mengelakkan pelaksanaan pengesahan tersuai  
2. **Keselamatan Gred Perusahaan**: Memanfaatkan penyedia identiti yang mapan seperti Microsoft Entra ID dengan ciri keselamatan canggih  
3. **Pengurusan Identiti Berpusat**: Memudahkan pengurusan kitaran hayat pengguna, kawalan akses, dan pengauditan pematuhan  
4. **Pengesahan Pelbagai Faktor**: Mewarisi keupayaan MFA daripada penyedia identiti perusahaan  
5. **Dasar Akses Bersyarat**: Mendapat manfaat daripada kawalan akses berdasarkan risiko dan pengesahan adaptif  

**Keperluan Pelaksanaan:**
- **Pengesahan Penonton Token**: Pastikan semua token dikeluarkan secara eksplisit untuk pelayan MCP  
- **Pengesahan Penerbit**: Sahkan penerbit token sepadan dengan penyedia identiti yang dijangka  
- **Pengesahan Tandatangan**: Pengesahan kriptografi integriti token  
- **Penguatkuasaan Tamat Tempoh**: Penguatkuasaan ketat had masa hayat token  
- **Pengesahan Skop**: Pastikan token mengandungi kebenaran yang sesuai untuk operasi yang diminta  

### **Keselamatan Logik Kebenaran**

**Kawalan Kritikal:**
- **Audit Kebenaran Komprehensif**: Kajian keselamatan berkala pada semua titik keputusan kebenaran  
- **Default Gagal-Selamat**: Menolak akses apabila logik kebenaran tidak dapat membuat keputusan yang pasti  
- **Sempadan Kebenaran**: Pemisahan yang jelas antara tahap keistimewaan dan akses sumber  
- **Pelogkan Audit**: Pelogkan lengkap semua keputusan kebenaran untuk pemantauan keselamatan  
- **Kajian Akses Berkala**: Pengesahan berkala ke atas kebenaran pengguna dan penugasan keistimewaan  

## 2. **Keselamatan Token & Kawalan Anti-Passthrough**

### **Pencegahan Passthrough Token**

**Passthrough token secara eksplisit dilarang** dalam Spesifikasi Kebenaran MCP kerana risiko keselamatan yang kritikal:

**Risiko Keselamatan Ditangani:**
- **Pelanggaran Kawalan**: Memintas kawalan keselamatan penting seperti had kadar, pengesahan permintaan, dan pemantauan trafik  
- **Kerosakan Akauntabiliti**: Menjadikan pengenalan pelanggan mustahil, merosakkan jejak audit dan penyiasatan insiden  
- **Eksfiltrasi Berasaskan Proksi**: Membolehkan pelaku jahat menggunakan pelayan sebagai proksi untuk akses data tanpa kebenaran  
- **Pelanggaran Sempadan Kepercayaan**: Merosakkan andaian kepercayaan perkhidmatan hiliran tentang asal token  
- **Pergerakan Lateral**: Token yang dikompromi merentasi pelbagai perkhidmatan membolehkan pengembangan serangan yang lebih luas  

**Kawalan Pelaksanaan:**
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

### **Pola Pengurusan Token Selamat**

**Amalan Terbaik:**
- **Token Jangka Pendek**: Meminimumkan tetingkap pendedahan dengan putaran token yang kerap  
- **Pengeluaran Tepat Pada Masanya**: Mengeluarkan token hanya apabila diperlukan untuk operasi tertentu  
- **Penyimpanan Selamat**: Gunakan modul keselamatan perkakasan (HSM) atau peti kunci selamat  
- **Pengikatan Token**: Mengikat token kepada pelanggan, sesi, atau operasi tertentu jika boleh  
- **Pemantauan & Peringatan**: Pengesanan masa nyata penyalahgunaan token atau pola akses tanpa kebenaran  

## 3. **Kawalan Keselamatan Sesi**

### **Pencegahan Pengambilalihan Sesi**

**Vektor Serangan Ditangani:**
- **Suntikan Prompt Pengambilalihan Sesi**: Peristiwa jahat disuntik ke dalam keadaan sesi yang dikongsi  
- **Penyamaran Sesi**: Penggunaan tanpa kebenaran ID sesi yang dicuri untuk memintas pengesahan  
- **Serangan Aliran Boleh Disambung Semula**: Eksploitasi penyambungan semula acara yang dihantar oleh pelayan untuk suntikan kandungan jahat  

**Kawalan Sesi Wajib:**
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

**Keselamatan Pengangkutan:**
- **Penguatkuasaan HTTPS**: Semua komunikasi sesi melalui TLS 1.3  
- **Atribut Kuki Selamat**: HttpOnly, Secure, SameSite=Strict  
- **Pinning Sijil**: Untuk sambungan kritikal bagi mencegah serangan MITM  

### **Pertimbangan Stateful vs Stateless**

**Untuk Pelaksanaan Stateful:**
- Keadaan sesi yang dikongsi memerlukan perlindungan tambahan terhadap serangan suntikan  
- Pengurusan sesi berasaskan barisan memerlukan pengesahan integriti  
- Pelbagai instance pelayan memerlukan penyegerakan keadaan sesi yang selamat  

**Untuk Pelaksanaan Stateless:**
- Pengurusan sesi berasaskan token seperti JWT  
- Pengesahan kriptografi integriti keadaan sesi  
- Permukaan serangan yang dikurangkan tetapi memerlukan pengesahan token yang kukuh  

## 4. **Kawalan Keselamatan Khusus AI**

### **Pertahanan Suntikan Prompt**

**Integrasi Microsoft Prompt Shields:**
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

**Kawalan Pelaksanaan:**
- **Pembersihan Input**: Pengesahan dan penapisan komprehensif semua input pengguna  
- **Definisi Sempadan Kandungan**: Pemisahan yang jelas antara arahan sistem dan kandungan pengguna  
- **Hierarki Arahan**: Peraturan keutamaan yang betul untuk arahan yang bercanggah  
- **Pemantauan Output**: Pengesanan output yang berpotensi berbahaya atau dimanipulasi  

### **Pencegahan Keracunan Alat**

**Kerangka Keselamatan Alat:**
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

**Pengurusan Alat Dinamik:**
- **Aliran Kerja Kelulusan**: Persetujuan pengguna eksplisit untuk pengubahsuaian alat  
- **Keupayaan Rollback**: Keupayaan untuk kembali ke versi alat sebelumnya  
- **Pengauditan Perubahan**: Sejarah lengkap pengubahsuaian definisi alat  
- **Penilaian Risiko**: Penilaian automatik terhadap postur keselamatan alat  

## 5. **Pencegahan Serangan Confused Deputy**

### **Keselamatan Proksi OAuth**

**Kawalan Pencegahan Serangan:**
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

**Keperluan Pelaksanaan:**
- **Pengesahan Persetujuan Pengguna**: Jangan sekali-kali melangkau skrin persetujuan untuk pendaftaran pelanggan dinamik  
- **Pengesahan URI Pengalihan**: Pengesahan berasaskan senarai putih yang ketat untuk destinasi pengalihan  
- **Perlindungan Kod Kebenaran**: Kod jangka pendek dengan penguatkuasaan penggunaan tunggal  
- **Pengesahan Identiti Pelanggan**: Pengesahan kukuh terhadap kelayakan dan metadata pelanggan  

## 6. **Keselamatan Pelaksanaan Alat**

### **Pengasingan & Kotak Pasir**

**Pengasingan Berasaskan Kontena:**
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

**Pengasingan Proses:**
- **Konteks Proses Berasingan**: Setiap pelaksanaan alat dalam ruang proses yang diasingkan  
- **Komunikasi Antara Proses**: Mekanisme IPC yang selamat dengan pengesahan  
- **Pemantauan Proses**: Analisis tingkah laku masa nyata dan pengesanan anomali  
- **Penguatkuasaan Sumber**: Had keras pada CPU, memori, dan operasi I/O  

### **Pelaksanaan Keistimewaan Minimum**

**Pengurusan Kebenaran:**
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

## 7. **Kawalan Keselamatan Rantaian Bekalan**

### **Pengesahan Kebergantungan**

**Keselamatan Komponen Komprehensif:**
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

### **Pemantauan Berterusan**

**Pengesanan Ancaman Rantaian Bekalan:**
- **Pemantauan Kesihatan Kebergantungan**: Penilaian berterusan terhadap semua kebergantungan untuk isu keselamatan  
- **Integrasi Perisikan Ancaman**: Kemas kini masa nyata tentang ancaman rantaian bekalan yang muncul  
- **Analisis Tingkah Laku**: Pengesanan tingkah laku luar biasa dalam komponen luaran  
- **Tindak Balas Automatik**: Penahanan segera komponen yang dikompromi  

## 8. **Kawalan Pemantauan & Pengesanan**

### **Pengurusan Maklumat Keselamatan dan Peristiwa (SIEM)**

**Strategi Pelogkan Komprehensif:**
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

### **Pengesanan Ancaman Masa Nyata**

**Analitik Tingkah Laku:**
- **Analitik Tingkah Laku Pengguna (UBA)**: Pengesanan pola akses pengguna yang luar biasa  
- **Analitik Tingkah Laku Entiti (EBA)**: Pemantauan tingkah laku pelayan MCP dan alat  
- **Pengesanan Anomali Pembelajaran Mesin**: Pengenalpastian ancaman keselamatan yang dikuasakan AI  
- **Korelasi Perisikan Ancaman**: Padanan aktiviti yang diperhatikan dengan pola serangan yang diketahui  

## 9. **Tindak Balas & Pemulihan Insiden**

### **Keupayaan Tindak Balas Automatik**

**Tindakan Tindak Balas Segera:**
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

### **Keupayaan Forensik**

**Sokongan Penyiasatan:**
- **Pemeliharaan Jejak Audit**: Pelogkan tidak boleh diubah dengan integriti kriptografi  
- **Pengumpulan Bukti**: Pengumpulan automatik artifak keselamatan yang relevan  
- **Rekonstruksi Garis Masa**: Urutan peristiwa terperinci yang membawa kepada insiden keselamatan  
- **Penilaian Impak**: Penilaian skop kompromi dan pendedahan data  

## **Prinsip Seni Bina Keselamatan Utama**

### **Pertahanan Mendalam**
- **Lapisan Keselamatan Pelbagai**: Tiada satu titik kegagalan dalam seni bina keselamatan  
- **Kawalan Redundan**: Langkah keselamatan yang bertindih untuk fungsi kritikal  
- **Mekanisme Gagal-Selamat**: Default selamat apabila sistem menghadapi ralat atau serangan  

### **Pelaksanaan Zero Trust**
- **Jangan Percaya, Sentiasa Sahkan**: Pengesahan berterusan terhadap semua entiti dan permintaan  
- **Prinsip Keistimewaan Minimum**: Hak akses minimum untuk semua komponen  
- **Mikro-Segmentasi**: Kawalan rangkaian dan akses yang granular  

### **Evolusi Keselamatan Berterusan**
- **Adaptasi Landskap Ancaman**: Kemas kini berkala untuk menangani ancaman yang muncul  
- **Keberkesanan Kawalan Keselamatan**: Penilaian dan penambahbaikan berterusan kawalan  
- **Pematuhan Spesifikasi**: Penjajaran dengan standard keselamatan MCP yang berkembang  

---

## **Sumber Pelaksanaan**

### **Dokumentasi MCP Rasmi**
- [Spesifikasi MCP (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [Amalan Terbaik Keselamatan MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [Spesifikasi Kebenaran MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Penyelesaian Keselamatan Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Standard Keselamatan**
- [Amalan Terbaik Keselamatan OAuth 2.0 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 untuk Model Bahasa Besar](https://genai.owasp.org/)  
- [Kerangka Keselamatan Siber NIST](https://www.nist.gov/cyberframework)  

---

> **Penting**: Kawalan keselamatan ini mencerminkan spesifikasi MCP semasa (2025-06-18). Sentiasa sahkan dengan [dokumentasi rasmi](https://spec.modelcontextprotocol.io/) terkini kerana standard terus berkembang dengan pantas.

**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk memastikan ketepatan, sila ambil perhatian bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang berwibawa. Untuk maklumat penting, terjemahan manusia profesional adalah disyorkan. Kami tidak bertanggungjawab atas sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.