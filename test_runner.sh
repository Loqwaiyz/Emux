#!/bin/bash

EMULATOR_PATH="./shell_emulator.py"
SCRIPT_PATH="./test_script.emu"

echo "================================================="
echo "  ТЕСТ 1: Запуск в интерактивном режиме (REPL)   "
echo "================================================="
echo "Команда: python3 $EMULATOR_PATH"
python3 "$EMULATOR_PATH" --vfs_path "/opt/my_vfs" 
echo "  (Для продолжения введите 'exit' в эмуляторе)  "
# Примечание: Здесь ожидается ручной ввод 'exit' для завершения

echo ""
echo "================================================="
echo " ТЕСТ 2: Запуск с выполнением стартового скрипта "
echo "================================================="
echo "Команда: python3 $EMULATOR_PATH --startup_script $SCRIPT_PATH --vfs_path /var/emu_root"
python3 "$EMULATOR_PATH" --startup_script "$SCRIPT_PATH" --vfs_path "/var/emu_root"

echo ""
echo "================================================="
echo " ТЕСТ 3: Запуск с ошибкой (скрипт не найден) "
echo "================================================="
echo "Команда: python3 $EMULATOR_PATH --startup_script non_existent.emu"
python3 "$EMULATOR_PATH" --startup_script "non_existent.emu"

echo "================================================="
echo "  Тестирование завершено.                        "
echo "================================================="