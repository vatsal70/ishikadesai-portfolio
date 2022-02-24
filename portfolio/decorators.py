from django.contrib.auth.decorators import user_passes_test, login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse

# Created a custom decorator
def dec_func(user):
    if user.is_superuser == True:
        return user
    return None

user_login_required = user_passes_test(dec_func, login_url='/authentication_required/')

def active_user_required(view_func):
    decorated_view_func = login_required(user_login_required(view_func))
    return decorated_view_func


def authentication_required(request):
    if request.user.is_authenticated:
        data = {
            'error': '403',
            'message': 'Dear user you are not authorized to access the contents.'
        }
    else:
        data = {
            'error': '401',
            'message': 'Dear user you are currently not logged-in to visit the page.'
        }
    return render(request, 'frontend/login_required.html', data)

class RedirectMixin:
    """
    Redirect to redirect_url if the test_func() method returns False.
    """

    redirect_url = '/authentication_required/'

    def get_redirect_url(self):
        """
        Override this method to override the redirect_url attribute.
        """
        redirect_url = self.redirect_url
        if not redirect_url:
            raise ImproperlyConfigured(
                '{0} is missing the redirect_url attribute. Define {0}.redirect_url or override '
                '{0}.get_redirect_url().'.format(self.__class__.__name__)
            )
        return str(redirect_url)

    def test_func(self):
        raise NotImplementedError(
            '{0} is missing the implementation of the test_func() method.'.format(self.__class__.__name__)
        )

    def get_test_func(self):
        """
        Override this method to use a different test_func method.
        """
        return self.test_func

    def dispatch(self, request, *args, **kwargs):
        test_result = self.get_test_func()()
        if not test_result:
            return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)





class LoggedInRedirectMixin(RedirectMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser