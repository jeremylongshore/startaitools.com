<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:03:02+00:00",
  "source_file": "changelog.md",
  "language_code": "tr"
}
-->
# Değişiklik Günlüğü: MCP for Beginners Müfredatı

Bu belge, Model Context Protocol (MCP) for Beginners müfredatında yapılan tüm önemli değişikliklerin kaydını tutar. Değişiklikler, en yeni değişiklikler en üstte olacak şekilde ters kronolojik sırayla belgelenmiştir.

## 6 Ekim 2025

### Başlangıç Bölümü Genişletmesi – Gelişmiş Sunucu Kullanımı ve Basit Kimlik Doğrulama

#### Gelişmiş Sunucu Kullanımı (03-GettingStarted/10-advanced)
- **Yeni Bölüm Eklendi**: Hem normal hem de düşük seviyeli sunucu mimarilerini kapsayan gelişmiş MCP sunucu kullanımına yönelik kapsamlı bir rehber tanıtıldı.
  - **Normal vs. Düşük Seviyeli Sunucu**: Her iki yaklaşım için Python ve TypeScript'te detaylı karşılaştırma ve kod örnekleri.
  - **Handler Tabanlı Tasarım**: Ölçeklenebilir, esnek sunucu uygulamaları için handler tabanlı araç/kaynak/istek yönetimi açıklaması.
  - **Pratik Örüntüler**: Gelişmiş özellikler ve mimariler için düşük seviyeli sunucu örüntülerinin faydalı olduğu gerçek dünya senaryoları.

#### Basit Kimlik Doğrulama (03-GettingStarted/11-simple-auth)
- **Yeni Bölüm Eklendi**: MCP sunucularında basit kimlik doğrulama uygulamak için adım adım rehber.
  - **Kimlik Doğrulama Kavramları**: Kimlik doğrulama ve yetkilendirme arasındaki farkın ve kimlik bilgisi yönetiminin net açıklaması.
  - **Temel Kimlik Doğrulama Uygulaması**: Python (Starlette) ve TypeScript (Express) ile middleware tabanlı kimlik doğrulama örüntüleri, kod örnekleriyle birlikte.
  - **Gelişmiş Güvenliğe Geçiş**: Basit kimlik doğrulama ile başlayıp OAuth 2.1 ve RBAC'a ilerleme konusunda rehberlik, gelişmiş güvenlik modüllerine referanslarla birlikte.

Bu eklemeler, daha sağlam, güvenli ve esnek MCP sunucu uygulamaları oluşturmak için pratik, uygulamalı rehberlik sağlar ve temel kavramları üretim düzeyindeki gelişmiş örüntülerle birleştirir.

## 29 Eylül 2025

### MCP Sunucu Veritabanı Entegrasyonu Laboratuvarları - Kapsamlı Uygulamalı Öğrenme Yolu

#### 11-MCPServerHandsOnLabs - Yeni Tam Veritabanı Entegrasyonu Müfredatı
- **Tam 13-Laboratuvar Öğrenme Yolu**: PostgreSQL veritabanı entegrasyonu ile üretim düzeyinde MCP sunucuları oluşturmak için kapsamlı uygulamalı müfredat eklendi.
  - **Gerçek Dünya Uygulaması**: Zava Retail analitik kullanım durumu, kurumsal düzeyde örüntüleri gösteriyor.
  - **Yapılandırılmış Öğrenme İlerlemesi**:
    - **Laboratuvarlar 00-03: Temeller** - Giriş, Temel Mimari, Güvenlik ve Çoklu Kiracılık, Ortam Kurulumu
    - **Laboratuvarlar 04-06: MCP Sunucusunu Oluşturma** - Veritabanı Tasarımı ve Şeması, MCP Sunucu Uygulaması, Araç Geliştirme  
    - **Laboratuvarlar 07-09: Gelişmiş Özellikler** - Semantik Arama Entegrasyonu, Test ve Hata Ayıklama, VS Code Entegrasyonu
    - **Laboratuvarlar 10-12: Üretim ve En İyi Uygulamalar** - Dağıtım Stratejileri, İzleme ve Görünürlük, En İyi Uygulamalar ve Optimizasyon
  - **Kurumsal Teknolojiler**: FastMCP framework, PostgreSQL ve pgvector, Azure OpenAI embeddings, Azure Container Apps, Application Insights
  - **Gelişmiş Özellikler**: Satır Düzeyi Güvenlik (RLS), semantik arama, çoklu kiracı veri erişimi, vektör gömme, gerçek zamanlı izleme

