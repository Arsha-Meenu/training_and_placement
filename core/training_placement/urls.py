from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about/', views.AboutUsView.as_view(), name='about'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='training_placement:login'), name='logout'),
    path('add-new-user/', views.CreateNewUserView.as_view(), name='add-new-user'),
    path("password-change", views.PasswordsChangeView.as_view(), name="password-change"),
    # ADMIN
    path('admin-dashboard/', views.AdminDashboard.as_view(), name='admin-dashboard'),
    path("admin-report/", views.AdminReportView.as_view(), name="admin-report"),
    path("admin-edit/<int:pk>/", views.AdminUpdateView.as_view(), name="admin-edit"),
    path("admin-delete/<int:pk>/", views.AdminDeleteView.as_view(), name="admin-delete"),
    # TPO
    path('tpo-dashboard/', views.TPODashboard.as_view(), name='tpo-dashboard'),
    path("TPO-report/", views.TPOReportView.as_view(), name="TPO-report"),
    path("TPO-edit/<int:pk>/", views.TPOUpdateView.as_view(), name="TPO-edit"),
    path("TPO-delete/<int:pk>/", views.TPODeleteView.as_view(), name="TPO-delete"),
    # STUDENT
    path('student-dashboard/', views.StudentDashboard.as_view(), name='student-dashboard'),
    path("student-report/", views.StudentReportView.as_view(), name="student-report"),
    path("student-edit/<int:pk>/", views.StudentUpdateView.as_view(), name="student-edit"),
    path("student-delete/<int:pk>/", views.StudentDeleteView.as_view(), name="student-delete"),
    path("student-jobs/", views.StudentJobsListView.as_view(), name="student-jobs"),
    path("student-trainings/", views.StudentTrainingsListView.as_view(), name="student-training"),

    # JOB
    path('add-job/', views.CreateJobView.as_view(), name='add-job'),
    path("all-jobs/", views.AllJobsView.as_view(), name="all-jobs"),
    path("job-detail/<int:pk>", views.JobDetailView.as_view(), name="job-detail"),
    path("job-report/", views.JobReportView.as_view(), name="job-report"),
    path("job-edit/<int:pk>/", views.JobUpdateView.as_view(), name="job-edit"),
    path("job-delete/<int:pk>/", views.JobDeleteView.as_view(), name="job-delete"),
    path("job-registration/", views.JobRegistrationView.as_view(), name="job-registration"),
    # TRAINING
    path("all-trainings/", views.AllTrainingView.as_view(), name="all-trainings"),
    path("training-detail/<int:pk>", views.TrainingDetailView.as_view(), name="training-detail"),
    path('add-training/', views.CreateTrainingView.as_view(), name='add-training'),
    path('download-training-file/<int:pk>', views.DownloadContentFileView.as_view(), name='download-training-file'),
    path("training-report/", views.TrainingReportView.as_view(), name="training-report"),
    path("training-edit/<int:pk>/", views.TrainingUpdateView.as_view(), name="training-edit"),
    path("training-delete/<int:pk>/", views.TrainingDeleteView.as_view(), name="training-delete"),
    path("training-registration/", views.TrainingRegistrationView.as_view(), name="training-registration"),
    # path("enroll-training/", views.EnrollTrainingView.as_view(), name="enroll-training"),
    path("apply-job/", views.ApplyJobView.as_view(), name="apply-job"),
    path("verify-email/", views.VerifyOTP, name="verify-email"),


#     trial
    path("send_otp/", views.send_otp, name="send_otp"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),









]
