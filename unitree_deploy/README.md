# Unitree Deploy - Wdrożenie na Robotach Unitree

<div align="center">
  <p align="right">
    <span> 🇵🇱Polski </span> | <a href="README_en_backup.md"> 🌎English </a> | <a href="./docs/README_cn.md"> 🇨🇳中文 </a>
  </p>
</div>

Ten dokument zawiera instrukcje konfiguracji środowiska wdrożeniowego dla platform Unitree G1 (z chwytakiem) i Z1, w tym instalację zależności, uruchomienie usługi obrazu oraz sterowanie chwytakiem.

## 0. 📖 Wprowadzenie

**Dla początkujących:** Ten moduł służy do wdrażania wytrenowanych modeli na rzeczywistych robotach firmy Unitree. Pozwala na połączenie modelu AI z fizycznym robotem, aby mógł wykonywać zadania w prawdziwym świecie.

To repozytorium jest używane do wdrażania modeli na robotach Unitree. Zawiera wszystkie narzędzia potrzebne do:
- Komunikacji z robotem przez sieć
- Zbierania danych z kamer i czujników
- Wysyłania komend ruchu do ramion i chwytaków
- Wizualizacji i logowania działania robota

---

## 1. 🛠️ Konfiguracja Środowiska

**Wyjaśnienie:** Tworzymy osobne środowisko dla wdrożenia, oddzielone od środowiska treningowego. To pozwala uniknąć konfliktów między wersjami bibliotek.

### Krok 1: Tworzenie środowiska conda

```bash
# Utwórz nowe środowisko o nazwie "unitree_deploy" z Pythonem 3.10
conda create -n unitree_deploy python=3.10

# Aktywuj nowo utworzone środowisko
conda activate unitree_deploy
```

### Krok 2: Instalacja zależności

```bash
# Pinocchio - biblioteka do obliczeń kinematycznych (pozycje i ruchy robota)
conda install pinocchio -c conda-forge

# Zainstaluj główny pakiet w trybie edytowalnym
# Flaga -e pozwala na edycję kodu bez konieczności reinstalacji
pip install -e .

# (Opcjonalnie) Zainstaluj zależności LeRobot, jeśli chcesz pracować z danymi w tym formacie
pip install -e ".[lerobot]"
```

### Krok 3: Instalacja SDK Unitree

SDK (Software Development Kit) to zestaw narzędzi do komunikacji z robotami Unitree.

```bash
# Sklonuj oficjalne SDK Python dla robotów Unitree
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git

# Zainstaluj SDK
cd unitree_sdk2_python && pip install -e . && cd ..
```

**Gotowe!** Środowisko jest skonfigurowane. Teraz możesz przejść do konfiguracji konkretnego robota.

---

## 2. 🚀 Uruchamianie Robotów

**Ważna wskazówka:** Upewnij się, że wszystkie urządzenia (komputer, robot, kamery) są podłączone do tej samej sieci lokalnej (LAN). To kluczowe dla prawidłowej komunikacji.

## 2.1 🤖 Uruchamianie Robota G1 z Chwytakiem Dex_1

Robot G1 to humanoidalny robot firmy Unitree z ramionami i chwytakami Dex_1.

### 2.1.1 📷 Konfiguracja Usługi Obrazu (Płyta G1)

**Wyjaśnienie:** Usługa obrazu (image_server) to program działający na pokładowym komputerze robota, który przesyła obrazy z kamer przez sieć. To pozwala twojemu komputerowi otrzymywać obraz z kamery robota w czasie rzeczywistym.

