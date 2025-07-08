import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image
import os

def rengi_seffaf_yap(resim_dosyasi, kaldirilacak_rgb, tolerans, cikti_dosyasi):
    try:
        img = Image.open(resim_dosyasi).convert('RGBA')
        pikseller = img.load()
        genislik, yukseklik = img.size

        for x in range(genislik):
            for y in range(yukseklik):
                r, g, b, a = pikseller[x, y]

                fark_kirmizi = abs(r - kaldirilacak_rgb[0])
                fark_yesil = abs(g - kaldirilacak_rgb[1])
                fark_mavi = abs(b - kaldirilacak_rgb[2])

                if fark_kirmizi <= tolerans and \
                   fark_yesil <= tolerans and \
                   fark_mavi <= tolerans:
                    pikseller[x, y] = (r, g, b, 0)

        img.save(cikti_dosyasi)
        return True
    except FileNotFoundError:
        messagebox.showerror("Hata", f"Dosya bulunamadı: {resim_dosyasi}")
        return False
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu {e}")
        return False

class RenkKaldiriciUygulamasi:
    def __init__(self, master):
        self.master = master
        master.title("Resimden Renk Kaldırıcı")
        master.geometry("600x500")
        master.resizable(False, False)

        self.secilen_resim_yolu = ""
        self.secilen_renk_rgb = (0, 0, 0)

        self.label_resim = tk.Label(master, text="Resim Seçiniz:")
        self.label_resim.pack(pady=5)

        self.entry_resim_yolu = tk.Entry(master, width=50)
        self.entry_resim_yolu.pack(pady=5)

        self.btn_resim_sec = tk.Button(master, text="Gözat...", command=self.resim_sec)
        self.btn_resim_sec.pack(pady=5)

        self.label_renk = tk.Label(master, text="Kaldırılacak Rengi Seçiniz")
        self.label_renk.pack(pady=5)

        self.btn_renk_sec = tk.Button(master, text="Renk Seç", command=self.renk_sec)
        self.btn_renk_sec.pack(pady=5)

        self.label_gosterilen_renk = tk.Label(master, text="Seçilen Renk: (Yok)", bg="lightgray", width=20, height=2, relief="solid")
        self.label_gosterilen_renk.pack(pady=5)

        self.label_tolerans = tk.Label(master, text="Tolerans (0-255):")
        self.label_tolerans.pack(pady=5)

        self.tolerans_slider = tk.Scale(master, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
        self.tolerans_slider.set(30)
        self.tolerans_slider.pack(pady=20)

        self.btn_islem_baslat = tk.Button(master, text="Rengi Kaldır ve Kaydet", command=self.islem_baslat)
        self.btn_islem_baslat.pack(pady=5)

    def resim_sec(self):
        dosya_yolu = filedialog.askopenfilename(
            title="Bir Resim Seçin",
            filetypes=[("PNG Resimleri", "*.png"), ("JPEG Resimleri", "*.jpg;*.jpeg"), ("Tüm Dosyalar","*.*")]
        )
        if dosya_yolu:
            self.secilen_resim_yolu = dosya_yolu
            self.entry_resim_yolu.delete(0, tk.END)
            self.entry_resim_yolu.insert(0, dosya_yolu)
            print(f"Resim seçildi: {self.secilen_resim_yolu}")

    def renk_sec(self):
        color_code = colorchooser.askcolor(title="Renk Seçiniz")
        if color_code[0] is not None:
            self.secilen_renk_rgb = tuple(int(c) for c in color_code[0])
            hex_color = color_code[1]
            self.label_gosterilen_renk.config(text=f"Seçilen Renk: {self.secilen_renk_rgb}", bg=hex_color)
            print(f"Renk seçildi: {self.secilen_renk_rgb} (Hex: {hex_color})")

    def islem_baslat(self):
        tolerans = self.tolerans_slider.get()

        if not self.secilen_resim_yolu:
            messagebox.showwarning("Uyarı", "Lütfen önce bir resim seçin!")
            return
        if self.secilen_renk_rgb == (0, 0, 0) and self.label_gosterilen_renk["text"] == "Seçilen Renk: (Yok)":
            messagebox.showwarning("Uyarı", "Lütfen kaldırılacak rengi seçin!")
            return

        input_filename_without_extension = os.path.splitext(os.path.basename(self.secilen_resim_yolu))[0]
        output_resim_yolu = filedialog.asksaveasfilename(
            title="İşlenmiş Resmi Kaydet",
            initialfile=f"{input_filename_without_extension}_temizlenmis.png",
            defaultextension=".png",
            filetypes=[("PNG Resimleri", "*.png"), ("Tüm Dosyalar", "*.*")]
        )

        if not output_resim_yolu:
            return

        if rengi_seffaf_yap(self.secilen_resim_yolu, self.secilen_renk_rgb, tolerans, output_resim_yolu):
            messagebox.showinfo("Başarılı", f"Resimdeki renk başarıyla kaldırıldı ve '{output_resim_yolu}' olarak kaydedildi!")

if __name__ == "__main__":
    root = tk.Tk()
    app = RenkKaldiriciUygulamasi(root)
    root.mainloop()
