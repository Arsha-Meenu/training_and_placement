from datetime import date
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import AddJobForm, AddTrainingForm, AddUserForm, UserUpdateForm, PasswordChangingForm, ApplyJobForm
from .models import Job, Training, User


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


class ApplyJobView(CreateView):
    template_name = 'job/apply_job.html'
    model = Job
    form_class = ApplyJobForm

    def form_valid(self, form):
        form.user = self.request.user
        print('form.user',form.user)
        obj = form.save(commit=False)
        obj.type = 'Student'
        obj.save()
        return super(ApplyJobView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'successfully applied for the job')
        return reverse("training_placement:apply-job")