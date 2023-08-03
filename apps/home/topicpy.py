def topic(text):
    text = text.lower()
    if 'chest pain' in text:
        a= 'Heart Problem'
    elif 'stomach pain' in text:
        a= 'Kidney Problem'
    elif 'knee pain' in text:
        a= 'Knee Problem'
    elif 'rash' in text:
        a= 'Skin Problem'
    elif 'have diabetes' in text:
        a= 'Diabetes'
    elif 'bladder' in text:
        a= 'Urinary Problem'
    elif 'breathlessness' in text:
        a= 'Asthma'
    elif 'abdomen' in text:
        a= 'Stomach Pain'
    elif 'fibromyalgia' in text:
        a= 'Muscle Problem'
    elif 'diarrhea' in text:
        a= 'Diarrhea'
    return a
    
