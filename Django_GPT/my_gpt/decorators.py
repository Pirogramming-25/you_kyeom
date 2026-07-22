from functools import wraps
from django.shortcuts import redirect

def model_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = "/accounts/login/"
            return redirect(f"{login_url}?next={request.path}&required=1")
        return view_func(request, *args, **kwargs)
    return _wrapped_view