from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('my-profile/', views.my_profile, name='my_profile'),
    path('upload-photo/', views.upload_photo, name='upload_photo'),
    path('delete-user/', views.delete_user, name='delete_user'),
    
    path('superadmin-login/', views.SuperAdminLoginView.as_view(), name='superadmin_login'),
    path('staff-patient-login/', views.StaffPatientLoginView.as_view(), name='staff_patient_login'),
    
    path('register-superadmin/', views.register_superadmin, name='register_superadmin'),
    
    path('create-staff/', views.create_staff, name='create_staff'),
    path('create-patient/', views.create_patient, name='create_patient'),

    # newly added path
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password')
    # path('reset-password/', reset_password, name='reset_password')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
