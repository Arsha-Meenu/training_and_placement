import math

import pyotp
import random
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.mail import EmailMessage, send_mail
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import AddJobForm, AddTrainingForm, AddUserForm, UserUpdateForm, PasswordChangingForm, ApplyJobForm, \
    SendEmailForm
from .models import Job, Training, User, JobSelectedUser
from django.contrib.sites.shortcuts import get_current_site

from .utils import send_otp
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt


class HomeView(TemplateView):
    template_name = 'common/index.html'


class ContactView(TemplateView):
    template_name = 'common/contact.html'


class AboutUsView(TemplateView):
    template_name = 'common/about.html'


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'authentication/login.html'
    fields = "__all__"

    def form_valid(self, form):
        super().form_valid(form)
        # Use this in model :
        # REQUEST_TYPE = (
        #         (ADMIT, 'ADMIT'),
        #         (TRANSFER, 'TRANSFER'),
        #         (DISCHARGE, 'DISCHARGE'),
        #     )
        # USE this in view: bed_request.request_type = BedRequest.ADMIT
        if self.request.user.type == 'Student':
            return redirect('training_placement:student-dashboard')
            # return redirect('training_placement:student-dashboard')
        elif self.request.user.type == 'TPO':
            return redirect('training_placement:tpo-dashboard')
            # return render(self.request,'dashboard/tpo-dashboard.html')
        else:
            return redirect('training_placement:admin-dashboard')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class AdminDashboard(TemplateView):
    template_name = 'dashboard/admin-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(AdminDashboard, self).get_context_data(**kwargs)
        context['user'] = self.request.user.type
        return context


class TPODashboard(TemplateView):
    template_name = 'dashboard/tpo-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(TPODashboard, self).get_context_data(**kwargs)
        context['user'] = self.request.user.type
        return context


class StudentDashboard(TemplateView):
    template_name = 'dashboard/student-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(StudentDashboard, self).get_context_data(**kwargs)
        context['user'] = self.request.user.type
        return context


