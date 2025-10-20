import requests
from typing import Optional

from Source import parsing as parse
from Source.database.requests import return_address_if_exist
from Source.utils import DEFAULT_HEADERS, NOMINATIM_URL


async def send_request(address: str) -> None:
    headers = DEFAULT_HEADERS
    params = {"q": address, "format": "json", "limit": 1, "accept-language": "ru", "addressdetails": 1}

    cached = await return_address_if_exist(address)
    if cached is not None:
        print(f"Полный адрес: {cached.full_address}")
        return

    try:
        resp = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
    except Exception as exc:
        print(f"Ошибка запроса: {exc}")
        return

    if not resp.ok:
        print(f"Ошибка HTTP: {resp.status_code}")
        return

    try:
        data = resp.json()
    except ValueError:
        print("Некорректный JSON в ответе")
        return

    if not data:
        print("Адрес не найден")
        return

    await parse.parse_output_address(address, data[0])
