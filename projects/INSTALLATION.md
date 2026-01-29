# Установка и настройка GUI конвертера

## Требования

- **Python 3.7+** (рекомендуется Python 3.9+)
- **Windows** (тестировалось на Windows 10/11)
- **PySimpleGUI 5.0+**

## Установка

### Шаг 1: Проверка Python

Откройте командную строку и выполните:

```bash
python --version
```

Должна отобразиться версия Python 3.7 или выше.

### Шаг 2: Установка FreeSimpleGUI

```bash
pip install FreeSimpleGUI
```

Или если у вас есть лицензия PySimpleGUI:

```bash
pip install --upgrade --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
```

### Шаг 3: Проверка установки

```bash
python -m pip show FreeSimpleGUI
```

Должна отобразиться информация о пакете.

## Запуск

### Способ 1: Через .cmd файл (рекомендуется)

Двойной клик по файлу:
```
run_gui.cmd
```

### Способ 2: Через командную строку

```bash
cd f:\1C\Projects\1CFilesConverter\projects
python converter_gui.py
```

### Способ 3: Через Python напрямую

```bash
python f:\1C\Projects\1CFilesConverter\projects\converter_gui.py
```

## Структура файлов

```
projects/
├── converter_gui.py          # Главный файл GUI (520+ строк)
├── run_gui.cmd              # Скрипт запуска
├── convert.py               # Скрипт конвертации
├── base.env                 # Базовые настройки
├── GUI_README.md            # Подробная документация
├── QUICK_START.md           # Краткая инструкция
├── INSTALLATION.md          # Этот файл
├── CHANGELOG_GUI.md         # История изменений
└── [папки проектов]/
    ├── *.env                # Настройки проекта
    └── *.cmd                # Скрипт конвертации
```

## Проверка работоспособности

После запуска GUI должно открыться окно с:
- Заголовком: "1C Files Converter - Cyberpunk Edition | Версия 1.0"
- Темным фоном с неоново-синими элементами
- Таблицей проектов (если есть проекты с .env файлами)
- Двумя вкладками: "Проекты" и "Лог выполнения"

## Устранение проблем

### Ошибка: "python не является внутренней или внешней командой"

**Решение**: Добавьте Python в PATH или используйте полный путь к python.exe

### Ошибка: "No module named 'PySimpleGUI'" или "No module named 'FreeSimpleGUI'"

**Решение**: Установите FreeSimpleGUI:
```bash
pip install FreeSimpleGUI
```

### Ошибка: "Не найден скрипт convert.py"

**Решение**: Убедитесь, что файл `convert.py` находится в той же папке, что и `converter_gui.py`

### GUI не отображает проекты

**Причины**:
1. В подпапках `projects/` нет .env файлов
2. В подпапках нет .cmd файлов
3. Неправильная структура папок

**Решение**: Проверьте структуру проектов. Каждый проект должен быть в отдельной подпапке и содержать:
- Хотя бы один .env файл
- Хотя бы один .cmd файл

### Кодировка в логе отображается неправильно

**Решение**: Это нормально для Windows. Скрипт использует кодировку CP1251 для subprocess.

## Обновление

Для обновления GUI:
1. Скачайте новую версию `converter_gui.py`
2. Замените старый файл
3. Проверьте `CHANGELOG_GUI.md` для информации об изменениях

## Удаление

Для удаления GUI:
1. Удалите файлы:
   - `converter_gui.py`
   - `run_gui.cmd`
   - `GUI_README.md`
   - `QUICK_START.md`
   - `INSTALLATION.md`
   - `CHANGELOG_GUI.md`
2. (Опционально) Удалите FreeSimpleGUI:
   ```bash
   pip uninstall FreeSimpleGUI
   ```

## Поддержка

При возникновении проблем:
1. Проверьте `GUI_README.md` для подробной документации
2. Проверьте `CHANGELOG_GUI.md` для известных проблем
3. Убедитесь, что используете последнюю версию Python и PySimpleGUI

## Лицензия

См. файл LICENSE в корне проекта.
