# Architektura Projektu / Project Architecture

## Przegląd / Overview

UnifoLM-WMA-0 to framework łączący model świata (world model) z polityką akcji (action policy) dla uczenia robotów. Projekt składa się z trzech głównych komponentów:

UnifoLM-WMA-0 is a framework combining a world model with an action policy for robot learning. The project consists of three main components:

1. **Model Świata (World Model)** - przewiduje przyszłe stany środowiska
2. **Głowa Akcji (Action Head)** - generuje akcje do wykonania
3. **System Wdrożenia (Deployment System)** - uruchamia model na rzeczywistych robotach

## Architektura Wysokiego Poziomu / High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    UnifoLM-WMA-0 Framework                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │   World Model    │◄────────┤  Action Head     │          │
│  │  (Prediction)    │         │  (Decision)      │          │
│  └──────────────────┘         └──────────────────┘          │
│         ▲                              ▲                     │
│         │                              │                     │
│         └──────────────┬───────────────┘                     │
│                        │                                     │
│              ┌─────────▼─────────┐                          │
│              │  Data Pipeline    │                          │
│              │  (Processing)     │                          │
│              └───────────────────┘                          │
│                        ▲                                     │
└────────────────────────┼─────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
    ┌────▼─────┐                  ┌─────▼────┐
    │ Training │                  │ Inference│
    │  Mode    │                  │   Mode   │
    └──────────┘                  └──────────┘
```

## Komponenty Główne / Main Components

### 1. Model Świata / World Model

**Lokalizacja:** `src/unifolm_wma/models/world_model.py`

Model świata to transformer-based model generowania wideo, który:
- Przyjmuje sekwencję obrazów i akcji
- Przewiduje przyszłe ramki wideo
- Służy jako symulator dla uczenia robotów

The world model is a transformer-based video generation model that:
- Takes a sequence of images and actions
- Predicts future video frames
- Serves as a simulator for robot learning

**Kluczowe funkcje:**
- Enkodowanie obrazów do przestrzeni latent
- Generowanie przyszłych stanów
- Dekodowanie z powrotem do przestrzeni pikseli

```python
class WorldModel(nn.Module):
    def __init__(self):
        self.image_encoder = ImageEncoder()
        self.temporal_transformer = TemporalTransformer()
        self.action_conditioner = ActionConditioner()
        self.video_decoder = VideoDecoder()
    
    def forward(self, images, actions):
        # Encode images
        latents = self.image_encoder(images)
        # Predict future latents conditioned on actions
        future_latents = self.temporal_transformer(latents, actions)
        # Decode to video frames
        future_frames = self.video_decoder(future_latents)
        return future_frames
```

### 2. Głowa Akcji / Action Head

**Lokalizacja:** `src/unifolm_wma/models/action_head.py`

Głowa akcji to policy network, która:
- Przetwarza obserwacje robota
- Generuje sekwencję akcji (action chunking)
- Wykorzystuje temporal ensembling dla płynności

The action head is a policy network that:
- Processes robot observations
- Generates action sequences (action chunking)
- Uses temporal ensembling for smoothness

**Kluczowe funkcje:**
- Przetwarzanie wielomodalnych danych wejściowych (obraz, stan)
- Generowanie horizon akcji
- Kondycjonowanie na instrukcje językowe

```python
class ActionHead(nn.Module):
    def __init__(self, action_dim, action_horizon):
        self.observation_encoder = ObservationEncoder()
        self.policy_network = PolicyNetwork()
        self.action_decoder = ActionDecoder(action_dim, action_horizon)
    
    def forward(self, observations, language_instruction):
        # Encode multimodal observations
        obs_features = self.observation_encoder(observations)
        # Generate action features
        action_features = self.policy_network(obs_features, language_instruction)
        # Decode to action sequence
        actions = self.action_decoder(action_features)
        return actions
```

### 3. Pipeline Danych / Data Pipeline

**Lokalizacja:** `src/unifolm_wma/data/`

Pipeline danych obsługuje:
- Ładowanie danych z formatów LeRobot
- Normalizację i augmentację
- Batch processing

Data pipeline handles:
- Loading data from LeRobot formats
- Normalization and augmentation
- Batch processing

**Komponenty:**
- `dataloader.py` - klasy do ładowania danych
- `transforms.py` - transformacje obrazów i stanów

### 4. System Wdrożenia / Deployment System

**Lokalizacja:** `unitree_deploy/`

System wdrożenia to architektura klient-serwer:

The deployment system is a client-server architecture:

```
┌─────────────────┐                    ┌──────────────────┐
│  Server (GPU)   │                    │  Client (Robot)  │
│                 │                    │                  │
│  ┌───────────┐  │                    │  ┌────────────┐  │
│  │   Model   │  │◄───Observations────│  │  Sensors   │  │
│  │ Inference │  │                    │  │  (Cameras) │  │
│  └───────────┘  │                    │  └────────────┘  │
│       │         │                    │        ▲         │
│       │         │                    │        │         │
│       ▼         │                    │        │         │
│  ┌───────────┐  │                    │  ┌────────────┐  │
│  │  Action   │  │────Actions────────►│  │ Actuators  │  │
│  │Generation │  │                    │  │ (Motors)   │  │
│  └───────────┘  │                    │  └────────────┘  │
└─────────────────┘                    └──────────────────┘
         ▲                                      │
         │                                      │
         └──────────── SSH Tunnel ──────────────┘
