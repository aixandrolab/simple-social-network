from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from profiles.models import Profile


@login_required()
def profile_search_view(request):
    profile_list = Profile.objects.all()
    context = {
        'profile_list': profile_list,
    }
    return render(request, 'profiles/profile_search.html', context)
