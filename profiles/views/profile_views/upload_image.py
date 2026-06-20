# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from profiles.utils.validate_image import validate_image


@login_required()
def upload_image_view(request):
    user = request.user

    if request.method == 'POST' and user.id == request.user.id:
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            is_valid, error_msg = validate_image(avatar)

            if not is_valid:
                messages.error(request, error_msg)
                return redirect('profiles:profile_detail', slug=user.profile.slug)

            user.profile.avatar = avatar
            user.save()
            messages.success(request, 'Your avatar was successfully changed.')

    return redirect('profiles:profile_detail', slug=user.profile.slug)