#### Terminoloji Standartlaştırma - Modülün Laboratuvara Dönüştürülmesi
- **Kapsamlı Dokümantasyon Güncellemesi**: 11-MCPServerHandsOnLabs içindeki tüm README dosyaları sistematik olarak "Modül" terminolojisinden "Laboratuvar" terminolojisine güncellendi.
  - **Bölüm Başlıkları**: Tüm 13 laboratuvar boyunca "Bu Modül Ne Kapsıyor" başlıkları "Bu Laboratuvar Ne Kapsıyor" olarak güncellendi.
  - **İçerik Açıklaması**: "Bu modül şunları sağlar..." ifadeleri "Bu laboratuvar şunları sağlar..." olarak değiştirildi.
  - **Öğrenme Hedefleri**: "Bu modülün sonunda..." ifadeleri "Bu laboratuvarın sonunda..." olarak güncellendi.
  - **Navigasyon Bağlantıları**: Tüm "Modül XX:" referansları "Laboratuvar XX:" olarak çapraz referanslarda ve navigasyonda dönüştürüldü.
  - **Tamamlanma Takibi**: "Bu modülü tamamladıktan sonra..." ifadeleri "Bu laboratuvarı tamamladıktan sonra..." olarak güncellendi.
  - **Teknik Referansların Korunması**: Yapılandırma dosyalarındaki Python modül referansları korundu (ör. `"module": "mcp_server.main"`).

#### Çalışma Kılavuzu Geliştirmesi (study_guide.md)
- **Görsel Müfredat Haritası**: "11. Veritabanı Entegrasyonu Laboratuvarları" bölümünü içeren kapsamlı laboratuvar yapısı görselleştirmesi eklendi.
- **Depo Yapısı**: On ana bölümden on bir ana bölüme güncellenerek 11-MCPServerHandsOnLabs detaylı açıklaması eklendi.
- **Öğrenme Yolu Rehberliği**: 00-11 bölümlerini kapsayan navigasyon talimatları geliştirildi.
- **Teknoloji Kapsamı**: FastMCP, PostgreSQL, Azure hizmet entegrasyonu detayları eklendi.
- **Öğrenme Çıktıları**: Üretim düzeyinde sunucu geliştirme, veritabanı entegrasyonu örüntüleri ve kurumsal güvenlik vurgulandı.

#### Ana README Yapı Geliştirmesi
- **Laboratuvar Tabanlı Terminoloji**: 11-MCPServerHandsOnLabs içindeki ana README.md, tutarlı bir şekilde "Laboratuvar" yapısını kullanacak şekilde güncellendi.
- **Öğrenme Yolu Organizasyonu**: Temel kavramlardan gelişmiş uygulamaya ve üretim dağıtımına kadar net bir ilerleme.
- **Gerçek Dünya Odaklı**: Kurumsal düzeyde örüntüler ve teknolojilerle pratik, uygulamalı öğrenme vurgusu.

### Dokümantasyon Kalitesi ve Tutarlılık İyileştirmeleri
- **Uygulamalı Öğrenme Vurgusu**: Tüm dokümantasyon boyunca pratik, laboratuvar tabanlı yaklaşım güçlendirildi.
- **Kurumsal Örüntüler Odaklı**: Üretim düzeyinde uygulamalar ve kurumsal güvenlik hususları vurgulandı.
- **Teknoloji Entegrasyonu**: Modern Azure hizmetleri ve AI entegrasyon örüntülerinin kapsamlı kapsanması.
- **Öğrenme İlerlemesi**: Temel kavramlardan üretim dağıtımına kadar net, yapılandırılmış bir yol.

## 26 Eylül 2025

### Vaka Çalışmaları Geliştirmesi - GitHub MCP Registry Entegrasyonu

