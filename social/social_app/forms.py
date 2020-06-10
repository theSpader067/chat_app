from django import forms
from .models import profile

class social_links_profileForm(forms.Form):
    twitter_handle = forms.CharField(label='Twitter',widget=forms.TextInput(attrs={'placeholder':'your twitter handle','type':'text','class':'form-control'}) ,max_length=100)
    facebook_handle = forms.CharField(label='Facebook',widget=forms.TextInput(attrs={'placeholder':'your facebook handle','type':'text','class':'form-control'}), max_length=100)
    instagram_handle = forms.CharField(label='Instagram',widget=forms.TextInput(attrs={'placeholder':'your instagram handle','type':'text','class':'form-control'}), max_length=100)
    linkedin_handle = forms.CharField(label='linkedin',widget=forms.TextInput(attrs={'placeholder':'your linkedin handle','type':'text','class':'form-control'}) ,max_length=100)
    youtube_handle = forms.CharField(label='youtube',widget=forms.TextInput(attrs={'placeholder':'your youtube handle','type':'text','class':'form-control'}) ,max_length=100)

class personal_profileForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control" ,'id':"fullname",'type':'text'}) ,max_length=100)
    email = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control" ,'id':"fulname",'type':'text'}) ,max_length=100)
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'class':"form-control" ,'id':"phone",'type':'text'}))


class about_profileForm(forms.Form):
    personal_motto = forms.CharField(widget=forms.Textarea(attrs={'class':"form-control" ,'id':"about-text"}),max_length=100)

class contactLookupForm(forms.Form):
    contact_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Contact name...','type':'text','class':'form-control','id':'contact_input'}) ,max_length=100)

class testForm(forms.Form):
    hell_kitty = forms.CharField(max_length=100)
    entries=dict()
    def __init__(self,*args,**kwargs):
        super(testForm, self).__init__(*args, **kwargs)

        #for k,v in enumerate(args[0]):
        #    self.fields[v] = forms.BooleanField()')
    def create(self,*args,**kwargs):
        print('ffffffffffffffffffffffffffffffffff',args[0])
        for k,v in enumerate(args[0]):
            self.entries[args[0][k]]= forms.BooleanField()
        return testForm().entries
