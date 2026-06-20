# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
import base64
from io import BytesIO

import pyotp
import qrcode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from profiles.forms.enable_two_factor_form import Enable2FAForm


@login_required()
@require_http_methods(['GET', "POST"])
def two_factor_setup_view(request):
    user = request.user

    if user.profile.is_2fa_active:
        messages.warning(request, '2FA already activated!')
        return redirect('profiles:two_factor_manage')

    if not user.profile.two_fa_secret:
        user.profile.two_fa_secret = pyotp.random_base32()
        user.profile.save(update_fields=['two_fa_secret'])

    totp = user.profile.get_totp_device()

    if request.method == 'POST':
        form = Enable2FAForm(user, request.POST)
        if form.is_valid():
            user.profile.enable_2fa(user.profile.two_fa_secret)
            backup_codes = user.profile.generate_backup_codes()

            request.session['backup_codes'] = backup_codes
            request.session['backup_codes_shown'] = False

            messages.success(request, '2FA successfully enabled to your account.')
            return redirect('profiles:two_factor_backup_codes')
    else:
         form = Enable2FAForm(user)

    issuer = "Simple-Social-Network-"
    username = f'{user.username}'.replace('_', '-')
    uri = totp.provisioning_uri(name=username, issuer_name=issuer)

    qr = qrcode.QRCode(version=1, box_size=30, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    context = {
        'form': form,
        'qr_code': qr_code_base64,
        'secret': user.profile.two_fa_secret,
        'uri': uri
    }
    return render(request, 'profiles/two_factor_templates/two_factor_setup.html', context)
