import tkinter as tk
from tkinter import ttk

class Aplikacja:
    def __init__(self, root):
        self.root = root
        self.root.title("Stegonografia")
        self.root.geometry("1000x600")

        # Motywy
        self.motywy = {
            "jasny": {"bg": "white", "fg": "black", "frame": "#f0f0f0"},
            "ciemny": {"bg": "#2b2b2b", "fg": "white", "frame": "#3a3a3a"}
        }
        self.aktualny_motyw = "ciemny"

        # Menu motywu
        self.etap_1()
        self.menu()
    def etap_1(self):
        self._czysc_okno()

        self.frame = tk.Frame(self.root, bg=self.motywy[self.aktualny_motyw]["frame"])
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Początek", fg=self.motywy[self.aktualny_motyw]["fg"],
                 bg=self.motywy[self.aktualny_motyw]["frame"], font=("Arial", 16)).place(x=50, y=50)
        tk.Button(self.frame, text="Nowy projekt", command=self.etap_2).place(x=50, y=90)

    def etap_2(self):
        self._czysc_okno()
        self.menu()
        # Górna część
        self.frame_top = tk.Frame(self.root, bg=self.motywy[self.aktualny_motyw]["bg"])
        self.frame_top.pack(fill="both", expand=True)

        self.lewa_ramka = tk.Frame(self.frame_top, width=300, bg=self.motywy[self.aktualny_motyw]["bg"])
        self.srodek_ramka = tk.Frame(self.frame_top, width=100, bg=self.motywy[self.aktualny_motyw]["frame"])
        self.prawa_ramka = tk.Frame(self.frame_top, width=300, bg=self.motywy[self.aktualny_motyw]["bg"])

        self.lewa_ramka.pack(side="left", fill="both", expand=True)
        self.srodek_ramka.pack(side="left", fill="y")
        self.prawa_ramka.pack(side="left", fill="both", expand=True)

        self.obraz_wejsciowy_label = tk.Label(self.lewa_ramka, text="Obraz wejściowy", bg=self.motywy[self.aktualny_motyw]["frame"])
        self.obraz_wejsciowy_label.pack(pady=10)

        tk.Label(self.srodek_ramka, text="→", font=("Arial", 24),
                 bg=self.motywy[self.aktualny_motyw]["frame"],
                 fg=self.motywy[self.aktualny_motyw]["fg"]).pack(pady=20)

        tk.Label(self.srodek_ramka, text="Szyfrowanie:", bg=self.motywy[self.aktualny_motyw]["frame"],
                 fg=self.motywy[self.aktualny_motyw]["fg"]).pack(pady=10)
        self.algorytm = ttk.Combobox(self.srodek_ramka, values=["AES", "RSA", "Caesar"])
        self.algorytm.pack()

        self.obraz_wyjsciowy_label = tk.Label(self.prawa_ramka, text="Obraz zaszyfrowany", bg=self.motywy[self.aktualny_motyw]["frame"])
        self.obraz_wyjsciowy_label.pack(pady=10)

        # Dolna część
        self.frame_bottom = tk.Frame(self.root, bg=self.motywy[self.aktualny_motyw]["bg"])
        self.frame_bottom.pack(fill="x", padx=10, pady=5)

        self.label_tekst = tk.Label(self.frame_bottom, text="Tekst do zaszyfrowania:",
                                    bg=self.motywy[self.aktualny_motyw]["bg"],
                                    fg=self.motywy[self.aktualny_motyw]["fg"])
        self.label_tekst.pack(anchor="w")
        self.tekst = tk.Text(self.frame_bottom, height=4,
                             bg=self.motywy[self.aktualny_motyw]["bg"],
                             fg=self.motywy[self.aktualny_motyw]["fg"],
                             insertbackground=self.motywy[self.aktualny_motyw]["frame"])
        self.tekst.pack(fill="x")

    def ustaw_motyw(self, nazwa):
        self.aktualny_motyw = nazwa
        self.etap_2() if hasattr(self, 'frame_top') else self.etap_1()

    def _czysc_okno(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def menu(self):
        menubar = tk.Menu(self.root)
        motyw_menu = tk.Menu(menubar, tearoff=0)
        motyw_menu.add_command(label=" Jasny", command=lambda: self.ustaw_motyw("jasny"))
        motyw_menu.add_command(label=" Ciemny", command=lambda: self.ustaw_motyw("ciemny"))
        menubar.add_cascade(label="Motyw", menu=motyw_menu)
        self.root.config(menu=menubar) 
       
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplikacja(root)
    root.mainloop()
