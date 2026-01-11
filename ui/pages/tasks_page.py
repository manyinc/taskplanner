import customtkinter as ctk
from tkinter import ttk, messagebox
import ctypes
from core.config import PALETTE, RADIUS
from core.utils import to_pl_datetime_from_any, days_left_signed, parse_date_pl_or_iso, parse_pl_date
from CTkScrollableDropdown import CTkScrollableDropdown
from datetime import date, datetime # Importing standard things

# Fix imports if datetime conflicts
from datetime import datetime as dt_class, date as date_class 

class TasksPage(ctk.CTkFrame):
    def __init__(self, master, db_manager, navigation_callback):
        super().__init__(master, fg_color="transparent")
        self.db = db_manager
        self.navigation_callback = navigation_callback
        
        self.sort_key = None
        self.sort_reverse = False
        self.filter_status_var = ctk.StringVar(value="Status")
        self.filter_area_var = ctk.StringVar(value="Obszar")
        self.search_query = ""
        self.active_dropdowns = []
        
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # Filter Bar
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Area Filter
        area_vals = ["Obszar"] + self.db.get_distinct_areas()
        self.filter_area_cb = ctk.CTkOptionMenu(
            toolbar, variable=self.filter_area_var, values=area_vals,
            width=140, height=32,
            fg_color=PALETTE["btn_secondary"], button_color=PALETTE["btn_secondary"],
            button_hover_color=PALETTE["btn_secondary_hover"],
            text_color=PALETTE["text"], dropdown_fg_color=PALETTE["panel"],
            corner_radius=20,
            command=lambda v: self.refresh()
        )
        self.filter_area_cb.pack(side="left", padx=(0, 8))
        dd1 = CTkScrollableDropdown(
            attach=self.filter_area_cb, values=area_vals, 
            command=lambda v: (self.filter_area_var.set(v), self.refresh()), 
            frame_border_color="#575AC8", frame_corner_radius=RADIUS, 
            fg_color=PALETTE["panel_alt"], button_color=PALETTE["panel_alt"]
        )
        self.active_dropdowns.append(dd1)
        
        # Status Filter
        self.filter_status_cb = ctk.CTkOptionMenu(
            toolbar, variable=self.filter_status_var, values=["Status", "Do zrobienia", "W toku", "Zrobione"],
            width=130, height=32,
            fg_color=PALETTE["btn_secondary"], button_color=PALETTE["btn_secondary"],
            button_hover_color=PALETTE["btn_secondary_hover"],
            text_color=PALETTE["text"], dropdown_fg_color=PALETTE["panel"],
            corner_radius=20,
            command=lambda v: self.refresh()
        )
        self.filter_status_cb.pack(side="left", padx=(0, 8))
        dd2 = CTkScrollableDropdown(
            attach=self.filter_status_cb, values=["Status", "Do zrobienia", "W toku", "Zrobione"], 
            command=lambda v: (self.filter_status_var.set(v), self.refresh()), 
            frame_border_color="#575AC8", frame_corner_radius=RADIUS, 
            fg_color=PALETTE["panel_alt"], button_color=PALETTE["panel_alt"]
        )
        self.active_dropdowns.append(dd2)

        # Buttons
        ctk.CTkButton(toolbar, text="Usuń", command=self.delete_task, fg_color=PALETTE["danger"], hover_color=PALETTE["danger"], width=100, corner_radius=20).pack(side="right", padx=10)
        ctk.CTkButton(toolbar, text="Edytuj", command=self.edit_task, fg_color=PALETTE["btn_secondary"], hover_color=PALETTE["btn_secondary_hover"], width=100, corner_radius=20).pack(side="right")
        ctk.CTkButton(toolbar, text="Dodaj", command=self.add_task, fg_color=PALETTE["accent"], hover_color=PALETTE["accent_hover"], width=100, corner_radius=20).pack(side="right", padx=10)

        # Table Wrapper
        table_wrap = ctk.CTkFrame(self, fg_color=PALETTE["table_wrap"], corner_radius=RADIUS)
        table_wrap.grid(row=1, column=0, sticky="nsew")

        cols = ["area", "title", "due", "left", "status", "desc", "finished", "created"]
        
        self.tree = ttk.Treeview(
            table_wrap,
            columns=cols,
            show="headings",
            selectmode="browse",
            style="Dark.Treeview",
        )

        # Windows Scaling Fix
        try:
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            dpi = user32.GetDpiForSystem()
            table_wrap.tk.call("tk", "scaling", dpi / 80)
        except: pass

        # Scrollbar
        scroll_container = ctk.CTkFrame(table_wrap, fg_color=PALETTE["panel_alt"], corner_radius=10, width=10)
        scroll_container.pack(side="right", fill="y", padx=5, pady=10)
        
        vs = ctk.CTkScrollbar(scroll_container, command=self.tree.yview, button_color=PALETTE["scroll_handle"], fg_color="transparent", corner_radius=20)
        vs.pack(fill="y", expand=True, padx=2, pady=2)
        
        self.tree.configure(yscrollcommand=vs.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Headers
        headers = {
            "area": "Obszar", "title": "Tytuł", "due": "Termin",
            "left": "Do terminu", "status": "Status",
            "desc": "Opis", "finished": "Zakończono", "created": "Utworzono"
        }
        
        for col in cols:
            self.tree.column(col, width=100, anchor="center" if col not in ("title", "desc") else "w")
            self.tree.heading(col, text=headers.get(col, col), command=lambda c=col: self.sort_by(c))

        self.tree.tag_configure("even", background=PALETTE["row_even"])
        self.tree.tag_configure("odd", background=PALETTE["row_odd"])
        self.tree.tag_configure("status_done", foreground=PALETTE["success"])
        self.tree.tag_configure("status_doing", foreground=PALETTE["warning"])
        self.tree.tag_configure("overdue", foreground="#ff3333")
        self.tree.bind("<Double-1>", lambda e: self.edit_task())
        
        self.refresh()

    def update_search(self, query):
        self.search_query = query
        self.refresh()

    def refresh(self):
        if not self.tree.winfo_exists():
            return

        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Update area dropdown values
        area_vals = ["Obszar"] + sorted([a for a in self.db.get_distinct_areas() if a])
        self.filter_area_cb.configure(values=area_vals)
        # Update active dropdown if reference exists
        # In a real rigorous refactor, we would manage dropdowns better.

        status_label = self.filter_status_var.get()
        status = "all" if status_label in ["Status", "Wszystkie"] else status_label
        
        area_label = self.filter_area_var.get()
        area = None if area_label in ["Obszar", "Wszystkie"] else area_label
        
        rows = self.db.list_tasks(status=None if status == "all" else status, query=self.search_query, area=area)
        rows = self._sorted_rows(rows)

        for idx, (id_, title, desc, area, due, status, created, finished_at, left_fixed) in enumerate(rows):
            created_pl = to_pl_datetime_from_any(created)

            if status == "Zrobione" and left_fixed is not None:
                left_num = int(left_fixed)
            else:
                left_num = days_left_signed(due or "")
            left_str = "" if left_num is None else f"{left_num} dni"

            row_tags = ["even" if idx % 2 == 0 else "odd"]
            
            if status == "Zrobione":
                row_tags.append("status_done")
            elif status == "W toku":
                row_tags.append("status_doing")
            else:
                row_tags.append("status_todo")

            if left_num is not None and left_num < 0 and status != "Zrobione":
                row_tags.append("overdue")

            self.tree.insert(
                "", "end", iid=str(id_),
                values=(area or "", title, due or "", left_str, status, desc or "", finished_at or "", created_pl),
                tags=tuple(row_tags)
            )

    def _sorted_rows(self, rows):
        if not self.sort_key:
            return rows
        key = self.sort_key
        reverse = self.sort_reverse
        
        # Helper imports inside method to avoid clutter
        from core.config import PL_DATETIME_FMT

        def keyfunc(r):
            if key == "title": return (r[1] or "").lower()
            if key == "description": return (r[2] or "").lower()
            if key == "area": return (r[3] or "").lower()
            if key == "due_date":
                d = parse_date_pl_or_iso(r[4] or "")
                return d or date_class.max
            if key == "left":
                if (r[5] or "") == "Zrobione" and r[8] is not None:
                    return r[8]
                val = days_left_signed(r[4] or "")
                return 10**9 if val is None else val
            if key == "status": return (r[5] or "")
            if key == "finished_at":
                d = parse_date_pl_or_iso(r[7] or "")
                return d or date_class.min
            if key == "created_at":
                s = r[6] or ""
                try:
                    return dt_class.strptime(s, PL_DATETIME_FMT)
                except Exception:
                    return dt_class.max
            return r[0]
        return sorted(rows, key=keyfunc, reverse=reverse)

    def sort_by(self, key):
        if self.sort_key == key:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_key = key
            self.sort_reverse = False
        self.refresh()

    def add_task(self):
        self.navigation_callback("new_task")

    def edit_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Edycja", "Zaznacz zadanie.")
            return
        self.navigation_callback("edit_task", task_id=sel[0])

    def delete_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Usuń", "Zaznacz zadanie.")
            return
        if messagebox.askyesno("Potwierdź", "Usunąć zaznaczone zadanie?"):
            self.db.delete_task(int(sel[0]))
            self.refresh()
