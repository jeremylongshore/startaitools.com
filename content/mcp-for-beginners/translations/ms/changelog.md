<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:37:28+00:00",
  "source_file": "changelog.md",
  "language_code": "ms"
}
-->
# Log Perubahan: Kurikulum MCP untuk Pemula

Dokumen ini berfungsi sebagai rekod semua perubahan penting yang dibuat pada kurikulum Model Context Protocol (MCP) untuk Pemula. Perubahan didokumentasikan dalam urutan kronologi terbalik (perubahan terbaru di atas).

## 6 Oktober 2025

### Pengembangan Bahagian Memulakan – Penggunaan Pelayan Lanjutan & Pengesahan Mudah

#### Penggunaan Pelayan Lanjutan (03-GettingStarted/10-advanced)
- **Bab Baru Ditambah**: Memperkenalkan panduan komprehensif tentang penggunaan pelayan MCP lanjutan, merangkumi seni bina pelayan biasa dan tahap rendah.
  - **Pelayan Biasa vs. Tahap Rendah**: Perbandingan terperinci dan contoh kod dalam Python dan TypeScript untuk kedua-dua pendekatan.
  - **Reka Bentuk Berasaskan Pengendali**: Penjelasan tentang pengurusan alat/sumber/prompt berasaskan pengendali untuk pelaksanaan pelayan yang boleh diskalakan dan fleksibel.
  - **Corak Praktikal**: Senario dunia nyata di mana corak pelayan tahap rendah bermanfaat untuk ciri dan seni bina lanjutan.

#### Pengesahan Mudah (03-GettingStarted/11-simple-auth)
- **Bab Baru Ditambah**: Panduan langkah demi langkah untuk melaksanakan pengesahan mudah dalam pelayan MCP.
  - **Konsep Pengesahan**: Penjelasan jelas tentang pengesahan vs. kebenaran, dan pengendalian kelayakan.
  - **Pelaksanaan Pengesahan Asas**: Corak pengesahan berasaskan middleware dalam Python (Starlette) dan TypeScript (Express), dengan contoh kod.
  - **Perkembangan ke Keselamatan Lanjutan**: Panduan untuk bermula dengan pengesahan mudah dan maju ke OAuth 2.1 dan RBAC, dengan rujukan kepada modul keselamatan lanjutan.

Penambahan ini menyediakan panduan praktikal dan langsung untuk membina pelaksanaan pelayan MCP yang lebih kukuh, selamat, dan fleksibel, menghubungkan konsep asas dengan corak pengeluaran lanjutan.

## 29 September 2025

### Makmal Integrasi Pangkalan Data Pelayan MCP - Laluan Pembelajaran Praktikal Komprehensif

#### 11-MCPServerHandsOnLabs - Kurikulum Integrasi Pangkalan Data Lengkap Baru
- **Laluan Pembelajaran 13-Makmal Lengkap**: Menambah kurikulum praktikal komprehensif untuk membina pelayan MCP bersedia pengeluaran dengan integrasi pangkalan data PostgreSQL.
  - **Pelaksanaan Dunia Nyata**: Kes penggunaan analitik Zava Retail yang menunjukkan corak tahap perusahaan.
  - **Perkembangan Pembelajaran Berstruktur**:
    - **Makmal 00-03: Asas** - Pengenalan, Seni Bina Teras, Keselamatan & Multi-Tenancy, Persediaan Persekitaran
    - **Makmal 04-06: Membina Pelayan MCP** - Reka Bentuk & Skema Pangkalan Data, Pelaksanaan Pelayan MCP, Pembangunan Alat  
    - **Makmal 07-09: Ciri Lanjutan** - Integrasi Carian Semantik, Ujian & Debugging, Integrasi VS Code
    - **Makmal 10-12: Pengeluaran & Amalan Terbaik** - Strategi Penghantaran, Pemantauan & Pemerhatian, Amalan Terbaik & Pengoptimuman
  - **Teknologi Perusahaan**: Rangka kerja FastMCP, PostgreSQL dengan pgvector, Azure OpenAI embeddings, Azure Container Apps, Application Insights
  - **Ciri Lanjutan**: Keselamatan Tahap Baris (RLS), carian semantik, akses data multi-penyewa, embeddings vektor, pemantauan masa nyata

