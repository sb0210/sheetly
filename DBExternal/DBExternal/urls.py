"""DBExternal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from sheets.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',login),
    url(r'^/$',login),
    url(r'^login/$',login),
    url(r'^signup/$',signup),
    url(r'^signin/$',signin),
    url(r'^signout/$',signout),
    url(r'^home/$',home),
    url(r'^home/my_docs/$',my_docs),
    url(r'^home/shared_docs/$',shared_docs),
    url(r'^home/docs/create_doc/$',doc_create_page),
    url(r'^home/docs/([^/]+)/$',doc_page),
    url(r'^home/docs/([^/]+)/create_sheet/$',sheet_create_page),
    url(r'^home/docs/([^/]+)/update_sheet/$',sheet_update_page),
    url(r'^home/docs/([^/]+)/sharing/$',doc_sharing_page),
    url(r'^home/docs/([^/]+)/delete_data/$',delete_data),
    url(r'^home/docs/([^/]+)/add_column/$',add_column),
    url(r'^home/docs/([^/]+)/add_row/$',add_row),
    url(r'^home/docs/([^/]+)/delete_sheet/$',delete_sheet),
    url(r'^home/docs/([^/]+)/delete_doc/$',delete_doc),
    url(r'^home/docs/([^/]+)/rename_doc/$',rename_doc),
    url(r'^home/docs/([^/]+)/upload_image/$',upload_image),
    url(r'^delete_everything/$',delete_everything),
    url(r'^profile/$',profile),
    url(r'^profile/edit_data/$',edit_data),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

