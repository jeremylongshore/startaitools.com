<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T17:51:51+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "tr"
}
-->
# MCP Güvenlik En İyi Uygulamaları - Ağustos 2025 Güncellemesi

> **Önemli**: Bu belge, en son [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) güvenlik gereksinimlerini ve resmi [MCP Güvenlik En İyi Uygulamaları](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) rehberini yansıtmaktadır. Her zaman en güncel rehberlik için mevcut spesifikasyona başvurun.

## MCP Uygulamaları için Temel Güvenlik Uygulamaları

Model Context Protocol, geleneksel yazılım güvenliğinin ötesine geçen benzersiz güvenlik zorlukları sunar. Bu uygulamalar, temel güvenlik gereksinimlerini ve MCP'ye özgü tehditleri ele alır; bunlar arasında prompt enjeksiyonu, araç zehirlenmesi, oturum ele geçirme, karışık vekil sorunları ve token geçişi açıkları bulunur.

### **ZORUNLU Güvenlik Gereksinimleri**

**MCP Spesifikasyonundan Kritik Gereksinimler:**

> **MUST NOT**: MCP sunucuları, MCP sunucusu için açıkça verilmemiş hiçbir token'ı kabul etmemelidir.  
> 
> **MUST**: Yetkilendirme uygulayan MCP sunucuları, tüm gelen istekleri doğrulamalıdır.  
>  
> **MUST NOT**: MCP sunucuları, kimlik doğrulama için oturumları kullanmamalıdır.  
>
> **MUST**: Statik istemci kimlikleri kullanan MCP proxy sunucuları, her dinamik olarak kaydedilen istemci için kullanıcı onayı almalıdır.

---

## 1. **Token Güvenliği ve Kimlik Doğrulama**

**Kimlik Doğrulama ve Yetkilendirme Kontrolleri:**
   - **Titiz Yetkilendirme İncelemesi**: MCP sunucusu yetkilendirme mantığının kapsamlı denetimlerini yaparak yalnızca amaçlanan kullanıcıların ve istemcilerin kaynaklara erişmesini sağlayın.
   - **Harici Kimlik Sağlayıcı Entegrasyonu**: Özel kimlik doğrulama uygulamak yerine Microsoft Entra ID gibi tanınmış kimlik sağlayıcıları kullanın.
   - **Token Hedef Doğrulaması**: Token'ların MCP sunucunuz için açıkça verildiğini her zaman doğrulayın - yukarı akış token'larını asla kabul etmeyin.
   - **Doğru Token Yaşam Döngüsü**: Güvenli token döndürme, son kullanma politikaları uygulayın ve token tekrar saldırılarını önleyin.

**Korunan Token Depolama:**
   - Tüm gizli bilgiler için Azure Key Vault veya benzeri güvenli kimlik bilgisi depolarını kullanın.
   - Token'ları hem bekleme hem de aktarım sırasında şifreleyin.
   - Yetkisiz erişim için düzenli kimlik bilgisi döndürme ve izleme uygulayın.

## 2. **Oturum Yönetimi ve Taşıma Güvenliği**

**Güvenli Oturum Uygulamaları:**
   - **Kriptografik Olarak Güvenli Oturum Kimlikleri**: Güvenli rastgele sayı üreteçleriyle oluşturulan güvenli, belirlenemez oturum kimlikleri kullanın.
   - **Kullanıcıya Özgü Bağlama**: Oturum kimliklerini `<user_id>:<session_id>` gibi formatlarla kullanıcı kimliklerine bağlayarak çapraz kullanıcı oturum kötüye kullanımını önleyin.
   - **Oturum Yaşam Döngüsü Yönetimi**: Uygun son kullanma, döndürme ve geçersiz kılma uygulayarak açık pencereleri sınırlayın.
   - **HTTPS/TLS Zorunluluğu**: Oturum kimliği ele geçirmeyi önlemek için tüm iletişimde HTTPS zorunlu kılın.

**Taşıma Katmanı Güvenliği:**
   - TLS 1.3'ü mümkün olduğunca doğru sertifika yönetimiyle yapılandırın.
   - Kritik bağlantılar için sertifika sabitleme uygulayın.
   - Düzenli sertifika döndürme ve geçerlilik doğrulaması yapın.

## 3. **AI'ye Özgü Tehdit Koruması** 🤖

**Prompt Enjeksiyon Savunması:**
   - **Microsoft Prompt Shields**: Kötü niyetli talimatların gelişmiş algılanması ve filtrelenmesi için AI Prompt Shields kullanın.
   - **Girdi Temizleme**: Enjeksiyon saldırılarını ve karışık vekil sorunlarını önlemek için tüm girdileri doğrulayın ve temizleyin.
   - **İçerik Sınırları**: Güvenilir talimatlar ile harici içerik arasında ayrım yapmak için ayırıcı ve veri işaretleme sistemleri kullanın.

**Araç Zehirlenmesini Önleme:**
   - **Araç Meta Veri Doğrulaması**: Araç tanımları için bütünlük kontrolleri uygulayın ve beklenmedik değişiklikleri izleyin.
   - **Dinamik Araç İzleme**: Çalışma zamanı davranışını izleyin ve beklenmedik yürütme desenleri için uyarı sistemleri kurun.
   - **Onay İş Akışları**: Araç değişiklikleri ve yetenek değişiklikleri için açık kullanıcı onayı gerektirin.

