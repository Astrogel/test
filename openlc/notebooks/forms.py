from django import forms
from models import Notebook, UserProfile, User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
    description = forms.CharField(max_length=500, required=False, widget=forms.Textarea())

    class Meta:
        model = UserProfile
        fields = ('picture', 'description')

class NotebookForm(forms.ModelForm):
    file = forms.FileField()
    title = forms.CharField(max_length=120)
    description = forms.CharField(max_length=300, required=False, widget=forms.Textarea())

    class Meta:
        model = Notebook
        fields = ('file', 'title', 'description', 'category',)



