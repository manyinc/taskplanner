# Specyfikacja Wymagań Aplikacji TaskPlanner

## 1. Wstęp
Niniejszy dokument definiuje wymagania funkcjonalne i pozafunkcjonalne dla systemu **TaskPlanner**. Każde wymaganie posiada unikalny identyfikator, priorytet oraz odniesienie do scenariusza testowego weryfikującego jego spełnienie (Traceability).

## 2. Wymagania Funkcjonalne

### 2.1. Moduł: Zarządzanie Zadaniami

#### F-01: Dodawanie nowych zadań
- **Opis**: System musi umożliwiać użytkownikowi utworzenie nowego zadania poprzez formularz wprowadzania danych. Wymagane pola to: Tytuł zadania. Pola opcjonalne: Opis, Termin realizacji, Kategoria (np. Praca, Dom).
- **Priorytet**: [1 - Wymagane]
- **Weryfikacja**: [TC-01, TC-02] (zob. plik *doc_testy.md*)

#### F-02: Edycja istniejących zadań
- **Opis**: Użytkownik musi posiadać możliwość modyfikacji wszystkich atrybutów zapisanego zadania (tytuł, opis, data, kategoria). Zmiany muszą być trwale zapisywane w bazie danych.
- **Priorytet**: [1 - Wymagane]
- **Weryfikacja**: [TC-03]

#### F-03: Usuwanie zadań
- **Opis**: System musi udostępniać funkcję trwałego usunięcia rekordu zadania z bazy danych. Operacja ta jest nieodwracalna z poziomu interfejsu użytkownika.
- **Priorytet**: [2 - Przydatne]
- **Weryfikacja**: [TC-05]

#### F-04: Zmiana statusu zadania
- **Opis**: System musi umożliwiać zmianę statusu zadania (np. z "Oczekujące" na "Zakończone"). Zmiana ta musi być natychmiast widoczna w interfejsie oraz uwzględniona w statystykach.
- **Priorytet**: [1 - Wymagane]
- **Weryfikacja**: [TC-04]

### 2.2. Moduł: Dashboard i Statystyki

#### F-05: Prezentacja zbiorczych statystyk
- **Opis**: Ekran główny (Dashboard) musi wyświetlać agregowane dane liczbowe: całkowita liczba zadań, liczba zadań wykonanych, liczba zadań zaległych.
- **Priorytet**: [2 - Przydatne]
- **Weryfikacja**: [TC-06]

#### F-06: Wizualizacja postępów
- **Opis**: System powinien generować wykresy graficzne (słupkowe/kołowe) obrazujące rozkład zadań w czasie lub podział według kategorii.
- **Priorytet**: [3 - Opcjonalne]
- **Weryfikacja**: [TC-06]

#### F-07: Kalendarz terminów
- **Opis**: System powinien zawierać interaktywny widżet kalendarza, wizualizujący dni posiadające przypisane terminy zadań.
- **Priorytet**: [2 - Przydatne]
- **Weryfikacja**: [TC-06]

### 2.3. Moduł: Dane i Konfiguracja

#### F-08: Obsługa lokalnej bazy danych
- **Opis**: Aplikacja musi automatycznie inicjalizować plik bazy danych SQLite przy pierwszym uruchomieniu i zapewniać spójność danych podczas operacji CRUD.
- **Priorytet**: [1 - Wymagane]
- **Weryfikacja**: [TC-01, TC-05] (Weryfikacja techniczna zapisu/odczytu)

#### F-09: Import i Eksport danych
- **Opis**: System powinien umożliwiać eksport listy zadań do formatu CSV oraz import danych z kompatybilnego pliku CSV.
- **Priorytet**: [2 - Przydatne]
- **Weryfikacja**: [TC-ImportExport] (Test manualny funkcjonalności)

## 3. Wymagania Pozafunkcjonalne (Non-Functional Requirements)

#### NF-01: Responsywność interfejsu
- **Opis**: Elementy GUI muszą skalować się poprawnie i być czytelne na ekranach o rozdzielczości minimum 1280x720 pikseli.
- **Priorytet**: [1 - Wymagane]
- **Kategoria**: Użyteczność

#### NF-02: Ciemny motyw (Dark Mode)
- **Opis**: Interfejs graficzny powinien być zaprojektowany w ciemnej tonacji kolorystycznej, aby zminimalizować zmęczenie wzroku użytkownika.
- **Priorytet**: [2 - Przydatne]
- **Kategoria**: Ergonomia

#### NF-03: Samowystarczalność (Portable/Standalone)
- **Opis**: Dystrybucja oprogramowania w formacie `.exe` musi działać bez konieczności instalacji zewnętrznych środowisk (np. interpretera Python) na komputerze docelowym.
- **Priorytet**: [1 - Wymagane]
- **Kategoria**: Wdrażanie
