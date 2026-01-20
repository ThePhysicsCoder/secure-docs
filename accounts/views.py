from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")

        elif password != password2:
            messages.error(request, "Password mismatch")

        else:
            # 🔐 CREATE USER BUT INACTIVE
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            user.is_active = False   # 🔥 IMPORTANT
            user.save()

            # 🔐 GENERATE VERIFICATION LINK
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            verification_link = request.build_absolute_uri(
                reverse('verify-email', kwargs={
                    'uidb64': uid,
                    'token': token
                })
            )

            # 📧 SEND EMAIL
            subject = "Verify your Digital Locker account"
            message = f"""
                Hi {user.username},

                Please verify your account by clicking the link below:

                {verification_link}

                If you did not create this account, ignore this email.
                """
            user.email_user(subject, message)

            messages.success(
                request,
                "Account created! Please check your email to verify your account."
            )
            return redirect('login')

    return render(request, 'accounts/register.html')

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        if user.is_active:
            messages.info(request, "Your account is already verified.")
        else:
            user.is_active = True
            user.save()
            messages.success(request, "Email verified successfully. You can now login.")
        return redirect('login')

    messages.error(request, "Verification link is invalid or expired.")
    return redirect('login')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password =  request.POST.get('password')

        user = authenticate(request, username=username,password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "invalid credentials")

    return render(request, "accounts/login.html")    

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("login")
    return render(request, 'accounts/confirm_logout.html')
