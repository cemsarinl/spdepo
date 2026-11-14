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

## BÖLÜM 5: Anahtarı (token) üretin (bilgisayarda, 5 dakika)

> **İpucu:** Meta'nın Türkçe çevirileri değişken. Sayfanın en altındaki dil seçicisinden **English (US)**'yi seçerseniz ekrandaki yazılar bu rehberdekilerle birebir aynı olur.

### 5A. Uygulamanızın paneline girin

1. Chrome'da **developers.facebook.com/apps** adresine gidin.
2. Uygulamalarınızın listesi açılır. **SariPartners Icerik** kutusuna tıklayın.
3. Uygulama paneli (**Dashboard / Pano**) açılır. Sol tarafta dikey bir menü görürsünüz.
   - Sol menü görünmüyorsa pencere dar olabilir. Sol üstteki **☰** simgesine basın veya pencereyi büyütün.

### 5B. Instagram ayar sayfasını bulun

4. Sol menüde **"Use cases"** (Türkçe ekranda "Kullanım durumları" veya "Kullanım örnekleri") yazısına tıklayın.
5. Ortada bir kart listesi açılır. **"Manage messaging & content on Instagram"** kartını bulun.
6. Bu kartın sağındaki **"Customize"** (Özelleştir) düğmesine basın.
7. Yeni sayfanın solunda iki-üç sekme görünür. **"API setup with Instagram business login"** sekmesine tıklayın.
   (Diğer sekmeler "Permissions and features" ve "API setup with Facebook login"dur; onlara dokunmayın.)

**Kart listede yoksa:** Uygulamayı oluştururken başka bir kullanım alanı seçilmiş demektir. Aynı sayfanın sağ üstündeki **"Add use case"** (Kullanım alanı ekle) düğmesine basın, **"Manage messaging & content on Instagram"**ı seçip ekleyin, sonra 5. adıma dönün.

### 5C. Anahtarı üretin

8. Açılan sayfada numaralı başlıklar görürsünüz. En üsttekine bakın: **"1. Generate access tokens"**.
9. Bu başlığın altındaki **"Add account"** düğmesine basın.
10. Küçük bir Instagram penceresi açılır. **saripartners** kullanıcı adı ve şifresiyle giriş yapın.
    - Pencere açılmıyorsa adres çubuğunun sağındaki 🚫 simgesine basın, **"Her zaman izin ver"**i seçin ve **Add account**'a tekrar basın.
    - Pencerede başka bir Instagram hesabı açık geliyorsa **"Siz değil misiniz?"** / **"Hesap değiştir"** deyip saripartners ile girin.
11. İzinler ekranında hiçbir işareti kaldırmayın ve **"Allow"** (İzin ver) düğmesine basın.
12. Pencere kapanır. "1. Generate access tokens" başlığının altında **saripartners** satırı görünür.
13. Bu satırın sağındaki **"Generate token"** düğmesine basın.
14. Açılan pencerede **"I Understand"** (Anladım) kutusunu işaretleyin.
15. Harf ve rakamlardan oluşan uzun bir metin görünür. Bu metin **anahtardır**. Yanındaki **kopyala** simgesine (iki üst üste kâğıt) basın.

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
