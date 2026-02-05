"""
Robot Client - Klient Robota

Ten skrypt implementuje klienta robota, który komunikuje się z serwerem polityki
w celu sterowania rzeczywistym robotem Unitree.

Architektura:
    - Klient (ten skrypt) działa na komputerze podłączonym do robota
    - Serwer polityki działa na mocnym komputerze z GPU
    - Komunikacja odbywa się przez HTTP/REST API
    
Przepływ danych:
    1. Klient zbiera obserwacje z robota (obrazy, stany przegubów)
    2. Wysyła obserwacje do serwera polityki
    3. Serwer przewiduje akcje używając modelu AI
    4. Klient otrzymuje akcje i wykonuje je na robocie
    5. Proces powtarza się w pętli

Dla początkujących:
    Ten program jest "klientem" w architekturze klient-serwer. Robot (klient)
    zbiera dane z czujników, wysyła je do serwera z modelem AI, otrzymuje
    decyzje i wykonuje je. To pozwala wykorzystać moc obliczeniową zdalnego
    serwera do sterowania robotem w czasie rzeczywistym.
"""

import argparse
import os
import time
import cv2
import numpy as np
import torch
import tqdm

from typing import Any, Deque, MutableMapping, OrderedDict
from collections import deque
from pathlib import Path

from unitree_deploy.real_unitree_env import make_real_env
from unitree_deploy.utils.eval_utils import (
    ACTTemporalEnsembler,
    LongConnectionClient,
    populate_queues,
)

# -----------------------------------------------------------------------------
# Konfiguracja sieci i środowiska
# Network & environment defaults
# -----------------------------------------------------------------------------

# Wyczyść proxy, aby zapewnić bezpośrednie połączenie
# Proxy może powodować opóźnienia i problemy z połączeniem
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

# Adres serwera polityki
# HOST: 127.0.0.1 oznacza localhost (komputer lokalny przez tunel SSH)
# PORT: 8000 - standardowy port dla serwera polityki
HOST = "127.0.0.1"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"


# fmt: off
# Pozycje początkowe dla różnych typów robotów
# INIT_POSE: Bezpieczne pozycje startowe przed rozpoczęciem zadania
# Są to pozycje, w których robot jest stabilny i gotowy do pracy
INIT_POSE = {
    # G1 z chwytakiem Dex1: 16 wartości (14 dla ramion + 2 dla chwytaków)
    'g1_dex1': np.array([0.10559805, 0.02726714, -0.01210221, -0.33341318, -0.22513399, -0.02627627, -0.15437093,  0.1273793 , -0.1674708 , -0.11544029, -0.40095493,  0.44332668,  0.11566751,  0.3936641, 5.4, 5.4], dtype=np.float32),
    
    # Z1 podwójny z chwytakiem Dex1: 14 wartości (12 dla ramion + 2 dla chwytaków)
    'z1_dual_dex1_realsense': np.array([-1.0262332,  1.4281361, -1.2149128,  0.6473399, -0.12425245, 0.44945636,  0.89584476,  1.2593982, -1.0737865,  0.6672816, 0.39730102, -0.47400007, 0.9894176, 0.9817477 ], dtype=np.float32),
    
    # Z1 pojedynczy: 7 wartości (6 dla ramienia + 1 dla chwytaka)
    'z1_realsense': np.array([-0.06940782, 1.4751548, -0.7554075, 1.0501366, 0.02931615, -0.02810347, -0.99238837], dtype=np.float32),
}

# Akcje zerowe (brak ruchu) dla różnych robotów
# Używane jako placeholder w pierwszej iteracji
ZERO_ACTION = {
    'g1_dex1': torch.zeros(16, dtype=torch.float32),
    'z1_dual_dex1_realsense': torch.zeros(14, dtype=torch.float32),
    'z1_realsense': torch.zeros(7, dtype=torch.float32),
}

# Klucze kamer dla różnych robotów
# Określają, z której kamery pobierać obraz główny
CAM_KEY = {
    'g1_dex1': 'cam_right_high',           # Prawa kamera wysoka dla G1
    'z1_dual_dex1_realsense': 'cam_high',  # Kamera wysoka dla Z1 dual
    'z1_realsense': 'cam_high',            # Kamera wysoka dla Z1
}
# fmt: on


