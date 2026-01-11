import os
import json
import re
import sys
import shutil

# -------------------- Paleta i formaty -------------------- #
PL_DATE_FMT = "%d.%m.%Y"
PL_DATETIME_FMT = "%d.%m.%Y | %H:%M:%S"

APP_SIZE = "1300x800"
MIN_SIZE = {"width": 1200, "height": 600}

RADIUS = 16

PALETTE = {
    # Modern Dark Theme Palette
    "bg": "#13141f",         
    "panel": "#1c1d2b",      
    "card": "#1c1d2b",       
    "table_wrap": "#1c1d2b", 
    "row_even": "#232433",   
    "row_odd": "#1c1d2b",    
    "header": "#1c1d2b",     
    "text": "#eeeeee",
    "muted": "#8d90a8",
    
    # Accents
    "accent": "#575ac8",
    "accent_hover": "#4548a8",
    "btn_secondary": "#282a3d",
    "btn_secondary_hover": "#32354a",
    
    # Status Colors (Vibrant/Neon-ish)
    "status_new": "#575ac8",       
    "status_open": "#f59e0b",
    "status_res": "#10b981",       
    
    # Functional Colors
    "danger": "#ef4444",
    "warning": "#f59e0b",
    "success": "#10b981",
    
    "scroll_trough": "#282a3d",
    "scroll_handle": "#575ac8",
    "selected": "#575ac8",
    
    # Soft/Legacy Mappings
    "panel_alt": "#232433",
    "success_soft": "#34d399",
    "danger_soft":  "#f87171",
    "info_soft":    "#fbbf24",
}

# -------------------- Paths & AppData -------------------- #

APP_DATA_DIR = os.path.join(os.environ["APPDATA"], "TaskPlanner")
CONFIG_DIR = os.path.join(APP_DATA_DIR, "config")
ASSETS_DIR = os.path.join(APP_DATA_DIR, "assets")

# Ensure base directories exist
for d in [APP_DATA_DIR, CONFIG_DIR, ASSETS_DIR]:
    if not os.path.exists(d):
        try:
            os.makedirs(d)
        except: pass

DB_CONFIG_FILE = os.path.join(CONFIG_DIR, "db_config.json")
AREAS_CONFIG_FILE = os.path.join(CONFIG_DIR, "areas_config.json")
DB_PATH = os.path.join(APP_DATA_DIR, "taskplanner.db")
PRESET_AREAS = ["Studia", "Dom", "Praca", "Inne"]

def initialize_app():
    """Calculates resource path and unpacks assets if frozen."""
    # Logic to handle PyInstaller _MEIPASS
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    # Initial copy of assets to APPDATA if they don't exist
    source_assets = os.path.join(base_path, "assets")
    
    if os.path.exists(source_assets):
        # We walk through source assets and copy missing ones
        try:
            for item in os.listdir(source_assets):
                s = os.path.join(source_assets, item)
                d = os.path.join(ASSETS_DIR, item)
                if os.path.isfile(s):
                    if not os.path.exists(d):
                         shutil.copy2(s, d)
        except Exception:
            pass

def load_db_config():
    global DB_PATH
    if os.path.exists(DB_CONFIG_FILE):
        try:
            with open(DB_CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "db_path" in data and data["db_path"]:
                    DB_PATH = data["db_path"]
        except: pass
    return DB_PATH

def save_db_config(path):
    global DB_PATH
    DB_PATH = path
    try:
        with open(DB_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"db_path": DB_PATH}, f)
    except Exception:
        pass

def load_areas_config():
    global PRESET_AREAS
    if os.path.exists(AREAS_CONFIG_FILE):
        try:
            with open(AREAS_CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "areas" in data and isinstance(data["areas"], list):
                    for a in data["areas"]:
                        if a not in PRESET_AREAS:
                            PRESET_AREAS.append(a)
        except: pass

def save_areas_config(new_areas_list=None):
    pass

# Initial loads
initialize_app()
load_db_config()
load_areas_config()