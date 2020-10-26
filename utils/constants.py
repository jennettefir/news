DEEPL_ENGINE = "deepl"
GOOGLE_ENGINE = "google"
BING_ENGINE = "bing"

DEFAULT_SEQUENCE = [
    {
        "source": "EN",
        "target": "DE",
        "engine": BING_ENGINE
    },
    {
        "source": "DE",
        "target": "ES",
        "engine": GOOGLE_ENGINE
    },
    {
        "source": "ES",
        "target": "DE",
        "engine": BING_ENGINE
    },
    {
        "source": "DE",
        "target": "EN",
        "engine": GOOGLE_ENGINE
    },
]