#### Penyeragaman Terminologi - Penukaran Modul kepada Makmal
- **Kemas Kini Dokumentasi Komprehensif**: Secara sistematik mengemas kini semua fail README dalam 11-MCPServerHandsOnLabs untuk menggunakan terminologi "Makmal" dan bukannya "Modul".
  - **Tajuk Bahagian**: Mengemas kini "Apa yang Diliputi Modul Ini" kepada "Apa yang Diliputi Makmal Ini" di semua 13 makmal.
  - **Penerangan Kandungan**: Menukar "Modul ini menyediakan..." kepada "Makmal ini menyediakan..." di seluruh dokumentasi.
  - **Objektif Pembelajaran**: Mengemas kini "Menjelang akhir modul ini..." kepada "Menjelang akhir makmal ini..."
  - **Pautan Navigasi**: Menukar semua rujukan "Modul XX:" kepada "Makmal XX:" dalam rujukan silang dan navigasi.
  - **Penjejakan Penyelesaian**: Mengemas kini "Selepas menyelesaikan modul ini..." kepada "Selepas menyelesaikan makmal ini..."
  - **Rujukan Teknikal Dikekalkan**: Mengekalkan rujukan modul Python dalam fail konfigurasi (contoh: `"module": "mcp_server.main"`).

#### Penambahbaikan Panduan Kajian (study_guide.md)
- **Peta Kurikulum Visual**: Menambah bahagian baru "11. Makmal Integrasi Pangkalan Data" dengan visualisasi struktur makmal yang komprehensif.
- **Struktur Repositori**: Dikemas kini daripada sepuluh kepada sebelas bahagian utama dengan penerangan terperinci 11-MCPServerHandsOnLabs.
- **Panduan Laluan Pembelajaran**: Meningkatkan arahan navigasi untuk merangkumi bahagian 00-11.
- **Liputan Teknologi**: Menambah butiran integrasi FastMCP, PostgreSQL, dan perkhidmatan Azure.
- **Hasil Pembelajaran**: Menekankan pembangunan pelayan bersedia pengeluaran, corak integrasi pangkalan data, dan keselamatan perusahaan.

#### Penambahbaikan Struktur README Utama
- **Terminologi Berasaskan Makmal**: Mengemas kini README.md utama dalam 11-MCPServerHandsOnLabs untuk menggunakan struktur "Makmal" secara konsisten.
- **Organisasi Laluan Pembelajaran**: Perkembangan yang jelas daripada konsep asas melalui pelaksanaan lanjutan kepada penghantaran pengeluaran.
- **Fokus Dunia Nyata**: Penekanan pada pembelajaran praktikal dan langsung dengan corak dan teknologi tahap perusahaan.

### Penambahbaikan Kualiti & Konsistensi Dokumentasi
- **Penekanan Pembelajaran Praktikal**: Memperkukuh pendekatan berasaskan makmal praktikal di seluruh dokumentasi.
- **Fokus Corak Perusahaan**: Menonjolkan pelaksanaan bersedia pengeluaran dan pertimbangan keselamatan perusahaan.
- **Integrasi Teknologi**: Liputan komprehensif tentang perkhidmatan Azure moden dan corak integrasi AI.
- **Perkembangan Pembelajaran**: Laluan berstruktur yang jelas daripada konsep asas kepada penghantaran pengeluaran.

## 26 September 2025

### Penambahbaikan Kajian Kes - Integrasi Registry MCP GitHub

