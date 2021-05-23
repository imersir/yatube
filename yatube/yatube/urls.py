from django.conf import settings as st
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa

urlpatterns = [
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
]

if st.DEBUG:
    urlpatterns += static(st.MEDIA_URL, document_root=st.MEDIA_ROOT)
    urlpatterns += static(st.STATIC_URL, document_root=st.STATIC_ROOT)
