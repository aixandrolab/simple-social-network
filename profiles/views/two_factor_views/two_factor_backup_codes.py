# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required()
def two_factor_backup_codes_view(request):
    backup_codes = request.session.get('backup_codes', [])
    codes_shown = request.session.get('backup_codes_shown', [])
    if not backup_codes:
        return redirect('profiles:two_factor_manage')

    if not codes_shown:
        request.session['backup_codes_shown'] = True
    else:
        return redirect('profiles:two_factor_manage')

    context = {
        'backup_codes': backup_codes
    }
    return render(request, 'profiles/two_factor_templates/two_factor_backup_codes.html', context)
