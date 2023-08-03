from .detection import language

def final(input,path):
    print("In translate.py")
    from googletrans import Translator
    lang=language(path)
    if lang!='en':
        k=Translator()
        output=k.translate(input,src='en',dest=lang).text
    else:
        output=input
    return output