def prepare_observation(args: argparse.Namespace, obs: Any) -> OrderedDict:
    """
    Przygotowuje obserwację do wysłania do serwera polityki.
    
    Konwertuje surowe dane z robota na format oczekiwany przez model AI.
    
    Args:
        args: Argumenty linii poleceń zawierające konfigurację robota
        obs: Surowa obserwacja z robota zawierająca:
            - obs.observation["images"][cam_key]: obraz BGR z kamery
            - obs.observation["qpos"]: pozycje przegubów (joint positions)
    
    Returns:
        OrderedDict: Słownik uporządkowany zawierający:
            - "observation.images.top": obraz RGB jako tensor (C, H, W)
            - "observation.state": stan przegubów jako tensor
            - "action": akcja zerowa (placeholder)
    
    Wyjaśnienie dla początkujących:
        Modele AI oczekują danych w konkretnym formacie. Ta funkcja:
        1. Konwertuje obraz z BGR (format OpenCV) na RGB (format standardowy)
        2. Zmienia układ wymiarów z (H, W, C) na (C, H, W) dla PyTorch
        3. Pakuje wszystko w słownik z odpowiednimi kluczami
    """
    # Konwersja obrazu z BGR (OpenCV) na RGB (standardowy format)
    # BGR to kolejność kolorów używana przez OpenCV, ale modele AI oczekują RGB
    rgb_image = cv2.cvtColor(
        obs.observation["images"][CAM_KEY[args.robot_type]], cv2.COLOR_BGR2RGB)
    
    # Tworzenie słownika obserwacji w formacie oczekiwanym przez model
    observation = {
        # Obraz: Konwersja na tensor i zmiana układu wymiarów
        # permute(2, 0, 1) zmienia (Height, Width, Channels) na (Channels, Height, Width)
        "observation.images.top":
        torch.from_numpy(rgb_image).permute(2, 0, 1),
        
        # Stan robota: Pozycje wszystkich przegubów (qpos = joint positions)
        "observation.state":
        torch.from_numpy(obs.observation["qpos"]),
        
        # Akcja: Początkowo zerowa (zostanie zastąpiona przez przewidywania)
        "action": ZERO_ACTION[args.robot_type],
    }
    
    # OrderedDict zachowuje kolejność elementów (ważne dla niektórych modeli)
    return OrderedDict(observation)


