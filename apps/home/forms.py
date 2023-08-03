from django import forms 
from .models import summary_file,meta_video,forum,cloud



class forumForm(forms.ModelForm):
    class Meta:
        model=forum
        fields=[
            'user_name',
            'answer',
        ]


class cloudForm(forms.ModelForm):
    class Meta:
        model=cloud
        fields=[
            'p_num',
            'p_name',
        ]



class summForm(forms.ModelForm):
    class Meta:
        model = summary_file
        fields = [
            'p_name',
            'p_num',
           
        ]
    
class vidForm(forms.ModelForm):
    class Meta:
        model = meta_video
        fields = [
            'pv_name',
            'pv_num',
           
        ]