#### Vaka Çalışmaları (09-CaseStudy/) - Ekosistem Geliştirme Odaklı
- **README.md**: GitHub MCP Registry vaka çalışmasıyla kapsamlı genişleme
  - **GitHub MCP Registry Vaka Çalışması**: GitHub'ın Eylül 2025'teki MCP Registry lansmanını inceleyen yeni kapsamlı vaka çalışması
    - **Sorun Analizi**: Parçalanmış MCP sunucu keşfi ve dağıtım zorluklarının detaylı incelemesi
    - **Çözüm Mimarisi**: GitHub'ın merkezi registry yaklaşımı ve tek tıkla VS Code kurulumu
    - **İş Etkisi**: Geliştirici onboarding ve üretkenlikte ölçülebilir iyileştirmeler
    - **Stratejik Değer**: Modüler ajan dağıtımı ve çapraz araç uyumluluğuna odaklanma
    - **Ekosistem Geliştirme**: Ajanik entegrasyon için temel platform olarak konumlandırma
  - **Geliştirilmiş Vaka Çalışması Yapısı**: Tüm yedi vaka çalışması, tutarlı formatlama ve kapsamlı açıklamalarla güncellendi.
    - Azure AI Seyahat Ajanları: Çoklu ajan orkestrasyonu vurgusu
    - Azure DevOps Entegrasyonu: İş akışı otomasyonu odaklı
    - Gerçek Zamanlı Dokümantasyon Alma: Python konsol istemcisi uygulaması
    - Etkileşimli Çalışma Planı Oluşturucu: Chainlit konuşma web uygulaması
    - Editör İçi Dokümantasyon: VS Code ve GitHub Copilot entegrasyonu
    - Azure API Yönetimi: Kurumsal API entegrasyon örüntüleri
    - GitHub MCP Registry: Ekosistem geliştirme ve topluluk platformu
  - **Kapsamlı Sonuç**: Yedi vaka çalışmasını kapsayan ve çeşitli MCP uygulama boyutlarını vurgulayan yeniden yazılmış sonuç bölümü
    - Kurumsal Entegrasyon, Çoklu Ajan Orkestrasyonu, Geliştirici Üretkenliği
    - Ekosistem Geliştirme, Eğitim Uygulamaları kategorizasyonu
    - Mimari örüntüler, uygulama stratejileri ve en iyi uygulamalar hakkında geliştirilmiş içgörüler
    - MCP'nin olgun, üretim düzeyinde bir protokol olarak vurgulanması

#### Çalışma Kılavuzu Güncellemeleri (study_guide.md)
- **Görsel Müfredat Haritası**: Vaka Çalışmaları bölümüne GitHub MCP Registry'yi eklemek için mindmap güncellendi.
- **Vaka Çalışmaları Açıklaması**: Genel açıklamalardan yedi kapsamlı vaka çalışmasının detaylı bir dökümüne geliştirildi.
- **Depo Yapısı**: 10. bölümü, spesifik uygulama detaylarıyla kapsamlı vaka çalışması kapsamını yansıtacak şekilde güncelledi.
- **Değişiklik Günlüğü Entegrasyonu**: GitHub MCP Registry eklemesini ve vaka çalışması geliştirmelerini belgeleyen 26 Eylül 2025 girişini ekledi.
- **Tarih Güncellemeleri**: Altbilgi zaman damgası en son revizyonu yansıtacak şekilde güncellendi (26 Eylül 2025).

### Dokümantasyon Kalitesi İyileştirmeleri
- **Tutarlılık Geliştirmesi**: Tüm yedi örnek arasında vaka çalışması formatlama ve yapı standartlaştırıldı.
- **Kapsamlı Kapsama**: Vaka çalışmaları artık kurumsal, geliştirici üretkenliği ve ekosistem geliştirme senaryolarını kapsıyor.
- **Stratejik Konumlandırma**: MCP'nin ajanik sistem dağıtımı için temel platform olarak geliştirilmiş odaklanması.
- **Kaynak Entegrasyonu**: Ek kaynaklar, GitHub MCP Registry bağlantısını içerecek şekilde güncellendi.

## 15 Eylül 2025

### Gelişmiş Konular Genişletmesi - Özel Taşıma Mekanizmaları ve Bağlam Mühendisliği

