from django import forms
from ca.models import UserProfile, Program, University, Package
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Minimum length of password required
MINIMUM_PASSWORD_LENGTH = 6

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    password_confirmation = forms.CharField(widget = forms.PasswordInput)
    username = forms.CharField()
    email = forms.CharField()

    # Set required minimum password length
    def clean_password(self):
        pw = self.cleaned_data.get('password')
        if len(pw) < MINIMUM_PASSWORD_LENGTH:
            raise ValidationError('Password cannot be shorter than 6 letters.')
        return pw

    def clean_password_con(self):
        pw1 = self.cleaned_data.get('password')
        pw2 = self.cleaned_data.get('password_confirmation')
        if pw1 and pw1 != pw2:
            raise forms.ValidationError("Passwords don't match")
        return pw2

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    # year_status = forms.ModelChoiceField(queryset = UserProfile.YEAR_STATUS_CHOICES, required = True)
    picture = forms.ImageField(help_text = "Select an image", required = False)
    fav_program = forms.ModelMultipleChoiceField(queryset = Program.objects.all(), to_field_name = "name", required = False)
    fav_university = forms.ModelMultipleChoiceField(queryset = University.objects.all(), required = False)
    packages = forms.ModelMultipleChoiceField(queryset = Package.objects.all(), required = False)
    class Meta:
        model = UserProfile
        fields = ['about_me', 'year_status', 'phone', 'picture', 'skype_id', 'qq_id', 'fav_program', 'fav_university', 'packages']

class UserRegisterForm(forms.ModelForm):
    # year_status = forms.ModelChoiceField(queryset = UserProfile.YEAR_STATUS_CHOICES, required = True)
    class Meta:
        model = UserProfile
        fields = ['year_status']

class EditUserForm(forms.ModelForm):
    password = forms.CharField(help_text = "Password")
    username = forms.CharField(help_text = "Username")
    email = forms.CharField(help_text = "Email")
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(required = True)
    email = forms.EmailField(required = True)
    class Meta:
        model = UserProfile
        fields = ['phone', 'picture', 'skype_id', 'qq_id']

class ProgramDetailForm(forms.ModelForm):
    class Meta:
        model = Program
        exclude = ['university', 'program_category', 'name', 'career', 'faculty', 'attendance rate', 'percentage_chinese', 'undergrad_institution']


