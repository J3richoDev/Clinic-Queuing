from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login/', views.StaffPatientLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('my-profile/', views.my_profile, name='my_profile'),
    path('upload-photo/', views.upload_photo, name='upload_photo'),
    path('delete-user/', views.delete_user, name='delete_user'),
    
    path('superadmin-login/', views.SuperAdminLoginView.as_view(), name='superadmin_login'),
    path('staff-patient-login/', views.StaffPatientLoginView.as_view(), name='staff_patient_login'),
    
    path('register-superadmin/', views.register_superadmin, name='register_superadmin'),
    
    path('manage-staff', views.manage_staff, name='manage_staff'),
    path('create-patient/', views.create_patient, name='create_patient'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
