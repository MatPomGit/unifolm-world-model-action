# UnifoLM-WMA-0: Framework World-Model-Action (WMA) z Rodziny UnifoLM

<p style="font-size: 1.2em;">
    <a href="https://unigen-x.github.io/unifolm-world-model-action.github.io"><strong>Strona Projektu</strong></a> | 
    <a href="https://huggingface.co/collections/unitreerobotics/unifolm-wma-0-68ca23027310c0ca0f34959c"><strong>Modele</strong></a> |
    <a href="https://huggingface.co/unitreerobotics/datasets"><strong>Zbiory Danych</strong></a> 
  </p>
<div align="center">
  <p align="right">
    <span> 🇵🇱Polski </span> | <a href="README_en.md"> 🌎English </a> | <a href="README_cn.md"> 🇨🇳中文 </a>
  </p>
</div>

<div align="justify">
    <b>UnifoLM-WMA-0</b> to otwartoźródłowa architektura modelu świata i akcji firmy Unitree, obejmująca wiele typów robotycznych ucieleśnień (embodiments), zaprojektowana specjalnie do ogólnego uczenia robotów. Jej głównym komponentem jest model świata (world-model) zdolny do rozumienia fizycznych interakcji między robotami a ich otoczeniem. Model ten zapewnia dwie kluczowe funkcje: (a) <b>Silnik Symulacji</b> – działa jako interaktywny symulator do generowania syntetycznych danych dla uczenia robotów; (b) <b>Wzmocnienie Polityki</b> – łączy się z głową akcji i poprzez przewidywanie przyszłych procesów interakcji z modelem świata, dodatkowo optymalizuje wydajność podejmowania decyzji przez robota.
</div>

## 💡 Co to jest Model Świata (World Model)?
**Dla początkujących:** Model świata to rodzaj sztucznej inteligencji, która "rozumie" jak działa otoczenie robota. Podobnie jak człowiek potrafi przewidzieć, że jeśli pchnie kubek, to ten się przewróci, model świata pozwala robotowi przewidywać skutki swoich działań przed ich wykonaniem. To pozwala robotowi planować lepsze ruchy i uczyć się z doświadczeń.

## 🦾 Demonstracje na Rzeczywistych Robotach
| <img src="assets/gifs/real_z1_stackbox.gif" style="border:none;box-shadow:none;margin:0;padding:0;" /> | <img src="assets/gifs/real_dual_stackbox.gif" style="border:none;box-shadow:none;margin:0;padding:0;" /> |
|:---:|:---:|
| <img src="assets/gifs/real_cleanup_pencils.gif" style="border:none;box-shadow:none;margin:0;padding:0;" /> | <img src="assets/gifs/real_g1_pack_camera.gif" style="border:none;box-shadow:none;margin:0;padding:0;" /> |

**Uwaga:** Okno w prawym górnym rogu pokazuje przewidywanie modelu świata dotyczące przyszłych akcji robota w formie wideo.

## 🔥 Aktualności

