<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T17:55:55+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "ms"
}
-->
# Amalan Terbaik Keselamatan MCP - Kemas Kini Ogos 2025

> **Penting**: Dokumen ini mencerminkan keperluan keselamatan terkini [Spesifikasi MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) dan [Amalan Terbaik Keselamatan MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) rasmi. Sentiasa rujuk spesifikasi semasa untuk panduan terkini.

## Amalan Keselamatan Penting untuk Pelaksanaan MCP

Model Context Protocol memperkenalkan cabaran keselamatan unik yang melangkaui keselamatan perisian tradisional. Amalan ini menangani keperluan keselamatan asas dan ancaman khusus MCP termasuk suntikan prompt, pencemaran alat, pengambilalihan sesi, masalah timbal balik yang keliru, dan kerentanan token passthrough.

### **Keperluan Keselamatan WAJIB**

**Keperluan Kritikal daripada Spesifikasi MCP:**

> **MUST NOT**: Pelayan MCP **MUST NOT** menerima sebarang token yang tidak dikeluarkan secara eksplisit untuk pelayan MCP  
> 
> **MUST**: Pelayan MCP yang melaksanakan kebenaran **MUST** mengesahkan SEMUA permintaan masuk  
>  
> **MUST NOT**: Pelayan MCP **MUST NOT** menggunakan sesi untuk pengesahan  
>
> **MUST**: Pelayan proksi MCP yang menggunakan ID pelanggan statik **MUST** mendapatkan persetujuan pengguna untuk setiap pelanggan yang didaftarkan secara dinamik  

---

## 1. **Keselamatan Token & Pengesahan**

**Kawalan Pengesahan & Kebenaran:**
   - **Semakan Kebenaran yang Ketat**: Lakukan audit menyeluruh terhadap logik kebenaran pelayan MCP untuk memastikan hanya pengguna dan pelanggan yang dimaksudkan boleh mengakses sumber
   - **Integrasi Penyedia Identiti Luaran**: Gunakan penyedia identiti yang mapan seperti Microsoft Entra ID daripada melaksanakan pengesahan tersuai
   - **Pengesahan Penonton Token**: Sentiasa sahkan bahawa token dikeluarkan secara eksplisit untuk pelayan MCP anda - jangan terima token hulu
   - **Kitaran Hayat Token yang Betul**: Laksanakan putaran token yang selamat, dasar tamat tempoh, dan cegah serangan ulangan token

**Penyimpanan Token yang Dilindungi:**
   - Gunakan Azure Key Vault atau stor kredensial selamat yang serupa untuk semua rahsia
   - Laksanakan penyulitan untuk token semasa rehat dan dalam transit
   - Putaran kredensial secara berkala dan pemantauan untuk akses tanpa kebenaran

## 2. **Pengurusan Sesi & Keselamatan Pengangkutan**

**Amalan Sesi Selamat:**
   - **ID Sesi Kriptografi Selamat**: Gunakan ID sesi yang selamat dan tidak deterministik yang dijana dengan penjana nombor rawak yang selamat
   - **Pengikatan Khusus Pengguna**: Ikat ID sesi kepada identiti pengguna menggunakan format seperti `<user_id>:<session_id>` untuk mencegah penyalahgunaan sesi antara pengguna
   - **Pengurusan Kitaran Hayat Sesi**: Laksanakan tamat tempoh, putaran, dan pembatalan yang betul untuk mengehadkan tingkap kerentanan
   - **Penguatkuasaan HTTPS/TLS**: HTTPS wajib untuk semua komunikasi bagi mencegah pemintasan ID sesi

**Keselamatan Lapisan Pengangkutan:**
   - Konfigurasikan TLS 1.3 di mana mungkin dengan pengurusan sijil yang betul
   - Laksanakan pinning sijil untuk sambungan kritikal
   - Putaran sijil secara berkala dan pengesahan kesahihan

## 3. **Perlindungan Ancaman Khusus AI** 🤖

**Pertahanan Suntikan Prompt:**
   - **Microsoft Prompt Shields**: Gunakan AI Prompt Shields untuk pengesanan dan penapisan arahan berniat jahat yang canggih
   - **Pembersihan Input**: Sahkan dan bersihkan semua input untuk mencegah serangan suntikan dan masalah timbal balik yang keliru
   - **Sempadan Kandungan**: Gunakan sistem pemisah dan penandaan data untuk membezakan antara arahan yang dipercayai dan kandungan luaran

**Pencegahan Pencemaran Alat:**
   - **Pengesahan Metadata Alat**: Laksanakan pemeriksaan integriti untuk definisi alat dan pantau perubahan yang tidak dijangka
   - **Pemantauan Alat Dinamik**: Pantau tingkah laku masa jalan dan sediakan amaran untuk corak pelaksanaan yang tidak dijangka
   - **Aliran Kerja Kelulusan**: Memerlukan kelulusan pengguna eksplisit untuk pengubahsuaian alat dan perubahan keupayaan