class CreateJobView(CreateView):
    template_name = 'job/add_job.html'
    model = Job
    form_class = AddJobForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.posted_at = date.today()
        form.save(commit=False)
        return super(CreateJobView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse("training_placement:admin-dashboard")


class AllJobsView(ListView):
    template_name = 'job/all_jobs.html'
    queryset = Job.objects.all()
    context_object_name = 'jobs'


class JobDetailView(DetailView):
    model = Job
    template_name = 'job/job_details.html'
    context_object_name = 'job'


class AllTrainingView(ListView):
    template_name = 'training/all_trainings.html'
    queryset = Training.objects.all()
    context_object_name = 'trainings'


class TrainingDetailView(DetailView):
    model = Training
    template_name = 'training/training_details.html'
    context_object_name = 'training'


class CreateTrainingView(CreateView):
    template_name = 'training/add_training.html'
    model = Training
    form_class = AddTrainingForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save(commit=False)
        return super(CreateTrainingView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse("training_placement:all-trainings")


class DownloadContentFileView(View):
    def get(self, request, pk):
        file_obj = get_object_or_404(Training, pk=pk)
        response = HttpResponse(file_obj.content_file, content_type='application/octet-stream')
        return response


class CreateNewUserView(CreateView):
    template_name = 'authentication/add_user.html'
    model = User
    form_class = AddUserForm

    def form_valid(self, form):
        form.user = self.request.user
        password = form.cleaned_data['password']
        user = form.save(commit=False)
        user.set_password(password)
        user.save()
        return super(CreateNewUserView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse("training_placement:admin-dashboard")


class AdminReportView(ListView):
    template_name = 'authentication/admin_report.html'
    queryset = User.objects.filter(type='Admin').all()
    context_object_name = 'admins'


class StudentReportView(ListView):
    template_name = 'authentication/student_report.html'
    queryset = User.objects.filter(type='Student').all()
    context_object_name = 'students'


class TPOReportView(ListView):
    template_name = 'authentication/TPO_report.html'
    queryset = User.objects.filter(type='TPO').all()
    context_object_name = 'TPO'


class TrainingReportView(ListView):
    template_name = 'training/training_report.html'
    context_object_name = 'trainings'

    def get_queryset(self):
        if self.request.user.type == 'Admin':
            training = Training.objects.all()
        else:
            training = Training.objects.filter(user__type='Admin')
        return training


class JobReportView(ListView):
    template_name = 'job/job_report.html'
    queryset = Job.objects.all()
    context_object_name = 'jobs'


class AdminUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'authentication/add_user.html'

    def get_success_url(self, **kwargs):
        return reverse("training_placement:admin-report")


class AdminDeleteView(DeleteView):
    model = User
    template_name = 'authentication/admin_delete.html'

    def get_success_url(self, **kwargs):
        return reverse("training_placement:admin-report")


class StudentUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'authentication/add_user.html'

    def get_success_url(self, **kwargs):
        return reverse("training_placement:student-report")


class StudentDeleteView(DeleteView):
    model = User
    template_name = 'authentication/admin_delete.html'

    def get_success_url(self, **kwargs):
        return reverse("training_placement:student-report")


class TPOUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'authentication/add_user.html'

    def get_success_url(self, **kwargs):
        return reverse("training_placement:TPO-report")


class TPODeleteView(DeleteView):
    model = User
    template_name = 'authentication/admin_delete.html'

    def get_success_url(self, **kwargs):
        return reverse("training_placement:TPO-report")


class TrainingUpdateView(UpdateView):
    model = Training
    form_class = AddTrainingForm
    template_name = 'training/add_training.html'

    def get_success_url(self, **kwargs):
        return reverse("training_placement:training-report")


class TrainingDeleteView(DeleteView):
    model = Training
    template_name = 'training/training_delete.html'

    def get_success_url(self, **kwargs):
        return reverse("training_placement:training-report")


class JobUpdateView(UpdateView):
    model = Job
    form_class = AddJobForm
    template_name = 'job/add_job.html'

    def get_success_url(self, **kwargs):
        return reverse("training_placement:job-report")


class JobDeleteView(DeleteView):
    model = Job
    template_name = 'job/job_delete.html'

    def get_success_url(self, **kwargs):
        return reverse("training_placement:job-report")


class JobRegistrationView(ListView):
    model = Job
    template_name = 'job/job_registration.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.model.objects.filter(user__type='Student').all()


class TrainingRegistrationView(ListView):
    model = Training
    template_name = 'training/training_registration.html'
    context_object_name = 'trainings'

    def get_queryset(self):
        return self.model.objects.filter(user__type='Student').all()


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    template_name = 'authentication/change_password.html'

    def get_success_url(self, **kwargs):
        return reverse("training_placement:login")


class StudentJobsListView(ListView):
    template_name = 'job/student_all_jobs.html'
    model = Job
    context_object_name = 'jobs'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class StudentTrainingsListView(ListView):
    template_name = 'training/student_all_training.html'
    model = Training
    context_object_name = 'trainings'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


#
# class EnrollTrainingView(View):
#
#     def get(self, request):
#         print('get',request.user.id)
#         training_id = Training.objects.get(user__id=request.user.id).id
#         print('id', training_id)
#         messages.success(request, 'You have successfully enrolled.')
#         return render(request, 'training/training_details.html', {})

# class ApplyJobView(CreateView):
#     template_name = 'job/apply_job.html'
#     model = JobSelectedUser
#     form_class = ApplyJobForm
#
#     def form_valid(self, form):
#         form.user = self.request.user
#         obj = form.save(commit=False)
#         job = Job.objects.get(title='Django')
#         jobs = JobSelectedUser.objects.create(jobs=job)
#         obj.type = 'Student'
#         jobs.user.add(self.request.user)
#         obj.save()
#         return super(ApplyJobView, self).form_valid(form)
#
#     def get_success_url(self, **kwargs):
#         messages.success(self.request, 'successfully applied for the job')
#         return reverse("training_placement:send-otp")


class ApplyJobView(View):
    form_class = SendEmailForm
    template_name = 'job/apply_job.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    # send email without attachment using smtp.gmail
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            subject = 'Sign in with this one time passcode'
            email = form.cleaned_data['email']
            # attachment_path = request.FILES.getlist('attach')
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            otp = random.randint(100000, 999999)
            message = f"Verify your mail by the OTP:  {otp}"
            try:
                # ### send email with attachment
                # mail = EmailMessage(subject, message, email_from, recipient_list)
                # # # for file in attachment_path:
                # # #     mail.attach(file.name, file.read(), file.content_type)
                # mail.send()

                # ### sending email with custom template
                html_content = render_to_string('common/custom_email_template.html',
                                                {'message': message, 'subject': subject})
                send_mail(subject, message, email_from, recipient_list, fail_silently=False, html_message=html_content)
                return render(request, 'common/verify.html',
                              {'otp': otp, 'email_form': form, 'messages': 'Sent email to %s' % email})

            except:
                return render(request, self.template_name,
                              {'email_form': form, 'messages': 'Either the attachment is too big or corrupt'})

        return render(request, self.template_name,
                      {'email_form': form, 'messages': 'Otp is not correct.Try Again.'})


@csrf_exempt
def VerifyOTP(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        print("otp:", user_otp)
    return JsonResponse({'data': 'data'}, status=200)  # return JsonResponse({'data': 'data'}, status=200)


def send_otp(request):
    if request.method == 'POST':
        user = request.user
        email = "mollymeenu143@gmail.com"
        print('email', email)
        otp_code = ''.join(random.choice('0123456789') for _ in range(6))
        # OTP.objects.create(user=user, otp=otp_code)

        # Send OTP via email
        subject = 'Your OTP for Verification'
        message = f'Your OTP is: {otp_code}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]

        send_mail(subject, message, email_from, recipient_list)

        return JsonResponse({'message': 'OTP sent successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def verify_otp(request):
    if request.method == 'POST':
        user = request.user
        otp_code = request.POST.get('otp')
        print('user', user)
        user_obj = User.objects.filter(otp=otp_code, is_verified=False).first()
        if User.objects.filter(otp=otp_code, is_verified=True).exists():
            return JsonResponse({'error': 'Invalid OTP or OTP already verified'})
        else:
            user_obj.is_verified = True
            user_obj.otp = otp_code
            user_obj.save()
            print('op', user_obj.is_verified)
            return JsonResponse({'message': 'OTP verified successfully'})
        # else:
        #     return JsonResponse({'error': 'Invalid OTP or OTP already verified'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
