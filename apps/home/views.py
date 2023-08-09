# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from .extract import extract_audio
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.conf import settings
from .forms import vidForm,summForm,forumForm,cloudForm
from .models import summary_file,meta_video
from django.shortcuts import render
from .reading import read
from .topicpy import topic
from .keywords import key
from .summary import bart
import os
from .file import combine
from .sentiment import get_sentiment_score
from .speech import transcript
from .final_translate import final
from .duration import get_audio_duration
from .cloud_upload import main
from .cloud_retrieve import retrieve_files_with_contents_from_s3
import time
import datetime
from .keysentences import key_sentences



def cloud_retrieval(request):   
    form = cloudForm(request.POST or None)
    print(form.is_valid())
    print(form.errors)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        name=obj.p_name
        name=name.upper()
        num=obj.p_num
        
        folder_name = f'{name}_{num}'  
        contents=[]
        dates=[]
        tempc=1

        files_with_contents,summary_content= retrieve_files_with_contents_from_s3(folder_name)
        print("Files retrieved:")
        for file_info in files_with_contents:
            file_path, file_content, date_uploaded = file_info
            print(f"File: {file_path}, Date Uploaded: {date_uploaded}")
            if tempc%2==0:
                v=file_path.split("/")[1]
                dates.append(v.split("_")[0])
                print(dates)
            tempc+=1
            contents.append(file_content)
            print("-" * 50)
            time.sleep(1)
        summary_text=""
        for c in summary_content:
            summary_text+=c
        # Specify the directory path within Django's MEDIA_ROOT to save the files
        # local_directory = 'C:/Users/sumit/Summarizer/apps/static/assets/audio'
        base = os.path.dirname(os.path.abspath(__file__))
        base=base[:-4]
        base=base.replace("\\","/")
        print(base)
        local_directory = f'{base}/static/assets/audio/'

        # Create the local directory if it doesn't exist
        if not os.path.exists(local_directory):
            os.makedirs(local_directory)

        # Move the files from the temporary directory to the specified local directory
        downloaded_files = []
        for file_info in files_with_contents:
            file_path, _, _ = file_info
            if file_path.endswith('.mp3') or file_path.endswith('.mp4'):
                filename = os.path.basename(file_path)
                local_file_path = os.path.join(local_directory, filename)
                os.rename(file_path, local_file_path)
                downloaded_files.append(local_file_path)
                
        paths=[]
        for i in downloaded_files:
            a=i.split("\\")
            paths.append((a[-1].split("/")[-1]))
        print(paths)
        table_data = list(zip(dates, summary_content, paths))

        print(summary_content)
        out_summ=bart(summary_text,200,250)
        out1=f'Name: {name}\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t Date: {datetime.datetime.now().strftime("%Y-%m-%d")}\n{out_summ}'


        

        
        context = { "audios":paths,"contents":summary_content,"dates":dates,"data":table_data,"overall":out_summ,"download":out1,"name":name.upper()}


        html_template = loader.get_template('home/recent.html')
        return HttpResponse(html_template.render(context, request))

    context = {'form' : form}
    html_template = loader.get_template('home/recent.html')
    return HttpResponse(html_template.render(context, request))




def disussion(request):
    d=forumForm(request.POST or None)
    if d.is_valid():
        obj = d.save(commit=False)
        obj.save()
        name=obj.user_name
        ans=obj.answer

    context={'name':name,'ans':ans}

    html_template = loader.get_template('home/feedback.html')
    return HttpResponse(html_template.render(context, request))

