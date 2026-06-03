from django.contrib import messages

from django.shortcuts import render, redirect
from django.urls import reverse

from core.forms.register_form import RegisterForm
from core.services.email_service import Email
from profiles.models.email_verification_token_model import EmailVerificationToken



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        try:
            if form.is_valid:
                new_user = form.save(commit=False)

                new_user.set_password(form.cleaned_data['password'])
                new_user.save()

                token = EmailVerificationToken.create_token(new_user)

                url = request.build_absolute_uri(
                    reverse('core:confirm_register', kwargs={'token': token.token})
                )

                Email.verification(new_user.email, url, new_user.username)
                messages.success(request,
                                 "User is successfully created!"
                                 " Now, you need to confirm your registration."
                                 " Please check your E-mail"
                                 )
                return redirect('core:login')
        except Exception as e:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'core/auth/register.html', {'form': form})
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'core/auth/register.html', context)
