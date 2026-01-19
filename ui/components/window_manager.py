import ctypes
from ctypes import windll, c_int, byref
import os

#Współtworzone z ai

class WindowManager:
    """
    Klasa pomocnicza do zarządzania wyglądem okna w systemie Windows.
    Obsługuje ustawianie ikony oraz dostosowywanie koloru paska tytułu (tryb ciemny i niestandardowy RGB).
    """

    @staticmethod
    def setup_icon(window, icon_path):
        """
        Ustawia ikonę okna oraz ikonę na pasku zadań (AppUserModelID).
        :param window: Instancja okna CTk/Tk.
        :param icon_path: Absolutna ścieżka do pliku .ico.
        """
        # 1. Ustaw AppUserModelID, aby odłączyć się od domyślnej grupy Pythona
        try:
            myappid = "mycompany.myproduct.subproduct.version"  # Dowolny ciąg znaków
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            print(f"Failed to set AppUserModelID: {e}")

        # 2. Set window icon
        if os.path.exists(icon_path):
            try:
                window.iconbitmap(icon_path)
            except Exception as e:
                print(f"Failed to set icon: {e}")
        else:
            print(f"Icon not found at: {icon_path}")

    @staticmethod
    def setup_title_bar_color(window):
        """
        Zmusza pasek tytułu systemu Windows w tryb ciemny i ustawia niestandardowy kolor tła
        pasujący do motywu aplikacji.
        :param window: Instancja okna CTk/Tk.
        """
        try:
            window.update()
            hwnd = windll.user32.GetParent(window.winfo_id())

            #Stałe dla API DWM
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            DWMWA_CAPTION_COLOR = 35
            DWMWA_TEXT_COLOR = 36

            # 1. Włącz tryb ciemny dla kontrolek okna (przyciski min/max/close)
            value = c_int(2)
            windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, byref(value), ctypes.sizeof(value)
            )

            # 2. Ustaw dokładny kolor tła (format BGR: 0x00BBGGRR)
            # Tło aplikacji to #13141f (R=19, G=20, B=31) -> 0x001F1413
            # Używamy tego, aby pasek tytułu idealnie komponował się z ciałem aplikacji.
            color_ref = 0x001F1413

            color_value = c_int(color_ref)
            windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_CAPTION_COLOR,
                byref(color_value),
                ctypes.sizeof(color_value),
            )

            # 3. Ustaw kolor tekstu na biały/jasnoszary (0x00EEEEEE)
            text_color = 0x00EEEEEE
            text_value = c_int(text_color)
            windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_TEXT_COLOR, byref(text_value), ctypes.sizeof(text_value)
            )

        except Exception as e:
            print(f"Failed to set title bar color: {e}")
