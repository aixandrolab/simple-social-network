# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required()
def logout_view(request):
    logout(request)
    return redirect('core:login')
