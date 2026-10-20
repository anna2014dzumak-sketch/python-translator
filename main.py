import json
import urllib.parse
import urllib.request
from googletrans import LANGUAGES

def CodeLang(lang: str) -> str:
    if not lang:
        return "Помилка: Порожній параметр lang"

    lang_lower = str(lang).lower().strip()

    if lang_lower in LANGUAGES:
        return LANGUAGES[lang_lower].capitalize()

    for code, name in LANGUAGES.items():
        if name.lower() == lang_lower:
            return code

    return f"Помилка: Мову '{lang}' не знайдено"

def TransLate(str_text: str, lang: str) -> str:
    try:
        target_lang = str(lang).lower().strip()

        if target_lang not in LANGUAGES:
            code = CodeLang(target_lang)
            if code.startswith("Помилка"):
                return code
            target_lang = code

        url = "https://translate.googleapis.com/translate_a/single?" + urllib.parse.urlencode({
            "client": "gtx",
            "sl": "auto",
            "tl": target_lang,
            "dt": "t",
            "q": str_text
        })

        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            translated_text = "".join([part[0] for part in data[0] if part[0]])
            return translated_text

    except Exception as e:
        return f"Помилка перекладу: {str(e)}"

def LangDetect(txt: str) -> str:
    try:
        url = "https://translate.googleapis.com/translate_a/single?" + urllib.parse.urlencode({
            "client": "gtx",
            "sl": "auto",
            "tl": "en",
            "dt": "t",
            "q": txt
        })

        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            detected_lang = data[2] if len(data) > 2 else "uk"
            return f"Detected(lang={detected_lang}, confidence=1)"
    except Exception as e:
        return f"Помилка визначення мови: {str(e)}"

if __name__ == "__main__":
    txt = "Доброго дня. Як справи?"
    lang = "en"

    print(txt)
    print(LangDetect(txt))
    print(TransLate(txt, lang))
    print(CodeLang("En"))
    print(CodeLang("English"))