<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T17:58:23+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "ms"
}
-->
# Amalan Terbaik Keselamatan MCP 2025

Panduan komprehensif ini menggariskan amalan keselamatan penting untuk melaksanakan sistem Model Context Protocol (MCP) berdasarkan **Spesifikasi MCP 2025-06-18** terkini dan piawaian industri semasa. Amalan ini menangani kebimbangan keselamatan tradisional serta ancaman khusus AI yang unik kepada pelaksanaan MCP.

## Keperluan Keselamatan Kritikal

### Kawalan Keselamatan Wajib (Keperluan MESTI)

1. **Pengesahan Token**: Pelayan MCP **MESTI TIDAK** menerima sebarang token yang tidak dikeluarkan secara eksplisit untuk pelayan MCP itu sendiri
2. **Pengesahan Kebenaran**: Pelayan MCP yang melaksanakan kebenaran **MESTI** mengesahkan SEMUA permintaan masuk dan **MESTI TIDAK** menggunakan sesi untuk pengesahan  
3. **Persetujuan Pengguna**: Pelayan proksi MCP yang menggunakan ID klien statik **MESTI** mendapatkan persetujuan pengguna secara eksplisit untuk setiap klien yang didaftarkan secara dinamik
4. **ID Sesi Selamat**: Pelayan MCP **MESTI** menggunakan ID sesi yang selamat secara kriptografi, tidak deterministik yang dijana dengan penjana nombor rawak yang selamat

## Amalan Keselamatan Teras

### 1. Pengesahan & Sanitasi Input
- **Pengesahan Input Komprehensif**: Sahkan dan sanitasi semua input untuk mencegah serangan suntikan, masalah timbal balik, dan kerentanan suntikan prompt
- **Penguatkuasaan Skema Parameter**: Laksanakan pengesahan skema JSON yang ketat untuk semua parameter alat dan input API
- **Penapisan Kandungan**: Gunakan Microsoft Prompt Shields dan Azure Content Safety untuk menapis kandungan berniat jahat dalam prompt dan respons
- **Sanitasi Output**: Sahkan dan sanitasi semua output model sebelum dipersembahkan kepada pengguna atau sistem hiliran

### 2. Kecemerlangan Pengesahan & Kebenaran  
- **Penyedia Identiti Luaran**: Delegasikan pengesahan kepada penyedia identiti yang mapan (Microsoft Entra ID, penyedia OAuth 2.1) daripada melaksanakan pengesahan tersuai
- **Kebenaran Halus**: Laksanakan kebenaran granular, khusus alat mengikut prinsip keistimewaan minimum
- **Pengurusan Kitaran Hayat Token**: Gunakan token akses jangka pendek dengan putaran selamat dan pengesahan audiens yang betul
- **Pengesahan Pelbagai Faktor**: Wajibkan MFA untuk semua akses pentadbiran dan operasi sensitif

### 3. Protokol Komunikasi Selamat
- **Keselamatan Lapisan Pengangkutan**: Gunakan HTTPS/TLS 1.3 untuk semua komunikasi MCP dengan pengesahan sijil yang betul
- **Penyulitan Hujung-ke-Hujung**: Laksanakan lapisan penyulitan tambahan untuk data yang sangat sensitif semasa transit dan semasa disimpan
- **Pengurusan Sijil**: Kekalkan pengurusan kitaran hayat sijil yang betul dengan proses pembaharuan automatik
- **Penguatkuasaan Versi Protokol**: Gunakan versi protokol MCP semasa (2025-06-18) dengan rundingan versi yang betul

### 4. Had Kadar Lanjutan & Perlindungan Sumber
- **Had Kadar Berlapis**: Laksanakan had kadar pada tahap pengguna, sesi, alat, dan sumber untuk mencegah penyalahgunaan
- **Had Kadar Adaptif**: Gunakan had kadar berdasarkan pembelajaran mesin yang menyesuaikan diri dengan pola penggunaan dan indikator ancaman
- **Pengurusan Kuota Sumber**: Tetapkan had yang sesuai untuk sumber pengiraan, penggunaan memori, dan masa pelaksanaan
- **Perlindungan DDoS**: Gunakan perlindungan DDoS yang komprehensif dan sistem analisis trafik

