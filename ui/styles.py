from tkinter import ttk
from core.config import PALETTE

class StyleManager:
    @staticmethod
    def setup_style(root):
        style = ttk.Style(root)
        try:
            style.theme_use("clam")
        except:
            pass

        style.layout("Dark.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        style.configure(
            "Dark.Treeview",
            background=PALETTE["row_even"],
            fieldbackground=PALETTE["row_even"],
            foreground=PALETTE["text"],
            borderwidth=0,
            rowheight=32,
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", PALETTE["selected"])],
            foreground=[("selected", PALETTE["text"])],
        )
        style.configure(
            "Dark.Treeview.Heading",
            background=PALETTE["header"],
            foreground=PALETTE["muted"],
            relief="flat",
            font=("Arial", 11, "bold")
        )
        style.map(
            "Dark.Treeview.Heading",
            background=[("active", PALETTE["header"])],
            foreground=[("active", PALETTE["text"])],
        )