#### MCP Özel Taşıma Mekanizmaları (05-AdvancedTopics/mcp-transport/) - Yeni Gelişmiş Uygulama Rehberi
- **README.md**: Özel MCP taşıma mekanizmaları için tam uygulama rehberi
  - **Azure Event Grid Taşıma Mekanizması**: Kapsamlı sunucusuz olay odaklı taşıma uygulaması
    - Azure Functions entegrasyonu ile C#, TypeScript ve Python örnekleri
    - Ölçeklenebilir MCP çözümleri için olay odaklı mimari örüntüler
    - Webhook alıcıları ve push tabanlı mesaj işleme
  - **Azure Event Hubs Taşıma Mekanizması**: Yüksek verimli akış taşıma uygulaması
    - Düşük gecikmeli senaryolar için gerçek zamanlı akış yetenekleri
    - Bölümleme stratejileri ve kontrol noktası yönetimi
    - Mesaj gruplama ve performans optimizasyonu
  - **Kurumsal Entegrasyon Örüntüleri**: Üretim düzeyinde mimari örnekler
    - Birden fazla Azure Functions arasında dağıtılmış MCP işleme
    - Birden fazla taşıma türünü birleştiren hibrit taşıma mimarileri
    - Mesaj dayanıklılığı, güvenilirlik ve hata işleme stratejileri
  - **Güvenlik ve İzleme**: Azure Key Vault entegrasyonu ve görünürlük örüntüleri
    - Yönetilen kimlik doğrulama ve en az ayrıcalık erişimi
    - Application Insights telemetri ve performans izleme
    - Devre kesiciler ve hata toleransı örüntüleri
  - **Test Çerçeveleri**: Özel taşıma mekanizmaları için kapsamlı test stratejileri
    - Test doubles ve mocking çerçeveleri ile birim testi
    - Azure Test Containers ile entegrasyon testi
    - Performans ve yük testi hususları

#### Bağlam Mühendisliği (05-AdvancedTopics/mcp-contextengineering/) - Gelişen AI Disiplini
- **README.md**: Bağlam mühendisliği üzerine kapsamlı bir keşif
  - **Temel İlkeler**: Tam bağlam paylaşımı, eylem karar farkındalığı ve bağlam penceresi yönetimi
  - **MCP Protokol Uyumu**: MCP tasarımının bağlam mühendisliği zorluklarını nasıl ele aldığı
    - Bağlam penceresi sınırlamaları ve ilerici yükleme stratejileri
    - Alaka belirleme ve dinamik bağlam alma stratejileri
    - Çok modlu bağlam işleme ve güvenlik hususları
  - **Uygulama Yaklaşımları**: Tek iş parçacıklı ve çoklu ajan mimarileri
    - Bağlam parçalama ve önceliklendirme teknikleri
    - İlerici bağlam yükleme ve sıkıştırma stratejileri
    - Katmanlı bağlam yaklaşımları ve alma optimizasyonu
  - **Ölçüm Çerçevesi**: Bağlam etkinliği değerlendirmesi için gelişen metrikler
    - Girdi verimliliği, performans, kalite ve kullanıcı deneyimi hususları
    - Bağlam optimizasyonu için deneysel yaklaşımlar
    - Hata analizi ve iyileştirme metodolojileri

#### Müfredat Navigasyon Güncellemeleri (README.md)
- **Geliştirilmiş Modül Yapısı**: Yeni gelişmiş konuları içerecek şekilde müfredat tablosu güncellendi.
  - Bağlam Mühendisliği (5.14) ve Özel Taşıma Mekanizmaları (5.15) girişleri eklendi.
  - Tüm modüller arasında tutarlı formatlama ve navigasyon bağlantıları.
  - Mevcut içerik kapsamını yansıtacak şekilde açıklamalar güncellendi.

### Dizin Yapısı İyileştirmeleri
- **Adlandırma Standartlaştırması**: "mcp transport" "mcp-transport" olarak yeniden adlandırıldı, diğer gelişmiş konu klasörleriyle tutarlılık sağlandı.
- **İçerik Organizasyonu**: Tüm 05-AdvancedTopics klasörleri artık tutarlı bir adlandırma düzenini takip ediyor (mcp-[konu]).

### Dokümantasyon Kalitesi İyileştirmeleri
- **MCP Spesifikasyon Uyumu**: Tüm yeni içerik, mevcut MCP Spesifikasyonu 2025-06-18'e referans verir.
- **Çok Dilli Örnekler**: C#, TypeScript ve Python'da kapsamlı kod örnekleri.
- **Kurumsal Odak**: Üretim düzeyinde örüntüler ve Azure bulut entegrasyonu.
- **Görsel Dokümantasyon**: Mimari ve akış görselleştirmesi için Mermaid diyagramları.

## 18 Ağustos 2025

### Dokümantasyon Kapsamlı Güncellemesi - MCP 2025-06-18 Standartları

