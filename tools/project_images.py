import hashlib

IMAGE_POOL = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/ESP32-DevKitC_V4.jpg/640px-ESP32-DevKitC_V4.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/ESP32-WROOM-32.jpg/640px-ESP32-WROOM-32.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/NodeMCU_DEVKIT_1.0.jpg/640px-NodeMCU_DEVKIT_1.0.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Arduino_Uno_-_R3.jpg/640px-Arduino_Uno_-_R3.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Breadboard.jpg/640px-Breadboard.jpg",
    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1587620962725-abab9fe773d5?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1581093450032-e7072d391b8a?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1581094790499-2039b1221368?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1555949963-aa79d0869115?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1574717024650-f976712b7010?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1558002032-1097d11f3094?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1515378969642-b61ce369882b?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1550751827-4bd374c3d58d?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1535223398730-b9f2a67c2b08?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1517694712202-14dd953757aa?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1591797522362-eecc697fb423?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1461745500616-9c827dcf673e?w=640&h=360&fit=crop&q=80",
    "https://images.unsplash.com/photo-1581092162384-8987c1d64708?w=640&h=360&fit=crop&q=80",
]


def pick_image(slug: str) -> str:
    h = int(hashlib.md5(slug.encode("utf-8")).hexdigest(), 16)
    return IMAGE_POOL[h % len(IMAGE_POOL)]
