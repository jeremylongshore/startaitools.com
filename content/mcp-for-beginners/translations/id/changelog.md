<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:34:29+00:00",
  "source_file": "changelog.md",
  "language_code": "id"
}
-->
# Catatan Perubahan: Kurikulum MCP untuk Pemula

Dokumen ini berfungsi sebagai catatan semua perubahan signifikan yang dilakukan pada kurikulum Model Context Protocol (MCP) untuk Pemula. Perubahan dicatat dalam urutan kronologis terbalik (perubahan terbaru di atas).

## 6 Oktober 2025

### Perluasan Bagian Memulai – Penggunaan Server Lanjutan & Autentikasi Sederhana

#### Penggunaan Server Lanjutan (03-GettingStarted/10-advanced)
- **Bab Baru Ditambahkan**: Panduan komprehensif tentang penggunaan server MCP tingkat lanjut, mencakup arsitektur server reguler dan tingkat rendah.
  - **Server Reguler vs. Tingkat Rendah**: Perbandingan mendetail dan contoh kode dalam Python dan TypeScript untuk kedua pendekatan.
  - **Desain Berbasis Handler**: Penjelasan tentang pengelolaan alat/sumber daya/prompts berbasis handler untuk implementasi server yang skalabel dan fleksibel.
  - **Pola Praktis**: Skenario dunia nyata di mana pola server tingkat rendah bermanfaat untuk fitur dan arsitektur tingkat lanjut.

#### Autentikasi Sederhana (03-GettingStarted/11-simple-auth)
- **Bab Baru Ditambahkan**: Panduan langkah demi langkah untuk menerapkan autentikasi sederhana di server MCP.
  - **Konsep Autentikasi**: Penjelasan yang jelas tentang autentikasi vs. otorisasi, dan pengelolaan kredensial.
  - **Implementasi Autentikasi Dasar**: Pola autentikasi berbasis middleware dalam Python (Starlette) dan TypeScript (Express), dengan contoh kode.
  - **Kemajuan ke Keamanan Lanjutan**: Panduan untuk memulai dengan autentikasi sederhana dan beralih ke OAuth 2.1 dan RBAC, dengan referensi ke modul keamanan lanjutan.

Penambahan ini memberikan panduan praktis dan langsung untuk membangun implementasi server MCP yang lebih kuat, aman, dan fleksibel, menjembatani konsep dasar dengan pola produksi tingkat lanjut.

## 29 September 2025

### Lab Integrasi Database Server MCP - Jalur Pembelajaran Praktis yang Komprehensif

#### 11-MCPServerHandsOnLabs - Kurikulum Integrasi Database Lengkap Baru
- **Jalur Pembelajaran 13-Lab Lengkap**: Menambahkan kurikulum praktis yang komprehensif untuk membangun server MCP siap produksi dengan integrasi database PostgreSQL.
  - **Implementasi Dunia Nyata**: Studi kasus analitik Zava Retail yang menunjukkan pola tingkat perusahaan.
  - **Progresi Pembelajaran Terstruktur**:
    - **Lab 00-03: Dasar-Dasar** - Pengantar, Arsitektur Inti, Keamanan & Multi-Tenancy, Pengaturan Lingkungan
    - **Lab 04-06: Membangun Server MCP** - Desain & Skema Database, Implementasi Server MCP, Pengembangan Alat  
    - **Lab 07-09: Fitur Lanjutan** - Integrasi Pencarian Semantik, Pengujian & Debugging, Integrasi VS Code
    - **Lab 10-12: Produksi & Praktik Terbaik** - Strategi Penerapan, Pemantauan & Observabilitas, Praktik Terbaik & Optimasi
  - **Teknologi Perusahaan**: Kerangka kerja FastMCP, PostgreSQL dengan pgvector, embedding Azure OpenAI, Azure Container Apps, Application Insights
  - **Fitur Lanjutan**: Keamanan Tingkat Baris (RLS), pencarian semantik, akses data multi-tenant, embedding vektor, pemantauan real-time