#### Kajian Kes (09-CaseStudy/) - Fokus Pembangunan Ekosistem
- **README.md**: Pengembangan besar dengan kajian kes komprehensif Registry MCP GitHub.
  - **Kajian Kes Registry MCP GitHub**: Kajian kes baru yang komprehensif mengkaji pelancaran Registry MCP GitHub pada September 2025.
    - **Analisis Masalah**: Pemeriksaan terperinci tentang cabaran penemuan dan penghantaran pelayan MCP yang terpecah-pecah.
    - **Seni Bina Penyelesaian**: Pendekatan registry berpusat GitHub dengan pemasangan VS Code satu klik.
    - **Kesan Perniagaan**: Peningkatan yang boleh diukur dalam onboarding dan produktiviti pembangun.
    - **Nilai Strategik**: Fokus pada penghantaran agen modular dan interoperabiliti alat silang.
    - **Pembangunan Ekosistem**: Kedudukan sebagai platform asas untuk integrasi agen.
  - **Struktur Kajian Kes Dipertingkatkan**: Mengemas kini semua tujuh kajian kes dengan format yang konsisten dan penerangan komprehensif.
    - Azure AI Travel Agents: Penekanan pada orkestrasi multi-agen.
    - Integrasi Azure DevOps: Fokus pada automasi aliran kerja.
    - Pengambilan Dokumentasi Masa Nyata: Pelaksanaan klien konsol Python.
    - Penjana Pelan Kajian Interaktif: Aplikasi web perbualan Chainlit.
    - Dokumentasi Dalam Editor: Integrasi VS Code dan GitHub Copilot.
    - Pengurusan API Azure: Corak integrasi API perusahaan.
    - Registry MCP GitHub: Pembangunan ekosistem dan platform komuniti.
  - **Kesimpulan Komprehensif**: Bahagian kesimpulan yang ditulis semula menonjolkan tujuh kajian kes yang merangkumi pelbagai dimensi pelaksanaan MCP.
    - Integrasi Perusahaan, Orkestrasi Multi-Agen, Produktiviti Pembangun.
    - Pembangunan Ekosistem, Kategorisasi Aplikasi Pendidikan.
    - Wawasan yang dipertingkatkan tentang corak seni bina, strategi pelaksanaan, dan amalan terbaik.
    - Penekanan pada MCP sebagai protokol matang dan bersedia pengeluaran.

#### Kemas Kini Panduan Kajian (study_guide.md)
- **Peta Kurikulum Visual**: Dikemas kini mindmap untuk memasukkan Registry MCP GitHub dalam bahagian Kajian Kes.
- **Penerangan Kajian Kes**: Dipertingkatkan daripada penerangan generik kepada pecahan terperinci tujuh kajian kes komprehensif.
- **Struktur Repositori**: Dikemas kini bahagian 10 untuk mencerminkan liputan kajian kes komprehensif dengan butiran pelaksanaan khusus.
- **Integrasi Log Perubahan**: Menambah entri 26 September 2025 yang mendokumentasikan penambahan Registry MCP GitHub dan penambahbaikan kajian kes.
- **Kemas Kini Tarikh**: Dikemas kini cap masa footer untuk mencerminkan semakan terkini (26 September 2025).

### Penambahbaikan Kualiti Dokumentasi
- **Peningkatan Konsistensi**: Memperstandardkan format dan struktur kajian kes di semua tujuh contoh.
- **Liputan Komprehensif**: Kajian kes kini merangkumi senario perusahaan, produktiviti pembangun, dan pembangunan ekosistem.
- **Kedudukan Strategik**: Fokus yang dipertingkatkan pada MCP sebagai platform asas untuk penghantaran sistem agen.
- **Integrasi Sumber**: Dikemas kini sumber tambahan untuk memasukkan pautan Registry MCP GitHub.

## 15 September 2025

### Pengembangan Topik Lanjutan - Pengangkutan Tersuai & Kejuruteraan Konteks

