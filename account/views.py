from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from account.forms import EditProfileForm, PersonalEditForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from account.models import UserProfile
from account.tokens import account_activation_token
from mysite import repeated
from post.models import Post


# User Registration View
def register(request):
    if request.user.is_authenticated:
        return redirect('trendsup:index')
    context = {}

    #footer
    context['foot'] = repeated.footer()

    if request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken")
                return redirect('account:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect('account:register')
            else:
                user = User.objects.create_user(first_name=first_name,
                                                last_name=last_name,
                                                username=username,
                                                password=password1,
                                                email=email)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                message = render_to_string('account/acc_active_email.html', {
                    'user': user, 'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail_subject = 'Activate your TrendsUp account.'
                to_email = request.POST['email']
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                messages.info(request, 'Please confirm your email address to complete the registration.')
                return render(request, 'account/register.html')

        else:
            messages.info(request, 'Password not matching')
            return redirect('account:register')
    else:
        return render(request, 'account/register.html', context)


# User Account Activation View
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return render(request, 'account/thanks.html')
    else:
        messages.info(request, 'Activation link is invalid!')
        return render(request, 'account/register.html')


# User Profile View
@login_required(login_url='account:must_authenticate')
def view_profile(request):
    context = {}
    # API
    context = repeated.api(context)

    # Category Dropdown
    context['cate'] = repeated.category_dropdown()

    # Footer
    context['foot'] = repeated.footer()
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        pro = UserProfile.objects.get(user=request.user.id)
        context['user'] = user
        context['pro'] = pro
        post = Post.objects.all().filter(author=request.user, status=True).order_by('-date_posted')

        # Pagination

        posts = repeated.pagination(request, post)
        context['posts'] = posts

        return render(request, 'account/profile.html', context)


# User Profile Edit View
@login_required(login_url='account:must_authenticate')
@transaction.atomic
def edit_profile(request):
    context = {}
    # Footer
    context['foot'] = repeated.footer()
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = PersonalEditForm(request.POST or None, request.FILES or None, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('account:view_profile')
        else:
            messages.error(request, 'Please fill in the correct Details.')
            return redirect('account:edit_profile')
    else:
        user_form = EditProfileForm(instance=request.user)
        profile_form = PersonalEditForm(instance=request.user.userprofile)
        context['user_form'] = user_form
        context['profile_form'] = profile_form
    return render(request, 'account/edit_profile.html', context)


# User Account Deletion View
@login_required(login_url='account:must_authenticate')
def delete_account(request, username):
    context = {}

    # Footer
    context['foot'] = repeated.footer()
    try:
        u_obj = User.objects.get(username=username)
        u_obj.delete()
        context['message'] = 'Sorry, You have to Leave.'
    except User.DoesNotExist:
        context['message'] = "User Doesn't Exist"
    except Exception as e:
        context['message'] = e.message
    return render(request, 'account/del_profile.html', context)


# Change Password View
@login_required(login_url='account:must_authenticate')
def change_password(request):
    context = {}

    # Footer
    context['foot'] = repeated.footer()
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
        else:
            return redirect('account:change_password')
    else:
        form = PasswordChangeForm(request.user)
        context['form'] = form
        return render(request, 'account/change_password.html', context)


# User Login View
def login(request):
    if request.user.is_authenticated:
        return redirect('trendsup:index')
    context = {}
    # Footer
    context['foot'] = repeated.footer()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            request.session['username'] = username
            request.session['id'] = user.id
            return redirect('trendsup:index')
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('account:login')
    else:
        return render(request, 'account/login.html', context)


# User Logout View
def logout(request):
    try:
        del request.session['username']
        print('deleted')
    except:
        pass
    auth.logout(request)
    return redirect('trendsup:index')


# Must Authenticate View
def must_authenticate(request):
    context = {}

    # Footer
    context['foot'] = repeated.footer()

    return render(request, 'account/must_authenticate.html', context)


@login_required(login_url='account:must_authenticate')
def change_password_done(request):
    context = {}


    # Footer
    context['foot'] = repeated.footer()

    context['done'] = 'Your Password Has Been Changed Successfully.'
    return render(request, 'registration/password_change_done.html', context)
