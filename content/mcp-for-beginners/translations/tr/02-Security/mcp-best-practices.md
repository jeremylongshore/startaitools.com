<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T17:56:02+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "tr"
}
-->
# MCP Güvenlik En İyi Uygulamaları 2025

Bu kapsamlı rehber, **MCP Specification 2025-06-18** ve mevcut endüstri standartlarına dayalı olarak Model Context Protocol (MCP) sistemlerini uygulamak için gerekli güvenlik en iyi uygulamalarını özetlemektedir. Bu uygulamalar, hem geleneksel güvenlik endişelerini hem de MCP dağıtımlarına özgü yapay zeka tehditlerini ele alır.

## Kritik Güvenlik Gereksinimleri

### Zorunlu Güvenlik Kontrolleri (MUST Gereksinimleri)

1. **Token Doğrulama**: MCP sunucuları, kendileri için açıkça verilmemiş tokenları **KABUL ETMEMELİDİR**.
2. **Yetkilendirme Doğrulaması**: Yetkilendirme uygulayan MCP sunucuları, gelen tüm istekleri doğrulamalı ve kimlik doğrulama için oturumları **KULLANMAMALIDIR**.
3. **Kullanıcı Onayı**: Statik istemci kimlikleri kullanan MCP proxy sunucuları, her dinamik olarak kaydedilen istemci için açık kullanıcı onayı almalıdır.
4. **Güvenli Oturum Kimlikleri**: MCP sunucuları, güvenli rastgele sayı üreteçleriyle oluşturulan kriptografik olarak güvenli, belirlenemez oturum kimlikleri kullanmalıdır.

## Temel Güvenlik Uygulamaları

### 1. Girdi Doğrulama ve Temizleme
- **Kapsamlı Girdi Doğrulama**: Enjeksiyon saldırılarını, karışık vekil problemlerini ve istem enjeksiyonu açıklarını önlemek için tüm girdileri doğrulayın ve temizleyin.
- **Parametre Şema Uygulaması**: Tüm araç parametreleri ve API girdileri için sıkı JSON şema doğrulaması uygulayın.
- **İçerik Filtreleme**: İstem ve yanıtlarındaki kötü niyetli içeriği filtrelemek için Microsoft Prompt Shields ve Azure Content Safety kullanın.
- **Çıktı Temizleme**: Kullanıcılara veya alt sistemlere sunmadan önce tüm model çıktısını doğrulayın ve temizleyin.

### 2. Kimlik Doğrulama ve Yetkilendirme Mükemmelliği  
- **Harici Kimlik Sağlayıcılar**: Özel kimlik doğrulama uygulamak yerine Microsoft Entra ID, OAuth 2.1 sağlayıcıları gibi tanınmış kimlik sağlayıcılara yetki verin.
- **İnce Ayrıntılı İzinler**: En az ayrıcalık ilkesine uygun olarak araç bazında ayrıntılı izinler uygulayın.
- **Token Yaşam Döngüsü Yönetimi**: Güvenli döngü ve uygun hedef doğrulama ile kısa ömürlü erişim tokenları kullanın.
- **Çok Faktörlü Kimlik Doğrulama**: Tüm yönetim erişimi ve hassas işlemler için MFA gerektirir.

### 3. Güvenli İletişim Protokolleri
- **Taşıma Katmanı Güvenliği**: Tüm MCP iletişimleri için doğru sertifika doğrulaması ile HTTPS/TLS 1.3 kullanın.
- **Uçtan Uca Şifreleme**: Transit ve bekleyen çok hassas veriler için ek şifreleme katmanları uygulayın.
- **Sertifika Yönetimi**: Otomatik yenileme süreçleri ile uygun sertifika yaşam döngüsü yönetimini sürdürün.
- **Protokol Sürüm Uygulaması**: Doğru sürüm müzakeresi ile mevcut MCP protokol sürümünü (2025-06-18) kullanın.