#### MCP Güvenlik En İyi Uygulamaları (02-Security/) - Tam Modernizasyon
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: MCP Spesifikasyonu 2025-06-18 ile uyumlu olarak tamamen yeniden yazıldı.
  - **Zorunlu Gereksinimler**: Resmi spesifikasyondan açıkça belirtilmiş MUST/MUST NOT gereksinimleri, net görsel göstergelerle eklendi.
  - **12 Temel Güvenlik Uygulaması**: 15 maddelik listeden kapsamlı güvenlik alanlarına yeniden yapılandırıldı.
    - Dış kimlik sağlayıcı entegrasyonu ile Token Güvenliği ve Kimlik Doğrulama
    - Kriptografik gereksinimlerle Oturum Yönetimi ve Taşıma Güvenliği
    - Microsoft Prompt Shields entegrasyonu ile AI'ye Özgü Tehdit Koruması

#### Gelişmiş Konular Güvenlik (05-AdvancedTopics/mcp-security/) - Üretime Hazır Uygulama
- **README.md**: Kurumsal güvenlik uygulaması için tamamen yeniden yazıldı
  - **Mevcut Spesifikasyon Uyumu**: MCP Spesifikasyonu 2025-06-18'e güncellendi, zorunlu güvenlik gereksinimleri dahil edildi
  - **Gelişmiş Kimlik Doğrulama**: Microsoft Entra ID entegrasyonu, kapsamlı .NET ve Java Spring Security örnekleriyle
  - **AI Güvenlik Entegrasyonu**: Microsoft Prompt Shields ve Azure Content Safety uygulaması, detaylı Python örnekleriyle
  - **Gelişmiş Tehdit Azaltma**: Aşağıdaki konular için kapsamlı uygulama örnekleri:
    - PKCE ve kullanıcı onayı doğrulaması ile Karışık Vekil Saldırısı Önleme
    - Hedef doğrulama ve güvenli token yönetimi ile Token Passthrough Önleme
    - Kriptografik bağlama ve davranış analizi ile Oturum Ele Geçirme Önleme
  - **Kurumsal Güvenlik Entegrasyonu**: Azure Application Insights izleme, tehdit algılama hatları ve tedarik zinciri güvenliği
  - **Uygulama Kontrol Listesi**: Microsoft güvenlik ekosisteminin avantajlarıyla açıkça belirtilmiş zorunlu ve önerilen güvenlik kontrolleri

### Dokümantasyon Kalitesi ve Standart Uyumu
- **Spesifikasyon Referansları**: Tüm referanslar MCP Spesifikasyonu 2025-06-18'e güncellendi
- **Microsoft Güvenlik Ekosistemi**: Tüm güvenlik dokümantasyonu boyunca geliştirilmiş entegrasyon rehberliği
- **Pratik Uygulama**: .NET, Java ve Python'da detaylı kod örnekleri ve kurumsal desenler eklendi
- **Kaynak Organizasyonu**: Resmi dokümantasyon, güvenlik standartları ve uygulama rehberlerinin kapsamlı kategorilendirilmesi
- **Görsel Göstergeler**: Zorunlu gereksinimler ile önerilen uygulamalar arasında net işaretlemeler

#### Temel Kavramlar (01-CoreConcepts/) - Tam Modernizasyon
- **Protokol Versiyon Güncellemesi**: MCP Spesifikasyonu 2025-06-18'e güncellendi, tarih bazlı versiyonlama (YYYY-MM-DD formatı) ile
- **Mimari İyileştirme**: Mevcut MCP mimari desenlerini yansıtacak şekilde Host, Client ve Server açıklamaları geliştirildi
  - Hostlar artık birden fazla MCP istemci bağlantısını koordine eden AI uygulamaları olarak tanımlandı
  - İstemciler, bir sunucu ile birebir ilişkiyi sürdüren protokol bağlayıcıları olarak tanımlandı
  - Sunucular, yerel ve uzak dağıtım senaryolarıyla geliştirildi