#### Standarisasi Terminologi - Konversi Modul ke Lab
- **Pembaruan Dokumentasi Komprehensif**: Secara sistematis memperbarui semua file README di 11-MCPServerHandsOnLabs untuk menggunakan terminologi "Lab" alih-alih "Modul".
  - **Judul Bagian**: Mengubah "Apa yang Dicakup Modul Ini" menjadi "Apa yang Dicakup Lab Ini" di semua 13 lab.
  - **Deskripsi Konten**: Mengubah "Modul ini menyediakan..." menjadi "Lab ini menyediakan..." di seluruh dokumentasi.
  - **Tujuan Pembelajaran**: Mengubah "Pada akhir modul ini..." menjadi "Pada akhir lab ini..."
  - **Tautan Navigasi**: Mengonversi semua referensi "Modul XX:" menjadi "Lab XX:" dalam referensi silang dan navigasi.
  - **Pelacakan Penyelesaian**: Mengubah "Setelah menyelesaikan modul ini..." menjadi "Setelah menyelesaikan lab ini..."
  - **Referensi Teknis yang Dipertahankan**: Mempertahankan referensi modul Python dalam file konfigurasi (misalnya, `"module": "mcp_server.main"`).

#### Peningkatan Panduan Studi (study_guide.md)
- **Peta Kurikulum Visual**: Menambahkan bagian baru "11. Database Integration Labs" dengan visualisasi struktur lab yang komprehensif.
- **Struktur Repository**: Diperbarui dari sepuluh menjadi sebelas bagian utama dengan deskripsi mendetail 11-MCPServerHandsOnLabs.
- **Panduan Jalur Pembelajaran**: Meningkatkan instruksi navigasi untuk mencakup bagian 00-11.
- **Cakupan Teknologi**: Menambahkan detail integrasi FastMCP, PostgreSQL, dan layanan Azure.
- **Hasil Pembelajaran**: Menekankan pengembangan server siap produksi, pola integrasi database, dan keamanan tingkat perusahaan.

#### Peningkatan Struktur README Utama
- **Terminologi Berbasis Lab**: Memperbarui README.md utama di 11-MCPServerHandsOnLabs untuk secara konsisten menggunakan struktur "Lab".
- **Organisasi Jalur Pembelajaran**: Progresi yang jelas dari konsep dasar hingga implementasi lanjutan hingga penerapan produksi.
- **Fokus Dunia Nyata**: Penekanan pada pembelajaran praktis dengan pola dan teknologi tingkat perusahaan.

### Peningkatan Kualitas & Konsistensi Dokumentasi
- **Penekanan Pembelajaran Praktis**: Memperkuat pendekatan berbasis lab praktis di seluruh dokumentasi.
- **Fokus Pola Perusahaan**: Menyoroti implementasi siap produksi dan pertimbangan keamanan tingkat perusahaan.
- **Integrasi Teknologi**: Cakupan komprehensif layanan Azure modern dan pola integrasi AI.
- **Progresi Pembelajaran**: Jalur yang jelas dan terstruktur dari konsep dasar hingga penerapan produksi.

## 26 September 2025

### Peningkatan Studi Kasus - Integrasi Registry MCP GitHub

#### Studi Kasus (09-CaseStudy/) - Fokus Pengembangan Ekosistem
- **README.md**: Perluasan besar dengan studi kasus komprehensif Registry MCP GitHub.
  - **Studi Kasus Registry MCP GitHub**: Studi kasus baru yang komprehensif tentang peluncuran Registry MCP GitHub pada September 2025.
    - **Analisis Masalah**: Pemeriksaan mendetail tentang tantangan penemuan dan penerapan server MCP yang terfragmentasi.
    - **Arsitektur Solusi**: Pendekatan registry terpusat GitHub dengan instalasi VS Code satu klik.
    - **Dampak Bisnis**: Peningkatan yang terukur dalam onboarding dan produktivitas pengembang.
    - **Nilai Strategis**: Fokus pada penerapan agen modular dan interoperabilitas lintas alat.
    - **Pengembangan Ekosistem**: Posisi sebagai platform dasar untuk integrasi agentic.
  - **Struktur Studi Kasus yang Ditingkatkan**: Memperbarui semua tujuh studi kasus dengan format yang konsisten dan deskripsi yang komprehensif.
    - Agen Perjalanan AI Azure: Penekanan pada orkestrasi multi-agen.
    - Integrasi Azure DevOps: Fokus pada otomatisasi alur kerja.
    - Pengambilan Dokumentasi Real-Time: Implementasi klien konsol Python.
    - Generator Rencana Studi Interaktif: Aplikasi web percakapan Chainlit.
    - Dokumentasi Dalam Editor: Integrasi VS Code dan GitHub Copilot.
    - Manajemen API Azure: Pola integrasi API tingkat perusahaan.
    - Registry MCP GitHub: Pengembangan ekosistem dan platform komunitas.
  - **Kesimpulan Komprehensif**: Bagian kesimpulan yang ditulis ulang yang menyoroti tujuh studi kasus yang mencakup berbagai dimensi implementasi MCP.
    - Integrasi Perusahaan, Orkestrasi Multi-Agen, Produktivitas Pengembang.
    - Pengembangan Ekosistem, Kategorisasi Aplikasi Pendidikan.
    - Wawasan yang ditingkatkan tentang pola arsitektur, strategi implementasi, dan praktik terbaik.
    - Penekanan pada MCP sebagai protokol yang matang dan siap produksi.

