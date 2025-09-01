from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property
from .utils import get_all_properties

@cache_page(60 * 15)  # cache for 15 minutes
def property_list(request):
    properties = Property.objects.all().values("id", "title", "description", "price")
    return JsonResponse({"data": list(properties)}, safe=False)

def property_list(request):
    properties = get_all_properties()
    return JsonResponse({"data": properties}, safe=False)