def run_policy(
    args: argparse.Namespace,
    env: Any,
    client: LongConnectionClient,
    temporal_ensembler: ACTTemporalEnsembler,
    cond_obs_queues: MutableMapping[str, Deque[torch.Tensor]],
    output_dir: Path,
) -> None:
    """
    Główna pętla wykonywania polityki (rollout loop).
    
    Ta funkcja implementuje kompletny cykl sterowania robotem:
    1. Inicjalizacja: Przesuwa robota do pozycji startowej
    2. Percepcja: Zbiera obserwacje ze wszystkich czujników
    3. Komunikacja: Wysyła obserwacje do serwera i otrzymuje akcje
    4. Wygładzanie: Stosuje temporal ensembling dla płynniejszego sterowania
    5. Wykonanie: Wykonuje akcje na robocie w pętli czasu rzeczywistego
    
    Args:
        args: Argumenty konfiguracyjne (częstotliwość, horyzonty, itp.)
        env: Środowisko robota (interfejs do sprzętu)
        client: Klient HTTP do komunikacji z serwerem polityki
        temporal_ensembler: Obiekt wygładzający akcje w czasie
        cond_obs_queues: Kolejki przechowujące historię obserwacji
        output_dir: Katalog do zapisywania wyników (opcjonalnie)
    
    Wyjaśnienie Temporal Ensembling:
        Zamiast wykonywać akcje bezpośrednio z modelu, uśredniamy
        przewidywania z kilku kroków czasowych. To eliminuje szarpnięcia
        i sprawia, że ruchy są płynniejsze i bardziej naturalne.
    
    Wyjaśnienie Action Horizon:
        Model przewiduje sekwencję akcji do przodu (np. 16 kroków).
        To pozwala modelowi planować długofalowo i tworzyć spójne trajektorie.
    """
    
    # --- FAZA 1: INICJALIZACJA (WARM START) ---
    # Przesuń robota do bezpiecznej pozycji startowej
    # To zapewnia, że robot zaczyna z przewidywalnej konfiguracji
    print("Przesuwanie robota do pozycji startowej...")
    _ = env.step(INIT_POSE[args.robot_type])
    
    # Czekaj 2 sekundy, aby robot ustabilizował się w pozycji
    # Robot potrzebuje czasu, aby zatrzymać oscylacje po ruchu
    time.sleep(2.0)
    print("Robot gotowy. Rozpoczynam pętlę sterowania...")
    
    # Licznik kroków czasowych
    t = 0

    # --- FAZA 2: GŁÓWNA PĘTLA STEROWANIA ---
    while True:
        # --- Krok A: ZBIERANIE OBSERWACJI ---
        # Pobierz bieżący stan robota (obrazy, pozycje przegubów)
        obs = env.get_observation(t)
        
        # Przekonwertuj obserwację na format dla modelu
        obs = prepare_observation(args, obs)
        
        # Dodaj obserwację do kolejek historycznych
        # Model może używać kilku ostatnich obserwacji (observation_horizon)
        cond_obs_queues = populate_queues(cond_obs_queues, obs)
        
        # --- Krok B: ZAPYTANIE SERWERA O AKCJE ---
        # Wyślij obserwacje i instrukcję językową do serwera polityki
        # Serwer uruchomi model AI i zwróci przewidywane akcje
        pred_actions = client.predict_action(
            args.language_instruction,  # Np. "pack black camera into box"
            cond_obs_queues             # Historia obserwacji
        ).unsqueeze(0)  # Dodaj wymiar batch
        
        # --- Krok C: WYGŁADZANIE CZASOWE ---
        # Zastosuj temporal ensembling, aby uczynić akcje płynniejszymi
        # Bierzemy tylko pierwsze action_horizon akcji z przewidywanej sekwencji
        actions = temporal_ensembler.update(
            pred_actions[:, :args.action_horizon]
        )[0]  # Usuń wymiar batch

        # --- Krok D: WYKONYWANIE AKCJI ---
        # Wykonaj kolejne exe_steps akcji z przewidywanej sekwencji
        for n in range(args.exe_steps):
            # Konwertuj akcję z tensora PyTorch na tablicę NumPy
            action = actions[n].cpu().numpy()
            
            # Wyświetl akcję dla celów debugowania
            print(f">>> Wykonuję krok {n} z {args.exe_steps}")
            print(f"    Akcja: {action}")
            print("---------------------------------------------")

            # --- Synchronizacja czasu rzeczywistego ---
            # Zapisz czas przed wykonaniem akcji
            t1 = time.time()
            
            # Wykonaj akcję na robocie
            obs = env.step(action)
            
            # Oblicz ile czasu zajęło wykonanie
            elapsed = time.time() - t1
            
            # Poczekaj pozostały czas, aby zachować stałą częstotliwość
            # Np. dla 15 Hz: każdy krok powinien trwać 1/15 ≈ 0.067 sekundy
            target_dt = 1 / args.control_freq
            sleep_time = max(0, target_dt - elapsed)
            time.sleep(sleep_time)
            
            # Inkrementuj licznik kroków
            t += 1

            # --- Aktualizacja kolejek obserwacji ---
            # Przygotuj kolejki na następną iterację (z wyjątkiem ostatniego kroku)
            # W ostatnim kroku tego fragmentu i tak zapytamy serwer o nowe akcje
            if n < args.exe_steps - 1:
                obs = prepare_observation(args, obs)
                cond_obs_queues = populate_queues(cond_obs_queues, obs)


