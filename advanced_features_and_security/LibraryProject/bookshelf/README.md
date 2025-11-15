
# Permissions and Groups Setup
---
This Django application uses custom permissions and groups to control access to certain actions.
---
## Custom Permissions

The following custom permissions have been defined in the models:

- can_view: allows users to view instances of the model
- can_create: allows users to create new instances of the model
- can_edit: allows users to edit existing instances of the model
- can_delete: allows users to delete instances of the model

## Groups and Permissions

The following groups have been set up with assigned permissions:

- Editors: has can_edit and can_create permissions
- Viewers: has can_view permission
- Admins: has all permissions (can_view, can_create, can_edit, can_delete)

## Enforcing Permissions in Views

Permissions are enforced in views using the @permission_required decorator. For example:


from django.contrib.auth.decorators import permission_required

@permission_required('app_name.can_edit', raise_exception=True)
def edit_view(request):
    # view code here


## Testing Permissions

To test permissions, create test users and assign them to different groups. Log in as these users and attempt to access various parts of the application to ensure that permissions are applied correctly.

This setup provides a robust system for managing access to different parts of the application.