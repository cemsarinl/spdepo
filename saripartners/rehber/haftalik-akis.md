# Haftalık iş akışı (Claude için çalışma talimatı)

Bu dosya, zamanlanmış görevler tetiklendiğinde Claude'un izleyeceği adımları tanımlar.

## A. Haftalık taslak hazırlama (her Pazar, 20:47; paket Pazar akşamı kullanıcıya gönderilir)

1. `rehber/uyum-kurallari.md`, `rehber/seri-plani.md`, `takvim/ozel-gunler.md` ve `marka.json` dosyalarını oku. Görsel kimlik kurallarına ve seri planına uy; Alan Rehberi sırasını takip et.
2. **Gündem araştırması** (son 7 gün; `icerik-plani.md` §3). İnsanların gündemde karşılaştığı durumları ve bu durumlardaki haklarını ara. Mevzuat değişikliklerini yalnızca günlük hayata etkisi üzerinden ele al:
   - Resmî Gazete: yeni kanunlar, Cumhurbaşkanlığı kararnameleri ve önemli yönetmelikler
   - TBMM'de kabul edilen kanun teklifleri
   - Yargıtay İBK, Danıştay İDDK ve AYM kararları (özellikle bireysel başvuru ve iptal kararları)
   - KVKK, Rekabet Kurumu, SPK ve BDDK gibi kurumların duyuruları
   Geniş kitleyi ilgilendiren, somut ve doğrulanabilir **bir** konu seç. Her iddia için birincil kaynak (RG sayısı, karar künyesi) bul. Yalnızca haber sitesinde geçen bilgiyi `dogrulanacak` listesine yaz.
3. `icerik-plani.md` §4'e göre gelecek haftanın **Hollanda'daki Türkler** gönderisini (Çarşamba) hazırla. Konu, Türkiye'yle bağdan doğan bir hak olmalı: mal varlığı, evlilik ve boşanma, miras, sağlık ve sosyal güvenlik, vatandaşlık, askerlik. Hollanda'nın iç meselelerini işleme. Gerekirse isteğe bağlı Cuma gönderisini de hazırla. Önümüzdeki 10 günde `takvim/ozel-gunler.md`'de bir özel gün varsa onun içeriğini de hazırla.
4. Her gönderi için `icerik/YYYY-AA-GG_kisa-ad/` klasörü oluştur ve içine şu dosyaları koy: `spec.json`, `caption.txt`, `meta.json` (`durum: "taslak"`, `hukukcu_onayi: false`, `alt_text`, `kaynaklar`, `dogrulanacak`).
5. Görselleri üret ve kontrol et:
   ```bash
   node render/render.js icerik/<klasor>/spec.json
   python3 render/make_reel.py icerik/<klasor>/gorseller icerik/<klasor>/reel.mp4   # Reels için
   python3 ../instagram-agent-skill/scripts/caption_check.py --file icerik/<klasor>/caption.txt
   ```
   "sığmıyor" uyarısı veren slaytları kısalt. Görselleri bir temas sayfasında (montage) gözle kontrol et.
6. Uyum kurallarına göre son kontrolü yap: reklam dili, başarı paylaşımı ve iletişim çağrısı olmamalı, sonda yasal not bulunmalı.
7. `python3 onay_paketi.py <haftanın ilk günü> <son günü>` ile onay paketini üret. Commit'le ve push'la. Ardından kullanıcıya gönderi başına görselleri, açıklamayı, planlanan tarihi ve `dogrulanacak` maddelerini gönder ve onay iste.

## A2. @buseninhakkin kontrolü (her Pazar, A ile birlikte)

Video **indirilmez**. Yeni gönderi, "ekran görüntüsü" tarzında Sarı tasarımlı bir kart olarak @saripartners'ta Reels'e dönüştürülür.

1. `python3 repost.py kontrol` ile son kontrolden bu yana paylaşılan gönderileri listele.
2. Her gönderi için açıklamayı oku ve 2–6 kelimelik, dikkat çekici bir **kanca metni** yaz. Biçim: "Soru?\n*Vurgu.*", ikinci satır italik altın olur. Metin gönderinin konusuyla birebir örtüşmeli, abartı veya sonuç vaadi içermemeli.
3. `python3 repost.py hazirla <medya_id> <tarih> <kisa-ad> "<kanca>"` komutuyla kartı ve 8 saniyelik Reels'i hazırla. Tarih, haftanın boş bir günü olmalı.
4. "sığmıyor" uyarısı çıkarsa kanca metnini kısaltıp kartı yeniden üret. Kartı gözle kontrol et.

## A4. Aylık rakip analizi (her ayın ilk Pazarı)

1. `python3 rakip_analizi.py` çalıştır; `rakip/son_analiz.md` güncellenir.
2. `rehber/rakip-analizi.md` belgesindeki tablo ve stil kararlarını yeni verilere göre güncelle. Yeni benzer hesap bulduysan `rakip/hesaplar.json` listesine ekle.
3. @saripartners'ın son 30 günlük istatistiklerini (`ig_api.py insights`, `account-insights`) çek; en iyi çalışan konu ve formatları not et.
4. Önemli değişiklikleri haftalık onay paketinin başında kullanıcıya kısa bir özetle bildir.

## B. Onay

Kullanıcı bir gönderiyi onayladığında (ör. "16 Kasım gönderisini onaylıyorum") şunları yap:
- İstenen düzeltmeleri uygula, görselleri yeniden üret.
- `meta.json` içinde `hukukcu_onayi: true` ve `durum: "onaylandi"` değerlerini ayarla.
- Commit'le ve push'la.

## A3. Acil gündem taraması (günde 3 kez: 08:40, 13:40, 21:40)

1. `icerik-plani.md` §4'teki ölçütlere göre son saatlerin Türkiye ve Hollanda haberlerini tara.
2. Acil bir olay yoksa kısa bir not düş ve bitir; kullanıcıyı rahatsız etme.
3. Acil bir olay varsa:
   - Önce aynı olay için daha önce uyarı verilip verilmediğini `acil/kayit.json` dosyasından kontrol et.
   - Verilmediyse kullanıcıya **telefon bildirimi** (PushNotification) ve sohbet mesajı gönder. Mesajda olay, önerilen hukuki konu ve kaynak bulunsun.
   - `seri: "acil"` ile taslak hazırla ve onay iste. Kullanıcı "acil onay" derse `meta.json`'da tarihi bugün yap ve hemen yayınla.
4. Afetlerde tonla ilgili `icerik-plani.md` §4 kurallarına uy.

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
