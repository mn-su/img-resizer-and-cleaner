"""
Image Resizer & Cleaner (Lite)
Author: mn-su
License: MIT
Description: Lightweight CLI-based batch image resizer and EXIF cleaner.
"""
import os
import argparse
from PIL import Image
import sys

# Desteklenen uzantılar
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}

def process_images(directory, target_width, quality=85):
    """
    Verilen dizindeki resimleri yeniden boyutlandırır, temizler ve yeni bir klasöre kaydeder.
    """
    
    directory = os.path.abspath(directory)
    if not os.path.exists(directory):
        print(f"Hata: Belirtilen dizin bulunamadı: {directory}")
        sys.exit(1)
        
    parent_dir = os.path.dirname(directory)
    dir_name = os.path.basename(directory)
    output_dir = os.path.join(parent_dir, f"{dir_name}_resize")
    
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
                original_size = os.path.getsize(input_path)
                w_percent = (target_width / float(img.size[0]))
                h_size = int((float(img.size[1]) * float(w_percent)))
                
                resized_img = img.resize((target_width, h_size), Image.Resampling.LANCZOS)
                
                save_kwargs = {'optimize': True}
                img_format = img.format
                if not img_format:
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in ['.jpg', '.jpeg']: img_format = 'JPEG'
                    elif ext == '.png': img_format = 'PNG'
                    elif ext == '.webp': img_format = 'WEBP'
                
                if img_format == 'JPEG':
                    save_kwargs['quality'] = quality
                    if resized_img.mode in ("RGBA", "P"):
                        resized_img = resized_img.convert("RGB")
                elif img_format == 'WEBP':
                    save_kwargs['quality'] = quality
                
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
    parser = argparse.ArgumentParser(description="Image Resizer (Lite Version - CLI Only)")
    parser.add_argument("--path", required=True, help="Klasör yolu")
    parser.add_argument("--width", type=int, required=True, help="Hedef genişlik (px)")
    parser.add_argument("--quality", type=int, default=85, help="Kalite (1-100)")
    
    args = parser.parse_args()
    process_images(args.path, args.width, args.quality)
