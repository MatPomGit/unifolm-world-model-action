# Polityka Bezpieczeństwa / Security Policy

## Wspierane Wersje / Supported Versions

Obecnie wspieramy następujące wersje projektu UnifoLM-WMA-0 z aktualizacjami bezpieczeństwa:

We currently support the following versions of UnifoLM-WMA-0 with security updates:

| Wersja / Version | Wspierana / Supported          |
| ---------------- | ------------------------------ |
| 0.0.1 (current)  | :white_check_mark: Tak / Yes   |

## Zgłaszanie Podatności / Reporting a Vulnerability

### Po Polsku

Jeśli odkryjesz lukę w zabezpieczeniach w projekcie UnifoLM-WMA-0, prosimy o odpowiedzialne zgłoszenie jej nam. Bardzo doceniamy współpracę badaczy bezpieczeństwa w celu ochrony naszych użytkowników.

#### Jak zgłosić

**NIE** zgłaszaj luk w zabezpieczeniach poprzez publiczne zgłoszenia GitHub issues.

Zamiast tego, prosimy wysłać email do:
- **Email**: rd_xyc@unitree.com
- **Temat**: [SECURITY] Opis problemu

#### Czego oczekiwać

1. **Potwierdzenie**: Otrzymasz potwierdzenie w ciągu 48 godzin
2. **Wstępna ocena**: W ciągu 7 dni otrzymasz wstępną ocenę podatności
3. **Aktualizacje**: Będziemy Cię informować o postępach co najmniej raz w tygodniu
4. **Rozwiązanie**: Dołożymy wszelkich starań, aby naprawić krytyczne luki w ciągu 30 dni

#### Co powinno zawierać zgłoszenie

- Typ podatności
- Pełna ścieżka do pliku(ów) źródłowych związanych z manifestacją podatności
- Lokalizacja kodu źródłowego, którego dotyczy problem (tag/branch/commit lub bezpośredni URL)
- Krok po kroku instrukcje jak odtworzyć problem
- Kod proof-of-concept lub exploit (jeśli możliwe)
- Wpływ podatności, w tym jak atakujący może wykorzystać tę lukę

#### Nasza polityka ujawniania

- Gdy otrzymamy zgłoszenie o podatności, natychmiast rozpoczniemy pracę nad jej naprawą
- Będziemy Cię informować o postępach i współpracować z Tobą w celu zrozumienia i rozwiązania problemu
- Po wydaniu poprawki, wspólnie ustalimy odpowiedni czas na publiczne ujawnienie (zazwyczaj 90 dni)
- Doceniamy Twój wkład i (jeśli chcesz) z przyjemnością uznamy Twoje odkrycie w komunikacie o bezpieczeństwie

### In English

If you discover a security vulnerability in the UnifoLM-WMA-0 project, please report it to us responsibly. We greatly appreciate the collaboration of security researchers in protecting our users.

#### How to Report

**DO NOT** report security vulnerabilities through public GitHub issues.

Instead, please send an email to:
- **Email**: rd_xyc@unitree.com
- **Subject**: [SECURITY] Description of the issue

#### What to Expect

1. **Acknowledgment**: You will receive confirmation within 48 hours
2. **Initial Assessment**: Within 7 days you will receive an initial assessment of the vulnerability
3. **Updates**: We will keep you informed of progress at least once a week
4. **Resolution**: We will make every effort to fix critical vulnerabilities within 30 days

#### What Should a Report Include

- Type of vulnerability
- Full paths of source file(s) related to the manifestation of the vulnerability
- The location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the vulnerability, including how an attacker might exploit it

#### Our Disclosure Policy

- When we receive a vulnerability report, we will immediately begin work on fixing it
- We will keep you informed of progress and work with you to understand and resolve the issue
- After releasing a fix, we will jointly determine an appropriate time for public disclosure (typically 90 days)
- We appreciate your contribution and (if you wish) will gladly acknowledge your discovery in the security advisory

