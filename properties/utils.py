from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get from cache
    properties = cache.get('all_properties')
    
    if properties is None:
        # If not in cache, fetch from DB
        properties = list(Property.objects.all().values("id", "title", "description", "price"))
        # Save to cache for 1 hour (3600s)
        cache.set('all_properties', properties, 3600)
    
    return properties
