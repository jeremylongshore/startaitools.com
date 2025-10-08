<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T17:37:57+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "id"
}
-->
# Praktik Keamanan Terbaik MCP 2025

Panduan komprehensif ini menjelaskan praktik keamanan penting untuk mengimplementasikan sistem Model Context Protocol (MCP) berdasarkan **Spesifikasi MCP 2025-06-18** terbaru dan standar industri terkini. Praktik ini mencakup kekhawatiran keamanan tradisional serta ancaman spesifik AI yang unik untuk penerapan MCP.

## Persyaratan Keamanan Kritis

### Kontrol Keamanan Wajib (Persyaratan HARUS)

1. **Validasi Token**: Server MCP **TIDAK BOLEH** menerima token apa pun yang tidak secara eksplisit diterbitkan untuk server MCP itu sendiri.
2. **Verifikasi Otorisasi**: Server MCP yang menerapkan otorisasi **HARUS** memverifikasi SEMUA permintaan masuk dan **TIDAK BOLEH** menggunakan sesi untuk autentikasi.  
3. **Persetujuan Pengguna**: Server proxy MCP yang menggunakan ID klien statis **HARUS** mendapatkan persetujuan eksplisit dari pengguna untuk setiap klien yang didaftarkan secara dinamis.
4. **ID Sesi Aman**: Server MCP **HARUS** menggunakan ID sesi yang aman secara kriptografis, non-deterministik, yang dihasilkan dengan generator angka acak yang aman.

## Praktik Keamanan Inti

### 1. Validasi & Sanitasi Input
- **Validasi Input Komprehensif**: Validasi dan sanitasi semua input untuk mencegah serangan injeksi, masalah confused deputy, dan kerentanan injeksi prompt.
- **Penegakan Skema Parameter**: Terapkan validasi skema JSON yang ketat untuk semua parameter alat dan input API.
- **Penyaringan Konten**: Gunakan Microsoft Prompt Shields dan Azure Content Safety untuk menyaring konten berbahaya dalam prompt dan respons.
- **Sanitasi Output**: Validasi dan sanitasi semua output model sebelum disajikan kepada pengguna atau sistem downstream.

### 2. Keunggulan Autentikasi & Otorisasi  
- **Penyedia Identitas Eksternal**: Delegasikan autentikasi ke penyedia identitas yang sudah mapan (Microsoft Entra ID, penyedia OAuth 2.1) daripada membuat autentikasi khusus.
- **Izin yang Terperinci**: Terapkan izin spesifik alat yang terperinci sesuai dengan prinsip hak akses minimum.
- **Manajemen Siklus Hidup Token**: Gunakan token akses berumur pendek dengan rotasi yang aman dan validasi audiens yang tepat.
- **Autentikasi Multi-Faktor**: Wajibkan MFA untuk semua akses administratif dan operasi sensitif.

### 3. Protokol Komunikasi Aman
- **Keamanan Lapisan Transportasi**: Gunakan HTTPS/TLS 1.3 untuk semua komunikasi MCP dengan validasi sertifikat yang tepat.
- **Enkripsi Ujung ke Ujung**: Terapkan lapisan enkripsi tambahan untuk data yang sangat sensitif saat transit dan saat disimpan.
- **Manajemen Sertifikat**: Kelola siklus hidup sertifikat dengan proses pembaruan otomatis.
- **Penegakan Versi Protokol**: Gunakan versi protokol MCP terkini (2025-06-18) dengan negosiasi versi yang tepat.

### 4. Pembatasan Tingkat Lanjut & Perlindungan Sumber Daya
- **Pembatasan Tingkat Multi-Lapisan**: Terapkan pembatasan tingkat pada tingkat pengguna, sesi, alat, dan sumber daya untuk mencegah penyalahgunaan.
- **Pembatasan Tingkat Adaptif**: Gunakan pembatasan tingkat berbasis pembelajaran mesin yang beradaptasi dengan pola penggunaan dan indikator ancaman.
- **Manajemen Kuota Sumber Daya**: Tetapkan batas yang sesuai untuk sumber daya komputasi, penggunaan memori, dan waktu eksekusi.
- **Perlindungan DDoS**: Terapkan perlindungan DDoS yang komprehensif dan sistem analisis lalu lintas.

