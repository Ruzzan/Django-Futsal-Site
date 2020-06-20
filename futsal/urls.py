from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.views.generic.base import RedirectView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',RedirectView.as_view(url='futsal/')),
    path('accounts/', include('accounts.urls')),
    path('futsal/',include('futsalApp.urls')),
    path('booking/',include('booking.urls')),
    path('team/',include('team.urls')),
    path('match/',include('match.urls')),
    ############# API ENDPOINTS #############
    path('api/auth/',include('accounts.api.urls')),
    path('api/booking/',include('booking.api.urls')),
    path('api/futsal/',include('futsalApp.api.urls')),
    path('api/team/',include('team.api.urls')),
    path('api/match/',include('match.api.urls')),
    ############ Social Authentication #########    
    path('oauth/',include('social_django.urls',namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
