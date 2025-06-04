
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image
import numpy as np
from date_code import DateCipher
from datetime import datetime  # Dodaj tę linię
from caesar_code import CaesarCipher
from stgfile import FileHandler
from Themes import THEMES
from utils import display_image, detect_algorithm
from stgsnek import Steganography

class SteganoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Suite")
        self.root.geometry("1200x800")
        
        self.current_image = None
        self.processed_image = None
        self.decrypted_text = ""
        self.caesar_shift  = tk.IntVar(value=3)  # Domyślne przesunięcie
        self.date_key = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))  
        self.themes = THEMES
        self.current_theme = "dark"
        
        self._setup_ui()
        self._toggle_algorithm_controls()  # Ustaw widoczność kontrolek
        self._setup_menu()
        self._setup_bindings()
        self._toggle_algorithm_controls()  # Ustawienie widoczności ramki przesunięcia

    def _set_current_date(self):
        now = datetime.now().strftime("%Y-%m-%d")  # Użyj datetime z importu
        self.date_key.set(now)
    def _setup_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Wczytaj obraz", command=self._load_image)
        file_menu.add_command(label="Zapisz obraz", command=self._save_image)
        file_menu.add_command(label="Wczytaj tekst", command=self._load_text)
        file_menu.add_command(label="Zapisz tekst", command=self._save_text)
        menubar.add_cascade(label="Plik", menu=file_menu)
        
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Ciemny", command=lambda: self._change_theme("dark"))
        theme_menu.add_command(label="Jasny", command=lambda: self._change_theme("light"))
        theme_menu.add_command(label="Matrix", command=lambda: self._change_theme("matrix"))
        menubar.add_cascade(label="Motyw", menu=theme_menu)
        
        self.root.config(menu=menubar)

    def _setup_ui(self):
        self.root.config(bg=self.themes[self.current_theme]["bg"])
        
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
        
        if title == "Obraz wejściowy":
            self.input_canvas = canvas
        else:
            self.output_canvas = canvas

    def _create_control_section(self):
        # Ramka przesunięcia Cezara (widoczna na początku)
        self.shift_frame = tk.Frame(self.center_panel, bg=self.themes[self.current_theme]["frame"])
        self.shift_frame.pack(pady=5)
                # Ramka daty dla Date Cipher
        self.date_frame = tk.Frame(self.center_panel, bg=self.themes[self.current_theme]["frame"])
        
        tk.Label(self.date_frame, text="Data :", 
               bg=self.themes[self.current_theme]["frame"],
               fg=self.themes[self.current_theme]["fg"]).pack(side="left", padx=5)
        
        self.date_entry = ttk.Entry(self.date_frame, textvariable=self.date_key, width=10)
        self.date_entry.pack(side="left", padx=5)
        
        # Przycisk do ustawienia aktualnej daty
        current_date_btn = tk.Button(self.date_frame, text="Teraz", command=self._set_current_date,
                                   bg=self.themes[self.current_theme]["button"],
                                   fg=self.themes[self.current_theme]["fg"])
        current_date_btn.pack(side="left", padx=5)

        tk.Label(self.shift_frame, text="Przesunięcie:", 
               bg=self.themes[self.current_theme]["frame"],
               fg=self.themes[self.current_theme]["fg"]).pack(side="left")
        
        self.shift_entry = ttk.Entry(self.shift_frame, textvariable=self.caesar_shift, width=5)
        self.shift_entry.pack(side="left", padx=5)

        # Tryb pracy
        self.mode_slider = tk.Scale(self.center_panel, from_=0, to=1, orient="horizontal",
                                  showvalue=0, command=self._toggle_mode,
                                  bg=self.themes[self.current_theme]["frame"],
                                  troughcolor=self.themes[self.current_theme]["button"])
        self.mode_slider.pack(pady=10)
        
        self.mode_label = tk.Label(self.center_panel, text="TRYB: SZYFROWANIE",
                                 bg=self.themes[self.current_theme]["frame"],
                                 fg=self.themes[self.current_theme]["fg"])
        self.mode_label.pack()

        # Wybór algorytmu
        algorithm_frame = tk.Frame(self.center_panel, bg=self.themes[self.current_theme]["frame"])
        algorithm_frame.pack(fill="x", pady=10)
        
        tk.Label(algorithm_frame, text="Algorytm:", 
               bg=self.themes[self.current_theme]["frame"],
               fg=self.themes[self.current_theme]["fg"]).pack(side="left")
        
        self.algorithm_combo = ttk.Combobox(algorithm_frame, 
                                          values=["Wybierz szyfr","Date Cipher","Caesar"],
                                          width=12)
        self.algorithm_combo.current(0)
        self.algorithm_combo.pack(side="left", padx=5)
        self.algorithm_combo.bind("<<ComboboxSelected>>", self._toggle_algorithm_controls)
        
        # Przyciski akcji
        btn_frame = tk.Frame(self.center_panel, bg=self.themes[self.current_theme]["frame"])
        btn_frame.pack(pady=10)
        
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

    def _toggle_algorithm_controls(self, event=None):
        """Pokazuje/ukrywa kontrolki w zależności od wybranego algorytmu"""
        algorithm = self.algorithm_combo.get()
        
        # Ukryj wszystkie ramki
        self.shift_frame.pack_forget()
        self.date_frame.pack_forget()
        
        # Pokaż odpowiednią ramkę
        if algorithm == "Caesar":
            self.shift_frame.pack(pady=5)
        elif algorithm == "Date Cipher":
            self.date_frame.pack(pady=5)

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
        self.root.config(bg=theme["bg"])
        
        widgets = [self.main_frame, self.input_canvas, self.output_canvas,
                 self.center_panel, self.text_panel, self.text_entry]

        for widget in widgets:
            bg = theme["bg"] if widget not in [self.center_panel] else theme["frame"]
            widget.config(bg=bg)

        self.text_entry.config(bg=theme["text_bg"], fg=theme["text_fg"])
        self.process_btn.config(bg=theme["button"], fg=theme["fg"])
        self.save_btn.config(bg=theme["button"], fg=theme["fg"])
        self.capacity_label.config(bg=theme["frame"], fg=theme["fg"])
        
        # Aktualizacja kolorów dla ramki przesunięcia
        if hasattr(self, 'shift_frame'):
            self.shift_frame.config(bg=theme["frame"])
            for widget in self.shift_frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg=theme["frame"], fg=theme["fg"])

    def _resize_images(self):
        if hasattr(self, 'input_canvas') and hasattr(self, 'output_canvas'):
            for canvas, image in [(self.input_canvas, self.current_image),
                                (self.output_canvas, self.processed_image)]:
                if image is not None:
                    display_image(Image.fromarray(image), canvas)

    def _toggle_mode(self, value):
        mode = int(value)
        self.mode_label.config(text=f"TRYB: {'SZYFROWANIE' if mode == 0 else 'DESZYFROWANIE'}")
        
        if mode == 1:
            self._clear_output()
            self.text_entry.config(state="disabled", bg=self.themes[self.current_theme]["disabled_bg"])
            self.text_label.config(text="Odszyfrowany tekst:")
        else:
            self.text_entry.config(state="normal", bg=self.themes[self.current_theme]["text_bg"])
            self.text_label.config(text="Tekst do zaszyfrowania:")

    def _clear_output(self):
        self.processed_image = None
        if hasattr(self, 'output_canvas'):
            self.output_canvas.delete("all")
        self.save_btn.config(state="disabled")
        self.decrypted_text = ""

    def _process(self):
        try:
            if self.current_image is None:
                raise ValueError("Najpierw wczytaj obraz!")
            
            if self.mode_slider.get() == 0:
                self._encode_process()
            else:
                self._decode_process()
        except Exception as e:
            tk.messagebox.showerror("Błąd przetwarzania", str(e))

    def _encode_process(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        # DODAJ TĘ LINIĘ: Pobierz aktualnie wybrany algorytm
        algorithm = self.algorithm_combo.get()
        
        try:
            encrypted_text = encrypt_text(text, algorithm, self.caesar_shift.get(), self.date_key.get())
        except Exception as e:
            tk.messagebox.showerror("Błąd szyfrowania", f"Użyto bieżącej daty: {str(e)}")
            encrypted_text = encrypt_text(text, algorithm, self.caesar_shift.get(), None)
        
        binary_data = Steganography.get_bin_str(encrypted_text)
        
        try:
            self.processed_image, _ = Steganography.encode(self.current_image, binary_data)
            display_image(Image.fromarray(self.processed_image), self.output_canvas)
            self.save_btn.config(state="normal")
        except ValueError as e:
            tk.messagebox.showerror("Błąd kodowania", str(e))



    def _decode_process(self):
        try:
            if not isinstance(self.current_image, np.ndarray):
                raise TypeError("Nieprawidłowy format obrazu")
            
            decoded_bits = Steganography.decode_utf8(self.current_image)
            
         
            algorithm = self.algorithm_combo.get()
            
            try:
                self.decrypted_text = decrypt_text(decoded_bits, algorithm, self.caesar_shift.get(), self.date_key.get())
            except Exception as e:
                tk.messagebox.showerror("Błąd deszyfrowania", f"Użyto bieżącej daty: {str(e)}")
                self.decrypted_text = decrypt_text(decoded_bits, algorithm, self.caesar_shift.get(), None)
            
            self._update_text_display(self.decrypted_text)
        except Exception as e:
            tk.messagebox.showerror("Błąd dekodowania", str(e))

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
                         f"Użyto: {text_chars * 8} ({text_chars} znaków)\n"
                         f"Pozostało: {max_bits - (text_chars * 8)}"
                )
            except AttributeError:
                self.capacity_label.config(text="Dostępne bity: 0")

    def _load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.current_image = FileHandler.load_image(file_path)
                display_image(Image.fromarray(self.current_image), self.input_canvas)
                self._update_capacity()
            except Exception as e:
                tk.messagebox.showerror("Błąd wczytywania", str(e))

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
                    tk.messagebox.showinfo("Sukces", "Obraz zapisany pomyślnie!")
            except Exception as e:
                tk.messagebox.showerror("Błąd zapisu", str(e))

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
                tk.messagebox.showerror("Błąd wczytywania", str(e))

    def _save_text(self):
        if self.decrypted_text:
            try:
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=list(FileHandler.get_supported_text_formats().items())
                )
                if file_path:
                    FileHandler.save_text(self.decrypted_text, file_path)
                    tk.messagebox.showinfo("Sukces", "Tekst zapisany pomyślnie!")
            except Exception as e:
                tk.messagebox.showerror("Błąd zapisu", str(e))
        else:
            tk.messagebox.showwarning("Ostrzeżenie", "Brak tekstu do zapisania!")



def encrypt_text(text, algorithm, shift=3, date_str=None):
    if algorithm == "Caesar":
        return CaesarCipher.encode(text, shift)
    elif algorithm == "Date Cipher":
        try:
            return DateCipher(date_str).encrypt(text)
        except ValueError as e:
            return DateCipher().encrypt(text)
    return text

def decrypt_text(text, algorithm, shift=3, date_str=None):
    if algorithm == "Caesar":
        return CaesarCipher.decode(text, shift)
    elif algorithm == "Date Cipher":
        try:
            return DateCipher(date_str).decrypt(text)
        except ValueError as e:
            return DateCipher().decrypt(text)
    return text        



if __name__ == "__main__":
    root = tk.Tk()
    app = SteganoApp(root)
    root.mainloop()
