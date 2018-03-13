from django.contrib import admin

from .models import Post, Tag, Comment, profile_c, TagAdmin, PostAdmin

admin.site.register(Post,PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)
admin.site.register(profile_c)
