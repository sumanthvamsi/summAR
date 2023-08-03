from .detection import language

def transcript(path):
  print("In speech.py")
  import whisper
  lang_detected=language(path)
  if lang_detected=='en':
    model = whisper.load_model("base")
    result = model.transcribe(path)
  else:
    model = whisper.load_model("large")
    result = model.transcribe(path, language=lang_detected, task='translate', fp16=False)
  
  return result["text"]