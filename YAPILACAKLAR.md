# YAPILACAKLAR

> **Durum:** Henüz başlatılmadı.  
> Bu dosya fabrika şablon reposunda **bilerek boştur**. Proje faz planı yalnızca sizin komutunuzla oluşturulur.

<!-- yapilacaklar-state: uninitialized -->

| Alan | Değer |
|------|-------|
| Proje | *(henüz tanımlanmadı)* |
| Package | *(henüz tanımlanmadı)* |
| Fabrika sürümü | v3.1.0-intelligence-operational |
| Oluşturulma | — |
| Aktif faz | — |
| Kaynak prompt | — |

---

## Nasıl başlatılır?

| Yol | Ne yapar? |
|-----|-----------|
| **Cursor `/baslat`** | Promptunuzdan F0–F8 planı üretir; F0 `işleniyor` |
| **`init-new-app.sh`** | Yeni uygulama + governance + dolu `YAPILACAKLAR.md` |
| **`init-yapilacaklar.sh`** | Mevcut projede şablondan plan oluşturur |

```bash
# Yeni Android uygulaması
./scripts/init-new-app.sh "My App" "com.example.myapp"

# Veya Cursor chat
/baslat
<ürün promptunuz>
```

**Şablon:** [`templates/YAPILACAKLAR.template.md`](templates/YAPILACAKLAR.template.md)  
**Sistem:** [`docs/YAPILACAKLAR_SISTEMI.md`](docs/YAPILACAKLAR_SISTEMI.md)

---

*Fabrika reposunda F0–F8 tabloları burada görünmez — bunlar uygulama projesine özeldir.*
