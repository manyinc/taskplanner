import customtkinter as ctk
from datetime import datetime, date, timedelta
from core.config import PALETTE, RADIUS
from core.utils import parse_pl_date, to_pl_date_from_any, parse_date_pl_or_iso

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

class HomePage(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master, fg_color="transparent")
        self.db = db_manager
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        rows = self.db.list_tasks(status=None, query="", area=None)

        # 1. Status Counts
        status_counts = {"Do zrobienia": 0, "W toku": 0, "Zrobione": 0, "Po terminie": 0}
        
        for r in rows:
            # r: 0:id, 1:title, 2:desc, 3:area, 4:due, 5:status, 6:created, 7:finished, 8:left_fixed
            st = r[5]
            due = r[4]
            
            if st == "Zrobione":
                status_counts["Zrobione"] += 1
            else:
                is_overdue = False
                if due:
                    try:
                        d_obj = parse_pl_date(due)
                        if d_obj < date.today():
                            is_overdue = True
                    except: pass
                
                if is_overdue:
                    status_counts["Po terminie"] += 1
                elif st == "W toku":
                    status_counts["W toku"] += 1
                else:
                    status_counts["Do zrobienia"] += 1

        # 2. Area Counts
        area_counts = {}
        for r in rows:
            area = r[3] if r[3] else "Brak"
            area_counts[area] = area_counts.get(area, 0) + 1

        # 3. Monthly Finished
        monthly_stats = {}
        for i in range(5, -1, -1):
            date_val = datetime.now() - timedelta(days=30*i)
            key = date_val.strftime("%Y-%m")
            monthly_stats[key] = 0
        
        for r in rows:
            if r[5] == "Zrobione" and r[7]:
                 try:
                     dt = datetime.strptime(r[7], "%d.%m.%Y")
                     key = dt.strftime("%Y-%m")
                     monthly_stats[key] = monthly_stats.get(key, 0) + 1
                 except Exception: pass
        
        sorted_months = sorted(monthly_stats.keys())[-6:]
        month_labels = sorted_months
        month_values = [monthly_stats[k] for k in sorted_months]

        # 4. Farthest Due Date
        max_due = "Brak zadań"
        valid_dates = []
        for r in rows:
             if r[5] != "Zrobione" and r[4]:
                 d = parse_date_pl_or_iso(r[4])
                 if d: valid_dates.append(d)
        if valid_dates:
             max_due = max(valid_dates).strftime("%d.%m.%Y")

        # Tiles
        self._build_status_chart(status_counts)
        self._build_bar_chart(month_labels, month_values)
        self._build_calendar()
        self._build_area_chart(area_counts)
        self._build_deadline_tile(max_due)

    def _build_status_chart(self, counts):
        tile = ctk.CTkFrame(self, fg_color=PALETTE["panel"], corner_radius=RADIUS)
        tile.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        if HAS_MATPLOTLIB:
            try:
                fig1, ax1 = plt.subplots(figsize=(5, 3), dpi=80)
                fig1.patch.set_facecolor(PALETTE["panel"])
                
                raw_labels = [k for k, v in counts.items() if v > 0]
                sizes = [v for k, v in counts.items() if v > 0]
                labels_with_counts = [f"{k} - {v}" for k, v in zip(raw_labels, sizes)]
                
                color_map = {
                    "Do zrobienia": PALETTE["status_new"],
                    "W toku": PALETTE["status_open"],
                    "Zrobione": PALETTE["status_res"],
                    "Po terminie": PALETTE["danger"]
                }
                final_colors = [color_map.get(l, "#888") for l in raw_labels]
                
                ax1.pie(
                    sizes, labels=labels_with_counts, autopct='%1.1f%%', 
                    startangle=90, colors=final_colors, pctdistance=0.80, 
                    textprops={'color': "white", 'fontsize': 11, 'weight': 'bold'}
                )
                
                centre_circle = plt.Circle((0,0), 0.60, fc=PALETTE["panel"])
                fig1.gca().add_artist(centre_circle)
                ax1.set_title("Status Zadań", color="white", fontsize=14, weight='bold')
                
                canvas1 = FigureCanvasTkAgg(fig1, master=tile)
                canvas1.draw()
                canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            except Exception as e:
                ctk.CTkLabel(tile, text=f"Błąd wykresu: {e}").pack()
        else:
             ctk.CTkLabel(tile, text="Brak matplotlib").pack()

    def _build_bar_chart(self, labels, values):
        tile = ctk.CTkFrame(self, fg_color=PALETTE["panel"], corner_radius=RADIUS)
        tile.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        if HAS_MATPLOTLIB:
            try:
                fig2, ax2 = plt.subplots(figsize=(4, 3), dpi=80)
                fig2.patch.set_facecolor(PALETTE["panel"])
                ax2.set_facecolor(PALETTE["panel"])
                
                ax2.bar(labels, values, color=PALETTE["accent"])
                ax2.set_title("Ostatnie 6 Miesięcy (Zrobione)", color="white", fontsize=12, weight='bold')
                ax2.tick_params(axis='x', colors='white', labelsize=10, rotation=45)
                ax2.tick_params(axis='y', colors='white', labelsize=10)
                from matplotlib.ticker import MaxNLocator
                ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
                ax2.spines['bottom'].set_color('white')
                ax2.spines['left'].set_color('white')
                ax2.spines['top'].set_color('none')
                ax2.spines['right'].set_color('none')
                
                plt.tight_layout()
                canvas2 = FigureCanvasTkAgg(fig2, master=tile)
                canvas2.draw()
                canvas2.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
            except Exception as e:
                ctk.CTkLabel(tile, text=f"Błąd wykresu: {e}").pack()

    def _build_calendar(self):
        tile = ctk.CTkFrame(self, fg_color=PALETTE["panel"], corner_radius=RADIUS)
        tile.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        try:
            from tkcalendar import Calendar
            cal = Calendar(
                tile, selectmode="day",
                background=PALETTE["panel"], disabledbackground=PALETTE["panel"],
                bordercolor=PALETTE["header"], headersbackground=PALETTE["header"],
                normalbackground=PALETTE["panel"], selectbackground=PALETTE["accent"],
                normalforeground=PALETTE["text"], headersforeground=PALETTE["muted"],
                weekendbackground=PALETTE["panel"], weekendforeground=PALETTE["text"],
                othermonthbackground=PALETTE["panel"], othermonthwebackground=PALETTE["panel"],
                othermonthforeground=PALETTE["muted"], othermonthweforeground=PALETTE["muted"],
                font=("Arial", 10)
            )
            cal.pack(fill="both", expand=True, padx=10, pady=10)
        except ImportError:
             ctk.CTkLabel(tile, text="Brak tkcalendar").pack(expand=True)

    def _build_area_chart(self, counts):
        tile = ctk.CTkFrame(self, fg_color=PALETTE["panel"], corner_radius=RADIUS)
        tile.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        if HAS_MATPLOTLIB:
            try:
                fig3, ax3 = plt.subplots(figsize=(4, 3), dpi=80)
                fig3.patch.set_facecolor(PALETTE["panel"])
                
                l_area = list(counts.keys())
                v_area = list(counts.values())
                labels_with_counts = [f"{k} - {v}" for k, v in zip(l_area, v_area)]
                
                import itertools
                cycler = itertools.cycle([PALETTE["accent"], PALETTE["status_open"], PALETTE["success"], "#e91e63", "#9c27b0", "#00bcd4"])
                colors = [next(cycler) for _ in l_area]
                
                ax3.pie(
                    v_area, labels=labels_with_counts, autopct=None, 
                    pctdistance=1.2, startangle=140, colors=colors, 
                    textprops={'color': "white", 'fontsize': 10, 'weight': 'bold'}
                )
                ax3.set_title("Zadania wg Obszaru", color="white", fontsize=12, weight='bold')
                
                centre_circle = plt.Circle((0,0), 0.60, fc=PALETTE["panel"])
                fig3.gca().add_artist(centre_circle)

                canvas3 = FigureCanvasTkAgg(fig3, master=tile)
                canvas3.draw()
                canvas3.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
            except Exception as e:
                ctk.CTkLabel(tile, text=f"Błąd: {e}").pack()

    def _build_deadline_tile(self, max_due):
        tile = ctk.CTkFrame(self, fg_color=PALETTE["accent"], corner_radius=RADIUS)
        tile.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        
        tile.grid_columnconfigure(0, weight=1)
        tile.grid_rowconfigure(0, weight=1)
        
        inner = ctk.CTkFrame(tile, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(inner, text="Najdalszy Termin", text_color="#DDDDDD", font=("Arial", 16)).pack(pady=(0, 10))
        ctk.CTkLabel(inner, text=max_due, text_color="#FFFFFF", font=("Arial", 28, "bold")).pack()
        ctk.CTkLabel(inner, text="Zaplanuj swoje zadania!", text_color="#EEEEEE", font=("Arial", 12)).pack(pady=(20, 0))
