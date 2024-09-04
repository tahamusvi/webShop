from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .settings import admin_url
from facades.models import ConfigShop
from django.views.generic import TemplateView

# news = ConfigShop.objects.get(current=True).news

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path(f'{admin_url}/', admin.site.urls),
    path('', include('facades.urls')),
    path('', include('stuff.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('blog/', include('blog.urls')),
    path('dashboard/', include('administratorship.urls')),
    path('704910.txt', TemplateView.as_view(template_name='facades/704910.txt', content_type='text/plain')),
]

# if(news):
#     urlpatterns += [
#         path('blog/', include('blog.urls')),
#     ]

if not settings.DEBUG:
    handler404 = 'facades.views.handler404'

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
