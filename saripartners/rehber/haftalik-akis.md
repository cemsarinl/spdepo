# Haftalık iş akışı (Claude için çalışma talimatı)

Bu dosya, zamanlanmış görevler tetiklendiğinde Claude'un izleyeceği adımları tanımlar.

## A. Haftalık taslak hazırlama (her Perşembe)

1. `rehber/uyum-kurallari.md`, `rehber/seri-plani.md`, `takvim/ozel-gunler.md` ve `marka.json` dosyalarını oku. Görsel kimlik kurallarına ve seri planına uy; Alan Rehberi sırasını takip et.
2. **Hukuk gündemi araştırması** (son 7 gün):
   - Resmî Gazete: yeni kanunlar, Cumhurbaşkanlığı kararnameleri ve önemli yönetmelikler
   - TBMM'de kabul edilen kanun teklifleri
   - Yargıtay İBK, Danıştay İDDK ve AYM kararları (özellikle bireysel başvuru ve iptal kararları)
   - KVKK, Rekabet Kurumu, SPK ve BDDK gibi kurumların duyuruları
   Geniş kitleyi ilgilendiren, somut ve doğrulanabilir **bir** konu seç. Her iddia için birincil kaynak (RG sayısı, karar künyesi) bul. Yalnızca haber sitesinde geçen bilgiyi `dogrulanacak` listesine yaz.
3. Seri planındaki gelecek haftanın diğer gönderilerini (Alan Rehberi, Hukuk Sözlüğü vb.) hazırla. Önümüzdeki 10 günde `takvim/ozel-gunler.md`'de bir özel gün varsa onun içeriğini de hazırla.
4. Her gönderi için `icerik/YYYY-AA-GG_kisa-ad/` klasörü oluştur ve içine şu dosyaları koy: `spec.json`, `caption.txt`, `meta.json` (`durum: "taslak"`, `hukukcu_onayi: false`, `alt_text`, `kaynaklar`, `dogrulanacak`).
5. Görselleri üret ve kontrol et:
   ```bash
   node render/render.js icerik/<klasor>/spec.json
   python3 render/make_reel.py icerik/<klasor>/gorseller icerik/<klasor>/reel.mp4   # Reels için
   python3 ../instagram-agent-skill/scripts/caption_check.py --file icerik/<klasor>/caption.txt
   ```
   "sığmıyor" uyarısı veren slaytları kısalt. Görselleri bir temas sayfasında (montage) gözle kontrol et.
6. Uyum kurallarına göre son kontrolü yap: reklam dili, başarı paylaşımı ve iletişim çağrısı olmamalı, sonda yasal not bulunmalı.
7. Commit'le ve push'la. Ardından kullanıcıya gönderi başına görselleri, açıklamayı, planlanan tarihi ve `dogrulanacak` maddelerini gönder ve onay iste.

## A2. @buseninhakkin kontrolü (her Perşembe, A ile birlikte)

1. `python3 repost.py kontrol` ile son kontrolden bu yana paylaşılan videoları listele.
2. Her uygun video için içeriği anlamak üzere videodan birkaç kare çıkar ve açıklamayı oku. 2–6 kelimelik, dikkat çekici bir **kanca metni** yaz (ikinci satır *italik altın*). Metin videonun içeriğiyle birebir örtüşmeli, abartı veya sonuç vaadi içermemeli.
3. `python3 repost.py hazirla <medya_id> <tarih> <kisa-ad> "<Soru?\n*Vurgu.*>"` komutuyla taslağı hazırla. Tarih, haftanın boş bir günü olmalı.
4. Kareleri gözle kontrol et: şerit yüzü veya videodaki yazıları kapatmamalı.
5. Telifli müzik nedeniyle atlanan videoları `python3 repost.py isaretle <medya_id> atlandi` ile kaydet ve kullanıcıya bildir.

## B. Onay

Kullanıcı bir gönderiyi onayladığında (ör. "16 Kasım gönderisini onaylıyorum") şunları yap:
- İstenen düzeltmeleri uygula, görselleri yeniden üret.
- `meta.json` içinde `hukukcu_onayi: true` ve `durum: "onaylandi"` değerlerini ayarla.
- Commit'le ve push'la.

## C. Günlük yayın (her gün 09:50, Türkiye saati)

```bash
python3 yayinla.py --bugun          # önce deneme
python3 yayinla.py --bugun --yes    # sonra yayın
```

- Yalnızca onaylı içerik yayınlanır. Onaysız ama tarihi gelmiş bir içerik varsa yayınlama; kullanıcıya hatırlat.
- Yayından sonra `meta.json` güncellenir. Bu değişikliği commit'le, push'la ve kullanıcıya permalink'i gönder.
- Hata alırsan `instagram-agent-skill/references/graph-api.md` içindeki hata tablosuna bak. Tekrar denemeden önce kullanıcıya bildir.

## D. Aylık rapor (ayın ilk Pazartesi'si, isteğe bağlı)

`ig_api.py media` ve `insights` ile son 30 günün gönderilerini çek. Erişim, kaydetme ve paylaşım tablosunu ve en iyi performans gösteren 2 konuyu raporla.

## Yorumlar

Yorumlara Claude kendiliğinden cevap vermez. Haftalık özette yeni yorumları listeler ve kullanıcının onayladığı yanıtları gönderir.