### 5. Pembalakan & Pemantauan Komprehensif
- **Pembalakan Audit Berstruktur**: Laksanakan log terperinci yang boleh dicari untuk semua operasi MCP, pelaksanaan alat, dan acara keselamatan
- **Pemantauan Keselamatan Masa Nyata**: Gunakan sistem SIEM dengan pengesanan anomali berkuasa AI untuk beban kerja MCP
- **Pembalakan Patuh Privasi**: Log acara keselamatan sambil menghormati keperluan dan peraturan privasi data
- **Integrasi Respons Insiden**: Sambungkan sistem pembalakan kepada aliran kerja respons insiden automatik

### 6. Amalan Penyimpanan Selamat yang Dipertingkatkan
- **Modul Keselamatan Perkakasan**: Gunakan penyimpanan kunci yang disokong HSM (Azure Key Vault, AWS CloudHSM) untuk operasi kriptografi kritikal
- **Pengurusan Kunci Penyulitan**: Laksanakan putaran kunci yang betul, pengasingan, dan kawalan akses untuk kunci penyulitan
- **Pengurusan Rahsia**: Simpan semua kunci API, token, dan kelayakan dalam sistem pengurusan rahsia khusus
- **Pengelasan Data**: Klasifikasikan data berdasarkan tahap sensitiviti dan gunakan langkah perlindungan yang sesuai

### 7. Pengurusan Token Lanjutan
- **Pencegahan Passthrough Token**: Larang secara eksplisit pola passthrough token yang memintas kawalan keselamatan
- **Pengesahan Audiens**: Sentiasa sahkan tuntutan audiens token sepadan dengan identiti pelayan MCP yang dimaksudkan
- **Kebenaran Berdasarkan Tuntutan**: Laksanakan kebenaran granular berdasarkan tuntutan token dan atribut pengguna
- **Pengikatan Token**: Ikat token kepada sesi, pengguna, atau peranti tertentu jika sesuai

### 8. Pengurusan Sesi Selamat
- **ID Sesi Kriptografi**: Jana ID sesi menggunakan penjana nombor rawak yang selamat secara kriptografi (bukan urutan yang boleh diramal)
- **Pengikatan Khusus Pengguna**: Ikat ID sesi kepada maklumat khusus pengguna menggunakan format selamat seperti `<user_id>:<session_id>`
- **Kawalan Kitaran Hayat Sesi**: Laksanakan mekanisme tamat tempoh, putaran, dan pembatalan sesi yang betul
- **Header Keselamatan Sesi**: Gunakan header HTTP keselamatan yang sesuai untuk perlindungan sesi

### 9. Kawalan Keselamatan Khusus AI
- **Pertahanan Suntikan Prompt**: Gunakan Microsoft Prompt Shields dengan teknik spotlighting, delimiters, dan datamarking
- **Pencegahan Keracunan Alat**: Sahkan metadata alat, pantau perubahan dinamik, dan sahkan integriti alat
- **Pengesahan Output Model**: Imbas output model untuk potensi kebocoran data, kandungan berbahaya, atau pelanggaran polisi keselamatan
- **Perlindungan Tingkap Konteks**: Laksanakan kawalan untuk mencegah keracunan tingkap konteks dan serangan manipulasi

### 10. Keselamatan Pelaksanaan Alat
- **Sandboxing Pelaksanaan**: Jalankan pelaksanaan alat dalam persekitaran yang diasingkan, berasaskan kontena dengan had sumber
- **Pemisahan Keistimewaan**: Laksanakan alat dengan keistimewaan minimum yang diperlukan dan akaun perkhidmatan yang berasingan
- **Pengasingan Rangkaian**: Laksanakan segmentasi rangkaian untuk persekitaran pelaksanaan alat
- **Pemantauan Pelaksanaan**: Pantau pelaksanaan alat untuk tingkah laku anomali, penggunaan sumber, dan pelanggaran keselamatan

