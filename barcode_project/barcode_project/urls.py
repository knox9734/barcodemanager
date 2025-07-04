from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),  # include your app's URLs
]

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Serve media files (like barcode images) during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
