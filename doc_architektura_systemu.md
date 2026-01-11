# Architektura systemu i oprogramowania TaskPlanner

## 1. Architektura rozwoju (Development Environment)

Poniższy wykaz prezentuje stos technologiczny wykorzystywany w procesie wytwórczym oprogramowania. Dobór narzędzi podyktowany został wymaganiami nowoczesnego cyklu rozwoju oprogramowania (SDLC).

| Technologia / Narzędzie | Wersja | Przeznaczenie i Rola w Systemie |
|-------------------------|--------|---------------------------------|
| **Python** | 3.8+ | Język programowania wysokiego poziomu. Implementuje logikę biznesową, warstwę dostępu do danych (DAL) oraz integrację komponentów. |
| **Visual Studio Code** | Stable | Podstawowe środowisko programistyczne (IDE). Wykorzystywane do edycji kodu, debugowania, analizy statycznej oraz zarządzania repozytorium. |
| **Git** | 2.30+ | Rozproszony system kontroli wersji (VCS). Umożliwia śledzenie historii zmian, zarządzanie gałęziami (branching) oraz współpracę zespołową. |
| **PyInstaller** | 5.0+ | Narzędzie do budowania dystrybucji (Build Tool). Odpowiada za kompilację kodu bajtowego i pakowanie zależności do pliku wykonywalnego (`.exe`). |
| **Microsoft Windows** | 10/11 | Platforma operacyjna stacji roboczej dewelopera. Zapewnia kompatybilność środowiskową z platformą docelową. |

## 2. Architektura uruchomieniowa (Runtime Environment)

Wykaz komponentów programowych wymaganych do funkcjonowania aplikacji w środowisku produkcyjnym (użytkownika końcowego).

| Komponent / Biblioteka | Wersja | Przeznaczenie i Rola w Systemie |
|------------------------|--------|---------------------------------|
| **CustomTkinter** | 5.2.0 | Biblioteka GUI Wrapper. Dostarcza nowoczesne kontrolki (widgety) z natywną obsługą trybu ciemnego i skalowania HighDPI w systemie Windows. |
| **SQLite3** | Native | Silnik relacyjnej bazy danych. Działa w procesie aplikacji (in-process), zapewniając lokalną trwałość danych bez konieczności konfiguracji serwera. |
| **Matplotlib** | 3.7.0 | Biblioteka do wizualizacji danych. Odpowiada za renderowanie wykresów statystycznych na panelu Dashboard w czasie rzeczywistym. |
| **Pillow (PIL)** | 10.0.0 | Biblioteka przetwarzania obrazu. Obsługuje ładowanie, skalowanie i wyświetlanie zasobów graficznych (ikony, logotypy) w interfejsie. |
| **tkcalendar** | 1.6.1 | Komponent kalendarza. Rozszerza standardowe możliwości GUI o interaktywny wybór dat i wizualizację terminów. |
| **System Operacyjny** | Win 10/11 | Środowisko wykonawcze (Host OS). Zarządza procesami, pamięcią operacyjną oraz obsługą urządzeń wejścia/wyjścia. |

## 3. Prezentacja technologii

### 3.1. Język Python i paradygmat obiektowy
Projekt został zrealizowany w języku **Python**, wykorzystując **paradygmat programowania obiektowego (OOP)**. Architektura kodu bazuje na klasach reprezentujących główne byty domenowe (np. `Task`, `Category`) oraz kontrolery widoków. Podejście to zapewnia modularność, łatwość testowania (testability) oraz możliwość przyszłej rozbudowy systemu (extensibility).

### 3.2. Warstwa prezentacji: CustomTkinter
Jako fundament interfejsu graficznego wybrano **CustomTkinter**. Jest to nowoczesna abstrakcja nad standardową biblioteką `tkinter`, która rozwiązuje problemy związane z przestarzałym wyglądem natywnych kontrolek. Technologia ta implementuje własny silnik renderowania stylów, umożliwiając tworzenie spójnych, estetycznych interfejsów (tzw. *Modern UI*) zgodnych z aktualnymi trendami User Experience (UX).

### 3.3. Warstwa trwałoci danych: SQLite (ACID)
System wykorzystuje **SQLite** jako wbudowany (embedded) silnik bazy danych. Kluczową cechą jest zgodność ze standardem **ACID** (Atomicity, Consistency, Isolation, Durability), co gwarantuje bezpieczeństwo danych nawet w przypadku awarii zasilania. Baza danych przechowywana jest w pojedynczym pliku na dysku użytkownika, co eliminuje skomplikowaną procedurę instalacji i konfiguracji serwerów bazodanowych.

### 3.4. Dystrybucja i Wdrażanie (Deployment)
Dzięki zastosowaniu **PyInstaller**, aplikacja jest dystrybuowana jako samodzielny artefakt (Single File Executable). Proces ten, zwany "zamrażaniem" (freezing), polega na dołączeniu interpretera Pythona oraz wszystkich skompilowanych bibliotek dynamicznych (.dll) do pliku binarnego. Użytkownik końcowy otrzymuje produkt gotowy do uruchomienia (Plug & Play), niewymagający instalacji dodatkowego oprogramowania runtime.