## Najlepsze Praktyki Bezpieczeństwa / Security Best Practices

### Dla Użytkowników / For Users

1. **Aktualizuj regularnie** / **Update regularly**
   - Zawsze używaj najnowszej wersji projektu
   - Always use the latest version of the project

2. **Bezpieczne przechowywanie punktów kontrolnych** / **Secure checkpoint storage**
   - Nie udostępniaj publicznie swoich wytrenowanych modeli bez przeglądu
   - Don't share your trained models publicly without review
   - Modele mogą zawierać informacje o Twoim środowisku
   - Models may contain information about your environment

3. **Ochrona danych** / **Data protection**
   - Nie trenuj modeli na wrażliwych lub prywatnych danych bez odpowiednich zabezpieczeń
   - Don't train models on sensitive or private data without proper safeguards
   - Sprawdź dane treningowe pod kątem informacji identyfikujących osobę
   - Check training data for personally identifiable information

4. **Komunikacja sieciowa** / **Network communication**
   - Używaj szyfrowanych połączeń (SSH tunel) podczas komunikacji klient-serwer
   - Use encrypted connections (SSH tunnel) for client-server communication
   - Nie wystawiaj serwerów inferencyjnych bezpośrednio na internet bez uwierzytelniania
   - Don't expose inference servers directly to the internet without authentication

5. **Bezpieczeństwo fizyczne robotów** / **Physical robot safety**
   - Zawsze miej przycisk awaryjny w zasięgu ręki
   - Always have an emergency stop button within reach
   - Nigdy nie zostawiaj robota bez nadzoru podczas działania
   - Never leave a robot unattended while operating
   - Ustaw fizyczne limity bezpiecznego obszaru roboczego
   - Set physical limits for safe working area

### Dla Programistów / For Developers

1. **Weryfikacja kodu** / **Code verification**
   - Zawsze przeglądaj kod przed włączeniem go do projektu
   - Always review code before including it in the project
   - Używaj narzędzi do statycznej analizy kodu
   - Use static code analysis tools

2. **Zarządzanie zależnościami** / **Dependency management**
   - Regularnie aktualizuj zależności
   - Regularly update dependencies
   - Sprawdzaj znane luki w zależnościach
   - Check for known vulnerabilities in dependencies
   - Używaj pinned versions w produkcji
   - Use pinned versions in production

3. **Walidacja danych wejściowych** / **Input validation**
   - Zawsze waliduj dane wejściowe od użytkownika
   - Always validate user input
   - Nie zakładaj, że dane z zewnątrz są bezpieczne
   - Don't assume external data is safe

4. **Bezpieczne przechowywanie** / **Secure storage**
   - Nie commituj sekretów do repozytorium (klucze API, hasła, tokeny)
   - Don't commit secrets to the repository (API keys, passwords, tokens)
   - Używaj zmiennych środowiskowych lub menedżerów sekretów
   - Use environment variables or secret managers

## Znane Ograniczenia / Known Limitations

### Ograniczenia Modelu / Model Limitations

- Model może generować nieprzewidywalne zachowania poza zakresem danych treningowych
- The model may generate unpredictable behaviors outside the training data range
- Zawsze testuj w kontrolowanym środowisku przed wdrożeniem
- Always test in a controlled environment before deployment

### Ograniczenia Środowiska / Environment Limitations

- Kod wdrożeniowy nie jest zabezpieczony przeciwko złośliwym akcjom
- The deployment code is not hardened against malicious actions
- Należy uruchamiać tylko w zaufanych środowiskach
- Should only be run in trusted environments

## Kontakt / Contact

W sprawach bezpieczeństwa kontaktuj się z:
For security matters, contact:

- **Email**: rd_xyc@unitree.com
- **Temat / Subject**: [SECURITY] Twój problem / Your issue

Dziękujemy za pomoc w utrzymaniu bezpieczeństwa projektu UnifoLM-WMA-0!

Thank you for helping keep UnifoLM-WMA-0 secure!
