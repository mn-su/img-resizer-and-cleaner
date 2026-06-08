"""
Image Resizer & Cleaner (Pro)
Author: mn-su
License: MIT
Description: Modern GUI-based batch image resizer and EXIF cleaner.
"""
import os
import argparse
from PIL import Image
import sys
import threading
import customtkinter as ctk
from tkinter import filedialog

# Desteklenen uzantılar
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}

def process_images(directory, target_width, quality=85, to_webp=False, log_callback=print, progress_callback=None):
    """
    Verilen dizindeki resimleri yeniden boyutlandırır, temizler ve yeni bir klasöre kaydeder.
    """
    
    directory = os.path.abspath(directory)
    if not os.path.exists(directory):
        log_callback(f"Hata: Belirtilen dizin bulunamadı: {directory}")
        return False
        
    parent_dir = os.path.dirname(directory)
    dir_name = os.path.basename(directory)
    output_dir = os.path.join(parent_dir, f"{dir_name}_resize")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        log_callback(f"Klasör oluşturuldu: {output_dir}")
    else:
        log_callback(f"Klasör zaten mevcut, üzerine yazılacak: {output_dir}")

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    image_files = [f for f in files if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS]
    
    if not image_files:
        log_callback("İşlenecek resim bulunamadı.")
        return False

    log_callback(f"Toplam {len(image_files)} resim işlenecek...")
    
    processed_count = 0
    saved_space = 0
    total_initial_size = 0
    total_final_size = 0
    total_files = len(image_files)
    
    for i, filename in enumerate(image_files):
        input_path = os.path.join(directory, filename)
        
        filename_without_ext, _ = os.path.splitext(filename)
        output_filename = f"{filename_without_ext}.webp" if to_webp else filename
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            with Image.open(input_path) as img:
                original_size = os.path.getsize(input_path)
                total_initial_size += original_size
                orig_w, orig_h = img.size
                
                w_percent = (target_width / float(orig_w))
                h_size = int((float(orig_h) * float(w_percent)))
                
                resized_img = img.resize((target_width, h_size), Image.Resampling.LANCZOS)
                
                save_kwargs = {'optimize': True}
                img_format = img.format
                if not img_format:
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in ['.jpg', '.jpeg']: img_format = 'JPEG'
                    elif ext == '.png': img_format = 'PNG'
                    elif ext == '.webp': img_format = 'WEBP'
                
                if to_webp:
                    img_format = 'WEBP'
                
                if img_format == 'JPEG':
                    save_kwargs['quality'] = quality
                    if resized_img.mode in ("RGBA", "P"):
                        resized_img = resized_img.convert("RGB")
                elif img_format == 'WEBP':
                    save_kwargs['quality'] = quality
                    if resized_img.mode == "P":
                        resized_img = resized_img.convert("RGBA")
                    elif resized_img.mode == "CMYK":
                        resized_img = resized_img.convert("RGB")
                
                resized_img.save(output_path, format=img_format, **save_kwargs)
                
                final_size = os.path.getsize(output_path)
                total_final_size += final_size
                diff = original_size - final_size
                saved_space += diff
                processed_count += 1
                
                log_callback(f"[OK] {filename} ({orig_w}x{orig_h}) -> {target_width}x{h_size} | "
                            f"{original_size/1024:.1f}KB -> {final_size/1024:.1f}KB")
                
                if progress_callback:
                    progress_callback((i + 1) / total_files)
                
        except Exception as e:
            log_callback(f"[HATA] {filename} işlenirken hata oluştu: {e}")

    total_saved_mb = saved_space / (1024 * 1024)
    total_initial_mb = total_initial_size / (1024 * 1024)
    total_final_mb = total_final_size / (1024 * 1024)

    log_callback("\n" + "="*30)
    log_callback(f"İşlem Tamamlandı.")
    log_callback(f"İşlenen Dosya: {processed_count}/{len(image_files)}")
    log_callback(f"Orijinal Toplam Boyut: {total_initial_mb:.2f} MB")
    log_callback(f"Yeni Toplam Boyut: {total_final_mb:.2f} MB")
    log_callback(f"Toplam Tasarruf: {total_saved_mb:.2f} MB")
    log_callback(f"Çıktı Klasörü: {output_dir}")
    log_callback("="*30)
    return True

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Image Resizer & Cleaner")
        self.geometry("750x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Header
        self.header_label = ctk.CTkLabel(self, text="Image Resizer & Cleaner", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Path Selection
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.path_frame.grid_columnconfigure(0, weight=1)

        self.path_entry = ctk.CTkEntry(self.path_frame, placeholder_text="Resim klasörünü seçin...")
        self.path_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")

        self.browse_button = ctk.CTkButton(self.path_frame, text="Gözat", command=self.browse_path, width=80)
        self.browse_button.grid(row=0, column=1, padx=(5, 10), pady=10)

        # Settings
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.settings_frame.grid_columnconfigure((0, 1), weight=1)

        # Width Setting Frame
        self.width_config_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        self.width_config_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.width_config_frame.grid_columnconfigure(0, weight=1)

        self.width_label = ctk.CTkLabel(self.width_config_frame, text="Hedef Genişlik (px):")
        self.width_label.grid(row=0, column=0, sticky="w")
        
        self.width_entry = ctk.CTkEntry(self.width_config_frame, width=80)
        self.width_entry.grid(row=0, column=1, sticky="e")
        self.width_entry.insert(0, "1024")
        self.width_entry.bind("<Return>", self.on_width_entry_change)
        self.width_entry.bind("<FocusOut>", self.on_width_entry_change)

        self.width_slider = ctk.CTkSlider(self.width_config_frame, from_=100, to=4000, number_of_steps=390, command=self.on_width_slider_change)
        self.width_slider.set(1024)
        self.width_slider.grid(row=1, column=0, columnspan=2, pady=(5, 0), sticky="ew")

        # Quality Setting Frame
        self.quality_config_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        self.quality_config_frame.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        self.quality_config_frame.grid_columnconfigure(0, weight=1)

        self.quality_label = ctk.CTkLabel(self.quality_config_frame, text="Kalite: 85%")
        self.quality_label.grid(row=0, column=0, sticky="w")
        
        self.quality_slider = ctk.CTkSlider(self.quality_config_frame, from_=1, to=100, number_of_steps=99, command=self.on_quality_slider_change)
        self.quality_slider.set(85)
        self.quality_slider.grid(row=1, column=0, pady=(5, 0), sticky="ew")

        # WebP Format Option
        self.webp_var = ctk.BooleanVar(value=False)
        self.webp_checkbox = ctk.CTkCheckBox(self.settings_frame, text="Görselleri WebP formatına dönüştür", variable=self.webp_var)
        self.webp_checkbox.grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 10), sticky="w")

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.progress_bar.set(0)

        # Log Area
        self.log_text = ctk.CTkTextbox(self, height=200)
        self.log_text.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        # Start Button
        self.start_button = ctk.CTkButton(self, text="İşlemi Başlat", command=self.start_processing, font=ctk.CTkFont(size=16, weight="bold"), height=40)
        self.start_button.grid(row=5, column=0, padx=20, pady=(10, 20), sticky="ew")

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)

    def on_width_slider_change(self, value):
        width_val = int(value)
        self.width_entry.delete(0, "end")
        self.width_entry.insert(0, str(width_val))

    def on_width_entry_change(self, event=None):
        try:
            value = int(self.width_entry.get())
            if 10 <= value <= 10000: # Daha geniş bir sınır tanıyalım
                self.width_slider.set(value)
            else:
                self.log("Uyarı: Genişlik 10 ile 10000 arasında olmalıdır.")
        except ValueError:
            self.log("Hata: Lütfen geçerli bir sayı girin.")

    def on_quality_slider_change(self, value):
        self.quality_label.configure(text=f"Kalite: {int(value)}%")

    def log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")

    def update_progress(self, value):
        self.progress_bar.set(value)

    def start_processing(self):
        path = self.path_entry.get()
        if not path:
            self.log("Hata: Lütfen önce bir klasör seçin.")
            return

        try:
            width = int(self.width_entry.get())
        except ValueError:
            self.log("Hata: Geçersiz genişlik değeri.")
            return

        self.start_button.configure(state="disabled")
        self.log_text.delete("1.0", "end")
        self.progress_bar.set(0)
        
        quality = int(self.quality_slider.get())
        to_webp = self.webp_var.get()

        thread = threading.Thread(target=self.run_process, args=(path, width, quality, to_webp))
        thread.start()

    def run_process(self, path, width, quality, to_webp):
        success = process_images(path, width, quality, to_webp=to_webp, log_callback=self.log, progress_callback=self.update_progress)
        self.start_button.configure(state="normal")

def main():
    parser = argparse.ArgumentParser(description="Resim boyutlandırma ve temizleme aracı")
    parser.add_argument("--path", help="İşlenecek resimlerin bulunduğu klasör yolu")
    parser.add_argument("--width", type=int, help="Hedef genişlik değeri (px)")
    parser.add_argument("--quality", type=int, default=85, help="JPG/WEBP Kalitesi (0-100, Varsayılan: 85)")
    parser.add_argument("--to-webp", action="store_true", help="Görselleri WebP formatına dönüştür")
    
    args = parser.parse_args()
    
    if args.path and args.width:
        process_images(args.path, args.width, args.quality, args.to_webp)
    else:
        # Launch GUI
        app = App()
        app.mainloop()

if __name__ == "__main__":
    main()
