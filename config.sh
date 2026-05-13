#!/bin/bash

# config.sh - Скрипт настройки среды для сборки приложения аутентификации

set -e

echo "=== Настройка среды сборки ==="

# Обновление пакетов
echo "Обновление списка пакетов..."
apt update

# Установка Python3 и Tkinter
echo "Установка Python3 и Tkinter..."
apt install -y python3 python3-tk

# Установка pip
echo "Установка pip..."
apt install -y python3-pip

# Установка pyinstaller
echo "Установка pyinstaller..."
pip3 install pyinstaller --break-system-packages

# Установка doxygen
echo "Установка doxygen..."
apt install -y doxygen graphviz

# Создание структуры папок
echo "Создание структуры папок..."
mkdir -p build/release build/debug docs

echo "=== Настройка завершена ==="
