# 🔊 Sesli Chatbot (pyttsx3)

Python ile yazılmış, **kural tabanlı** ve **sesli** bir chatbot. Yapay zekâ kullanmaz: yazdığın cümlede belirli anahtar kelimeleri arar, eşleşen kurala göre hazır bir cevap verir. Cevabı hem ekrana yazar hem de `pyttsx3` ile **Türkçe sesle** okur.

## 📁 Dosyalar

| Dosya | Açıklama |
|---|---|
| `main.py` | `pyttsx3` kütüphanesinin temel deneme dosyası: konuşma hızı, ses seviyesi, ses seçimi ve sesi dosyaya kaydetme örnekleri. |
| `chatbot.py` | Asıl proje: anahtar kelimelere göre cevap veren, cevabı sesli okuyan Türkçe chatbot. |

## ⚙️ Kurulum

Gereksinimler: **Python 3.8+** ve **Windows** (Türkçe ses için).

```bash
pip install pyttsx3
```

> `comtypes` paketi Windows'ta `pyttsx3` ile birlikte otomatik kurulur.
> `urllib`, `random` ve `datetime` Python ile hazır gelir.

## ▶️ Çalıştırma

**pyttsx3 denemesi:**
```bash
python main.py
```
Ekrana mevcut konuşma hızını ve ses seviyesini yazar, "Hello World!" der ve sesi `test.mp3` dosyasına kaydeder.

**Chatbot:**
```bash
python chatbot.py
```
Çıkmak için `çık` (veya `cik` / `exit`) yaz.

## 💬 Chatbot'a Sorabileceklerin

Büyük/küçük harf fark etmez (`SAAT KAÇ` = `saat kaç`).

| Konu | Örnek soru | Örnek cevap |
|---|---|---|
| 🌤️ Hava durumu | `Hava nasıl?`, `Bugün hava kaç derece?` | Şu an Istanbul: +10°C |
| 📅 Gün / tarih | `Günlerden ne?`, `Bugün hangi gün?` | Bugün Pazar, 8 Kasım 2026. |
| 🕒 Saat | `Saat kaç?` | Saat şu an 18:47. |
| 👋 Selamlaşma | `Selam`, `Merhaba` | Selam! Sana nasıl yardımcı olabilirim? |
| 🙂 Hal hatır | `Nasılsın?` | İyiyim, teşekkürler! Sen nasılsın? |
| 🤖 Bot kim | `Adın ne?`, `Kimsin?` | Ben Python ile yazılmış basit bir chatbotum. |
| 😄 Şaka | `Şaka anlat`, `Fıkra anlat` | (Listeden rastgele bir şaka) |
| ❓ Yardım | `Sorular?`, `Yardım` | Sorulabilecek soruların listesi |

### Örnek konuşma

```
Chatbot hazır! 'Sorular?' yazarak neler sorabileceğini gör, çıkmak için 'çık' yaz.

Sen: Selam
Bot: Selam! Sana nasıl yardımcı olabilirim?

Sen: Saat kaç?
Bot: Saat şu an 18:47.

Sen: çık
Bot: Görüşürüz!
```

## 🧠 Nasıl Çalışır?

```
Sen yazarsın → küçük harfe çevrilir → anahtar kelime aranır → cevap seçilir → ekrana yazılır → sesli okunur
```

- **`kucult()`** — Python'un `.lower()` komutu Türkçe `I/İ` harflerini yanlış çevirir; bu fonksiyon önce onları düzeltip sonra küçültür.
- **`cevap_ver()`** — Kurallar **yukarıdan aşağıya** kontrol edilir, eşleşen ilk kuralın cevabı döner. Örneğin `Selam, saat kaç?` yazılırsa cevap *saat* olur, çünkü o kural daha önce kontrol edilir.
- **`hava_durumu()`** — Ücretsiz [wttr.in](https://wttr.in) servisinden canlı sıcaklığı çeker (API anahtarı gerekmez). Şehri internet bağlantısına göre tahmin eder. İnternet yoksa program çökmez, uyarı mesajı verir.
- **`konus()`** — Cevabı sesli okur; okurken garip duyulacak işaretleri temizler (`°C` → "derece" gibi).
- **Türkçe ses** — `pyttsx3` normalde sadece İngilizce sesleri görür. Windows'taki Türkçe **Microsoft Tolga** sesi `Speech_OneCore` altında durduğu için `comtypes` ile oradan bulunup motora verilir. Tolga sesi yoksa program hata vermeden İngilizce sesle devam eder.

> 💡 Bilgisayarında Türkçe ses yoksa: **Ayarlar → Saat ve dil → Konuşma → Ses ekle → Türkçe**.

## ➕ Yeni Soru Eklemek

`chatbot.py` içindeki `cevap_ver()` fonksiyonunda, en alttaki `return` satırının üstüne ekle:

```python
if "en sevdiğin renk" in m:
    return "Mavi!"
```

Yeni şaka eklemek için `SAKALAR` listesine bir cümle eklemen yeterli.

## 🛠️ Kullanılan Teknolojiler

- [pyttsx3](https://pypi.org/project/pyttsx3/) — Metni sese çevirme (çevrimdışı çalışır)
- comtypes — Windows ses sistemine (SAPI) erişim
- urllib — Hava durumu için internet isteği
- [wttr.in](https://wttr.in) — Ücretsiz hava durumu servisi
