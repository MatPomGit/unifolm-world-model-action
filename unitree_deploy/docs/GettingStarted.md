# Pierwsze Kroki - Getting Started

**Dla początkujących:** Ten dokument pokazuje jak zorganizowany jest kod i jak napisać podstawowy program sterujący robotem. To dobry punkt startowy, jeśli chcesz zrozumieć strukturę projektu i stworzyć własne aplikacje.

## Struktura Modułów Kodu

Kod jest podzielony na moduły odpowiadające różnym komponentom robota. Każdy moduł ma swoją dokumentację:

| Nazwa Modułu              | Link do Dokumentacji                                 | Co zawiera |
| ------------------------- | -------------------------------------------------- | ---------- |
| robots                    | [build_robot](./build_robot.md)                    | Jak zbudować kompletną konfigurację robota |
| robot_devices/arm         | [add_robot_arm](./add_robot_arm.md)                | Jak dodać nowe ramię robotyczne |
| robot_devices/cameras     | [add_robot_camera](./add_robot_camera.md)          | Jak dodać nową kamerę |
| robot_devices/endeffector | [add_robot_endeffector](./add_robot_endeffector.md)| Jak dodać nowy efektor końcowy (chwytaka) |

## Proste Użycie - Podstawowy Przykład

**Uwaga:** Poniższy kod to przykład ilustrujący strukturę programu. Nie jest gotowy do bezpośredniego uruchomienia - wymaga uzupełnienia szczegółów twojego robota.

### Wyjaśnienie Architektury

Program sterujący robotem składa się z trzech głównych elementów:

1. **Policy (Polityka)**: Algorytm decyzyjny, który na podstawie obserwacji wybiera akcje do wykonania
2. **Environment (Środowisko)**: Interfejs do robota, który zbiera obserwacje i wykonuje akcje
3. **Control Loop (Pętla Sterowania)**: Główna pętla programu, która synchronizuje obserwacje, decyzje i akcje

### Kod Przykładowy z Rozszerzonymi Komentarzami