[Aby uruchomić image_server, wykonaj następujące kroki](https://github.com/unitreerobotics/xr_teleoperate?tab=readme-ov-file#31-%EF%B8%8F-image-service):

**Krok 1:** Połącz się z płytą robota G1 przez SSH

```bash
# Połącz się z płytą G1 (domyślne hasło: 123)
ssh unitree@192.168.123.164
```

**Wyjaśnienie SSH:** SSH (Secure Shell) to protokół pozwalający na bezpieczne zdalne logowanie do komputera robota i wykonywanie na nim komend.

**Krok 2:** Uruchom serwer obrazu na robocie

```bash
# Aktywuj środowisko conda na robocie
conda activate tv

# Przejdź do katalogu z serwerem obrazu
cd ~/image_server

# Uruchom serwer obrazu
# Ten program będzie przesyłał obrazy z kamery robota do sieci
python image_server.py
```

**Co się dzieje:** Serwer zaczyna nasłuchiwać na połączenia i przesyła obraz z kamery robota do wszystkich podłączonych klientów.

---

### 2.1.2 🤏 Konfiguracja Usługi Chwytaka Dex_1 (Komputer Deweloperski)

**Wyjaśnienie:** Chwytaki Dex_1 to zaawansowane końcówki robotyczne z wieloma palcami. Wymagają osobnej usługi do sterowania, która działa na twoim komputerze deweloperskim.

Zapoznaj się z [Przewodnikiem Instalacji Chwytaka Dex_1](https://github.com/unitreerobotics/dex1_1_service?tab=readme-ov-file#1--installation) po szczegółowe instrukcje.

**Krok 1:** Przejdź do katalogu z usługą

```bash
# Katalog build zawiera skompilowane programy sterujące
cd ~/dex1_1_service/build
```

**Krok 2:** Uruchom usługę chwytaka

```bash
# Uruchom serwer chwytaka
# --network eth0: określa interfejs sieciowy (użyj ifconfig, aby sprawdzić swój)
# -l: tryb lokalny
# -r: tryb robota rzeczywistego (nie symulator)
sudo ./dex1_1_gripper_server --network eth0 -l -r
```

**Ważne:** Parametr `eth0` to nazwa twojego interfejsu sieciowego. Użyj komendy `ifconfig`, aby sprawdzić nazwę twojego interfejsu sieciowego (może to być np. `eth0`, `enp0s3`, `wlan0` itp.).

**Krok 3:** Weryfikacja komunikacji z chwytakiem

```bash
# Test sprawdzający czy chwytaka odpowiada prawidłowo
./test_dex1_1_gripper_server --network eth0 -l -r
```

**Co powinno się stać:** Test powinien pokazać, że komunikacja z chwytakiem działa. Powinieneś zobaczyć informacje o statusie chwytaka.

---

### 2.1.3 ✅ Testowanie Konfiguracji G1

**Wyjaśnienie:** Przed użyciem robota do rzeczywistych zadań, zawsze warto przeprowadzić testy, aby upewnić się, że wszystkie komponenty działają prawidłowo.

Wykonaj następujące testy, aby zapewnić prawidłowe działanie:

**Test 1: Chwytaka Dex1**

```bash
# Ten test sprawdza czy możemy sterować chwytakiem
python test/endeffector/test_dex1.py
```

Co sprawdza: Czy chwytaka otwiera się i zamyka prawidłowo, czy wszystkie palce działają.

**Test 2: Ramienia G1**

```bash
# Ten test sprawdza czy możemy sterować ramieniem robota
python test/arm/g1/test_g1_arm.py
```

Co sprawdza: Czy wszystkie przeguby ramienia poruszają się prawidłowo, czy robot reaguje na komendy.

**Test 3: Kamery (Klient Obrazu)**

```bash
# Ten test sprawdza czy możemy odbierać obraz z kamery robota
python test/camera/test_image_client_camera.py
```

Co sprawdza: Czy obraz z kamery jest odbierany, czy jakość jest dobra.

**Test 4: Odtwarzanie Zebranych Danych (Replay)**

```bash
# Ten test odtwarza wcześniej nagrane demonstracje na robocie
# --repo-id: ID repozytorium na Hugging Face Hub z danymi
# --robot_type: typ robota (g1_dex1, z1_realsense, z1_dual_dex1_realsense)

python test/test_replay.py \
    --repo-id unitreerobotics/G1_CameraPackaging_NewDataset \
    --robot_type g1_dex1
```

Co sprawdza: Czy robot potrafi odtworzyć wcześniej nagrane ruchy. To dobry test całego systemu.

---

## 2.2 🦿 Uruchamianie Robota Z1

Robot Z1 to ramię robotyczne firmy Unitree, lżejsze i bardziej mobilne niż G1.

### 2.2.1 🦿 Konfiguracja Z1

**Wyjaśnienie:** Robot Z1 wymaga specjalnego kontrolera (z1_controller) i SDK (z1_sdk) do komunikacji i sterowania.

**Krok 1:** Pobierz wymagane repozytoria

```bash
# Sklonuj kontroler Z1 (program sterujący robotem)
git clone https://github.com/unitreerobotics/z1_controller.git

# Sklonuj SDK Z1 (biblioteka do komunikacji z robotem)
git clone https://github.com/unitreerobotics/z1_sdk.git
```

**Krok 2:** Skompiluj repozytoria

```bash
# Przejdź do katalogu z kontrolerem
cd z1_controller

# Utwórz katalog build i przejdź do niego
mkdir build && cd build

# Skompiluj projekt (CMake generuje pliki budowania, make kompiluje kod)
cmake .. && make -j

# Powtórz dla SDK
cd ../../z1_sdk
mkdir build && cd build
cmake .. && make -j
```

**Wyjaśnienie kompilacji:** Kod źródłowy w C++ musi być przekonwertowany (skompilowany) na program wykonywalny. CMake to narzędzie do konfiguracji procesu kompilacji, a make wykonuje faktyczną kompilację.

**Krok 3:** Skopiuj bibliotekę interfejsu

```bash
# Skopiuj bibliotekę Pythona pozwalającą na komunikację z robotem
# UWAGA: Dostosuj ścieżki do swojej instalacji!
cp z1_sdk/lib/unitree_arm_interface.cpython-310-x86_64-linux-gnu.so \
   ./unitree_deploy/robot_devices/arm/
```

**Krok 4:** Uruchom kontroler Z1

```bash
# Przejdź do katalogu build kontrolera
# UWAGA: Dostosuj ścieżkę do swojej instalacji!
cd z1_controller/build

# Uruchom kontroler (ten program komunikuje się bezpośrednio z robotem)
./z1_ctrl
```

**Co robi kontroler:** Z1_ctrl to niskopo ziomowy program, który odbiera twoje komendy wysokiego poziomu (np. "przesuń ramię do pozycji X") i przekłada je na sygnały sterujące dla silników robota.

---

### 2.2.2 ✅ Testowanie Konfiguracji Z1

**Test 1: Kamery RealSense**

```bash
# Test kamery RealSense (popularna kamera RGB-D używana w robotyce)
# UWAGA: Zmodyfikuj numer seryjny kamery zgodnie z twoją kamerą!
python test/camera/test_realsense_camera.py
```

**Wskazówka:** Numer seryjny kamery RealSense możesz sprawdzić używając narzędzia `realsense-viewer` lub czytając naklejkę na kamerze.

**Test 2: Ramienia Z1**

```bash
# Test podstawowej komunikacji z ramieniem Z1
python test/arm/z1/test_z1_arm.py
```

**Test 3: Środowisko Z1**

```bash
# Test kompletnego środowiska robota (kamera + ramię + logika sterowania)
python test/arm/z1/test_z1_env.py
```

**Test 4: Odtwarzanie Danych Z1**

```bash
# Odtwórz demonstracje ze zbioru danych Z1
python test/test_replay.py \
    --repo-id unitreerobotics/Z1_StackBox_Dataset \
    --robot_type z1_realsense
```

---

## 2.3 🦿🦿 Uruchamianie Podwójnego Z1 (Z1_Dual)

**Wyjaśnienie:** Konfiguracja Z1_Dual to system z dwoma ramionami Z1 pracującymi jednocześnie. Jest bardziej złożony, bo wymaga koordynacji między dwoma robotami.

### 2.3.1 🦿 Konfiguracja Z1 i Dex1

**Krok 1:** Instalacja podstawowa

Pobierz i skompiluj odpowiedni kod zgodnie z powyższymi krokami dla Z1 oraz pobierz program chwytaka, aby uruchomić go lokalnie.

**Krok 2:** Konfiguracja sterowania wielomaszynowego

Skonfiguruj komunikację między wieloma robotami zgodnie z [dokumentacją Unitree](https://support.unitree.com/home/zh/Z1_developer/sdk_operation).

**Wyjaśnienie:** W konfiguracji z wieloma robotami, każdy robot potrzebuje unikalnego ID i adresu sieciowego. Dokumentacja Unitree szczegółowo opisuje jak to skonfigurować.

**Krok 3:** Instalacja zmodyfikowanego SDK

```bash
# Pobierz specjalną wersję SDK dla dwóch ramion
git clone -b z1_dual https://github.com/unitreerobotics/z1_sdk.git z1_sdk_dual

# Skompiluj SDK
cd z1_sdk_dual
mkdir build && cd build
cmake .. && make -j

# Skopiuj bibliotekę (UWAGA: dostosuj ścieżkę!)
cp z1_sdk_dual/lib/unitree_arm_interface.cpython-310-x86_64-linux-gnu.so \
   ./unitree_deploy/robot_devices/arm/
```

**Krok 4:** Uruchom oba kontrolery

```bash
# Uruchom kontroler dla pierwszego ramienia
cd z1_controller/build && ./z1_ctrl

# W osobnym terminalu uruchom kontroler dla drugiego ramienia
cd z1_controller_1/build && ./z1_ctrl
```

**Krok 5:** Uruchom usługę chwytaka

```bash
# Uruchom serwer chwytaka (sprawdź swój interfejs sieciowy przez ifconfig!)
sudo ./dex1_1_gripper_server --network eth0 -l -r
```

---

### 2.3.2 ✅ Testowanie Konfiguracji Z1_Dual

**Test 1: Podwójne Ramię Z1**

```bash
# Test sterowania dwoma ramionami jednocześnie
python test/arm/z1/test_z1_arm_dual.py
```

Co sprawdza: Czy oba ramiona reagują na komendy, czy są zsynchronizowane, czy nie kolidują ze sobą.

**Test 2: Odtwarzanie Danych Z1_Dual**

```bash
# Odtwórz demonstracje z podwójnym ramieniem
python test/test_replay.py \
    --repo-id unitreerobotics/Z1_Dual_Dex1_StackBox_Dataset_V2 \
    --robot_type z1_dual_dex1_realsense
```

---

## 3. 🧠 Inferencja i Wdrożenie

**Wyjaśnienie:** Po skonfigurowaniu robota, czas uruchomić model AI do sterowania robotem w czasie rzeczywistym.

**Krok 1:** Konfiguracja parametrów robota

[Zmodyfikuj odpowiednie parametry zgodnie z twoją konfiguracją](./unitree_deploy/robot/robot_configs.py).

W pliku `robot_configs.py` znajdziesz:
- Zakresy ruchu przegubów (limity bezpieczeństwa)
- Konfiguracje kamer (rozdzielczość, FPS)
- Parametry chwytaków (siła, prędkość)
- Adresy sieciowe urządzeń

**Krok 2:** Uruchomienie systemu

Wróć do **Kroku 2 w sekcji "Konfiguracja Klienta"** w [Inferencja i Wdrożenie w Trybie Podejmowania Decyzji](https://github.com/unitreerobotics/unifolm-world-model-action/blob/main/README.md).

---

## 4. 🏗️ Struktura Kodu

**Wyjaśnienie:** Jeśli chcesz dodać wsparcie dla własnego sprzętu (nowa kamera, nowe ramię, nowy chwytaka), ta sekcja ci pomoże.

[Jeśli chcesz dodać własne urządzenie robotyczne, możesz je zbudować zgodnie z tą dokumentacją](./docs/GettingStarted.md).

Dokumenty dla poszczególnych komponentów:
- **Dodawanie nowego robota**: [docs/build_robot.md](./docs/build_robot.md)
- **Dodawanie nowego ramienia**: [docs/add_robot_arm.md](./docs/add_robot_arm.md)
- **Dodawanie nowej kamery**: [docs/add_robot_camera.md](./docs/add_robot_camera.md)
- **Dodawanie nowego efektora końcowego**: [docs/add_robot_endeffector.md](./docs/add_robot_endeffector.md)

**Podstawowa struktura modułu:**

```
unitree_deploy/
├── robot/                  # Definicje kompletnych robotów
│   ├── robot.py           # Główna klasa robota (łączy wszystkie komponenty)
│   ├── robot_configs.py   # Konfiguracje dla różnych modeli robotów
│   └── robot_utils.py     # Funkcje pomocnicze
│
├── robot_devices/         # Poszczególne komponenty robotów
│   ├── arm/              # Implementacje ramion
│   │   ├── z1_arm.py     # Klasa dla ramienia Z1
│   │   ├── g1_arm.py     # Klasa dla ramienia G1
│   │   └── utils.py      # Funkcje pomocnicze dla ramion
│   │
│   ├── cameras/          # Implementacje kamer
│   │   ├── realsense.py  # Kamera Intel RealSense
│   │   └── utils.py      # Funkcje pomocnicze dla kamer
│   │
│   └── endeffector/      # Implementacje chwytaków
│       ├── dex1.py       # Chwytaka Dex_1
│       └── utils.py      # Funkcje pomocnicze dla chwytaków
│
├── utils/                # Narzędzia ogólne
│   ├── eval_utils.py     # Funkcje do ewaluacji
│   ├── trajectory_generator.py  # Generowanie gładkich trajektorii
│   └── visualizer.py     # Wizualizacja danych
│
└── scripts/              # Skrypty uruchomieniowe
    └── robot_client.py   # Główny klient sterujący robotem
```

**Jak dodać nowy komponent:**
1. Stwórz nową klasę dziedziczącą po odpowiednim interfejsie bazowym
2. Zaimplementuj wymagane metody (`connect`, `read`, `write`, etc.)
3. Dodaj konfigurację w `robot_configs.py`
4. Przetestuj nowy komponent osobno przed integracją

---

## 5. 🤔 Rozwiązywanie Problemów

**Najczęstsze problemy i rozwiązania:**

### Problem 1: Robot nie odpowiada

**Możliwe przyczyny:**
- Roboty nie są w tej samej sieci LAN
- Kontroler nie jest uruchomiony
- Zły adres IP lub port

**Rozwiązanie:**
1. Sprawdź połączenie sieciowe: `ping <adres_IP_robota>`
2. Upewnij się, że kontroler jest uruchomiony
3. Sprawdź konfigurację w `robot_configs.py`

### Problem 2: Kamera nie przesyła obrazu

**Możliwe przyczyny:**
- Usługa image_server nie jest uruchomiona na robocie
- Problem z siecią
- Zły numer seryjny kamery

**Rozwiązanie:**
1. SSH do robota i sprawdź czy image_server działa
2. Sprawdź logi: `journalctl -u image_server`
3. Dla RealSense, sprawdź numer seryjny: `rs-enumerate-devices`

### Problem 3: Chwytaka nie reaguje

**Możliwe przyczyny:**
- Usługa dex1_1_gripper_server nie jest uruchomiona
- Zły interfejs sieciowy
- Brak uprawnień sudo

**Rozwiązanie:**
1. Sprawdź czy usługa działa: `ps aux | grep dex1`
2. Użyj `ifconfig` do sprawdzenia interfejsu sieciowego
3. Upewnij się, że uruchamiasz z `sudo`

### Problem 4: Ruchy robota są nieregularne

**Możliwe przyczyny:**
- Za wysoka częstotliwość sterowania dla możliwości sieci
- Konflikt procesów
- Przeciążenie CPU

**Rozwiązanie:**
1. Zmniejsz `control_freq` w robot_client.py
2. Zamknij niepotrzebne procesy
3. Użyj `htop` do monitorowania użycia CPU

---

## 6. 🙏 Podziękowania

Ten kod bazuje na następujących projektach open-source. Odwiedź odpowiednie URL, aby zobaczyć licencje (Jeśli uważasz te projekty za wartościowe, byłoby wspaniale, gdybyś mógł dać im gwiazdkę):

1. **LeRobot** - [https://github.com/huggingface/lerobot](https://github.com/huggingface/lerobot)
   - Format danych, narzędzia do zbierania demonstracji
   
2. **Unitree SDK2 Python** - [https://github.com/unitreerobotics/unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python)
   - Oficjalne SDK do komunikacji z robotami Unitree

Dziękujemy wszystkim kontrybutorm tych projektów za ich ciężką pracę!

---

## 7. 📚 Dodatkowe Zasoby

**Dokumentacja Unitree:**
- [Oficjalna strona Unitree](https://www.unitree.com/)
- [Forum wsparcia technicznego](https://support.unitree.com/)
- [Kanał YouTube z tutorialami](https://www.youtube.com/@UnitreeRobotics)

**Przydatne tutoriale dla początkujących:**
- Podstawy kinematyki robotów
- Wprowadzenie do ROS (Robot Operating System)
- Programowanie robotów w Pythonie
- Wizja komputerowa dla robotyki

**Zalecane narzędzia:**
- **RViz**: Wizualizacja robotów 3D
- **rqt**: Narzędzia do debugowania ROS
- **realsense-viewer**: Podgląd kamer RealSense
- **Wireshark**: Analiza ruchu sieciowego (dla zaawansowanych)
