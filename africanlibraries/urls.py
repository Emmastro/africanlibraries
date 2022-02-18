from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
#from jet_django.urls import jet_urls


urlpatterns = [

    path('accounts/', include('account.urls')),
    path('', include('schools.urls')),
    path('messaging/', include('messaging.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns+=static(r'^static/(?P<path>.*)$', document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#handler404 = 'africanlibraries.views.my_custom_page_not_found_view'
# the custom 404 hadler make a CSRF Error on production

