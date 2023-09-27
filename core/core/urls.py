from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include(('training_placement.urls', 'training_placement'), namespace='training_placement')),
    path('pages/',include('django.contrib.flatpages.urls'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
