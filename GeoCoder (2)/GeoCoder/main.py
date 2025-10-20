import asyncio
import os
import subprocess
import sys
from typing import Optional

from Source import parsing as parse
from Source.database.models import init_db


def ensure_dependencies_installed(requirements: Optional[str] = "requirements.txt") -> None:
    if requirements:
        with open(os.devnull, "wb") as devnull:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements], stdout=devnull, stderr=devnull)


def show_help():
    print("""
Доступные команды:
1 — Ввести координаты (широта и долгота)
2 — Ввести адрес (город, улица, дом)
--help — Показать справку
--example — Посмотреть примеры работы программы
exit — Выйти из программы


Примеры использования:
python main.py --help
""")

def show_examples():
    print("""
Вариант 1 - поиск координат по широте и долготе 

**Ввод**
Введите широту и долготу через пробел: 56.7928003 60.6165292

**Вывод**
Полный адрес: 1 Родонитовая улица; Екатеринбург; Свердловская область; 620089; Россия  

  
    
Вариант 2 — поиск координат по адресу

**Ввод:**
Введите город: Екатеринбург
Введите улицу: Родонитовая
Введите номер дома: 1

**Вывод:**
Полный адрес: 1 Родонитовая улица; Екатеринбург; Свердловская область; 620089; Россия
""")


async def process_command(command: str):
    if command in ("--help", "-h"):
        show_help()
    elif command in ("1", "2"):
        await parse.choose_input(command)
    elif command == "exit":
        print("Выход из программы.")
        sys.exit(0)
    else:
        print("Неизвестная команда. Введите --help для справки.")


async def interactive_mode():
    print("Добро пожаловать в Geocoder!")
    try:
        while True:
            print("\nВведите команду (или --help):")
            command = input().strip().lower()
            await process_command(command)
    except (EOFError, StopIteration):
        print("Завершение из-за окончания ввода.")
        sys.exit(0)


async def main():
    await init_db()

    if len(sys.argv) > 1:
        command = sys.argv[1].strip().lower()
        if command in ("--help", "-h"):
            show_help()
            sys.exit(0)
        elif command == "exit":
            print("Выход из программы.")
            sys.exit(0)
        elif command in ("1", "2"):
            await parse.choose_input(command)
            sys.exit(0)
        elif command == "--examples":
            print("Пример работы программы:")
            show_examples()
            sys.exit(0)
        else:
            print(f"Неизвестная команда: {command}")
            show_help()
            sys.exit(1)

    await interactive_mode()


if __name__ == '__main__':
    try:
        ensure_dependencies_installed()
    except Exception:
        pass

    asyncio.run(main())
