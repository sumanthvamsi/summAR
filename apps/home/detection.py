def language(path):
  print("In detection.py")
      
  import whisper

  model = whisper.load_model("base")

  # load audio and pad/trim it to fit 30 seconds
  audio = whisper.load_audio(path)
  audio = whisper.pad_or_trim(audio)

  # make log-Mel spectrogram and move to the same device as the model
  mel = whisper.log_mel_spectrogram(audio).to(model.device)

  # detect the spoken language
  _, probs = model.detect_language(mel)
  lang_detected=max(probs, key=probs.get)
  return lang_detected