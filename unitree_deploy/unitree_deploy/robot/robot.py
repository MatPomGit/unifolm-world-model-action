"""
Robot Module - Moduł Robota

Ten moduł definiuje główną klasę UnitreeRobot, która jest wysokopoziomowym
interfejsem do sterowania robotami Unitree (G1, Z1, itp.).

Klasa UnitreeRobot zarządza wszystkimi komponentami robota:
- Ramiona (arms) - przeguby i silniki ramion
- Efektory końcowe (endeffectors) - chwytaki, gripper
- Kamery (cameras) - kamery RGB, RGB-D

Dla początkujących:
    Ta klasa to "dyrygent orkiestry" - koordynuje wszystkie części robota,
    aby działały razem harmonijnie. Ukrywa złożoność komunikacji z
    poszczególnymi komponentami i udostępnia prosty interfejs.
"""

import time

import torch

from unitree_deploy.robot.robot_configs import UnitreeRobotConfig
from unitree_deploy.robot_devices.arm.utils import make_arm_motors_buses_from_configs
from unitree_deploy.robot_devices.cameras.utils import make_cameras_from_configs
from unitree_deploy.robot_devices.endeffector.utils import (
    make_endeffector_motors_buses_from_configs,
)
from unitree_deploy.utils.rich_logger import log_success


