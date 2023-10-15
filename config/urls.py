from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('youCantFindIt/', admin.site.urls),
    path('', include('facades.urls')),
    path('', include('stuff.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('blog/', include('blog.urls')),
    path('dashboard/', include('administratorship.urls')),
]

if not settings.DEBUG:
    handler404 = 'facades.views.handler404'

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