### 4. Gelişmiş Hız Sınırlama ve Kaynak Koruma
- **Çok Katmanlı Hız Sınırlama**: Kötüye kullanımı önlemek için kullanıcı, oturum, araç ve kaynak seviyelerinde hız sınırlama uygulayın.
- **Uyarlanabilir Hız Sınırlama**: Kullanım modellerine ve tehdit göstergelerine uyum sağlayan makine öğrenimi tabanlı hız sınırlama kullanın.
- **Kaynak Kota Yönetimi**: Hesaplama kaynakları, bellek kullanımı ve yürütme süresi için uygun sınırlar belirleyin.
- **DDoS Koruması**: Kapsamlı DDoS koruma ve trafik analiz sistemleri dağıtın.

### 5. Kapsamlı Günlükleme ve İzleme
- **Yapılandırılmış Denetim Günlüğü**: Tüm MCP işlemleri, araç yürütmeleri ve güvenlik olayları için ayrıntılı, aranabilir günlükler uygulayın.
- **Gerçek Zamanlı Güvenlik İzleme**: MCP iş yükleri için AI destekli anomali algılama ile SIEM sistemleri dağıtın.
- **Gizlilik Uyumluluğu Günlüğü**: Veri gizliliği gereksinimlerine ve düzenlemelerine saygı göstererek güvenlik olaylarını kaydedin.
- **Olay Yanıtı Entegrasyonu**: Günlükleme sistemlerini otomatik olay yanıtı iş akışlarına bağlayın.

### 6. Gelişmiş Güvenli Depolama Uygulamaları
- **Donanım Güvenlik Modülleri**: Kritik kriptografik işlemler için HSM destekli anahtar depolama (Azure Key Vault, AWS CloudHSM) kullanın.
- **Şifreleme Anahtar Yönetimi**: Şifreleme anahtarları için uygun anahtar döndürme, ayrım ve erişim kontrolleri uygulayın.
- **Gizli Bilgi Yönetimi**: Tüm API anahtarlarını, tokenları ve kimlik bilgilerini özel gizli bilgi yönetim sistemlerinde saklayın.
- **Veri Sınıflandırması**: Verileri hassasiyet seviyelerine göre sınıflandırın ve uygun koruma önlemleri uygulayın.

### 7. Gelişmiş Token Yönetimi
- **Token Geçişini Önleme**: Güvenlik kontrollerini atlayan token geçişi modellerini açıkça yasaklayın.
- **Hedef Doğrulama**: Token hedef iddialarının MCP sunucu kimliğiyle eşleştiğini her zaman doğrulayın.
- **İddia Tabanlı Yetkilendirme**: Token iddialarına ve kullanıcı özelliklerine dayalı ayrıntılı yetkilendirme uygulayın.
- **Token Bağlama**: Tokenları uygun olduğunda belirli oturumlara, kullanıcılara veya cihazlara bağlayın.

### 8. Güvenli Oturum Yönetimi
- **Kriptografik Oturum Kimlikleri**: Tahmin edilebilir diziler yerine kriptografik olarak güvenli rastgele sayı üreteçleri kullanarak oturum kimlikleri oluşturun.
- **Kullanıcıya Özgü Bağlama**: Oturum kimliklerini `<user_id>:<session_id>` gibi güvenli formatlar kullanarak kullanıcıya özgü bilgilere bağlayın.
- **Oturum Yaşam Döngüsü Kontrolleri**: Uygun oturum süresi dolma, döndürme ve geçersiz kılma mekanizmaları uygulayın.
- **Oturum Güvenlik Başlıkları**: Oturum koruması için uygun HTTP güvenlik başlıklarını kullanın.

### 9. Yapay Zeka Özel Güvenlik Kontrolleri
- **İstem Enjeksiyonu Savunması**: Microsoft Prompt Shields ile spot ışığı, sınırlayıcılar ve veri işaretleme tekniklerini dağıtın.
- **Araç Zehirlenmesini Önleme**: Araç meta verilerini doğrulayın, dinamik değişiklikleri izleyin ve araç bütünlüğünü doğrulayın.
- **Model Çıktı Doğrulaması**: Model çıktısını veri sızıntısı, zararlı içerik veya güvenlik politikası ihlalleri açısından tarayın.
- **Bağlam Penceresi Koruması**: Bağlam penceresi zehirlenmesini ve manipülasyon saldırılarını önlemek için kontroller uygulayın.