### 5. Logging & Pemantauan Komprehensif
- **Logging Audit Terstruktur**: Terapkan log yang terperinci dan dapat dicari untuk semua operasi MCP, eksekusi alat, dan peristiwa keamanan.
- **Pemantauan Keamanan Real-time**: Gunakan sistem SIEM dengan deteksi anomali berbasis AI untuk beban kerja MCP.
- **Logging yang Mematuhi Privasi**: Catat peristiwa keamanan sambil menghormati persyaratan dan regulasi privasi data.
- **Integrasi Respons Insiden**: Hubungkan sistem logging ke alur kerja respons insiden otomatis.

### 6. Praktik Penyimpanan Aman yang Ditingkatkan
- **Modul Keamanan Perangkat Keras**: Gunakan penyimpanan kunci yang didukung HSM (Azure Key Vault, AWS CloudHSM) untuk operasi kriptografi penting.
- **Manajemen Kunci Enkripsi**: Terapkan rotasi kunci, segregasi, dan kontrol akses yang tepat untuk kunci enkripsi.
- **Manajemen Rahasia**: Simpan semua kunci API, token, dan kredensial dalam sistem manajemen rahasia khusus.
- **Klasifikasi Data**: Klasifikasikan data berdasarkan tingkat sensitivitas dan terapkan langkah-langkah perlindungan yang sesuai.

### 7. Manajemen Token Lanjutan
- **Pencegahan Passthrough Token**: Secara eksplisit melarang pola passthrough token yang melewati kontrol keamanan.
- **Validasi Audiens**: Selalu verifikasi klaim audiens token sesuai dengan identitas server MCP yang dimaksud.
- **Otorisasi Berbasis Klaim**: Terapkan otorisasi terperinci berdasarkan klaim token dan atribut pengguna.
- **Pengikatan Token**: Ikat token ke sesi, pengguna, atau perangkat tertentu jika diperlukan.

### 8. Manajemen Sesi Aman
- **ID Sesi Kriptografis**: Hasilkan ID sesi menggunakan generator angka acak yang aman secara kriptografis (bukan urutan yang dapat diprediksi).
- **Pengikatan Spesifik Pengguna**: Ikat ID sesi ke informasi spesifik pengguna menggunakan format aman seperti `<user_id>:<session_id>`.
- **Kontrol Siklus Hidup Sesi**: Terapkan mekanisme kedaluwarsa, rotasi, dan pembatalan sesi yang tepat.
- **Header Keamanan Sesi**: Gunakan header HTTP keamanan yang sesuai untuk perlindungan sesi.

### 9. Kontrol Keamanan Spesifik AI
- **Pertahanan Injeksi Prompt**: Terapkan Microsoft Prompt Shields dengan teknik spotlighting, delimiter, dan datamarking.
- **Pencegahan Peracunan Alat**: Validasi metadata alat, pantau perubahan dinamis, dan verifikasi integritas alat.
- **Validasi Output Model**: Pindai output model untuk potensi kebocoran data, konten berbahaya, atau pelanggaran kebijakan keamanan.
- **Perlindungan Jendela Konteks**: Terapkan kontrol untuk mencegah peracunan jendela konteks dan serangan manipulasi.

### 10. Keamanan Eksekusi Alat
- **Sandboxing Eksekusi**: Jalankan eksekusi alat dalam lingkungan terisolasi yang terkontainerisasi dengan batas sumber daya.
- **Pemisahan Hak Istimewa**: Eksekusi alat dengan hak istimewa minimal yang diperlukan dan akun layanan terpisah.
- **Isolasi Jaringan**: Terapkan segmentasi jaringan untuk lingkungan eksekusi alat.
- **Pemantauan Eksekusi**: Pantau eksekusi alat untuk perilaku anomali, penggunaan sumber daya, dan pelanggaran keamanan.

