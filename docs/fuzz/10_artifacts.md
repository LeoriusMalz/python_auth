# 10. Артефакты fuzzing-тестирования

## Назначение артефактов

Артефакты fuzzing используются для фиксации результатов тестирования, воспроизведения найденных ошибок и подготовки задач разработчикам.

В рамках текущего проекта артефакты включают:

- логи запусков;
- coverage-отчёты;
- crash-входы при наличии;
- seed-корпус;
- fuzzing harness-файлы;
- shell-скрипты автоматизации.

## Структура артефактов

```text
docs/fuzz/appendix/
├── crashes/
│   └── radamsa/
├── logs/
│   ├── hypothesis.log
│   ├── hypofuzz.log
│   └── radamsa.log
└── reports/
    ├── hypothesis/
    │   ├── html/
    │   └── coverage.xml
    └── hypofuzz/
        ├── html/
        └── coverage.xml
```

## Crash-входы

Crash-входы сохраняются в директории:

```text
docs/fuzz/appendix/crashes/
```

Назначение:

- сохранить входные данные, вызвавшие падение;
- обеспечить воспроизводимость ошибки;
- использовать вход как регрессионный тест после исправления.

Для текущей конфигурации crash-входы сохраняются в основном для Radamsa:

```text
docs/fuzz/appendix/crashes/radamsa/
```

По результатам текущего запуска crash-входы не обнаружены.

## Логи

Логи сохраняются в директории:

```text
docs/fuzz/appendix/logs/
```

Основные файлы:

```text
hypothesis.log
hypofuzz.log
radamsa.log
```

Назначение логов:

- фиксация команд запуска;
- фиксация результатов тестирования;
- фиксация ошибок;
- фиксация stack trace при падении;
- подтверждение выполнения fuzzing.

## Лог Hypothesis

Файл:

```text
docs/fuzz/appendix/logs/hypothesis.log
```

Содержит:

- информацию о pytest-сессии;
- список выполненных тестов;
- результат прохождения;
- coverage summary;
- пути к coverage-отчётам.

По результатам текущего запуска:

```text
6 passed in 5.37s
```

## Лог HypoFuzz

Файл:

```text
docs/fuzz/appendix/logs/hypofuzz.log
```

Содержит:

- результат pytest-запуска;
- coverage summary;
- пути к coverage-отчётам.

По результатам текущего запуска:

```text
1 passed in 0.37s
```

Важно: HypoFuzz не создаёт собственные crash-файлы и отдельные нативные отчёты. Для фиксации результатов используются pytest-лог и coverage-отчёты.

## Лог Radamsa

Файл:

```text
docs/fuzz/appendix/logs/radamsa.log
```

Содержит результат mutation-based fuzzing.

По результатам текущего запуска:

```text
[*] Radamsa fuzzing finished
```

Crash-входы не обнаружены.

## Отчёты покрытия

Отчёты покрытия сохраняются в директории:

```text
docs/fuzz/appendix/reports/
```

Основные отчёты Hypothesis:

```text
docs/fuzz/appendix/reports/hypothesis/html/
docs/fuzz/appendix/reports/hypothesis/coverage.xml
```

Основные отчёты HypoFuzz:

```text
docs/fuzz/appendix/reports/hypofuzz/html/
docs/fuzz/appendix/reports/hypofuzz/coverage.xml
```

HTML-отчёты можно открыть в браузере:

```text
docs/fuzz/appendix/reports/hypothesis/html/index.html
docs/fuzz/appendix/reports/hypofuzz/html/index.html
```

## Seed-корпус

Seed-файлы расположены в:

```text
tests/fuzz/seeds/
```

Примеры seed-файлов:

```text
valid_admin.txt
valid_vovuas.txt
empty.txt
unicode.txt
special.txt
long.txt
```

Назначение seed-корпуса:

- задать начальные валидные и невалидные входы;
- использовать их для mutation-based fuzzing;
- обеспечить повторяемость эксперимента.

## Тест-кейсы

Fuzzing-тесты расположены в:

```text
tests/fuzz/
```

Основные файлы:

```text
test_hypothesis_auth.py
test_hypofuzz_auth.py
test_radamsa_auth.py
```

Назначение файлов:

| Файл | Назначение |
|---|---|
| `test_hypothesis_auth.py` | Property-based fuzzing через Hypothesis |
| `test_hypofuzz_auth.py` | Coverage-guided pytest/Hypothesis запуск |
| `test_radamsa_auth.py` | Harness для мутированных входов Radamsa |

## Скрипты запуска

Скрипты запуска расположены в:

```text
scripts/fuzz/
```

Основные файлы:

```text
run_hypothesis.sh
run_radamsa.sh
run_all_fuzz.sh
```

В текущей конфигурации HypoFuzz запускается из общего скрипта `run_all_fuzz.sh` как отдельный pytest-based этап с сохранением логов и coverage-отчётов.

## Автоматизация

Основной скрипт запуска:

```bash
bash scripts/fuzz/run_all_fuzz.sh
```

Он выполняет:

1. Запуск Hypothesis.
2. Запуск HypoFuzz через pytest/coverage.
3. Проверку наличия Radamsa.
4. Запуск Radamsa при наличии.
5. Сохранение логов.
6. Сохранение coverage-отчётов.
7. Сохранение crash-входов для Radamsa при обнаружении падений.

## Правила обработки найденных ошибок

При обнаружении ошибки необходимо:

1. Сохранить входные данные в `docs/fuzz/appendix/crashes`.
2. Сохранить лог ошибки в `docs/fuzz/appendix/logs`.
3. Описать ошибку в `docs/fuzz/07_results.md`.
4. Проанализировать причину в `docs/fuzz/08_analysis.md`.
5. Сформировать задачу разработчику.
6. После исправления добавить crash-вход в регрессионные тесты.

## Итог

Артефакты fuzzing позволяют подтвердить факт выполнения тестирования, воспроизвести найденные ошибки и использовать результаты для дальнейшего улучшения безопасности приложения.

По результатам текущего запуска:

- Hypothesis завершился успешно;
- HypoFuzz завершился успешно;
- Radamsa завершился успешно;
- crash-входы не обнаружены;
- coverage-отчёты сохранены для Hypothesis и HypoFuzz.