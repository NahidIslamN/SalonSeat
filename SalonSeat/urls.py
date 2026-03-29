
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HelloHorld(APIView):
    def get(self, request):
        return Response(
            {
               "message":"Hello Wrold!"
                
            },
            status=status.HTTP_200_OK
        )

urlpatterns = [
    path('', HelloHorld.as_view(), name='hello'),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('auths.urls')),
    path('api/v1/', include('chats.urls')),
    path('api/v1/profiles/', include('profiles.urls')),
    path('api/v1/owners/', include('salun_owner_app.urls')),
    path('api/v1/admin/', include('admin_dashboard.urls')),
    
]
# path('blog/', include('blog.urls'))

if settings.DEBUG:
       
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
