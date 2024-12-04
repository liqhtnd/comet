import base64
import orjson

from RTN import SettingsModel, BestRanking, ParsedData

from comet.utils.models import ConfigModel, default_config


def config_check(b64config: str):
    try:
        config = orjson.loads(base64.b64decode(b64config).decode())
        validated_config = ConfigModel(**config)
        validated_config = validated_config.model_dump()
        validated_config["rtnSettings"] = SettingsModel(
            **validated_config["rtnSettings"]
        )
        validated_config["rtnRanking"] = BestRanking(**validated_config["rtnRanking"])
        return validated_config
    except:
        return default_config  # if it doesn't pass, return default config


def bytes_to_size(bytes: int):
    sizes = ["Bytes", "KB", "MB", "GB", "TB"]
    if bytes == 0:
        return "0 Byte"

    i = 0
    while bytes >= 1024 and i < len(sizes) - 1:
        bytes /= 1024
        i += 1

    return f"{round(bytes, 2)} {sizes[i]}"


def size_to_bytes(size_str: str):
    sizes = ["bytes", "kb", "mb", "gb", "tb"]

    value, unit = size_str.split()
    value = float(value)
    unit = unit.lower()

    if unit not in sizes:
        return None

    multiplier = 1024 ** sizes.index(unit)
    return int(value * multiplier)


languages_emojis = {
    "unknown": "❓",  # Unknown
    "multi": "🌎",  # Dubbed
    "en": "🇬🇧",  # English
    "ja": "🇯🇵",  # Japanese
    "zh": "🇨🇳",  # Chinese
    "ru": "🇷🇺",  # Russian
    "ar": "🇸🇦",  # Arabic
    "pt": "🇵🇹",  # Portuguese
    "es": "🇪🇸",  # Spanish
    "fr": "🇫🇷",  # French
    "de": "🇩🇪",  # German
    "it": "🇮🇹",  # Italian
    "ko": "🇰🇷",  # Korean
    "hi": "🇮🇳",  # Hindi
    "bn": "🇧🇩",  # Bengali
    "pa": "🇵🇰",  # Punjabi
    "mr": "🇮🇳",  # Marathi
    "gu": "🇮🇳",  # Gujarati
    "ta": "🇮🇳",  # Tamil
    "te": "🇮🇳",  # Telugu
    "kn": "🇮🇳",  # Kannada
    "ml": "🇮🇳",  # Malayalam
    "th": "🇹🇭",  # Thai
    "vi": "🇻🇳",  # Vietnamese
    "id": "🇮🇩",  # Indonesian
    "tr": "🇹🇷",  # Turkish
    "he": "🇮🇱",  # Hebrew
    "fa": "🇮🇷",  # Persian
    "uk": "🇺🇦",  # Ukrainian
    "el": "🇬🇷",  # Greek
    "lt": "🇱🇹",  # Lithuanian
    "lv": "🇱🇻",  # Latvian
    "et": "🇪🇪",  # Estonian
    "pl": "🇵🇱",  # Polish
    "cs": "🇨🇿",  # Czech
    "sk": "🇸🇰",  # Slovak
    "hu": "🇭🇺",  # Hungarian
    "ro": "🇷🇴",  # Romanian
    "bg": "🇧🇬",  # Bulgarian
    "sr": "🇷🇸",  # Serbian
    "hr": "🇭🇷",  # Croatian
    "sl": "🇸🇮",  # Slovenian
    "nl": "🇳🇱",  # Dutch
    "da": "🇩🇰",  # Danish
    "fi": "🇫🇮",  # Finnish
    "sv": "🇸🇪",  # Swedish
    "no": "🇳🇴",  # Norwegian
    "ms": "🇲🇾",  # Malay
    "la": "💃🏻",  # Latino
}


def get_language_emoji(language: str):
    language_formatted = language.lower()
    return (
        languages_emojis[language_formatted]
        if language_formatted in languages_emojis
        else language
    )


def format_metadata(data: ParsedData):
    extras = []
    if data.quality:
        extras.append(data.quality)
    if data.hdr:
        extras.extend(data.hdr)
    if data.codec:
        extras.append(data.codec)
    if data.audio:
        extras.extend(data.audio)
    if data.channels:
        extras.extend(data.channels)
    if data.bit_depth:
        extras.append(data.bit_depth)
    if data.network:
        extras.append(data.network)
    if data.group:
        extras.append(data.group)

    return "|".join(extras)


def format_title(
    data: ParsedData, seeders: int, size: int, tracker: str, result_format: list
):
    has_all = "all" in result_format

    title = ""
    if has_all or "title" in result_format:
        title += f"{data.raw_title}\n"

    if has_all or "metadata" in result_format:
        metadata = format_metadata(data)
        if metadata != "":
            title += f"💿 {metadata}\n"

    if (has_all or "seeders" in result_format) and seeders is not None:
        title += f"👤 {seeders} "

    if has_all or "size" in result_format:
        title += f"💾 {bytes_to_size(size)} "

    if has_all or "tracker" in result_format:
        title += f"🔎 {tracker}"

    if has_all or "languages" in result_format:
        languages = data.languages
        if data.dubbed:
            languages.insert(0, "multi")
        if languages:
            formatted_languages = "/".join(
                get_language_emoji(language) for language in languages
            )
            languages_str = "\n" + formatted_languages
            title += f"{languages_str}"

    if title == "":
        # Without this, Streamio shows SD as the result, which is confusing
        title = "Empty result format configuration"

    return title