```

**Kluczowe komponenty:**
- `real_eval_server.py` - serwer inferencji
- `robot_client.py` - klient robota
- `robot/` - abstrakcje robotów
- `robot_devices/` - komponenty sprzętowe

## Przepływ Danych / Data Flow

### Trening / Training

```
1. Zbieranie Danych / Data Collection
   ├─► Demonstracje człowieka / Human demonstrations
   └─► Format LeRobot V2.1

2. Przetwarzanie / Processing
   ├─► prepare_training_data.py
   ├─► Normalizacja / Normalization
   └─► Podział train/val / Train/val split

3. Trening / Training
   ├─► Dataloader
   ├─► Model forward pass
   ├─► Loss computation
   └─► Backpropagation

4. Ewaluacja / Evaluation
   ├─► Metryki treningowe / Training metrics
   └─► Checkpoints
```

### Inferencja / Inference

#### Tryb Symulacji / Simulation Mode

```
1. Wejście / Input
   ├─► Obraz startowy / Initial image
   ├─► Stan robota / Robot state
   └─► Instrukcja językowa / Language instruction

2. Model świata / World model
   ├─► Enkodowanie / Encoding
   ├─► Przewidywanie / Prediction
   └─► Generowanie wideo / Video generation

3. Wyjście / Output
   └─► Symulowane przyszłe stany / Simulated future states
```

#### Tryb Podejmowania Decyzji / Decision Making Mode

```
1. Zbieranie Obserwacji / Observation Collection
   ├─► Obrazy z kamer / Camera images
   ├─► Stan przegubów / Joint positions
   └─► Instrukcja zadania / Task instruction

2. Serwer Inferencji / Inference Server
   ├─► Enkodowanie obserwacji / Encode observations
   ├─► Generowanie akcji / Generate actions
   └─► Temporal ensembling

3. Klient Robota / Robot Client
   ├─► Odbieranie akcji / Receive actions
   ├─► Wykonanie / Execution
   └─► Bezpieczeństwo / Safety checks

4. Pętla / Loop
   └─► Powrót do kroku 1 / Return to step 1
```

## Kluczowe Algorytmy / Key Algorithms

### Action Chunking

Generowanie sekwencji akcji zamiast pojedynczych akcji:

Generating action sequences instead of single actions:

```python
def generate_action_chunk(observation, action_horizon=16):
    """
    Generuje horizon akcji do przodu
    Generates horizon of actions ahead
    """
    actions = model.predict(observation)  # Shape: (horizon, action_dim)
    return actions
```

**Zalety / Benefits:**
- Lepsze planowanie długoterminowe / Better long-term planning
- Płynniejsze trajektorie / Smoother trajectories
- Mniejsza liczba zapytań do modelu / Fewer model queries

### Temporal Ensembling

Wygładzanie akcji poprzez uśrednianie przewidywań:

Smoothing actions by averaging predictions:

```python
def temporal_ensemble(new_actions, prev_actions, coeff=0.01):
    """
    Łączy nowe akcje z poprzednimi dla płynności
    Combines new actions with previous ones for smoothness
    """
    ensembled = coeff * new_actions + (1 - coeff) * prev_actions
    return ensembled
```

**Zalety / Benefits:**
- Eliminuje szarpnięcia / Eliminates jerkiness
- Stabilne sterowanie / Stable control
- Lepsze osiągi / Better performance

## Wzorce Projektowe / Design Patterns

### 1. Strategy Pattern (Policy)

Różne strategie treningowe i inferencji:

Different training and inference strategies:

```python
class TrainingStrategy(ABC):
    @abstractmethod
    def train_step(self, batch):
        pass

class DecisionMakingStrategy(TrainingStrategy):
    def train_step(self, batch):
        # Train only action head
        pass

class SimulationStrategy(TrainingStrategy):
    def train_step(self, batch):
        # Train world model
        pass