#### Pembaruan Panduan Studi (study_guide.md)
- **Peta Kurikulum Visual**: Memperbarui mindmap untuk menyertakan Registry MCP GitHub di bagian Studi Kasus.
- **Deskripsi Studi Kasus**: Ditingkatkan dari deskripsi umum menjadi rincian mendalam dari tujuh studi kasus yang komprehensif.
- **Struktur Repository**: Memperbarui bagian 10 untuk mencerminkan cakupan studi kasus yang komprehensif dengan detail implementasi spesifik.
- **Integrasi Catatan Perubahan**: Menambahkan entri 26 September 2025 yang mendokumentasikan penambahan Registry MCP GitHub dan peningkatan studi kasus.
- **Pembaruan Tanggal**: Memperbarui timestamp footer untuk mencerminkan revisi terbaru (26 September 2025).

### Peningkatan Kualitas Dokumentasi
- **Peningkatan Konsistensi**: Standarisasi format dan struktur studi kasus di semua tujuh contoh.
- **Cakupan Komprehensif**: Studi kasus kini mencakup skenario perusahaan, produktivitas pengembang, dan pengembangan ekosistem.
- **Posisi Strategis**: Fokus yang ditingkatkan pada MCP sebagai platform dasar untuk penerapan sistem agentic.
- **Integrasi Sumber Daya**: Memperbarui sumber daya tambahan untuk menyertakan tautan Registry MCP GitHub.

## 15 September 2025

### Perluasan Topik Lanjutan - Transportasi Kustom & Rekayasa Konteks

#### Transportasi Kustom MCP (05-AdvancedTopics/mcp-transport/) - Panduan Implementasi Lanjutan Baru
- **README.md**: Panduan implementasi lengkap untuk mekanisme transportasi kustom MCP.
  - **Transportasi Azure Event Grid**: Implementasi transportasi berbasis event serverless yang komprehensif.
    - Contoh dalam C#, TypeScript, dan Python dengan integrasi Azure Functions.
    - Pola arsitektur berbasis event untuk solusi MCP yang skalabel.
    - Penerima webhook dan penanganan pesan berbasis push.
  - **Transportasi Azure Event Hubs**: Implementasi transportasi streaming throughput tinggi.
    - Kemampuan streaming real-time untuk skenario latensi rendah.
    - Strategi partisi dan manajemen checkpoint.
    - Pengelompokan pesan dan optimasi kinerja.
  - **Pola Integrasi Perusahaan**: Contoh arsitektur siap produksi.
    - Pemrosesan MCP terdistribusi di beberapa Azure Functions.
    - Arsitektur transportasi hibrida yang menggabungkan beberapa jenis transportasi.
    - Strategi ketahanan pesan, keandalan, dan penanganan kesalahan.
  - **Keamanan & Pemantauan**: Integrasi Azure Key Vault dan pola observabilitas.
    - Autentikasi identitas terkelola dan akses dengan hak istimewa minimum.
    - Telemetri Application Insights dan pemantauan kinerja.
    - Pemutus sirkuit dan pola toleransi kesalahan.
  - **Kerangka Pengujian**: Strategi pengujian komprehensif untuk transportasi kustom.
    - Pengujian unit dengan test doubles dan kerangka kerja mocking.
    - Pengujian integrasi dengan Azure Test Containers.
    - Pertimbangan pengujian kinerja dan beban.