```python
import time
import math
import torch

from unitree_deploy.robot.robot_utils import make_robot
from unitree_deploy.robot_devices.robots_devices_utils import precise_wait

class YourPolicy:
    """
    Klasa implementująca politykę (strategię decyzyjną) robota.
    
    To jest miejsce, gdzie umieszczasz swój model AI lub algorytm
    decyzyjny. Model otrzymuje obserwacje (np. obraz z kamery,
    pozycje przegubów) i zwraca akcje (docelowe pozycje przegubów).
    """
    def predict_action(self, observation, policy):
        """
        Przewiduje następną akcję na podstawie bieżącej obserwacji.
        
        Args:
            observation: Słownik zawierający:
                - 'observation.images.cam_name': obraz z kamery (tensor)
                - 'observation.state': stan przegubów robota (tensor)
            policy: Referencja do obiektu polityki (dla zaawansowanych przypadków)
        
        Returns:
            action: Tablica numpy z docelowymi pozycjami przegubów
        
        Przykład implementacji:
            - Załaduj obraz i stan do modelu
            - Przeprowadź inferencję (forward pass)
            - Zwróć przewidywane akcje
        """
        # TODO: Tutaj umieść logikę przewidywania akcji
        # Przykład: return self.model.predict(observation)
        pass

class UnitreeEnv:
    """
    Klasa reprezentująca środowisko robota.
    
    Środowisko to abstrakcja robota, która ukrywa szczegóły
    komunikacji sprzętowej i udostępnia prosty interfejs:
    - get_obs(): pobierz obserwacje
    - step(action): wykonaj akcję
    """
    def __init__(self, robot_type='g1_dex1'):
        """
        Inicjalizuje środowisko robota.
        
        Args:
            robot_type: Typ robota ('g1_dex1', 'z1_realsense', 'z1_dual_dex1_realsense')
        """
        self.robot_type = robot_type
        
        # Tworzy obiekt robota na podstawie typu
        # make_robot() automatycznie ładuje odpowiednią konfigurację
        self.robot = make_robot(self.robot_type)
        
        # Sprawdza czy robot jest podłączony i łączy się jeśli nie
        if not self.robot.is_connected:
            print("Łączenie z robotem...")
            self.robot.connect()
            print("Połączono!")
            
            # Jeśli potrzebujesz rozłączyć robota później, użyj:
            # self.robot.disconnect()
    
    def get_obs(self):
        """
        Pobiera bieżące obserwacje ze wszystkich czujników robota.
        
        Returns:
            observation: Słownik zawierający:
                - 'observation.images.cam_name': obrazy z kamer
                - 'observation.state': bieżący stan przegubów
        
        Wyjaśnienie:
            Robot zbiera dane z:
            - Kamer (obrazy RGB lub RGB-D)
            - Enkoderów przegubów (pozycje, prędkości)
            - Czujników siły w chwytaku (opcjonalnie)
        """
        observation = self.robot.capture_observation()
        return observation
    
    def step(self, pred_action, t_command_target):
        """
        Wykonuje akcję na robocie.
        
        Args:
            pred_action: Tablica numpy z docelowymi pozycjami przegubów
            t_command_target: Czas (w sekundach od startu), kiedy akcja powinna być wykonana
        
        Returns:
            action: Faktycznie wykonana akcja (może się różnić od pred_action
                   ze względu na ograniczenia fizyczne robota)
        
        Wyjaśnienie:
            Robot otrzymuje docelowe pozycje i planuje trajektorię do ich osiągnięcia.
            Planowanie trajektorii zapewnia płynne ruchy bez nagłych szarpnięć.
        """
        # Oblicza czas zakończenia bieżącego cyklu sterowania
        t_cycle_end = time.monotonic() + self.control_dt
        
        # Oblicza czas docelowy dla następnej komendy
        # Jest to t_cycle_end + control_dt, co daje robotowi czas na przygotowanie
        t_command_target = t_cycle_end + self.control_dt
        
        # Wysyła akcję do robota i otrzymuje potwierdzenie
        action = self.robot.send_action(torch.from_numpy(pred_action), t_command_target)
        
        # Czeka precyzyjnie do końca cyklu (ważne dla zachowania stałej częstotliwości)
        precise_wait(t_cycle_end)
        
        return action

# ============================================================================
# GŁÓWNA PĘTLA STEROWANIA
# ============================================================================

if __name__ == "__main__":
    """
    Główny program sterujący robotem.
    
    Ten blok wykonuje się, gdy uruchamiasz skrypt bezpośrednio.
    Implementuje pętlę sterowania o stałej częstotliwości (np. 30 Hz).
    """
    
    # Krok 1: Inicjalizacja
    print("Inicjalizacja polityki i środowiska...")
    policy = YourPolicy()      # Tworzy instancję polityki (twój model AI)
    env = UnitreeEnv()         # Tworzy instancję środowiska (połączenie z robotem)
    
    # Krok 2: Konfiguracja parametrów czasowych
    t_start = time.monotonic()    # Pobiera czas startowy (monotoniczny zegar systemowy)
    iter_idx = 0                  # Indeks iteracji (licznik cykli sterowania)
    control_dt = 1 / 30           # Okres cyklu sterowania (30 Hz = 33.33 ms na cykl)
    
    print(f"Uruchamianie pętli sterowania z częstotliwością {1/control_dt:.1f} Hz")
    print("Naciśnij Ctrl+C aby zakończyć...")
    
    # Krok 3: Główna pętla sterowania
    try:
        while True:
            # --- FAZA 1: OBLICZANIE CZASÓW ---
            # Oblicza kiedy bieżący cykl powinien się zakończyć
            t_cycle_end = t_start + (iter_idx + 1) * control_dt
            
            # Oblicza czas docelowy dla komendy robota
            # Robot dostaje zadanie z wyprzedzeniem (1 cykl do przodu)
            t_command_target = t_cycle_end + control_dt
            
            # --- FAZA 2: PERCEPCJA ---
            # Pobiera obserwacje ze wszystkich czujników robota
            observation = env.get_obs()
            
            # --- FAZA 3: DECYZJA ---
            # Polityka analizuje obserwacje i przewiduje najlepszą akcję
            pred_action = policy.predict_action(observation, policy)
            
            # --- FAZA 4: AKCJA ---
            # Wykonuje przewidzianą akcję na robocie
            env.step(pred_action, t_command_target)
            
            # --- FAZA 5: SYNCHRONIZACJA ---
            # Czeka precyzyjnie do końca cyklu, aby zachować stałą częstotliwość
            # To jest kluczowe dla stabilnego sterowania robotem
            precise_wait(t_cycle_end)
            
            # Inkrementuje licznik iteracji
            iter_idx += 1
            
            # Opcjonalnie: Wyświetl status co 30 iteracji (raz na sekundę przy 30 Hz)
            if iter_idx % 30 == 0:
                print(f"Iteracja {iter_idx}, czas {time.monotonic() - t_start:.2f}s")
                
    except KeyboardInterrupt:
        # Obsługa przerwania przez użytkownika (Ctrl+C)
        print("\nZakończono przez użytkownika")
        
    finally:
        # --- FAZA 6: SPRZĄTANIE ---
        # Ten blok wykona się zawsze, nawet jeśli wystąpił błąd
        print("Wykonywanie operacji czyszczących...")
        
        # Tutaj możesz dodać kod czyszczący, np.:
        # - Zatrzymaj robot w bezpiecznej pozycji
        # - Rozłącz połączenia
        # - Zapisz logi
        # env.robot.disconnect()
        
        print("Program zakończony")
```

