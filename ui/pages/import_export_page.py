import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import csv
from PIL import Image
from core.config import PALETTE, ASSETS_DIR
from core.utils import to_pl_date_from_any, now_pl_datetime, days_left_signed, to_pl_datetime_from_any

class ImportExportPage(ctk.CTkFrame):
    def __init__(self, master, db_manager, mode="import"):
        super().__init__(master, fg_color="transparent")
        self.db = db_manager
        self.mode = mode
        self._build_ui()

    def _build_ui(self):
        fr = ctk.CTkFrame(self, fg_color="transparent")
        fr.place(relx=0.5, rely=0.5, anchor="center")
        
        asset_name = "import.png" if self.mode == "import" else "export.png"
        action_name = "zaimportować" if self.mode == "import" else "wyeksportować"
        cmd = self.import_csv if self.mode == "import" else self.export_csv
        
        if os.path.exists(os.path.join(ASSETS_DIR, asset_name)):
             try:
                 pil = Image.open(os.path.join(ASSETS_DIR, asset_name))
                 img = ctk.CTkImage(light_image=pil, dark_image=pil, size=(200, 200))
                 btn = ctk.CTkButton(fr, text="", image=img, command=cmd, fg_color="transparent", hover_color=PALETTE["panel"])
                 btn.pack()
                 ctk.CTkLabel(fr, text=f"Kliknij aby {action_name} CSV", font=("Arial", 16)).pack(pady=10)
             except:
                 ctk.CTkButton(fr, text=f"{self.mode.upper()} CSV", width=200, height=100, command=cmd).pack()
        else:
             ctk.CTkButton(fr, text=f"{self.mode.upper()} CSV", width=200, height=100, command=cmd).pack()

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")], title="Wybierz plik CSV")
        if not path: return

        def norm(s: str) -> str:
            return (s or "").strip().lower()

        added = 0
        skipped = 0

        try:
            with open(path, "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f, delimiter=";")
                headers = next(reader, [])
                idx = {norm(h): i for i, h in enumerate(headers)}

                def get(row, *names):
                    for n in names:
                        i = idx.get(norm(n))
                        if i is not None and i < len(row):
                            return row[i].strip()
                    return ""

                for row in reader:
                    title = get(row, "tytuł", "tytul", "title")
                    if not title:
                        skipped += 1
                        continue

                    area = get(row, "obszar", "area") or None
                    description = get(row, "opis", "description") or None
                    due_raw = get(row, "termin (dd.mm.rrrr)", "termin", "due", "due date")
                    due_pl = to_pl_date_from_any(due_raw) if due_raw else None
                    status = get(row, "status") or "Do zrobienia"

                    finished_at = get(row, "zakończono (dd.mm.rrrr)", "zakończono", "finished", "finished at") or None
                    created_at = get(row, "utworzone (dd.mm.rrrr | hh:mm:ss)", "utworzone", "created", "created at") or now_pl_datetime()

                    left_txt = get(row, "do terminu (dni)", "do terminu", "left", "days left")
                    left_fixed = None
                    if left_txt:
                        try:
                            left_fixed = int(left_txt)
                        except:
                            left_fixed = None

                    if status == "Zrobione" and left_fixed is None:
                        left_fixed = days_left_signed(due_pl) if due_pl else None
                    if status != "Zrobione":
                        left_fixed = None
                        finished_at = None

                    self.db.add_task_raw(title, description, area, due_pl, status, created_at, finished_at, left_fixed)
                    added += 1

            messagebox.showinfo("Import CSV", f"Zaimportowano: {added}\nPominięto: {skipped}")
            
        except Exception as e:
            messagebox.showerror("Import CSV", f"Nie udało się wczytać pliku.\n\nSzczegóły: {e}")

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], title="Zapisz jako")
        if not path: return
        
        rows = self.db.list_tasks(status=None, query="", area=None)
        # Note: Exporting ALL tasks, assuming filters are not applied to global export button on separate page
        # Original code used current filters. Since this is now a separate page, we export all or we might need to pass filters. 
        # The design shows Export as a separate page, likely exporting everything.
        
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow([
                    "Obszar", "Tytuł", "Opis",
                    "Termin (DD.MM.RRRR)", "Do terminu (dni)",
                    "Status",
                    "Zakończono (DD.MM.RRRR)",
                    "Utworzone (DD.MM.RRRR | HH:MM:SS)"
                ])
                for (_id, title, desc, area, due, status, created, finished_at, left_fixed) in rows:
                    created_pl = to_pl_datetime_from_any(created)
                    if status == "Zrobione" and left_fixed is not None:
                        left_num = int(left_fixed)
                    else:
                        left_num = days_left_signed(due or "")
                    
                    writer.writerow([
                        area or "", title, desc,
                        due or "", str(left_num) if left_num is not None else "",
                        status, finished_at or "", created_pl
                    ])
            messagebox.showinfo("Eksport CSV", "Zapisano plik CSV (UTF-8).")
        except Exception as e:
            messagebox.showerror("Eksport CSV", f"Nie udało się zapisać pliku.\n\nSzczegóły: {e}")