#### Rekayasa Konteks (05-AdvancedTopics/mcp-contextengineering/) - Disiplin AI yang Berkembang
- **README.md**: Eksplorasi komprehensif tentang rekayasa konteks sebagai bidang yang berkembang.
  - **Prinsip Inti**: Berbagi konteks lengkap, kesadaran keputusan tindakan, dan manajemen jendela konteks.
  - **Keselarasan Protokol MCP**: Bagaimana desain MCP mengatasi tantangan rekayasa konteks.
    - Keterbatasan jendela konteks dan strategi pemuatan progresif.
    - Penentuan relevansi dan pengambilan konteks dinamis.
    - Penanganan konteks multi-modal dan pertimbangan keamanan.
  - **Pendekatan Implementasi**: Arsitektur single-threaded vs. multi-agen.
    - Teknik pengelompokan dan prioritas konteks.
    - Strategi pemuatan progresif dan kompresi konteks.
    - Pendekatan berlapis untuk konteks dan optimasi pengambilan.
  - **Kerangka Pengukuran**: Metrik yang muncul untuk evaluasi efektivitas konteks.
    - Efisiensi input, kinerja, kualitas, dan pertimbangan pengalaman pengguna.
    - Pendekatan eksperimental untuk optimasi konteks.
    - Analisis kegagalan dan metodologi perbaikan.

#### Pembaruan Navigasi Kurikulum (README.md)
- **Struktur Modul yang Ditingkatkan**: Memperbarui tabel kurikulum untuk menyertakan topik lanjutan baru.
  - Menambahkan Rekayasa Konteks (5.14) dan Transportasi Kustom (5.15).
  - Format dan tautan navigasi yang konsisten di semua modul.
  - Deskripsi yang diperbarui untuk mencerminkan cakupan konten saat ini.

### Peningkatan Struktur Direktori
- **Standarisasi Penamaan**: Mengganti nama "mcp transport" menjadi "mcp-transport" untuk konsistensi dengan folder topik lanjutan lainnya.
- **Organisasi Konten**: Semua folder 05-AdvancedTopics kini mengikuti pola penamaan yang konsisten (mcp-[topik]).

### Peningkatan Kualitas Dokumentasi
- **Keselarasan Spesifikasi MCP**: Semua konten baru merujuk pada Spesifikasi MCP terkini 2025-06-18.
- **Contoh Multi-Bahasa**: Contoh kode komprehensif dalam C#, TypeScript, dan Python.
- **Fokus Perusahaan**: Pola siap produksi dan integrasi cloud Azure di seluruh konten.
- **Dokumentasi Visual**: Diagram Mermaid untuk visualisasi arsitektur dan alur.

## 18 Agustus 2025

### Pembaruan Dokumentasi Komprehensif - Standar MCP 2025-06-18

#### Praktik Terbaik Keamanan MCP (02-Security/) - Modernisasi Lengkap
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Penulisan ulang lengkap yang selaras dengan Spesifikasi MCP 2025-06-18.
  - **Persyaratan Wajib**: Menambahkan persyaratan eksplisit HARUS/TIDAK HARUS dari spesifikasi resmi dengan indikator visual yang jelas.
  - **12 Praktik Keamanan Inti**: Disusun ulang dari daftar 15 item menjadi domain keamanan yang komprehensif.
    - Keamanan Token & Autentikasi dengan integrasi penyedia identitas eksternal.
    - Manajemen Sesi & Keamanan Transportasi dengan persyaratan kriptografi.
    - Perlindungan Ancaman AI-Specific dengan integrasi Microsoft Prompt Shields.
    - Kontrol Akses & Izin dengan prinsip hak istimewa minimum.
    - Keamanan Konten & Pemantauan dengan integrasi Azure Content Safety.
    - Keamanan Rantai Pasokan dengan verifikasi komponen yang komprehensif.
    - Keamanan OAuth & Pencegahan Serangan Confused Deputy dengan implementasi PKCE.
    - Respons & Pemulihan Insiden dengan kemampuan otomatis.
    - Kepatuhan & Tata Kelola dengan keselarasan regulasi.
    - Kontrol Keamanan Lanjutan dengan arsitektur zero trust.
    - Integrasi Ekosistem Keamanan Microsoft dengan solusi yang komprehensif.
    - Evolusi Keamanan Berkelanjutan dengan praktik adaptif.
  - **Solusi Keamanan Microsoft**: Panduan integrasi yang ditingkatkan untuk Prompt Shields, Azure Content Safety, Entra ID, dan GitHub Advanced Security.
  - **Sumber Daya Implementasi**: Tautan sumber daya komprehensif yang dikategorikan berdasarkan Dokumentasi MCP Resmi, Solusi Keamanan Microsoft, Standar Keamanan, dan Panduan Implementasi.

