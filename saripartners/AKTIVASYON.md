# @saripartners hesabını Claude'a bağlama (adım adım)

**Ne yapıyoruz?** Meta'dan, Claude'un @saripartners hesabına gönderi atabilmesi için bir **anahtar (token)** alıyoruz. Claude şifrenizi hiç görmez. Anahtarı istediğiniz an iptal edebilirsiniz.

**Süre:** 20–30 dakika, bir kez.

**Hazırlayın:**
- Bir **bilgisayar** (telefondan bu işlem çok zor). Tarayıcı olarak Google Chrome önerilir.
- **Telefonunuz**: Instagram uygulaması açık olsun. Doğrulama kodları için de lazım.
- @saripartners Instagram şifresi.
- Kişisel **Facebook** hesabınızın şifresi. Meta'nın geliştirici sitesine Facebook hesabıyla girilir. Bu hesap Instagram'da görünmez.

Her bölümün sonunda ✅ işareti var. Bir yerde takılırsanız bana **bölüm numarasını ve ekranda yazan hatayı** (veya ekran görüntüsünü) gönderin.

---

## BÖLÜM 1: Instagram hesabını kontrol edin (telefonda, 2 dakika)

1. Telefonda Instagram'ı açın ve **@saripartners** hesabına geçin.
2. Sağ alttaki **profil fotoğrafınıza** dokunun.
3. Sağ üstteki **üç çizgiye (☰)** dokunun.
4. Listede **"Hesap türü ve araçlar"** yazısını arayın ve dokunun.
5. Bir sonraki ekranda:
   - **"Kişisel hesaba geç"** yazıyorsa hesabınız zaten profesyoneldir. ✅ Bölüm 2'ye geçin.
   - **"Profesyonel hesaba geç"** yazıyorsa dokunun, kategori olarak **"Avukat ve Hukuk Hizmeti"** seçin, hesap türünde **"İşletme"**yi seçin ve adımları bitirin.

✅ Hesap profesyonel.

---

## BÖLÜM 2: Meta geliştirici hesabı açın (bilgisayarda, 5 dakika)

1. Bilgisayarda Chrome'u açın, adres çubuğuna **developers.facebook.com** yazıp Enter'a basın.
2. Sağ üstte **"Giriş yap"** (Log in) düğmesine basın ve **Facebook** hesabınızla giriş yapın.
3. Sağ üstte **"Başlayın"** (Get Started) düğmesi varsa basın. Yoksa bu bölüm zaten tamamdır, Bölüm 3'e geçin.
4. Açılan pencerede sırayla:
   - **Devam**'a basın.
   - Telefon numaranızı doğrulayın (SMS ile kod gelir, kodu yazın).
   - E-posta adresinizi onaylayın.
   - "Rolünüz nedir?" sorusunda **"Geliştirici"** veya **"Diğer"**i seçin.
   - **Tamamla**'ya basın.

✅ Geliştirici hesabınız hazır.

---

## BÖLÜM 3: Uygulama oluşturun (bilgisayarda, 5 dakika)

"Uygulama", Claude'un Instagram'a bağlanacağı kapıdır. Sadece sizin için çalışır, kimse görmez.

1. developers.facebook.com sayfasında sağ üstteki **"Uygulamalarım"** (My Apps) yazısına basın.
2. **"Uygulama oluştur"** (Create App) düğmesine basın.
3. **Uygulama adı:** `SariPartners Icerik` yazın. **E-posta:** kendi e-postanız. **İleri**'ye basın.
4. **Kullanım alanı** (Use cases) ekranında listede şunu bulun ve seçin:
   **"Instagram'da mesajları ve içeriği yönetin"** (İngilizcesi: *Manage messaging & content on Instagram*).
   **İleri**'ye basın.
5. **İşletme** (Business) sorulursa **"Henüz bir işletme portföyü bağlamak istemiyorum"** seçeneğini seçin. **İleri**'ye basın.
6. Son ekranda **"Uygulama oluştur"**a basın. Facebook şifrenizi tekrar sorabilir; yazın.

✅ Uygulama panelini (Dashboard) görüyorsunuz.

---

## BÖLÜM 4: Instagram hesabını "test kullanıcısı" yapın (en çok atlanan adım)

Meta, yeni uygulamaların yalnızca izin verilen hesaplarla çalışmasına izin verir. Bu adımla @saripartners hesabına izin veriyoruz.

**Bilgisayarda:**

1. Uygulama panelinde sol menüde **"Uygulama rolleri"** (App roles) → **"Roller"** (Roles) yazısına basın.
2. **"Kişi ekle"** (Add People) düğmesine basın.
3. Açılan pencerede **"Instagram Test Kullanıcısı"** (Instagram Tester) seçeneğini seçin.
4. Arama kutusuna **saripartners** yazın, çıkan hesabı seçin ve **Ekle**'ye basın.

