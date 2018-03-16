import time

from django.db.models import Count


def get_all_url_entries(urllist, namespace=None, depth=0):
    for entry in urllist:
        if hasattr(entry, 'url_patterns'):
            yield from get_all_url_entries(entry.url_patterns, entry.namespace or namespace, depth + 1)
        else:
            yield [entry,namespace,depth]

def user_uploads_path(instance,filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    time_part=time.strftime('%Y%m%d_%H%M%S', time.localtime())
    path = 'user_{0}/{1}/{2}'.format(instance.user.id, time_part, filename)
    Count
    return path

def response_decode(response, enc='utf-8'):
    return response.content.decode('utf-8')