- **İlkel Yapılandırma**: Sunucu ve istemci ilkel yapılarının tamamen yeniden düzenlenmesi
  - Sunucu İlkel Yapıları: Kaynaklar (veri kaynakları), İstekler (şablonlar), Araçlar (çalıştırılabilir fonksiyonlar) detaylı açıklamalar ve örneklerle
  - İstemci İlkel Yapıları: Örnekleme (LLM tamamlama), Bilgi Toplama (kullanıcı girdisi), Günlükleme (hata ayıklama/izleme)
  - Mevcut keşif (`*/list`), alma (`*/get`) ve çalıştırma (`*/call`) yöntem desenleriyle güncellendi
- **Protokol Mimarisi**: İki katmanlı mimari modeli tanıtıldı
  - Veri Katmanı: JSON-RPC 2.0 temeli, yaşam döngüsü yönetimi ve ilkel yapılar
  - Taşıma Katmanı: STDIO (yerel) ve Streamable HTTP ile SSE (uzaktan) taşıma mekanizmaları
- **Güvenlik Çerçevesi**: Açık kullanıcı onayı, veri gizliliği koruması, araç çalıştırma güvenliği ve taşıma katmanı güvenliği dahil kapsamlı güvenlik ilkeleri
- **İletişim Desenleri**: Protokol mesajları, başlatma, keşif, çalıştırma ve bildirim akışlarını gösterecek şekilde güncellendi
- **Kod Örnekleri**: Mevcut MCP SDK desenlerini yansıtacak şekilde çok dilli örnekler (.NET, Java, Python, JavaScript) yenilendi

#### Güvenlik (02-Security/) - Kapsamlı Güvenlik Revizyonu  
- **Standart Uyumu**: MCP Spesifikasyonu 2025-06-18 güvenlik gereksinimleriyle tam uyum
- **Kimlik Doğrulama Evrimi**: Özel OAuth sunucularından harici kimlik sağlayıcı delegasyonuna (Microsoft Entra ID) geçiş belgelenmiştir
- **AI'ye Özgü Tehdit Analizi**: Modern AI saldırı vektörlerinin kapsamlı analizi
  - Gerçek dünya örnekleriyle detaylı prompt enjeksiyon saldırı senaryoları
  - Araç zehirleme mekanizmaları ve "halı çekme" saldırı desenleri
  - Bağlam penceresi zehirlenmesi ve model karışıklığı saldırıları
- **Microsoft AI Güvenlik Çözümleri**: Microsoft güvenlik ekosisteminin kapsamlı kapsaması
  - Gelişmiş algılama, vurgulama ve ayırıcı tekniklerle AI Prompt Shields
  - Azure Content Safety entegrasyon desenleri
  - Tedarik zinciri koruması için GitHub Advanced Security
- **Gelişmiş Tehdit Azaltma**: Detaylı güvenlik kontrolleri
  - MCP'ye özgü saldırı senaryoları ve kriptografik oturum kimliği gereksinimleriyle oturum ele geçirme
  - MCP proxy senaryolarında açık onay gereksinimleriyle karışık vekil sorunları
  - Zorunlu doğrulama kontrolleriyle token passthrough açıkları
- **Tedarik Zinciri Güvenliği**: Temel modeller, gömme hizmetleri, bağlam sağlayıcılar ve üçüncü taraf API'ler dahil genişletilmiş AI tedarik zinciri kapsamı
- **Temel Güvenlik**: Sıfır güven mimarisi ve Microsoft güvenlik ekosistemi dahil kurumsal güvenlik desenleriyle geliştirilmiş entegrasyon
- **Kaynak Organizasyonu**: Türüne göre (Resmi Belgeler, Standartlar, Araştırma, Microsoft Çözümleri, Uygulama Rehberleri) kapsamlı kaynak bağlantıları kategorilendirildi

### Dokümantasyon Kalitesi İyileştirmeleri
- **Yapılandırılmış Öğrenme Hedefleri**: Belirli, uygulanabilir sonuçlarla geliştirilmiş öğrenme hedefleri
- **Çapraz Referanslar**: İlgili güvenlik ve temel kavram konuları arasında bağlantılar eklendi
- **Güncel Bilgiler**: Tüm tarih referansları ve spesifikasyon bağlantıları güncel standartlara göre güncellendi
- **Uygulama Rehberliği**: Her iki bölümde de belirli, uygulanabilir uygulama yönergeleri eklendi

## 16 Temmuz 2025

