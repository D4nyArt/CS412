from django.contrib import admin
from django.urls import path, include  
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Django admin interface
    path("admin/", admin.site.urls),
    
    # Application URL
    path("dadjokes/", include("dadjokes.urls")),
    path("quotes/", include("quotes.urls")),          
    path("restaurant/", include("restaurant.urls")),  
    path("mini_insta/", include("mini_insta.urls")),
    path("voter_analytics/", include("voter_analytics.urls")),  
]

# Serve static files (CSS, JavaScript, images) 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files (user uploads) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