class UnitreeRobot:
    """
    Główna klasa reprezentująca robota Unitree.
    
    Ta klasa zarządza wszystkimi komponentami robota i zapewnia
    ujednolicony interfejs do:
    - Łączenia się z robotem
    - Zbierania obserwacji (obrazy, stany)
    - Wysyłania akcji (ruchy ramion, chwytaków)
    - Rozłączania się
    
    Attributes:
        config: Konfiguracja robota zawierająca parametry wszystkich urządzeń
        robot_type: Typ robota (np. 'g1_dex1', 'z1_realsense')
        cameras: Słownik kamer {nazwa: obiekt_kamery}
        arm: Słownik ramion {nazwa: obiekt_ramienia}
        endeffector: Słownik chwytaków {nazwa: obiekt_chwytaka}
        initial_data_received: Flaga określająca czy to pierwsza komenda
    
    Przykład użycia:
        ```python
        from unitree_deploy.robot.robot_utils import make_robot
        
        # Utwórz robota
        robot = make_robot('g1_dex1')
        
        # Połącz się
        robot.connect()
        
        # Zbierz obserwacje
        obs = robot.capture_observation()
        
        # Wyślij akcję
        action = torch.tensor([...])  # Docelowe pozycje przegubów
        robot.send_action(action)
        
        # Rozłącz się
        robot.disconnect()
        ```
    """
    
    def __init__(
        self,
        config: UnitreeRobotConfig,
    ):
        """
        Inicjalizuje robota z podaną konfiguracją.
        
        Args:
            config: Obiekt konfiguracji zawierający parametry wszystkich
                   komponentów robota (ramiona, kamery, chwytaki)
        
        Wyjaśnienie:
            Konstruktor tworzy obiekty dla wszystkich urządzeń robota
            na podstawie konfiguracji, ale jeszcze się z nimi nie łączy.
            Faktyczne połączenie następuje gdy wywołasz connect().
        """
        # Zapisz konfigurację
        self.config = config
        self.robot_type = self.config.type
        
        # Inicjalizuj kamery na podstawie konfiguracji
        # Tworzy obiekty kamer, ale jeszcze nie łączy się z nimi
        self.cameras = make_cameras_from_configs(self.config.cameras)
        
        # Inicjalizuj ramiona
        self.arm = make_arm_motors_buses_from_configs(self.config.arm)
        
        # Inicjalizuj efektory końcowe (chwytaki)
        self.endeffector = make_endeffector_motors_buses_from_configs(self.config.endeffector)

        # Flaga określająca czy to pierwsza komenda
        # Pierwsza komenda używa "drive_to_waypoint" (natychmiastowe przejście)
        # Kolejne używają "schedule_waypoint" (zaplanowane w harmonogramie)
        self.initial_data_received = True

    def connect(self):
        """
        Łączy się ze wszystkimi urządzeniami robota.
        
        Proces łączenia:
        1. Sprawdza czy robot ma jakiekolwiek urządzenia
        2. Łączy się z kamerami i "rozgrzewa" je (warmup)
        3. Łączy się z ramionami
        4. Łączy się z chwytakami
        5. Czeka na stabilizację wszystkich połączeń
        
        Raises:
            ValueError: Jeśli robot nie ma żadnych urządzeń do połączenia
        
        Wyjaśnienie "rozgrzewania" kamer:
            Kamery potrzebują kilku klatek na start, aby ustabilizować
            parametry ekspozycji i balansu bieli. Bez tego pierwsze obrazy
            mogą być zbyt jasne/ciemne lub mieć złe kolory.
        """
        # Sprawdź czy robot ma przynajmniej jedno urządzenie
        if not self.arm and self.endeffector and not self.cameras:
            raise ValueError(
                "UnitreeRobot nie ma żadnego urządzenia do połączenia. "
                "Zobacz przykład użycia w docstringu klasy."
            )
        
        # --- FAZA 1: ŁĄCZENIE Z KAMERAMI ---
        # Połącz się z każdą kamerą
        for name in self.cameras:
            self.cameras[name].connect()
            log_success(f"Łączenie z kamerą {name}.")

        # "Rozgrzej" kamery - pobierz 20 klatek na start
        # To pozwala kamerom ustabilizować parametry (ekspozycja, balans bieli)
        print("Rozgrzewanie kamer (pobieranie pierwszych klatek)...")
        for _ in range(20):
            for name in self.cameras:
                # async_read() pobiera klatkę bez blokowania
                self.cameras[name].async_read()
            # Czekaj ~33ms między klatkami (symulacja ~30 FPS)
            time.sleep(1 / 30)

        # --- FAZA 2: ŁĄCZENIE Z RAMIONAMI ---
        for name in self.arm:
            self.arm[name].connect()
            log_success(f"Łączenie z ramieniem {name}.")

        # --- FAZA 3: ŁĄCZENIE Z CHWYTAKAMI ---
        for name in self.endeffector:
            self.endeffector[name].connect()
            log_success(f"Łączenie z chwytakiem {name}.")

        # --- FAZA 4: STABILIZACJA ---
        # Czekaj 2 sekundy na ustabilizowanie wszystkich połączeń
        # To daje czas protokołom komunikacyjnym na pełną inicjalizację
        time.sleep(2)
        log_success("Wszystkie urządzenia połączone pomyślnie! ✅")

    def capture_observation(self):
        """
        Zbiera obserwacje ze wszystkich czujników robota.
        
        Zbiera:
        - Stany przegubów (pozycje) ze wszystkich ramion
        - Stany chwytaków (otwarcie/zamknięcie)
        - Obrazy ze wszystkich kamer
        
        Returns:
            dict: Słownik zawierający:
                - "observation.state": tensor ze stanami wszystkich przegubów
                - "observation.images.{cam_name}": tensory z obrazami z kamer
        
        Uwaga: Zwracane obserwacje NIE mają wymiaru batch (nie ma wiodącego wymiaru B).
        
        Wyjaśnienie dla początkujących:
            "Obserwacja" to wszystkie dane, które robot może "zobaczyć" i "poczuć"
            w danym momencie. To jak zmysły robota - wzrok (kamery) i propriocepcja
            (czucie własnego ciała - pozycje przegubów).
        """

        # --- FAZA 1: ZBIERANIE STANÓW PRZEGUBÓW ---
        
        # Listy do przechowywania stanów różnych komponentów
        state = []
        arm_state_list = []
        endeffector_state_list = []
        
        # Zbierz stany ze wszystkich ramion
        for arm_name in self.arm:
            # read_current_arm_q() zwraca bieżące pozycje przegubów (q = joint angles)
            arm_state = self.arm[arm_name].read_current_arm_q()
            # Konwertuj na tensor PyTorch
            arm_state_list.append(torch.from_numpy(arm_state))

        # Zbierz stany ze wszystkich chwytaków
        for endeffector_name in self.endeffector:
            # read_current_endeffector_q() zwraca bieżące stany palców chwytaka
            endeffector_state = self.endeffector[endeffector_name].read_current_endeffector_q()
            endeffector_state_list.append(torch.from_numpy(endeffector_state))

        # Połącz wszystkie stany w jeden wektor
        # Jeśli są jakieś stany, konkatenuj je; w przeciwnym razie pusty tensor
        state = (
            torch.cat(arm_state_list + endeffector_state_list, dim=0)
            if arm_state_list or endeffector_state_list
            else torch.tensor([])
        )

        # --- FAZA 2: ZBIERANIE OBRAZÓW Z KAMER ---
        
        images = {}
        for name in self.cameras:
            # async_read() pobiera najnowszą klatkę z kamery
            output = self.cameras[name].async_read()
            
            # Niektóre kamery zwracają wiele strumieni (np. RGB + depth)
            if isinstance(output, dict):
                # Jeśli słownik, dodaj wszystkie strumienie z prefiksem nazwy kamery
                images.update({k: torch.from_numpy(v) for k, v in output.items()})
            else:
                # Jeśli pojedynczy obraz, użyj nazwy kamery jako klucza
                images[name] = torch.from_numpy(output)

        # --- FAZA 3: FORMATOWANIE WYNIKÓW ---
        
        # Utwórz słownik w standardowym formacie
        obs_dict = {}
        
        # Dodaj stan (połączone pozycje wszystkich przegubów)
        obs_dict["observation.state"] = state
        
        # Dodaj obrazy z odpowiednimi kluczami
        for name, value in images.items():
            obs_dict[f"observation.images.{name}"] = value
            
        return obs_dict

    def send_action(self, action: torch.Tensor, t_command_target: float | None = None) -> torch.Tensor:
        """
        Wysyła akcję do robota (przesuwa ramiona i chwytaki do docelowych pozycji).
        
        Args:
            action: Tensor z docelowymi pozycjami dla wszystkich przegubów.
                   Kolejność: [pozycje_ramion, pozycje_chwytaków]
            t_command_target: Czas docelowy wykonania komendy (w sekundach od epoch).
                            Jeśli None, komenda wykonuje się natychmiast.
        
        Returns:
            torch.Tensor: Faktycznie wysłane akcje (mogą się różnić od żądanych
                         ze względu na ograniczenia fizyczne robota)
        
        Wyjaśnienie trybu komendy:
            - "drive_to_waypoint": Natychmiastowe przejście do pozycji docelowej
              (używane dla pierwszej komendy)
            - "schedule_waypoint": Zaplanowane przejście (używane w kolejnych komendach)
              Pozwala to robotowi płynnie interpolować między kolejnymi punktami
        
        Wyjaśnienie time_target:
            Robot potrzebuje czasu na wykonanie ruchu. t_command_target określa
            KIEDY robot powinien osiągnąć docelową pozycję. Dzięki temu możemy
            planować trajektorie z wyprzedzeniem i uzyskać płynne ruchy.
        """
        
        # --- FAZA 1: PRZYGOTOWANIE AKCJI DLA RAMION ---
        
        # Indeksy do wycinania odpowiednich fragmentów wektora akcji
        from_idx_arm = 0
        to_idx_arm = 0
        action_sent_arm = []  # Lista faktycznie wysłanych akcji dla ramion
        
        # Wybierz tryb komendy w zależności czy to pierwsza komenda
        # Pierwsza komenda: natychmiastowe przejście
        # Kolejne: zaplanowane (pozwala na płynną interpolację)
        cmd_target = "drive_to_waypoint" if self.initial_data_received else "schedule_waypoint"

        # Dla każdego ramienia
        for arm_name in self.arm:
            # Oblicz zakres indeksów dla tego ramienia
            to_idx_arm += len(self.arm[arm_name].motor_names)
            
            # Wytnij fragment akcji odpowiadający temu ramieniu
            action_arm = action[from_idx_arm:to_idx_arm].numpy()
            from_idx_arm = to_idx_arm

            # Zapisz wysłaną akcję
            action_sent_arm.append(torch.from_numpy(action_arm))

            # Wyślij akcję do ramienia
            # time_target jest konwertowany z time.monotonic() (czas systemowy)
            # na time.perf_counter() (czas wydajnościowy używany przez kontroler)
            self.arm[arm_name].write_arm(
                action_arm,
                time_target=t_command_target - time.monotonic() + time.perf_counter(),
                cmd_target=cmd_target,
            )

        # --- FAZA 2: PRZYGOTOWANIE AKCJI DLA CHWYTAKÓW ---
        
        # Kontynuuj od miejsca, gdzie zakończyły się akcje dla ramion
        from_idx_endeffector = to_idx_arm
        to_idx_endeffector = to_idx_arm

        action_endeffector_set = []  # Lista faktycznie wysłanych akcji dla chwytaków
        
        # Dla każdego chwytaka
        for endeffector_name in self.endeffector:
            # Oblicz zakres indeksów dla tego chwytaka
            to_idx_endeffector += len(self.endeffector[endeffector_name].motor_names)
            
            # Wytnij fragment akcji odpowiadający temu chwytakowi
            action_endeffector = action[from_idx_endeffector:to_idx_endeffector].numpy()
            from_idx_endeffector = to_idx_endeffector

            # Zapisz wysłaną akcję
            action_endeffector_set.append(torch.from_numpy(action_endeffector))

            # Wyślij akcję do chwytaka
            self.endeffector[endeffector_name].write_endeffector(
                action_endeffector,
                time_target=t_command_target - time.monotonic() + time.perf_counter(),
                cmd_target=cmd_target,
            )

        # --- FAZA 3: AKTUALIZACJA STANU ---
        
        # Po pierwszej komendzie, następne będą używać trybu "schedule_waypoint"
        self.initial_data_received = False

        # Zwróć wszystkie faktycznie wysłane akcje jako jeden tensor
        return torch.cat(action_sent_arm + action_endeffector_set, dim=0)

    def disconnect(self):
        """
        Rozłącza się ze wszystkimi urządzeniami robota.
        
        Bezpiecznie zamyka połączenia z:
        - Wszystkimi ramionami
        - Wszystkimi chwytakami
        - Wszystkimi kamerami
        
        Ważne: Zawsze wywołaj tę funkcję przed zakończeniem programu!
        
        Wyjaśnienie:
            Prawidłowe rozłączenie jest kluczowe dla bezpieczeństwa robota
            i stabilności systemu. Bez tego robot może pozostać w nieokreślonym
            stanie, a połączenia sieciowe mogą nie zostać zwolnione.
        """
        # Rozłącz wszystkie ramiona
        for name in self.arm:
            self.arm[name].disconnect()
            log_success(f"Rozłączono ramię {name}.")

        # Rozłącz wszystkie chwytaki
        for name in self.endeffector:
            self.endeffector[name].disconnect()
            log_success(f"Rozłączono chwytaka {name}.")

        # Rozłącz wszystkie kamery
        for name in self.cameras:
            self.cameras[name].disconnect()
            log_success(f"Rozłączono kamerę {name}.")

    def __del__(self):
        """
        Destruktor - wywoływany automatycznie gdy obiekt jest usuwany.
        
        Zapewnia, że robot zostanie rozłączony nawet jeśli programista
        zapomni wywołać disconnect().
        
        Wyjaśnienie:
            To "siatka bezpieczeństwa". Jeśli z jakiegoś powodu program
            zakończy się nieoczekiwanie lub programista zapomni rozłączyć
            robota, destruktor zrobi to automatycznie.
        """
        # Sprawdź czy robot jest połączony
        # getattr() bezpiecznie pobiera atrybut (nie rzuca błędu jeśli nie istnieje)
        if getattr(self, "is_connected", False):
            self.disconnect()