### 10. Araç Yürütme Güvenliği
- **Yürütme Sandboxing**: Araç yürütmelerini kaynak sınırlarıyla konteynerize edilmiş, izole edilmiş ortamlarda çalıştırın.
- **Ayrıcalık Ayrımı**: Araçları minimum gerekli ayrıcalıklarla ve ayrı hizmet hesaplarıyla çalıştırın.
- **Ağ İzolasyonu**: Araç yürütme ortamları için ağ segmentasyonu uygulayın.
- **Yürütme İzleme**: Araç yürütmesini anormal davranış, kaynak kullanımı ve güvenlik ihlalleri açısından izleyin.

### 11. Sürekli Güvenlik Doğrulaması
- **Otomatik Güvenlik Testi**: GitHub Advanced Security gibi araçlarla güvenlik testini CI/CD hatlarına entegre edin.
- **Güvenlik Açığı Yönetimi**: AI modelleri ve harici hizmetler dahil tüm bağımlılıkları düzenli olarak tarayın.
- **Penetrasyon Testi**: Özellikle MCP uygulamalarını hedef alan düzenli güvenlik değerlendirmeleri yapın.
- **Güvenlik Kod İncelemeleri**: MCP ile ilgili tüm kod değişiklikleri için zorunlu güvenlik incelemeleri uygulayın.

