import os
import getpass
import socket
import shlex
import sys
import argparse

# --- Глобальные переменные для конфигурации ---
VFS_PATH = ""
STARTUP_SCRIPT = ""
INTERACTIVE_MODE = True # Флаг: True - REPL, False - Скрипт

# --- 1. Формирование приглашения к вводу ---
def get_prompt():
    """Формирует приглашение к вводу в стиле username@hostname:~$"""
    try:
        username = getpass.getuser()
    except Exception:
        username = "user"

    try:
        hostname = socket.gethostname().split('.')[0]
    except Exception:
        hostname = "localhost"

    # Просто берем текущую директорию для отображения
    current_dir = os.path.basename(os.getcwd())
    if not current_dir:
         current_dir = '/'

    return f"{username}@{hostname}:{current_dir}$ "

# --- 4. и 5. Реализация команд (из Этапа 1) ---

def handle_ls(args):
    """Заглушка для команды ls"""
    print(f"[ls] Команда ls выполнена. Аргументы: {args}")
    return 0 # Возвращаем код успешного завершения

def handle_cd(args):
    """Заглушка для команды cd"""
    if not args:
        print("[cd] Команда cd (без аргументов)")
        return 0
        
    print(f"[cd] Команда cd выполнена. Аргументы: {args}")
    # Имитация ошибки при попытке перейти в '/non-existent-dir'
    if args and args[0] == '/non-existent-dir':
        print(f"[cd] Ошибка: Директория '{args[0]}' не найдена (имитация).")
        return 1 # Возвращаем код ошибки
        
    return 0

def handle_exit(args):
    """Команда exit"""
    print("Выход из эмулятора.")
    sys.exit(0)

# Словарь для диспетчеризации команд
COMMANDS = {
    "ls": handle_ls,
    "cd": handle_cd,
    "exit": handle_exit,
}

def execute_command(line):
    """
    Парсит и исполняет одну строку команды.
    Возвращает код завершения команды (0 - успех, >0 - ошибка).
    """
    line = line.strip()
    if not line:
        return 0

    try:
        # shlex.split() для корректной обработки кавычек
        tokens = shlex.split(line)
    except ValueError as e:
        if INTERACTIVE_MODE:
            print(f"Ошибка парсинга: Некорректные кавычки. {e}")
        return 1 # Ошибка парсинга

    command = tokens[0]
    args = tokens[1:]

    if command in COMMANDS:
        return COMMANDS[command](args)
    else:
        if INTERACTIVE_MODE:
            print(f"Ошибка: Команда '{command}' не найдена.")
        return 127 # Код ошибки "команда не найдена" (как в bash)

# --- 2. Логика выполнения стартового скрипта ---

def run_startup_script():
    """Выполняет команды из стартового скрипта с имитацией диалога."""
    global INTERACTIVE_MODE
    INTERACTIVE_MODE = False
    
    script_path = STARTUP_SCRIPT
    
    print(f"\n--- Запуск стартового скрипта: {script_path} ---")
    try:
        with open(script_path, 'r') as f:
            for i, raw_line in enumerate(f, 1):
                line = raw_line.strip()
                if not line or line.startswith('#'):
                    continue # Пропускаем пустые строки и комментарии

                # Имитация ввода команды (требование 2)
                print(f"{get_prompt()}{line}")
                
                exit_code = execute_command(line)

                # Остановка при первой ошибке (требование 2)
                if exit_code != 0:
                    print(f"\nОшибка выполнения в строке {i} ('{line}'). Код: {exit_code}.")
                    print("Выполнение скрипта остановлено.")
                    return
        print("\n--- Выполнение скрипта завершено успешно ---")

    except FileNotFoundError:
        print(f"Ошибка: Стартовый скрипт не найден по пути: {script_path}")
    except Exception as e:
        print(f"Непредвиденная ошибка при чтении скрипта: {e}")


# --- Главный REPL цикл (из Этапа 1) ---

def shell_emulator_repl():
    """Главный цикл Read-Eval-Print Loop (интерактивный режим)"""
    global INTERACTIVE_MODE
    INTERACTIVE_MODE = True
    
    print("\n--- Запуск в интерактивном режиме (REPL) ---")
    
    while True:
        try:
            line = input(get_prompt())
            
            exit_code = execute_command(line)
            # В REPL код завершения не влияет на продолжение цикла

        except EOFError:
            print("\nВыход из эмулятора (EOF).")
            break
        except KeyboardInterrupt:
            print("\n^C")
            continue
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

# --- Инициализация и парсинг аргументов ---

def main():
    """Основная функция, обрабатывающая аргументы и запускающая режим работы."""
    global VFS_PATH, STARTUP_SCRIPT
    
    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки (Shell Emulator). Этап 2: Конфигурация."
    )
    
    # Требование 1: Путь к VFS
    parser.add_argument(
        '--vfs_path',
        type=str,
        default='/tmp/emulator_vfs',
        help='Путь к физическому расположению Виртуальной Файловой Системы (VFS).'
    )
    
    # Требование 1: Путь к стартовому скрипту
    parser.add_argument(
        '--startup_script',
        type=str,
        default=None,
        help='Путь к стартовому скрипту для выполнения команд эмулятора.'
    )
    
    args = parser.parse_args()
    
    # Отладочный вывод всех заданных параметров (Цель этапа)
    print("\n--- Отладочный вывод параметров конфигурации ---")
    print(f"VFS Path:         {args.vfs_path}")
    print(f"Startup Script:   {args.startup_script}")
    print("---------------------------------------------")

    # Сохранение параметров в глобальные переменные
    VFS_PATH = args.vfs_path
    STARTUP_SCRIPT = args.startup_script

    # Запуск соответствующего режима
    if STARTUP_SCRIPT:
        run_startup_script()
    else:
        shell_emulator_repl()
if __name__ == "__main__":
    main()