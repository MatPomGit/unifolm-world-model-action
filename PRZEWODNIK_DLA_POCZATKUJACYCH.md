# Przewodnik dla Początkujących - Beginner's Guide

## Przegląd Projektu

Ten projekt, **UnifoLM-WMA-0**, to kompleksowy framework do uczenia robotów przy użyciu modeli świata (world models). Jest przeznaczony dla studentów i badaczy, którzy chcą nauczyć się, jak trenować i wdrażać modele AI na rzeczywistych robotach.

## Kluczowe Koncepcje

### 1. Model Świata (World Model)
Model świata to AI, która "rozumie" fizyczne zasady działania świata. Przewiduje co się stanie, gdy robot wykona określoną akcję.

**Analogia:** Jak szachista, który potrafi przewidzieć kilka ruchów do przodu, model świata pozwala robotowi planować swoje działania przed ich wykonaniem.

### 2. Polityka (Policy)
Polityka to strategia decyzyjna robota - algorytm określający jakie akcje wykonać w danej sytuacji.

**Analogia:** To jak "mózg" robota - otrzymuje informacje ze zmysłów (kamery, czujniki) i decyduje co robić dalej.

### 3. Action Chunking
Zamiast przewidywać jedną akcję na raz, model przewiduje sekwencję akcji (np. 16 kroków). To pozwala na:
- Lepsze planowanie długoterminowe
- Płynniejsze trajektorie
- Mniejszą liczbę zapytań do serwera

### 4. Temporal Ensembling
Technika wygładzania akcji poprzez uśrednianie przewidywań z wielu kroków czasowych. Eliminuje szarpnięcia i sprawia, że ruchy są płynne.

**Matematycznie:** `akcja_wygładzona = α * akcja_nowa + (1-α) * akcja_poprzednia`

## Struktura Workflow

### Trening Modelu
```
Zbieranie danych → Przetwarzanie → Trening → Ewaluacja → Dostrajanie
     ↓                  ↓            ↓          ↓           ↓
Demonstracje      Format LeRobot   Model AI   Metryki   Iteracja
```

### Wdrożenie na Robocie
```
Serwer (GPU)                    Klient (Robot)
    ↓                                ↓
Model AI                      Zbieranie obserwacji
    ↓                                ↓
Przewidywanie akcji ← ─ ─ ─ ─  Wysłanie obserwacji
    ↓                                ↑
Zwrócenie akcji  ─ ─ ─ ─ ─ →  Wykonanie akcji
```

## Typowe Problemy i Rozwiązania

### Problem: Robot nie reaguje na komendy
**Możliwe przyczyny:**
- Brak połączenia sieciowego
- Kontroler nie jest uruchomiony
- Zły adres IP

**Diagnostyka:**
```bash
# Sprawdź połączenie
ping <IP_robota>

# Sprawdź status kontrolera
ps aux | grep ctrl

# Sprawdź porty
netstat -an | grep 8000
```

### Problem: Ruchy są szarpane
**Możliwe przyczyny:**
- Za wysoka częstotliwość sterowania
- Problemy z siecią
- Brak temporal ensembling

**Rozwiązanie:**
```python
# Zmniejsz częstotliwość
--control_freq 15  # zamiast 30

# Zwiększ współczynnik wygładzania
temporal_ensemble_coeff=0.05  # zamiast 0.01
```

### Problem: Model przewiduje złe akcje
**Możliwe przyczyny:**
- Za mało danych treningowych
- Niezgodność między danymi a środowiskiem
- Model nie jest dostatecznie wytrenowany

**Rozwiązanie:**
- Zbierz więcej różnorodnych demonstracji
- Sprawdź normalizację danych
- Trenuj dłużej lub zwiększ rozmiar modelu

## Najlepsze Praktyki

### Bezpieczeństwo
1. **Zawsze testuj w symulatorze** przed rzeczywistym robotem
2. **Ustaw limity bezpieczeństwa** dla prędkości i zakresu ruchu
3. **Miej przycisk awaryjny** w zasięgu ręki
4. **Nigdy nie zostawiaj** robota bez nadzoru podczas testów

### Wydajność
1. **Monitoruj opóźnienia** między robotem a serwerem
2. **Używaj kabla Ethernet** zamiast WiFi (gdy możliwe)
3. **Zamknij niepotrzebne procesy** na komputerze robota
4. **Optymalizuj rozdzielczość obrazu** - nie zawsze więcej = lepiej

### Debugowanie
1. **Zapisuj wszystkie logi** do plików
2. **Nagrywaj wideo** każdego epizodu
3. **Wizualizuj przewidywania** modelu
4. **Porównuj z demonstracjami** człowieka

## Zasoby Edukacyjne

### Kursy Online
- **CS231n (Stanford)**: Computer Vision
- **CS285 (Berkeley)**: Deep Reinforcement Learning
- **ROS Tutorials**: Robot Operating System

### Książki
- "Probabilistic Robotics" - Sebastian Thrun
- "Reinforcement Learning" - Sutton & Barto
- "Deep Learning" - Goodfellow et al.

### Społeczność
- Forum Unitree: https://www.unitree.com/
- Discord serwer robotyki
- GitHub Issues tego projektu

## Ścieżka Nauki

### Poziom 1: Podstawy (1-2 tygodnie)
- [ ] Zrozum strukturę projektu
- [ ] Uruchom przykładowe testy
- [ ] Wykonaj replay demonstracji
- [ ] Przeczytaj całą dokumentację

### Poziom 2: Trening (2-4 tygodnie)
- [ ] Przygotuj własny zbiór danych
- [ ] Wytrenuj model na małym zbiorze
- [ ] Oceń wydajność w symulacji
- [ ] Dostosuj hiperparametry

### Poziom 3: Wdrożenie (2-4 tygodnie)
- [ ] Uruchom serwer polityki
- [ ] Połącz się z rzeczywistym robotem
- [ ] Wykonaj pierwsze testy bezpieczeństwa
- [ ] Przeprowadź pełne ewaluacje

### Poziom 4: Zaawansowane (ongoing)
- [ ] Dodaj nowe zadania
- [ ] Eksperymentuj z różnymi architekturami
- [ ] Optymalizuj wydajność
- [ ] Publikuj wyniki

## Słowniczek Terminów

- **DoF (Degrees of Freedom)**: Stopnie swobody - liczba niezależnych ruchów
- **Joint**: Przegub - punkt obrotu w robocie
- **End Effector**: Efektor końcowy - narzędzie na końcu ramienia (chwytaka)
- **Trajectory**: Trajektoria - ścieżka ruchu robota w czasie
- **Policy**: Polityka - strategia decyzyjna robota
- **Rollout**: Epizod - jedna kompletna próba wykonania zadania
- **Inference**: Inferencja - używanie wytrenowanego modelu do przewidywań
- **Checkpoint**: Punkt kontrolny - zapisany stan modelu
- **Epoch**: Epoka - jedno pełne przejście przez dane treningowe
- **Batch**: Partia - podzbiór danych przetwarzany jednocześnie

## Następne Kroki

Po opanowaniu podstaw:
1. Eksperymentuj z różnymi zadaniami
2. Dołącz do społeczności i dziel się wynikami
3. Przyczyniaj się do projektu (contribute)
4. Rozważ publikację swoich odkryć

---

**Pamiętaj:** Nauka robotyki to maraton, nie sprint. Bądź cierpliwy, eksperymentuj i nie bój się popełniać błędów - to najlepszy sposób nauki!

Powodzenia w Twojej przygodzie z robotyką! 🤖🚀