### 11. Pengesahan Keselamatan Berterusan
- **Ujian Keselamatan Automatik**: Integrasikan ujian keselamatan ke dalam saluran CI/CD dengan alat seperti GitHub Advanced Security
- **Pengurusan Kerentanan**: Imbas secara berkala semua kebergantungan, termasuk model AI dan perkhidmatan luaran
- **Ujian Penembusan**: Lakukan penilaian keselamatan secara berkala yang secara khusus menyasarkan pelaksanaan MCP
- **Semakan Kod Keselamatan**: Laksanakan semakan keselamatan wajib untuk semua perubahan kod berkaitan MCP

### 12. Keselamatan Rantaian Bekalan untuk AI
- **Pengesahan Komponen**: Sahkan asal usul, integriti, dan keselamatan semua komponen AI (model, embeddings, API)
- **Pengurusan Kebergantungan**: Kekalkan inventori semasa semua perisian dan kebergantungan AI dengan penjejakan kerentanan
- **Repositori Dipercayai**: Gunakan sumber yang disahkan dan dipercayai untuk semua model AI, perpustakaan, dan alat
- **Pemantauan Rantaian Bekalan**: Pantau secara berterusan untuk kompromi dalam penyedia perkhidmatan AI dan repositori model

## Corak Keselamatan Lanjutan

### Seni Bina Zero Trust untuk MCP
- **Jangan Percaya, Sentiasa Sahkan**: Laksanakan pengesahan berterusan untuk semua peserta MCP
- **Mikro-segmentasi**: Asingkan komponen MCP dengan kawalan rangkaian dan identiti granular
- **Akses Bersyarat**: Laksanakan kawalan akses berdasarkan risiko yang menyesuaikan diri dengan konteks dan tingkah laku
- **Penilaian Risiko Berterusan**: Menilai postur keselamatan secara dinamik berdasarkan indikator ancaman semasa

### Pelaksanaan AI yang Memelihara Privasi
- **Pengurangan Data**: Hanya dedahkan data minimum yang diperlukan untuk setiap operasi MCP
- **Privasi Berbeza**: Laksanakan teknik pemeliharaan privasi untuk pemprosesan data sensitif
- **Penyulitan Homomorfik**: Gunakan teknik penyulitan lanjutan untuk pengiraan selamat pada data yang disulitkan
- **Pembelajaran Teragih**: Laksanakan pendekatan pembelajaran teragih yang memelihara lokaliti dan privasi data

### Respons Insiden untuk Sistem AI
- **Prosedur Insiden Khusus AI**: Bangunkan prosedur respons insiden yang disesuaikan untuk ancaman khusus AI dan MCP
- **Respons Automatik**: Laksanakan penahanan dan pemulihan automatik untuk insiden keselamatan AI yang biasa  
- **Keupayaan Forensik**: Kekalkan kesediaan forensik untuk kompromi sistem AI dan pelanggaran data
- **Prosedur Pemulihan**: Tetapkan prosedur untuk pemulihan daripada keracunan model AI, serangan suntikan prompt, dan kompromi perkhidmatan

## Sumber Pelaksanaan & Piawaian

