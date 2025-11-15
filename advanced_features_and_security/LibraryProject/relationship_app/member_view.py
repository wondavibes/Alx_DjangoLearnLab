from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from relationship_app.utils import has_role


@user_passes_test(lambda u: has_role(u, "Member"))
def member_view(request):
    return HttpResponse("Hi Member! Enjoy browsing your library.")
