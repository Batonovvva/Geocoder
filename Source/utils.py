from typing import Dict, List, Optional

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
DEFAULT_HEADERS = {"User-Agent": "MyGeocoderApp/1.0 (platonovae50@gmail.com)"}


def build_address_from_components(address_obj: Dict[str, str], include: Optional[List[str]] = None) -> Optional[str]:
    if not address_obj:
        return None

    def pick(*keys):
        for k in keys:
            v = address_obj.get(k)
            if v:
                return v
        return None

    house = pick("house_number", "house")
    road = pick("road", "street", "residential")
    city = pick("city", "town", "village")
    region = pick("state", "region")
    postcode = pick("postcode")
    country = pick("country")

    parts: List[str] = []
    if house and road:
        parts.append(f"{house} {road}")
    elif road:
        parts.append(road)
    if city:
        parts.append(city)
    if region:
        parts.append(region)
    if postcode:
        parts.append(postcode)
    if country:
        parts.append(country)

    return "; ".join(parts) if parts else None
