from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging


def get_all_properties():
    # Try to get from cache
    properties = cache.get('all_properties')
    
    if properties is None:
        # If not in cache, fetch from DB
        properties = list(Property.objects.all().values("id", "title", "description", "price"))
        # Save to cache for 1 hour (3600s)
        cache.set('all_properties', properties, 3600)
    
    return properties

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    """
    conn = get_redis_connection("default")
    info = conn.info("stats")

    keyspace_hits = info.get("keyspace_hits", 0)
    keyspace_misses = info.get("keyspace_misses", 0)

    total = keyspace_hits + keyspace_misses
    hit_ratio = (keyspace_hits / total) if total > 0 else 0

    metrics = {
        "keyspace_hits": keyspace_hits,
        "keyspace_misses": keyspace_misses,
        "hit_ratio": hit_ratio,
    }

    # Log the metrics for analysis
    logger.info(f"Redis Cache Metrics: {metrics}")

    return metrics
