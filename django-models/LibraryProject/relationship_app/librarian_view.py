from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from relationship_app.utils import has_role

@user_passes_test(lambda u: has_role(u, 'Librarian'))
def librarian_view(request):
    return HttpResponse("Hello Librarian! You can manage library content here.")