#### Kontrol Keamanan Lanjutan (02-Security/) - Implementasi Perusahaan
- **MCP-SECURITY-CONTROLS-2025.md**: Perombakan lengkap dengan kerangka kerja keamanan tingkat perusahaan.
  - **9 Domain Keamanan Komprehensif**: Diperluas dari kontrol dasar menjadi kerangka kerja perusahaan yang mendetail.
    - Autentikasi & Otorisasi Lanjutan dengan integrasi Microsoft Entra ID.
    - Keamanan Token & Kontrol Anti-Passthrough dengan validasi yang komprehensif.
    - Kontrol Keamanan Sesi dengan pencegahan pembajakan.
    - Kontrol Keamanan AI-Specific dengan pencegahan injeksi prompt dan peracunan alat.
    - Pencegahan Serangan Confused Deputy dengan keamanan proxy OAuth.
    - Keamanan Eksekusi Alat dengan sandboxing dan isolasi.
    - Kontrol Keamanan Rantai Pasokan dengan verifikasi dependensi.
    - Kontrol Pemantauan & Deteksi dengan integrasi SIEM.
    - Respons & Pemulihan Insiden dengan kemampuan otomatis.
  - **Contoh Implementasi**: Menambahkan blok konfigurasi YAML yang mendetail dan contoh kode.
  - **Integrasi Solusi Microsoft**: Cakupan komprehensif layanan keamanan Azure, GitHub Advanced Security, dan manajemen identitas perusahaan.
#### Topik Lanjutan Keamanan (05-AdvancedTopics/mcp-security/) - Implementasi Siap Produksi
- **README.md**: Penulisan ulang lengkap untuk implementasi keamanan tingkat perusahaan
  - **Penyelarasan Spesifikasi Terkini**: Diperbarui sesuai Spesifikasi MCP 2025-06-18 dengan persyaratan keamanan wajib
  - **Otentikasi yang Ditingkatkan**: Integrasi Microsoft Entra ID dengan contoh lengkap .NET dan Java Spring Security
  - **Integrasi Keamanan AI**: Implementasi Microsoft Prompt Shields dan Azure Content Safety dengan contoh Python yang terperinci
  - **Mitigasi Ancaman Lanjutan**: Contoh implementasi komprehensif untuk
    - Pencegahan Serangan Confused Deputy dengan PKCE dan validasi persetujuan pengguna
    - Pencegahan Token Passthrough dengan validasi audiens dan manajemen token yang aman
    - Pencegahan Pembajakan Sesi dengan pengikatan kriptografi dan analisis perilaku
  - **Integrasi Keamanan Perusahaan**: Pemantauan Azure Application Insights, pipeline deteksi ancaman, dan keamanan rantai pasokan
  - **Daftar Periksa Implementasi**: Kontrol keamanan wajib vs. yang direkomendasikan dengan manfaat ekosistem keamanan Microsoft yang jelas

### Kualitas Dokumentasi & Penyelarasan Standar
- **Referensi Spesifikasi**: Memperbarui semua referensi ke Spesifikasi MCP terkini 2025-06-18
- **Ekosistem Keamanan Microsoft**: Panduan integrasi yang ditingkatkan di seluruh dokumentasi keamanan
- **Implementasi Praktis**: Menambahkan contoh kode terperinci dalam .NET, Java, dan Python dengan pola perusahaan
- **Organisasi Sumber Daya**: Kategorisasi komprehensif dokumentasi resmi, standar keamanan, dan panduan implementasi
- **Indikator Visual**: Penandaan yang jelas untuk persyaratan wajib vs. praktik yang direkomendasikan

#### Konsep Inti (01-CoreConcepts/) - Modernisasi Lengkap
- **Pembaruan Versi Protokol**: Diperbarui untuk merujuk Spesifikasi MCP terkini 2025-06-18 dengan penanggalan berbasis versi (format YYYY-MM-DD)
- **Penyempurnaan Arsitektur**: Deskripsi yang ditingkatkan tentang Host, Client, dan Server untuk mencerminkan pola arsitektur MCP terkini
  - Host kini didefinisikan dengan jelas sebagai aplikasi AI yang mengoordinasikan beberapa koneksi client MCP
  - Client dijelaskan sebagai konektor protokol yang mempertahankan hubungan satu-ke-satu dengan server
  - Server ditingkatkan dengan skenario penerapan lokal vs. jarak jauh
