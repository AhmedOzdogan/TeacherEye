from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from functools import wraps

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role != role:
                return HttpResponseForbidden("Access denied.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

manager_required = role_required('manager')
admin_required = role_required('admin')