#### Pengangkutan Tersuai MCP (05-AdvancedTopics/mcp-transport/) - Panduan Pelaksanaan Lanjutan Baru
- **README.md**: Panduan pelaksanaan lengkap untuk mekanisme pengangkutan MCP tersuai.
  - **Pengangkutan Azure Event Grid**: Pelaksanaan pengangkutan berasaskan acara tanpa pelayan yang komprehensif.
    - Contoh dalam C#, TypeScript, dan Python dengan integrasi Azure Functions.
    - Corak seni bina berasaskan acara untuk penyelesaian MCP yang boleh diskalakan.
    - Penerima webhook dan pengendalian mesej berasaskan push.
  - **Pengangkutan Azure Event Hubs**: Pelaksanaan pengangkutan streaming throughput tinggi.
    - Keupayaan streaming masa nyata untuk senario latensi rendah.
    - Strategi pembahagian dan pengurusan checkpoint.
    - Pengelompokan mesej dan pengoptimuman prestasi.
  - **Corak Integrasi Perusahaan**: Contoh seni bina bersedia pengeluaran.
    - Pemprosesan MCP teragih merentasi pelbagai Azure Functions.
    - Seni bina pengangkutan hibrid yang menggabungkan pelbagai jenis pengangkutan.
    - Ketahanan mesej, kebolehpercayaan, dan strategi pengendalian ralat.
  - **Keselamatan & Pemantauan**: Integrasi Azure Key Vault dan corak pemerhatian.
    - Pengesahan identiti terurus dan akses keistimewaan minimum.
    - Telemetri Application Insights dan pemantauan prestasi.
    - Pemutus litar dan corak toleransi kesalahan.
  - **Rangka Kerja Ujian**: Strategi ujian komprehensif untuk pengangkutan tersuai.
    - Ujian unit dengan test doubles dan rangka kerja mocking.
    - Ujian integrasi dengan Azure Test Containers.
    - Pertimbangan ujian prestasi dan beban.

#### Kejuruteraan Konteks (05-AdvancedTopics/mcp-contextengineering/) - Disiplin AI Baru
- **README.md**: Eksplorasi komprehensif tentang kejuruteraan konteks sebagai bidang yang sedang berkembang.
  - **Prinsip Teras**: Perkongsian konteks lengkap, kesedaran keputusan tindakan, dan pengurusan tetingkap konteks.
  - **Penyelarasan Protokol MCP**: Bagaimana reka bentuk MCP menangani cabaran kejuruteraan konteks.
    - Had tetingkap konteks dan strategi pemuatan progresif.
    - Penentuan relevansi dan pengambilan konteks dinamik.
    - Pengendalian konteks multi-modal dan pertimbangan keselamatan.
  - **Pendekatan Pelaksanaan**: Seni bina satu benang vs. multi-agen.
    - Teknik chunking dan keutamaan konteks.
    - Pemuatan konteks progresif dan strategi pemampatan.
    - Pendekatan berlapis konteks dan pengoptimuman pengambilan.
  - **Rangka Kerja Pengukuran**: Metrik baru untuk penilaian keberkesanan konteks.
    - Kecekapan input, prestasi, kualiti, dan pertimbangan pengalaman pengguna.
    - Pendekatan eksperimen untuk pengoptimuman konteks.
    - Analisis kegagalan dan metodologi peningkatan.

#### Kemas Kini Navigasi Kurikulum (README.md)
- **Struktur Modul Dipertingkatkan**: Dikemas kini jadual kurikulum untuk memasukkan topik lanjutan baru.
  - Menambah Kejuruteraan Konteks (5.14) dan Pengangkutan Tersuai (5.15).
  - Format dan pautan navigasi yang konsisten di semua modul.
  - Penerangan yang dikemas kini untuk mencerminkan skop kandungan semasa.

