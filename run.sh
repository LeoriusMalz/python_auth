#!/bin/bash

# run.sh - Скрипт запуска приложения аутентификации

set -e

show_usage() {
    echo "Использование: sudo $0 <режим>"
    echo "Режимы:"
    echo "  src    - запуск из исходного кода (src/main.py)"
    echo "  release - запуск релизной версии (build/release/auth_app)"
    echo "  debug  - запуск отладочной версии (build/debug/auth_app)"
    echo ""
    echo "Пример: sudo $0 src"
}

if [ $# -ne 1 ]; then
    show_usage
    exit 1
fi

mode="$1"

case "$mode" in
    "src")
        echo "=== Запуск из исходного кода ==="
        if [ ! -f "src/main.py" ]; then
            echo "Ошибка: файл src/main.py не найден!"
            exit 1
        fi
        
        # Проверка прав на выполнение
        if [ ! -x "src/main.py" ]; then
            echo "Установка прав на выполнение для src/main.py..."
            chmod +x src/main.py
        fi
        
        echo "Запуск Python скрипта..."
        cd src && ./main.py
        ;;
        
    "release")
        echo "=== Запуск релизной версии ==="
        if [ ! -f "build/release/auth_app" ]; then
            echo "Ошибка: файл build/release/auth_app не найден!"
            echo "Сначала выполните сборку: sudo ./build.sh"
            exit 1
        fi
        
        # Проверка прав на выполнение
        if [ ! -x "build/release/auth_app" ]; then
            echo "Установка прав на выполнение для build/release/auth_app..."
            chmod +x build/release/auth_app
        fi
        
        echo "Запуск релизной версии..."
        ./build/release/auth_app
        ;;
        
    "debug")
        echo "=== Запуск отладочной версии ==="
        if [ ! -f "build/debug/auth_app" ]; then
            echo "Ошибка: файл build/debug/auth_app не найден!"
            echo "Сначала выполните сборку: sudo ./build.sh"
            exit 1
        fi
        
        # Проверка прав на выполнение
        if [ ! -x "build/debug/auth_app" ]; then
            echo "Установка прав на выполнение для build/debug/auth_app..."
            chmod +x build/debug/auth_app
        fi
        
        echo "Запуск отладочной версии..."
        ./build/debug/auth_app
        ;;
        
    *)
        echo "Неизвестный режим: $mode"
        show_usage
        exit 1
        ;;
esac
