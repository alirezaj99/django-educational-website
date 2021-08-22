"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from ckeditor_uploader.views import upload
from azbankgateways.urls import az_bank_gateways_urls
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('index_app.urls', namespace='index')),
    path('', include('course_app.urls', namespace='course')),
    path('bankgateways/', az_bank_gateways_urls()),
    path('', include('order_app.urls', namespace='order')),
    path('', include('blog_app.urls', namespace='blog')),
    path('account/', include('account_app.urls', namespace='account')),
    path('editor/uploads/', login_required(upload), name='ckeditor_upload'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/login/', RedirectView.as_view(url='/account/login/')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    # ADD ROOT MEDIA FILES
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