## 4. **Kawalan Akses & Kebenaran**

**Prinsip Keistimewaan Minimum:**
   - Berikan pelayan MCP hanya keistimewaan minimum yang diperlukan untuk fungsi yang dimaksudkan
   - Laksanakan kawalan akses berasaskan peranan (RBAC) dengan kebenaran yang terperinci
   - Semakan kebenaran secara berkala dan pemantauan berterusan untuk peningkatan keistimewaan

**Kawalan Kebenaran Masa Jalan:**
   - Terapkan had sumber untuk mencegah serangan keletihan sumber
   - Gunakan pengasingan kontena untuk persekitaran pelaksanaan alat  
   - Laksanakan akses tepat pada masanya untuk fungsi pentadbiran

## 5. **Keselamatan Kandungan & Pemantauan**

**Pelaksanaan Keselamatan Kandungan:**
   - **Integrasi Keselamatan Kandungan Azure**: Gunakan Azure Content Safety untuk mengesan kandungan berbahaya, percubaan jailbreak, dan pelanggaran dasar
   - **Analisis Tingkah Laku**: Laksanakan pemantauan tingkah laku masa jalan untuk mengesan anomali dalam pelayan MCP dan pelaksanaan alat
   - **Pembalakan Komprehensif**: Log semua percubaan pengesahan, panggilan alat, dan acara keselamatan dengan storan yang selamat dan kalis gangguan

**Pemantauan Berterusan:**
   - Amaran masa nyata untuk corak mencurigakan dan percubaan akses tanpa kebenaran  
   - Integrasi dengan sistem SIEM untuk pengurusan acara keselamatan berpusat
   - Audit keselamatan secara berkala dan ujian penembusan pelaksanaan MCP

## 6. **Keselamatan Rantaian Bekalan**

**Pengesahan Komponen:**
   - **Imbasan Kebergantungan**: Gunakan imbasan kerentanan automatik untuk semua kebergantungan perisian dan komponen AI
   - **Pengesahan Asal**: Sahkan asal, pelesenan, dan integriti model, sumber data, dan perkhidmatan luaran
   - **Pakej Bertandatangan**: Gunakan pakej yang ditandatangani secara kriptografi dan sahkan tandatangan sebelum pelaksanaan

**Saluran Pembangunan Selamat:**
   - **Keselamatan Lanjutan GitHub**: Laksanakan imbasan rahsia, analisis kebergantungan, dan analisis statik CodeQL
   - **Keselamatan CI/CD**: Integrasikan pengesahan keselamatan sepanjang saluran pelaksanaan automatik
   - **Integriti Artifak**: Laksanakan pengesahan kriptografi untuk artifak dan konfigurasi yang dilaksanakan

## 7. **Keselamatan OAuth & Pencegahan Timbal Balik Keliru**

**Pelaksanaan OAuth 2.1:**
   - **Pelaksanaan PKCE**: Gunakan Proof Key for Code Exchange (PKCE) untuk semua permintaan kebenaran
   - **Persetujuan Eksplisit**: Dapatkan persetujuan pengguna untuk setiap pelanggan yang didaftarkan secara dinamik untuk mencegah serangan timbal balik keliru
   - **Pengesahan URI Pengalihan**: Laksanakan pengesahan ketat URI pengalihan dan pengecam pelanggan

**Keselamatan Proksi:**
   - Cegah pintasan kebenaran melalui eksploitasi ID pelanggan statik
   - Laksanakan aliran kerja persetujuan yang betul untuk akses API pihak ketiga
   - Pantau pencurian kod kebenaran dan akses API tanpa kebenaran

## 8. **Tindak Balas & Pemulihan Insiden**

**Keupayaan Tindak Balas Pantas:**
   - **Tindak Balas Automatik**: Laksanakan sistem automatik untuk putaran kredensial dan pembendungan ancaman
   - **Prosedur Rollback**: Keupayaan untuk segera kembali kepada konfigurasi dan komponen yang diketahui baik
   - **Keupayaan Forensik**: Jejak audit terperinci dan pembalakan untuk penyiasatan insiden

**Komunikasi & Koordinasi:**
   - Prosedur eskalasi yang jelas untuk insiden keselamatan
   - Integrasi dengan pasukan tindak balas insiden organisasi
   - Simulasi insiden keselamatan dan latihan meja secara berkala

## 9. **Pematuhan & Tadbir Urus**