### Penambahbaikan Struktur Direktori
- **Penyeragaman Penamaan**: Menamakan semula "mcp transport" kepada "mcp-transport" untuk konsistensi dengan folder topik lanjutan lain.
- **Organisasi Kandungan**: Semua folder 05-AdvancedTopics kini mengikuti corak penamaan yang konsisten (mcp-[topik]).

### Penambahbaikan Kualiti Dokumentasi
- **Penyelarasan Spesifikasi MCP**: Semua kandungan baru merujuk kepada Spesifikasi MCP semasa 2025-06-18.
- **Contoh Pelbagai Bahasa**: Contoh kod komprehensif dalam C#, TypeScript, dan Python.
- **Fokus Perusahaan**: Corak bersedia pengeluaran dan integrasi awan Azure di seluruh.
- **Dokumentasi Visual**: Diagram Mermaid untuk visualisasi seni bina dan aliran.

## 18 Ogos 2025

### Kemas Kini Komprehensif Dokumentasi - Piawaian MCP 2025-06-18

#### Amalan Terbaik Keselamatan MCP (02-Security/) - Pemodenan Lengkap
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Penulisan semula lengkap yang selaras dengan Spesifikasi MCP 2025-06-18.
  - **Keperluan Wajib**: Menambah keperluan MUST/MUST NOT eksplisit daripada spesifikasi rasmi dengan penunjuk visual yang jelas.
  - **12 Amalan Keselamatan Teras**: Disusun semula daripada senarai 15 item kepada domain keselamatan yang komprehensif.
    - Keselamatan Token & Pengesahan dengan integrasi penyedia identiti luaran.
    - Pengurusan Sesi & Keselamatan Pengangkutan dengan keperluan kriptografi.
    - Perlindungan Ancaman Khusus AI dengan integrasi Microsoft Prompt Shields.
    - Kawalan Akses & Kebenaran dengan prinsip keistimewaan minimum.
    - Keselamatan Kandungan & Pemantauan dengan integrasi Azure Content Safety.
    - Keselamatan Rantaian Bekalan dengan pengesahan komponen yang komprehensif.
    - Keselamatan OAuth & Pencegahan Serangan Confused Deputy dengan pelaksanaan PKCE.
    - Tindak Balas & Pemulihan Insiden dengan keupayaan automatik.
    - Pematuhan & Tadbir Urus dengan penjajaran peraturan.
    - Kawalan Keselamatan Lanjutan dengan seni bina zero trust.
    - Integrasi Ekosistem Keselamatan Microsoft dengan penyelesaian komprehensif.
    - Evolusi Keselamatan Berterusan dengan amalan adaptif.
  - **Penyelesaian Keselamatan Microsoft**: Panduan integrasi yang dipertingkatkan untuk Prompt Shields, Azure Content Safety, Entra ID, dan GitHub Advanced Security.
  - **Sumber Pelaksanaan**: Pautan sumber komprehensif yang dikategorikan mengikut Dokumentasi MCP Rasmi, Penyelesaian Keselamatan Microsoft, Piawaian Keselamatan, dan Panduan Pelaksanaan.

#### Kawalan Keselamatan Lanjutan (02-Security/) - Pelaksanaan Perusahaan
- **MCP-SECURITY-CONTROLS-2025.md**: Penulisan semula lengkap dengan rangka kerja keselamatan tahap perusahaan.
  - **9 Domain Keselamatan Komprehensif**: Diperluas daripada kawalan asas kepada rangka kerja perusahaan yang terperinci.
    - Pengesahan & Kebenaran Lanjutan dengan integrasi Microsoft Entra ID.
    - Keselamatan Token & Kawalan Anti-Passthrough dengan pengesahan komprehensif.
    - Kawalan Keselamatan Sesi dengan pencegahan hijacking.
    - Kawalan Keselamatan Khusus AI dengan suntikan prompt dan pencegahan keracunan alat.
    - Pencegahan Serangan Confused Deputy dengan keselamatan proksi OAuth.
    - Keselamatan Pelaksanaan Alat dengan sandboxing dan pengasingan.
    - Kawalan Keselamatan Rantaian Bekalan dengan pengesahan