def run_eval(args: argparse.Namespace) -> None:
    """
    Główna funkcja uruchamiająca ewaluację polityki na rzeczywistym robocie.
    
    Ta funkcja:
    1. Inicjalizuje klienta HTTP do komunikacji z serwerem
    2. Tworzy obiekt temporal ensembler do wygładzania akcji
    3. Przygotowuje kolejki do przechowywania historii obserwacji
    4. Tworzy środowisko robota i łączy się z nim
    5. Uruchamia określoną liczbę epizodów (rollouts)
    6. Zamyka połączenie po zakończeniu
    
    Args:
        args: Argumenty konfiguracyjne z linii poleceń
    
    Wyjaśnienie dla początkujących:
        "Ewaluacja" oznacza testowanie wytrenowanego modelu na rzeczywistym
        robocie. "Epizod" (rollout) to jedna próba wykonania zadania od
        początku do końca (np. jedno pakowanie kamery do pudełka).
    """
    
    # --- FAZA 1: INICJALIZACJA KLIENTA ---
    # Utwórz klienta HTTP do komunikacji z serwerem polityki
    # LongConnectionClient utrzymuje trwałe połączenie dla lepszej wydajności
    print(f"Łączenie z serwerem polityki pod adresem: {BASE_URL}")
    client = LongConnectionClient(BASE_URL)

    # --- FAZA 2: INICJALIZACJA TEMPORAL ENSEMBLER ---
    # ACTTemporalEnsembler wygładza akcje poprzez uśrednianie eksponencjalne
    # temporal_ensemble_coeff: współczynnik wygładzania (0.01 = bardzo płynne)
    # chunk_size: liczba przewidywanych akcji do przodu
    # exe_steps: liczba akcji faktycznie wykonywanych
    temporal_ensembler = ACTTemporalEnsembler(
        temporal_ensemble_coeff=0.01,
        chunk_size=args.action_horizon,
        exe_steps=args.exe_steps
    )
    temporal_ensembler.reset()  # Zresetuj stan początkowy

    # --- FAZA 3: INICJALIZACJA KOLEJEK OBSERWACJI ---
    # Kolejki (deques) przechowują historię ostatnich obserwacji
    # Model może używać wielu ostatnich klatek do lepszego zrozumienia dynamiki
    cond_obs_queues = {
        # Kolejka obrazów: przechowuje observation_horizon ostatnich obrazów
        "observation.images.top": deque(maxlen=args.observation_horizon),
        
        # Kolejka stanów: przechowuje observation_horizon ostatnich stanów przegubów
        "observation.state": deque(maxlen=args.observation_horizon),
        
        # Kolejka akcji: przechowuje 16 ostatnich akcji
        # UWAGA: Na sztywno zakodowane na 16, ponieważ model przewiduje 16 kroków do przodu
        "action": deque(maxlen=16),
    }

    # --- FAZA 4: INICJALIZACJA ŚRODOWISKA ROBOTA ---
    # Tworzy interfejs do rzeczywistego robota
    # robot_type: typ robota (g1_dex1, z1_realsense, itp.)
    # dt: okres próbkowania (1/częstotliwość sterowania)
    print(f"Inicjalizacja środowiska robota typu: {args.robot_type}")
    env = make_real_env(
        robot_type=args.robot_type,
        dt=1 / args.control_freq,  # Np. dla 15 Hz: dt = 0.067s
    )
    
    # Łączy się z robotem (kamery, ramiona, chwytaki)
    print("Łączenie z urządzeniami robota...")
    env.connect()
    print("Połączono pomyślnie!")

    # --- FAZA 5: WYKONYWANIE EPIZODÓW ---
    try:
        # Wykonaj określoną liczbę prób (rollouts)
        # tqdm.tqdm pokazuje pasek postępu
        for episode_idx in tqdm.tqdm(range(0, args.num_rollouts_planned),
                                      desc="Epizody"):
            # Utwórz katalog dla wyników tego epizodu
            output_dir = Path(args.output_dir) / f"episode_{episode_idx:03d}"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"\n=== Rozpoczynam epizod {episode_idx + 1}/{args.num_rollouts_planned} ===")
            
            # Uruchom pojedynczy epizod (rollout)
            run_policy(args, env, client, temporal_ensembler, cond_obs_queues,
                      output_dir)
            
            print(f"=== Zakończono epizod {episode_idx + 1} ===\n")
            
    finally:
        # --- FAZA 6: CZYSZCZENIE ---
        # Ten blok wykona się zawsze, nawet jeśli wystąpi błąd
        # Zamyka połączenie z robotem (ważne dla bezpieczeństwa!)
        print("Zamykanie połączenia z robotem...")
        env.close()
        print("Połączenie zamknięte. Program zakończony.")


