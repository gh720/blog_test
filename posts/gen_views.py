from django.http import HttpResponse
from django.views import View

import


class password_reset_view_c(View):
    def get(self,request):
        response=HttpResponse(mimetype="image/png")

