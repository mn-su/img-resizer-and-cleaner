# Image Resizer & Cleaner

Belirtilen bir dizindeki görselleri toplu olarak yeniden boyutlandıran, EXIF verilerini temizleyen ve optimize eden Python aracı.

## Özellikler

- **Toplu İşlem:** Bir klasördeki tüm JPG, PNG, WEBP ve BMP dosyalarını işler.
- **Akıllı Boyutlandırma:** Verilen genişlik değerine göre en-boy oranını koruyarak yeniden boyutlandırır.
- **Gizlilik Odaklı:** Fotoğraflardaki EXIF ve metadata (konum, kamera bilgisi vb.) verilerini tamamen siler.
- **Optimizasyon:** Görselleri optimize ederek dosya boyutunu minimuma indirir (LANCZOS filtresi kullanılır).
- **Temiz Çıktı:** İşlenen dosyaları `[OrijinalKlasor]_resize` adında yeni bir klasöre kaydeder, orijinal dosyaları değiştirmez.

## Gereksinimler

- Python 3.6 veya üzeri
- Pillow kütüphanesi

## Kurulum

1. Depoyu klonlayın veya indirin:
   ```bash
   git clone https://github.com/mn-su/img-resizer-and-cleaner.git
   cd img-resizer-and-cleaner
   ```

2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## Kullanım

Aracı terminal veya komut satırı üzerinden çalıştırabilirsiniz.

**Temel Kullanım:**
```bash
python main.py --path "/Resimlerin/Oldugu/Klasor" --width 1024
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
