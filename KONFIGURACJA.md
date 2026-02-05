# Konfiguracja dla Początkujących

Ten przewodnik pomoże Ci skonfigurować projekt przed pierwszym użyciem.

## Wymagane Konfiguracje

### 1. Konfiguracja Treningu

Przed rozpoczęciem treningu musisz zaktualizować następujące pliki:

#### `configs/train/config.yaml`

Otwórz plik i zaktualizuj następujące ścieżki:

```yaml
model:
    # Zmień na rzeczywistą ścieżkę do pretrenowanego modelu
    pretrained_checkpoint: /path/to/pretrained/checkpoint
    # Przykład:
    # pretrained_checkpoint: /home/user/models/UnifoLM-WMA-0-Base
```

```yaml
data:
    train:
        # Zmień na rzeczywistą ścieżkę do katalogu z danymi treningowymi
        data_dir: /path/to/training/dataset/directory
        # Przykład:
        # data_dir: /home/user/datasets/robot_training
```

#### `scripts/train.sh`

Otwórz plik i zaktualizuj następujące zmienne:

```bash
# Nazwa eksperymentu - możesz wybrać dowolną nazwę
experiment_name="my_experiment"

# Katalog gdzie zapisać punkty kontrolne modelu
save_root="/path/to/savedir"
# Przykład:
# save_root="/home/user/experiments"
```

### 2. Konfiguracja Inferencji

#### Tryb Interakcji (World Model Interaction)

W pliku `configs/inference/world_model_interaction.yaml`:

```yaml
pretrained_checkpoint: /path/to/checkpoint
data_dir: /path/to/prompts
```

#### Tryb Podejmowania Decyzji (Decision Making)

W pliku `configs/inference/world_model_decision_making.yaml`:

```yaml
data_dir: /path/to/dataset
```

W pliku `scripts/run_real_eval_server.sh`:

```bash
ckpt="/path/to/checkpoint"
res_dir="/path/to/results"
```

## Szybki Start - Przykładowa Konfiguracja

### Struktura Katalogów (Zalecana)

Zalecamy utworzenie następującej struktury katalogów:

```
~/unifolm_workspace/
    ├── models/                    # Pretrenowane modele
    │   ├── UnifoLM-WMA-0-Base/
    │   └── UnifoLM-WMA-0-Dual/
    ├── datasets/                  # Zbiory danych
    │   ├── Z1_StackBox/
    │   └── ...
    ├── experiments/               # Wyniki treningów
    │   ├── experiment1/
    │   └── ...
    └── results/                   # Wyniki inferencji
```

### Przykładowe Komendy

#### Utworzenie struktury katalogów

```bash
mkdir -p ~/unifolm_workspace/{models,datasets,experiments,results}
```

#### Pobieranie pretrenowanego modelu

```bash
cd ~/unifolm_workspace/models
# Pobierz model z HuggingFace (instrukcje na stronie modelu)
```

#### Aktualizacja konfiguracji

Po utworzeniu struktury, zaktualizuj pliki konfiguracyjne używając pełnych ścieżek:

```yaml
# W configs/train/config.yaml
pretrained_checkpoint: /home/user/unifolm_workspace/models/UnifoLM-WMA-0-Base
data_dir: /home/user/unifolm_workspace/datasets
```

```bash
# W scripts/train.sh
save_root="/home/user/unifolm_workspace/experiments"
```

## Weryfikacja Konfiguracji

Przed uruchomieniem treningu lub inferencji, upewnij się że:

1. ✅ Wszystkie ścieżki wskazują na istniejące katalogi lub pliki
2. ✅ Masz uprawnienia do odczytu/zapisu w tych katalogach
3. ✅ Katalogi z danymi zawierają wymagane pliki (patrz README.md)
4. ✅ Pretrenowane modele zostały pobrane i rozpakowane

## Sprawdzanie Ścieżek

Użyj następujących komend aby sprawdzić czy ścieżki są poprawne:

```bash
# Sprawdź czy katalog istnieje
ls -la /path/to/your/directory

# Sprawdź czy plik istnieje
ls -lh /path/to/your/file

# Sprawdź dostępne miejsce na dysku
df -h /path/to/your/directory
```

## Pomoc

Jeśli napotkasz problemy z konfiguracją:

1. Sprawdź czy wszystkie ścieżki są bezwzględne (zaczynają się od `/`)
2. Sprawdź czy nie ma literówek w ścieżkach
3. Upewnij się że wszystkie wymagane pliki i katalogi istnieją
4. Sprawdź logi błędów - często wskazują na brakujące pliki lub katalogi
