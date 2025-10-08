<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T17:38:50+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "id"
}
-->
# Kontrol Keamanan MCP - Pembaruan Agustus 2025

> **Standar Saat Ini**: Dokumen ini mencerminkan persyaratan keamanan [Spesifikasi MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) dan [Praktik Terbaik Keamanan MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) resmi.

Model Context Protocol (MCP) telah berkembang secara signifikan dengan kontrol keamanan yang ditingkatkan untuk mengatasi ancaman keamanan perangkat lunak tradisional dan ancaman spesifik AI. Dokumen ini menyediakan kontrol keamanan komprehensif untuk implementasi MCP yang aman per Agustus 2025.

## **Persyaratan Keamanan WAJIB**

### **Larangan Kritis dari Spesifikasi MCP:**

> **DILARANG**: Server MCP **TIDAK BOLEH** menerima token apa pun yang tidak secara eksplisit diterbitkan untuk server MCP  
>
> **TERLARANG**: Server MCP **TIDAK BOLEH** menggunakan sesi untuk autentikasi  
>
> **WAJIB**: Server MCP yang mengimplementasikan otorisasi **HARUS** memverifikasi SEMUA permintaan masuk  
>
> **MANDATORI**: Server proxy MCP yang menggunakan ID klien statis **HARUS** mendapatkan persetujuan pengguna untuk setiap klien yang didaftarkan secara dinamis  

---

## 1. **Kontrol Autentikasi & Otorisasi**

### **Integrasi Penyedia Identitas Eksternal**

**Standar MCP Saat Ini (2025-06-18)** memungkinkan server MCP mendelegasikan autentikasi ke penyedia identitas eksternal, yang merupakan peningkatan keamanan yang signifikan:

**Manfaat Keamanan:**
1. **Menghilangkan Risiko Autentikasi Kustom**: Mengurangi permukaan kerentanan dengan menghindari implementasi autentikasi kustom  
2. **Keamanan Kelas Enterprise**: Memanfaatkan penyedia identitas mapan seperti Microsoft Entra ID dengan fitur keamanan canggih  
3. **Manajemen Identitas Terpusat**: Menyederhanakan pengelolaan siklus hidup pengguna, kontrol akses, dan audit kepatuhan  
4. **Autentikasi Multi-Faktor**: Mendapatkan kemampuan MFA dari penyedia identitas enterprise  
5. **Kebijakan Akses Bersyarat**: Memanfaatkan kontrol akses berbasis risiko dan autentikasi adaptif  

**Persyaratan Implementasi:**
- **Validasi Audiens Token**: Verifikasi semua token diterbitkan secara eksplisit untuk server MCP  
- **Verifikasi Penerbit**: Validasi penerbit token sesuai dengan penyedia identitas yang diharapkan  
- **Verifikasi Tanda Tangan**: Validasi kriptografi untuk integritas token  
- **Penegakan Kedaluwarsa**: Penegakan ketat terhadap batas waktu hidup token  
- **Validasi Ruang Lingkup**: Pastikan token memiliki izin yang sesuai untuk operasi yang diminta  

### **Keamanan Logika Otorisasi**

**Kontrol Kritis:**
- **Audit Otorisasi Komprehensif**: Tinjauan keamanan rutin terhadap semua titik keputusan otorisasi  
- **Default Aman**: Tolak akses jika logika otorisasi tidak dapat membuat keputusan yang pasti  
- **Batasan Izin**: Pemisahan yang jelas antara tingkat hak istimewa dan akses sumber daya  
- **Pencatatan Audit**: Pencatatan lengkap semua keputusan otorisasi untuk pemantauan keamanan  
- **Tinjauan Akses Rutin**: Validasi berkala terhadap izin pengguna dan penugasan hak istimewa  

## 2. **Keamanan Token & Kontrol Anti-Passthrough**

### **Pencegahan Passthrough Token**

**Passthrough token secara eksplisit dilarang** dalam Spesifikasi Otorisasi MCP karena risiko keamanan yang kritis:

**Risiko Keamanan yang Ditangani:**
- **Pengelakan Kontrol**: Melewati kontrol keamanan penting seperti pembatasan laju, validasi permintaan, dan pemantauan lalu lintas  
- **Kerusakan Akuntabilitas**: Membuat identifikasi klien tidak mungkin, merusak jejak audit dan investigasi insiden  
- **Eksfiltrasi Berbasis Proxy**: Memungkinkan aktor jahat menggunakan server sebagai proxy untuk akses data yang tidak sah  
- **Pelanggaran Batas Kepercayaan**: Merusak asumsi kepercayaan layanan downstream tentang asal token  
- **Pergerakan Lateral**: Token yang dikompromikan di beberapa layanan memungkinkan perluasan serangan yang lebih luas  

