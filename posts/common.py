import time

def get_all_url_entries(urllist, depth=0):
    for entry in urllist:
        yield entry
        if hasattr(entry, 'url_patterns'):
            get_all_url_entries(entry.url_patterns, depth + 1)

def user_uploads_path(instance,filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    time_part=time.strftime('%Y%m%d_%H%M%S', time.localtime())
    path = 'user_{0}/{1}/{2}'.format(instance.user.id, time_part, filename)
    return path

def response_decode(response, enc='utf-8'):
    return response.content.decode('utf-8')