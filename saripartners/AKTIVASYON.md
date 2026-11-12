# @saripartners hesabını Claude'a bağlama

Claude hesabınıza **şifrenizle giriş yapmaz**. Instagram'ın resmi yöntemini kullanır: Meta'nın verdiği bir **erişim token'ı** (dijital anahtar). Bu anahtar yalnızca sizin onayladığınız işler için kullanılır: gönderi yayınlama, istatistikleri okuma ve yorumları yönetme. Anahtarı istediğiniz an iptal edebilirsiniz. Şifreniz ve iki adımlı doğrulamanız değişmez.

Kurulum yaklaşık 15–20 dakika sürer ve bir kez yapılır.

---

## Adım 1: Hesabı profesyonel hesaba çevirin (zaten öyleyse atlayın)

1. Instagram uygulamasında profilinize gidin → sağ üstteki **☰** → **Ayarlar ve hareketler**.
2. **Hesap türü ve araçlar** → **Profesyonel hesaba geç**.
3. Kategori olarak **Avukat ve Hukuk Hizmeti** gibi uygun bir kategori seçin. Hesap türü olarak **İşletme**'yi seçin.

## Adım 2: Meta geliştirici hesabı ve uygulama oluşturun

1. Bilgisayardan **developers.facebook.com** adresine gidin ve Facebook hesabınızla giriş yapın. İlk kez kullanıyorsanız **Başlayın** deyip geliştirici kaydını tamamlayın (telefon/e-posta doğrulaması).
2. **Uygulamalarım** → **Uygulama oluştur**.
3. Uygulama adı olarak örneğin `SariPartners Icerik` yazın. İletişim e-postası olarak kendi adresinizi girin.
4. Kullanım alanı (use case) olarak **"Instagram'da mesajları ve içeriği yönetin"** (*Manage messaging & content on Instagram*) seçeneğini seçin.
5. İşletme portföyü sorulursa büronuzun portföyünü seçin veya "şimdilik bağlama" deyin. Ardından **Uygulama oluştur**'a basın.

## Adım 3: Instagram hesabınızı uygulamaya bağlayıp token üretin

1. Uygulama panelinde **Instagram** → **API setup with Instagram business login** (Instagram işletme girişi ile API kurulumu) bölümünü açın.
2. **"1. Generate access tokens"** başlığında **Add account** (Hesap ekle) düğmesine basın.
3. Açılan pencerede **@saripartners** hesabıyla giriş yapın ve istenen izinleri onaylayın:
   - `instagram_business_basic`: profil ve gönderileri okuma
   - `instagram_business_content_publish`: gönderi yayınlama
   - `instagram_business_manage_comments`: yorumları okuma ve yanıtlama
   - `instagram_business_manage_insights`: istatistikleri okuma
4. Hesap listede göründükten sonra yanındaki **Generate token** düğmesine basın ve çıkan uzun metni kopyalayın. Bu, yaklaşık **60 gün** geçerli bir anahtardır.

> Uygulama "Geliştirme" (Development) modunda kalabilir. Uygulamanın yöneticisi siz olduğunuz ve yalnızca kendi hesabınızı kullandığınız için App Review gerekmez. Meta bir uyarı gösterirse bana iletin.

## Adım 4: Token'ı Claude'a güvenli şekilde verin

**Token'ı sohbete yapıştırmayın.**

1. Bu sohbete **"Token hazır"** yazın.
2. Ben size güvenli bir form açacağım. Token'ı oraya yapıştırın.
3. Token, oturumun ağ ayarlarında şifreli olarak saklanır. Ben değerini hiçbir zaman görmem; token yalnızca Instagram'a giden isteklere eklenir.
4. Ardından bağlantıyı test ederim (`whoami`): hesap adını ve takipçi sayısını size gösteririm.

## Adım 5: İlk onay ve otomatik yayın

- Taslaklar her Perşembe hazırlanır ve size gönderilir.
- **"Onaylıyorum"** dediğiniz gönderiler planlanan gün sabah 09:50'de otomatik yayınlanır.
- Onaylamadığınız hiçbir şey yayınlanmaz.

---

## Güvenlik ve kontrol

| İstediğiniz | Nasıl yapılır |
|---|---|
| Erişimi tamamen kesmek | developers.facebook.com → uygulamanız → **Instagram** → hesabın yanında **Remove**. Ya da Instagram → Ayarlar → **Web siteleri ve uygulamalar** (Hesap Merkezi altında) → uygulamayı kaldırın. |
| Token'ı yenilemek (60 günde bir) | Adım 3.4'ü tekrarlayın ve bana "token yenilendi" deyin. Süresi dolmadan önce size hatırlatırım. |
| Yayınları durdurmak | Bana "yayınları durdur" demeniz yeterli. Zamanlanmış görevleri kapatırım. |

## Sizden ayrıca beklediklerim

1. **Logo** (PNG veya SVG) ve varsa **kurumsal renk kodları**. Şu an geçici olarak lacivert ve hardal sarısı kullanıyorum (`marka.json`).
2. Büronun **çalışma alanları**: haftalık konuları buna göre seçerim.
3. Gönderileri **kimin onaylayacağı**: hukuki içerik bir avukatın onayı olmadan yayınlanmamalıdır (bkz. `rehber/uyum-kurallari.md`).
