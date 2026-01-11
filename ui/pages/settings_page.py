import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import json
from core.config import PALETTE, RADIUS, PRESET_AREAS, DB_PATH, save_db_config, save_areas_config, DB_CONFIG_FILE, AREAS_CONFIG_FILE

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master, fg_color="transparent")
        self.db = db_manager # Reference to update db connection if needed
        self.current_db_path = DB_PATH
        self._build_ui()

    def _build_ui(self):
        fr = ctk.CTkFrame(self, fg_color=PALETTE["panel"], corner_radius=RADIUS)
        fr.pack(fill="both", expand=True, padx=40, pady=40)
        
        ctk.CTkLabel(fr, text="Ustawienia", font=("Arial", 22, "bold")).pack(pady=(20, 10))
        
        # DB Path Selection
        db_frame = ctk.CTkFrame(fr, fg_color="transparent")
        db_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(db_frame, text="Wybór ścieżki z bazą danych:", text_color=PALETTE["muted"], font=("Arial", 14)).pack(anchor="w")
        
        row = ctk.CTkFrame(db_frame, fg_color="transparent")
        row.pack(fill="x", pady=(10, 0))
        
        entry_container = ctk.CTkFrame(row, fg_color=PALETTE["panel_alt"], corner_radius=20, height=40)
        entry_container.pack(side="left", fill="x", expand=True, padx=(0, 15))
        entry_container.pack_propagate(False)

        self.entry_db_path = ctk.CTkEntry(
            entry_container, border_width=0, fg_color=PALETTE["panel_alt"], 
            text_color=PALETTE["text"], font=("Arial", 13)
        )
        self.entry_db_path.pack(side="left", fill="both", expand=True, padx=15, pady=5)
        self.entry_db_path.insert(0, self.current_db_path)
        
        ctk.CTkButton(row, text="Przeglądaj", width=120, height=40, corner_radius=20, font=("Arial", 13, "bold"), fg_color=PALETTE["accent"], hover_color=PALETTE["accent_hover"], command=self.change_db_path).pack(side="right")

        # Add Area Section
        area_frame = ctk.CTkFrame(fr, fg_color="transparent")
        area_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(area_frame, text="Dodaj obszar zadania:", text_color=PALETTE["muted"], font=("Arial", 14)).pack(anchor="w")
        
        row_area = ctk.CTkFrame(area_frame, fg_color="transparent")
        row_area.pack(fill="x", pady=(10, 0))
        
        area_container = ctk.CTkFrame(row_area, fg_color=PALETTE["panel_alt"], corner_radius=20, height=40)
        area_container.pack(side="left", fill="x", expand=True, padx=(0, 15))
        area_container.pack_propagate(False)

        self.entry_new_area = ctk.CTkEntry(
            area_container, border_width=0, fg_color=PALETTE["panel_alt"], 
            text_color=PALETTE["text"], font=("Arial", 13)
        )
        self.entry_new_area.pack(side="left", fill="both", expand=True, padx=15, pady=5)
        
        ctk.CTkButton(row_area, text="Dodaj", width=120, height=40, corner_radius=20, font=("Arial", 13, "bold"), fg_color=PALETTE["accent"], hover_color=PALETTE["accent_hover"], command=self.add_custom_area).pack(side="right")

    def add_custom_area(self):
        new_area = self.entry_new_area.get().strip()
        if not new_area: return
            
        if new_area in PRESET_AREAS:
            messagebox.showinfo("Info", "Taki obszar już istnieje.")
            return
            
        PRESET_AREAS.append(new_area)
        
        # Save custom logic
        current_custom = []
        if os.path.exists(AREAS_CONFIG_FILE):
             try:
                 with open(AREAS_CONFIG_FILE, "r", encoding="utf-8") as f:
                     d = json.load(f)
                     current_custom = d.get("areas", [])
             except: pass
        
        if new_area not in current_custom:
            current_custom.append(new_area)
            try:
                with open(AREAS_CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump({"areas": current_custom}, f)
                messagebox.showinfo("Sukces", f"Dodano obszar: {new_area}")
                self.entry_new_area.delete(0, "end")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się zapisać obszaru: {e}")

    def change_db_path(self):
        initial_dir = os.environ.get("USERPROFILE")
        path = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Wybierz plik bazy danych",
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")]
        )
        if path:
            self.entry_db_path.delete(0, "end")
            self.entry_db_path.insert(0, path)
            
            save_db_config(path)
            
            # Reconnect DB
            try:
                self.db.db_path = path
                # Ideally we close old conn if any, but db_manager creates fresh conns for every op in this design
                # But we should verify connection
                self.db.get_connection().close()
                messagebox.showinfo("Sukces", "Baza danych została zmieniona.")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się połączyć z nową bazą: {e}")
