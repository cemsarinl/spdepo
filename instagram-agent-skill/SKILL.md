---
name: instagram
description: Bir Instagram İşletme veya İçerik Üreticisi hesabı için içerik planlama, yazma, kontrol etme ve yayınlama. Kullanıcı Instagram açıklaması (caption), hashtag, carousel veya Reels senaryosu, içerik takvimi istediğinde; bir açıklamanın Instagram limitlerine uygunluğunun kontrolünü istediğinde; Instagram Graph API üzerinden gönderi/carousel/Reels/hikaye yayınlamak, gönderi ya da hesap istatistiklerini çekmek veya yorumları okuyup yanıtlamak istediğinde kullan. Başkalarının hesaplarını kazımak (scraping), takipçi/etkileşim satın almak veya beğeni/takip/DM otomasyonu için kullanılmaz.
---

# Instagram

Bu skill iki tür işte yardımcı olur:

1. **İçerik**: açıklama, hashtag, carousel, Reels senaryosu, hikaye ve içerik takvimi yazmak.
2. **Operasyon**: resmi **Instagram Graph API** üzerinden yayınlama, istatistikler ve yorumlar (`scripts/ig_api.py`).

Kullanıcı ne istediyse oradan başla. API tarafını yalnızca bir şey yayınlanmak, ölçülmek veya yönetilmek istendiğinde devreye sok.

## 1. Brief'i topla (yalnızca eksik olanları)

- **Hesap**: niş, hedef kitle, marka sesi. Kullanıcıdan beğendiği 2–3 eski açıklamayı iste.
- **Gönderinin amacı**: erişim, kaydetme, yorum, link tıklaması, satış veya topluluk.
- **Format**: tek görsel, carousel, Reels veya hikaye.
- **Olmazsa olmazlar**: CTA (harekete geçirici çağrı), ürün, kampanya, @etiketler, konum, dil(ler).

Kullanıcı tek satır verirse ("yeni kahve lansmanımız için açıklama"), soru yağmuruna tutma. Makul varsayımlar yap, bunları tek satırda belirt ve teslim et.

## 2. İçeriği yaz

`references/content-guide.md` dosyasını izle. Kanca (hook) kalıpları, açıklama yapısı, formatlara göre yöntemler, hashtag stratejisi ve takvim şablonu oradadır. Temel kurallar:

- "…devamı"ndan önce **ilk ~125 karakter** görünür, kanca oraya gider.
- Bir gönderi, bir fikir, bir CTA.
- Formata göre yaz: Reels için ekran yazısı ve seslendirme metni, carousel için slayt slayt taslak.
- Ton belirsizse kanca veya açıklamanın **2–3 alternatifini** sun.
- Her görsel için **alternatif metin (alt text)** ekle.

Açıklamayı teslim etmeden önce kontrol aracını çalıştır:

```bash
python3 scripts/caption_check.py --file caption.txt        # veya: echo "..." | python3 scripts/caption_check.py
```

Araç uzunluğu (en fazla 2.200 karakter), hashtag ve @etiket sayısını, tekrarlanan etiketleri, sorunlu karakterleri ve kancanın "…devamı" öncesinde ne kadarının göründüğünü raporlar. Her **HATA**'yı düzelt. Her **UYARI**'yı kullanıcıya bildir.

## 3. Yayınla / ölç / yönet (Graph API)

Önce `references/graph-api.md` dosyasını oku. Kurulum, izinler, medya gereksinimleri, limitler ve hatalar oradadır.

Gereksinimler: bir Instagram **İşletme veya İçerik Üreticisi** hesabı ve `IG_ACCESS_TOKEN` ile `IG_USER_ID` ortam değişkenleri. İsteğe bağlı olarak `IG_GRAPH_HOST` ayarlanabilir: `graph.facebook.com` (varsayılan, Facebook Login için) veya `graph.instagram.com` (Instagram Login için). İsteğe bağlı olarak `IG_API_VERSION` de ayarlanabilir. **Token'ı asla ekrana yazdırma, loglama veya commit'leme.**

```bash
python3 scripts/ig_api.py whoami
python3 scripts/ig_api.py quota
python3 scripts/ig_api.py publish-image    --image-url URL --caption-file caption.txt [--alt-text "..."] --yes
python3 scripts/ig_api.py publish-carousel --media-url URL1 --media-url URL2 ... --caption-file caption.txt --yes
python3 scripts/ig_api.py publish-reel     --video-url URL --caption-file caption.txt [--cover-url URL] [--no-feed] --yes
python3 scripts/ig_api.py publish-story    --image-url URL | --video-url URL --yes
python3 scripts/ig_api.py media  [--limit 10]
python3 scripts/ig_api.py insights --media-id ID
python3 scripts/ig_api.py account-insights [--period day]
python3 scripts/ig_api.py comments --media-id ID
python3 scripts/ig_api.py reply --comment-id ID --message "..." --yes
python3 scripts/ig_api.py hide-comment --comment-id ID [--unhide] --yes
```

`--yes` olmadan her yazma komutu **deneme çalıştırması** yapar: ne göndereceğini yazdırır ve durur. Şu kurallara uy:

- Bir yazma komutunu `--yes` ile çalıştırmadan önce **her zaman** son açıklamayı ve medya listesini kullanıcıya göster ve açık onay al. Yayınlanan gönderi anında herkese açık olur.
- Medya, Meta sunucularının indirebileceği **herkese açık bir HTTPS URL**'de olmalıdır. Yerel dosyalar önce bir yere yüklenmelidir.
- Toplu yayından önce `quota` ile kotayı kontrol et.
- Hata alırsan `code`/`error_subcode` değerlerine bak ve `references/graph-api.md` içindeki hata tablosuna başvur. Körlemesine tekrar deneme.

## 4. Sonucu bildir

- İçerik için: son açıklamayı kopyalanabilir bir blokta ver, ardından hashtag'leri, alt text'i ve varsa kontrol aracı uyarılarını ekle.
- Yayın için: kalıcı bağlantıyı (permalink) ve medya ID'sini ver.
- İstatistikler için: küçük bir tablo göster, ardından gönderinin amacına bağlı 2–3 somut çıkarım yap.

## Kapsam dışı

İstense bile şunları yapma: başkalarının profillerini veya takipçi listelerini kazımak, beğeni/takip/DM otomasyonu, etkileşim satın almak, limitleri aşmaya çalışmak veya kullanıcının şifresiyle giriş yapmak. Bunlar Instagram Kullanım Koşulları'nı ihlal eder ve hesapların kapatılmasına yol açar. Bunun yerine kurallara uygun alternatifi öner: Graph API, herkese açık işletme hesabı verileri için Business Discovery veya organik taktikler.
