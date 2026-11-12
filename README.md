# Instagram Agent Skill

Instagram içeriği planlamak, yazmak, kontrol etmek ve yayınlamak için bir [Claude Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview). Resmi Instagram Graph API'yi kullanır.

```
instagram-agent-skill/
├── SKILL.md                     # giriş noktası: Claude skill'i ne zaman ve nasıl kullanır
├── references/
│   ├── content-guide.md         # kancalar, açıklama yapısı, formatlar, hashtag'ler, takvim
│   └── graph-api.md             # kurulum, yayın akışı, limitler, istatistikler, hata tablosu
└── scripts/
    ├── caption_check.py         # açıklama kontrolü (uzunluk, hashtag, etiket, "…devamı", spam)
    └── ig_api.py                # Graph API komut satırı aracı: yayın, istatistik, yorum (yalnızca standart kütüphane)
```

## Kurulum

- **Claude Code**: `instagram-agent-skill/` klasörünü `~/.claude/skills/instagram/` (kişisel) veya `.claude/skills/instagram/` (proje) altına kopyala.
- **Claude.ai / Desktop**: `instagram-agent-skill` klasörünü zip'le ve Ayarlar → Yetenekler → Skills altından yükle.
- **Claude API / Agent SDK**: özel skill olarak yükle.

## Yapılandırma (yalnızca yayın, istatistik ve yorumlar için gerekli)

```bash
export IG_ACCESS_TOKEN=...        # uzun ömürlü token; asla commit'leme
export IG_USER_ID=...             # Instagram profesyonel hesap ID'si
export IG_GRAPH_HOST=graph.instagram.com   # "Instagram Login" kullanıyorsan; varsayılan graph.facebook.com
```

Uygulama kurulumu ve izinler için `instagram-agent-skill/references/graph-api.md` dosyasına bak.

## Örnek istekler

- "Yeni yulaf sütlü latte lansmanımız için 3 açıklama seçeneği yaz, eğlenceli ton, amaç = kaydetme."
- "Bu blog yazısını alt text'leriyle birlikte 7 slaytlık bir carousel taslağına dönüştür."
- "Paketleme sürecimizi gösteren 20 saniyelik bir Reels senaryosu yaz."
- "Bu açıklamayı Instagram limitlerine göre kontrol et."
- "Bu görsel URL'leriyle carousel'i yayınla." (Claude önce deneme çalıştırmasını gösterir, yalnızca sen onayladıktan sonra yayınlar.)
- "Son 5 gönderim nasıl performans gösterdi? Neyi daha çok paylaşmalıyım?"

## Güvenlik

`--yes` verilmedikçe her yazma komutu deneme çalıştırmasıdır. Claude'a yayınlamadan veya yanıtlamadan önce senden onay alması söylenmiştir. Skill; veri kazımayı, takip/beğeni/DM otomasyonunu ve şifreyle girişi reddeder.
