# Простое python приложение аутентификации с GUI на tkinter для Debian 12

#### Статус SAST пайплайна:
[![SAST Analysis](https://github.com/LeoriusMalz/python_auth/actions/workflows/sast.yml/badge.svg)](https://github.com/LeoriusMalz/python_auth/actions/workflows/sast.yml)

#### Последние отчеты SAST анализа
- [Bandit Report](reports/latest/bandit_report.txt)
- [Flake8 Report](reports/latest/flake8_report.txt)
- [Radon Complexity](reports/latest/radon_complexity.txt)
- [Radon Maintainability](reports/latest/radon_mi.txt)

TODO:

1. Добавить соль к паролю перед хешированием.

2. Использовать SQLite для сохранения БД пользователей, добавить интерфейс администрирования БД.

## Порядок запуска с нуля (проверялось на live usb с Debian 12.5.0 amd64 Cinnamon)

**ВНИМАНИЕ:** pyinstaller устанавливается через pip3 с флагом --break-system-packages! По-хорошему надо делать через venv (виртуальное окружение).

Не забудьте сделать chmod +x *.sh перед запуском скриптов.

### Установка зависимостей

sudo ./config.sh

### Сборка через pyinstaller, документация doxygen

sudo ./build.sh

### Запуск приложения

sudo ./run.sh

# Собранные бинарники и документация в релизах!!!