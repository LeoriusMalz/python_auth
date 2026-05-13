# 06. Установка, настройка и интеграция

## Среда тестирования

Fuzzing-тестирование выполнялось в локальной среде разработки.

Используемая среда:

- macOS;
- Python 3;
- pip;
- pytest;
- pytest-cov;
- hypothesis;
- hypofuzz;
- radamsa.

Также проект может быть запущен в Linux-среде, например Ubuntu 20.04 или Debian 12.

## Подготовка структуры проекта

Для fuzzing были добавлены директории:

```text
docs/fuzz/
docs/fuzz/appendix/crashes/
docs/fuzz/appendix/logs/
docs/fuzz/appendix/reports/
scripts/fuzz/
tests/fuzz/
tests/fuzz/seeds/
```

## Установка Python-зависимостей

```bash
python3 -m pip install pytest pytest-cov hypothesis hypofuzz
```

## Установка Radamsa

На macOS:

```bash
brew install radamsa
```

На Linux:

```bash
apt update
apt install radamsa
```

Если пакет `radamsa` недоступен в окружении, инструмент может быть установлен из исходников или исключён из практического запуска с фиксацией ограничения в отчёте.

## Интеграция с проектом

Так как основной файл `src/main.py` создаёт GUI-окно при запуске, для fuzzing рекомендуется вынести бизнес-логику в отдельный модуль:

```text
src/auth_logic.py
```

В модуль выносится:

- функция хеширования;
- словарь пользователей;
- функция проверки логина и пароля.

Пример тестируемого интерфейса:

```python
def myhash(value: str) -> str:
    ...

def authenticate(login: str, password: str) -> bool:
    ...
```

Такой подход позволяет запускать fuzzing без инициализации `tkinter` и без необходимости графического окружения.

## Запуск Hypothesis

```bash
bash scripts/fuzz/run_hypothesis.sh
```

Результаты:

```text
docs/fuzz/appendix/logs/hypothesis.log
docs/fuzz/appendix/reports/hypothesis/
docs/fuzz/appendix/reports/hypothesis/coverage.xml
```

## Запуск HypoFuzz

`HypoFuzz` используется как coverage-guided слой поверх pytest/Hypothesis-тестов. В текущей конфигурации он запускается через pytest-based скрипт.

```bash
bash scripts/fuzz/run_hypofuzz.sh
```

Результаты:

```text
docs/fuzz/appendix/logs/hypofuzz.log
docs/fuzz/appendix/reports/hypofuzz/
docs/fuzz/appendix/reports/hypofuzz_coverage.xml
```

Важно: `HypoFuzz` не создаёт собственные crash-файлы и отдельные нативные отчёты. Для фиксации результатов используются pytest-логи и coverage-отчёты.

## Пример запуска HypoFuzz через pytest

```bash
PYTHONPATH=. pytest -q \
  --disable-warnings \
  --maxfail=1 \
  --cov=src \
  --cov-report=term-missing \
  --cov-report=html:docs/fuzz/appendix/reports/hypofuzz \
  --cov-report=xml:docs/fuzz/appendix/reports/hypofuzz_coverage.xml \
  tests/fuzz/fuzz_hypofuzz_auth.py
```

## Запуск Radamsa

```bash
bash scripts/fuzz/run_radamsa.sh
```

Результаты:

```text
docs/fuzz/appendix/logs/radamsa.log
docs/fuzz/appendix/crashes/radamsa/
```

`Radamsa` сам по себе не генерирует coverage-отчёты. Он используется как генератор мутированных входных данных. Crash-входы и логи сохраняются shell-скриптом запуска.

## Запуск всех fuzzing-тестов одной командой

```bash
bash scripts/fuzz/run_all_fuzz.sh
```

## Автоматизация

Скрипт `scripts/fuzz/run_all_fuzz.sh` выполняет:

1. Запуск Hypothesis.
2. Запуск HypoFuzz.
3. Проверку наличия Radamsa.
4. Запуск Radamsa при наличии.
5. Сохранение логов.
6. Сохранение coverage-отчётов.
7. Сохранение crash-входов для mutation-based fuzzing.

## Особенности запуска на macOS

В macOS отсутствует утилита `shuf`, которая обычно доступна в Linux. Поэтому в shell-скриптах для случайного выбора seed-файла используется Python-код, а не `shuf`.

Также при запуске fuzzing-тестов необходимо учитывать `PYTHONPATH`, чтобы Python корректно находил модуль `src.auth_logic`.

Пример:

```bash
export PYTHONPATH="$(pwd)"
```
