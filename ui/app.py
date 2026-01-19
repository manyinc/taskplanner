import customtkinter as ctk
import sys
from core.config import APP_SIZE, MIN_SIZE, PALETTE
from data.database import DatabaseManager
from ui.styles import StyleManager
from ui.components.sidebar import Sidebar
from ui.components.header import Header
from ui.pages.home_page import HomePage
from ui.pages.tasks_page import TasksPage
from ui.pages.form_page import TaskFormPage
from ui.pages.import_export_page import ImportExportPage
from ui.pages.settings_page import SettingsPage


from ui.components.window_manager import WindowManager


class TaskPlanner(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("TaskPlanner")
        self.geometry(APP_SIZE)
        self.minsize(MIN_SIZE["width"], MIN_SIZE["height"])

        # Customize Title Bar & Icon
        WindowManager.setup_icon(self, "assets/icon.ico")
        WindowManager.setup_title_bar_color(self)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.configure(fg_color=PALETTE["bg"])

        self.db = DatabaseManager()
        StyleManager.setup_style(self)

        self.init_layout()
        self.active_dropdowns = []
        self.current_page_name = None
        self.current_frame = None

        self.show_page("home")

    def on_close(self):
        self.destroy()
        sys.exit(0)

    def init_layout(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, navigation_callback=self.show_page)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.main_view = ctk.CTkFrame(self, fg_color="transparent")
        self.main_view.grid(row=0, column=1, sticky="nsew")
        self.main_view.grid_columnconfigure(0, weight=1)
        self.main_view.grid_rowconfigure(1, weight=1)

        self.header = Header(self.main_view, search_callback=self.on_global_search)
        self.header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))

        self.content_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def show_page(self, page_name, **kwargs):
        self.sidebar.update_active_button(page_name)

        titles = {
            "home": "Strona główna",
            "tasks": "Lista Zadań",
            "new_task": "Nowe Zadanie",
            "edit_task": "Edycja Zadania",
            "import": "Importowanie Danych",
            "export": "Eksport Danych",
            "settings": "Ustawienia",
        }
        self.header.set_title(titles.get(page_name, "TaskPlanner"))

        for child in self.content_frame.winfo_children():
            child.destroy()

        if page_name == "home":
            self.current_frame = HomePage(self.content_frame, self.db)
        elif page_name == "tasks":
            self.current_frame = TasksPage(self.content_frame, self.db, self.show_page)
        elif page_name == "new_task":
            self.current_frame = TaskFormPage(
                self.content_frame, self.db, self.show_page
            )
        elif page_name == "edit_task":
            self.current_frame = TaskFormPage(
                self.content_frame,
                self.db,
                self.show_page,
                task_id=kwargs.get("task_id"),
            )
        elif page_name == "import":
            self.current_frame = ImportExportPage(
                self.content_frame, self.db, mode="import"
            )
        elif page_name == "export":
            self.current_frame = ImportExportPage(
                self.content_frame, self.db, mode="export"
            )
        elif page_name == "settings":
            self.current_frame = SettingsPage(self.content_frame, self.db)

        if self.current_frame:
            self.current_frame.grid(row=0, column=0, sticky="nsew")

        self.current_page_name = page_name

    def on_global_search(self, query):
        if self.current_page_name != "tasks" and query:
            self.show_page("tasks")

        if isinstance(self.current_frame, TasksPage):
            self.current_frame.update_search(query)
