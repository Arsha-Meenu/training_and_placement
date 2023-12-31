from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from .managers import UserManager
from django.core.validators import validate_image_file_extension, FileExtensionValidator


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_TYPE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=10)
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile_number = PhoneNumberField(null=True, blank=True, unique=True, validators=[phone_regex])
    gender = models.CharField(max_length=2, null=False, choices=GENDER_TYPE, blank=True)
    current_address = models.TextField()
    permanent_address = models.TextField(null=True)
    profile_image = models.ImageField(upload_to='profile-images', null=True, validators=[
        FileExtensionValidator(["png", "jpg", "jpeg", 'svg', 'webp', ])])  # for images
    # country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    # city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    upload_resume = models.FileField(upload_to='uploaded-resume', null=True, blank=True,
                                     validators=[FileExtensionValidator(
                                         ["pdf", "doc", "docx", "txt", "mp3", "aac", "m4a", "mp4", "ogg", "odt"])])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6)

    class UserTypes(models.TextChoices):
        ADMIN = "Admin", "ADMIN"  # caps ADMIN - for db only
        TPO = "TPO", "TPO"
        STUDENT = "Student", "STUDENT"

    default_type = UserTypes.ADMIN

    type = models.CharField(_('Type'), max_length=255, choices=UserTypes.choices, default=default_type)
    # type = MultiSelectField(verbose_name='default types', choices=UserTypes.choices, blank=True, max_choices=5,
    #                         max_length=255, default=[])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    company_logo = models.FileField(upload_to='company_logo', null=True, verbose_name='company logo',
                                    validators=[FileExtensionValidator(
                                        ['svg', 'jpg', 'jpeg', 'png', 'webp', 'xls', 'xlsx',
                                         'ppt', 'pptx', 'zip', 'rar', '7zip', 'avif'])])
    description = models.TextField(max_length=400, null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    skills = models.TextField(max_length=200, null=True, blank=True)
    posted_at = models.DateField(null=True, blank=True)
    is_applied = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.title


class Subject(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Training(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField(max_length=400, null=True, blank=True)
    training_date = models.DateField(null=True, blank=True)
    is_enrolled = models.BooleanField(default=False, blank=True, null=True)
    content_file = models.FileField(upload_to='training_content_file', null=True, verbose_name='training content file',
                                    validators=[FileExtensionValidator(
                                        ['pdf', 'docx', 'doc', 'xls', 'xlsx', 'zip', 'rar', '7zip', 'txt'])])

    def __str__(self):
        return self.title


class JobSelectedUser(models.Model):
    user = models.ManyToManyField(User, related_name='selected_user')
    jobs = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='selected_jobs')

    def __str__(self):
        return self.jobs.title
