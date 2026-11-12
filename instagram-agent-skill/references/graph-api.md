# Instagram Graph API başvuru rehberi

Meta sürümleri, metrikleri ve limitleri sık değiştirir. Buradaki bilgiyle bir API hatası çelişirse hataya güven ve güncel belgelere bak: developers.facebook.com/docs/instagram-platform.

## Kurulum

1. Instagram hesabını **İşletme** veya **İçerik Üreticisi** hesabına çevir.
2. developers.facebook.com'da bir Meta uygulaması oluştur ve **Instagram** ürününü ekle. Şunlardan birini seç:
   - **Instagram API with Instagram Login**: sunucu `graph.instagram.com`, Facebook Sayfası gerekmez.
   - **Instagram API with Facebook Login**: sunucu `graph.facebook.com`, IG hesabı bir Facebook Sayfasına bağlı olmalı.
3. İzinleri iste.
   - Instagram Login: `instagram_business_basic`, `instagram_business_content_publish`, `instagram_business_manage_comments`, `instagram_business_manage_insights`.
   - Facebook Login: `instagram_basic`, `instagram_content_publish`, `instagram_manage_comments`, `instagram_manage_insights`, `pages_show_list`, `pages_read_engagement`.
4. **Uzun ömürlü bir token** al; yaklaşık 60 gün geçerlidir ve yenilenebilir. `IG_ACCESS_TOKEN` olarak sakla. IG kullanıcı ID'sini `GET /me?fields=user_id,username` (Instagram Login) veya `GET /{page-id}?fields=instagram_business_account` (Facebook Login) ile al ve `IG_USER_ID` olarak sakla.

## Yayın akışı (iki adım)

1. **Container oluştur**: `POST /{ig-user-id}/media` → `{id}` döner.
   - Görsel: `image_url`, `caption`, isteğe bağlı `alt_text`.
   - Reels: `media_type=REELS`, `video_url`, `caption`, isteğe bağlı `cover_url`, `thumb_offset`, `share_to_feed`.
   - Hikaye: `media_type=STORIES` ile birlikte `image_url` veya `video_url`.
   - Carousel öğesi: `is_carousel_item=true` ile birlikte `image_url` veya (`media_type=VIDEO`, `video_url`).
   - Carousel ana container'ı: `media_type=CAROUSEL`, `children=id1,id2,…`, `caption`.
2. **Hazır olana kadar sorgula** (video için önemli): sonuç `FINISHED` olana kadar `GET /{container-id}?fields=status_code`. Diğer değerler: `IN_PROGRESS`, `ERROR`, `EXPIRED` (container'lar 24 saatte süresi dolar) ve `PUBLISHED`.
3. **Yayınla**: `creation_id` ile `POST /{ig-user-id}/media_publish` → medya ID'si döner.
4. **Kalıcı bağlantı**: `GET /{media-id}?fields=permalink`.

`scripts/ig_api.py` bu akışın tamamını çalıştırır.

## Medya gereksinimleri (özet)

- Görseller: yalnızca JPEG, en fazla 8 MB, en-boy oranı 4:5 ile 1.91:1 arası, genişlik 320–1440 px.
- Reels: MP4/MOV, H.264/HEVC, AAC ses, 3 sn–15 dk, 9:16 önerilir, en fazla ~300 MB.
- Carousel: API üzerinden 2–10 öğe. Uygulama daha fazlasına izin verebilir; güncel belgelere bak. Görsel ve video karıştırılabilir.
- URL'ler herkese açık ve HTTPS olmalı, giriş sayfasına yönlendirmemeli.

## Limitler

- **Yayın**: hesap başına kayan 24 saatte API ile 100 gönderi. Bir carousel 1 sayılır. `GET /{ig-user-id}/content_publishing_limit?fields=config,quota_usage` ile kontrol et.
- **Açıklama**: 2.200 karakter, ≤30 hashtag, ≤20 @etiket.
- **İstek limiti**: Business Use Case limitleri geçerlidir. Kısıtlanırsan saniyeler değil dakikalar bekle.

## İstatistikler (insights)

- Medya: `GET /{media-id}/insights?metric=…`. Yaygın metrikler: `reach`, `views`, `likes`, `comments`, `shares`, `saved` ve `total_interactions`. Reels için `ig_reels_avg_watch_time` da vardır. `impressions`/`plays` kullanımdan kaldırıldı, yerine `views` geldi. Bir metrik hata verirse onu çıkarıp tekrar dene.
- Hesap: `GET /{ig-user-id}/insights?metric=reach,views,accounts_engaged,total_interactions&period=day&metric_type=total_value`.
- Veriler biraz gecikmeli gelir; 100'den az takipçisi olan hesaplar demografik veri alamayabilir.

## Yorumlar

- Listele: `GET /{media-id}/comments?fields=id,text,username,timestamp,like_count,replies{id,text,username}`.
- Yanıtla: `message` ile `POST /{comment-id}/replies`.
- Gizle/göster: `hide=true|false` ile `POST /{comment-id}`.
- Sil: `DELETE /{comment-id}`. Yalnızca kullanıcı açıkça isterse yap.

## Yaygın hatalar

| code / subcode | Anlamı | Çözüm |
|---|---|---|
| 190 | Token geçersiz/süresi dolmuş | Uzun ömürlü token'ı yenile veya yeniden oluştur |
| 10 / 200 | İzin eksik | İzni ekle ve yeniden yetkilendir; uygulama App Review gerektirebilir |
| 4, 17, 32, 613 | İstek limiti aşıldı | Bekle ve sıklığı azalt |
| 9 / 2207042 | Yayın limitine ulaşıldı | `quota` ile kontrol et; 24 saatlik pencereyi bekle |
| 36003 / 2207009 | Hatalı en-boy oranı | 4:5–1.91:1 aralığına kırp |
| 9004 / 2207052 | Medya URL'si indirilemiyor | Herkese açık HTTPS URL kullan; kimlik doğrulama veya yönlendirme olmasın |
| 2207026 | Desteklenmeyen video formatı | H.264 + AAC MP4 olarak yeniden kodla |
| 2207027 | Container hazır değil | `status_code` sorgulamaya devam et |
| 24 / 2207006 | Medya/container bulunamadı veya süresi doldu | Container'ı yeniden oluştur |
