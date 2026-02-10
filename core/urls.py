from django.contrib import admin
from django.urls import path
from visitors import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.parent_login, name='login'), # Home is now Login
    path('dashboard/', views.dashboard, name='dashboard'),
    path('scan/<int:visit_id>/', views.scan_qr, name='scan_qr'),
    path('logout/', views.logout_view, name='logout'),
]