"""cnblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from blog import views
from cnblog import settings
from django.views.static import  serve


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^get_valid_img/', views.get_valid_img),
    url(r'^index/$', views.index),
    url(r'^$', views.index),
    url(r'^pc-geetest/register', views.pcgetcaptcha, name='pcgetcaptcha'),
    url(r'^zhuce/', views.zhuce),
    url(r'^headp/', views.headp),
    url(r'^logout/', views.log_out),
    url(r'^(?P<username>\w+)/article/(?P<aid>\d+)', views.article),

    url(r'^media/(?P<path>.*)$',serve,{"document_root":settings.MEDIA_ROOT}),
    url(r'^index/(?P<para>\d+)',views.index),

    url(r'^up/$', views.up),
    url(r'^adelete/$', views.adelete),
    url(r'^backend/edit_article/(?P<id>\d+)$', views.edit_article),
    url(r'^down/$', views.down),
    url(r'^get_comment_tree/(\d+)$', views.get_comment_tree),
    url(r'^comment/$', views.comment),
    url(r'^backend/add_article/$', views.add_article),
    url(r'^backend/(?P<username>\w+)/$', views.backend),
    url(r'^backendd/$', views.backendd),
    url(r'^upload_img/',views.upload_img),
    url(r'^zblog/',views.zblog),
    url(r'^addcate/',views.addcate),
    url(r'^addtag/',views.addtag),
    url(r'^logedit/',views.logedit),



    # url(r'^comment/$', views.comment),
    # home_site(request,username="",condition="",para="")
    url(r'^(?P<username>\w+)/(?P<condition>tag|cate|archive)/(?P<para>.*)', views.home_site),
    url(r'^(?P<username>\w+)/$', views.home_site),  # home_site(request,username='yuan')





]
