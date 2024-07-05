"""
URL configuration for otp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from app1.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('register/',RegisterAPI.as_view()),
    path('verifyotp/<email>',VerifyOTP.as_view()),#baaki+ui
    path('verifyotponly/',VerifyOTPOnly.as_view()),    
    path('verifyemail/',VerifyEmail.as_view()),#baaki+ui
    path('login/', SignIn.as_view()),
    path('logout/', SignOut.as_view()),
    path('adminmonitor/', AdminMonitor.as_view()),#baaki
    path('resourcedetail/<resource>', ResourceDetail.as_view()),#put baaki
    path('auth/',include('rest_framework.urls'),name = "rest_framework"),
    path('grant/<int:booking_id>',AcceptRequest.as_view()),
    path('deny/<int:booking_id>',DenyRequest.as_view()),
    path('pendingrequest/',PendingRequests.as_view()),
    path('userrequests/', UserRequests.as_view()),
    path('UserInfo/', UserInfo.as_view()),
]