#### Topik Lanjutan Keselamatan (05-AdvancedTopics/mcp-security/) - Pelaksanaan Sedia Pengeluaran
- **README.md**: Penulisan semula sepenuhnya untuk pelaksanaan keselamatan perusahaan
  - **Penyelarasan Spesifikasi Semasa**: Dikemas kini kepada Spesifikasi MCP 2025-06-18 dengan keperluan keselamatan wajib
  - **Pengesahan Dipertingkatkan**: Integrasi Microsoft Entra ID dengan contoh menyeluruh dalam .NET dan Java Spring Security
  - **Integrasi Keselamatan AI**: Pelaksanaan Microsoft Prompt Shields dan Azure Content Safety dengan contoh terperinci dalam Python
  - **Mitigasi Ancaman Lanjutan**: Contoh pelaksanaan menyeluruh untuk
    - Pencegahan Serangan Confused Deputy dengan PKCE dan pengesahan persetujuan pengguna
    - Pencegahan Token Passthrough dengan pengesahan audiens dan pengurusan token yang selamat
    - Pencegahan Pengambilalihan Sesi dengan pengikatan kriptografi dan analisis tingkah laku
  - **Integrasi Keselamatan Perusahaan**: Pemantauan Azure Application Insights, saluran pengesanan ancaman, dan keselamatan rantaian bekalan
  - **Senarai Semak Pelaksanaan**: Kawalan keselamatan wajib vs. disyorkan yang jelas dengan manfaat ekosistem keselamatan Microsoft

### Kualiti Dokumentasi & Penyelarasan Piawaian
- **Rujukan Spesifikasi**: Semua rujukan dikemas kini kepada Spesifikasi MCP 2025-06-18 semasa
- **Ekosistem Keselamatan Microsoft**: Panduan integrasi dipertingkatkan di seluruh dokumentasi keselamatan
- **Pelaksanaan Praktikal**: Contoh kod terperinci ditambah dalam .NET, Java, dan Python dengan corak perusahaan
- **Organisasi Sumber**: Pengkategorian menyeluruh dokumentasi rasmi, piawaian keselamatan, dan panduan pelaksanaan
- **Penunjuk Visual**: Penandaan jelas keperluan wajib vs. amalan yang disyorkan

#### Konsep Asas (01-CoreConcepts/) - Pemodenan Lengkap
- **Kemas Kini Versi Protokol**: Dikemas kini untuk merujuk kepada Spesifikasi MCP semasa 2025-06-18 dengan penentuan versi berdasarkan tarikh (format YYYY-MM-DD)
- **Penyempurnaan Seni Bina**: Penerangan dipertingkatkan tentang Hos, Klien, dan Pelayan untuk mencerminkan corak seni bina MCP semasa
  - Hos kini ditakrifkan dengan jelas sebagai aplikasi AI yang menyelaraskan pelbagai sambungan klien MCP
  - Klien diterangkan sebagai penyambung protokol yang mengekalkan hubungan satu-ke-satu dengan pelayan
  - Pelayan dipertingkatkan dengan senario pelaksanaan tempatan vs. jauh
- **Penyusunan Semula Primitif**: Penstrukturan semula sepenuhnya primitif pelayan dan klien
  - Primitif Pelayan: Sumber (pangkalan data), Prompt (templat), Alat (fungsi boleh laksana) dengan penerangan dan contoh terperinci
  - Primitif Klien: Sampling (penyelesaian LLM), Elicitation (input pengguna), Logging (debugging/pemantauan)
  - Dikemas kini dengan corak kaedah penemuan (`*/list`), pengambilan (`*/get`), dan pelaksanaan (`*/call`) semasa
