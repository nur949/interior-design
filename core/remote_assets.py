from pathlib import Path

HERO_IMAGE_URL = "https://cdn.pixabay.com/photo/2017/08/27/10/16/interior-2685521_1280.jpg"

BLOG_IMAGE_URLS = [
    "https://cdn.pixabay.com/photo/2017/08/07/16/39/living-room-2605530_1280.jpg",
    "https://cdn.pixabay.com/photo/2017/08/27/10/16/interior-2685521_1280.jpg",
    "https://cdn.pixabay.com/photo/2017/09/09/18/25/living-room-2732939_640.jpg",
    "https://cdn.pixabay.com/photo/2016/11/22/23/38/apartment-1851201_640.jpg",
    "https://cdn.pixabay.com/photo/2020/01/20/10/33/room-4779953_640.jpg",
    "https://cdn.pixabay.com/photo/2024/02/06/15/40/living-room-8557308_640.jpg",
    "https://cdn.pixabay.com/photo/2014/07/21/19/20/lobby-398845_1280.jpg",
    "https://cdn.pixabay.com/photo/2024/01/30/09/19/hotel-8541580_1280.jpg",
]

FURNITURE_IMAGE_URLS = [
    "https://cdn.pixabay.com/photo/2019/05/12/20/58/hotel-4199113_640.jpg",
    "https://cdn.pixabay.com/photo/2017/03/19/01/43/living-room-2155376_640.jpg",
    "https://cdn.pixabay.com/photo/2017/08/06/01/49/table-2587598_640.jpg",
    "https://cdn.pixabay.com/photo/2017/08/07/16/39/living-room-2605530_1280.jpg",
    "https://cdn.pixabay.com/photo/2017/09/09/18/25/living-room-2732939_640.jpg",
    "https://cdn.pixabay.com/photo/2024/02/06/15/40/living-room-8557308_640.jpg",
    "https://cdn.pixabay.com/photo/2015/06/19/16/30/lobby-815062_1280.jpg",
    "https://cdn.pixabay.com/photo/2014/07/21/19/20/lobby-398845_1280.jpg",
]

PROJECT_IMAGE_URLS = [
    "https://cdn.pixabay.com/photo/2017/08/27/10/16/interior-2685521_1280.jpg",
    "https://cdn.pixabay.com/photo/2014/07/21/19/20/lobby-398845_1280.jpg",
    "https://cdn.pixabay.com/photo/2015/06/19/16/30/lobby-815062_1280.jpg",
    "https://cdn.pixabay.com/photo/2024/01/30/09/19/hotel-8541580_1280.jpg",
    "https://cdn.pixabay.com/photo/2022/08/09/04/08/hotel-7374082_640.jpg",
    "https://cdn.pixabay.com/photo/2013/09/25/12/27/reception-186102_640.jpg",
]


def _stable_index(key: str, size: int) -> int:
    if size <= 0:
        return 0
    return sum(ord(char) for char in (key or "")) % size


def _fallback_url(field) -> str:
    try:
        return field.url
    except Exception:
        return ""


def attach_image_url(obj, urls, image_field_name, target_attr="display_image_url"):
    source_key = getattr(obj, "slug", None) or getattr(obj, "title", None) or str(getattr(obj, "pk", ""))
    remote_url = urls[_stable_index(str(source_key), len(urls))] if urls else ""
    fallback = _fallback_url(getattr(obj, image_field_name, None)) if hasattr(obj, image_field_name) else ""
    setattr(obj, target_attr, remote_url or fallback)
    return obj


def attach_many(objects, urls, image_field_name, target_attr="display_image_url"):
    for obj in objects:
        attach_image_url(obj, urls, image_field_name, target_attr=target_attr)
    return objects
