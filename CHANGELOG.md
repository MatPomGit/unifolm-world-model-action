# Historia Zmian / Changelog

Wszystkie znaczące zmiany w tym projekcie będą dokumentowane w tym pliku.

All notable changes to this project will be documented in this file.

Format oparty na [Keep a Changelog](https://keepachangelog.com/pl/1.0.0/),
a projekt stosuje [Semantic Versioning](https://semver.org/lang/pl/).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Niepublikowane / Unreleased]

### Dodano / Added
- Plik CODE_OF_CONDUCT.md - kodeks postępowania dla społeczności
- Plik SECURITY.md - polityka bezpieczeństwa
- Plik CHANGELOG.md - historia zmian
- Plik .editorconfig - spójne formatowanie kodu
- Plik .pre-commit-config.yaml - automatyczne sprawdzanie kodu
- Plik Makefile - uproszczenie wspólnych zadań
- Podstawowe workflow CI/CD w katalogu .github/workflows
- Plik .flake8 - konfiguracja lintera
- Plik ARCHITECTURE.md - dokumentacja architektury

### Zmieniono / Changed
- Ulepszona dokumentacja w README.md
- Rozszerzona dokumentacja konfiguracji

## [0.0.1] - 2025-09-22

### Dodano / Added
- Kod wdrożeniowy dla robotów Unitree
- Kod treningowy i inferencyjny
- Wagi modeli UnifoLM-WMA-0-Base i UnifoLM-WMA-0-Dual
- Dokumentacja instalacji i konfiguracji
- Przykładowe skrypty treningowe i inferencyjne
- Wsparcie dla robotów Unitree Z1 i G1
- Integracja z formatem LeRobot V2.1
- Interaktywny tryb symulacji
- Tryb podejmowania decyzji dla rzeczywistych robotów
- Dokumentacja po polsku (README.md, KONFIGURACJA.md, PRZEWODNIK_DLA_POCZATKUJACYCH.md)
- Dokumentacja po angielsku (README_en.md, CONFIGURATION.md)
- Dokumentacja po chińsku (README_cn.md)
- Plik CONTRIBUTING.md - przewodnik dla kontrybutorów
- Podstawowe testy jednostkowe
- Konfiguracja pytest

### Architektura / Architecture
- Model świata oparty na architekturze UnifoLM
- Głowa akcji (action head) dla polityki
- Temporal ensembling dla wygładzania akcji
- Wsparcie dla action chunking
- Architektura klient-serwer dla wdrożenia

### Zbiory Danych / Datasets
- Z1_StackBox - układanie pudełek
- Z1_DualArm_StackBox - układanie pudełek dwoma ramionami
- Z1_DualArm_StackBox_V2 - ulepszona wersja
- Z1_DualArm_Cleanup_Pencils - sprzątanie ołówków
- G1_Pack_Camera - pakowanie kamery

### Znane Problemy / Known Issues
- Trening modelu obsługuje tylko jedną główną kamerę
- Wymaga Pythona 3.10.18
- Wymaga CUDA dla treningu i inferencji z GPU

## Typy Zmian / Types of Changes

- **Dodano / Added** - dla nowych funkcji
- **Zmieniono / Changed** - dla zmian w istniejących funkcjach
- **Zdeprecjonowano / Deprecated** - dla funkcji, które zostaną usunięte
- **Usunięto / Removed** - dla usuniętych funkcji
- **Naprawiono / Fixed** - dla naprawionych błędów
- **Bezpieczeństwo / Security** - w przypadku luk bezpieczeństwa

---

## Format Wpisów / Entry Format

```markdown
## [Wersja] - YYYY-MM-DD

### Dodano / Added
- Nowa funkcja X
- New feature X

### Zmieniono / Changed
- Zmiana w funkcji Y
- Change in feature Y

### Naprawiono / Fixed
- Naprawa błędu Z
- Fix for bug Z
```

## Linki / Links

- [Projekt / Project](https://unigen-x.github.io/unifolm-world-model-action.github.io)
- [Modele / Models](https://huggingface.co/collections/unitreerobotics/unifolm-wma-0-68ca23027310c0ca0f34959c)
- [Zbiory Danych / Datasets](https://huggingface.co/unitreerobotics/datasets)
- [Repozytorium / Repository](https://github.com/unitreerobotics/unifolm-world-model-action)