**Kontrol Implementasi:**
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

### **Pola Manajemen Token yang Aman**

**Praktik Terbaik:**
- **Token Berumur Pendek**: Meminimalkan jendela eksposur dengan rotasi token yang sering  
- **Penerbitan Tepat Waktu**: Menerbitkan token hanya saat diperlukan untuk operasi tertentu  
- **Penyimpanan Aman**: Gunakan modul keamanan perangkat keras (HSM) atau brankas kunci yang aman  
- **Pengikatan Token**: Mengikat token ke klien, sesi, atau operasi tertentu jika memungkinkan  
- **Pemantauan & Peringatan**: Deteksi waktu nyata terhadap penyalahgunaan token atau pola akses tidak sah  

## 3. **Kontrol Keamanan Sesi**

### **Pencegahan Pembajakan Sesi**

**Vektor Serangan yang Ditangani:**
- **Penyuntikan Prompt Pembajakan Sesi**: Peristiwa berbahaya yang disuntikkan ke dalam status sesi bersama  
- **Penyamaran Sesi**: Penggunaan tidak sah dari ID sesi yang dicuri untuk melewati autentikasi  
- **Serangan Aliran yang Dapat Dilanjutkan**: Eksploitasi kelanjutan peristiwa yang dikirim server untuk penyuntikan konten berbahaya  

**Kontrol Sesi Wajib:**
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

**Keamanan Transportasi:**
- **Penegakan HTTPS**: Semua komunikasi sesi melalui TLS 1.3  
- **Atribut Cookie Aman**: HttpOnly, Secure, SameSite=Strict  
- **Pinning Sertifikat**: Untuk koneksi penting guna mencegah serangan MITM  

### **Pertimbangan Stateful vs Stateless**

**Untuk Implementasi Stateful:**
- Status sesi bersama memerlukan perlindungan tambahan terhadap serangan penyuntikan  
- Manajemen sesi berbasis antrian memerlukan verifikasi integritas  
- Beberapa instance server memerlukan sinkronisasi status sesi yang aman  

**Untuk Implementasi Stateless:**
- Manajemen sesi berbasis token seperti JWT  
- Verifikasi kriptografi terhadap integritas status sesi  
- Permukaan serangan yang lebih kecil tetapi memerlukan validasi token yang kuat  

## 4. **Kontrol Keamanan Spesifik AI**

### **Pertahanan Penyuntikan Prompt**

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

**Kontrol Implementasi:**
- **Sanitasi Input**: Validasi dan penyaringan komprehensif terhadap semua input pengguna  
- **Definisi Batas Konten**: Pemisahan yang jelas antara instruksi sistem dan konten pengguna  
- **Hierarki Instruksi**: Aturan prioritas yang tepat untuk instruksi yang bertentangan  
- **Pemantauan Output**: Deteksi output yang berpotensi berbahaya atau dimanipulasi  

### **Pencegahan Peracunan Alat**

**Kerangka Keamanan Alat:**
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

**Manajemen Alat Dinamis:**
- **Alur Persetujuan**: Persetujuan eksplisit pengguna untuk modifikasi alat  
- **Kemampuan Rollback**: Kemampuan untuk mengembalikan ke versi alat sebelumnya  
- **Audit Perubahan**: Riwayat lengkap modifikasi definisi alat  
- **Penilaian Risiko**: Evaluasi otomatis terhadap postur keamanan alat  

## 5. **Pencegahan Serangan Confused Deputy**

### **Keamanan Proxy OAuth**

**Kontrol Pencegahan Serangan:**
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

**Persyaratan Implementasi:**
- **Verifikasi Persetujuan Pengguna**: Jangan pernah melewati layar persetujuan untuk pendaftaran klien dinamis  
- **Validasi URI Pengalihan**: Validasi berbasis daftar putih yang ketat terhadap tujuan pengalihan  
- **Perlindungan Kode Otorisasi**: Kode berumur pendek dengan penegakan penggunaan tunggal  
- **Verifikasi Identitas Klien**: Validasi yang kuat terhadap kredensial dan metadata klien  

## 6. **Keamanan Eksekusi Alat**

### **Sandboxing & Isolasi**

**Isolasi Berbasis Kontainer:**
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

**Isolasi Proses:**
- **Konteks Proses Terpisah**: Setiap eksekusi alat dalam ruang proses yang terisolasi  
- **Komunikasi Antar-Proses**: Mekanisme IPC yang aman dengan validasi  
- **Pemantauan Proses**: Analisis perilaku runtime dan deteksi anomali  
- **Penegakan Sumber Daya**: Batas keras pada operasi CPU, memori, dan I/O  

