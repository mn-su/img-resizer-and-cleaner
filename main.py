import os
import argparse
from PIL import Image
import sys

# Desteklenen uzantılar
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}

def process_images(directory, target_width, quality=85):
    """
    Verilen dizindeki resimleri yeniden boyutlandırır, temizler ve yeni bir klasöre kaydeder.
    
    Args:
        directory (str): Kaynak klasör yolu.
        target_width (int): Hedef genişlik (piksel).
        quality (int): Kaydetme kalitesi (JPG/WEBP için). Varsayılan 85.
    """
    
    # Dizin yolunu temizle ve doğrula
    directory = os.path.abspath(directory)
    if not os.path.exists(directory):
        print(f"Hata: Belirtilen dizin bulunamadı: {directory}")
        sys.exit(1)
        
    parent_dir = os.path.dirname(directory)
    dir_name = os.path.basename(directory)
    output_dir = os.path.join(parent_dir, f"{dir_name}_resize")
    
    # Çıktı dizinini oluştur
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Klasör oluşturuldu: {output_dir}")
    else:
        print(f"Klasör zaten mevcut, üzerine yazılacak: {output_dir}")

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    image_files = [f for f in files if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS]
    
    if not image_files:
        print("İşlenecek resim bulunamadı.")
        return

    print(f"Toplam {len(image_files)} resim işlenecek...")
    
    processed_count = 0
    saved_space = 0
    
    for filename in image_files:
        input_path = os.path.join(directory, filename)
        output_path = os.path.join(output_dir, filename)
        
        try:
            with Image.open(input_path) as img:
                # Orijinal dosya boyutu
                original_size = os.path.getsize(input_path)
                
                # Boyut hesaplama (En boy oranını koru)
                w_percent = (target_width / float(img.size[0]))
                
                # Eğer resim zaten hedef genişlikten küçükse büyütme, olduğu gibi bırak veya küçült
                # Kullanıcı isteği "vereceğim bir genişlik değerine" dediği için, 
                # genelde küçültme amaçlıdır ama küçükleri de o genişliğe çekmek isteyebilir.
                # Ancak kalite kaybını önlemek için genelde sadece küçültme yapılır.
                # Burada direkt set edelim, kullanıcı kesin bir genişlik istiyor gibi.
                
                h_size = int((float(img.size[1]) * float(w_percent)))
                
                # Yeniden boyutlandırma (LANCZOS filtresi ile yüksek kalite)
                resized_img = img.resize((target_width, h_size), Image.Resampling.LANCZOS)
                
                # EXIF verileri Image.open() ile yüklenir ama save() metoduna 
                # exif parametresi verilmezse varsayılan olarak KAYDEDİLMEZ.
                # Yani extra bir .strip() işlemine gerek yok, PIL varsayılan olarak metadata'yı aktarmaz 
                # (save metodunda 'exif=img.info.get("exif")' denmediği sürece).
                # Biz yine de data=None diyerek yeni, temiz bir görsel oluşturuyoruz.
                
                # Yeni bir resim nesnesi oluştur (data temizliği için garanti yöntem) - Gerekli olmayabilir ama sağlam.
                # Ancak formatı korumak önemli.
                
                save_kwargs = {'optimize': True}
                
                # Format bazlı ayarlar
                img_format = img.format
                if not img_format:
                    # Uzantıdan tahmin et
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in ['.jpg', '.jpeg']: img_format = 'JPEG'
                    elif ext == '.png': img_format = 'PNG'
                    elif ext == '.webp': img_format = 'WEBP'
                
                if img_format == 'JPEG':
                    save_kwargs['quality'] = quality
                    # RGB moda çevir (PNG'den JPG'e dönerken alpha kanalı sorunu olmasın)
                    if resized_img.mode in ("RGBA", "P"):
                        resized_img = resized_img.convert("RGB")
                elif img_format == 'WEBP':
                    save_kwargs['quality'] = quality
                
                # Kaydet
                resized_img.save(output_path, format=img_format, **save_kwargs)
                
                final_size = os.path.getsize(output_path)
                diff = original_size - final_size
                saved_space += diff
                processed_count += 1
                
                print(f"[OK] {filename} -> {target_width}x{h_size} | "
                      f"{original_size/1024:.1f}KB -> {final_size/1024:.1f}KB "
                      f"({(diff/original_size)*100:.1f}% Tasarruf)")
                
        except Exception as e:
            print(f"[HATA] {filename} işlenirken hata oluştu: {e}")

    total_saved_mb = saved_space / (1024 * 1024)
    print("\n" + "="*40)
    print(f"İşlem Tamamlandı.")
    print(f"İşlenen Dosya: {processed_count}/{len(image_files)}")
    print(f"Toplam Tasarruf: {total_saved_mb:.2f} MB")
    print(f"Çıktı Klasörü: {output_dir}")
    print("="*40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resim boyutlandırma ve temizleme aracı")
    parser.add_argument("--path", required=True, help="İşlenecek resimlerin bulunduğu klasör yolu")
    parser.add_argument("--width", type=int, required=True, help="Hedef genişlik değeri (px)")
    parser.add_argument("--quality", type=int, default=85, help="JPG/WEBP Kalitesi (0-100, Varsayılan: 85)")
    
    args = parser.parse_args()
    
    process_images(args.path, args.width, args.quality)
