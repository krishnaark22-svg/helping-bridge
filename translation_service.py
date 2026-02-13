from googletrans import Translator
LANG_CODES={
    'Hindi':'hi',
    'Malayalam':'ml',
    'Tamil':'ta',
    'Telegu':'te',
    'English':'en'
}
def translate_text(text,target_lang_name):
    try:
        if target_lang_name=='English':
            return text
        translator=Translator()
        target_code=LANG_CODES.get(target_lang_name,'en')
        translation=translator.translate(text,dest=target_code)
        return translation.text
    except Exception as e:
        print(f"Translation error:{e}")
        return text
