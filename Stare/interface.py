import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import re

from stgsnek import Steganography
from stgfile import FileHandler
from date_code import DateCipher
from caesar_code import CaesarCipher

class SteganoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Suite")
        self.root.geometry("1200x800")
        
        self.current_image = None    # Przechowuje oryginalny obraz jako numpy array
        self.processed_image = None # Przechowuje przetworzony obraz
        self.decrypted_text = ""    # Przechowuje odszyfrowany tekst
        
        self._setup_themes()
        self._setup_ui()
        self._setup_menu()
        self._setup_bindings()

    def _setup_themes(self):
        self.themes = {
            "dark": {
                "bg": "#2D2D2D", "fg": "#FFFFFF",
                "frame": "#3A3A3A", "button": "#4A4A4A",
                "text_bg": "#404040", "text_fg": "#FFFFFF",
                "disabled_bg": "#303030"
            },
            "light": {
                "bg": "#FFFFFF", "fg": "#000000", 
                "frame": "#F0F0F0", "button": "#E0E0E0",
                "text_bg": "#FFFFFF", "text_fg": "#000000",
                "disabled_bg": "#E8E8E8"
            },
            "matrix": {
                "bg": "#0D0208", "fg": "#0D0208",
                "frame": "#008F11", "button": "#0D0208",
                "text_bg": "#008F11", "text_fg": "#0D0208",
                "disabled_bg": "#0D0208"
            }
        }
        self.current_theme = "dark"

    def _setup_menu(self):
        menubar = tk.Menu(self.root)
        
        # Menu plikowe
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Wczytaj obraz", command=self._load_image)
        file_menu.add_command(label="Zapisz obraz", command=self._save_image)
        file_menu.add_command(label="Zapisz tekst", command=self._save_text)
        file_menu.add_command(label="Wczytaj tekst", command=self._load_text)
        menubar.add_cascade(label="Plik", menu=file_menu)
        
        # Menu motywów
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Ciemny", command=lambda: self._change_theme("dark"))
        theme_menu.add_command(label="Jasny", command=lambda: self._change_theme("light"))
        theme_menu.add_command(label="Matrix", command=lambda: self._change_theme("matrix"))
        menubar.add_cascade(label="Motyw", menu=theme_menu)
        
        self.root.config(menu=menubar)

    def _setup_ui(self):
        # Główna ramka
        self.main_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel lewy - obraz wejściowy
        self.left_panel = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]["bg"])
        self.left_panel.pack(side="left", fill="both", expand=True)
        self._create_image_section(self.left_panel, "Obraz wejściowy")

        # Panel środkowy - sterowanie
        self.center_panel = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]["frame"], width=250)
        self.center_panel.pack(side="left", fill="y", padx=10)
        self._create_control_section()

        # Panel prawy - obraz wynikowy
        self.right_panel = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]["bg"])
        self.right_panel.pack(side="left", fill="both", expand=True)
        self._create_image_section(self.right_panel, "Obraz wynikowy")

        # Panel tekstowy
        self.text_panel = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        self.text_panel.pack(fill="x", padx=10, pady=10)
        self._create_text_section()

    def _create_image_section(self, parent, title):
        label = tk.Label(parent, text=title, bg=self.themes[self.current_theme]["frame"],
                       fg=self.themes[self.current_theme]["fg"])
        label.pack(fill="x", pady=5)
        
        canvas = tk.Canvas(parent, bg=self.themes[self.current_theme]["frame"], highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Poprawiona inicjalizacja atrybutów
        if title == "Obraz wejściowy":
            self.input_canvas = canvas
        else:
            self.output_canvas = canvas

    
    def _create_control_section(self):
        # Tryb pracy
        self.mode_slider = tk.Scale(self.center_panel, from_=0, to=1, orient="horizontal",
                                  showvalue=0, command=self._toggle_mode,
                                  bg=self.themes[self.current_theme]["frame"],
                                  troughcolor=self.themes[self.current_theme]["button"])
        self.mode_slider.pack(pady=15)
        
        self.mode_label = tk.Label(self.center_panel, text="TRYB: SZYFROWANIE",
                                 bg=self.themes[self.current_theme]["frame"],
                                 fg=self.themes[self.current_theme]["fg"])
        self.mode_label.pack()

        # Wybór algorytmu
        self.algorithm_combo = ttk.Combobox(self.center_panel, 
                                          values=["Caesar", "Date Cipher", "AES", "RSA"])
        self.algorithm_combo.current(0)
        self.algorithm_combo.pack(pady=10)

        # Przyciski akcji
        btn_frame = tk.Frame(self.center_panel, bg=self.themes[self.current_theme]["frame"])
        btn_frame.pack(pady=20)
        
        self.process_btn = tk.Button(btn_frame, text="START", command=self._process,
                                   bg=self.themes[self.current_theme]["button"],
                                   fg=self.themes[self.current_theme]["fg"])
        self.process_btn.pack(side="left", padx=5)
        
        self.save_btn = tk.Button(btn_frame, text="ZAPISZ", command=self._save_image,
                                bg=self.themes[self.current_theme]["button"],
                                fg=self.themes[self.current_theme]["fg"], state="disabled")
        self.save_btn.pack(side="left", padx=5)

        # Licznik pojemności
        self.capacity_label = tk.Label(self.center_panel, text="Dostępne bity: 0",
                                     bg=self.themes[self.current_theme]["frame"],
                                     fg=self.themes[self.current_theme]["fg"])
        self.capacity_label.pack(pady=10)

    def _create_text_section(self):
        self.text_label = tk.Label(self.text_panel, text="Tekst do zaszyfrowania:",
                                 bg=self.themes[self.current_theme]["bg"],
                                 fg=self.themes[self.current_theme]["fg"])
        self.text_label.pack(anchor="w")
        
        self.text_entry = tk.Text(self.text_panel, height=5,
                                bg=self.themes[self.current_theme]["text_bg"],
                                fg=self.themes[self.current_theme]["text_fg"],
                                insertbackground=self.themes[self.current_theme]["fg"])
        self.text_entry.pack(fill="x")
        self.text_entry.bind("<KeyRelease>", self._update_capacity)

    def _setup_bindings(self):
        self.root.bind("<Configure>", lambda e: self._resize_images())

    def _change_theme(self, theme_name):
        self.current_theme = theme_name
        self._update_ui_colors()

    def _update_ui_colors(self):
        theme = self.themes[self.current_theme]
        widgets = [self.main_frame, self.input_canvas, self.output_canvas,
                 self.center_panel, self.text_panel, self.text_entry]

        for widget in widgets:
            bg = theme["bg"] if widget not in [self.center_panel] else theme["frame"]
            widget.config(bg=bg)

        self.text_entry.config(bg=theme["text_bg"], fg=theme["text_fg"])
        self.process_btn.config(bg=theme["button"], fg=theme["fg"])
        self.save_btn.config(bg=theme["button"], fg=theme["fg"])
        self.capacity_label.config(bg=theme["frame"], fg=theme["fg"])

    def _resize_images(self):
        # Dodajemy sprawdzenie istnienia atrybutów
        if hasattr(self, 'input_canvas') and hasattr(self, 'output_canvas'):
            for canvas, image in [
                (self.input_canvas, self.current_image),
                (self.output_canvas, self.processed_image)
            ]:
                if image is not None:
                    self._display_image(Image.fromarray(image), canvas)


    def _display_image(self, img, canvas):
        try:
            if not isinstance(img, Image.Image):
                raise TypeError("Nieprawidłowy typ obrazu")
            
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            
            if canvas_width < 10 or canvas_height < 10:
                return

            ratio = min(canvas_width/img.width, canvas_height/img.height)
            new_size = (int(img.width*ratio), int(img.height*ratio))
            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized_img)
            
            canvas.image = photo
            canvas.delete("all")
            canvas.create_image(canvas_width//2, canvas_height//2, anchor="center", image=photo)
        except Exception as e:
            messagebox.showerror("Błąd wyświetlania", str(e))

    def _toggle_mode(self, value):
        mode = int(value)
        self.mode_label.config(text=f"TRYB: {'SZYFROWANIE' if mode == 0 else 'DESZYFROWANIE'}")
        
        if mode == 1:
            # Czyszczenie prawego panelu
            self._clear_output()
            self.text_entry.config(state="disabled", bg=self.themes[self.current_theme]["disabled_bg"])
            self.text_label.config(text="Odszyfrowany tekst:")
        else:
            self.text_entry.config(state="normal", bg=self.themes[self.current_theme]["text_bg"])
            self.text_label.config(text="Tekst do zaszyfrowania:")

    def _clear_output(self):
        self.processed_image = None
        self.output_canvas.delete("all")
        self.save_btn.config(state="disabled")  # Dezaktywuj przycisk zapisu
        self.decrypted_text = ""  # Wyczyszczenie przechowywanego tekstu

    def _decode_process(self):
        try:
            if not isinstance(self.current_image, np.ndarray):
                raise TypeError("Nieprawidłowy format obrazu")
            
            decoded_bits = Steganography.decode_utf8(self.current_image)
            detected_algo = self._detect_algorithm(decoded_bits)
            
            if detected_algo:
                self.algorithm_combo.set(detected_algo)
                messagebox.showinfo("Wykryto algorytm", f"Wykryto: {detected_algo}")
            
            self.decrypted_text = self._decrypt_text(decoded_bits)
            self._update_text_display(self.decrypted_text)
            
            # Dodatkowe czyszczenie po udanej deszyfracji
            self._clear_output()
            
        except Exception as e:
            messagebox.showerror("Błąd dekodowania", str(e))

    def _process(self):
        try:
            if self.current_image is None:
                raise ValueError("Najpierw wczytaj obraz!")
            
            if self.mode_slider.get() == 0:
                self._encode_process()
            else:
                self._decode_process()
        except Exception as e:
            messagebox.showerror("Błąd przetwarzania", str(e))

    def _encode_process(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        algorithm = self.algorithm_combo.get()
        
        encrypted_text = self._encrypt_text(text, algorithm)
        binary_data = Steganography.get_bin_str(encrypted_text)
        
        try:
            # Poprawka: Rozpakowanie krotki
            self.processed_image, _ = Steganography.encode(self.current_image, binary_data)
            self._display_image(Image.fromarray(self.processed_image), self.output_canvas)
            self.save_btn.config(state="normal")
        except ValueError as e:
            messagebox.showerror("Błąd kodowania", str(e))

    def _decode_process(self):
        try:
            # Poprawka: Sprawdzenie typu przed dekodowaniem
            if not isinstance(self.current_image, np.ndarray):
                raise TypeError("Nieprawidłowy format obrazu")
            
            decoded_bits = Steganography.decode_utf8(self.current_image)
           
           
            
            self.decrypted_text = self._decrypt_text(decoded_bits)
            self._update_text_display(self.decrypted_text)
        except Exception as e:
            messagebox.showerror("Błąd dekodowania", str(e))

    def _encrypt_text(self, text, algorithm):
        if algorithm == "Caesar":
            return CaesarCipher.encode(text, 3)
        elif algorithm == "Date Cipher":
            return DateCipher().encrypt(text)
        return text

    def _decrypt_text(self, text):
        algorithm = self.algorithm_combo.get()
        if algorithm == "Caesar":
            return CaesarCipher.decode(text, 3)
        elif algorithm == "Date Cipher":
            return DateCipher().decrypt(text)
        return text


    def _update_text_display(self, text):
        self.text_entry.config(state="normal")
        self.text_entry.delete("1.0", tk.END)
        self.text_entry.insert(tk.END, text)
        self.text_entry.config(state="disabled")

    def _update_capacity(self, event=None):
        if self.current_image is not None:
            try:
                max_chars, max_bits = Steganography.show_picture_capacity(self.current_image)
                current_text = self.text_entry.get("1.0", tk.END).strip()
                text_chars = len(current_text)
                
                self.capacity_label.config(
                    text=f"Dostępne bity: {max_bits}\n"
                         f"Wykorzystane:\n {text_chars * 8} ({text_chars} znaków)\n"
                         f"Pozostało: {max_bits - (text_chars * 8)}"
                )
            except AttributeError:
                self.capacity_label.config(text="Dostępne bity: 0")

    def _load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.current_image = FileHandler.load_image(file_path)
                self._display_image(Image.fromarray(self.current_image), self.input_canvas)
                self._update_capacity()
            except Exception as e:
                messagebox.showerror("Błąd wczytywania", str(e))

    def _save_image(self):
        if self.processed_image is not None:
            try:
                if not isinstance(self.processed_image, np.ndarray):
                    raise TypeError("Nieprawidłowy format obrazu wynikowego")
                
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=list(FileHandler.get_supported_image_formats().items())
                )
                if file_path:
                    FileHandler.save_image(self.processed_image, file_path)
                    messagebox.showinfo("Sukces", "Obraz zapisany pomyślnie!")
            except Exception as e:
                messagebox.showerror("Błąd zapisu", str(e))

    def _load_text(self):
        file_path = filedialog.askopenfilename(
            filetypes=list(FileHandler.get_supported_text_formats().items())
        )
        if file_path:
            try:
                content = FileHandler.load_text(file_path)
                self.text_entry.delete("1.0", tk.END)
                self.text_entry.insert(tk.END, content)
                self._update_capacity()
            except Exception as e:
                messagebox.showerror("Błąd wczytywania", str(e))

    def _save_text(self):
        if self.decrypted_text:
            try:
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=list(FileHandler.get_supported_text_formats().items())
                )
                if file_path:
                    FileHandler.save_text(self.decrypted_text, file_path)
                    messagebox.showinfo("Sukces", "Tekst zapisany pomyślnie!")
            except Exception as e:
                messagebox.showerror("Błąd zapisu", str(e))
        else:
            messagebox.showwarning("Ostrzeżenie", "Brak tekstu do zapisania!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganoApp(root)
    root.mainloop()
