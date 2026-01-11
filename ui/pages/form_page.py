import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date
from core.config import PALETTE, RADIUS, PRESET_AREAS, PL_DATE_FMT
from core.utils import parse_pl_date, now_pl_date, days_left_signed, to_pl_date_from_any
from CTkScrollableDropdown import CTkScrollableDropdown

class TaskFormPage(ctk.CTkFrame):
    def __init__(self, master, db_manager, navigation_callback, task_id=None):
        super().__init__(master, fg_color=PALETTE["panel"], corner_radius=RADIUS)
        self.db = db_manager
        self.navigation_callback = navigation_callback
        self.task_id = task_id
        self.edit_mode = task_id is not None
        self.task_data = None
        
        self.active_dropdowns = []
        
        if self.edit_mode:
            self.task_data = self.db.get_task_by_id(task_id)
            if not self.task_data:
                messagebox.showerror("Błąd", "Nie znaleziono zadania.")
                self.navigation_callback("tasks")
                return

        self._build_ui()

    def _build_ui(self):
        # Title
        title_text = "Edycja Zadania" if self.edit_mode else "Dodaj Nowe Zadanie"
        ctk.CTkLabel(self, text=title_text, font=("Arial", 22, "bold"), text_color=PALETTE["text"]).pack(pady=20)
        
        # Form Container
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(pady=10)
        
        pad = {"padx": 12, "pady": 8}
        label_kwargs = {"text_color": PALETTE["muted"]}
        
        # 1. Title
        ctk.CTkLabel(form, text="Tytuł *", **label_kwargs).grid(row=0, column=0, sticky="w", **pad)
        title_cont = ctk.CTkFrame(form, width=420, height=40, corner_radius=20, fg_color=PALETTE["panel_alt"])
        title_cont.grid(row=0, column=1, **pad)
        title_cont.pack_propagate(False)
        self.nt_title = ctk.CTkEntry(title_cont, border_width=0, fg_color=PALETTE["panel_alt"], text_color=PALETTE["text"], font=("Arial", 13))
        self.nt_title.pack(fill="both", expand=True, padx=15, pady=5)
        
        # 2. Description
        ctk.CTkLabel(form, text="Opis", **label_kwargs).grid(row=1, column=0, sticky="w", **pad)
        self.nt_desc = ctk.CTkTextbox(form, width=420, height=120, corner_radius=20, fg_color=PALETTE["panel_alt"], border_color=PALETTE["header"], text_color=PALETTE["text"])
        self.nt_desc.grid(row=1, column=1, **pad)
        
        # 3. Area
        ctk.CTkLabel(form, text="Obszar (wpisz lub wybierz)", **label_kwargs).grid(row=2, column=0, sticky="w", **pad)
        self.nt_area = ctk.CTkComboBox(
            form, values=PRESET_AREAS, width=220, height=32, corner_radius=16,
            fg_color=PALETTE["panel_alt"], button_color=PALETTE["header"], button_hover_color=PALETTE["accent_hover"],
            text_color=PALETTE["text"], dropdown_fg_color=PALETTE["panel_alt"],
            dropdown_hover_color=PALETTE["header"], dropdown_text_color=PALETTE["text"],
            border_color=PALETTE["header"]
        )
        self.nt_area.grid(row=2, column=1, sticky="w", **pad)
        
        # 4. Due Date
        ctk.CTkLabel(form, text="Termin (DD.MM.RRRR)", **label_kwargs).grid(row=3, column=0, sticky="w", **pad)
        due_frame = ctk.CTkFrame(form, fg_color="transparent")
        due_frame.grid(row=3, column=1, sticky="w", **pad)
        
        due_cont = ctk.CTkFrame(due_frame, width=180, height=40, corner_radius=20, fg_color=PALETTE["panel_alt"])
        due_cont.pack(side="left")
        due_cont.pack_propagate(False)
        self.nt_due = ctk.CTkEntry(due_cont, border_width=0, fg_color=PALETTE["panel_alt"], text_color=PALETTE["text"], font=("Arial", 13))
        self.nt_due.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.nt_btn_cal = ctk.CTkButton(due_frame, text="📅", width=40, height=40, corner_radius=20, fg_color=PALETTE["header"], hover_color=PALETTE["accent_hover"], command=self._open_cal)
        self.nt_btn_cal.pack(side="left", padx=(8,0))
        
        # 5. Status
        ctk.CTkLabel(form, text="Status", **label_kwargs).grid(row=4, column=0, sticky="w", **pad)
        self.nt_status_var = ctk.StringVar(value="Do zrobienia")
        self.nt_status = ctk.CTkOptionMenu(
            form, values=["Do zrobienia", "W toku", "Zrobione"], variable=self.nt_status_var,
            width=220, height=32, corner_radius=16,
            fg_color=PALETTE["panel_alt"], button_color=PALETTE["header"], button_hover_color=PALETTE["accent_hover"],
            text_color=PALETTE["text"], dropdown_fg_color=PALETTE["panel_alt"],
            dropdown_hover_color=PALETTE["header"], dropdown_text_color=PALETTE["text"]
        )
        self.nt_status.grid(row=4, column=1, sticky="w", **pad)

        # Pre-fill
        if self.edit_mode and self.task_data:
            self.nt_title.insert(0, self.task_data["title"])
            self.nt_desc.insert("1.0", self.task_data["description"] or "")
            if self.task_data["area"]: self.nt_area.set(self.task_data["area"])
            if self.task_data["due_date"]: self.nt_due.insert(0, self.task_data["due_date"])
            self.nt_status_var.set(self.task_data["status"])

        # Buttons
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(pady=30)
        
        btn_text = "Zapisz Zmiany" if self.edit_mode else "Zapisz Zadanie"
        ctk.CTkButton(btns, text=btn_text, width=160, height=40, corner_radius=20, font=("Arial", 13, "bold"), fg_color=PALETTE["accent"], hover_color=PALETTE["accent_hover"], command=self._save_task).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="Anuluj", width=160, height=40, corner_radius=20, font=("Arial", 13, "bold"), fg_color=PALETTE["header"], hover_color=PALETTE["accent_hover"], command=lambda: self.navigation_callback("tasks" if self.edit_mode else "home")).pack(side="left", padx=10)

        # Attach dropdowns
        self._attach_scrollable_dropdowns()

    def _open_cal(self):
        try:
            from tkcalendar import Calendar
        except Exception:
            messagebox.showinfo("Kalendarz", "Zainstaluj 'tkcalendar'.")
            return

        top = ctk.CTkToplevel(self)
        top.title("Wybierz datę")
        top.resizable(False, False)
        top.configure(fg_color=PALETTE["panel"])
        top.grab_set()
        
        cal = Calendar(
            top, selectmode="day", date_pattern="dd.mm.yyyy",
            background=PALETTE["panel"], disabledbackground=PALETTE["panel"],
            bordercolor=PALETTE["header"], headersbackground=PALETTE["header"],
            normalbackground=PALETTE["panel_alt"], weekendbackground=PALETTE["panel_alt"],
            othermonthbackground=PALETTE["panel"], othermonthwebackground=PALETTE["panel"],
            selectbackground=PALETTE["accent"], normalforeground=PALETTE["text"],
            weekendforeground=PALETTE["text"], headersforeground=PALETTE["muted"],
            othermonthforeground=PALETTE["muted"], othermonthweforeground=PALETTE["muted"],
            selectforeground=PALETTE["text"], foreground=PALETTE["text"]
        )
        cal.pack(padx=12, pady=12)
        
        def set_date():
            d = cal.selection_get()
            self.nt_due.delete(0, "end")
            self.nt_due.insert(0, d.strftime(PL_DATE_FMT))
            top.destroy()
            
        btns = ctk.CTkFrame(top, fg_color="transparent")
        btns.pack(pady=(0,12))
        ctk.CTkButton(btns, text="OK", width=120, fg_color=PALETTE["accent"], hover_color=PALETTE["accent_hover"], command=set_date).pack(side="left", padx=8)
        ctk.CTkButton(btns, text="Anuluj", width=120, fg_color=PALETTE["header"], hover_color=PALETTE["accent_hover"], command=top.destroy).pack(side="left", padx=8)

    def _attach_scrollable_dropdowns(self):
         common = {
            "frame_corner_radius": RADIUS,
            "fg_color": PALETTE["panel_alt"],
            "button_color": PALETTE["panel_alt"],
            "hover_color": PALETTE["header"],
            "text_color": PALETTE["text"],
            "frame_border_color": PALETTE["header"]
         }
         # Verify widgets exist before attaching
         if hasattr(self, 'nt_area') and self.nt_area.winfo_exists():
            d1 = CTkScrollableDropdown(attach=self.nt_area, values=PRESET_AREAS, autocomplete=False, **common)
            self.active_dropdowns.append(d1)
         if hasattr(self, 'nt_status') and self.nt_status.winfo_exists():
            d2 = CTkScrollableDropdown(attach=self.nt_status, values=["Do zrobienia", "W toku", "Zrobione"], **common)
            self.active_dropdowns.append(d2)

    def _save_task(self):
        title = self.nt_title.get().strip()
        desc = self.nt_desc.get("1.0", "end").strip()
        area = self.nt_area.get().strip()
        due = self.nt_due.get().strip()
        status = self.nt_status_var.get()
        
        if not title:
            messagebox.showwarning("Walidacja", "Tytuł jest wymagany.")
            return

        due_pl = None
        if due:
            try: 
                 d_obj = parse_pl_date(due)
                 due_pl = due
            except ValueError:
                messagebox.showwarning("Walidacja", "Termin musi być w formacie DD.MM.RRRR.")
                return
        
        if self.edit_mode:
            prev_status = self.task_data["status"]
            new_status = status
            finished_at = self.task_data["finished_at"]
            left_fixed = self.task_data["left_fixed"]
            
            if prev_status != "Zrobione" and new_status == "Zrobione":
                finished_at = now_pl_date()
                left_fixed = days_left_signed(to_pl_date_from_any(due_pl)) if due_pl else None
            elif prev_status == "Zrobione" and new_status != "Zrobione":
                finished_at = None
                left_fixed = None
            else:
                if new_status != "Zrobione":
                    left_fixed = None
                    
            self.db.update_task(self.task_id, title, desc, area or None, due_pl, new_status, finished_at, left_fixed)
        else:
            self.db.add_task(title, desc, area or None, due or None, status)
            
        self.navigation_callback("tasks")
