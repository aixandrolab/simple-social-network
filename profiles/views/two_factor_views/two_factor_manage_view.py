from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


@login_required()
@require_http_methods(['GET', 'POST'])
def two_factor_manage_view(request):
    user = request.user

    if request.method == 'POST' and 'regenerate_backup_codes' in request.POST:
        backup_codes = user.profile.generate_backup_codes()
        request.session['backup_codes'] = backup_codes
        request.session['backup_codes_shown'] = False
        messages.success(request, 'New backup codes have been generated!')
        return redirect('profiles:two_factor_backup_codes')

    context = {
        'is_2fa_active': user.profile.is_2fa_active,
        'has_backup_codes': bool(user.profile.backup_codes)
    }
    return render(request, 'profiles/two_factor_templates/two_factor_manage.html', context)