### 12. Yapay Zeka için Tedarik Zinciri Güvenliği
- **Bileşen Doğrulaması**: Tüm yapay zeka bileşenlerinin (modeller, gömüler, API'ler) kökenini, bütünlüğünü ve güvenliğini doğrulayın.
- **Bağımlılık Yönetimi**: Güvenlik açığı takibi ile tüm yazılım ve yapay zeka bağımlılıklarının güncel envanterlerini tutun.
- **Güvenilir Depolar**: Tüm yapay zeka modelleri, kütüphaneleri ve araçları için doğrulanmış, güvenilir kaynaklar kullanın.
- **Tedarik Zinciri İzleme**: Yapay zeka hizmet sağlayıcılarında ve model depolarında meydana gelen ihlalleri sürekli izleyin.

## Gelişmiş Güvenlik Modelleri

### MCP için Sıfır Güven Mimarisi
- **Asla Güvenme, Her Zaman Doğrula**: Tüm MCP katılımcıları için sürekli doğrulama uygulayın.
- **Mikro Segmentasyon**: MCP bileşenlerini ayrıntılı ağ ve kimlik kontrolleriyle izole edin.
- **Koşullu Erişim**: Bağlama ve davranışa uyum sağlayan risk tabanlı erişim kontrolleri uygulayın.
- **Sürekli Risk Değerlendirmesi**: Mevcut tehdit göstergelerine dayalı olarak güvenlik duruşunu dinamik olarak değerlendirin.

### Gizliliği Koruyan Yapay Zeka Uygulaması
- **Veri Minimizasyonu**: Her MCP işlemi için yalnızca gerekli minimum veriyi açığa çıkarın.
- **Diferansiyel Gizlilik**: Hassas veri işleme için gizliliği koruyan teknikler uygulayın.
- **Homomorfik Şifreleme**: Şifrelenmiş veriler üzerinde güvenli hesaplama için gelişmiş şifreleme teknikleri kullanın.
- **Federated Learning**: Veri yerelliğini ve gizliliğini koruyan dağıtılmış öğrenme yaklaşımlarını uygulayın.

### Yapay Zeka Sistemleri için Olay Yanıtı
- **Yapay Zeka Özel Olay Prosedürleri**: Yapay zeka ve MCP'ye özgü tehditlere yönelik olay yanıt prosedürleri geliştirin.
- **Otomatik Yanıt**: Yaygın yapay zeka güvenlik olayları için otomatik sınırlama ve iyileştirme uygulayın.
- **Adli Yetkinlikler**: Yapay zeka sistem ihlalleri ve veri sızıntıları için adli hazırlık sağlayın.
- **Kurtarma Prosedürleri**: Yapay zeka model zehirlenmesi, istem enjeksiyonu saldırıları ve hizmet ihlallerinden kurtulma prosedürleri oluşturun.

## Uygulama Kaynakları ve Standartlar

### Resmi MCP Belgeleri
- [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Mevcut MCP protokol spesifikasyonu
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Resmi güvenlik rehberi
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Kimlik doğrulama ve yetkilendirme modelleri
- [MCP Transport Security](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Taşıma katmanı güvenlik gereksinimleri

### Microsoft Güvenlik Çözümleri
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Gelişmiş istem enjeksiyonu koruması
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Kapsamlı yapay zeka içerik filtreleme
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Kurumsal kimlik ve erişim yönetimi
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Güvenli gizli bilgi ve kimlik bilgisi yönetimi
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Tedarik zinciri ve kod güvenliği taraması

### Güvenlik Standartları ve Çerçeveler
- [OAuth 2.1 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Mevcut OAuth güvenlik rehberi
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Web uygulaması güvenlik riskleri
- [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Yapay zeka özel güvenlik riskleri
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) - Kapsamlı yapay zeka risk yönetimi
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Bilgi güvenliği yönetim sistemleri

### Uygulama Rehberleri ve Eğitimler
- [Azure API Management as MCP Auth Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Kurumsal kimlik doğrulama modelleri
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Kimlik sağlayıcı entegrasyonu
- [Secure Token Storage Implementation](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Token yönetimi en iyi uygulamaları
- [End-to-End Encryption for AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Gelişmiş şifreleme modelleri

### Gelişmiş Güvenlik Kaynakları
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/sdl) - Güvenli geliştirme uygulamaları
- [AI Red Team Guidance](https://learn.microsoft.com/security/ai-red-team/) - Yapay zeka özel güvenlik testi
- [Threat Modeling for AI Systems](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Yapay zeka tehdit modelleme metodolojisi
- [Privacy Engineering for AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Gizliliği koruyan yapay zeka teknikleri

### Uyumluluk ve Yönetim
- [GDPR Compliance for AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Yapay zeka sistemlerinde gizlilik uyumluluğu
- [AI Governance Framework](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Sorumlu yapay zeka uygulaması
- [SOC 2 for AI Services](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Yapay zeka hizmet sağlayıcıları için güvenlik kontrolleri
- [HIPAA Compliance for AI](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Sağlık yapay zeka uyumluluk gereksinimleri

### DevSecOps ve Otomasyon
- [DevSecOps Pipeline for AI](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Güvenli yapay zeka geliştirme hatları
- [Automated Security Testing](https://learn.microsoft.com/security/engineering/devsecops) - Sürekli güvenlik doğrulaması
- [Infrastructure as Code Security](https://learn.microsoft.com/security/engineering/infrastructure-security) - Güvenli altyapı dağıtımı
- [Container Security for AI](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - Yapay zeka iş yükü konteynerizasyon güvenliği

### İzleme ve Olay Yanıtı  
- [Azure Monitor for AI Workloads](https://learn.microsoft.com/azure/azure-monitor/overview) - Kapsamlı izleme çözümleri
- [AI Security Incident Response](https://learn.microsoft.com/security/compass/incident-response-playbooks) - Yapay zeka özel olay prosedürleri
- [SIEM for AI Systems](https://learn.microsoft.com/azure/sentinel/overview) - Güvenlik bilgi ve olay yönetimi
- [Threat Intelligence for AI](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - Yapay zeka tehdit istihbaratı kaynakları

## 🔄 Sürekli İyileştirme

###
- **Araç Geliştirme**: MCP ekosistemi için güvenlik araçları ve kütüphaneleri geliştirin ve paylaşın

---

*Bu belge, 18 Ağustos 2025 itibarıyla MCP Spesifikasyonu 2025-06-18'e dayanan MCP güvenlik en iyi uygulamalarını yansıtmaktadır. Protokol ve tehdit ortamı geliştikçe güvenlik uygulamaları düzenli olarak gözden geçirilmeli ve güncellenmelidir.*

**Feragatname**:  
Bu belge, [Co-op Translator](https://github.com/Azure/co-op-translator) adlı yapay zeka çeviri hizmeti kullanılarak çevrilmiştir. Doğruluk için çaba göstersek de, otomatik çevirilerin hata veya yanlışlıklar içerebileceğini lütfen unutmayın. Orijinal belgenin kendi dilindeki hali, yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımından kaynaklanan yanlış anlamalar veya yanlış yorumlamalar için sorumluluk kabul etmiyoruz.