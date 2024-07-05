from django.core.cache import cache

from postmails.models import Mailing
from config.settings import CACHE_ENABLED


def get_mailing_from_cache():
    if not CACHE_ENABLED:
        return Mailing.objects.all()

    key = "mailing_list"
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = Mailing.objects.all()
    cache.set(key, mailings)
    return mailings