### **Implementasi Hak Istimewa Minimum**

**Manajemen Izin:**
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

## 7. **Kontrol Keamanan Rantai Pasokan**

### **Verifikasi Ketergantungan**

**Keamanan Komponen Komprehensif:**
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

### **Pemantauan Berkelanjutan**

**Deteksi Ancaman Rantai Pasokan:**
- **Pemantauan Kesehatan Ketergantungan**: Penilaian berkelanjutan terhadap semua ketergantungan untuk masalah keamanan  
- **Integrasi Intelijen Ancaman**: Pembaruan waktu nyata tentang ancaman rantai pasokan yang muncul  
- **Analisis Perilaku**: Deteksi perilaku tidak biasa dalam komponen eksternal  
- **Respons Otomatis**: Penahanan langsung terhadap komponen yang dikompromikan  

## 8. **Kontrol Pemantauan & Deteksi**

### **Manajemen Informasi Keamanan dan Peristiwa (SIEM)**

**Strategi Pencatatan Komprehensif:**
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

### **Deteksi Ancaman Waktu Nyata**

**Analitik Perilaku:**
- **Analitik Perilaku Pengguna (UBA)**: Deteksi pola akses pengguna yang tidak biasa  
- **Analitik Perilaku Entitas (EBA)**: Pemantauan perilaku server MCP dan alat  
- **Deteksi Anomali Berbasis Pembelajaran Mesin**: Identifikasi ancaman keamanan yang didukung AI  
- **Korelasi Intelijen Ancaman**: Mencocokkan aktivitas yang diamati dengan pola serangan yang diketahui  

## 9. **Respons & Pemulihan Insiden**

### **Kemampuan Respons Otomatis**

**Tindakan Respons Langsung:**
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

### **Kemampuan Forensik**

**Dukungan Investigasi:**
- **Pelestarian Jejak Audit**: Pencatatan yang tidak dapat diubah dengan integritas kriptografi  
- **Pengumpulan Bukti**: Pengumpulan otomatis artefak keamanan yang relevan  
- **Rekonstruksi Garis Waktu**: Urutan peristiwa yang terperinci menuju insiden keamanan  
- **Penilaian Dampak**: Evaluasi cakupan kompromi dan eksposur data  

## **Prinsip Arsitektur Keamanan Utama**

### **Pertahanan Berlapis**
- **Banyak Lapisan Keamanan**: Tidak ada titik kegagalan tunggal dalam arsitektur keamanan  
- **Kontrol Redundan**: Langkah-langkah keamanan yang saling tumpang tindih untuk fungsi penting  
- **Mekanisme Aman Default**: Default aman saat sistem menghadapi kesalahan atau serangan  

### **Implementasi Zero Trust**
- **Jangan Pernah Percaya, Selalu Verifikasi**: Validasi terus-menerus terhadap semua entitas dan permintaan  
- **Prinsip Hak Istimewa Minimum**: Hak akses minimal untuk semua komponen  
- **Segmentasi Mikro**: Kontrol jaringan dan akses yang granular  

### **Evolusi Keamanan Berkelanjutan**
- **Adaptasi Lanskap Ancaman**: Pembaruan rutin untuk mengatasi ancaman yang muncul  
- **Efektivitas Kontrol Keamanan**: Evaluasi dan peningkatan berkelanjutan terhadap kontrol  
- **Kepatuhan Spesifikasi**: Penyesuaian dengan standar keamanan MCP yang terus berkembang  

---

## **Sumber Daya Implementasi**

### **Dokumentasi Resmi MCP**
- [Spesifikasi MCP (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [Praktik Terbaik Keamanan MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [Spesifikasi Otorisasi MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Solusi Keamanan Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Standar Keamanan**
- [Praktik Terbaik Keamanan OAuth 2.0 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 untuk Model Bahasa Besar](https://genai.owasp.org/)  
- [Kerangka Kerja Keamanan Siber NIST](https://www.nist.gov/cyberframework)  

---

> **Penting**: Kontrol keamanan ini mencerminkan spesifikasi MCP saat ini (2025-06-18). Selalu verifikasi terhadap [dokumentasi resmi](https://spec.modelcontextprotocol.io/) terbaru karena standar terus berkembang dengan cepat.

**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan layanan penerjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk memberikan hasil yang akurat, harap diperhatikan bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang berwenang. Untuk informasi yang bersifat kritis, disarankan menggunakan jasa penerjemahan manusia profesional. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.