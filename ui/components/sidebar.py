import customtkinter as ctk
import os
from PIL import Image
from core.config import PALETTE, ASSETS_DIR

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, navigation_callback):
        super().__init__(master, fg_color=PALETTE["panel"], width=240, corner_radius=0)
        self.navigation_callback = navigation_callback
        self.nav_buttons = {}
        self.grid_propagate(False)
        self._build_ui()

    def _build_ui(self):
        top_box = ctk.CTkFrame(self, fg_color="transparent")
        top_box.pack(pady=30, padx=20, fill="x")
        
        logo_path = os.path.join(ASSETS_DIR, "logo.png")
        if os.path.exists(logo_path):
             try:
                 pil = Image.open(logo_path)
                 self.nav_logo_img = ctk.CTkImage(light_image=pil, dark_image=pil, size=(40, 40))
                 lbl_icon = ctk.CTkLabel(top_box, text="", image=self.nav_logo_img)
                 lbl_icon.pack(side="left", padx=(0, 10))
             except: pass

        ctk.CTkLabel(top_box, text="TaskPlanner", font=("Arial", 22, "bold"), text_color=PALETTE["text"]).pack(side="left")
        
        ctk.CTkFrame(self, height=20, fg_color="transparent").pack()

        self._add_nav_btn("Strona Główna", "🏠", "home")
        self._add_nav_btn("Nowe Zadanie", "➕", "new_task")
        self._add_nav_btn("Zadania", "📋", "tasks")
        self._add_nav_btn("Import", "📥", "import")
        self._add_nav_btn("Export", "📤", "export")
        self._add_nav_btn("Ustawienia", "⚙️", "settings")

    def _add_nav_btn(self, text, icon, page_name):
        btn = ctk.CTkButton(
            self, text=f"  {icon}  {text}",
            fg_color="transparent", hover_color=PALETTE["btn_secondary_hover"],
            anchor="w", font=("Arial", 14), height=45, corner_radius=8,
            text_color=PALETTE["muted"],
            command=lambda: self.navigation_callback(page_name)
        )
        btn.pack(pady=5, padx=15, fill="x")
        self.nav_buttons[page_name] = btn

    def update_active_button(self, page_name):
        for name, btn in self.nav_buttons.items():
            if name == page_name:
                btn.configure(fg_color=PALETTE["accent"], text_color="#FFF")
            else:
                btn.configure(fg_color="transparent", text_color=PALETTE["muted"])