def get_parser() -> argparse.ArgumentParser:
    """
    Tworzy parser argumentów linii poleceń.
    
    Returns:
        argparse.ArgumentParser: Parser z zdefiniowanymi wszystkimi argumentami
    
    Wyjaśnienie dla początkujących:
        ArgumentParser pozwala użytkownikom dostosować zachowanie programu
        bez modyfikowania kodu. Parametry są podawane przez linię poleceń, np.:
        python robot_client.py --robot_type g1_dex1 --control_freq 30
    """
    parser = argparse.ArgumentParser(
        description="Klient robota do wykonywania polityki w czasie rzeczywistym"
    )
    
    # Typ robota
    parser.add_argument(
        "--robot_type",
        type=str,
        default="g1_dex1",
        help="Typ ucieleśnienia robota (g1_dex1, z1_realsense, z1_dual_dex1_realsense)"
    )
    
    # Horyzont akcji - ile kroków do przodu przewiduje model
    parser.add_argument(
        "--action_horizon",
        type=int,
        default=16,
        help="Liczba przyszłych akcji przewidywanych przez politykę. "
             "Większa wartość = lepsze planowanie długoterminowe, ale wolniejsze. "
             "Typowo: 16-32 kroków."
    )
    
    # Liczba kroków wykonania
    parser.add_argument(
        "--exe_steps",
        type=int,
        default=16,
        help="Liczba przyszłych akcji faktycznie wykonywanych na robocie. "
             "Musi być <= action_horizon. Typowo równe action_horizon. "
             "Mniejsza wartość = częstsze odpytywanie serwera."
    )
    
    # Horyzont obserwacji - ile klatek wstecz uwzględnia model
    parser.add_argument(
        "--observation_horizon",
        type=int,
        default=2,
        help="Liczba ostatnich klatek/stanów uwzględnianych przez model. "
             "2 = bieżąca + poprzednia klatka (pozwala modelować prędkości). "
             "Większa wartość = więcej kontekstu, ale więcej danych do przesłania."
    )
    
    # Instrukcja językowa
    parser.add_argument(
        "--language_instruction",
        type=str,
        default="Pack black camera into box",
        help="Instrukcja językowa opisująca zadanie dla polityki. "
             "Przykłady: 'pack black camera into box', 'stack red box on blue box', "
             "'clean up pencils from table'"
    )
    
    # Liczba prób
    parser.add_argument(
        "--num_rollouts_planned",
        type=int,
        default=10,
        help="Liczba epizodów (prób) do wykonania. "
             "Każdy epizod to jedna kompletna próba wykonania zadania."
    )
    
    # Katalog wyników
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./results",
        help="Katalog do zapisywania wyników, logów i nagrań. "
             "Dla każdego epizodu tworzony jest podkatalog episode_XXX."
    )
    
    # Częstotliwość sterowania
    parser.add_argument(
        "--control_freq",
        type=float,
        default=30,
        help="Częstotliwość sterowania nisko-poziomowego w Hz. "
             "15-30 Hz: typowo dla precyzyjnej manipulacji. "
             "Za wysoka: sieć może nie nadążyć. "
             "Za niska: ruchy będą szarpane."
    )
    
    return parser


if __name__ == "__main__":
    """
    Punkt wejścia programu.
    
    Ten blok wykona się tylko, gdy uruchamiasz ten plik bezpośrednio,
    nie gdy importujesz go jako moduł.
    """
    # Parsuj argumenty linii poleceń
    parser = get_parser()
    args = parser.parse_args()
    
    # Wyświetl konfigurację
    print("=" * 70)
    print("ROBOT CLIENT - KLIENT ROBOTA")
    print("=" * 70)
    print(f"Typ robota:             {args.robot_type}")
    print(f"Serwer polityki:        {BASE_URL}")
    print(f"Instrukcja:             {args.language_instruction}")
    print(f"Częstotliwość:          {args.control_freq} Hz")
    print(f"Horyzont akcji:         {args.action_horizon}")
    print(f"Kroki wykonania:        {args.exe_steps}")
    print(f"Horyzont obserwacji:    {args.observation_horizon}")
    print(f"Liczba epizodów:        {args.num_rollouts_planned}")
    print(f"Katalog wyników:        {args.output_dir}")
    print("=" * 70)
    print()
    
    # Uruchom ewaluację
    run_eval(args)
