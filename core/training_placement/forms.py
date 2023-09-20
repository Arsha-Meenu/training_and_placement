from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from .models import User, Job, Training, JobSelectedUser
from phonenumber_field.formfields import PhoneNumberField


class AddJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('title', 'company', 'company_logo', 'salary', 'experience', 'skills', 'description', 'location')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Job Title',
                'required': True
            }),
            'company': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Enter Company Name',
                'required': True
            }),
            'company_logo': forms.FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Enter Company Logo',
                'required': True
            }),
            'salary': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Enter Salary (per month)',
                'required': True
            }),
            'experience': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Experience required (in years)',
                'required': True
            }),
            'skills': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'cols': 10, 'rows': 10,
                'placeholder': 'Enter the required skills for the job',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'cols': 10, 'rows': 10,
                'placeholder': 'Description of the exact job',
                'required': True
            }),
            'location': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Enter exact location of the Company',
                'required': True
            })
        }


class AddTrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ('title', 'subject', 'description', 'training_date', 'content_file')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Training Title',
                'required': True
            }),
            'subject': forms.Select(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Subject',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'cols': 10, 'rows': 10,
                'placeholder': 'Training Description',
                'required': True
            }),
            'training_date': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control',
                       'style': 'max-width: 500px;',
                       'placeholder': 'Training Start Date',
                       'required': True,
                       'type': 'date'
                       }),

            'content_file': forms.FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Training File',
                'required': True
            }),
        }


GENDER_TYPE = (
    ('M', 'Male'),
    ('F', 'Female'),
)

User_Type = (
    ('Admin', 'ADMIN'),
    ('TPO', 'TPO'),
    ('Student', 'STUDENT'),
)


class AddUserForm(forms.ModelForm):
    # mobile_number = PhoneNumberField()
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    type = forms.ChoiceField(choices=User_Type)

    # confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            'type', 'name', 'first_name', 'last_name', 'gender', 'current_address', 'permanent_address',
            'profile_image',
            'email',
            'mobile_number', 'password', 'confirm_password')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User Name',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User FirstName'
            }),
            'last_name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User LastName'
            }),
            'mobile_number': forms.NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Mobile Number',
                'required': True
            }),
            'current_address': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Current Address',
                'cols': 7, 'rows': 7,
                'required': True
            }),
            'permanent_address': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Permanent Address',
                'cols': 7, 'rows': 7,
                'required': True
            }),
            'profile_image': forms.FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User Profile Image'
            }),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User Email',
                'required': True,
            }),
            'password': forms.PasswordInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Password',
                'required': True
            })
            ,
            'confirm_password': forms.PasswordInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Confirm Password',
                'required': True
            })

        }

    def clean(self):
        cleaned_data = super(AddUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class UserUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    type = forms.ChoiceField(choices=User_Type)

    class Meta:
        model = User
        fields = (
            'type', 'name', 'first_name', 'last_name', 'gender', 'current_address', 'permanent_address',
            'profile_image',
            'email',
            'mobile_number')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User Name',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User FirstName'
            }),
            'last_name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User LastName'
            }),
            'mobile_number': forms.NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Mobile Number',
                'required': True
            }),
            'current_address': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Current Address',
                'cols': 7, 'rows': 7,
                'required': True
            }),
            'permanent_address': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Permanent Address',
                'cols': 7, 'rows': 7,
                'required': True
            }),
            'profile_image': forms.FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User Profile Image'
            }),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User Email',
                'required': True,
            })
        }


class PasswordChangingForm(PasswordChangeForm):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}),
                                       max_length=100)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}),
                                   max_length=100)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}),
                                       max_length=100)

    class Meta:
        model = User
        fields = ('current_password', 'new_password', 'confirm_password ')


#
# CHOICES = [(supervisor.id, supervisor.get_full_name())
#            for supervisor in User.objects.all()]


class ApplyJobForm(forms.ModelForm):
    # name = forms.ModelChoiceField(queryset=User.objects.all())
    # supervisor = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = User
        fields = (
            'name', 'current_address',
            'profile_image', 'upload_resume',
            'email',
            'mobile_number')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User Name',
                'required': True
            }),
            'upload_resume': forms.FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User Resume'
            }),
            'mobile_number': forms.NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Mobile Number',
                'required': True
            }),
            'current_address': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Current Address',
                'cols': 3, 'rows': 3,
                'required': True
            }),
            'profile_image': forms.FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User Profile Image'
            }),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User Email',
                'required': True,
            })

        }


class SendEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'User Email',
                'required': True,
            })}
