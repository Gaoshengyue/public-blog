from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserInfo)
admin.site.register(Blog)
admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(HomeCategory)
admin.site.register(Comment)
admin.site.register(ArticleUpDown)
admin.site.register(ArticleDetail)
admin.site.register(Article2Tag)
admin.site.register(SiteCategory)
admin.site.register(SiteDetaiCategory)