- **Seni Bina Protokol**: Memperkenalkan model seni bina dua lapisan
  - Lapisan Data: Asas JSON-RPC 2.0 dengan pengurusan kitaran hayat dan primitif
  - Lapisan Pengangkutan: STDIO (tempatan) dan HTTP yang boleh distrim dengan SSE (jauh)
- **Kerangka Keselamatan**: Prinsip keselamatan menyeluruh termasuk persetujuan pengguna eksplisit, perlindungan privasi data, keselamatan pelaksanaan alat, dan keselamatan lapisan pengangkutan
- **Corak Komunikasi**: Mesej protokol dikemas kini untuk menunjukkan aliran inisialisasi, penemuan, pelaksanaan, dan pemberitahuan
- **Contoh Kod**: Contoh pelbagai bahasa dikemas kini (.NET, Java, Python, JavaScript) untuk mencerminkan corak SDK MCP semasa

#### Keselamatan (02-Security/) - Penstrukturan Semula Keselamatan Menyeluruh  
- **Penyelarasan Piawaian**: Penyelarasan penuh dengan keperluan keselamatan Spesifikasi MCP 2025-06-18
- **Evolusi Pengesahan**: Dokumentasi evolusi daripada pelayan OAuth tersuai kepada delegasi penyedia identiti luaran (Microsoft Entra ID)
- **Analisis Ancaman AI Khusus**: Liputan dipertingkatkan vektor serangan AI moden
  - Senario serangan suntikan prompt terperinci dengan contoh dunia sebenar
  - Mekanisme keracunan alat dan corak serangan "rug pull"
  - Keracunan tetingkap konteks dan serangan kekeliruan model
- **Penyelesaian Keselamatan AI Microsoft**: Liputan menyeluruh ekosistem keselamatan Microsoft
  - AI Prompt Shields dengan teknik pengesanan, penyorotan, dan pemisah lanjutan
  - Corak integrasi Azure Content Safety
  - Keselamatan Lanjutan GitHub untuk perlindungan rantaian bekalan
- **Mitigasi Ancaman Lanjutan**: Kawalan keselamatan terperinci untuk
  - Pengambilalihan sesi dengan senario serangan khusus MCP dan keperluan ID sesi kriptografi
  - Masalah Confused Deputy dalam senario proksi MCP dengan keperluan persetujuan eksplisit
  - Kerentanan token passthrough dengan kawalan pengesahan wajib
- **Keselamatan Rantaian Bekalan**: Liputan rantaian bekalan AI yang diperluas termasuk model asas, perkhidmatan embeddings, penyedia konteks, dan API pihak ketiga
- **Keselamatan Asas**: Integrasi dipertingkatkan dengan corak keselamatan perusahaan termasuk seni bina zero trust dan ekosistem keselamatan Microsoft
- **Organisasi Sumber**: Pautan sumber menyeluruh dikategorikan mengikut jenis (Dokumen Rasmi, Piawaian, Penyelidikan, Penyelesaian Microsoft, Panduan Pelaksanaan)

### Penambahbaikan Kualiti Dokumentasi
- **Objektif Pembelajaran Berstruktur**: Objektif pembelajaran dipertingkatkan dengan hasil yang spesifik dan boleh dilaksanakan
- **Rujukan Silang**: Pautan ditambah antara topik keselamatan dan konsep asas yang berkaitan
- **Maklumat Terkini**: Semua rujukan tarikh dan pautan spesifikasi dikemas kini kepada piawaian semasa
- **Panduan Pelaksanaan**: Panduan pelaksanaan spesifik dan boleh dilaksanakan ditambah di seluruh kedua-dua bahagian

## 16 Julai 2025