```

### 2. Factory Pattern (Robot Configuration)

Tworzenie różnych konfiguracji robotów:

Creating different robot configurations:

```python
class RobotFactory:
    @staticmethod
    def create_robot(robot_type):
        if robot_type == "g1_dex1":
            return G1DexRobot()
        elif robot_type == "z1_dual":
            return Z1DualRobot()
        # ...
```

### 3. Observer Pattern (Callbacks)

System callbacków podczas treningu:

Callback system during training:

```python
class TrainingCallback(ABC):
    @abstractmethod
    def on_epoch_end(self, epoch, logs):
        pass

class CheckpointCallback(TrainingCallback):
    def on_epoch_end(self, epoch, logs):
        if epoch % self.save_freq == 0:
            self.save_checkpoint()
```

## Optymalizacje / Optimizations

### Wydajność Pamięci / Memory Efficiency

- Gradient checkpointing dla dużych modeli
- Mixed precision training (FP16/FP32)
- Batch size adaptation

### Wydajność Obliczeniowa / Computational Efficiency

- Distributed training support
- Model parallelism
- Efficient data loading with prefetching

### Wydajność I/O / I/O Efficiency

- Caching preprocessed data
- Asynchronous data loading
- Compressed storage formats

## Rozszerzalność / Extensibility

### Dodawanie Nowych Robotów / Adding New Robots

1. Utwórz konfigurację robota w `robot_configs.py`
2. Zaimplementuj interfejs `Robot` w `robot.py`
3. Dodaj urządzenia w `robot_devices/`
4. Zaktualizuj `RobotFactory`

### Dodawanie Nowych Zadań / Adding New Tasks

1. Przygotuj dane w formacie LeRobot
2. Dodaj instrukcje językowe
3. Skonfiguruj dataset weights
4. Wytrenuj lub dostosuj model

### Dodawanie Nowych Modeli / Adding New Models

1. Zaimplementuj klasę modelu w `models/`
2. Dodaj do rejestru modeli
3. Zaktualizuj konfigurację
4. Dodaj odpowiednie testy

## Bezpieczeństwo / Security

### Walidacja Wejścia / Input Validation

```python
def validate_action(action, limits):
    """Sprawdza czy akcja jest w bezpiecznych granicach"""
    return np.all(action >= limits.min) and np.all(action <= limits.max)
```

### Rate Limiting

```python
class RateLimiter:
    def __init__(self, max_freq):
        self.min_interval = 1.0 / max_freq
        self.last_time = 0
    
    def wait(self):
        elapsed = time.time() - self.last_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_time = time.time()
```

## Testowanie / Testing

### Testy Jednostkowe / Unit Tests

Lokalizacja: `tests/`

- Test importów modułów
- Test kształtów tensorów
- Test funkcji pomocniczych

### Testy Integracyjne / Integration Tests

- Test pipeline danych
- Test treningu end-to-end
- Test inferencji

### Testy Systemowe / System Tests

- Test komunikacji klient-serwer
- Test na rzeczywistych robotach
- Test bezpieczeństwa

## Monitorowanie / Monitoring

### Metryki Treningowe / Training Metrics

- Loss functions (reconstruction, action prediction)
- Validation metrics
- Learning rate schedules

### Metryki Wdrożenia / Deployment Metrics

- Latency (network + inference)
- Success rate
- Safety violations
- Resource usage (CPU/GPU/memory)

## Zależności / Dependencies

### Główne Zależności / Core Dependencies

- **PyTorch** (2.3.1) - deep learning framework
- **Transformers** (4.40.1) - model architectures
- **PyTorch Lightning** (1.9.3) - training framework
- **OpenCV** (4.10.0.84) - image processing
- **Pinocchio** (3.2.0) - robot kinematics

### Opcjonalne Zależności / Optional Dependencies

- **pre-commit** - git hooks
- **pytest** - testing
- **black/isort** - code formatting
- **flake8** - linting

## Referencje / References

### Prace Naukowe / Research Papers

- UnifoLM: Unified Language Model Family
- DynamiCrafter: Video generation
- Diffusion Policy: Action prediction with diffusion

### Projekty Powiązane / Related Projects

- [LeRobot](https://github.com/huggingface/lerobot) - dataset format
- [Open-X Embodiment](https://robotics-transformer-x.github.io/) - dataset
- [Unitree Robots](https://www.unitree.com/) - hardware platform

## Kontakt i Wsparcie / Contact and Support

- **Email**: rd_xyc@unitree.com
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas

---

Dokument ten jest aktywnie utrzymywany. Sugestie ulepszeń są mile widziane!

This document is actively maintained. Suggestions for improvements are welcome!
