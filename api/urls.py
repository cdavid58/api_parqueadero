from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^user/', include('user.urls')),
    url(r'^parking_lot/', include('parking_lot.urls')),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^history/', include('history.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)