<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T17:56:31+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "ms"
}
-->
# MCP Keselamatan: Perlindungan Komprehensif untuk Sistem AI

[![Amalan Terbaik Keselamatan MCP](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.ms.png)](https://youtu.be/88No8pw706o)

_(Klik imej di atas untuk menonton video pelajaran ini)_

Keselamatan adalah asas dalam reka bentuk sistem AI, sebab itulah kami mengutamakannya sebagai bahagian kedua. Ini sejajar dengan prinsip **Secure by Design** Microsoft daripada [Secure Future Initiative](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Model Context Protocol (MCP) membawa keupayaan baharu yang kuat kepada aplikasi berasaskan AI sambil memperkenalkan cabaran keselamatan unik yang melangkaui risiko perisian tradisional. Sistem MCP menghadapi kebimbangan keselamatan yang telah lama wujud (pengkodan selamat, keistimewaan minimum, keselamatan rantaian bekalan) dan ancaman khusus AI baharu termasuk suntikan prompt, keracunan alat, rampasan sesi, serangan timbal balik keliru, kelemahan token passthrough, dan pengubahsuaian keupayaan dinamik.

Pelajaran ini meneroka risiko keselamatan paling kritikal dalam pelaksanaan MCP—meliputi pengesahan, kebenaran, keistimewaan berlebihan, suntikan prompt tidak langsung, keselamatan sesi, masalah timbal balik keliru, pengurusan token, dan kelemahan rantaian bekalan. Anda akan mempelajari kawalan yang boleh diambil tindakan dan amalan terbaik untuk mengurangkan risiko ini sambil memanfaatkan penyelesaian Microsoft seperti Prompt Shields, Azure Content Safety, dan GitHub Advanced Security untuk memperkukuh pelaksanaan MCP anda.

## Objektif Pembelajaran

Menjelang akhir pelajaran ini, anda akan dapat:

- **Kenal Pasti Ancaman Khusus MCP**: Mengenal pasti risiko keselamatan unik dalam sistem MCP termasuk suntikan prompt, keracunan alat, keistimewaan berlebihan, rampasan sesi, masalah timbal balik keliru, kelemahan token passthrough, dan risiko rantaian bekalan
- **Terapkan Kawalan Keselamatan**: Melaksanakan mitigasi berkesan termasuk pengesahan yang kukuh, akses keistimewaan minimum, pengurusan token yang selamat, kawalan keselamatan sesi, dan pengesahan rantaian bekalan
- **Manfaatkan Penyelesaian Keselamatan Microsoft**: Memahami dan menggunakan Microsoft Prompt Shields, Azure Content Safety, dan GitHub Advanced Security untuk perlindungan beban kerja MCP
- **Sahkan Keselamatan Alat**: Mengiktiraf kepentingan pengesahan metadata alat, pemantauan perubahan dinamik, dan mempertahankan daripada serangan suntikan prompt tidak langsung
- **Gabungkan Amalan Terbaik**: Menggabungkan asas keselamatan yang telah ditetapkan (pengkodan selamat, pengerasan pelayan, zero trust) dengan kawalan khusus MCP untuk perlindungan menyeluruh

# Seni Bina & Kawalan Keselamatan MCP

Pelaksanaan MCP moden memerlukan pendekatan keselamatan berlapis yang menangani kedua-dua keselamatan perisian tradisional dan ancaman khusus AI. Spesifikasi MCP yang berkembang pesat terus mematangkan kawalan keselamatannya, membolehkan integrasi yang lebih baik dengan seni bina keselamatan perusahaan dan amalan terbaik yang telah ditetapkan.

Penyelidikan daripada [Microsoft Digital Defense Report](https://aka.ms/mddr) menunjukkan bahawa **98% pelanggaran yang dilaporkan dapat dicegah dengan kebersihan keselamatan yang kukuh**. Strategi perlindungan paling berkesan menggabungkan amalan keselamatan asas dengan kawalan khusus MCP—langkah keselamatan asas yang terbukti kekal paling berkesan dalam mengurangkan risiko keselamatan keseluruhan.

## Lanskap Keselamatan Semasa

> **Nota:** Maklumat ini mencerminkan piawaian keselamatan MCP setakat **18 Ogos 2025**. Protokol MCP terus berkembang dengan pesat, dan pelaksanaan masa depan mungkin memperkenalkan corak pengesahan baharu dan kawalan yang dipertingkatkan. Sentiasa rujuk [Spesifikasi MCP](https://spec.modelcontextprotocol.io/), [repositori GitHub MCP](https://github.com/modelcontextprotocol), dan [dokumentasi amalan terbaik keselamatan](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) terkini untuk panduan terkini.

### Evolusi Pengesahan MCP

Spesifikasi MCP telah berkembang dengan ketara dalam pendekatannya terhadap pengesahan dan kebenaran:

- **Pendekatan Asal**: Spesifikasi awal memerlukan pembangun untuk melaksanakan pelayan pengesahan tersuai, dengan pelayan MCP bertindak sebagai Pelayan Kebenaran OAuth 2.0 yang mengurus pengesahan pengguna secara langsung
- **Piawaian Semasa (2025-06-18)**: Spesifikasi yang dikemas kini membolehkan pelayan MCP mendelegasikan pengesahan kepada penyedia identiti luaran (seperti Microsoft Entra ID), meningkatkan postur keselamatan dan mengurangkan kerumitan pelaksanaan
- **Keselamatan Lapisan Pengangkutan**: Sokongan yang dipertingkatkan untuk mekanisme pengangkutan selamat dengan corak pengesahan yang betul untuk sambungan tempatan (STDIO) dan jauh (Streamable HTTP)

## Keselamatan Pengesahan & Kebenaran

### Cabaran Keselamatan Semasa

Pelaksanaan MCP moden menghadapi beberapa cabaran pengesahan dan kebenaran:

### Risiko & Vektor Ancaman

- **Logik Kebenaran yang Salah Konfigurasi**: Pelaksanaan kebenaran yang cacat dalam pelayan MCP boleh mendedahkan data sensitif dan menerapkan kawalan akses dengan salah
- **Kompromi Token OAuth**: Kecurian token pelayan MCP tempatan membolehkan penyerang menyamar sebagai pelayan dan mengakses perkhidmatan hiliran
- **Kelemahan Token Passthrough**: Pengendalian token yang tidak betul mencipta pintasan kawalan keselamatan dan jurang akauntabiliti
- **Keistimewaan Berlebihan**: Pelayan MCP yang terlalu berkeistimewaan melanggar prinsip keistimewaan minimum dan memperluas permukaan serangan

#### Token Passthrough: Corak Anti Kritikal

**Token passthrough secara eksplisit dilarang** dalam spesifikasi kebenaran MCP semasa kerana implikasi keselamatan yang serius:

##### Pencabulan Kawalan Keselamatan
- Pelayan MCP dan API hiliran melaksanakan kawalan keselamatan kritikal (had kadar, pengesahan permintaan, pemantauan trafik) yang bergantung pada pengesahan token yang betul
- Penggunaan token langsung oleh klien kepada API memintas perlindungan penting ini, merosakkan seni bina keselamatan

##### Cabaran Akauntabiliti & Audit  
- Pelayan MCP tidak dapat membezakan antara klien yang menggunakan token yang dikeluarkan oleh pihak hulu, memecahkan jejak audit
- Log pelayan sumber hiliran menunjukkan asal permintaan yang mengelirukan dan bukannya perantara pelayan MCP sebenar
- Penyiasatan insiden dan audit pematuhan menjadi jauh lebih sukar

##### Risiko Eksfiltrasi Data
- Tuntutan token yang tidak disahkan membolehkan pelaku jahat dengan token yang dicuri menggunakan pelayan MCP sebagai proksi untuk eksfiltrasi data
- Pelanggaran sempadan kepercayaan membolehkan corak akses tanpa kebenaran yang memintas kawalan keselamatan yang dimaksudkan

##### Vektor Serangan Pelbagai Perkhidmatan
- Token yang dikompromi diterima oleh pelbagai perkhidmatan membolehkan pergerakan lateral merentasi sistem yang disambungkan
- Andaian kepercayaan antara perkhidmatan boleh dilanggar apabila asal token tidak dapat disahkan

### Kawalan Keselamatan & Mitigasi

**Keperluan Keselamatan Kritikal:**

> **WAJIB**: Pelayan MCP **TIDAK BOLEH** menerima sebarang token yang tidak dikeluarkan secara eksplisit untuk pelayan MCP

#### Kawalan Pengesahan & Kebenaran

- **Semakan Kebenaran yang Ketat**: Lakukan audit menyeluruh terhadap logik kebenaran pelayan MCP untuk memastikan hanya pengguna dan klien yang dimaksudkan boleh mengakses sumber sensitif
  - **Panduan Pelaksanaan**: [Azure API Management sebagai Gateway Pengesahan untuk Pelayan MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Integrasi Identiti**: [Menggunakan Microsoft Entra ID untuk Pengesahan Pelayan MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Pengurusan Token Selamat**: Laksanakan [amalan terbaik pengesahan dan kitaran hayat token Microsoft](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Sahkan tuntutan penonton token sepadan dengan identiti pelayan MCP
  - Laksanakan dasar putaran dan tamat tempoh token yang betul
  - Cegah serangan ulangan token dan penggunaan tanpa kebenaran

- **Penyimpanan Token Dilindungi**: Simpan token dengan selamat menggunakan penyulitan semasa rehat dan dalam transit
  - **Amalan Terbaik**: [Garis Panduan Penyimpanan dan Penyulitan Token Selamat](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Pelaksanaan Kawalan Akses

- **Prinsip Keistimewaan Minimum**: Berikan pelayan MCP hanya keistimewaan minimum yang diperlukan untuk fungsi yang dimaksudkan
  - Semakan dan kemas kini keistimewaan secara berkala untuk mencegah peningkatan keistimewaan
  - **Dokumentasi Microsoft**: [Akses Keistimewaan Minimum yang Selamat](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Kawalan Akses Berasaskan Peranan (RBAC)**: Laksanakan tugasan peranan yang terperinci
  - Skopkan peranan dengan ketat kepada sumber dan tindakan tertentu
  - Elakkan keistimewaan yang luas atau tidak perlu yang memperluas permukaan serangan

- **Pemantauan Keistimewaan Berterusan**: Laksanakan audit dan pemantauan akses yang berterusan
  - Pantau corak penggunaan keistimewaan untuk anomali
  - Segera atasi keistimewaan yang berlebihan atau tidak digunakan

## Ancaman Keselamatan Khusus AI

### Serangan Suntikan Prompt & Manipulasi Alat

Pelaksanaan MCP moden menghadapi vektor serangan khusus AI yang canggih yang tidak dapat ditangani sepenuhnya oleh langkah keselamatan tradisional:

#### **Suntikan Prompt Tidak Langsung (Suntikan Prompt Rentas Domain)**

**Suntikan Prompt Tidak Langsung** mewakili salah satu kelemahan paling kritikal dalam sistem AI yang didayakan MCP. Penyerang menyisipkan arahan berniat jahat dalam kandungan luaran—dokumen, laman web, e-mel, atau sumber data—yang kemudiannya diproses oleh sistem AI sebagai arahan yang sah.

**Senario Serangan:**
- **Suntikan Berasaskan Dokumen**: Arahan berniat jahat tersembunyi dalam dokumen yang diproses yang mencetuskan tindakan AI yang tidak diingini
- **Eksploitasi Kandungan Web**: Laman web yang dikompromi mengandungi prompt tertanam yang memanipulasi tingkah laku AI apabila diimbas
- **Serangan Berasaskan E-mel**: Prompt berniat jahat dalam e-mel yang menyebabkan pembantu AI membocorkan maklumat atau melakukan tindakan tanpa kebenaran
- **Pencemaran Sumber Data**: Pangkalan data atau API yang dikompromi menyajikan kandungan tercemar kepada sistem AI

**Kesan Dunia Sebenar**: Serangan ini boleh mengakibatkan eksfiltrasi data, pelanggaran privasi, penjanaan kandungan berbahaya, dan manipulasi interaksi pengguna. Untuk analisis terperinci, lihat [Prompt Injection dalam MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Rajah Serangan Suntikan Prompt](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.ms.png)

#### **Serangan Keracunan Alat**

**Keracunan Alat** menyasarkan metadata yang mentakrifkan alat MCP, mengeksploitasi cara LLM mentafsirkan penerangan alat dan parameter untuk membuat keputusan pelaksanaan.

**Mekanisme Serangan:**
- **Manipulasi Metadata**: Penyerang menyisipkan arahan berniat jahat ke dalam penerangan alat, definisi parameter, atau contoh penggunaan
- **Arahan Tidak Kelihatan**: Prompt tersembunyi dalam metadata alat yang diproses oleh model AI tetapi tidak kelihatan kepada pengguna manusia
- **Pengubahsuaian Alat Dinamik ("Rug Pulls")**: Alat yang diluluskan oleh pengguna kemudiannya diubah untuk melakukan tindakan berniat jahat tanpa pengetahuan pengguna
- **Suntikan Parameter**: Kandungan berniat jahat yang tertanam dalam skema parameter alat yang mempengaruhi tingkah laku model

**Risiko Pelayan Dihoskan**: Pelayan MCP jauh menghadirkan risiko yang lebih tinggi kerana definisi alat boleh dikemas kini selepas kelulusan awal pengguna, mencipta senario di mana alat yang sebelum ini selamat menjadi berniat jahat. Untuk analisis menyeluruh, lihat [Serangan Keracunan Alat (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Rajah Suntikan Alat](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.ms.png)

#### **Vektor Serangan AI Tambahan**

- **Suntikan Prompt Rentas Domain (XPIA)**: Serangan canggih yang memanfaatkan kandungan daripada pelbagai domain untuk memintas kawalan keselamatan
- **Pengubahsuaian Keupayaan Dinamik**: Perubahan masa nyata kepada keupayaan alat yang melarikan diri daripada penilaian keselamatan awal
- **Pencemaran Tetingkap Konteks**: Serangan yang memanipulasi tetingkap konteks besar untuk menyembunyikan arahan berniat jahat
- **Serangan Kekeliruan Model**: Mengeksploitasi batasan model untuk mencipta tingkah laku yang tidak dapat diramalkan atau tidak selamat

### Kesan Risiko Keselamatan AI

**Akibat Berimpak Tinggi:**
- **Eksfiltrasi Data**: Akses tanpa kebenaran dan kecurian data perusahaan atau peribadi yang sensitif
- **Pelanggaran Privasi**: Pendedahan maklumat peribadi yang boleh dikenal pasti (PII) dan data perniagaan sulit  
- **Manipulasi Sistem**: Pengubahsuaian yang tidak diingini kepada sistem dan aliran kerja kritikal
- **Kecurian Kredensial**: Kompromi token pengesahan dan kelayakan perkhidmatan
- **Pergerakan Lateral**: Penggunaan sistem AI yang dikompromi sebagai titik tumpuan untuk serangan rangkaian yang lebih luas

### Penyelesaian Keselamatan AI Microsoft

#### **AI Prompt Shields: Perlindungan Lanjutan Terhadap Serangan Suntikan**

Microsoft **AI Prompt Shields** menyediakan pertahanan menyeluruh terhadap kedua-dua serangan suntikan prompt langsung dan tidak langsung melalui pelbagai lapisan keselamatan:

##### **Mekanisme Perlindungan Teras:**

1. **Pengesanan & Penapisan Lanjutan**
   - Algoritma pembelajaran mesin dan teknik NLP mengesan arahan berniat jahat dalam kandungan luaran
   - Analisis masa nyata dokumen, laman web, e-mel, dan sumber data untuk ancaman tertanam
   - Pemahaman kontekstual tentang corak prompt yang sah vs. berniat jahat

2. **Teknik Spotlighting**  
   - Membezakan antara arahan sistem yang dipercayai dan input luaran yang berpotensi dikompromi
   - Kaedah transformasi teks yang meningkatkan kaitan model sambil mengasingkan kandungan berniat jahat
   - Membantu sistem AI mengekalkan hierarki arahan yang betul dan mengabaikan arahan yang disuntik

3. **Sistem Delimiter & Datamarking**
   - Takrifan sempadan eksplisit antara mesej sistem yang dipercayai dan teks input luaran
   - Penanda khas menyerlahkan sempadan antara sumber data yang dipercayai dan tidak dipercayai
   - Pemisahan yang jelas mencegah kekeliruan arahan dan pelaksanaan arahan tanpa kebenaran

4. **Perisikan Ancaman Berterusan**
   - Microsoft sentiasa memantau corak serangan yang muncul dan mengemas kini pertahanan
   - Pemburuan ancaman proaktif untuk teknik suntikan baharu dan vektor serangan
   - Kemas kini model keselamatan secara berkala untuk mengekalkan keberkesanan terhadap ancaman yang berkembang

5. **Integrasi Azure Content Safety**
   - Sebahagian daripada suite keselamatan kandungan Azure AI yang komprehensif
   - Pengesanan tambahan untuk percubaan jailbreak, kandungan berbahaya, dan pelanggaran dasar keselamatan
   - Kawalan keselamatan bersatu merentasi komponen aplikasi AI

**Sumber Pelaksanaan**: [Dokumentasi Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)

![Perlindungan Microsoft Prompt Shields](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.ms.png)


## Ancaman Keselamatan MCP Lanjutan

### Kelemahan Rampasan Sesi

**Rampasan sesi** mewakili vektor serangan kritikal dalam pelaksanaan MCP berkeadaan di mana pihak yang tidak dibenarkan memperoleh dan menyalahgunakan pengecam sesi yang sah untuk menyamar sebagai klien dan melakukan tindakan tanpa kebenaran.

#### **Senario Serangan & Risiko**

- **Suntikan Prompt Rampasan Sesi**: Penyerang dengan ID sesi yang dicuri menyuntik peristiwa berniat jahat ke dalam pelayan yang berkongsi keadaan sesi, berpotensi mencetuskan tindakan berbahaya atau mengakses data sensitif
- **
- **Penciptaan Sesi Selamat**: Gunakan ID sesi yang selamat secara kriptografi dan tidak deterministik yang dihasilkan dengan penjana nombor rawak yang selamat  
- **Pengikatan Khusus Pengguna**: Ikat ID sesi kepada maklumat khusus pengguna menggunakan format seperti `<user_id>:<session_id>` untuk mencegah penyalahgunaan sesi antara pengguna  
- **Pengurusan Kitaran Hayat Sesi**: Laksanakan tamat tempoh, putaran, dan pembatalan yang betul untuk mengehadkan tingkap kerentanan  
- **Keselamatan Pengangkutan**: HTTPS wajib untuk semua komunikasi bagi mencegah pemintasan ID sesi  

### Masalah Timbalan Keliru  

**Masalah timbalan keliru** berlaku apabila pelayan MCP bertindak sebagai proksi pengesahan antara klien dan perkhidmatan pihak ketiga, mewujudkan peluang untuk pintasan kebenaran melalui eksploitasi ID klien statik.  

#### **Mekanisme Serangan & Risiko**  

- **Pintasan Persetujuan Berasaskan Kuki**: Pengesahan pengguna sebelumnya mencipta kuki persetujuan yang dieksploitasi oleh penyerang melalui permintaan kebenaran berniat jahat dengan URI pengalihan yang direka  
- **Kecurian Kod Kebenaran**: Kuki persetujuan sedia ada boleh menyebabkan pelayan kebenaran melangkau skrin persetujuan, mengalihkan kod ke titik akhir yang dikawal penyerang  
- **Akses API Tanpa Kebenaran**: Kod kebenaran yang dicuri membolehkan pertukaran token dan penyamaran pengguna tanpa kelulusan eksplisit  

#### **Strategi Mitigasi**  

**Kawalan Wajib:**  
- **Keperluan Persetujuan Eksplisit**: Pelayan proksi MCP yang menggunakan ID klien statik **MESTI** mendapatkan persetujuan pengguna untuk setiap klien yang didaftarkan secara dinamik  
- **Pelaksanaan Keselamatan OAuth 2.1**: Ikuti amalan terbaik keselamatan OAuth semasa termasuk PKCE (Proof Key for Code Exchange) untuk semua permintaan kebenaran  
- **Pengesahan Klien Ketat**: Laksanakan pengesahan ketat terhadap URI pengalihan dan pengecam klien untuk mencegah eksploitasi  

### Kerentanan Passthrough Token  

**Passthrough token** mewakili corak anti eksplisit di mana pelayan MCP menerima token klien tanpa pengesahan yang betul dan meneruskannya ke API hiliran, melanggar spesifikasi kebenaran MCP.  

#### **Implikasi Keselamatan**  

- **Pintasan Kawalan**: Penggunaan token klien-ke-API secara langsung memintas kawalan penting seperti had kadar, pengesahan, dan pemantauan  
- **Pencemaran Jejak Audit**: Token yang dikeluarkan oleh hulu menjadikan pengenalan klien mustahil, merosakkan keupayaan penyiasatan insiden  
- **Eksfiltrasi Data Berasaskan Proksi**: Token yang tidak disahkan membolehkan pelaku berniat jahat menggunakan pelayan sebagai proksi untuk akses data tanpa kebenaran  
- **Pelanggaran Sempadan Kepercayaan**: Andaian kepercayaan perkhidmatan hiliran mungkin dilanggar apabila asal token tidak dapat disahkan  
- **Pengembangan Serangan Multi-Perkhidmatan**: Token yang dikompromi diterima di pelbagai perkhidmatan membolehkan pergerakan lateral  

#### **Kawalan Keselamatan Diperlukan**  

**Keperluan Tidak Boleh Ditawar:**  
- **Pengesahan Token**: Pelayan MCP **MESTI TIDAK** menerima token yang tidak dikeluarkan secara eksplisit untuk pelayan MCP  
- **Pengesahan Penonton**: Sentiasa sahkan tuntutan penonton token sepadan dengan identiti pelayan MCP  
- **Kitaran Hayat Token yang Betul**: Laksanakan token akses jangka pendek dengan amalan putaran yang selamat  

## Keselamatan Rantaian Bekalan untuk Sistem AI  

Keselamatan rantaian bekalan telah berkembang melangkaui pergantungan perisian tradisional untuk merangkumi keseluruhan ekosistem AI. Pelaksanaan MCP moden mesti mengesahkan dan memantau semua komponen berkaitan AI dengan teliti, kerana setiap satu memperkenalkan potensi kerentanan yang boleh menjejaskan integriti sistem.  

### Komponen Rantaian Bekalan AI yang Diperluas  

**Pergantungan Perisian Tradisional:**  
- Perpustakaan dan rangka kerja sumber terbuka  
- Imej kontena dan sistem asas  
- Alat pembangunan dan saluran binaan  
- Komponen dan perkhidmatan infrastruktur  

**Elemen Rantaian Bekalan Khusus AI:**  
- **Model Asas**: Model pra-latih daripada pelbagai penyedia yang memerlukan pengesahan asal usul  
- **Perkhidmatan Penyisipan**: Perkhidmatan vektorisasi dan carian semantik luaran  
- **Penyedia Konteks**: Sumber data, pangkalan pengetahuan, dan repositori dokumen  
- **API Pihak Ketiga**: Perkhidmatan AI luaran, saluran ML, dan titik akhir pemprosesan data  
- **Artifak Model**: Berat, konfigurasi, dan varian model yang disesuaikan  
- **Sumber Data Latihan**: Set data yang digunakan untuk latihan dan penyesuaian model  

### Strategi Keselamatan Rantaian Bekalan Komprehensif  

#### **Pengesahan Komponen & Kepercayaan**  
- **Pengesahan Asal Usul**: Sahkan asal, pelesenan, dan integriti semua komponen AI sebelum integrasi  
- **Penilaian Keselamatan**: Lakukan imbasan kerentanan dan ulasan keselamatan untuk model, sumber data, dan perkhidmatan AI  
- **Analisis Reputasi**: Nilai rekod jejak keselamatan dan amalan penyedia perkhidmatan AI  
- **Pengesahan Pematuhan**: Pastikan semua komponen memenuhi keperluan keselamatan dan peraturan organisasi  

#### **Saluran Penerapan Selamat**  
- **Keselamatan CI/CD Automatik**: Integrasikan imbasan keselamatan sepanjang saluran penerapan automatik  
- **Integriti Artifak**: Laksanakan pengesahan kriptografi untuk semua artifak yang diterapkan (kod, model, konfigurasi)  
- **Penerapan Berperingkat**: Gunakan strategi penerapan progresif dengan pengesahan keselamatan di setiap peringkat  
- **Repositori Artifak Terpercaya**: Terapkan hanya dari registri dan repositori artifak yang disahkan dan selamat  

#### **Pemantauan & Tindak Balas Berterusan**  
- **Imbasan Pergantungan**: Pemantauan kerentanan berterusan untuk semua pergantungan perisian dan komponen AI  
- **Pemantauan Model**: Penilaian berterusan terhadap tingkah laku model, penyimpangan prestasi, dan anomali keselamatan  
- **Penjejakan Kesihatan Perkhidmatan**: Pantau perkhidmatan AI luaran untuk ketersediaan, insiden keselamatan, dan perubahan polisi  
- **Integrasi Perisikan Ancaman**: Gabungkan suapan ancaman khusus untuk risiko keselamatan AI dan ML  

#### **Kawalan Akses & Keistimewaan Minimum**  
- **Kebenaran Tahap Komponen**: Hadkan akses kepada model, data, dan perkhidmatan berdasarkan keperluan perniagaan  
- **Pengurusan Akaun Perkhidmatan**: Laksanakan akaun perkhidmatan khusus dengan keistimewaan minimum yang diperlukan  
- **Segmentasi Rangkaian**: Isolasi komponen AI dan hadkan akses rangkaian antara perkhidmatan  
- **Kawalan Gerbang API**: Gunakan gerbang API berpusat untuk mengawal dan memantau akses kepada perkhidmatan AI luaran  

#### **Tindak Balas Insiden & Pemulihan**  
- **Prosedur Tindak Balas Pantas**: Proses yang ditetapkan untuk menampal atau menggantikan komponen AI yang dikompromi  
- **Putaran Kredensial**: Sistem automatik untuk memutar rahsia, kunci API, dan kredensial perkhidmatan  
- **Keupayaan Rollback**: Keupayaan untuk segera kembali ke versi komponen AI yang diketahui baik sebelumnya  
- **Pemulihan Pelanggaran Rantaian Bekalan**: Prosedur khusus untuk bertindak balas terhadap kompromi perkhidmatan AI hulu  

### Alat Keselamatan Microsoft & Integrasi  

**GitHub Advanced Security** menyediakan perlindungan rantaian bekalan yang komprehensif termasuk:  
- **Imbasan Rahsia**: Pengesanan automatik kredensial, kunci API, dan token dalam repositori  
- **Imbasan Pergantungan**: Penilaian kerentanan untuk pergantungan dan perpustakaan sumber terbuka  
- **Analisis CodeQL**: Analisis kod statik untuk kerentanan keselamatan dan isu pengkodan  
- **Wawasan Rantaian Bekalan**: Penglihatan ke dalam kesihatan dan status keselamatan pergantungan  

**Integrasi Azure DevOps & Azure Repos:**  
- Integrasi imbasan keselamatan yang lancar di seluruh platform pembangunan Microsoft  
- Pemeriksaan keselamatan automatik dalam Azure Pipelines untuk beban kerja AI  
- Penguatkuasaan polisi untuk penerapan komponen AI yang selamat  

**Amalan Dalaman Microsoft:**  
Microsoft melaksanakan amalan keselamatan rantaian bekalan yang luas di seluruh produk. Ketahui pendekatan yang terbukti dalam [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).  

## Amalan Terbaik Keselamatan Asas  

Pelaksanaan MCP mewarisi dan membina di atas postur keselamatan organisasi anda yang sedia ada. Mengukuhkan amalan keselamatan asas secara signifikan meningkatkan keselamatan keseluruhan sistem AI dan penerapan MCP.  

### Asas Keselamatan Teras  

#### **Amalan Pembangunan Selamat**  
- **Pematuhan OWASP**: Lindungi daripada kerentanan aplikasi web [OWASP Top 10](https://owasp.org/www-project-top-ten/)  
- **Perlindungan Khusus AI**: Laksanakan kawalan untuk [OWASP Top 10 untuk LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559)  
- **Pengurusan Rahsia Selamat**: Gunakan peti besi khusus untuk token, kunci API, dan data konfigurasi sensitif  
- **Penyulitan Hujung-ke-Hujung**: Laksanakan komunikasi selamat di seluruh komponen aplikasi dan aliran data  
- **Pengesahan Input**: Pengesahan ketat terhadap semua input pengguna, parameter API, dan sumber data  

#### **Pengerasan Infrastruktur**  
- **Pengesahan Multi-Faktor**: MFA wajib untuk semua akaun pentadbiran dan perkhidmatan  
- **Pengurusan Tampalan**: Penampalan automatik dan tepat waktu untuk sistem operasi, rangka kerja, dan pergantungan  
- **Integrasi Penyedia Identiti**: Pengurusan identiti berpusat melalui penyedia identiti perusahaan (Microsoft Entra ID, Active Directory)  
- **Segmentasi Rangkaian**: Pengasingan logik komponen MCP untuk mengehadkan potensi pergerakan lateral  
- **Prinsip Keistimewaan Minimum**: Keistimewaan minimum yang diperlukan untuk semua komponen sistem dan akaun  

#### **Pemantauan & Pengesanan Keselamatan**  
- **Pembalakan Komprehensif**: Pembalakan terperinci aktiviti aplikasi AI, termasuk interaksi klien-pelayan MCP  
- **Integrasi SIEM**: Pengurusan maklumat keselamatan dan acara berpusat untuk pengesanan anomali  
- **Analitik Tingkah Laku**: Pemantauan berkuasa AI untuk mengesan corak luar biasa dalam tingkah laku sistem dan pengguna  
- **Perisikan Ancaman**: Integrasi suapan ancaman luaran dan indikator kompromi (IOCs)  
- **Tindak Balas Insiden**: Prosedur yang ditetapkan untuk pengesanan, tindak balas, dan pemulihan insiden keselamatan  

#### **Seni Bina Zero Trust**  
- **Jangan Percaya, Sentiasa Sahkan**: Pengesahan berterusan pengguna, peranti, dan sambungan rangkaian  
- **Mikro-Segmentasi**: Kawalan rangkaian granular yang mengasingkan beban kerja dan perkhidmatan individu  
- **Keselamatan Berpusatkan Identiti**: Polisi keselamatan berdasarkan identiti yang disahkan dan bukannya lokasi rangkaian  
- **Penilaian Risiko Berterusan**: Penilaian postur keselamatan dinamik berdasarkan konteks dan tingkah laku semasa  
- **Akses Bersyarat**: Kawalan akses yang menyesuaikan berdasarkan faktor risiko, lokasi, dan kepercayaan peranti  

### Corak Integrasi Perusahaan  

#### **Integrasi Ekosistem Keselamatan Microsoft**  
- **Microsoft Defender for Cloud**: Pengurusan postur keselamatan awan yang komprehensif  
- **Azure Sentinel**: Keupayaan SIEM dan SOAR asli awan untuk perlindungan beban kerja AI  
- **Microsoft Entra ID**: Pengurusan identiti dan akses perusahaan dengan polisi akses bersyarat  
- **Azure Key Vault**: Pengurusan rahsia berpusat dengan sokongan modul keselamatan perkakasan (HSM)  
- **Microsoft Purview**: Tadbir urus data dan pematuhan untuk sumber data AI dan aliran kerja  

#### **Pematuhan & Tadbir Urus**  
- **Penyelarasan Peraturan**: Pastikan pelaksanaan MCP memenuhi keperluan pematuhan industri tertentu (GDPR, HIPAA, SOC 2)  
- **Pengelasan Data**: Kategorisasi dan pengendalian yang betul terhadap data sensitif yang diproses oleh sistem AI  
- **Jejak Audit**: Pembalakan komprehensif untuk pematuhan peraturan dan penyiasatan forensik  
- **Kawalan Privasi**: Pelaksanaan prinsip privasi-dalam-reka bentuk dalam seni bina sistem AI  
- **Pengurusan Perubahan**: Proses formal untuk ulasan keselamatan terhadap pengubahsuaian sistem AI  

Amalan asas ini mencipta asas keselamatan yang kukuh yang meningkatkan keberkesanan kawalan keselamatan khusus MCP dan menyediakan perlindungan komprehensif untuk aplikasi yang didorong oleh AI.  

## Pengambilan Keselamatan Utama  

- **Pendekatan Keselamatan Berlapis**: Gabungkan amalan keselamatan asas (pengkodan selamat, keistimewaan minimum, pengesahan rantaian bekalan, pemantauan berterusan) dengan kawalan khusus AI untuk perlindungan komprehensif  

- **Landskap Ancaman Khusus AI**: Sistem MCP menghadapi risiko unik termasuk suntikan prompt, keracunan alat, pembajakan sesi, masalah timbalan keliru, kerentanan passthrough token, dan keistimewaan berlebihan yang memerlukan mitigasi khusus  

- **Kecemerlangan Pengesahan & Kebenaran**: Laksanakan pengesahan yang kukuh menggunakan penyedia identiti luaran (Microsoft Entra ID), kuatkuasakan pengesahan token yang betul, dan jangan sekali-kali menerima token yang tidak dikeluarkan secara eksplisit untuk pelayan MCP anda  

- **Pencegahan Serangan AI**: Terapkan Microsoft Prompt Shields dan Azure Content Safety untuk mempertahankan daripada suntikan prompt tidak langsung dan serangan keracunan alat, sambil mengesahkan metadata alat dan memantau perubahan dinamik  

- **Keselamatan Sesi & Pengangkutan**: Gunakan ID sesi yang selamat secara kriptografi dan tidak deterministik yang diikat kepada identiti pengguna, laksanakan pengurusan kitaran hayat sesi yang betul, dan jangan sekali-kali menggunakan sesi untuk pengesahan  

- **Amalan Terbaik Keselamatan OAuth**: Cegah serangan timbalan keliru melalui persetujuan pengguna eksplisit untuk klien yang didaftarkan secara dinamik, pelaksanaan OAuth 2.1 yang betul dengan PKCE, dan pengesahan URI pengalihan yang ketat  

- **Prinsip Keselamatan Token**: Elakkan corak anti passthrough token, sahkan tuntutan penonton token, laksanakan token jangka pendek dengan putaran yang selamat, dan kekalkan sempadan kepercayaan yang jelas  

- **Keselamatan Rantaian Bekalan Komprehensif**: Perlakukan semua komponen ekosistem AI (model, penyisipan, penyedia konteks, API luaran) dengan ketegasan keselamatan yang sama seperti pergantungan perisian tradisional  

- **Evolusi Berterusan**: Kekal terkini dengan spesifikasi MCP yang berkembang pesat, sumbangkan kepada standard komuniti keselamatan, dan kekalkan postur keselamatan adaptif apabila protokol matang  

- **Integrasi Keselamatan Microsoft**: Manfaatkan ekosistem keselamatan komprehensif Microsoft (Prompt Shields, Azure Content Safety, GitHub Advanced Security, Entra ID) untuk perlindungan penerapan MCP yang dipertingkatkan  

## Sumber Komprehensif  

### **Dokumentasi Keselamatan MCP Rasmi**  
- [Spesifikasi MCP (Semasa: 2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [Amalan Terbaik Keselamatan MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [Spesifikasi Kebenaran MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  
- [Repositori GitHub MCP](https://github.com/modelcontextprotocol)  

### **Standard Keselamatan & Amalan Terbaik**  
- [Amalan Terbaik Keselamatan OAuth 2.0 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 Keselamatan Aplikasi Web](https://owasp.org/www-project-top-ten/)  
- [
### **Penyelesaian Keselamatan Microsoft**
- [Dokumentasi Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Perkhidmatan Keselamatan Kandungan Azure](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Keselamatan Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Amalan Terbaik Pengurusan Token Azure](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [Keselamatan Lanjutan GitHub](https://github.com/security/advanced-security)

### **Panduan Pelaksanaan & Tutorial**
- [Pengurusan API Azure sebagai Gerbang Pengesahan MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Pengesahan Microsoft Entra ID dengan Pelayan MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Penyimpanan dan Penyulitan Token yang Selamat (Video)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps & Keselamatan Rantaian Bekalan**
- [Keselamatan Azure DevOps](https://azure.microsoft.com/products/devops)
- [Keselamatan Azure Repos](https://azure.microsoft.com/products/devops/repos/)
- [Perjalanan Keselamatan Rantaian Bekalan Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Dokumentasi Keselamatan Tambahan**

Untuk panduan keselamatan yang menyeluruh, rujuk dokumen khusus dalam bahagian ini:

- **[Amalan Terbaik Keselamatan MCP 2025](./mcp-security-best-practices-2025.md)** - Amalan terbaik keselamatan lengkap untuk pelaksanaan MCP
- **[Pelaksanaan Keselamatan Kandungan Azure](./azure-content-safety-implementation.md)** - Contoh pelaksanaan praktikal untuk integrasi Keselamatan Kandungan Azure  
- **[Kawalan Keselamatan MCP 2025](./mcp-security-controls-2025.md)** - Kawalan keselamatan dan teknik terkini untuk pelaksanaan MCP
- **[Rujukan Pantas Amalan Terbaik MCP](./mcp-best-practices.md)** - Panduan rujukan pantas untuk amalan keselamatan MCP yang penting

---

## Apa Seterusnya

Seterusnya: [Bab 3: Memulakan](../03-GettingStarted/README.md)

**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk memastikan ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang berwibawa. Untuk maklumat penting, terjemahan manusia profesional adalah disyorkan. Kami tidak bertanggungjawab atas sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.