**Pematuhan Peraturan:**
   - Pastikan pelaksanaan MCP memenuhi keperluan industri tertentu (GDPR, HIPAA, SOC 2)
   - Laksanakan kawalan klasifikasi data dan privasi untuk pemprosesan data AI
   - Kekalkan dokumentasi komprehensif untuk audit pematuhan

**Pengurusan Perubahan:**
   - Proses semakan keselamatan formal untuk semua pengubahsuaian sistem MCP
   - Kawalan versi dan aliran kerja kelulusan untuk perubahan konfigurasi
   - Penilaian pematuhan secara berkala dan analisis jurang

## 10. **Kawalan Keselamatan Lanjutan**

**Seni Bina Zero Trust:**
   - **Jangan Percaya, Sentiasa Sahkan**: Pengesahan berterusan pengguna, peranti, dan sambungan
   - **Mikro-segmen**: Kawalan rangkaian granular yang mengasingkan komponen MCP individu
   - **Akses Bersyarat**: Kawalan akses berdasarkan risiko yang menyesuaikan diri dengan konteks dan tingkah laku semasa

**Perlindungan Aplikasi Masa Jalan:**
   - **Perlindungan Aplikasi Masa Jalan (RASP)**: Gunakan teknik RASP untuk pengesanan ancaman masa nyata
   - **Pemantauan Prestasi Aplikasi**: Pantau anomali prestasi yang mungkin menunjukkan serangan
   - **Dasar Keselamatan Dinamik**: Laksanakan dasar keselamatan yang menyesuaikan diri berdasarkan landskap ancaman semasa

## 11. **Integrasi Ekosistem Keselamatan Microsoft**

**Keselamatan Komprehensif Microsoft:**
   - **Microsoft Defender for Cloud**: Pengurusan postur keselamatan awan untuk beban kerja MCP
   - **Azure Sentinel**: Keupayaan SIEM dan SOAR asli awan untuk pengesanan ancaman lanjutan
   - **Microsoft Purview**: Tadbir urus data dan pematuhan untuk aliran kerja AI dan sumber data

**Pengurusan Identiti & Akses:**
   - **Microsoft Entra ID**: Pengurusan identiti perusahaan dengan dasar akses bersyarat
   - **Pengurusan Identiti Keistimewaan (PIM)**: Akses tepat pada masanya dan aliran kerja kelulusan untuk fungsi pentadbiran
   - **Perlindungan Identiti**: Akses bersyarat berdasarkan risiko dan tindak balas ancaman automatik

## 12. **Evolusi Keselamatan Berterusan**

**Sentiasa Terkini:**
   - **Pemantauan Spesifikasi**: Semakan berkala kemas kini spesifikasi MCP dan perubahan panduan keselamatan
   - **Perisikan Ancaman**: Integrasi suapan ancaman khusus AI dan petunjuk kompromi
   - **Penglibatan Komuniti Keselamatan**: Penyertaan aktif dalam komuniti keselamatan MCP dan program pendedahan kerentanan

**Keselamatan Adaptif:**
   - **Keselamatan Pembelajaran Mesin**: Gunakan pengesanan anomali berasaskan ML untuk mengenal pasti corak serangan baru
   - **Analitik Keselamatan Prediktif**: Laksanakan model prediktif untuk pengenalpastian ancaman secara proaktif
   - **Automasi Keselamatan**: Kemas kini dasar keselamatan automatik berdasarkan perisikan ancaman dan perubahan spesifikasi

---

## **Sumber Keselamatan Kritikal**

### **Dokumentasi MCP Rasmi**
- [Spesifikasi MCP (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)
- [Amalan Terbaik Keselamatan MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)
- [Spesifikasi Kebenaran MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)

### **Penyelesaian Keselamatan Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Keselamatan Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Keselamatan Lanjutan GitHub](https://github.com/security/advanced-security)

### **Standard Keselamatan**
- [Amalan Terbaik Keselamatan OAuth 2.0 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [OWASP Top 10 untuk Model Bahasa Besar](https://genai.owasp.org/)
- [Kerangka Pengurusan Risiko AI NIST](https://www.nist.gov/itl/ai-risk-management-framework)

### **Panduan Pelaksanaan**
- [Gerbang Pengesahan MCP Pengurusan API Azure](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Microsoft Entra ID dengan Pelayan MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)

---

> **Notis Keselamatan**: Amalan keselamatan MCP berkembang dengan pantas. Sentiasa sahkan terhadap [spesifikasi MCP](https://spec.modelcontextprotocol.io/) semasa dan [dokumentasi keselamatan rasmi](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) sebelum pelaksanaan.

**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk memastikan ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang berwibawa. Untuk maklumat penting, terjemahan manusia profesional adalah disyorkan. Kami tidak bertanggungjawab atas sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.