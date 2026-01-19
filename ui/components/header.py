import customtkinter as ctk
from core.config import PALETTE

#Współtworzone z ai

class Header(ctk.CTkFrame):
    def __init__(self, master, search_callback):
        super().__init__(master, fg_color="transparent", height=70)
        self.search_callback = search_callback
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        self.lbl_title = ctk.CTkLabel(self, text="Dashboard", font=("Arial", 24, "bold"), text_color=PALETTE["text"])
        self.lbl_title.pack(side="left", padx=10)

        search_frame = ctk.CTkFrame(self, fg_color=PALETTE["panel"], corner_radius=30, width=300)
        search_frame.pack(side="right")

        self.entry_search = ctk.CTkEntry(
            search_frame, width=220, border_width=0, fg_color=PALETTE["panel"],
            placeholder_text="Szukaj zadania...",
            placeholder_text_color=PALETTE["muted"],
            text_color=PALETTE["text"]
        )
        self.entry_search.pack(side="left", padx=15, pady=8, fill="x", expand=True)
        self.entry_search.bind("<KeyRelease>", self._on_search)

    def _on_search(self, event):
        query = self.entry_search.get()
        if self.search_callback:
            self.search_callback(query)

    def set_title(self, title):
        self.lbl_title.configure(text=title)