### 11. Validasi Keamanan Berkelanjutan
- **Pengujian Keamanan Otomatis**: Integrasikan pengujian keamanan ke dalam pipeline CI/CD dengan alat seperti GitHub Advanced Security.
- **Manajemen Kerentanan**: Secara rutin pindai semua dependensi, termasuk model AI dan layanan eksternal.
- **Pengujian Penetrasi**: Lakukan penilaian keamanan secara rutin yang secara khusus menargetkan implementasi MCP.
- **Tinjauan Kode Keamanan**: Terapkan tinjauan keamanan wajib untuk semua perubahan kode terkait MCP.

### 12. Keamanan Rantai Pasokan untuk AI
- **Verifikasi Komponen**: Verifikasi asal, integritas, dan keamanan semua komponen AI (model, embedding, API).
- **Manajemen Dependensi**: Pertahankan inventaris terkini dari semua perangkat lunak dan dependensi AI dengan pelacakan kerentanan.
- **Repositori Tepercaya**: Gunakan sumber yang diverifikasi dan tepercaya untuk semua model AI, pustaka, dan alat.
- **Pemantauan Rantai Pasokan**: Pantau secara terus-menerus untuk kompromi pada penyedia layanan AI dan repositori model.

## Pola Keamanan Lanjutan

### Arsitektur Zero Trust untuk MCP
- **Jangan Pernah Percaya, Selalu Verifikasi**: Terapkan verifikasi berkelanjutan untuk semua peserta MCP.
- **Mikro-segmentasi**: Isolasi komponen MCP dengan kontrol jaringan dan identitas yang terperinci.
- **Akses Bersyarat**: Terapkan kontrol akses berbasis risiko yang beradaptasi dengan konteks dan perilaku.
- **Penilaian Risiko Berkelanjutan**: Evaluasi postur keamanan secara dinamis berdasarkan indikator ancaman saat ini.

### Implementasi AI yang Melindungi Privasi
- **Minimasi Data**: Hanya ekspos data minimum yang diperlukan untuk setiap operasi MCP.
- **Privasi Diferensial**: Terapkan teknik yang melindungi privasi untuk pemrosesan data sensitif.
- **Enkripsi Homomorfik**: Gunakan teknik enkripsi canggih untuk komputasi aman pada data terenkripsi.
- **Pembelajaran Terfederasi**: Terapkan pendekatan pembelajaran terdistribusi yang menjaga lokalitas dan privasi data.

### Respons Insiden untuk Sistem AI
- **Prosedur Insiden Spesifik AI**: Kembangkan prosedur respons insiden yang disesuaikan dengan ancaman spesifik AI dan MCP.
- **Respons Otomatis**: Terapkan penanganan dan remediasi otomatis untuk insiden keamanan AI umum.  
- **Kemampuan Forensik**: Pertahankan kesiapan forensik untuk kompromi sistem AI dan pelanggaran data.
- **Prosedur Pemulihan**: Tetapkan prosedur untuk pemulihan dari peracunan model AI, serangan injeksi prompt, dan kompromi layanan.

## Sumber Daya & Standar Implementasi

