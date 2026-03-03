# Image Resizer & Cleaner

Belirtilen bir dizindeki görselleri toplu olarak yeniden boyutlandıran, EXIF verilerini temizleyen ve optimize eden Python aracı.

## 🚀 Hızlı Başlat (EXE)

Programı kurmadan doğrudan kullanmak için:
**[Görsel Boyutlandırıcıyı İndir (v1.0.0)](https://github.com/mn-su/img-resizer-and-cleaner/releases/download/v1.0.0/main.exe)**
*(Not: Bu bağlantının çalışması için Release oluşturup `main.exe` dosyasını oraya yüklemeniz gerekmektedir).*

## Özellikler

- **Gelişmiş Arayüz (Pro):** Modern, karanlık mod destekli Windows arayüzü (`main.py`).
- **Hafif Sürüm (Lite):** Hiçbir kütüphane bağımlılığı gerektirmeyen (sadece Pillow), terminal odaklı sade sürüm (`lite.py`).
- **Toplu İşlem:** Bir klasördeki tüm JPG, PNG, WEBP ve BMP dosyalarını işler.
- **Akıllı Boyutlandırma:** Verilen genişlik değerine göre en-boy oranını koruyarak yeniden boyutlandırır.
- **Gizlilik Odaklı:** Fotoğraflardaki EXIF ve metadata (konum, kamera bilgisi vb.) verilerini tamamen siler.
- **Optimizasyon:** Görselleri optimize ederek dosya boyutunu minimuma indirir.
- **Temiz Çıktı:** İşlenen dosyaları `[OrijinalKlasor]_resize` adında yeni bir klasöre kaydeder.


## Gereksinimler

- Python 3.6 veya üzeri
- Pillow kütüphanesi

## Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/mn-su/img-resizer-and-cleaner.git
   cd img-resizer-and-cleaner
   ```

2. Sürümünüze göre paketleri yükleyin:

   **Pro Sürüm (Arayüzlü) için:**
   ```bash
   pip install -r requirements.txt
   ```

   **Lite Sürüm (Terminal) için:**
   ```bash
   pip install -r requirements-lite.txt
   ```

## Kullanım

### Pro Sürüm (Arayüzlü):
Terminalde hiçbir parametre vermeden çalıştırın:
```bash
python main.py
```

### Lite Sürüm (Terminal):
```bash
python lite.py --path "/Resimlerin/Oldugu/Klasor" --width 1024
```

*Bu komut, belirtilen klasördeki resimleri 1024px genişliğe ayarlar.*

**Kalite Ayarı ile Kullanım (Opsiyonel):**
```bash
python main.py --path "/Resimlerin/Oldugu/Klasor" --width 1920 --quality 90
```
*Varsayılan kalite: 85*

### Parametreler

- `--path`: İşlenecek resimlerin bulunduğu klasörün tam yolu (Zorunlu).
- `--width`: Hedef genişlik değeri piksel cinsinden (Zorunlu).
- `--quality`: JPG ve WEBP için sıkıştırma kalitesi. 1-100 arası değer. (Varsayılan: 85).

## Lisans

Bu proje MIT lisansı altında dağıtılmaktadır.
