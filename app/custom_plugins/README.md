# Документация по написанию плагинов для бота на базе `aiogram`

Эта документация описывает структуру и подходы для разработки плагинов в рамках архитектуры, где используются `aiogram` версии 3.x, модули для разделения логики и автоматическая регистрация плагинов.

---

## Основы архитектуры плагинов

Плагин — это независимый модуль, который расширяет функциональность бота. Каждый плагин:

1. Хранится в папке `app/plugins`.
2. Представляет собой отдельный Python-модуль.
3. Содержит маршрутизатор `Router` для регистрации обработчиков.
4. (Опционально) Имеет фоновую задачу или другие вспомогательные функции.

---

## Структура плагина

Плагин представляет собой файл `.py` со следующими основными элементами:

1. **Документация в начале файла:** 
    Описание плагина, версия, и краткое пояснение.
2. **Импорт модулей:**
    Используйте только необходимые модули, такие как `aiogram`, стандартные библиотеки Python или функции из проекта.
3. **Объявление `Router`:**
    Каждый плагин должен содержать переменную `router` для регистрации обработчиков.
4. **Обработчики:**
    Основная логика плагина, например команды, фильтры, ответы на сообщения.
5. **Дополнительные функции:**
    Вспомогательная логика или задачи, запускаемые при старте.

---

### Пример плагина

#### `app/plugins/example_plugin.py`
```python
"""
Plugin: example_plugin
Version: 1.0.0
Description: Example plugin that demonstrates basic structure.
"""

from aiogram import Router
from aiogram.types import Message

# Create a router
router = Router()

@router.message(commands=["hello"])
async def hello_command(message: Message):
    """
    name: hello
    description: Responds with a greeting message when the user sends /hello.
    """
    await message.answer("Hello! This is an example plugin.")
```

---

## Обязательные элементы плагина

### 1. **Имя файла**
Имя файла плагина должно соответствовать следующим правилам:
- Использовать только латиницу, цифры и символ `_`.
- Начинаться с буквы.
- Например: `my_plugin.py`, `weather_bot.py`.

### 2. **Документация в начале**
Каждый плагин должен содержать краткое описание в формате многострочного комментария:
```python
"""
Plugin: plugin_name
Version: x.y.z
Description: Short description of the plugin's purpose.
"""
```

### 3. **Объявление маршрутизатора**
Переменная `router` обязательна для автоматической регистрации обработчиков:
```python
from aiogram import Router

router = Router()
```

### 4. **Обработчики**
Обработчики — это функции, которые реагируют на события, такие как команды или текстовые сообщения. Пример команды:
```python
@router.message(commands=["example"])
async def example_command(message: Message):
    """
    name: example
    description: Responds to the /example command.
    """
    await message.answer("This is an example command.")
```

---

## Расширенные возможности

### Фоновые задачи
Для выполнения задач в фоновом режиме, например, ежедневных уведомлений, используйте модуль `asyncio`:
```python
import asyncio

async def background_task():
    while True:
        print("Running background task...")
        await asyncio.sleep(3600)  # Run every hour
```

Для запуска задачи при старте бота:
```python
async def on_startup(bot):
    asyncio.create_task(background_task())
```

---

## Рекомендации

1. **Декомпозиция логики:**
    - Сложные плагины разбивайте на несколько функций.
    - Используйте модули из папок `utils`, `db` и других.

2. **Валидация данных:**
    - Проверяйте входные данные от пользователей.
    - Используйте фильтры, такие как `commands` и `text`.

3. **Логирование:**
    - Логируйте действия и ошибки для удобства отладки.
    - Используйте логгер:
      ```python
      import logging
      logger = logging.getLogger("plugin_name")
      logger.info("Plugin loaded.")
      ```

4. **Тестирование:**
    - Тестируйте плагины отдельно перед добавлением их в проект.

---

## Полезные команды для разработчиков

- **Создание нового плагина:**
  Скопируйте шаблон и измените название/логику:
  ```bash
  cp app/plugins/example_plugin.py app/plugins/my_plugin.py
  ```

- **Логирование:**
  Запустите бота с подробными логами:
  ```bash
  python main.py --log=DEBUG
  ```

- **Отладка маршрутов:**
  Убедитесь, что маршруты зарегистрированы корректно:
  ```python
  print(router.handlers)
  ```

---

## Часто задаваемые вопросы (FAQ)

### 1. **Как передать данные из основного бота в плагин?**
Используйте объект `Dispatcher` для передачи параметров:
```python
async def on_startup(dispatcher: Dispatcher):
    dispatcher["my_data"] = "some_value"
```
В плагине:
```python
dispatcher["my_data"]
```

### 2. **Как загрузить внешний API или базу данных в плагине?**
Инициализируйте подключение при старте:
```python
from app.utils.database import db_session

@router.message(commands=["data"])
async def get_data(message: Message):
    data = db_session.query(MyModel).all()
    await message.answer(f"Data: {data}")
```

### 3. **Как отладить ошибки загрузки плагинов?**
Проверьте логи загрузчика плагинов. Если есть ошибка, она будет видна:
```
[ERROR] - plugin_loader - Error loading plugin my_plugin: ImportError
```

---

## Итоговая структура папки `plugins`

```
app/
└── plugins/
    ├── __init__.py        # Загрузчик плагинов
    ├── example_plugin.py  # Пример плагина
    ├── my_plugin.py       # Ваш новый плагин
    └── ...
```

---

## Шаблон плагина

Для упрощения работы, вот готовый шаблон плагина:

```python
"""
Plugin: plugin_name
Version: 1.0.0
Description: Short description of the plugin.
"""

from aiogram import Router
from aiogram.types import Message

# Create router
router = Router()

@router.message(commands=["example"])
async def example_command(message: Message):
    """
    name: example
    description: Example command that replies to /example.
    """
    await message.answer("This is a reply from the plugin.")
```