**Telefonda:** daveti kabul edin.

5. Instagram'da @saripartners hesabındayken: **profil** → **☰** → **"Web siteleri ve uygulamalar"**. Bu menü "Hesap Merkezi" veya "Ayarlar ve hareketler" altında olabilir; bulamazsanız ayarların en üstündeki arama kutusuna "uygulamalar" yazın.
6. **"Test kullanıcısı davetleri"** (Tester Invites) sekmesine dokunun.
7. `SariPartners Icerik` davetinin yanındaki **"Kabul et"**e dokunun.

> Davet görünmüyorsa bilgisayardan **instagram.com** adresine @saripartners ile girin. Sonra **Ayarlar → Web siteleri ve uygulamalar → Test kullanıcısı davetleri** yolunu izleyin.

✅ Davet kabul edildi.

---

## BÖLÜM 5: Anahtarı (token) üretin (bilgisayarda, 3 dakika)

1. Uygulama panelinde sol menüde **"Instagram"** → **"API setup with Instagram business login"** (Instagram işletme girişi ile API kurulumu) yazısına basın.
   Bu yazıyı göremiyorsanız sol menüde **"Kullanım alanları"** (Use cases) → Instagram satırındaki **"Özelleştir"** (Customize) düğmesine basın.
2. Sayfada **"1. Generate access tokens"** başlığını bulun.
3. **"Add account"** (Hesap ekle) düğmesine basın.
4. Küçük bir Instagram giriş penceresi açılır. **@saripartners** kullanıcı adı ve şifresiyle giriş yapın.
   - Pencere açılmıyorsa tarayıcı açılır pencereyi engelliyordur. Adres çubuğunun sağındaki 🚫 simgesine basıp **"Her zaman izin ver"**i seçin ve tekrar deneyin.
5. İzinler ekranında **hepsini işaretli bırakın** ve **"İzin ver"** (Allow) deyin.
6. Pencere kapanır. Listede **saripartners** görünür; yanında **"Generate token"** düğmesi vardır. Bu düğmeye basın.
7. Uyarı penceresinde **"Anladım"** kutusunu işaretleyin. Uzun bir metin (harf ve rakamlar) görünür. Bu metin **anahtardır**. Yanındaki **kopyala** düğmesine basın.

⚠️ Bu metni **sohbete, e-postaya veya WhatsApp'a yapıştırmayın.** Bir sonraki bölümde güvenli forma yapıştıracaksınız.

✅ Anahtar kopyalandı.

---

## BÖLÜM 6: Anahtarı Claude'a verin (1 dakika)

1. Bu sohbete sadece **"Token hazır"** yazın.
2. Size **güvenli bir form** açılır. Kopyaladığınız metni oraya yapıştırıp kaydedin.
3. Ben bağlantıyı test edip hesap adını ve takipçi sayısını size gösteririm.

✅ Bitti. Bundan sonra yalnızca sizin "onaylıyorum" dediğiniz gönderiler yayınlanır.

---

## Sık karşılaşılan sorunlar

| Ekranda gördüğünüz | Ne yapmalı? |
|---|---|
| "Insufficient developer role" / "Geliştirici rolü yetersiz" | Bölüm 4'ü yapın (davet + kabul). |
| Hesap listesinde Instagram hesabı yok | Bölüm 1: hesap profesyonel değil. |
| "Add account" sonrası pencere açılmıyor | Açılır pencere engelleyicisine izin verin (Bölüm 5, adım 4) veya Chrome'da deneyin. |
| "Invalid scope" / "Geçersiz izin" | Bölüm 3'te yanlış kullanım alanı seçilmiş. Yeni bir uygulama oluşturup doğru seçeneği seçin. |
| Kullanım alanı listesinde Instagram seçeneği yok | Sağ üstten dili İngilizceye çevirip *Manage messaging & content on Instagram* seçeneğini arayın. |
| Telefon doğrulama kodu gelmiyor | Numarayı +90 ile yazın; 1–2 dakika bekleyip "Tekrar gönder"e basın. |
| Instagram iki adımlı doğrulama kodu istiyor | Normaldir; telefonunuza gelen kodu girin. |

## Güvenlik

| İstediğiniz | Nasıl yapılır |
|---|---|
| Erişimi tamamen kesmek | Instagram → Ayarlar → **Web siteleri ve uygulamalar** → `SariPartners Icerik` → **Kaldır**. |
| Anahtarı yenilemek (60 günde bir) | Bölüm 5, adım 6–7'yi tekrarlayın ve bana "token yenilendi" yazın. Süre dolmadan size hatırlatırım. |
| Yayınları durdurmak | Bana "yayınları durdur" yazmanız yeterli. |
