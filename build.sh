#!/bin/bash

# build.sh - Скрипт сборки приложения через pyinstaller

set -e

# Функция для генерации упрощенного Doxyfile
generate_simple_doxyfile() {
    cat > Doxyfile << 'EOF'
# Упрощенный Doxyfile для Python проекта
PROJECT_NAME           = "Authentication App"
PROJECT_NUMBER         = 1.0
PROJECT_BRIEF          = "Простое приложение аутентификации"
OUTPUT_DIRECTORY       = docs
OUTPUT_LANGUAGE        = Russian
INPUT                  = src
FILE_PATTERNS          = *.py
RECURSIVE              = YES
EXTRACT_ALL            = YES
EXTRACT_PRIVATE        = NO
GENERATE_HTML          = YES
HTML_OUTPUT            = html
SEARCHENGINE           = YES
GENERATE_LATEX         = NO
EOF
    echo "Создан упрощенный Doxyfile"
}

# Функция для валидации ввода DEBUG
validate_debug() {
    local input="$1"
    if [[ "$input" =~ ^[YyДд]?$ ]] || [[ "$input" == "true" ]] || [[ "$input" == "1" ]]; then
        echo "true"
    elif [[ "$input" =~ ^[NnНн]?$ ]] || [[ "$input" == "false" ]] || [[ "$input" == "0" ]]; then
        echo "false"
    else
        echo ""
    fi
}

# Функция для валидации ввода START_ATTEMPTS
validate_attempts() {
    local input="$1"
    if [[ "$input" =~ ^[0-9]+$ ]] && [ "$input" -ge 1 ] && [ "$input" -le 10 ]; then
        echo "$input"
    else
        echo ""
    fi
}

echo "=== Сборка приложения аутентификации ==="

# Проверка и создание Doxyfile если нужно
if [ ! -f "Doxyfile" ]; then
    echo "Doxyfile не найден, создается упрощенная версия..."
    generate_simple_doxyfile
fi

# Запрос режима сборки
read -p "Сборка в режиме DEBUG? [y/N] (по умолчанию N): " debug_input
debug_input=$(validate_debug "$debug_input")

if [ -z "$debug_input" ]; then
    echo "Некорректный ввод! Используется значение по умолчанию: false"
    debug_input="false"
fi

# Запрос количества попыток
read -p "Количество попыток входа [1-10] (по умолчанию 3): " attempts_input
attempts_input=$(validate_attempts "$attempts_input")

if [ -z "$attempts_input" ]; then
    echo "Некорректный ввод! Используется значение по умолчанию: 3"
    attempts_input="3"
fi

echo "Параметры сборки: DEBUG=$debug_input, START_ATTEMPTS=$attempts_input"

# Проверка существования исходного файла
if [ ! -f "src/main.py" ]; then
    echo "Ошибка: исходный файл src/main.py не найден!"
    exit 1
fi

# Создание временной копии для модификации
cp src/main.py src/main.py.bak

# Изменение значений DEBUG и START_ATTEMPTS в исходном коде
echo "Модификация исходного кода..."

# Замена DEBUG (первое вхождение)
sed -i "0,/^DEBUG=/s/^DEBUG=.*/DEBUG=$debug_input/" src/main.py

# Замена START_ATTEMPTS (первое вхождение) 
sed -i "0,/^START_ATTEMPTS=/s/^START_ATTEMPTS=.*/START_ATTEMPTS=$attempts_input/" src/main.py

# Проверка успешности замены
if grep -q "DEBUG=$debug_input" src/main.py && grep -q "START_ATTEMPTS=$attempts_input" src/main.py; then
    echo "Успешно заменены параметры в исходном коде"
else
    echo "Ошибка при замене параметров! Восстановление исходного файла..."
    mv src/main.py.bak src/main.py
    exit 1
fi

# Определение параметров сборки
if [ "$debug_input" == "true" ]; then
    build_dir="build/debug"
    console_param="--console"
    echo "Режим сборки: DEBUG"
else
    build_dir="build/release"
    console_param="-w"
    echo "Режим сборки: RELEASE"
fi

# Сборка через pyinstaller
echo "Запуск pyinstaller..."
pyinstaller $console_param --onefile --distpath "$build_dir" --name auth_app src/main.py

# Генерация документации doxygen
echo "Генерация документации..."
doxygen Doxyfile

# Восстановление исходного файла
mv src/main.py.bak src/main.py

echo "=== Сборка завершена ==="
echo "Исполняемый файл: $build_dir/auth_app"
echo "Документация: docs/html/index.html"
