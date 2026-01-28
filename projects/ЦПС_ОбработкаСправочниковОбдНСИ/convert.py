#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт конвертации обработки 1С из EDT в EPF формат
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


# ANSI цветовые коды для Windows
class Colors:
    """Цветовые коды для консоли"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    
    @staticmethod
    def enable_windows_colors():
        """Включает поддержку ANSI цветов в Windows"""
        if sys.platform == 'win32':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except Exception:
                pass


def print_info(message):
    """Выводит информационное сообщение зеленым цветом"""
    print(f"{Colors.GREEN}[INFO]{Colors.RESET} {message}")


def print_error(message):
    """Выводит сообщение об ошибке красным цветом"""
    print(f"{Colors.RED}[ERROR]{Colors.RESET} {message}")


def print_warning(message):
    """Выводит предупреждение желтым цветом"""
    print(f"{Colors.YELLOW}[WARNING]{Colors.RESET} {message}")


def print_success(message):
    """Выводит сообщение об успехе зеленым цветом"""
    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {message}")


def load_env_file(env_path):
    """
    Загружает переменные из .env файла
    
    Args:
        env_path: путь к .env файлу
        
    Returns:
        dict: словарь с переменными окружения
    """
    env_vars = {}
    
    if not os.path.exists(env_path):
        print_error(f"Файл .env не найден: {env_path}")
        return None
    
    print_info(f"Чтение переменных окружения из: {env_path}")
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                # Убираем кавычки если есть
                value = value.strip('"').strip("'")
                env_vars[key.strip()] = value
    
    return env_vars


def find_env_files(path):
    """
    Находит .env файлы по указанному пути
    
    Args:
        path: путь к .env файлу или каталогу с .env файлами
        
    Returns:
        list: список путей к найденным .env файлам
    """
    path = Path(path)
    
    # Если это файл, возвращаем его
    if path.is_file():
        if path.suffix == '.env' or path.name.endswith('.env'):
            return [str(path)]
        else:
            print_error(f"Файл {path} не является .env файлом")
            return []
    
    # Если это каталог, ищем все .env файлы
    if path.is_dir():
        env_files = sorted(path.glob('*.env'))
        if env_files:
            print_info(f"Найдено {len(env_files)} .env файлов в каталоге {path}:")
            for env_file in env_files:
                print_info(f"  - {env_file.name}")
            return [str(f) for f in env_files]
        else:
            print_error(f"Не найдено .env файлов в каталоге {path}")
            return []
    
    print_error(f"Путь не существует: {path}")
    return []


def merge_env_files(env_files):
    """
    Объединяет несколько .env файлов в один словарь
    Последующие файлы переопределяют значения из предыдущих
    
    Args:
        env_files: список путей к .env файлам
        
    Returns:
        dict: объединенный словарь с переменными окружения
    """
    merged_vars = {}
    
    for env_file in env_files:
        env_vars = load_env_file(env_file)
        if env_vars is None:
            return None
        # Объединяем, переопределяя существующие значения
        merged_vars.update(env_vars)
    
    if len(env_files) > 1:
        print_info(f"Объединено {len(env_files)} файлов конфигурации")
    
    return merged_vars


def run_conversion(env_files, output_path=None):
    """
    Запускает конвертацию обработки
    
    Args:
        env_files: список путей к .env файлам или один путь
        output_path: путь для сохранения EPF (опционально)
        
    Returns:
        int: код возврата (0 - успех, 1 - ошибка)
    """
    # Преобразуем в список если передан один файл
    if isinstance(env_files, str):
        env_files = [env_files]
    
    # Получаем абсолютные пути к .env файлам
    env_files = [os.path.abspath(f) for f in env_files]
    
    # Загружаем и объединяем переменные из всех .env файлов
    env_vars = merge_env_files(env_files)
    if env_vars is None:
        return 1
    
    # Получаем путь к скрипту из переменной ScriptName или используем dp2epf.cmd по умолчанию
    script_name = env_vars.get('ScriptName', 'dp2epf.cmd')
    script_dir = Path(__file__).parent
    conversion_script = script_dir / script_name
    
    if not conversion_script.exists():
        print_error(f"Скрипт {script_name} не найден: {conversion_script}")
        return 1
    
    print_info(f"Используется скрипт конвертации: {script_name}")
    
    # Получаем пути из переменных окружения
    src_path = env_vars.get('V8_SRC_PATH', '')
    dst_path = env_vars.get('V8_DST_PATH', '')
    
    # Если передан output_path, используем его вместо V8_DST_PATH
    if output_path:
        dst_path = os.path.abspath(output_path)
        print_info(f"Используется переданный путь назначения: {dst_path}")
        # Обновляем переменную в .env файле временно
        env_vars['V8_DST_PATH'] = dst_path
    
    if not src_path:
        print_error("Переменная V8_SRC_PATH не определена в .env файле")
        return 1
    
    if not dst_path:
        print_error("Путь назначения не указан (V8_DST_PATH в .env или параметр --output)")
        return 1
    
    # Создаем каталог назначения если не существует
    os.makedirs(dst_path, exist_ok=True)
    print_info(f"Каталог назначения: {dst_path}")
    
    # Создаем временный .env файл с объединенными настройками
    import tempfile
    temp_fd, temp_env_file = tempfile.mkstemp(suffix='.env', text=True)
    try:
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
            for key, value in env_vars.items():
                # Пропускаем служебную переменную ScriptName
                if key == 'ScriptName':
                    continue
                # Добавляем кавычки для путей с пробелами
                if ' ' in value and not (value.startswith('"') and value.endswith('"')):
                    value = f'"{value}"'
                f.write(f'{key}={value}\n')
        print_info("Создан временный объединенный .env файл")
    except Exception as e:
        print_error(f"Ошибка создания временного .env: {e}")
        return 1
    
    # Формируем команду для запуска
    cmd = [
        'cmd.exe',
        '/c',
        str(conversion_script),
        '',  # первый параметр пустой (путь источника берется из .env)
        '',  # второй параметр пустой (путь назначения берется из .env)
        temp_env_file  # третий параметр - путь к временному объединенному .env
    ]
    
    print_info("Запуск конвертации...")
    print_info(f"Источник: {src_path}")
    print_info(f"Назначение: {dst_path}")
    
    # Запускаем процесс конвертации
    try:
        result = subprocess.run(
            cmd,
            cwd=str(script_dir),
            encoding='cp1251',
            errors='replace'
        )
        
        # Удаляем временный файл
        try:
            os.unlink(temp_env_file)
            print_info("Временный .env файл удален")
        except Exception as e:
            print_warning(f"Не удалось удалить временный файл: {e}")
        
        if result.returncode == 0:
            # Определяем имя EPF файла из пути источника
            epf_name = Path(src_path).name + '.epf'
            epf_path = Path(dst_path) / epf_name
            
            if epf_path.exists():
                print()
                print_success(f"Обработка успешно сконвертирована: {epf_path}")
                print_info(f"Размер файла: {epf_path.stat().st_size:,} байт")
            else:
                print()
                print_warning(f"Конвертация завершена, но файл не найден: {epf_path}")
            
            return 0
        else:
            print()
            print_error(f"Ошибка конвертации (код возврата: {result.returncode})")
            return 1
            
    except Exception as e:
        print_error(f"Исключение при выполнении конвертации: {e}")
        return 1


def main():
    """Главная функция"""
    # Включаем поддержку цветов в Windows
    Colors.enable_windows_colors()
    
    parser = argparse.ArgumentParser(
        description='Конвертация обработки 1С из EDT в EPF формат',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python convert.py
  python convert.py --env base.env
  python convert.py --env .
  python convert.py --env ../configs
  python convert.py --env base.env --env config.env
  python convert.py --env . --output f:\\1C\\Projects\\build
        """
    )
    
    parser.add_argument(
        '-e', '--env',
        action='append',
        dest='env_paths',
        help='Путь к .env файлу или каталогу с .env файлами (можно указать несколько раз)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Путь для сохранения EPF файла (опционально, переопределяет V8_DST_PATH из .env)'
    )
    
    args = parser.parse_args()
    
    # Собираем все .env файлы
    all_env_files = []
    
    if not args.env_paths:
        # Если пути не указаны, ищем в папке скрипта
        script_dir = Path(__file__).parent
        print_info(f"Параметр --env не указан, поиск .env файлов в: {script_dir}")
        env_files = find_env_files(script_dir)
        
        if not env_files:
            # Пробуем найти .env по умолчанию
            default_env = script_dir / '.env'
            if default_env.exists():
                env_files = [str(default_env)]
                print_info(f"Используется файл по умолчанию: .env")
            else:
                print_error("Не найдено ни одного .env файла")
                sys.exit(1)
        
        all_env_files.extend(env_files)
    else:
        # Обрабатываем каждый указанный путь
        for env_path in args.env_paths:
            # Преобразуем относительный путь в абсолютный
            if not os.path.isabs(env_path):
                env_path = os.path.join(os.getcwd(), env_path)
            
            env_files = find_env_files(env_path)
            if not env_files:
                print_error(f"Не удалось найти .env файлы по пути: {env_path}")
                sys.exit(1)
            
            all_env_files.extend(env_files)
    
    if not all_env_files:
        print_error("Не найдено ни одного .env файла для обработки")
        sys.exit(1)
    
    # Запускаем конвертацию
    exit_code = run_conversion(all_env_files, args.output)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
