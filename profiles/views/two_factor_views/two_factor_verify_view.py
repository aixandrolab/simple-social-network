from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from profiles.forms.two_factor_login_form import TwoFactorLoginForm


@never_cache
@require_http_methods(['GET', 'POST'])
def two_factor_verify_view(request):
    user_id = request.session.get('2fa_user_id')

    if not user_id:
        messages.error(request, 'Session expired. Please login again.')

    user = get_object_or_404(User, id=user_id)
    session_key = f"2fa_failed_attempts_{user_id}"
    failed_attempts = request.session.get(session_key, 0)
    max_attempts = 3
    remaining_attempts = max_attempts - failed_attempts

    if failed_attempts >= max_attempts:
        messages.error(request, 'Too many failed attempts! Please login again.')
        request.session.pop('2fa_user_id', None)
        request.session.pop('2fa_next_url', None)
        request.session.pop(session_key, None)
        return redirect('core:login')

    if request.method == 'POST':
        form = TwoFactorLoginForm(user, request.POST)
        if form.is_valid():
            request.session.pop('2fa_user_id', None)
            request.session.pop('2fa_next_url', None)
            request.session.pop(session_key, None)

            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')

            return redirect('profiles:profile_detail')
        else:
            failed_attempts += 1
            request.session[session_key] = failed_attempts
            remaining_attempts = max_attempts - failed_attempts

            if remaining_attempts > 0:
                messages.error(request, 'Invalid authentication code! Please try again.')
            else:
                messages.error(request, 'Invalid authentication code! No attempts remaining')
                request.session.pop('2fa_user_id', None)
                request.session.pop('2fa_next_url', None)
                return redirect('core:login')

            form = TwoFactorLoginForm(user)
    else:
        form = TwoFactorLoginForm(user)

    context = {
        'form': form,
        'user': user,
        'remaining_attempts': remaining_attempts,
        'failed_attempts': failed_attempts,
        'max_attempts': max_attempts
    }
    return render(request, 'profiles/two_factor_templates/two_factor_verify.html', context)
