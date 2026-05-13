# 07. Результаты fuzzing-тестирования

## Проверяемые компоненты

В рамках fuzzing были проверены:

- функция хеширования пароля;
- функция проверки логина и пароля;
- обработка строк формата `login:password`;
- обработка пустых строк;
- обработка Unicode-строк;
- обработка длинных строк;
- обработка специальных символов;
- обработка бинарных данных после декодирования в UTF-8.

Основной объект тестирования — модуль `src/auth_logic.py`, в который была вынесена бизнес-логика аутентификации. GUI-слой `src/main.py` напрямую не тестировался, так как он зависит от `tkinter` и требует графического окружения.

## Hypothesis

### Команда запуска

```bash
bash scripts/fuzz/run_hypothesis.sh
```

### Проверяемые свойства

1. Функция хеширования не должна падать на строковых входах.
2. Результат хеширования должен быть строкой.
3. SHA-256-хеш должен иметь длину 64 символа.
4. Функция аутентификации должна возвращать `bool`.
5. Некорректные логины и пароли не должны приводить к успешной аутентификации.
6. Unicode-входы не должны вызывать необработанных исключений.
7. Бинарные данные после декодирования в UTF-8 не должны приводить к аварийному завершению.

### Результат

Тестирование Hypothesis завершилось успешно.

Результат запуска:

```text
collected 6 items

tests/fuzz/test_hypothesis_auth.py ......

6 passed in 5.37s
```

Необработанные исключения, падения и зависания не обнаружены.

### Покрытие

Покрытие по результатам запуска Hypothesis:

```text
Name                Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------
src/auth_logic.py      18      3     10      4    75%   12, 19, 22, 24->27
src/main.py            94     94     24      0     0%   28-265
---------------------------------------------------------------
TOTAL                 112     97     34      4    14%
```

Низкое общее покрытие объясняется тем, что `src/main.py` содержит GUI-код `tkinter`, который в рамках fuzzing не запускался. Основной интерес представляет покрытие модуля `src/auth_logic.py`.

### Артефакты

Лог запуска:

```text
docs/fuzz/appendix/logs/hypothesis.log
```

Отчёт покрытия:

```text
docs/fuzz/appendix/reports/hypothesis/html/
docs/fuzz/appendix/reports/hypothesis/coverage.xml
```

## HypoFuzz

### Команда запуска

HypoFuzz запускается в составе общего fuzzing pipeline через `pytest` и `pytest-cov`:

```bash
bash scripts/fuzz/run_all_fuzz.sh
```

Фактическая команда запуска внутри общего скрипта:

```bash
pytest -q \
  --disable-warnings \
  --maxfail=1 \
  --cov=src \
  --cov-report=term-missing \
  --cov-report=html:docs/fuzz/appendix/reports/hypofuzz/html \
  --cov-report=xml:docs/fuzz/appendix/reports/hypofuzz/coverage.xml \
  tests/fuzz/test_hypofuzz_auth.py
```

### Проверяемые свойства

1. Функция аутентификации должна принимать строковые значения логина и пароля.
2. Некорректные строки не должны приводить к аварийному завершению.
3. Возвращаемое значение функции аутентификации должно иметь тип `bool`.
4. Coverage-guided запуск должен фиксировать покрытие тестируемого модуля.

### Особенность HypoFuzz

В текущей конфигурации HypoFuzz используется как coverage-guided слой поверх property-based тестов на базе `Hypothesis` и `pytest`.

Он не создаёт собственные crash-файлы по аналогии с Radamsa или AFL. Результаты фиксируются через:

- pytest-лог;
- coverage HTML-отчёт;
- coverage XML-отчёт.

### Результат

Тестирование HypoFuzz завершилось успешно.

Результат запуска:

```text
.                                                                        [100%]
1 passed in 0.37s
```

Необработанные исключения, падения и зависания не обнаружены.

### Покрытие

Покрытие по результатам запуска HypoFuzz:

```text
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
src/auth_logic.py      18      4    78%   12, 19, 22, 33
src/main.py            94     94     0%   28-265
-------------------------------------------------
TOTAL                 112     98    12%
```

Покрытие `src/auth_logic.py` составило 78%. Файл `src/main.py` не покрыт, так как содержит GUI-слой и не является целью fuzzing в данной методике.

### Артефакты

Лог запуска:

```text
docs/fuzz/appendix/logs/hypofuzz.log
```

Отчёт покрытия:

```text
docs/fuzz/appendix/reports/hypofuzz/html/
docs/fuzz/appendix/reports/hypofuzz/coverage.xml
```

## Radamsa

### Команда запуска

```bash
bash scripts/fuzz/run_radamsa.sh
```

### Seed-корпус

Использовались seed-файлы:

```text
tests/fuzz/seeds/valid_admin.txt
tests/fuzz/seeds/valid_vovuas.txt
tests/fuzz/seeds/empty.txt
tests/fuzz/seeds/unicode.txt
tests/fuzz/seeds/special.txt
tests/fuzz/seeds/long.txt
```

### Проверяемые свойства

1. Мутированные входы не должны приводить к падению.
2. Некорректные входы не должны приводить к успешной аутентификации.
3. Результат проверки должен иметь тип `bool`.
4. Бинарные и повреждённые входы должны безопасно декодироваться или обрабатываться как некорректные данные.

### Что делает Radamsa

Radamsa используется как mutation-based fuzzer. Он берёт валидные и невалидные seed-входы формата `login:password`, создаёт их мутированные варианты и передаёт их в Python harness.

Radamsa сам по себе не формирует coverage-отчёты и не анализирует результат выполнения приложения. Он отвечает только за генерацию искажённых входных данных. Проверка результата, сохранение crash-входов и логов выполняются shell-скриптом `scripts/fuzz/run_radamsa.sh`.

### Результат

Radamsa fuzzing завершился успешно.

Результат запуска:

```text
[*] Radamsa fuzzing finished
```

Crash-входы не обнаружены.

Путь для crash-входов:

```text
docs/fuzz/appendix/crashes/radamsa/
```

Лог запуска:

```text
docs/fuzz/appendix/logs/radamsa.log
```

## Сводная таблица

| Инструмент | Тип fuzzing | Результат | Артефакты |
|---|---|---|---|
| Hypothesis | Generation-based | 6 тестов успешно пройдены, необработанные исключения не обнаружены | logs, coverage |
| HypoFuzz | Coverage-guided pytest/Hypothesis execution | 1 тест успешно пройден, покрытие зафиксировано | logs, coverage |
| Radamsa | Mutation-based | 1000 мутированных входов обработаны, crash-входы не обнаружены | logs, crashes при наличии |

## Покрытие

Покрытие собиралось с помощью `pytest-cov`.

Отчёты покрытия расположены в:

```text
docs/fuzz/appendix/reports/
```

Основные отчёты:

```text
docs/fuzz/appendix/reports/hypothesis/html/
docs/fuzz/appendix/reports/hypothesis/coverage.xml
docs/fuzz/appendix/reports/hypofuzz/html/
docs/fuzz/appendix/reports/hypofuzz/coverage.xml
```

## Общий вывод по результатам

Fuzzing-тестирование не выявило падений, зависаний или необработанных исключений в тестируемой бизнес-логике аутентификации.

Основной вывод: функции обработки логина, пароля и хеширования устойчивы к проверенным классам некорректных, случайных и мутированных входных данных в рамках выбранной методики.

При этом покрытие GUI-слоя отсутствует, так как `tkinter`-интерфейс не является основной целью текущего fuzzing и требует отдельной методики GUI-тестирования.