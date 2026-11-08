# =====================================================================
#  SESLİ CHATBOT
#  Kural tabanlı bir chatbot: Yapay zekâ kullanmaz. Yazdığın cümlede
#  belirli ANAHTAR KELİMELERİ arar ve bulduğu kelimeye göre hazır bir
#  cevap verir. Cevabı hem ekrana yazar hem de pyttsx3 ile sesli okur.
#
#  Akış:
#  Sen yazarsın -> küçük harfe çevrilir -> anahtar kelime aranır
#  -> cevap seçilir -> ekrana yazılır -> sesli okunur
# =====================================================================


# ---------------------------------------------------------------------
# 1. KÜTÜPHANELER
# ---------------------------------------------------------------------
import random            # Şakalardan rastgele birini seçmek için
import urllib.request    # İnternetten hava durumunu çekmek için (Python'la hazır gelir)
import urllib.parse      # İnternet adresini (URL) doğru biçimde oluşturmak için
from datetime import datetime  # Bugünün tarihini, gününü ve saatini öğrenmek için
import pyttsx3           # Yazıyı sese çevirmek için (ödevin zorunlu modülü)
import comtypes.client   # Windows'taki Türkçe sesi bulmak için (pyttsx3 ile birlikte kurulu gelir)


# ---------------------------------------------------------------------
# 2. SES MOTORUNU HAZIRLAMA
# ---------------------------------------------------------------------
motor = pyttsx3.init()          # Konuşma motorunu oluştur
motor.setProperty("rate", 150)  # Konuşma hızı (varsayılan ~200). Küçük sayı = daha yavaş


# ---------------------------------------------------------------------
# 3. TÜRKÇE SESİ SEÇME
# Sorun : pyttsx3'ün kendi ses listesinde sadece İngilizce ses (Zira) var,
#         Türkçe cümleleri İngilizce aksanla okuyor.
# Sebep : Windows'ta "Microsoft Tolga" adlı Türkçe bir ses var ama Windows
#         onu pyttsx3'ün bakmadığı ayrı bir yerde (Speech_OneCore) tutuyor.
# Çözüm : Sesi o yerden kendimiz bulup pyttsx3'ün motoruna doğrudan veriyoruz.
# Not   : _driver ve _tts, pyttsx3'ün iç (resmi olmayan) parçalarıdır.
#         Tolga sesi olmayan bilgisayarda "if" hiç çalışmaz, program hata
#         vermeden İngilizce sesle devam eder.
# ---------------------------------------------------------------------
kategori = comtypes.client.CreateObject("SAPI.SpObjectTokenCategory")  # Windows ses sistemine bağlan
kategori.SetId(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)  # Tolga'nın bulunduğu yere bak
sesler = kategori.EnumerateTokens()   # Oradaki sesleri listele
for i in range(sesler.Count):         # Sesleri tek tek gez
    if "Tolga" in sesler.Item(i).GetDescription():   # Adında "Tolga" geçeni bul
        motor.proxy._driver._tts.Voice = sesler.Item(i)  # pyttsx3'e o sesi ver


# ---------------------------------------------------------------------
# 4. KONUŞ FONKSİYONU: Verilen metni sesli okur
# ---------------------------------------------------------------------
def konus(metin):
    # Sesli okunurken garip duyulacak işaretleri temizle:
    #   "+10°C" -> "10 derece",  "->" -> ":",  tırnak (') işaretleri silinir
    metin = metin.replace("°C", " derece").replace("+", "").replace("->", ":").replace("'", "")
    motor.say(metin)      # Okunacak metni sıraya koy
    motor.runAndWait()    # Oku ve bitene kadar bekle


# ---------------------------------------------------------------------
# 5. HAZIR VERİLER
# ---------------------------------------------------------------------
# Python günleri sayı olarak verir (Pazartesi = 0 ... Pazar = 6).
# Bu liste sayıyı Türkçe gün adına çevirir.
GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

# Aynı işi aylar için yapar (Ocak = 1. ay, ama listede 0. sırada)
AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
         "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

# "Şaka anlat" denince içinden rastgele biri seçilir. İstediğin kadar ekleyebilirsin.
SAKALAR = [
    "Bilgisayar neden üşümüş? Çünkü Windows'u açık bırakmış!",
    "Programcı neden denize girmemiş? Çünkü bug'lardan korkuyormuş!",
    "Temel'e sormuşlar: En sevdiğin dil hangisi? Demiş: Python, çünkü yılan gibi kıvrak!",
]


# ---------------------------------------------------------------------
# 6. HAVA DURUMU FONKSİYONU
# wttr.in adlı ücretsiz siteden canlı sıcaklığı çeker (hesap/anahtar istemez).
# Şehir verilmezse, şehri internet bağlantına göre kendisi tahmin eder.
# ---------------------------------------------------------------------
def hava_durumu(sehir=""):
    try:
        # %l = konum, %t = sıcaklık  -> örnek sonuç: "Istanbul: +10°C"
        adres = "https://wttr.in/" + urllib.parse.quote(sehir) + "?format=%l:+%t"
        istek = urllib.request.Request(adres, headers={"User-Agent": "curl"})
        # timeout=8: Site 8 saniye içinde cevap vermezse beklemeyi bırak
        with urllib.request.urlopen(istek, timeout=8) as yanit:
            return "Şu an " + yanit.read().decode("utf-8").strip()
    except Exception:
        # İnternet yoksa veya site çalışmıyorsa program çökmesin, bu mesajı versin
        return "Hava durumuna şu an ulaşamadım, internet bağlantını kontrol et."