- **Restrukturisasi Primitif**: Perombakan lengkap primitif server dan client
  - Primitif Server: Resources (sumber data), Prompts (template), Tools (fungsi yang dapat dieksekusi) dengan penjelasan dan contoh terperinci
  - Primitif Client: Sampling (penyelesaian LLM), Elicitation (input pengguna), Logging (debugging/pemantauan)
  - Diperbarui dengan pola metode penemuan (`*/list`), pengambilan (`*/get`), dan eksekusi (`*/call`) terkini
- **Arsitektur Protokol**: Memperkenalkan model arsitektur dua lapis
  - Lapisan Data: Fondasi JSON-RPC 2.0 dengan manajemen siklus hidup dan primitif
  - Lapisan Transportasi: STDIO (lokal) dan HTTP yang dapat di-streaming dengan SSE (jarak jauh)
- **Kerangka Keamanan**: Prinsip keamanan komprehensif termasuk persetujuan pengguna eksplisit, perlindungan privasi data, keamanan eksekusi alat, dan keamanan lapisan transportasi
- **Pola Komunikasi**: Pesan protokol yang diperbarui untuk menunjukkan alur inisialisasi, penemuan, eksekusi, dan notifikasi
- **Contoh Kode**: Contoh multi-bahasa yang diperbarui (.NET, Java, Python, JavaScript) untuk mencerminkan pola SDK MCP terkini

#### Keamanan (02-Security/) - Perombakan Keamanan Komprehensif  
- **Penyelarasan Standar**: Penyelarasan penuh dengan persyaratan keamanan Spesifikasi MCP 2025-06-18
- **Evolusi Otentikasi**: Dokumentasi evolusi dari server OAuth khusus ke delegasi penyedia identitas eksternal (Microsoft Entra ID)
- **Analisis Ancaman AI Khusus**: Cakupan yang ditingkatkan tentang vektor serangan AI modern
  - Skenario serangan injeksi prompt yang terperinci dengan contoh dunia nyata
  - Mekanisme peracunan alat dan pola serangan "rug pull"
  - Peracunan jendela konteks dan serangan kebingungan model
- **Solusi Keamanan AI Microsoft**: Cakupan komprehensif ekosistem keamanan Microsoft
  - AI Prompt Shields dengan teknik deteksi, spotlighting, dan delimiter yang canggih
  - Pola integrasi Azure Content Safety
  - Keamanan Lanjutan GitHub untuk perlindungan rantai pasokan
- **Mitigasi Ancaman Lanjutan**: Kontrol keamanan terperinci untuk
  - Pembajakan sesi dengan skenario serangan spesifik MCP dan persyaratan ID sesi kriptografi
  - Masalah deputi bingung dalam skenario proxy MCP dengan persyaratan persetujuan eksplisit
  - Kerentanan token passthrough dengan kontrol validasi wajib
- **Keamanan Rantai Pasokan**: Cakupan rantai pasokan AI yang diperluas termasuk model fondasi, layanan embedding, penyedia konteks, dan API pihak ketiga
- **Keamanan Fondasi**: Integrasi yang ditingkatkan dengan pola keamanan perusahaan termasuk arsitektur zero trust dan ekosistem keamanan Microsoft
- **Organisasi Sumber Daya**: Mengkategorikan tautan sumber daya komprehensif berdasarkan jenis (Dokumen Resmi, Standar, Penelitian, Solusi Microsoft, Panduan Implementasi)

### Peningkatan Kualitas Dokumentasi
- **Tujuan Pembelajaran yang Terstruktur**: Tujuan pembelajaran yang ditingkatkan dengan hasil yang spesifik dan dapat ditindaklanjuti
- **Referensi Silang**: Menambahkan tautan antara topik keamanan dan konsep inti yang terkait
- **Informasi Terkini**: Memperbarui semua referensi tanggal dan tautan spesifikasi ke standar terkini
- **Panduan Implementasi**: Menambahkan panduan implementasi yang spesifik dan dapat ditindaklanjuti di seluruh kedua bagian

