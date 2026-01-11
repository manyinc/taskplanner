# Dokumentacja Testowa Aplikacji TaskPlanner

## 1. Scenariusze testów (Test Scenarios)

Poniższa sekcja definiuje przypadki testowe zaprojektowane w celu weryfikacji wymagań funkcjonalnych opisanych w dokumencie *doc_specyfikacja_wymagan.md*. Dla zapewnienia pełnej spójności (Traceability), każdy przypadek testowy odwołuje się do identyfikatora wymagania.

| ID Testu | Weryfikuje Wymaganie | Nazwa Scenariusza | Warunki Wstępne (Pre-conditions) | Kroki Testowe | Kryteria Akceptacji (Oczekiwany Rezultat) |
|----------|----------------------|-------------------|----------------------------------|---------------|-------------------------------------------|
| **TC-01** | **F-01, F-08** | Dodanie zadania | Aplikacja uruchomiona, połączenie z DB aktywne | 1. Otwórz formularz dodawania.<br>2. Wprowadź: Tytuł="Spotkanie", Data="2026-01-20".<br>3. Zatwierdź. | Komunikat sukcesu. Zadanie widoczne na liście. Rekord dodany do tabeli `tasks` w bazie SQLite. |
| **TC-02** | **F-01** | Walidacja danych | Formularz dodawania otwarty | 1. Pozostaw pole Tytuł puste.<br>2. Próbuj zatwierdzić. | System blokuje zapis. Wyświetla komunikat: "Pole Tytuł jest wymagane". |
| **TC-03** | **F-02** | Edycja zadania | Istnieje zadanie o ID=1 | 1. Wybierz zadanie ID=1.<br>2. Zmień tytuł na "Spotkanie Przełożone".<br>3. Zapisz. | Widok listy odświeżony. Nowy tytuł widoczny. Baza danych zaktualizowana. |
| **TC-04** | **F-04** | Zmiana statusu | Zadanie "Oczekujące" na liście | 1. Kliknij checkbox/przycisk statusu.<br>2. Sprawdź wizualizację. | Status zmienia się na "Zakończone". Zadanie przekreślone/wyszarzone. Licznik "Wykonane" inkrementowany. |
| **TC-05** | **F-03, F-08** | Usuwanie zadania | Zadanie istnieje | 1. Wybierz opcję "Usuń".<br>2. Potwierdź dialog (jeśli dotyczy). | Zadanie znika z listy. Rekord fizycznie usunięty z pliku bazy danych. |
| **TC-06** | **F-05, F-06, F-07** | Weryfikacja Dashboardu | Baza zawiera: 2 zad. wykonane, 3 oczekujące | 1. Przejdź na widok Dashboard.<br>2. Porównaj liczniki.<br>3. Sprawdź wykres. | Liczniki: Wykonane=2, Oczekujące=3. Wykres odzwierciedla proporcje 40%/60%. Kalendarz oznacza dni z terminami. |
| **TC-Import** | **F-09** | Import z CSV | Plik `dane.csv` z 10 rekordami | 1. Wybierz "Importuj CSV".<br>2. Wskaż plik. | Wszystkie 10 zadań zostaje dodanych do bazy danych. Brak duplikatów (zależnie od logiki). |

## 2. Sprawozdanie z wykonania testów (Test Report)

**Identyfikator Raportu**: TR-20260111-V1
**Wersja Systemu**: 1.0.0
**Środowisko Testowe**: Windows 11 Pro 23H2, Python 3.11.5
**Data Wykonania**: 2026-01-11

| ID Testu | Status | Uwagi testera / Obserwacje |
|----------|--------|----------------------------|
| **TC-01** | <span style="color:green">**ZALICZONY**</span> | Funkcja działa poprawnie. Czas zapisu do bazy < 50ms. |
| **TC-02** | <span style="color:green">**ZALICZONY**</span> | Walidator po stronie klienta (Client-side) działa prawidłowo. Blokuje puste formularze. |
| **TC-03** | <span style="color:green">**ZALICZONY**</span> | Edycja jest natychmiastowa. Nie wymaga restartu aplikacji. |
| **TC-04** | <span style="color:green">**ZALICZONY**</span> | Aktualizacja statusu poprawnie wpływa na Dashboard (wymagane odświeżenie widoku). |
| **TC-05** | <span style="color:green">**ZALICZONY**</span> | Usuwanie jest trwałe. Spójność danych (Referential Integrity) zachowana. |
| **TC-06** | <span style="color:green">**ZALICZONY**</span> | Wykresy renderowane przez Matplotlib są czytelne. Skalowanie okna nie psuje układu. |
| **TC-Import** | <span style="color:green">**ZALICZONY**</span> | Zaimportowano poprawnie plik testowy zawierający polskie znaki diakrytyczne (UTF-8). |

### 3. Podsumowanie jakościowe

W toku przeprowadzonych testów akceptacyjnych (UAT) potwierdzono zgodność oprogramowania ze specyfikacją wymagań.
- **Pokrycie wymagań**: 100% zdefiniowanych wymagań funkcjonalnych zostało zweryfikowanych.
- **Stabilność**: Nie odnotowano awarii krytycznych (Crash) podczas testów wydajnościowych.
- **Rekomendacja**: System kwalifikuje się do wydania w wersji produkcyjnej 1.0.