# ---------------------------------------------------------------------
# 7. KÜÇÜLT FONKSİYONU: Metni Türkçeye uygun şekilde küçük harfe çevirir
# Python'un .lower() komutu Türkçe harflerde hata yapar:
#   "I" harfini "ı" değil "i" yapar, "İ" harfini de bozar.
# Bu yüzden önce bu iki harfi elle düzeltip sonra küçültüyoruz.
# Böylece "SAAT KAÇ", "Saat kaç" ve "saat kaç" aynı şekilde anlaşılır.
# ---------------------------------------------------------------------
def kucult(metin):
    # strip(): Baştaki ve sondaki boşlukları siler
    return metin.replace("İ", "i").replace("I", "ı").lower().strip()


# ---------------------------------------------------------------------
# 8. CEVAP VER FONKSİYONU: Botun beyni
# Mesajdaki anahtar kelimeleri YUKARIDAN AŞAĞIYA sırayla kontrol eder ve
# eşleşen İLK kuralın cevabını döndürür.
# Sıra önemli: "Selam, saat kaç?" yazılırsa cevap SAAT olur, çünkü
# "saat" kuralı "selam" kuralından önce kontrol ediliyor.
#
# YENİ SORU EKLEMEK İÇİN: En alttaki "return" satırının üstüne şunu yaz:
#     if "en sevdiğin renk" in m:
#         return "Mavi!"
# ---------------------------------------------------------------------
def cevap_ver(mesaj):
    m = kucult(mesaj)         # Mesajı küçük harfe çevir
    simdi = datetime.now()    # Şu anki tarih ve saat

    # Hava durumu
    if "hava" in m or "derece" in m:
        return hava_durumu()

    # Gün ve tarih -> örnek: "Bugün Pazar, 8 Kasım 2026."
    if "günlerden" in m or "hangi gün" in m or "bugün ne" in m:
        return f"Bugün {GUNLER[simdi.weekday()]}, {simdi.day} {AYLAR[simdi.month - 1]} {simdi.year}."

    # Saat -> %H = saat, %M = dakika  (örnek: "18:47")
    if "saat" in m:
        return f"Saat şu an {simdi.strftime('%H:%M')}."

    # Selamlaşma
    if "selam" in m or "merhaba" in m:
        return "Selam! Sana nasıl yardımcı olabilirim?"

    # Hal hatır
    if "nasılsın" in m:
        return "İyiyim, teşekkürler! Sen nasılsın?"

    # Bot kendini tanıtır
    if "adın" in m or "kimsin" in m:
        return "Ben Python ile yazılmış basit bir chatbotum."

    # Rastgele şaka
    if "şaka" in m or "fıkra" in m:
        return random.choice(SAKALAR)

    # Sorulabilecek soruların listesi ("\n" = yeni satır)
    if "soru" in m or "yardım" in m or "neler yapabilirsin" in m:
        return ("Bana şu soruları sorabilirsin (büyük/küçük harf fark etmez):\n"
                "  1. Hava durumu  -> 'Bugün hava kaç derece?' veya 'Hava nasıl?'\n"
                "  2. Gün / tarih  -> 'Günlerden ne?' veya 'Bugün hangi gün?'\n"
                "  3. Saat         -> 'Saat kaç?'\n"
                "  4. Selamlaşma   -> 'Selam' veya 'Merhaba'\n"
                "  5. Hal hatır    -> 'Nasılsın?'\n"
                "  6. Bot kim      -> 'Adın ne?' veya 'Kimsin?'\n"
                "  7. Şaka         -> 'Şaka anlat' veya 'Fıkra anlat'\n"
                "  8. Bu liste     -> 'Sorular?' veya 'Yardım'\n"
                "Çıkmak için 'çık' yaz.")

    # Hiçbir kural eşleşmediyse
    return "Bunu anlamadım. Ne sorabileceğini görmek için 'Sorular?' yaz."


# ---------------------------------------------------------------------
# 9. ANA DÖNGÜ
# Bu kısım sadece dosya doğrudan çalıştırıldığında (python chatbot.py) çalışır.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print("Chatbot hazır! 'Sorular?' yazarak neler sorabileceğini gör, çıkmak için 'çık' yaz.\n")

    while True:                          # Sonsuz döngü: sen çıkana kadar devam eder
        mesaj = input("Sen: ")           # Senden mesaj al

        if kucult(mesaj) in ("çık", "cik", "exit"):   # "çık" yazdıysan
            print("Bot: Görüşürüz!")
            break                        # Döngüden çık, program biter

        cevap = cevap_ver(mesaj)         # Cevabı bul
        print("Bot:", cevap, "\n")       # Ekrana yaz
        konus(cevap)                     # Sesli oku
