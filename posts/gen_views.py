from django.http import HttpResponse
from django.views import View

import auxiliary.lightning_logo as ll

class lightning_logo_view_c(View):
    def get(self,request):
        response=HttpResponse(content_type="image/png")
        image = ll.generate_lightning_logo()
        image.save(response, 'PNG')
        return response




