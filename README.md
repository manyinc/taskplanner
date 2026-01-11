# TaskPlanner

**TaskPlanner** to nowoczesna aplikacja desktopowa do zarządzania zadaniami, projektami i terminami, napisana w języku Python przy użyciu biblioteki CustomTkinter.

## Funkcjonalności

- **Zarządzanie Zadaniami**: Dodawanie, edycja i usuwanie zadań.
- **Kategorie**: Przypisywanie zadań do obszarów (Studia, Dom, Praca, itp.).
- **Śledzenie Terminów**: Automatyczne obliczanie dni pozostałych do terminu.
- **Dashboard**: Podgląd statystyk, wykresów statusu i kalendarza.
- **Import/Eksport**: Możliwość zapisu i odczytu zadań z plików CSV.
- **Baza Danych**: Automatyczny zapis danych w pliku SQLite (`taskplanner.db`) w profilu użytkownika.
- **Nowoczesny Interfejs**: Ciemny motyw z intuicyjną nawigacją.

## Wymagania

- Python 3.8 lub nowszy
- System operacyjny Windows (testowano na Windows 10/11)

## Instalacja i Uruchomienie (Developerskie)

Aby uruchomić aplikację w trybie developerskim, wykonaj poniższe kroki (zalecane użycie terminala PowerShell lub CMD):

1. **Utwórz środowisko wirtualne**:
   ```bash
   python -m venv .venv
   ```

2. **Aktywuj środowisko**:
   - Windows (CMD): `.venv\Scripts\activate.bat`
   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`

3. **Zainstaluj zależności**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Uruchom aplikację**:
   Możesz skorzystać z gotowego skryptu:
   ```bash
   run.bat
   ```
   Lub uruchomić ręcznie:
   ```bash
   python main.py
   ```

## Budowanie Aplikacji (.exe)

Aby utworzyć plik wykonywalny `.exe`:

1. Upewnij się, że masz aktywne środowisko wirtualne i zainstalowane zależności (w tym `pyinstaller`).
2. Uruchom skrypt budujący:
   ```bash
   build.bat
   ```
3. Gotowy plik `TaskPlanner.exe` znajdzie się w folderze `dist/`.

## Struktura Projektu

- `main.py`: Punkt wejściowy aplikacji.
- `core/`: Konfiguracja i narzędzia.
- `data/`: Obsługa bazy danych.
- `ui/`: Kod interfejsu użytkownika (strony, komponenty, style).
- `config/`: Pliki konfiguracyjne (tworzone automatycznie).
