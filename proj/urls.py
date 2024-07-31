from django.contrib import admin
from django.urls import path,include
from app1.views import *

urlpatterns = [
    path('', SignIn.as_view()),
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
    # path('GetCookies/', GetCookies.as_view()),
]

