import asyncio
import os
from typing import Optional, Dict

from Source import response as req
from Source.database.requests import add_new_address
from Source.utils import build_address_from_components
from dotenv import load_dotenv

load_dotenv()

try:
    from dadata import Dadata

    token = os.getenv("token")
    secret = os.getenv("secret")
    dadata = Dadata(token, secret)
except ModuleNotFoundError:
    class _StubDadata:
        def clean(self, *_args, **_kwargs):
            raise RuntimeError("dadata is not installed")

    dadata = _StubDadata()


def clean_address(address: str) -> Optional[Dict]:
    try:
        return dadata.clean("address", address)
    except Exception as exc:
        print(f"[Ошибка Dadata] Не удалось очистить адрес: {exc}")
        return None


def build_normalized_address(cleaned_data: Dict) -> Optional[str]:
    if not isinstance(cleaned_data, dict) or not cleaned_data:
        print("Не удалось построить нормализованный адрес — данные отсутствуют")
        return None

    parts = []
    for key in ("street", "house", "city", "region", "country"):
        v = cleaned_data.get(key)
        if v:
            parts.append(v)

    if not parts:
        print("Не удалось построить нормализованный адрес — все поля пусты")
        return None

    return " ".join(parts)


async def parse_input_address() -> None:
    try:
        city = sanitize_input(input("Введите город: "))
        street = sanitize_input(input("Введите улицу: "))
        number = sanitize_input(input("Введите номер дома: "))
        address = f"{street} {number} {city} Россия"

        cleaned = clean_address(address)
        if not cleaned:
            print("Нормализация адреса не удалась")
            return

        normalized = build_normalized_address(cleaned)
        if not normalized:
            print("Не удалось собрать адрес из полученных данных")
            return

        await req.send_request(normalized)

    except Exception as exc:
        print(f"[Ошибка ввода] {exc}")


async def parse_input_coordinates() -> None:
    try:
        coords = input("Введите широту и долготу через пробел: ").strip().split()
        if len(coords) != 2:
            raise ValueError("Нужно ввести две координаты")

        lat, lon = float(coords[0]), float(coords[1])
        await req.send_request(f"{lat} {lon}")

    except ValueError:
        print("Координаты должны быть числами (пример: 55.7558 37.6173)")
    except Exception as exc:
        print(f"[Ошибка координат] {exc}")


async def parse_output_address(input_address: str, output_address: Dict) -> None:
    if not output_address:
        print("Пустой ответ от геокодера")
        return

    address_obj = output_address.get("address") or {}
    lat = output_address.get("lat")
    lon = output_address.get("lon")

    full_address = build_address_from_components(address_obj) or output_address.get("display_name")

    if not all([full_address, lat, lon]):
        print("Отсутствуют необходимые данные в ответе")
        return

    country = address_obj.get("country")
    if country:
        if country != "Россия" and not country.endswith("Россия"):
            print("Адрес не находится в России")
            return
    else:
        if not full_address or not full_address.endswith("Россия"):
            print("Адрес не находится в России")
            return

    try:
        await add_new_address(input_address, full_address, lat, lon)
    except Exception as exc:
        print(f"[Ошибка записи в БД] {exc}")
        return

    print(f"Широта: {lat}\nДолгота: {lon}\nПолный адрес: {full_address}")


def sanitize_input(text: str) -> str:
    normalized = text.encode("utf-8", errors="ignore").decode("utf-8").strip().lower()
    return normalized if normalized else None


async def choose_input(choice: str) -> None:
    try:
        if choice == "1":
            await parse_input_coordinates()
        elif choice == "2":
            await parse_input_address()
        else:
            print("Введите 1 (координаты) или 2 (адрес)")
    except Exception as exc:
        print(f"[Ошибка выбора] {exc}")
