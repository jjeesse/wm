from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

#Custom Django-AllAuth Redirects
class CustomAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/profile/"
        return path.format(username=request.user.username)