def audio_upload(request):   
    form = summForm(request.POST or None, request.FILES or None)
    print(form.is_valid())
    if form.is_valid():
        temp=1
        obj = form.save(commit=False)
        obj.save()
        name=obj.p_name
        name=name.upper()
        number=obj.p_num
        value=request.POST.get('slider_value')
        min_value=(int(value)*50)+200
        max_value=min_value+50
        audio = request.FILES.get('audio_file')
        # Get the directory where you want to save the uploaded audio file
        save_directory = os.path.join(settings.MEDIA_ROOT, 'new_audio')
    
        # Create the directory if it doesn't exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

    # Generate a unique filename for the uploaded audio file
        filename = 'output.mp3'
        file_path = os.path.join(save_directory, filename)

    # Open the file and save the uploaded content
        with open(file_path, 'wb') as destination:
            for chunk in audio.chunks():
                destination.write(chunk)
        print(file_path)
        value=(int(value)*50)+200
        id=obj.id
        # file_path = settings.MEDIA_ROOT + '/new_files/'
        # audio_path = settings.MEDIA_ROOT + '/new_audio/' + obj.uploadAudio.url.split('/')[-1]
        c_path=os.path.join(settings.MEDIA_ROOT, 'new_transcripts/')
        

        script=transcript(file_path)
        transcript_file=combine("transcript.txt",script,c_path)
        summ_out=bart(script,min_value,max_value)
        out=final(summ_out,file_path)
        fillle=combine("summary.txt",out,c_path)
        c=main(file_path,number,name)
        d_path=f'{c_path}summary.txt'
        print(d_path)
        out1=f'Name: {name}\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t Date: {datetime.datetime.now().strftime("%Y-%m-%d")}\n{out}'
    

        context = { 'p_name': name,'sum': out,'id':id,'download':out1}


        html_template = loader.get_template('home/summary.html')
        return HttpResponse(html_template.render(context, request))

    context = {'form' : form}
    html_template = loader.get_template('home/summary.html')
    return HttpResponse(html_template.render(context, request))

def video_upload(request):   
    form = vidForm(request.POST or None, request.FILES or None)
    print(form.is_valid())
    if form.is_valid():
        temp=1
        obj = form.save(commit=False)
        obj.save()
        name=obj.pv_name
        name=name.upper()
        number=obj.pv_num
        id=obj.id
        value=request.POST.get('slider_value')
        min_value=(int(value)*50)+200
        max_value=min_value+50
        video=request.FILES.get('video_file')
        save_directory = os.path.join(settings.MEDIA_ROOT, 'new_video')
    
        # Create the directory if it doesn't exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

    # Generate a unique filename for the uploaded audio file
        filename = video.name
        file_path = os.path.join(save_directory, filename)

    # Open the file and save the uploaded content
        with open(file_path, 'wb') as destination:
            for chunk in video.chunks():
                destination.write(chunk)
        print(file_path)
        t=extract_audio(file_path)
        audio_path=os.path.join(settings.MEDIA_ROOT,'new_audio/output.mp3')

        v_path=os.path.join(settings.MEDIA_ROOT, 'new_transcripts/')
         
        script=transcript(file_path)
        transcript_file=combine("transcript.txt",script,v_path)
        summ_out=bart(script,max_value)
        # summ_out=summarize(script,min_value,max_value)
        out=final(summ_out,file_path)
        fillle=combine("summary.txt",out,v_path)
        c=main(file_path,number,name)
        out1=f'Name: {name}\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t Date: {datetime.datetime.now().strftime("%Y-%m-%d")}\n{out}'

    

        context = { 'pv_name': name,'sum': out,'id':id,"download":out1}


        html_template = loader.get_template('home/video.html')
        return HttpResponse(html_template.render(context, request))

    context = {'form' : form}
    html_template = loader.get_template('home/video.html')
    return HttpResponse(html_template.render(context, request))



def home(request):
    return render(request, 'home/home.html')

@login_required(login_url="/login/")
def new_get_time(request, id=None):
    summ = meta_video.objects.get(id=id)
    p=summ.pv_name
    

    media = os.path.join(settings.MEDIA_ROOT,'new_audio/output.mp3')
    number=get_audio_duration(media)/60
    duration = format(number, ".2f")
    path=os.path.join(settings.MEDIA_ROOT,'new_transcripts/new_trans.docx')
    t=read(path,1)
    print(t)
    words=key(t)
    topic_for_transcript=topic(t)
    sent=get_sentiment_score(t)
    print(topic_for_transcript)
    sentence=key_sentences(t)
    # sentence=['Okay, and does this happen in any other settings? Uh, like sometimes when its really cold outside, Ill go out and like my chest feels tight and feel like I cant breathe and kind of sucks','Um, and, uh, in your family, has anybody ever had any of these similar symptoms before? Uh, like my, my dad, I think he maybe had also when he was younger, but like he doesnt really have it now','So, um, yeah, so they just told me to come back today','Okay, and how long does it take for the breathing difficulty to go away? Like if I stop doing like the thing Im doing it, I dont know, not very long, like a couple of minutes','Um, was there anything, was there anything that you tried besides the rest to make those symptoms go away? Like I have the uh, the inhaler that the doctor gave me last time']
    # sentences=key_sentences(t)
    link='#'
    if topic_for_transcript=="Heart Problem":
        link='heart.html'
    elif topic_for_transcript=="Kidney Problem":
        link='kidney.html'
    elif topic_for_transcript=="Skin Problem":
        link='skin.html'
    elif topic_for_transcript=="Diabetes":
        link='sugar.html'
    elif topic_for_transcript=="Urinary Problem":
        link='urinary.html' 
    elif topic_for_transcript=="Asthma":
        link='asthma.html'  
    elements = zip(words,words)
    
    context={'duration':duration,'p':p,'words':words,'topic':topic_for_transcript,'link':link,'sentiment':sent,'sentences':words ,'elements':elements}
    
    html_template = loader.get_template('home/video_analystics.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def get_time(request, id=None):
    summ = summary_file.objects.get(id=id)
    p=summ.p_name
    

    media = os.path.join(settings.MEDIA_ROOT,'new_audio/output.mp3')
    number=get_audio_duration(media)/60
    duration = format(number, ".2f")
    path=os.path.join(settings.MEDIA_ROOT,'new_transcripts/new_trans.docx')
    t=read(path,1)
    print(t)
    words=key(t)
    topic_for_transcript=topic(t)
    sent=get_sentiment_score(t)
    print(topic_for_transcript)
    sentence=key_sentences(t)
    # sentence=['Okay, and does this happen in any other settings? Uh, like sometimes when its really cold outside, Ill go out and like my chest feels tight and feel like I cant breathe and kind of sucks','Um, and, uh, in your family, has anybody ever had any of these similar symptoms before? Uh, like my, my dad, I think he maybe had also when he was younger, but like he doesnt really have it now','So, um, yeah, so they just told me to come back today','Okay, and how long does it take for the breathing difficulty to go away? Like if I stop doing like the thing Im doing it, I dont know, not very long, like a couple of minutes','Um, was there anything, was there anything that you tried besides the rest to make those symptoms go away? Like I have the uh, the inhaler that the doctor gave me last time']
    # sentences=key_sentences(t)
    link='#'
    if topic_for_transcript=="Heart Problem":
        link='heart.html'
    elif topic_for_transcript=="Kidney Problem":
        link='kidney.html'
    elif topic_for_transcript=="Skin Problem":
        link='skin.html'
    elif topic_for_transcript=="Knee Problem":
        link='knee.html'
    elif topic_for_transcript=="Urinary Problem":
        link='skin.html' 
    elif topic_for_transcript=="Diarrhea":
        link='asthma.html'  
    elif topic_for_transcript=="Asthma":
        link='asthma.html' 
    elif topic_for_transcript=="Diabetes":
        link='asthma.html' 
    elif topic_for_transcript=="Muscle Problem":
        link='asthma.html' 
    elements = zip(words,words)
    
    context={'duration':duration,'p':p,'words':words,'topic':topic_for_transcript,'link':link,'sentiment':sent,'sentences':words ,'elements':elements}
    
    html_template = loader.get_template('home/analystics.html')
    return HttpResponse(html_template.render(context, request))
















@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))
   


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
