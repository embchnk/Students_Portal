from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # when user request anything that starts with users - go to users.urls to find out what to do
    url(r'^users/', include('users.urls', namespace="users")),
    url(r'^users/', include('recipes.urls', namespace="recipes")),
    #url(r'^users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