## 4. **Erişim Kontrolü ve İzinler**

**En Az Ayrıcalık İlkesi:**
   - MCP sunucularına yalnızca amaçlanan işlevsellik için gereken minimum izinleri verin.
   - İnce ayrıntılı izinlerle rol tabanlı erişim kontrolü (RBAC) uygulayın.
   - Düzenli izin incelemeleri ve ayrıcalık yükseltme için sürekli izleme yapın.

**Çalışma Zamanı İzin Kontrolleri:**
   - Kaynak tükenmesi saldırılarını önlemek için kaynak sınırları uygulayın.
   - Araç yürütme ortamları için konteyner izolasyonu kullanın.
   - Yönetim işlevleri için tam zamanında erişim uygulayın.

## 5. **İçerik Güvenliği ve İzleme**

**İçerik Güvenliği Uygulaması:**
   - **Azure İçerik Güvenliği Entegrasyonu**: Zararlı içerik, jailbreak girişimleri ve politika ihlallerini algılamak için Azure İçerik Güvenliği kullanın.
   - **Davranışsal Analiz**: MCP sunucusu ve araç yürütme sırasında anormallikleri algılamak için çalışma zamanı davranış izleme uygulayın.
   - **Kapsamlı Günlükleme**: Tüm kimlik doğrulama girişimlerini, araç çağrılarını ve güvenlik olaylarını güvenli, değiştirilemez bir depoda kaydedin.

**Sürekli İzleme:**
   - Şüpheli desenler ve yetkisiz erişim girişimleri için gerçek zamanlı uyarılar.
   - Merkezi güvenlik olay yönetimi için SIEM sistemleriyle entegrasyon.
   - MCP uygulamalarının düzenli güvenlik denetimleri ve penetrasyon testleri.

## 6. **Tedarik Zinciri Güvenliği**

**Bileşen Doğrulaması:**
   - **Bağımlılık Taraması**: Tüm yazılım bağımlılıkları ve AI bileşenleri için otomatik güvenlik açığı taraması kullanın.
   - **Kaynak Doğrulaması**: Modellerin, veri kaynaklarının ve harici hizmetlerin kökenini, lisansını ve bütünlüğünü doğrulayın.
   - **İmzalı Paketler**: Kriptografik olarak imzalanmış paketler kullanın ve dağıtımdan önce imzaları doğrulayın.

**Güvenli Geliştirme Hattı:**
   - **GitHub Gelişmiş Güvenlik**: Gizli tarama, bağımlılık analizi ve CodeQL statik analiz uygulayın.
   - **CI/CD Güvenliği**: Otomatik dağıtım hatlarında güvenlik doğrulamasını entegre edin.
   - **Eser Bütünlüğü**: Dağıtılan eserler ve yapılandırmalar için kriptografik doğrulama uygulayın.

## 7. **OAuth Güvenliği ve Karışık Vekil Önleme**

**OAuth 2.1 Uygulaması:**
   - **PKCE Uygulaması**: Tüm yetkilendirme istekleri için Proof Key for Code Exchange (PKCE) kullanın.
   - **Açık Onay**: Karışık vekil saldırılarını önlemek için her dinamik olarak kaydedilen istemci için kullanıcı onayı alın.
   - **Yönlendirme URI Doğrulaması**: Yönlendirme URI'leri ve istemci tanımlayıcılarının sıkı doğrulamasını uygulayın.

**Proxy Güvenliği:**
   - Statik istemci kimliği istismarları yoluyla yetkilendirme atlamayı önleyin.
   - Üçüncü taraf API erişimi için uygun onay iş akışlarını uygulayın.
   - Yetkilendirme kodu hırsızlığı ve yetkisiz API erişimini izleyin.

## 8. **Olay Müdahalesi ve Kurtarma**

**Hızlı Müdahale Yetkinlikleri:**
   - **Otomatik Müdahale**: Kimlik bilgisi döndürme ve tehdit sınırlama için otomatik sistemler uygulayın.
   - **Geri Alma Prosedürleri**: Bilinen iyi yapılandırmalara ve bileşenlere hızla geri dönme yeteneği.
   - **Adli Yetkinlikler**: Olay soruşturması için ayrıntılı denetim izleri ve günlükleme.

**İletişim ve Koordinasyon:**
   - Güvenlik olayları için açık yükseltme prosedürleri.
   - Kurumsal olay müdahale ekipleriyle entegrasyon.
   - Düzenli güvenlik olay simülasyonları ve masa başı tatbikatları.

## 9. **Uyumluluk ve Yönetim**

**Yasal Uyumluluk:**
   - MCP uygulamalarının sektör spesifik gereksinimleri (GDPR, HIPAA, SOC 2) karşılamasını sağlayın.
   - AI veri işleme için veri sınıflandırma ve gizlilik kontrolleri uygulayın.
   - Uyumluluk denetimi için kapsamlı belgeler tutun.