## 16 Juli 2025

### README dan Peningkatan Navigasi
- Mendesain ulang sepenuhnya navigasi kurikulum di README.md
- Mengganti tag `<details>` dengan format berbasis tabel yang lebih mudah diakses
- Membuat opsi tata letak alternatif di folder "alternative_layouts" baru
- Menambahkan contoh navigasi gaya kartu, tab, dan akordeon
- Memperbarui bagian struktur repositori untuk menyertakan semua file terbaru
- Meningkatkan bagian "Cara Menggunakan Kurikulum Ini" dengan rekomendasi yang jelas
- Memperbarui tautan spesifikasi MCP untuk mengarah ke URL yang benar
- Menambahkan bagian Teknik Konteks (5.14) ke struktur kurikulum

### Pembaruan Panduan Studi
- Merevisi sepenuhnya panduan studi untuk menyelaraskan dengan struktur repositori terkini
- Menambahkan bagian baru untuk Client dan Tools MCP, serta Server MCP Populer
- Memperbarui Peta Kurikulum Visual untuk mencerminkan semua topik secara akurat
- Meningkatkan deskripsi Topik Lanjutan untuk mencakup semua area khusus
- Memperbarui bagian Studi Kasus untuk mencerminkan contoh nyata
- Menambahkan changelog komprehensif ini

### Kontribusi Komunitas (06-CommunityContributions/)
- Menambahkan informasi terperinci tentang server MCP untuk pembuatan gambar
- Menambahkan bagian komprehensif tentang penggunaan Claude di VSCode
- Menambahkan instruksi pengaturan dan penggunaan client terminal Cline
- Memperbarui bagian client MCP untuk menyertakan semua opsi client populer
- Meningkatkan contoh kontribusi dengan sampel kode yang lebih akurat

### Topik Lanjutan (05-AdvancedTopics/)
- Mengorganisasi semua folder topik khusus dengan penamaan yang konsisten
- Menambahkan materi dan contoh teknik konteks
- Menambahkan dokumentasi integrasi agen Foundry
- Meningkatkan dokumentasi integrasi keamanan Entra ID

## 11 Juni 2025

### Pembuatan Awal
- Merilis versi pertama kurikulum MCP untuk Pemula
- Membuat struktur dasar untuk semua 10 bagian utama
- Mengimplementasikan Peta Kurikulum Visual untuk navigasi
- Menambahkan proyek sampel awal dalam berbagai bahasa pemrograman

### Memulai (03-GettingStarted/)
- Membuat contoh implementasi server pertama
- Menambahkan panduan pengembangan client
- Menyertakan instruksi integrasi client LLM
- Menambahkan dokumentasi integrasi VS Code
- Mengimplementasikan contoh server Server-Sent Events (SSE)

### Konsep Inti (01-CoreConcepts/)
- Menambahkan penjelasan terperinci tentang arsitektur client-server
- Membuat dokumentasi tentang komponen utama protokol
- Mendokumentasikan pola pesan dalam MCP

## 23 Mei 2025

### Struktur Repositori
- Menginisialisasi repositori dengan struktur folder dasar
- Membuat file README untuk setiap bagian utama
- Menyiapkan infrastruktur terjemahan
- Menambahkan aset gambar dan diagram

### Dokumentasi
- Membuat README.md awal dengan gambaran umum kurikulum
- Menambahkan CODE_OF_CONDUCT.md dan SECURITY.md
- Menyiapkan SUPPORT.md dengan panduan untuk mendapatkan bantuan
- Membuat struktur panduan studi awal

## 15 April 2025

### Perencanaan dan Kerangka Kerja
- Perencanaan awal untuk kurikulum MCP untuk Pemula
- Mendefinisikan tujuan pembelajaran dan audiens target
- Menguraikan struktur 10 bagian kurikulum
- Mengembangkan kerangka konseptual untuk contoh dan studi kasus
- Membuat contoh prototipe awal untuk konsep utama

---

**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan layanan penerjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk memberikan hasil yang akurat, harap diperhatikan bahwa terjemahan otomatis dapat mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang otoritatif. Untuk informasi yang bersifat kritis, disarankan menggunakan jasa penerjemahan manusia profesional. Kami tidak bertanggung jawab atas kesalahpahaman atau interpretasi yang keliru yang timbul dari penggunaan terjemahan ini.