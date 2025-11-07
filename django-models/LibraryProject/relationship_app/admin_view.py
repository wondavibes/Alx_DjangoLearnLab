from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from relationship_app.utils import has_role  # or define inline


@user_passes_test(lambda u: has_role(u, "Admin"))
def admin_view(request):
    return HttpResponse("Welcome, Admin! You have access to this view.")
