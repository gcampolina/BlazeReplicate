from django.contrib import admin
from django.urls import path
from webapp import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('conta/', views.conta, name='conta'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
