"""lamonte URL Configuration

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

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin

admin.site.site_header = 'Lamonte'

# Text to put at the end of each page's <title>.
admin.site.site_title = 'Lamonte site admin'

# Text to put in each page's <h1>.
admin.site.site_header = 'Lamonte London'

# Text to put at the top of the admin index page.
admin.site.index_title = 'Lamonte administration'


urlpatterns = [
    url(r'^api/', include('lamonte_api.urls')),
    url(r'^api/admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
