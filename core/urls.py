from django.contrib import admin
from django.urls import path
from visitors import views 

urlpatterns = [
    # Add this line to fix the 404 error for /admin/
    path('admin/', admin.site.urls), 
    
    path('', views.home, name='home'), 
    path('login/', views.parent_login, name='parent_login'),
    
    # This is the path your 'Admin Portal' button uses
    path('admin/', views.admin, name='admin_dashboard'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('scan/<int:visit_id>/', views.scan_qr, name='scan_qr'),
]