### README ve Navigasyon İyileştirmeleri
- README.md'de müfredat navigasyonu tamamen yeniden tasarlandı
- `<details>` etiketleri daha erişilebilir tablo tabanlı formatla değiştirildi
- Yeni "alternative_layouts" klasöründe alternatif düzen seçenekleri oluşturuldu
- Kart tabanlı, sekmeli ve akordeon tarzı navigasyon örnekleri eklendi
- Depo yapısı bölümü en son dosyaları içerecek şekilde güncellendi
- "Bu Müfredat Nasıl Kullanılır" bölümüne net öneriler eklendi
- MCP spesifikasyon bağlantıları doğru URL'lere yönlendirilmek üzere güncellendi
- Müfredat yapısına Bağlam Mühendisliği bölümü (5.14) eklendi

### Çalışma Kılavuzu Güncellemeleri
- Çalışma kılavuzu mevcut depo yapısına uyacak şekilde tamamen revize edildi
- MCP İstemcileri ve Araçları ile Popüler MCP Sunucuları için yeni bölümler eklendi
- Görsel Müfredat Haritası tüm konuları doğru şekilde yansıtacak şekilde güncellendi
- Gelişmiş Konular açıklamaları tüm özel alanları kapsayacak şekilde geliştirildi
- Gerçek örnekleri yansıtacak şekilde Vaka Çalışmaları bölümü güncellendi
- Bu kapsamlı değişiklik günlüğü eklendi

### Topluluk Katkıları (06-CommunityContributions/)
- Görüntü oluşturma için MCP sunucuları hakkında detaylı bilgiler eklendi
- VSCode'da Claude kullanımı için kapsamlı bir bölüm eklendi
- Cline terminal istemcisi kurulum ve kullanım talimatları eklendi
- MCP istemci bölümü tüm popüler istemci seçeneklerini içerecek şekilde güncellendi
- Daha doğru kod örnekleriyle katkı örnekleri geliştirildi

### Gelişmiş Konular (05-AdvancedTopics/)
- Tüm özel konu klasörleri tutarlı adlandırma ile düzenlendi
- Bağlam mühendisliği materyalleri ve örnekleri eklendi
- Foundry ajan entegrasyonu dokümantasyonu eklendi
- Entra ID güvenlik entegrasyonu dokümantasyonu geliştirildi

## 11 Haziran 2025

### İlk Oluşturma
- MCP for Beginners müfredatının ilk versiyonu yayınlandı
- Tüm 10 ana bölüm için temel yapı oluşturuldu
- Navigasyon için Görsel Müfredat Haritası uygulandı
- Birden fazla programlama dilinde örnek projeler eklendi

### Başlarken (03-GettingStarted/)
- İlk sunucu uygulama örnekleri oluşturuldu
- İstemci geliştirme rehberliği eklendi
- LLM istemci entegrasyon talimatları dahil edildi
- VS Code entegrasyon dokümantasyonu eklendi
- Server-Sent Events (SSE) sunucu örnekleri uygulandı

### Temel Kavramlar (01-CoreConcepts/)
- İstemci-sunucu mimarisi detaylı şekilde açıklandı
- Anahtar protokol bileşenleri hakkında dokümantasyon oluşturuldu
- MCP'deki mesajlaşma desenleri belgelenmiştir

## 23 Mayıs 2025

### Depo Yapısı
- Temel klasör yapısıyla depo başlatıldı
- Her ana bölüm için README dosyaları oluşturuldu
- Çeviri altyapısı kuruldu
- Görsel varlıklar ve diyagramlar eklendi

### Dokümantasyon
- Müfredat genel görünümüyle ilk README.md oluşturuldu
- CODE_OF_CONDUCT.md ve SECURITY.md eklendi
- Yardım alma rehberiyle SUPPORT.md kuruldu
- İlk çalışma kılavuzu yapısı oluşturuldu

## 15 Nisan 2025

### Planlama ve Çerçeve
- MCP for Beginners müfredatı için ilk planlama yapıldı
- Öğrenme hedefleri ve hedef kitle tanımlandı
- Müfredatın 10 bölümlük yapısı taslak olarak belirlendi
- Örnekler ve vaka çalışmaları için kavramsal çerçeve geliştirildi
- Anahtar kavramlar için ilk prototip örnekler oluşturuldu

---

**Feragatname**:  
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba göstersek de, otomatik çeviriler hata veya yanlışlıklar içerebilir. Belgenin orijinal dili, yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımından kaynaklanan yanlış anlamalar veya yanlış yorumlamalar için sorumluluk kabul edilmez.