**Değişiklik Yönetimi:**
   - Tüm MCP sistem değişiklikleri için resmi güvenlik inceleme süreçleri.
   - Yapılandırma değişiklikleri için sürüm kontrolü ve onay iş akışları.
   - Düzenli uyumluluk değerlendirmeleri ve boşluk analizleri.

## 10. **Gelişmiş Güvenlik Kontrolleri**

**Sıfır Güven Mimarisi:**
   - **Asla Güvenme, Her Zaman Doğrula**: Kullanıcıların, cihazların ve bağlantıların sürekli doğrulanması.
   - **Mikro Segmentasyon**: Bireysel MCP bileşenlerini izole eden ayrıntılı ağ kontrolleri.
   - **Koşullu Erişim**: Mevcut bağlam ve davranışa uyum sağlayan risk tabanlı erişim kontrolleri.

**Çalışma Zamanı Uygulama Koruması:**
   - **Çalışma Zamanı Uygulama Kendini Koruma (RASP)**: Gerçek zamanlı tehdit algılama için RASP tekniklerini dağıtın.
   - **Uygulama Performans İzleme**: Saldırıları gösterebilecek performans anormalliklerini izleyin.
   - **Dinamik Güvenlik Politikaları**: Mevcut tehdit ortamına dayalı olarak uyum sağlayan güvenlik politikaları uygulayın.

## 11. **Microsoft Güvenlik Ekosistemi Entegrasyonu**

**Kapsamlı Microsoft Güvenliği:**
   - **Microsoft Defender for Cloud**: MCP iş yükleri için bulut güvenlik duruş yönetimi.
   - **Azure Sentinel**: Gelişmiş tehdit algılama için bulut tabanlı SIEM ve SOAR yetenekleri.
   - **Microsoft Purview**: AI iş akışları ve veri kaynakları için veri yönetimi ve uyumluluk.

**Kimlik ve Erişim Yönetimi:**
   - **Microsoft Entra ID**: Koşullu erişim politikalarıyla kurumsal kimlik yönetimi.
   - **Ayrıcalıklı Kimlik Yönetimi (PIM)**: Yönetim işlevleri için tam zamanında erişim ve onay iş akışları.
   - **Kimlik Koruma**: Risk tabanlı koşullu erişim ve otomatik tehdit yanıtı.

## 12. **Sürekli Güvenlik Evrimi**

**Güncel Kalma:**
   - **Spesifikasyon İzleme**: MCP spesifikasyon güncellemelerinin ve güvenlik rehberliği değişikliklerinin düzenli olarak gözden geçirilmesi.
   - **Tehdit İstihbaratı**: AI'ye özgü tehdit akışlarının ve tehlike göstergelerinin entegrasyonu.
   - **Güvenlik Topluluğu Katılımı**: MCP güvenlik topluluğuna aktif katılım ve güvenlik açığı bildirim programları.

**Uyarlanabilir Güvenlik:**
   - **Makine Öğrenimi Güvenliği**: Yeni saldırı desenlerini tanımlamak için ML tabanlı anomali algılama kullanın.
   - **Tahminsel Güvenlik Analitiği**: Proaktif tehdit tanımlama için tahminsel modeller uygulayın.
   - **Güvenlik Otomasyonu**: Tehdit istihbaratı ve spesifikasyon değişikliklerine dayalı olarak otomatik güvenlik politikası güncellemeleri.

---

## **Kritik Güvenlik Kaynakları**

### **Resmi MCP Belgeleri**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)
- [MCP Güvenlik En İyi Uygulamaları](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)
- [MCP Yetkilendirme Spesifikasyonu](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)

### **Microsoft Güvenlik Çözümleri**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure İçerik Güvenliği](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID Güvenliği](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [GitHub Gelişmiş Güvenlik](https://github.com/security/advanced-security)

### **Güvenlik Standartları**
- [OAuth 2.0 Güvenlik En İyi Uygulamaları (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [OWASP Büyük Dil Modelleri için İlk 10](https://genai.owasp.org/)
- [NIST AI Risk Yönetimi Çerçevesi](https://www.nist.gov/itl/ai-risk-management-framework)

### **Uygulama Rehberleri**
- [Azure API Yönetimi MCP Kimlik Doğrulama Geçidi](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Microsoft Entra ID ile MCP Sunucuları](https://den.dev/blog/mcp-server-auth-entra-id-session/)

---

> **Güvenlik Uyarısı**: MCP güvenlik uygulamaları hızla gelişmektedir. Uygulamadan önce her zaman mevcut [MCP spesifikasyonu](https://spec.modelcontextprotocol.io/) ve [resmi güvenlik belgeleri](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) ile doğrulayın.

**Feragatname**:  
Bu belge, [Co-op Translator](https://github.com/Azure/co-op-translator) adlı yapay zeka çeviri hizmeti kullanılarak çevrilmiştir. Doğruluk için çaba göstersek de, otomatik çevirilerin hata veya yanlışlıklar içerebileceğini lütfen unutmayın. Belgenin orijinal dili, yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımından kaynaklanan yanlış anlama veya yanlış yorumlamalardan sorumlu değiliz.