### README dan Penambahbaikan Navigasi
- Reka bentuk semula sepenuhnya navigasi kurikulum dalam README.md
- Menggantikan tag `<details>` dengan format berasaskan jadual yang lebih mudah diakses
- Mencipta pilihan susun atur alternatif dalam folder "alternative_layouts" baharu
- Menambah contoh navigasi gaya kad, tab, dan akordion
- Mengemas kini bahagian struktur repositori untuk memasukkan semua fail terkini
- Memperbaiki bahagian "Cara Menggunakan Kurikulum Ini" dengan cadangan yang jelas
- Mengemas kini pautan spesifikasi MCP untuk menunjuk kepada URL yang betul
- Menambah bahagian Kejuruteraan Konteks (5.14) kepada struktur kurikulum

### Kemas Kini Panduan Kajian
- Panduan kajian disemak sepenuhnya untuk menyelaraskan dengan struktur repositori semasa
- Menambah bahagian baharu untuk Klien dan Alat MCP, serta Pelayan MCP Popular
- Mengemas kini Peta Kurikulum Visual untuk mencerminkan semua topik dengan tepat
- Penerangan dipertingkatkan tentang Topik Lanjutan untuk merangkumi semua bidang khusus
- Mengemas kini bahagian Kajian Kes untuk mencerminkan contoh sebenar
- Menambah changelog menyeluruh ini

### Sumbangan Komuniti (06-CommunityContributions/)
- Menambah maklumat terperinci tentang pelayan MCP untuk penjanaan imej
- Menambah bahagian menyeluruh tentang menggunakan Claude dalam VSCode
- Menambah arahan persediaan dan penggunaan klien terminal Cline
- Mengemas kini bahagian klien MCP untuk memasukkan semua pilihan klien popular
- Contoh sumbangan dipertingkatkan dengan sampel kod yang lebih tepat

### Topik Lanjutan (05-AdvancedTopics/)
- Mengatur semua folder topik khusus dengan penamaan yang konsisten
- Menambah bahan dan contoh kejuruteraan konteks
- Menambah dokumentasi integrasi ejen Foundry
- Dokumentasi integrasi keselamatan Entra ID dipertingkatkan

## 11 Jun 2025

### Penciptaan Awal
- Melancarkan versi pertama kurikulum MCP untuk Pemula
- Mencipta struktur asas untuk semua 10 bahagian utama
- Melaksanakan Peta Kurikulum Visual untuk navigasi
- Menambah projek sampel awal dalam pelbagai bahasa pengaturcaraan

### Memulakan (03-GettingStarted/)
- Mencipta contoh pelaksanaan pelayan pertama
- Menambah panduan pembangunan klien
- Termasuk arahan integrasi klien LLM
- Menambah dokumentasi integrasi VS Code
- Melaksanakan contoh pelayan Server-Sent Events (SSE)

### Konsep Asas (01-CoreConcepts/)
- Menambah penerangan terperinci tentang seni bina klien-pelayan
- Mencipta dokumentasi tentang komponen utama protokol
- Mesej corak dalam MCP didokumentasikan

## 23 Mei 2025

### Struktur Repositori
- Memulakan repositori dengan struktur folder asas
- Mencipta fail README untuk setiap bahagian utama
- Menyediakan infrastruktur terjemahan
- Menambah aset imej dan diagram

### Dokumentasi
- Mencipta README.md awal dengan gambaran keseluruhan kurikulum
- Menambah CODE_OF_CONDUCT.md dan SECURITY.md
- Menyediakan SUPPORT.md dengan panduan untuk mendapatkan bantuan
- Mencipta struktur panduan kajian awal

## 15 April 2025

### Perancangan dan Kerangka
- Perancangan awal untuk kurikulum MCP untuk Pemula
- Menentukan objektif pembelajaran dan audiens sasaran
- Menggariskan struktur 10 bahagian kurikulum
- Membangunkan kerangka konseptual untuk contoh dan kajian kes
- Mencipta contoh prototaip awal untuk konsep utama

---

**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk memastikan ketepatan, sila ambil perhatian bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang berwibawa. Untuk maklumat yang kritikal, terjemahan manusia profesional adalah disyorkan. Kami tidak bertanggungjawab atas sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.