* 22 września 2025: 🚀 Udostępniliśmy kod wdrożeniowy do wspomagania eksperymentów z robotami [Unitree](https://www.unitree.com/).
* 15 września 2025: 🚀 Udostępniliśmy kod treningowy i inferencyjny wraz z wagami modelu [**UnifoLM-WMA-0**](https://huggingface.co/collections/unitreerobotics/unifolm-wma-0-68ca23027310c0ca0f34959c).

## 📑 Plan Otwartych Źródeł
- [x] Trening 
- [x] Inferencja (Wnioskowanie)
- [x] Punkty kontrolne (Checkpoints)
- [x] Wdrożenie (Deployment)

## ⚙️ Instalacja

**Wyjaśnienie dla początkujących:** Ta sekcja przeprowadzi Cię przez instalację wszystkich potrzebnych narzędzi i bibliotek. Conda to menedżer środowisk, który pozwala zarządzać różnymi wersjami Pythona i pakietów bez konfliktów.

### Krok 1: Tworzenie środowiska Conda
Najpierw utworzymy izolowane środowisko Python z konkretną wersją:

```bash
# Tworzy nowe środowisko o nazwie "unifolm-wma" z Pythonem 3.10.18
conda create -n unifolm-wma python==3.10.18

# Aktywuje utworzone środowisko (wszystkie kolejne instalacje będą w tym środowisku)
conda activate unifolm-wma
```

### Krok 2: Instalacja zależności systemowych
Teraz zainstalujemy wymagane biblioteki systemowe:

```bash
# Pinocchio - biblioteka do obliczeń kinematyki i dynamiki robotów
# Używana do obliczania pozycji i ruchów ramion robota
conda install pinocchio=3.2.0 -c conda-forge -y

# FFmpeg - narzędzie do przetwarzania wideo
# Potrzebne do zapisywania i odczytywania filmów z demonstracji robota
conda install ffmpeg=7.1.1 -c conda-forge
```

### Krok 3: Pobieranie repozytorium
Sklonuj repozytorium wraz z wszystkimi podmodułami (zewnętrznymi bibliotekami):

```bash
# --recurse-submodules zapewnia pobranie również zależnych repozytoriów
git clone --recurse-submodules https://github.com/unitreerobotics/unifolm-world-model-action.git
```

**Jeśli już pobrałeś repozytorium wcześniej bez podmodułów:**
```bash
cd unifolm-world-model-action
# Ta komenda pobiera wszystkie brakujące podmoduły
git submodule update --init --recursive
```

### Krok 4: Instalacja pakietu głównego
Zainstaluj główny pakiet projektu w trybie edytowalnym (pozwala na modyfikacje bez reinstalacji):

```bash
# -e oznacza tryb "editable" - zmiany w kodzie są od razu widoczne
pip install -e .
```

### Krok 5: Instalacja zewnętrznych zależności
Na koniec zainstaluj pakiet dlimp (zewnętrzną zależność):

```bash
cd external/dlimp
pip install -e .
```

**Gotowe!** Twoje środowisko jest teraz skonfigurowane i gotowe do pracy.

## 📋 Konfiguracja Projektu

Przed rozpoczęciem treningu lub inferencji, musisz skonfigurować ścieżki do modeli i danych. Zobacz szczegółowy przewodnik:

📖 **[KONFIGURACJA.md](KONFIGURACJA.md)** - Kompletny przewodnik konfiguracji po polsku
📖 **[CONFIGURATION.md](CONFIGURATION.md)** - Complete configuration guide in English

Przewodniki zawierają:
- Wymagane zmiany w plikach konfiguracyjnych
- Zalecaną strukturę katalogów
- Przykłady konfiguracji
- Weryfikację poprawności ustawień

## 🧰 Punkty Kontrolne Modelu (Model Checkpoints)

**Wyjaśnienie:** Punkty kontrolne to zapisane wagi modelu po treningu. Możesz je wykorzystać bez konieczności trenowania modelu od zera, co oszczędza czas i zasoby obliczeniowe.

| Model | Opis | Link|
|---------|-------|------|
|$\text{UnifoLM-WMA-0}_{Base}$| Dostrojony na zbiorze danych [Open-X](https://robotics-transformer-x.github.io/). Dobry punkt startowy do ogólnych zadań robotycznych. | [HuggingFace](https://huggingface.co/unitreerobotics/UnifoLM-WMA-0-Base)|
|$\text{UnifoLM-WMA-0}_{Dual}$| Dostrojony na pięciu [zbiorach danych Unitree](https://huggingface.co/collections/unitreerobotics/g1-dex1-datasets-68bae98bf0a26d617f9983ab) w trybie podejmowania decyzji i symulacji. Zoptymalizowany dla robotów Unitree. | [HuggingFace](https://huggingface.co/unitreerobotics/UnifoLM-WMA-0-Dual)|

## 🛢️ Zbiory Danych (Datasets)

**Wyjaśnienie:** Zbiory danych zawierają nagrania demonstracji robota wykonującego różne zadania. Model uczy się na tych przykładach, jak należy wykonywać poszczególne akcje.

W naszych eksperymentach wykorzystujemy następujące otwarte zbiory danych:

| Zbiór Danych | Robot | Zadanie | Link |
|---------|-------|---------|------|
|Z1_StackBox| [Unitree Z1](https://www.unitree.com/z1)| Układanie pudełek | [Huggingface](https://huggingface.co/datasets/unitreerobotics/Z1_StackBox_Dataset/tree/v2.1)|
|Z1_DualArm_StackBox|[Unitree Z1](https://www.unitree.com/z1)| Układanie pudełek dwoma ramionami | [Huggingface](https://huggingface.co/datasets/unitreerobotics/Z1_Dual_Dex1_StackBox_Dataset/tree/v2.1)|
|Z1_DualArm_StackBox_V2|[Unitree Z1](https://www.unitree.com/z1)| Układanie pudełek v2 | [Huggingface](https://huggingface.co/datasets/unitreerobotics/Z1_Dual_Dex1_StackBox_Dataset_V2/tree/v2.1)|
|Z1_DualArm_Cleanup_Pencils|[Unitree Z1](https://www.unitree.com/z1)| Sprzątanie ołówków | [Huggingface](https://huggingface.co/datasets/unitreerobotics/Z1_Dual_Dex1_CleanupPencils_Dataset/tree/v2.1)|
|G1_Pack_Camera|[Unitree G1](https://www.unitree.com/g1)| Pakowanie kamery do pudełka | [Huggingface](https://huggingface.co/datasets/unitreerobotics/G1_Dex1_MountCameraRedGripper_Dataset/tree/v2.1)|

### Przygotowanie własnego zbioru danych

Jeśli chcesz wytrenować model na swoich własnych danych, wykonaj następujące kroki:

**Krok 1:** Upewnij się, że Twoje dane są w formacie [Huggingface LeRobot V2.1](https://github.com/huggingface/lerobot). Struktura źródłowa powinna wyglądać tak:

```
source_dir/
    ├── dataset1_name    # Pierwszy zbiór danych
    ├── dataset2_name    # Drugi zbiór danych
    ├── dataset3_name    # Trzeci zbiór danych
    └── ...
```

**Krok 2:** Przekonwertuj zbiór danych do wymaganego formatu używając poniższej komendy:

```bash
cd prepare_data
python prepare_training_data.py \
    --source_dir /ścieżka/do/source_dir \
    --target_dir /ścieżka/gdzie/zapisać/przekonwertowane/dane \
    --dataset_name "dataset1_name" \
    --robot_name "tag robota w zbiorze danych"  # np. "Unitree Z1 Robot Arm" lub "Unitree G1 Robot with Gripper"
```

**Wyjaśnienie parametrów:**
- `--source_dir`: ścieżka do katalogu z oryginalnymi danymi
- `--target_dir`: ścieżka gdzie zapisać przetworzone dane
- `--dataset_name`: nazwa konkretnego zbioru danych do konwersji
- `--robot_name`: opisowa nazwa robota (używana w metadanych)

**Krok 3:** Po konwersji, struktura danych będzie wyglądać następująco:

```
target_dir/
    ├── videos                      # Filmy z demonstracji
    │     ├──dataset1_name
    │     │   ├──camera_view_dir    # Widok z konkretnej kamery
    │     │       ├── 0.mp4         # Film z pierwszej demonstracji
    │     │       ├── 1.mp4         # Film z drugiej demonstracji
    │     │       └── ...
    │     └── ...
    ├── transitions                 # Dane o stanach i akcjach robota
    │    ├── dataset1_name
    │        ├── meta_data          # Metadane (normalizacja, statystyki)
    │        ├── 0.h5               # Dane z pierwszej demonstracji
    │        ├── 1.h5               # Dane z drugiej demonstracji
    │        └── ...
    └──  dataset1_name.csv          # Indeks wszystkich demonstracji
```

**Ważna uwaga:** Trening modelu obsługuje tylko dane z jednej głównej kamery. Jeśli Twój zbiór danych zawiera wiele widoków kamer, usuń odpowiednie wartości z kolumny `data_dir` w pliku CSV.

## 🚴‍♂️ Trening Modelu

**Wyjaśnienie:** Ta sekcja opisuje jak trenować własny model. Proces treningu uczy model przewidywać ruchy robota na podstawie obrazów z kamery i instrukcji.

### A. Strategia Treningu

Nasz proces treningu składa się z trzech etapów:

- **Krok 1: Pretrening modelu świata**
  
  Najpierw dostrajamy model generowania wideo jako model świata, używając dużego zbioru danych [Open-X](https://robotics-transformer-x.github.io/). W tym etapie model uczy się podstawowych zasad fizyki i interakcji z obiektami.

- **Krok 2: Trening w trybie podejmowania decyzji**
  
  Następnie trenujemy $\text{UnifoLM-WMA}$ w trybie podejmowania decyzji na zbiorze danych specyficznym dla zadania. Model uczy się jakie akcje wykonać, aby osiągnąć cel.
  
  <div align="left">
      <img src="assets/pngs/dm_mode.png" width="600">
  </div>

- **Krok 3: Trening w trybie symulacji**
  
  Na koniec trenujemy $\text{UnifoLM-WMA}$ w trybie symulacji na tym samym zbiorze danych. Model uczy się przewidywać efekty swoich akcji.
  
  <div align="left">
      <img src="assets/pngs/sim_mode.png" width="600">
  </div>

**Uwaga:** Jeśli potrzebujesz tylko jednego trybu działania $\text{UnifoLM-WMA}$, możesz pominąć odpowiedni krok.

### B. Przeprowadzanie Treningu

Aby przeprowadzić trening na jednym lub wielu zbiorach danych, wykonaj poniższe kroki:

**Krok 1: Konfiguracja wymiarów**

Domyślnie zakładamy maksymalnie 16 stopni swobody (DoF - Degrees of Freedom). Stopnie swobody to liczba niezależnych przegubów/osi ruchu robota.

Jeśli Twój robot ma więcej niż 16 DoF, zaktualizuj parametry `agent_state_dim` i `agent_action_dim` w pliku [configs/train/config.yaml](https://github.com/unitreerobotics/unifolm-wma/blob/working/configs/train/config.yaml).

**Krok 2: Konfiguracja kształtów danych wejściowych**

Ustaw rozmiary wejściowe dla każdej modalności (obraz, stan robota, akcja) w pliku [configs/train/meta.json](https://github.com/unitreerobotics/unitree-world-model/blob/main/configs/train/meta.json).

**Krok 3: Konfiguracja parametrów treningu**

Skonfiguruj parametry treningu w [configs/train/config.yaml](https://github.com/unitreerobotics/unitree-world-model/blob/main/configs/train/config.yaml):

```yaml
model:
    # Ścieżka do pretrenowanego modelu (zalecamy użycie UnifoLM-WMA-0_Base)
    pretrained_checkpoint: /path/to/pretrained/checkpoint
    ...
    # Czy trenować tylko w trybie podejmowania decyzji
    # True = tylko podejmowanie decyzji
    # False = jednocześnie podejmowanie decyzji i symulacja
    decision_making_only: True
    ...
data:
    ...
    train:
        ...
        # Ścieżka do katalogu z danymi treningowymi
        data_dir: /path/to/training/dataset/directory
    # Lista zbiorów danych i ich wagi (suma wag musi wynosić 1.0)
    # Wagi określają jak często dany zbiór danych jest używany w treningu
    dataset_and_weights:
        dataset1_name: 0.2  # 20% danych treningowych
        dataset2_name: 0.2  # 20% danych treningowych
        dataset3_name: 0.2  # 20% danych treningowych
        dataset4_name: 0.2  # 20% danych treningowych
        dataset5_name: 0.2  # 20% danych treningowych
```

**Krok 4: Konfiguracja skryptu treningu**

Ustaw zmienne `experiment_name` (nazwa eksperymentu) i `save_root` (katalog gdzie zapisać model) w [scripts/train.sh](https://github.com/unitreerobotics/unitree-world-model/blob/main/scripts/train.sh).

**Krok 5: Uruchomienie treningu**

Rozpocznij trening wykonując komendę:

```bash
bash scripts/train.sh
```

**Co się dzieje podczas treningu:**
- Model przetwarza kolejne partie danych (batches)
- Oblicza błędy przewidywań (loss)
- Aktualizuje wagi sieci neuronowej, aby poprawić przewidywania
- Regularnie zapisuje punkty kontrolne (checkpoints)
- Może to potrwać od kilku godzin do kilku dni, w zależności od rozmiaru danych i sprzętu

## 🌏 Inferencja w Interaktywnym Trybie Symulacji

**Wyjaśnienie:** Inferencja to proces używania wytrenowanego modelu do generowania przewidywań. W trybie interaktywnej symulacji, model przewiduje przyszłe stany środowiska na podstawie obecnego stanu i planowanych akcji.

Aby uruchomić model świata w interaktywnym trybie symulacji, wykonaj następujące kroki:

**Krok 1: Przygotowanie promptów (opcjonalnie)**

Jeśli chcesz przetestować model na własnych danych, pomiń ten krok i użyj dostarczonych przykładów. W przeciwnym razie przygotuj własne prompty zgodnie z formatem w [examples/world_model_interaction_prompts](https://github.com/unitreerobotics/unitree-world-model/tree/main/examples/world_model_interaction_prompts):

```
world_model_interaction_prompts/
  ├── images                          # Obrazy jako punkty startowe
  │    ├── dataset1_name
  │    │       ├── 0.png              # Obraz promptu (obecny stan sceny)
  │    │       └── ...
  │    └── ...
  ├── transitions                     # Dane o stanach robota
  │    ├── dataset1_name
  │    │       ├── meta_data          # Używane do normalizacji
  │    │       ├── 0.h5               # Stan robota odpowiadający obrazowi
  │    │       │                      # (w trybie interakcji używany tylko do 
  │    │       │                      #  pobrania stanu robota)
  │    │       └── ...
  │    └── ...
  ├──  dataset1_name.csv              # Plik indeksujący obrazy, instrukcje 
  │                                   # tekstowe i odpowiadające stany robota
  └── ...
```

**Krok 2: Konfiguracja ścieżek**

Określ poprawne ścieżki dla `pretrained_checkpoint` (np. $\text{UnifoLM-WMA-0}_{Dual}$) i `data_dir` w [configs/inference/world_model_interaction.yaml](https://github.com/unitreerobotics/unitree-world-model/blob/main/configs/inference/world_model_interaction.yaml).

**Krok 3: Uruchomienie inferencji**

Ustaw ścieżki dla `checkpoint`, `res_dir` (katalog wyników) i `prompt_dir` (katalog z promptami) w [scripts/run_world_model_interaction.sh](https://github.com/unitreerobotics/unitree-world-model/blob/main/scripts/run_world_model_interaction.sh). 

Określ wszystkie nazwy zbiorów danych w `datasets=(...)`, a następnie uruchom inferencję komendą:

```bash
bash scripts/run_world_model_interaction.sh
```

**Co się dzieje:**
- Model wczytuje obraz początkowy i instrukcję
- Generuje sekwencję przyszłych obrazów pokazującą jak robot wykona zadanie
- Wyniki (wygenerowane wideo) są zapisywane w katalogu `res_dir`

## 🧠 Inferencja i Wdrożenie w Trybie Podejmowania Decyzji

**Wyjaśnienie:** W tym trybie uruchamiamy model na rzeczywistym robocie. Model działa na serwerze (mocny komputer z GPU), a robot (klient) wysyła obserwacje i otrzymuje akcje do wykonania. To architektura klient-serwer, która pozwala na wykorzystanie mocy obliczeniowej serwera do sterowania robotem w czasie rzeczywistym.

### Konfiguracja Serwera

Serwer to komputer, który uruchamia model i oblicza jakie akcje robot powinien wykonać.

**Krok 1: Konfiguracja parametrów serwera**

Określ zmienne `ckpt` (ścieżka do modelu), `res_dir` (katalog wyników), `datasets` (lista zbiorów danych) w [scripts/run_real_eval_server.sh](https://github.com/unitreerobotics/unifolm-world-model-action/blob/main/scripts/run_real_eval_server.sh).

**Krok 2: Konfiguracja danych**

Skonfiguruj `data_dir` (katalog danych) i `dataset_and_weights` (wagi zbiorów) w [config/inference/world_model_decision_making.yaml](https://github.com/unitreerobotics/unifolm-world-model-action/blob/f12b4782652ca00452941d851b17446e4ee7124a/configs/inference/world_model_decision_making.yaml#L225).

**Krok 3: Uruchomienie serwera**

Uruchom serwer używając następujących komend:

```bash
# Aktywuj środowisko conda
conda activate unifolm-wma

# Przejdź do katalogu projektu
cd unifolm-world-model-action

# Uruchom serwer (będzie nasłuchiwał na połączenia od klienta)
bash scripts/run_real_eval_server.sh
```

Serwer jest teraz uruchomiony i czeka na połączenie od klienta robota.

### Konfiguracja Klienta (Robot)

Klient to robot, który będzie wykonywał akcje przewidziane przez model na serwerze.

**Krok 1: Przygotowanie środowiska robota**

Postępuj zgodnie z instrukcjami w [unitree_deploy/README.md](https://github.com/unitreerobotics/unifolm-world-model-action/blob/main/unitree_deploy/README.md), aby:
- Utworzyć środowisko conda `unitree_deploy`
- Zainstalować wymagane pakiety
- Uruchomić kontrolery lub usługi na rzeczywistym robocie

**Krok 2: Ustanowienie tunelu SSH**

Otwórz nowy terminal i ustanów tunel SSH od klienta do serwera. To pozwala robotowi bezpiecznie komunikować się z serwerem:

```bash
# Zastąp user_name i remote_server_IP swoimi danymi
ssh user_name@remote_server_IP -CNg -L 8000:127.0.0.1:8000
```

**Wyjaśnienie tunelu:**
- `-C`: kompresja danych (szybsza transmisja)
- `-N`: nie wykonuj żadnych komend zdalnych
- `-g`: pozwól na połączenia zdalne
- `-L 8000:127.0.0.1:8000`: przekieruj port lokalny 8000 na port 8000 serwera

**Krok 3: Uruchomienie klienta robota**

W osobnym terminalu uruchom skrypt klienta robota:

```bash
cd unitree_deploy
python scripts/robot_client.py \
    --robot_type "g1_dex1" \              # Typ robota
    --action_horizon 16 \                 # Ile akcji przewidywać do przodu
    --exe_steps 16 \                      # Ile kroków wykonać
    --observation_horizon 2 \             # Ile obserwacji uwzględnić
    --language_instruction "pack black camera into box" \  # Instrukcja zadania
    --output_dir ./results \              # Katalog wyników
    --control_freq 15                     # Częstotliwość sterowania (Hz)
```

**Wyjaśnienie parametrów:**
- `--robot_type`: określa jakiego robota używasz (g1_dex1, z1_realsense, z1_dual_dex1_realsense)
- `--action_horizon`: ile kroków do przodu model powinien planować
- `--exe_steps`: ile kroków faktycznie wykonać (zazwyczaj równe action_horizon)
- `--observation_horizon`: ile poprzednich obserwacji uwzględnić w decyzji
- `--language_instruction`: opisuje zadanie, które robot ma wykonać
- `--control_freq`: jak często wysyłać komendy do robota (w Hz)

**Co się dzieje:**
1. Robot zbiera obserwacje (obrazy z kamery, pozycje przegubów)
2. Wysyła je do serwera przez tunel SSH
3. Serwer używa modelu do obliczenia najlepszych akcji
4. Robot otrzymuje akcje i wykonuje je
5. Proces powtarza się w pętli, aż zadanie zostanie ukończone

## 📝 Architektura Kodu

**Wyjaśnienie:** Ta sekcja opisuje organizację plików w projekcie. Zrozumienie struktury pomoże Ci znaleźć odpowiednie pliki, gdy będziesz chciał coś zmodyfikować.

Oto przegląd struktury kodu projektu i głównych komponentów:

```
unifolm-world-model-action/
    ├── assets/                         # Zasoby medialne
    │   ├── gifs/                       # Animacje demonstracyjne
    │   └── pngs/                       # Obrazy i diagramy
    │
    ├── configs/                        # Pliki konfiguracyjne
    │   ├── inference/                  # Konfiguracja dla inferencji
    │   │   ├── world_model_interaction.yaml         # Tryb symulacji
    │   │   └── world_model_decision_making.yaml     # Tryb podejmowania decyzji
    │   └── train/                      # Konfiguracja dla treningu
    │       ├── config.yaml             # Główne parametry treningu
    │       └── meta.json               # Metadane zbiorów danych
    │
    ├── examples/                       # Przykładowe dane wejściowe
    │   └── world_model_interaction_prompts/  # Przykłady do trybu interakcji
    │
    ├── external/                       # Zewnętrzne pakiety i zależności
    │   └── dlimp/                      # Biblioteka pomocnicza
    │
    ├── prepare_data/                   # Skrypty do przetwarzania danych
    │   └── prepare_training_data.py    # Konwersja danych do formatu treningowego
    │
    ├── scripts/                        # Główne skrypty projektu
    │   ├── trainer.py                  # Skrypt treningu modelu
    │   ├── train.sh                    # Skrypt bash do uruchomienia treningu
    │   ├── evaluation/                 # Skrypty ewaluacji
    │   │   ├── real_eval_server.py     # Serwer dla rzeczywistego robota
    │   │   ├── world_model_interaction.py  # Interaktywna symulacja
    │   │   └── eval_utils.py           # Funkcje pomocnicze
    │   ├── run_real_eval_server.sh     # Uruchamia serwer ewaluacji
    │   └── run_world_model_interaction.sh  # Uruchamia tryb interakcji
    │
    ├── src/                            # Kod źródłowy głównego pakietu
    │   └── unifolm_wma/                # Pakiet Python modelu świata
    │       ├── data/                   # Ładowanie i przetwarzanie danych
    │       │   ├── dataloader.py       # Klasy do ładowania danych
    │       │   └── transforms.py       # Transformacje danych
    │       ├── models/                 # Architektury modeli
    │       │   ├── world_model.py      # Model świata
    │       │   └── action_head.py      # Głowa akcji (policy)
    │       ├── modules/                # Niestandardowe moduły
    │       │   ├── attention.py        # Mechanizmy uwagi
    │       │   └── encoders.py         # Enkodery obrazów i stanów
    │       └── utils/                  # Funkcje pomocnicze
    │           ├── visualization.py    # Wizualizacja wyników
    │           └── training_utils.py   # Narzędzia do treningu
    │
    └── unitree_deploy/                 # Kod wdrożeniowy dla robotów Unitree
        ├── README.md                   # Dokumentacja wdrożenia
        ├── docs/                       # Szczegółowa dokumentacja
        │   ├── GettingStarted.md       # Przewodnik startowy
        │   ├── build_robot.md          # Jak zbudować konfigurację robota
        │   ├── add_robot_arm.md        # Dodawanie nowych ramion
        │   ├── add_robot_camera.md     # Dodawanie kamer
        │   └── add_robot_endeffector.md # Dodawanie chwytaków
        ├── scripts/                    # Skrypty wdrożeniowe
        │   └── robot_client.py         # Klient robota (sterowanie)
        └── unitree_deploy/             # Główny pakiet wdrożeniowy
            ├── robot/                  # Klasy robotów
            │   ├── robot.py            # Główna klasa robota
            │   ├── robot_configs.py    # Konfiguracje robotów
            │   └── robot_utils.py      # Funkcje pomocnicze
            ├── robot_devices/          # Komponenty robota
            │   ├── arm/                # Ramiona robotów
            │   │   ├── z1_arm.py       # Ramię Z1
            │   │   ├── g1_arm.py       # Ramię G1
            │   │   └── configs.py      # Konfiguracje ramion
            │   ├── cameras/            # Kamery
            │   │   └── realsense.py    # Kamera RealSense
            │   └── endeffector/        # Efektory końcowe (chwytaki)
            │       └── dex1.py         # Chwytka Dex1
            ├── utils/                  # Narzędzia pomocnicze
            │   ├── trajectory_generator.py  # Generowanie trajektorii
            │   ├── eval_utils.py       # Ewaluacja na robocie
            │   └── visualizer.py       # Wizualizacja danych robota
            └── real_unitree_env.py     # Środowisko rzeczywistego robota
```

**Najważniejsze pliki dla początkujących:**
- `README.md` (ten plik) - dokumentacja projektu
- `configs/` - tu zmieniasz parametry treningu i inferencji
- `unitree_deploy/scripts/robot_client.py` - tu steruj robotem
- `scripts/train.sh` - tu uruchamiasz trening

## 🙏 Podziękowania

Duża część kodu pochodzi z następujących projektów open-source:
- [DynamiCrafter](https://github.com/Doubiiu/DynamiCrafter) - generowanie wideo
- [Diffusion Policy](https://github.com/real-stanford/diffusion_policy) - polityki dyfuzyjne
- [ACT](https://github.com/MarkFzp/act-plus-plus) - Action Chunking Transformer
- [HPT](https://github.com/liruiw/HPT) - Heterogeneous Pre-trained Transformers

Dziękujemy autorom za udostępnienie swojego kodu!

## 📝 Cytowanie

Jeśli używasz tego projektu w swojej pracy naukowej, prosimy o cytowanie:

```
@misc{unifolm-wma-0,
  author       = {Unitree},
  title        = {UnifoLM-WMA-0: A World-Model-Action (WMA) Framework under UnifoLM Family},
  year         = {2025},
}
```

## 🧪 Testowanie

Projekt zawiera testy jednostkowe do weryfikacji poprawności instalacji i konfiguracji.

### Uruchomienie testów

```bash
# Zainstaluj zależności testowe
pip install -e ".[test]"

# Uruchom wszystkie testy
pytest

# Uruchom testy z raportem pokrycia kodu
pytest --cov=unifolm_wma --cov-report=html
```

Więcej informacji o testach znajduje się w [tests/README.md](tests/README.md).

## 📚 Dodatkowe Zasoby dla Początkujących

**Gdzie szukać pomocy:**
- [Dokumentacja Unitree Deploy](unitree_deploy/README.md) - szczegóły wdrożenia
- [Dokumentacja wideo LeRobot](https://github.com/huggingface/lerobot) - format danych
- [Forum Unitree](https://www.unitree.com/) - wsparcie społeczności

**Podstawowe pojęcia:**
- **DoF (Degrees of Freedom)**: Liczba niezależnych ruchów, które robot może wykonać
- **Checkpoint**: Zapisany stan modelu po treningu
- **Inference**: Używanie wytrenowanego modelu do przewidywań
- **Policy**: Strategia decyzyjna robota (co robić w danej sytuacji)
- **World Model**: Model przewidujący jak zmieni się świat po akcjach robota
