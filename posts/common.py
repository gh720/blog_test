import time

def user_uploads_path(instance,filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    time_part=time.strftime('%Y%m%d_%H%M%S', time.localtime())
    path = 'user_{0}/{1}/{2}'.format(instance.user.id, time_part, filename)
    return path