## Kluczowe Koncepcje

### 1. Częstotliwość Sterowania (Control Frequency)

**Czym jest:** Określa jak często robot otrzymuje nowe komendy (np. 30 Hz = 30 razy na sekundę).

**Dlaczego ważne:**
- Za niska: Robot reaguje powoli, ruchy są nieregularne
- Za wysoka: Sieć i CPU mogą nie nadążyć, komendy mogą być pomijane
- Typowe wartości: 10-50 Hz w zależności od zadania

### 2. Precyzyjne Czekanie (Precise Wait)

**Czym jest:** Funkcja `precise_wait()` zapewnia, że każdy cykl sterowania trwa dokładnie tyle samo czasu.

**Dlaczego ważne:**
- Stabilne sterowanie wymaga regularnych interwałów czasowych
- Zwykły `time.sleep()` nie jest wystarczająco precyzyjny
- `precise_wait()` aktywnie czeka, sprawdzając zegar w pętli

### 3. Czas Docelowy (Target Time)

**Czym jest:** `t_command_target` to czas w przyszłości, kiedy robot powinien osiągnąć docelową pozycję.

**Dlaczego ważne:**
- Daje robotowi czas na zaplanowanie trajektorii
- Pozwala na płynne, ciągłe ruchy
- Zapobiega opóźnieniom komunikacyjnym

## Najczęstsze Pułapki dla Początkujących

### Pułapka 1: Brak obsługi błędów

❌ **Źle:**
```python
while True:
    observation = env.get_obs()  # Co jeśli połączenie się urwie?
    action = policy.predict(observation)
    env.step(action)
```

✅ **Dobrze:**
```python
try:
    while True:
        observation = env.get_obs()
        action = policy.predict(observation)
        env.step(action)
except ConnectionError:
    print("Utracono połączenie z robotem!")
    env.robot.reconnect()
```

### Pułapka 2: Zapominanie o rozłączeniu robota

❌ **Źle:**
```python
robot = make_robot('g1_dex1')
robot.connect()
# ... kod sterowania ...
# Program kończy się bez robot.disconnect()
```

✅ **Dobrze:**
```python
robot = make_robot('g1_dex1')
try:
    robot.connect()
    # ... kod sterowania ...
finally:
    robot.disconnect()  # Zawsze się wykona
```

### Pułapka 3: Nieprawidłowe zarządzanie czasem

❌ **Źle:**
```python
while True:
    start = time.time()
    # ... sterowanie ...
    time.sleep(0.033)  # Nie uwzględnia czasu wykonania kodu!
```

✅ **Dobrze:**
```python
control_dt = 1/30
t_start = time.monotonic()
iter_idx = 0
while True:
    t_cycle_end = t_start + (iter_idx + 1) * control_dt
    # ... sterowanie ...
    precise_wait(t_cycle_end)  # Czeka do dokładnego czasu końca cyklu
    iter_idx += 1
```

## Następne Kroki

Po zrozumieniu tego przykładu, polecamy:

1. **Przeczytaj dokumentację modułów** w tabeli na górze tego pliku
2. **Uruchom przykłady testowe** z `unitree_deploy/test/`
3. **Zmodyfikuj przykładowy kod** aby dodać własną logikę
4. **Zaimplementuj własną politykę** używając modelu z treningu

## Przydatne Wskazówki

- **Zawsze testuj w symulatorze** przed uruchomieniem na prawdziwym robocie
- **Zapisuj logi** wszystkich akcji i obserwacji do debugowania
- **Dodaj limity bezpieczeństwa** (maksymalne prędkości, zakresy ruchu)
- **Monitoruj wydajność** (użycie CPU, opóźnienia sieciowe)
- **Twórz checkpointy** regularnie podczas długich eksperymentów

## Pomocy! Coś nie działa!

Jeśli napotkasz problemy:

1. Sprawdź logi robota: `journalctl -u robot_service`
2. Sprawdź połączenie sieciowe: `ping <IP_robota>`
3. Uruchom testy diagnostyczne: `python test/test_robot.py`
4. Przeczytaj sekcję "Rozwiązywanie Problemów" w głównym README
5. Zadaj pytanie na forum Unitree lub w Issues na GitHubie
