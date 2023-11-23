"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # new
from django.conf.urls.static import static #new
from trackandtrace import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginPage),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view_registration/', views.viewRegistration, name='view_registration'),
    path('new_registration/', views.newRegistration, name='new_registration'),
    path('production/', views.Production, name='production'),
    path('in_stock/', views.InStock, name='in_stock'),
    path('out_stock/', views.OutStock, name='out_stock'),
    path('server/', views.run_server, name='server'),
    path('transportation/', views.run_transportation, name='transportation'),
    path('logout/', views.logoutUser, name='logout'),
    path('tracking_items/', views.tracking_items, name='tracking_items'),
    path('download_invoice_pdf/', views.download_invoice_pdf, name='download_invoice_pdf'),
]


if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
