from django.contrib import admin
from wmcomment.models import BaseComment, NestedComment

# AdminSite Registration
admin.site.register(BaseComment)
admin.site.register(NestedComment)
