from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.contrib import messages
from django.urls import reverse

from .forms import CustomUserCreationForm, UserUpdateForm, PasswordChangeForm,CustomAuthenticationForm, ForgotPasswordForm, ResetPasswordForm, StaffCreationForm, PatientCreationForm, SuperAdminCreationForm
from .models import CustomUser
from projects.models import Project, ProjectMember, Notification
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("dashboard"))
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = request.POST.get('password')

            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username/email or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Replace with your login URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

class SuperAdminLoginView(LoginView):
    template_name = 'accounts/superadmin_login.html'

class StaffPatientLoginView(LoginView):
    template_name = 'accounts/staff_patient_login.html'

@login_required
def create_staff(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, request.FILES)
        staff_form = StaffCreationForm(request.POST)
        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save(commit=False)
            user.is_staff = True
            user.save()
            staff = staff_form.save(commit=False)
            staff.user = user
            staff.save()
            return redirect('staff_list')
    else:
        user_form = CustomUserCreationForm()
        staff_form = StaffCreationForm()

    return render(request, 'accounts/create_staff.html', {'user_form': user_form, 'staff_form': staff_form})

@login_required
def create_patient(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, request.FILES)
        patient_form = PatientCreationForm(request.POST)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            return redirect('patient_list')
    else:
        user_form = CustomUserCreationForm()
        patient_form = PatientCreationForm()

    return render(request, 'accounts/create_patient.html', {'user_form': user_form, 'patient_form': patient_form})

def is_superadmin(user):
    return user.is_superuser

@user_passes_test(is_superadmin, login_url='/accounts/staff-patient-login/')
def register_superadmin(request):
    if request.method == 'POST':
        form = SuperAdminCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            return redirect('superadmin_login')
    else:
        form = SuperAdminCreationForm()

    return render(request, 'accounts/register_superadmin.html', {'form': form})


@login_required
def project_list(request):
    user_projects = Project.objects.filter(owner=request.user) if request.user.role == 'manager' else []
    return render(request, 'projects/project_list.html', {'projects': user_projects})

@login_required
def upload_photo(request):
    if request.method == "POST" and request.FILES.get('profile_picture'):
        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        print("MEDIA_ROOT:", settings.MEDIA_ROOT)
        print("Saved file path:", user.profile_picture.path)
        print("File URL:", user.profile_picture.url)
        messages.success(request,"Profile Picture changed successfully!",extra_tags="alert-success")
        return JsonResponse({'new_photo_url': user.profile_picture.url})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # Deletes the user
        logout(request)  # Logs out the user
        return JsonResponse({'success': True, 'message': 'Account deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@login_required
def my_profile(request):
    user = request.user
    user_form = UserUpdateForm(instance=user)
    password_form = PasswordChangeForm(user=user)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user=user, data=request.POST)

        is_user_form_valid = user_form.is_valid()
        password_attempt = any(request.POST.get(field) for field in ['old_password', 'new_password', 'confirm_password'])
        is_password_form_valid = password_form.is_valid() if password_attempt else False

        # Process password change if there's an attempt
        if password_attempt:
            if is_password_form_valid:
                new_password = password_form.cleaned_data["new_password"]
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keeps the user logged in
                messages.success(request, "Password changed successfully!")
            else:
                messages.error(request, "Please correct the errors in the password form.")
                print("Password Form Errors:", password_form.errors)  # Debug errors

        # Both forms are valid and all updates are successful
        if is_user_form_valid and (not password_attempt or is_password_form_valid):
            if is_user_form_valid:  # Only save and show message if user form is valid
                user_form.save()
                messages.success(request, "Profile updated successfully!")
            return redirect("my_profile")

    context = {
        "user_form": user_form,
        "password_form": password_form,
    }
    return render(request, "users/my_profile.html", context)


def logout_view(request):
    logout(request)
    return redirect('login')


# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')

#         if email:
#             try:
#                 user = CustomUser.objects.get(email=email)

#                 token = default_token_generator.make_token(user)
#                 uid = urlsafe_base64_encode(str(user.pk).encode())

#                 reset_url = f"http://{get_current_site(request).domain}/reset-password/{uid}/{token}/"

#                 send_mail(
#                     "Password Reset Request",
#                     f"Click the link to reset your password: {reset_url}",
#                     "no-reply@omnia.com",
#                     [email],
#                 )

#                 messages.success(request, "A password reset link has been sent to your email address.")
#                 return redirect('login')
#             except CustomUser.DoesNotExist:
#                 messages.error(request, "No user found with that email address.")
#         else:
#             messages.error(request, "Please provide a valid email address.")

#     return render(request, 'users/forgotpass.html')
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)

                # Generate token and URL for password reset
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode())
                # Generate the password reset URL
                reset_url = f"http://{get_current_site(request).domain}/reset-password/{uid}/{token}/"
                # Send email
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link to reset your password: {reset_url}",
                    from_email="no-reply@omnia.com",  # Replace with your email address
                    recipient_list=[email],
                )
                messages.success(request, "A password reset link has been sent to your email address.")
                return redirect('login')
            except CustomUser.DoesNotExist:
                messages.error(request, "No user found with that email address.")
        else:
            messages.error(request, "Please provide a valid email address.")
    else:
        form = ForgotPasswordForm()
    return render(request, 'users/forgotpass.html', {'form': form})


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully!")
                return redirect('login')
        else:
            form = ResetPasswordForm(user)
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('login')

    return render(request, 'users/reset_password.html', {'form': form})
# def reset_password(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = CustomUser.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#         user = None

#     if user and default_token_generator.check_token(user, token):
#         if request.method == 'POST':
#             form = SetPasswordForm(user, request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Your password has been reset successfully!")
#                 return redirect('login')
#         else:
#             form = SetPasswordForm(user)
#     else:
#         messages.error(request, "The reset link is invalid or has expired.")
#         return redirect('login')

#     return render(request, 'users/reset_password.html', {'form': form})

@login_required
def dashboard(request):
   
    return render(request, 'clinic/dashboard.html', )
