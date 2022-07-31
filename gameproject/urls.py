"""gameproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from gameapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('', views.index),
    path('login/', views.login1),




    #admin
    path('adminhome/', views.adminhome),
    path('addcategory/', views.addcategory),
    path('adminviewuser/', views.adminviewuser),
    path('adminviewpayment/', views.adminviewpayment),
    path('adminviewbooking/', views.adminviewbooking),
    path('adminaddproduct/', views.adminaddproduct),
    path('adminviewdemand/', views.adminviewdemand),






    #user
    path('userhome/', views.userhome),
    path('userreg/', views.userreg),
    path('viewcategory/', views.viewcategory),
    path('viewgames/', views.viewgames),
    path('payment/', views.payment),
    path('payment1/', views.payment1),
    path('payment2/', views.payment2),
    path('payment3/', views.payment3),
    path('payment4/', views.payment4),
    path('download/', views.download),
    path('demandgame/', views.demandgame),
    path('askq/', views.askq),
    path('question/', views.question),
    path('viewquestion/', views.viewquestion),
    path('answeraq/', views.answerq),




    
]