### Dokumentasi Rasmi MCP
- [Spesifikasi MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Spesifikasi protokol MCP semasa
- [Amalan Keselamatan MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Panduan keselamatan rasmi
- [Spesifikasi Kebenaran MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Pola pengesahan dan kebenaran
- [Keselamatan Pengangkutan MCP](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Keperluan keselamatan lapisan pengangkutan

### Penyelesaian Keselamatan Microsoft
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Perlindungan suntikan prompt lanjutan
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Penapisan kandungan AI yang komprehensif
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Pengurusan identiti dan akses perusahaan
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Pengurusan rahsia dan kelayakan yang selamat
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Imbasan keselamatan rantaian bekalan dan kod

### Piawaian & Rangka Kerja Keselamatan
- [Amalan Terbaik Keselamatan OAuth 2.1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Panduan keselamatan OAuth semasa
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Risiko keselamatan aplikasi web
- [OWASP Top 10 untuk LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Risiko keselamatan khusus AI
- [Rangka Kerja Pengurusan Risiko AI NIST](https://www.nist.gov/itl/ai-risk-management-framework) - Pengurusan risiko AI yang komprehensif
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Sistem pengurusan keselamatan maklumat

### Panduan & Tutorial Pelaksanaan
- [Pengurusan API Azure sebagai Gerbang Auth MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Pola pengesahan perusahaan
- [Microsoft Entra ID dengan Pelayan MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integrasi penyedia identiti
- [Pelaksanaan Penyimpanan Token Selamat](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Amalan terbaik pengurusan token
- [Penyulitan Hujung-ke-Hujung untuk AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Pola penyulitan lanjutan

### Sumber Keselamatan Lanjutan
- [Kitaran Hayat Pembangunan Keselamatan Microsoft](https://www.microsoft.com/sdl) - Amalan pembangunan yang selamat
- [Panduan Pasukan Merah AI](https://learn.microsoft.com/security/ai-red-team/) - Ujian keselamatan khusus AI
- [Pemodelan Ancaman untuk Sistem AI](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Metodologi pemodelan ancaman AI
- [Kejuruteraan Privasi untuk AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Teknik AI yang memelihara privasi

### Pematuhan & Tadbir Urus
- [Pematuhan GDPR untuk AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Pematuhan privasi dalam sistem AI
- [Rangka Kerja Tadbir Urus AI](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Pelaksanaan AI yang bertanggungjawab
- [SOC 2 untuk Perkhidmatan AI](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Kawalan keselamatan untuk penyedia perkhidmatan AI
- [Pematuhan HIPAA untuk AI](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Keperluan pematuhan AI dalam penjagaan kesihatan

### DevSecOps & Automasi
- [Saluran DevSecOps untuk AI](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Saluran pembangunan AI yang selamat
- [Ujian Keselamatan Automatik](https://learn.microsoft.com/security/engineering/devsecops) - Pengesahan keselamatan berterusan
- [Keselamatan Infrastruktur sebagai Kod](https://learn.microsoft.com/security/engineering/infrastructure-security) - Pelaksanaan infrastruktur yang selamat
- [Keselamatan Kontena untuk AI](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - Keselamatan kontena beban kerja AI

### Pemantauan & Respons Insiden  
- [Azure Monitor untuk Beban Kerja AI](https://learn.microsoft.com/azure/azure-monitor/overview) - Penyelesaian pemantauan yang komprehensif
- [Respons Insiden Keselamatan AI](https://learn.microsoft.com/security/compass/incident-response-playbooks) - Prosedur insiden khusus AI
- [SIEM untuk Sistem AI](https://learn.microsoft.com/azure/sentinel/overview) - Pengurusan maklumat dan acara keselamatan
- [Perisikan Ancaman untuk AI](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - Sumber perisikan ancaman AI

## 🔄 Penambahbaikan Berterusan

### Kekal Terkini dengan Piawaian yang Berkembang
- **Kemas Kini Spesifikasi MCP**: Pantau perubahan spesifikasi MCP rasmi dan nasihat keselamatan
- **Perisikan Ancaman**: Langgan suapan ancaman keselamatan AI dan pangkalan data kerentanan  
- **Penglibatan Komuniti**: Sertai perbincangan komuniti keselamatan MCP dan kumpulan kerja
- **Penilaian Berkala**: Lakukan penilaian postur keselamatan suku tahunan dan kemas kini amalan mengikut keperluan

### Menyumbang kepada Keselamatan MCP
- **Penyelidikan Keselamatan**: Sumbang kepada penyelidikan keselamatan MCP dan program pendedahan kerentanan
- **Perkongsian Amalan Terbaik**: Kongsi pelaksanaan keselamatan dan pengajaran yang diperoleh dengan komuniti
- **Pembangunan Piawaian**: Sertai pembangunan spesifikasi MCP dan penciptaan piawaian keselamatan
- **Pembangunan Alat**: Membangunkan dan berkongsi alat keselamatan serta perpustakaan untuk ekosistem MCP

---

*Dokumen ini mencerminkan amalan terbaik keselamatan MCP pada 18 Ogos 2025, berdasarkan Spesifikasi MCP 2025-06-18. Amalan keselamatan harus dikaji dan dikemas kini secara berkala selaras dengan evolusi protokol dan landskap ancaman.*

**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk memastikan ketepatan, sila ambil perhatian bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang berwibawa. Untuk maklumat penting, terjemahan manusia profesional adalah disyorkan. Kami tidak bertanggungjawab atas sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.