### Dokumentasi Resmi MCP
- [Spesifikasi MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Spesifikasi protokol MCP terkini
- [Praktik Keamanan Terbaik MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Panduan keamanan resmi
- [Spesifikasi Otorisasi MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Pola autentikasi dan otorisasi
- [Keamanan Transportasi MCP](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Persyaratan keamanan lapisan transportasi

### Solusi Keamanan Microsoft
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Perlindungan injeksi prompt canggih
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Penyaringan konten AI yang komprehensif
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Manajemen identitas dan akses perusahaan
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Manajemen rahasia dan kredensial yang aman
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Pemindaian keamanan rantai pasokan dan kode

### Standar & Kerangka Keamanan
- [Praktik Keamanan OAuth 2.1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Panduan keamanan OAuth terkini
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Risiko keamanan aplikasi web
- [OWASP Top 10 untuk LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Risiko keamanan spesifik AI
- [Kerangka Manajemen Risiko AI NIST](https://www.nist.gov/itl/ai-risk-management-framework) - Manajemen risiko AI yang komprehensif
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Sistem manajemen keamanan informasi

### Panduan & Tutorial Implementasi
- [Azure API Management sebagai Gateway Autentikasi MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Pola autentikasi perusahaan
- [Microsoft Entra ID dengan Server MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integrasi penyedia identitas
- [Implementasi Penyimpanan Token Aman](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Praktik terbaik manajemen token
- [Enkripsi Ujung ke Ujung untuk AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Pola enkripsi canggih

### Sumber Daya Keamanan Lanjutan
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/sdl) - Praktik pengembangan yang aman
- [Panduan Tim Merah AI](https://learn.microsoft.com/security/ai-red-team/) - Pengujian keamanan spesifik AI
- [Pemodelan Ancaman untuk Sistem AI](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Metodologi pemodelan ancaman AI
- [Rekayasa Privasi untuk AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Teknik AI yang melindungi privasi

### Kepatuhan & Tata Kelola
- [Kepatuhan GDPR untuk AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Kepatuhan privasi dalam sistem AI
- [Kerangka Tata Kelola AI](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Implementasi AI yang bertanggung jawab
- [SOC 2 untuk Layanan AI](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Kontrol keamanan untuk penyedia layanan AI
- [Kepatuhan HIPAA untuk AI](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Persyaratan kepatuhan AI di bidang kesehatan

### DevSecOps & Otomasi
- [Pipeline DevSecOps untuk AI](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Pipeline pengembangan AI yang aman
- [Pengujian Keamanan Otomatis](https://learn.microsoft.com/security/engineering/devsecops) - Validasi keamanan berkelanjutan
- [Keamanan Infrastruktur sebagai Kode](https://learn.microsoft.com/security/engineering/infrastructure-security) - Penyebaran infrastruktur yang aman
- [Keamanan Kontainer untuk AI](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - Keamanan kontainerisasi beban kerja AI

### Pemantauan & Respons Insiden  
- [Azure Monitor untuk Beban Kerja AI](https://learn.microsoft.com/azure/azure-monitor/overview) - Solusi pemantauan yang komprehensif
- [Respons Insiden Keamanan AI](https://learn.microsoft.com/security/compass/incident-response-playbooks) - Prosedur insiden spesifik AI
- [SIEM untuk Sistem AI](https://learn.microsoft.com/azure/sentinel/overview) - Manajemen informasi dan peristiwa keamanan
- [Intelijen Ancaman untuk AI](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - Sumber intelijen ancaman AI

## 🔄 Peningkatan Berkelanjutan

### Tetap Terkini dengan Standar yang Berkembang
- **Pembaruan Spesifikasi MCP**: Pantau perubahan spesifikasi resmi MCP dan pemberitahuan keamanan.
- **Intelijen Ancaman**: Berlangganan feed ancaman keamanan AI dan basis data kerentanan.  
- **Keterlibatan Komunitas**: Berpartisipasi dalam diskusi komunitas keamanan MCP dan kelompok kerja.
- **Penilaian Rutin**: Lakukan penilaian postur keamanan triwulanan dan perbarui praktik sesuai kebutuhan.

### Berkontribusi pada Keamanan MCP
- **Riset Keamanan**: Berkontribusi pada riset keamanan MCP dan program pengungkapan kerentanan.
- **Berbagi Praktik Terbaik**: Bagikan implementasi keamanan dan pelajaran yang didapat dengan komunitas.
- **Pengembangan Standar**: Berpartisipasi dalam pengembangan spesifikasi MCP dan pembuatan standar keamanan.
- **Pengembangan Alat**: Mengembangkan dan membagikan alat serta pustaka keamanan untuk ekosistem MCP

---

*Dokumen ini mencerminkan praktik terbaik keamanan MCP per 18 Agustus 2025, berdasarkan Spesifikasi MCP 2025-06-18. Praktik keamanan harus secara rutin ditinjau dan diperbarui seiring dengan perkembangan protokol dan lanskap ancaman.*

**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan layanan penerjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk memberikan hasil yang akurat, harap diperhatikan bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang berwenang. Untuk informasi yang bersifat kritis, disarankan menggunakan jasa penerjemahan manusia profesional. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.