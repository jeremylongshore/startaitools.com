<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "904b59de1de9264801242d90a42cdd9d",
  "translation_date": "2025-09-05T10:59:15+00:00",
  "source_file": "01-CoreConcepts/README.md",
  "language_code": "tr"
}
-->
# MCP Temel Kavramlar: Yapay Zeka Entegrasyonu için Model Context Protocol'ü Anlamak

[![MCP Temel Kavramlar](../../../translated_images/02.8203e26c6fb5a797f38a10012061013ec66c95bb3260f6c9cfd2bf74b00860e1.tr.png)](https://youtu.be/earDzWGtE84)

_(Bu dersin videosunu izlemek için yukarıdaki görsele tıklayın)_

[Model Context Protocol (MCP)](https://github.com/modelcontextprotocol), Büyük Dil Modelleri (LLM'ler) ile harici araçlar, uygulamalar ve veri kaynakları arasındaki iletişimi optimize eden güçlü ve standart bir çerçevedir. Bu rehber, MCP'nin temel kavramlarını size adım adım anlatacaktır. MCP'nin istemci-sunucu mimarisi, temel bileşenleri, iletişim mekanikleri ve uygulama en iyi uygulamaları hakkında bilgi edineceksiniz.

- **Açık Kullanıcı Onayı**: Tüm veri erişimi ve işlemler, kullanıcı tarafından açık bir şekilde onaylanmadan gerçekleştirilemez. Kullanıcılar, hangi verilerin erişileceğini ve hangi işlemlerin yapılacağını net bir şekilde anlamalı ve izinler üzerinde ayrıntılı kontrol sahibi olmalıdır.

- **Veri Gizliliği Koruması**: Kullanıcı verileri yalnızca açık onayla açığa çıkarılır ve tüm etkileşim süreci boyunca güçlü erişim kontrolleri ile korunmalıdır. Uygulamalar, yetkisiz veri iletimini önlemeli ve sıkı gizlilik sınırlarını korumalıdır.

- **Araç Çalıştırma Güvenliği**: Her araç çağrısı, aracın işlevselliği, parametreleri ve potansiyel etkisi hakkında net bir anlayışla açık kullanıcı onayı gerektirir. Güçlü güvenlik sınırları, istenmeyen, güvensiz veya kötü niyetli araç çalıştırmalarını önlemelidir.

- **Taşıma Katmanı Güvenliği**: Tüm iletişim kanalları uygun şifreleme ve kimlik doğrulama mekanizmalarını kullanmalıdır. Uzaktan bağlantılar, güvenli taşıma protokolleri ve doğru kimlik bilgisi yönetimi uygulamalıdır.

#### Uygulama Yönergeleri:

- **İzin Yönetimi**: Kullanıcıların hangi sunuculara, araçlara ve kaynaklara erişebileceğini kontrol etmelerine olanak tanıyan ayrıntılı izin sistemleri uygulayın.
- **Kimlik Doğrulama ve Yetkilendirme**: Güvenli kimlik doğrulama yöntemleri (OAuth, API anahtarları) ve doğru token yönetimi ile süresi dolma mekanizmalarını kullanın.
- **Girdi Doğrulama**: Tüm parametreleri ve veri girişlerini tanımlı şemalara göre doğrulayarak enjeksiyon saldırılarını önleyin.
- **Denetim Günlüğü**: Güvenlik izleme ve uyumluluk için tüm işlemlerin kapsamlı kayıtlarını tutun.

## Genel Bakış

Bu ders, Model Context Protocol (MCP) ekosistemini oluşturan temel mimari ve bileşenleri incelemektedir. MCP etkileşimlerini güçlendiren istemci-sunucu mimarisi, anahtar bileşenler ve iletişim mekanizmaları hakkında bilgi edineceksiniz.

## Temel Öğrenme Hedefleri

Bu dersin sonunda:

- MCP istemci-sunucu mimarisini anlayacaksınız.
- Host, Client ve Server rollerini ve sorumluluklarını tanımlayacaksınız.
- MCP'yi esnek bir entegrasyon katmanı yapan temel özellikleri analiz edeceksiniz.
- MCP ekosisteminde bilginin nasıl aktığını öğreneceksiniz.
- .NET, Java, Python ve JavaScript'te kod örnekleriyle pratik bilgiler edineceksiniz.

## MCP Mimarisi: Derinlemesine Bakış

MCP ekosistemi, istemci-sunucu modeline dayalıdır. Bu modüler yapı, yapay zeka uygulamalarının araçlar, veritabanları, API'ler ve bağlamsal kaynaklarla verimli bir şekilde etkileşim kurmasını sağlar. Bu mimariyi temel bileşenlerine ayıralım.

MCP'nin temelinde, bir host uygulamasının birden fazla sunucuya bağlanabileceği bir istemci-sunucu mimarisi bulunur:

```mermaid
flowchart LR
    subgraph "Your Computer"
        Host["Host with MCP (Visual Studio, VS Code, IDEs, Tools)"]
        S1["MCP Server A"]
        S2["MCP Server B"]
        S3["MCP Server C"]
        Host <-->|"MCP Protocol"| S1
        Host <-->|"MCP Protocol"| S2
        Host <-->|"MCP Protocol"| S3
        S1 <--> D1[("Local\Data Source A")]
        S2 <--> D2[("Local\Data Source B")]
    end
    subgraph "Internet"
        S3 <-->|"Web APIs"| D3[("Remote\Services")]
    end
```

- **MCP Hostlar**: VSCode, Claude Desktop, IDE'ler veya MCP aracılığıyla veri erişimi sağlamak isteyen yapay zeka araçları gibi programlar.
- **MCP İstemciler**: Sunucularla birebir bağlantıları sürdüren protokol istemcileri.
- **MCP Sunucular**: Standart Model Context Protocol aracılığıyla belirli yetenekleri açığa çıkaran hafif programlar.
- **Yerel Veri Kaynakları**: MCP sunucularının güvenli bir şekilde erişebileceği bilgisayarınızdaki dosyalar, veritabanları ve hizmetler.
- **Uzaktan Hizmetler**: MCP sunucularının API'ler aracılığıyla bağlanabileceği internet üzerinden erişilebilir harici sistemler.

MCP Protokolü, tarih bazlı sürümleme (YYYY-MM-DD formatı) kullanan gelişen bir standarttır. Mevcut protokol sürümü **2025-06-18**'dir. [Protokol spesifikasyonundaki](https://modelcontextprotocol.io/specification/2025-06-18/) en son güncellemeleri görebilirsiniz.

### 1. Hostlar

Model Context Protocol (MCP) içinde **Hostlar**, kullanıcıların protokolle etkileşim kurduğu birincil arayüz olarak hizmet veren yapay zeka uygulamalarıdır. Hostlar, her bir sunucu bağlantısı için özel MCP istemcileri oluşturarak birden fazla MCP sunucusuna bağlantıları koordine eder ve yönetir. Host örnekleri şunları içerir:

- **Yapay Zeka Uygulamaları**: Claude Desktop, Visual Studio Code, Claude Code
- **Geliştirme Ortamları**: MCP entegrasyonuna sahip IDE'ler ve kod editörleri  
- **Özel Uygulamalar**: Amaca yönelik yapay zeka ajanları ve araçlar

**Hostlar**, yapay zeka modeli etkileşimlerini koordine eden uygulamalardır. Şunları yaparlar:

- **Yapay Zeka Modellerini Orkestre Etme**: LLM'leri çalıştırır veya yanıtlar oluşturmak ve yapay zeka iş akışlarını koordine etmek için etkileşim kurar.
- **İstemci Bağlantılarını Yönetme**: Her MCP sunucu bağlantısı için bir MCP istemcisi oluşturur ve sürdürür.
- **Kullanıcı Arayüzünü Kontrol Etme**: Konuşma akışını, kullanıcı etkileşimlerini ve yanıt sunumunu yönetir.  
- **Güvenliği Sağlama**: İzinleri, güvenlik kısıtlamalarını ve kimlik doğrulamayı kontrol eder.
- **Kullanıcı Onayını Yönetme**: Veri paylaşımı ve araç çalıştırma için kullanıcı onayını yönetir.

### 2. İstemciler

**İstemciler**, Hostlar ile MCP sunucuları arasında birebir bağlantıları sürdüren temel bileşenlerdir. Her MCP istemcisi, belirli bir MCP sunucusuna bağlanmak için Host tarafından oluşturulur ve düzenli ve güvenli iletişim kanalları sağlar. Birden fazla istemci, Hostların aynı anda birden fazla sunucuya bağlanmasını sağlar.

**İstemciler**, host uygulaması içindeki bağlayıcı bileşenlerdir. Şunları yaparlar:

- **Protokol İletişimi**: Sunuculara JSON-RPC 2.0 istekleri gönderir ve istemleri ile talimatları iletir.
- **Yetenek Müzakeresi**: Başlatma sırasında sunucularla desteklenen özellikleri ve protokol sürümlerini müzakere eder.
- **Araç Çalıştırma**: Modellerden gelen araç çalıştırma isteklerini yönetir ve yanıtları işler.
- **Gerçek Zamanlı Güncellemeler**: Sunuculardan gelen bildirimleri ve gerçek zamanlı güncellemeleri işler.
- **Yanıt İşleme**: Sunucu yanıtlarını kullanıcıya gösterim için işler ve biçimlendirir.

### 3. Sunucular

**Sunucular**, MCP istemcilerine bağlam, araçlar ve yetenekler sağlayan programlardır. Yerel olarak (Host ile aynı makinede) veya uzaktan (harici platformlarda) çalışabilirler ve istemci isteklerini işlemek ve yapılandırılmış yanıtlar sağlamakla sorumludurlar. Sunucular, standart Model Context Protocol aracılığıyla belirli işlevsellikleri açığa çıkarır.

**Sunucular**, bağlam ve yetenekler sağlayan hizmetlerdir. Şunları yaparlar:

- **Özellik Kaydı**: Kullanılabilir ilkel (kaynaklar, istemler, araçlar) öğeleri istemcilere kaydeder ve açığa çıkarır.
- **İstek İşleme**: İstemcilerden gelen araç çağrıları, kaynak istekleri ve istem isteklerini alır ve yürütür.
- **Bağlam Sağlama**: Model yanıtlarını geliştirmek için bağlamsal bilgi ve veri sağlar.
- **Durum Yönetimi**: Oturum durumunu korur ve gerektiğinde durumsal etkileşimleri yönetir.
- **Gerçek Zamanlı Bildirimler**: Bağlı istemcilere yetenek değişiklikleri ve güncellemeler hakkında bildirimler gönderir.

Sunucular, model yeteneklerini özel işlevsellikle genişletmek için herkes tarafından geliştirilebilir ve hem yerel hem de uzak dağıtım senaryolarını destekler.

### 4. Sunucu İlkeleri

Model Context Protocol (MCP) içindeki sunucular, istemciler, hostlar ve dil modelleri arasındaki zengin etkileşimlerin temel yapı taşlarını tanımlayan üç temel **ilke** sağlar. Bu ilkeler, protokol aracılığıyla sunulan bağlamsal bilgi ve eylem türlerini belirtir.

MCP sunucuları, aşağıdaki üç temel ilkenin herhangi bir kombinasyonunu açığa çıkarabilir:

#### Kaynaklar

**Kaynaklar**, yapay zeka uygulamalarına bağlamsal bilgi sağlayan veri kaynaklarıdır. Modelin anlayışını ve karar verme yeteneğini geliştirebilecek statik veya dinamik içeriği temsil eder:

- **Bağlamsal Veri**: Yapay zeka modeli tüketimi için yapılandırılmış bilgi ve bağlam.
- **Bilgi Tabanları**: Belge depoları, makaleler, kılavuzlar ve araştırma makaleleri.
- **Yerel Veri Kaynakları**: Dosyalar, veritabanları ve yerel sistem bilgileri.  
- **Harici Veri**: API yanıtları, web hizmetleri ve uzak sistem verileri.
- **Dinamik İçerik**: Harici koşullara bağlı olarak güncellenen gerçek zamanlı veri.

Kaynaklar, URI'ler ile tanımlanır ve `resources/list` yöntemiyle keşfedilir ve `resources/read` yöntemiyle alınır:

```text
file://documents/project-spec.md
database://production/users/schema
api://weather/current
```

#### İstemler

**İstemler**, dil modelleriyle etkileşimleri yapılandırmaya yardımcı olan yeniden kullanılabilir şablonlardır. Standartlaştırılmış etkileşim kalıpları ve şablonlu iş akışları sağlarlar:

- **Şablon Tabanlı Etkileşimler**: Önceden yapılandırılmış mesajlar ve konuşma başlatıcıları.
- **İş Akışı Şablonları**: Yaygın görevler ve etkileşimler için standartlaştırılmış diziler.
- **Few-shot Örnekler**: Model talimatı için örnek tabanlı şablonlar.
- **Sistem İstemleri**: Model davranışını ve bağlamını tanımlayan temel istemler.
- **Dinamik Şablonlar**: Belirli bağlamlara uyum sağlayan parametreli istemler.

İstemler, değişken ikamesini destekler ve `prompts/list` yöntemiyle keşfedilir ve `prompts/get` yöntemiyle alınır:

```markdown
Generate a {{task_type}} for {{product}} targeting {{audience}} with the following requirements: {{requirements}}
```

#### Araçlar

**Araçlar**, yapay zeka modellerinin belirli eylemleri gerçekleştirmek için çağırabileceği çalıştırılabilir işlevlerdir. MCP ekosisteminin "fiilleri"ni temsil eder ve modellerin harici sistemlerle etkileşim kurmasını sağlar:

- **Çalıştırılabilir İşlevler**: Modellerin belirli parametrelerle çağırabileceği ayrık işlemler.
- **Harici Sistem Entegrasyonu**: API çağrıları, veritabanı sorguları, dosya işlemleri, hesaplamalar.
- **Benzersiz Kimlik**: Her araç, belirgin bir ad, açıklama ve parametre şemasına sahiptir.
- **Yapılandırılmış G/Ç**: Araçlar doğrulanmış parametreleri kabul eder ve yapılandırılmış, türlendirilmiş yanıtlar döndürür.
- **Eylem Yetenekleri**: Modellerin gerçek dünya eylemleri gerçekleştirmesini ve canlı veri almasını sağlar.

Araçlar, parametre doğrulama için JSON Şeması ile tanımlanır ve `tools/list` yöntemiyle keşfedilir ve `tools/call` yöntemiyle çalıştırılır:

```typescript
server.tool(
  "search_products", 
  {
    query: z.string().describe("Search query for products"),
    category: z.string().optional().describe("Product category filter"),
    max_results: z.number().default(10).describe("Maximum results to return")
  }, 
  async (params) => {
    // Execute search and return structured results
    return await productService.search(params);
  }
);
```

## İstemci İlkeleri

Model Context Protocol (MCP) içinde **istemciler**, sunucuların host uygulamasından ek yetenekler talep etmesine olanak tanıyan ilkeler açığa çıkarabilir. Bu istemci tarafı ilkeler, sunucuların yapay zeka model yeteneklerine ve kullanıcı etkileşimlerine erişebileceği daha zengin, daha etkileşimli sunucu uygulamalarına olanak tanır.

### Örnekleme

**Örnekleme**, sunucuların istemcinin yapay zeka uygulamasından dil modeli tamamlama taleplerinde bulunmasına olanak tanır. Bu ilke, sunucuların kendi model bağımlılıklarını içermeden LLM yeteneklerine erişmesini sağlar:

- **Model Bağımsız Erişim**: Sunucular, LLM SDK'larını içermeden veya model erişimini yönetmeden tamamlama taleplerinde bulunabilir.
- **Sunucu Başlatmalı Yapay Zeka**: Sunucuların istemcinin yapay zeka modelini kullanarak içerik oluşturmasını sağlar.
- **Yinelemeli LLM Etkileşimleri**: Sunucuların işleme için yapay zeka yardımı gerektiği karmaşık senaryoları destekler.
- **Dinamik İçerik Üretimi**: Sunucuların host'un modelini kullanarak bağlamsal yanıtlar oluşturmasına olanak tanır.

Örnekleme, sunucuların istemcilere tamamlama talepleri gönderdiği `sampling/complete` yöntemiyle başlatılır.

### Bilgi Toplama  

**Bilgi Toplama**, sunucuların istemci arayüzü aracılığıyla kullanıcılardan ek bilgi veya onay talep etmesine olanak tanır:

- **Kullanıcı Girdi Talepleri**: Sunucular, araç çalıştırma için gereken ek bilgileri talep edebilir.
- **Onay Diyalogları**: Hassas veya etkili işlemler için kullanıcı onayı talep eder.
- **Etkileşimli İş Akışları**: Sunucuların adım adım kullanıcı etkileşimleri oluşturmasını sağlar.
- **Dinamik Parametre Toplama**: Araç çalıştırma sırasında eksik veya isteğe bağlı parametreleri toplar.

Bilgi toplama talepleri, istemcinin arayüzü aracılığıyla kullanıcı girdisi toplamak için `elicitation/request` yöntemi kullanılarak yapılır.

### Günlükleme

**Günlükleme**, sunucuların istemcilere hata ayıklama, izleme ve operasyonel görünürlük için yapılandırılmış günlük mesajları göndermesine olanak tanır:

- **Hata Ayıklama Desteği**: Sunucuların hata ayıklama için ayrıntılı yürütme günlükleri sağlamasına olanak tanır.
- **Operasyonel İzleme**: İstemcilere durum güncellemeleri ve performans metrikleri gönderir.
- **Hata Raporlama**: Ayrıntılı hata bağlamı ve tanı bilgileri sağlar.
- **Denetim İzleri**: Sunucu işlemlerinin ve kararlarının kapsamlı günlüklerini oluşturur.

Günlükleme mesajları, sunucu işlemlerine şeffaflık sağlamak ve hata ayıklamayı kolaylaştırmak için istemcilere gönderilir.

## MCP'deki Bilgi Akışı

Model Context Protocol (MCP), hostlar, istemciler, sunucular ve modeller arasında yapılandırılmış bir bilgi akışı tanımlar. Bu akışı anlamak, kullanıcı taleplerinin nasıl işlendiğini ve harici araçlar ile verilerin model yanıtlarına nasıl entegre edildiğini netleştirir.

- **Host Bağlantıyı Başlatır**  
  Host uygulaması (örneğin bir IDE veya sohbet arayüzü), genellikle STDIO, WebSocket veya başka bir desteklenen taşıma aracılığıyla bir MCP sunucusuna bağlantı kurar.

- **Yetenek Müzakeresi**  
  İstemci (host içinde yerleşik) ve sunucu, oturum için kullanılabilir yetenekler, araçlar, kaynaklar ve protokol sürümleri hakkında bilgi alışverişinde bulunur. Bu, her iki tarafın oturum için hangi yeteneklerin mevcut olduğunu anlamasını sağlar.

- **Kullanıcı Talebi**  
  Kullanıcı, host ile etkileşimde bulunur (örneğin bir istem veya komut girer). Host bu girdiyi toplar ve işlem için istemciye iletir.

- **Kaynak veya Araç Kullanımı**  
  - İstemci, modelin anlayışını zenginleştirmek için sunucudan ek bağlam veya kaynaklar (örneğin dosyalar, veritabanı girdileri veya bilgi tabanı makaleleri) talep edebilir.
  - Model, bir aracın gerekli olduğunu belirlerse (örneğin veri almak, hesaplama yapmak veya bir API çağrısı yapmak için), istemci, araç adı ve parametrelerini
- **JSON-RPC 2.0 Protokolü**: Tüm iletişim, yöntem çağrıları, yanıtlar ve bildirimler için standartlaştırılmış JSON-RPC 2.0 mesaj formatını kullanır.
- **Yaşam Döngüsü Yönetimi**: İstemciler ve sunucular arasında bağlantı başlatma, yetenek müzakeresi ve oturum sonlandırmayı yönetir.
- **Sunucu Primitifleri**: Sunucuların araçlar, kaynaklar ve istemler aracılığıyla temel işlevsellik sağlamasına olanak tanır.
- **İstemci Primitifleri**: Sunucuların LLM'lerden örnekleme talep etmesine, kullanıcı girdisi almasına ve günlük mesajları göndermesine olanak tanır.
- **Gerçek Zamanlı Bildirimler**: Dinamik güncellemeler için anket yapmadan asenkron bildirimleri destekler.

#### Temel Özellikler:

- **Protokol Sürüm Müzakeresi**: Uyumluluğu sağlamak için tarih tabanlı sürümleme (YYYY-MM-DD) kullanır.
- **Yetenek Keşfi**: İstemciler ve sunucular, başlatma sırasında desteklenen özellik bilgilerini paylaşır.
- **Durumlu Oturumlar**: Bağlantı durumunu birden fazla etkileşim boyunca koruyarak bağlam sürekliliği sağlar.

### Taşıma Katmanı

**Taşıma Katmanı**, MCP katılımcıları arasında iletişim kanallarını, mesaj çerçevelemeyi ve kimlik doğrulamayı yönetir:

#### Desteklenen Taşıma Mekanizmaları:

1. **STDIO Taşıma**:
   - Doğrudan işlem iletişimi için standart giriş/çıkış akışlarını kullanır.
   - Aynı makinedeki yerel işlemler için ağ yükü olmadan en uygun seçenektir.
   - Yerel MCP sunucu uygulamaları için yaygın olarak kullanılır.

2. **Akışlı HTTP Taşıma**:
   - İstemci-sunucu mesajları için HTTP POST kullanır.
   - Sunucu-istemci akışı için isteğe bağlı Sunucu Gönderimli Olaylar (SSE) içerir.
   - Ağlar arasında uzak sunucu iletişimini sağlar.
   - Standart HTTP kimlik doğrulamasını destekler (taşıyıcı jetonlar, API anahtarları, özel başlıklar).
   - MCP, güvenli jeton tabanlı kimlik doğrulama için OAuth'u önerir.

#### Taşıma Soyutlaması:

Taşıma katmanı, veri katmanından iletişim ayrıntılarını soyutlar ve tüm taşıma mekanizmaları arasında aynı JSON-RPC 2.0 mesaj formatını sağlar. Bu soyutlama, uygulamaların yerel ve uzak sunucular arasında sorunsuz bir şekilde geçiş yapmasına olanak tanır.

### Güvenlik Hususları

MCP uygulamaları, tüm protokol işlemleri boyunca güvenli, güvenilir ve emniyetli etkileşimleri sağlamak için birkaç kritik güvenlik ilkesine uymalıdır:

- **Kullanıcı Onayı ve Kontrolü**: Herhangi bir veri erişimi veya işlem gerçekleştirilmeden önce kullanıcılar açıkça onay vermelidir. Paylaşılan veriler ve yetkilendirilen işlemler üzerinde net bir kontrol sağlanmalı, kullanıcıların etkinlikleri gözden geçirmesi ve onaylaması için sezgisel arayüzler desteklenmelidir.

- **Veri Gizliliği**: Kullanıcı verileri yalnızca açık onayla ifşa edilmeli ve uygun erişim kontrolleriyle korunmalıdır. MCP uygulamaları, yetkisiz veri iletimine karşı koruma sağlamalı ve tüm etkileşimler boyunca gizliliği korumalıdır.

- **Araç Güvenliği**: Herhangi bir araç çağrılmadan önce açık kullanıcı onayı gereklidir. Kullanıcılar, her aracın işlevselliğini net bir şekilde anlamalıdır ve istenmeyen veya güvensiz araç çalıştırmalarını önlemek için sağlam güvenlik sınırları uygulanmalıdır.

Bu güvenlik ilkelerine uyarak MCP, kullanıcı güvenini, gizliliğini ve güvenliğini tüm protokol etkileşimlerinde korurken güçlü yapay zeka entegrasyonlarını mümkün kılar.

## Kod Örnekleri: Temel Bileşenler

Aşağıda, temel MCP sunucu bileşenlerini ve araçlarını nasıl uygulayacağınızı gösteren birkaç popüler programlama dilinde kod örnekleri bulunmaktadır.

### .NET Örneği: Araçlarla Basit Bir MCP Sunucusu Oluşturma

Aşağıda, özel araçlarla basit bir MCP sunucusunun nasıl uygulanacağını gösteren pratik bir .NET kod örneği bulunmaktadır. Bu örnek, araçları tanımlama ve kaydetme, istekleri işleme ve sunucuyu Model Context Protocol ile bağlama işlemlerini göstermektedir.

```csharp
using System;
using System.Threading.Tasks;
using ModelContextProtocol.Server;
using ModelContextProtocol.Server.Transport;
using ModelContextProtocol.Server.Tools;

public class WeatherServer
{
    public static async Task Main(string[] args)
    {
        // Create an MCP server
        var server = new McpServer(
            name: "Weather MCP Server",
            version: "1.0.0"
        );
        
        // Register our custom weather tool
        server.AddTool<string, WeatherData>("weatherTool", 
            description: "Gets current weather for a location",
            execute: async (location) => {
                // Call weather API (simplified)
                var weatherData = await GetWeatherDataAsync(location);
                return weatherData;
            });
        
        // Connect the server using stdio transport
        var transport = new StdioServerTransport();
        await server.ConnectAsync(transport);
        
        Console.WriteLine("Weather MCP Server started");
        
        // Keep the server running until process is terminated
        await Task.Delay(-1);
    }
    
    private static async Task<WeatherData> GetWeatherDataAsync(string location)
    {
        // This would normally call a weather API
        // Simplified for demonstration
        await Task.Delay(100); // Simulate API call
        return new WeatherData { 
            Temperature = 72.5,
            Conditions = "Sunny",
            Location = location
        };
    }
}

public class WeatherData
{
    public double Temperature { get; set; }
    public string Conditions { get; set; }
    public string Location { get; set; }
}
```

### Java Örneği: MCP Sunucu Bileşenleri

Bu örnek, yukarıdaki .NET örneğinde olduğu gibi aynı MCP sunucusunu ve araç kaydını Java'da uygulamayı göstermektedir.

```java
import io.modelcontextprotocol.server.McpServer;
import io.modelcontextprotocol.server.McpToolDefinition;
import io.modelcontextprotocol.server.transport.StdioServerTransport;
import io.modelcontextprotocol.server.tool.ToolExecutionContext;
import io.modelcontextprotocol.server.tool.ToolResponse;

public class WeatherMcpServer {
    public static void main(String[] args) throws Exception {
        // Create an MCP server
        McpServer server = McpServer.builder()
            .name("Weather MCP Server")
            .version("1.0.0")
            .build();
            
        // Register a weather tool
        server.registerTool(McpToolDefinition.builder("weatherTool")
            .description("Gets current weather for a location")
            .parameter("location", String.class)
            .execute((ToolExecutionContext ctx) -> {
                String location = ctx.getParameter("location", String.class);
                
                // Get weather data (simplified)
                WeatherData data = getWeatherData(location);
                
                // Return formatted response
                return ToolResponse.content(
                    String.format("Temperature: %.1f°F, Conditions: %s, Location: %s", 
                    data.getTemperature(), 
                    data.getConditions(), 
                    data.getLocation())
                );
            })
            .build());
        
        // Connect the server using stdio transport
        try (StdioServerTransport transport = new StdioServerTransport()) {
            server.connect(transport);
            System.out.println("Weather MCP Server started");
            // Keep server running until process is terminated
            Thread.currentThread().join();
        }
    }
    
    private static WeatherData getWeatherData(String location) {
        // Implementation would call a weather API
        // Simplified for example purposes
        return new WeatherData(72.5, "Sunny", location);
    }
}

class WeatherData {
    private double temperature;
    private String conditions;
    private String location;
    
    public WeatherData(double temperature, String conditions, String location) {
        this.temperature = temperature;
        this.conditions = conditions;
        this.location = location;
    }
    
    public double getTemperature() {
        return temperature;
    }
    
    public String getConditions() {
        return conditions;
    }
    
    public String getLocation() {
        return location;
    }
}
```

### Python Örneği: MCP Sunucusu Oluşturma

Bu örnek fastmcp kullanır, bu nedenle önce kurulum yapmanız gerekmektedir:

```python
pip install fastmcp
```  
Kod Örneği:

```python
#!/usr/bin/env python3
import asyncio
from fastmcp import FastMCP
from fastmcp.transports.stdio import serve_stdio

# Create a FastMCP server
mcp = FastMCP(
    name="Weather MCP Server",
    version="1.0.0"
)

@mcp.tool()
def get_weather(location: str) -> dict:
    """Gets current weather for a location."""
    return {
        "temperature": 72.5,
        "conditions": "Sunny",
        "location": location
    }

# Alternative approach using a class
class WeatherTools:
    @mcp.tool()
    def forecast(self, location: str, days: int = 1) -> dict:
        """Gets weather forecast for a location for the specified number of days."""
        return {
            "location": location,
            "forecast": [
                {"day": i+1, "temperature": 70 + i, "conditions": "Partly Cloudy"}
                for i in range(days)
            ]
        }

# Register class tools
weather_tools = WeatherTools()

# Start the server
if __name__ == "__main__":
    asyncio.run(serve_stdio(mcp))
```

### JavaScript Örneği: MCP Sunucusu Oluşturma

Bu örnek, JavaScript'te MCP sunucusu oluşturmayı ve hava durumu ile ilgili iki aracı nasıl kaydedeceğinizi göstermektedir.

```javascript
// Using the official Model Context Protocol SDK
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod"; // For parameter validation

// Create an MCP server
const server = new McpServer({
  name: "Weather MCP Server",
  version: "1.0.0"
});

// Define a weather tool
server.tool(
  "weatherTool",
  {
    location: z.string().describe("The location to get weather for")
  },
  async ({ location }) => {
    // This would normally call a weather API
    // Simplified for demonstration
    const weatherData = await getWeatherData(location);
    
    return {
      content: [
        { 
          type: "text", 
          text: `Temperature: ${weatherData.temperature}°F, Conditions: ${weatherData.conditions}, Location: ${weatherData.location}` 
        }
      ]
    };
  }
);

// Define a forecast tool
server.tool(
  "forecastTool",
  {
    location: z.string(),
    days: z.number().default(3).describe("Number of days for forecast")
  },
  async ({ location, days }) => {
    // This would normally call a weather API
    // Simplified for demonstration
    const forecast = await getForecastData(location, days);
    
    return {
      content: [
        { 
          type: "text", 
          text: `${days}-day forecast for ${location}: ${JSON.stringify(forecast)}` 
        }
      ]
    };
  }
);

// Helper functions
async function getWeatherData(location) {
  // Simulate API call
  return {
    temperature: 72.5,
    conditions: "Sunny",
    location: location
  };
}

async function getForecastData(location, days) {
  // Simulate API call
  return Array.from({ length: days }, (_, i) => ({
    day: i + 1,
    temperature: 70 + Math.floor(Math.random() * 10),
    conditions: i % 2 === 0 ? "Sunny" : "Partly Cloudy"
  }));
}

// Connect the server using stdio transport
const transport = new StdioServerTransport();
server.connect(transport).catch(console.error);

console.log("Weather MCP Server started");
```

Bu JavaScript örneği, bir MCP istemcisinin bir sunucuya bağlanmasını, bir istem gönderip yanıtı işlemesini ve yapılan araç çağrılarını nasıl yönettiğini göstermektedir.

## Güvenlik ve Yetkilendirme

MCP, protokol boyunca güvenlik ve yetkilendirme yönetimi için birkaç yerleşik kavram ve mekanizma içerir:

1. **Araç İzin Kontrolü**:  
   İstemciler, bir modelin bir oturum sırasında hangi araçları kullanmasına izin verildiğini belirtebilir. Bu, yalnızca açıkça yetkilendirilmiş araçların erişilebilir olmasını sağlar ve istenmeyen veya güvensiz işlemler riskini azaltır. İzinler, kullanıcı tercihleri, organizasyon politikaları veya etkileşim bağlamına göre dinamik olarak yapılandırılabilir.

2. **Kimlik Doğrulama**:  
   Sunucular, araçlara, kaynaklara veya hassas işlemlere erişim sağlamadan önce kimlik doğrulama talep edebilir. Bu, API anahtarları, OAuth jetonları veya diğer kimlik doğrulama yöntemlerini içerebilir. Uygun kimlik doğrulama, yalnızca güvenilir istemcilerin ve kullanıcıların sunucu tarafı yeteneklerini çağırmasını sağlar.

3. **Doğrulama**:  
   Tüm araç çağrıları için parametre doğrulaması uygulanır. Her araç, parametrelerinin beklenen türlerini, formatlarını ve kısıtlamalarını tanımlar ve sunucu gelen istekleri buna göre doğrular. Bu, hatalı veya kötü niyetli girdilerin araç uygulamalarına ulaşmasını önler ve işlemlerin bütünlüğünü korur.

4. **Hız Sınırlandırma**:  
   Sunucu kaynaklarının kötüye kullanılmasını önlemek ve adil kullanımını sağlamak için MCP sunucuları, araç çağrıları ve kaynak erişimi için hız sınırlandırması uygulayabilir. Hız sınırları kullanıcı başına, oturum başına veya genel olarak uygulanabilir ve hizmet reddi saldırılarına veya aşırı kaynak tüketimine karşı koruma sağlar.

Bu mekanizmaları birleştirerek MCP, dil modellerini harici araçlar ve veri kaynaklarıyla entegre etmek için güvenli bir temel sağlar ve kullanıcılar ile geliştiricilere erişim ve kullanım üzerinde ince ayar kontrolü sunar.

## Protokol Mesajları ve İletişim Akışı

MCP iletişimi, ana bilgisayarlar, istemciler ve sunucular arasında net ve güvenilir etkileşimleri kolaylaştırmak için yapılandırılmış **JSON-RPC 2.0** mesajlarını kullanır. Protokol, farklı işlem türleri için belirli mesaj desenlerini tanımlar:

### Temel Mesaj Türleri:

#### **Başlatma Mesajları**
- **`initialize` İsteği**: Bağlantıyı kurar ve protokol sürümünü ve yetenekleri müzakere eder.
- **`initialize` Yanıtı**: Desteklenen özellikleri ve sunucu bilgilerini doğrular.  
- **`notifications/initialized`**: Başlatmanın tamamlandığını ve oturumun hazır olduğunu bildirir.

#### **Keşif Mesajları**
- **`tools/list` İsteği**: Sunucudan mevcut araçları keşfeder.
- **`resources/list` İsteği**: Mevcut kaynakları (veri kaynakları) listeler.
- **`prompts/list` İsteği**: Mevcut istem şablonlarını alır.

#### **Yürütme Mesajları**  
- **`tools/call` İsteği**: Sağlanan parametrelerle belirli bir aracı çalıştırır.
- **`resources/read` İsteği**: Belirli bir kaynaktan içerik alır.
- **`prompts/get` İsteği**: İsteğe bağlı parametrelerle bir istem şablonu alır.

#### **İstemci Tarafı Mesajları**
- **`sampling/complete` İsteği**: Sunucu, istemciden LLM tamamlama talep eder.
- **`elicitation/request`**: Sunucu, istemci arayüzü aracılığıyla kullanıcı girdisi talep eder.
- **Günlük Mesajları**: Sunucu, istemciye yapılandırılmış günlük mesajları gönderir.

#### **Bildirim Mesajları**
- **`notifications/tools/list_changed`**: Sunucu, istemciyi araç değişiklikleri hakkında bilgilendirir.
- **`notifications/resources/list_changed`**: Sunucu, istemciyi kaynak değişiklikleri hakkında bilgilendirir.  
- **`notifications/prompts/list_changed`**: Sunucu, istemciyi istem değişiklikleri hakkında bilgilendirir.

### Mesaj Yapısı:

Tüm MCP mesajları JSON-RPC 2.0 formatını takip eder:
- **İstek Mesajları**: `id`, `method` ve isteğe bağlı `params` içerir.
- **Yanıt Mesajları**: `id` ve `result` veya `error` içerir.  
- **Bildirim Mesajları**: `method` ve isteğe bağlı `params` içerir (hiçbir `id` veya yanıt beklenmez).

Bu yapılandırılmış iletişim, gerçek zamanlı güncellemeler, araç zincirleme ve sağlam hata işleme gibi gelişmiş senaryoları destekleyen güvenilir, izlenebilir ve genişletilebilir etkileşimler sağlar.

## Önemli Noktalar

- **Mimari**: MCP, ana bilgisayarların sunuculara birden fazla istemci bağlantısını yönettiği istemci-sunucu mimarisini kullanır.
- **Katılımcılar**: Ekosistem, ana bilgisayarları (AI uygulamaları), istemcileri (protokol bağlayıcıları) ve sunucuları (yetenek sağlayıcıları) içerir.
- **Taşıma Mekanizmaları**: İletişim, STDIO (yerel) ve isteğe bağlı SSE ile Akışlı HTTP (uzak) destekler.
- **Temel Primitifler**: Sunucular, araçlar (çalıştırılabilir işlevler), kaynaklar (veri kaynakları) ve istemler (şablonlar) sağlar.
- **İstemci Primitifleri**: Sunucular, istemcilerden örnekleme (LLM tamamlama), kullanıcı girdisi (elicitasyon) ve günlük kaydı talep edebilir.
- **Protokol Temeli**: JSON-RPC 2.0 üzerine inşa edilmiştir ve tarih tabanlı sürümleme kullanır (mevcut: 2025-06-18).
- **Gerçek Zamanlı Yetenekler**: Dinamik güncellemeler ve gerçek zamanlı senkronizasyon için bildirimleri destekler.
- **Güvenlik Önceliği**: Açık kullanıcı onayı, veri gizliliği koruması ve güvenli taşıma temel gereksinimlerdir.

## Egzersiz

Alanınızda faydalı olabilecek basit bir MCP aracı tasarlayın. Belirleyin:
1. Aracın adı ne olacak?
2. Hangi parametreleri kabul edecek?
3. Hangi çıktıyı döndürecek?
4. Bir model bu aracı kullanıcı sorunlarını çözmek için nasıl kullanabilir?


---

## Sıradaki

Sonraki: [Bölüm 2: Güvenlik](../02-Security/README.md)

---

**Feragatname**:  
Bu belge, [Co-op Translator](https://github.com/Azure/co-op-translator) adlı yapay zeka çeviri hizmeti kullanılarak çevrilmiştir. Doğruluk için çaba göstersek de, otomatik çevirilerin hata veya yanlışlıklar içerebileceğini lütfen unutmayın. Belgenin orijinal dili, yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımından kaynaklanan yanlış anlama veya yanlış yorumlamalardan sorumlu değiliz.