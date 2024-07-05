from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import *
from .emails import *
from datetime import datetime, timedelta
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.utils.crypto import get_random_string
from passlib.hash import django_pbkdf2_sha256
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db.models import Q
from datetime import timedelta
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.contrib.auth import get_user_model

User = get_user_model()

# from django.views.decorators.csrf import ensure_csrf_cookie

# class RegisterAPI(APIView):
#     def post(self,request):
#         try:
#             data=request.data
#             serializer=PasswordResetSerializer(data=data)
#             if serializer.is_valid():
#                 user_mail=User.objects.filter(email=serializer.validated_data['email'])
#                 if user_mail:
#                     serializer.save()
#                     print("account exists")
#                     send_otp_via_email(serializer.data['email'])
#                     return Response({
#                         'status':200,
#                         'message':'please check mail',
#                         'data':serializer.data, 
#                     })
                
            
#                 return Response({
#                     'status':400,
#                     'message':'something went wrong',
#                     'data':'Account with this mail does not exist',

#                 })
#             # print("87909")
#             return Response({
#                     'status':400,
#                     'message':'something went wrong',
#                     'data':serializer.errors,

#                 })
            
#         except Exception as e:
#             # print("123s")
#             print(e)
#             return Response({'key': 'value'}, status=status.HTTP_200_OK)
        
class VerifyOTPOnly(APIView):
#verifying otp for pass reset
    def post(self, request):
      
        data=request.data
        serializer=VerifyOTPOnlySerializer(data=data)
       
        if serializer.is_valid():
            
            otp=serializer.data['otp']
            email = serializer.data['mail']
            # serializer.data['mail']=email
            user=User.objects.get(email=email)
            
            if not user:
                return Response({
                'status':400,
                'message':'something went wrong',
                'data':'invalid mail',

            })



            if user.otp!=otp:
                return Response({
                'status':400,
                'message':'something went wrong',
                'data':'wrong otp',

            })

            if(user.expires_at < timezone.now()):
                return Response({
                    'status': 400,
                'message':'OTP Validity expired',
                'data':'Resend OTP',

            })
            
            return Response({
            'status':status.HTTP_200_OK,
            'message':'Account verified',
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # except Exception as e:
        #     return Response({'key': 'value'}, status=status.HTTP_200_OK)
        
class VerifyOTP(APIView):
#verifying otp for pass reset
    def post(self, request, email):
      
        data=request.data
        serializer=VerifyOTPSerializer(data=data)
       
        if serializer.is_valid():
            
            otp=serializer.data['otp']
            new_p = serializer.data['new_password']
            # serializer.data['mail']=email
            user=User.objects.get(email=email)
            
            if not user:
                return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'message':'something went wrong',
                'data':'invalid mail',

            })



            if user.otp!=otp:
                return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'message':'something went wrong',
                'data':'wrong otp',
            })

            if(user.expires_at < timezone.now()):
                return Response({
                'message':'OTP Validity expired',
                'data':'Resend OTP',

            })


            # user=user.first()
            user.set_password(new_p)
            user.password=django_pbkdf2_sha256.hash(new_p)
            user.is_verified=True
            user.save()

            print(user.password)
            
            return Response({
            'status':status.HTTP_200_OK,
            'message':'Account verified',
            })


        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # except Exception as e:
        #     return Response({'key': 'value'}, status=status.HTTP_200_OK)
        
class VerifyEmail(APIView):
   
    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = EmailVerificationSerializer(data=request.data)
        print("!23")
        if serializer.is_valid():
            print("8977")
            user=User.objects.filter(email=serializer.validated_data['mail'])
            if user:
                print("ll ")
                print(serializer.validated_data['mail'])
                send_otp_via_email(serializer.validated_data['mail'])

                
                return Response({
                    'status':status.HTTP_200_OK,
                    'message':'email sent',
                    'data':serializer.data,
                })

            #user with that mail does not exist
            return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message':'something went wrong',
                    'data':'Account with this mail does not exist',

                })
            
        return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message':'something went wrong',
                    'data':serializer.errors,

                })

    
class SignIn(APIView):
   
    def get_object(self, queryset=None):
        return self.request.user
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user.id != None:
            return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message':'something went wrong',
                    'data':'An User already logged in',
                })
      
    
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                    user=User.objects.get(email=serializer.validated_data['email'])
                
                    print("k")
                    if authenticate(request, username=None, email=serializer.validated_data['email'], password=serializer.validated_data['password']):
                        login(request, user)
                        return Response({
                            'status':status.HTTP_200_OK,
                            'message':'User logged in',
                            'data':serializer.data
                        })
                    else:
                        return Response({
                            'status':status.HTTP_400_BAD_REQUEST,
                            'message':'Wrong password',
                        })
            except  ObjectDoesNotExist:
                        
                        return Response({
                            'status':status.HTTP_400_BAD_REQUEST,
                            'message':'User with this mail does not exist',
                        
                        })
        
        return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message':'something went wrong',
                    'data':serializer.errors,

                })
    
class SignOut(APIView):
   
    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            usr = request.user
            logout(request)
            return Response({
                'status':status.HTTP_200_OK,
                'message':'User logged out',
                'data':usr.email,
            })
        except:
            return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message':'something went wrong',

                })
    
# @ensure_csrf_cookie
class AdminMonitor(APIView):
   
    def get_object(self, queryset=None):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            if user.is_admin == True:
                if not User.objects.filter(email=serializer.validated_data['mail']).exists():
                    return Response({
                    'status':status.HTTP_200_OK,
                    'message':'User not found',
                })
                usr=User.objects.get(email=serializer.validated_data['mail'])
                e = usr.email
                usr.delete()
                return Response({
                    'status':status.HTTP_200_OK,
                    'message':'User deleted',
                    'user':e,
                })
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'message':'Permission denied',
            })
        return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message':'something went wrong',
                    'data':serializer.errors,

                })
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        serializer = AdminAddSerializer(data=request.data)
        if serializer.is_valid():
            if user.is_admin == True:
                temp_pass = get_random_string(length=10, allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789")
                usr=User.objects.create(email=serializer.validated_data['mail'], password=django_pbkdf2_sha256.hash(temp_pass), role=serializer.validated_data['role'])
                e = usr.email
                send_random_password(serializer.validated_data['mail'], temp_pass)
                return Response({
                    'status':status.HTTP_200_OK,
                    'message':'User created. Mail Sent',
                    'user':e,
                })
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'message':'Permission denied',
            })
        return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message':'something went wrong',
                    'data':serializer.errors,

                })
    
class ResourceDetail(APIView):
   
    def get_object(self, queryset=None):
        return self.request.user

    #Deatils of the booked session of a resource for 6 days after a particular date.
    def put(self, request, resource, *args, **kwargs):
        # self.object = self.get_object()

        serializer=Getdate(data=request.data)
        #returns booking of that particular resource for the next 7 days
        if request.user.is_authenticated:
            if serializer.is_valid():
               

                curr_date = serializer.validated_data['date']
                
                # bookings_list = []
                # list of dictionary
                serialized_bookings = []
        
                for i in range (0,7):
                    bookings=Booking.objects.filter(
                        resource=resource,
                        date=curr_date, 
                        all_true = True,                   
                    )
                    for booking in bookings:
                        # dictionary 
                        serialized_booking = {
                            'start_time': booking.start_time,
                            'end_time': booking.end_time,
                            'booked_by': booking.user.email,
                        }
                        serialized_bookings.append(serialized_booking)
                    
                    
                    curr_date = curr_date + timedelta(days = 1)

                
           
                return JsonResponse({
                    'status': status.HTTP_200_OK,
                    'message': 'Showing details',
                    # 'booking_allowed': e,
                    'bookings': serialized_bookings
                })
            else:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Something went wrong',
                    'errors': serializer.errors
                })
            
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Permission denied'
            })
    
        
            
    #Booking of the resource.
    def post(self, request, resource, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        data['user'] = user.id
        # data.res
        data['resource'] = resource

        resource = Resource.objects.get(pk=resource)
        resource_instance = resource.userperms
        data['userperms'] = resource_instance

        serializer = BookingSerializer(data=data)
        
        if serializer.is_valid():
            if user.is_authenticated:
                  
                bookings=Booking.objects.filter(resource=resource,date=serializer.validated_data['start_time'].date())   #doubt
                conflict_present=False
                for bookingg in bookings:
                    if bookingg.all_true==True:
                        if serializer.validated_data['start_time']>=bookingg.start_time and serializer.validated_data['start_time']<=bookingg.end_time: 
                            print("already booked")
                            conflict_present=True
                            break
                          

                        elif serializer.validated_data['end_time']>=bookingg.start_time and serializer.validated_data['end_time']<=bookingg.end_time: 
                            print("already booked")
                            conflict_present=True
                            break
                           
                        elif serializer.validated_data['start_time']<=bookingg.start_time and serializer.validated_data['end_time']>=bookingg.end_time:
                            print("already booked")
                            conflict_present=True
                            break
               
                if not conflict_present:
                    # curr_start_time=data['start_time']
                    # curr_end_time=data['end_time']
            
                    serializer.save()
                            

                    return Response({
                        'status': status.HTTP_200_OK,
                        'message': 'Permission Created',
                        # 'booking_id': bookingg.booking_id
                    })
                else:
                    
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Conflicting Requests',
                        # 'booking_id': bookingg.booking_id
                    })

            else:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'User Not Authencticated',
                    
                })

        
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                 'message': 'Something went wrong',
                'errors': serializer.errors
            })
        user = request.user
        data = request.data.copy()
        data['user'] = user.id
        # data.res
        data['resource'] = resource

        resource = Resource.objects.get(pk=resource)
        resource_instance = resource.userperms
        data['userperms'] = resource_instance
        data['date']=data['start_time'].date()

        serializer = BookingSerializer(data=data)
        
        if serializer.is_valid():
            if user.is_authenticated:
                # booking = serializer.save()/  
                bookings=Booking.objects.filter(resource=resource,date=data['date'])   #doubt
                conflict_present=False
                for bookingg in bookings:
                    if bookingg.all_true==True:
                        if data['start_time']>=bookingg.start_time and data['start_time']<=bookingg.end_time: 
                            print("already booked")
                            conflict_present=True
                            break
                          

                        elif data['end_time']>=bookingg.start_time and data['end_time']<=bookingg.end_time: 
                            print("already booked")
                            conflict_present=True
                            break
                           
                        elif data['start_time']<=bookingg.start_time and data['end_time']>=bookingg.end_time:
                            print("already booked")
                            conflict_present=True
                            break
               
                if conflict_present:
                    curr_start_time=data['start_time']
                    curr_end_time=data['end_time']
                    resource_head=resource.resource_head

                    print(resource_head) 
                            

                    return Response({
                        'status': status.HTTP_200_OK,
                        'message': 'Permission Created',
                        'booking_id': bookingg.booking_id
                    })
                else:
                    return Response({
                        'status': status.HTTP_200_OK,
                        'message': 'Conflicting Requests',
                        # 'booking_id': bookingg.booking_id
                    })

            else:
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'User Not Authencticated',
                    
                })

        
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                 'message': 'Something went wrong',
                'errors': serializer.errors
            })
           
            # # to upate partially we pass instance as a paramter
            # serializer=acceptrequestSerializer(booking_instance,data=request.data)
            # if serializer.is_valid():
            #     accept_value = serializer.validated_data.get('accept')
            #     if accept_value:
            #         curr_ind+=1
            #         booking_instance.list.append(True)
            #         serializer.save()
            #         print("hello")
            #         # curr_ind+=1
            #         # percent=0
                    
            #         for item in booking_instance.list:
            #            if item==True:
            #                cnt+=1
            #         percent=int((cnt/required)*100)

            #         if cnt==required:
            #             return Response(
            #                 {'message':"booking done"
            #                 }
            #             )
            #         else :
            #             return Response(
            #                 {'message':f"{percent}% done"
            #                 }
            #             )
            #     else :
            #         # booking_instance.list.append(False)
            #         booking_instance.delete()
            #         # serializer.save()
               
            # return  Response(serializer.errors, status=400)
        
        # else:
        #     return Response({"message": "User is not authenticated or does not have the required role."}, status=403)
class AcceptRequest(APIView):
    def get(self,request,booking_id,*args,**kwargs):

        booking_instance = Booking.objects.get(pk=booking_id)
        heirarchy_list=booking_instance.resource.userperms
        r_name=booking_instance.resource.resource_name
        # print(heirarchy_list[curr_ind])
        
        if request.user.is_authenticated and booking_instance.all_true==False and request.user.email==heirarchy_list[booking_instance.curr_index]:
            # user_instance=User.objects.get(pk=request.user.id)
            
            try:
                booking_instance = Booking.objects.get(pk=booking_id)
                

                booking_instance.curr_index +=1

                if(booking_instance.curr_index==booking_instance.max_index):
                    date=booking_instance.date
                    email=booking_instance.user.email
                    resource=booking_instance.resource.resource_name
                    booking_instance.all_true=True
                    RequestAcceptedMail(email,resource,date)

                    bookings=Booking.objects.filter(resource=r_name,date=booking_instance.date)#doubt

                    for booking in bookings:
                        if booking.start_time>=booking_instance.start_time and booking.start_time<=booking_instance.end_time: 
                            RequestDeniededMail(booking.user.email,resource,booking.date)
                            booking.delete()

                        elif booking.end_time>=booking_instance.start_time and booking.end_time<=booking_instance.end_time:
                            RequestDeniededMail(booking.user.email,resource,booking.date)
                            booking.delete()

                        elif booking_instance.start_time>=booking.start_time and booking_instance.end_time<=booking.end_time:
                            RequestDeniededMail(booking.user.email,resource,booking.date)
                            booking.delete()


                    
                booking_instance.save()

                return Response({"message": "Accepted by current user"}, status=status.HTTP_200_OK)

            except Booking.DoesNotExist:
                return Response({"message": "Booking does not exist."}, status=404)
          
        else:
            return Response({"message": "User is not authenticated or does not have the required role."}, status=403)
        
class DenyRequest(APIView):

    def get(self,request,booking_id, *args,**kwargs):
        print("here")
        try:
            booking_instance = Booking.objects.get(pk=booking_id)
            heirarchy_list=booking_instance.resource.userperms
            
            date=booking_instance.date
            email=booking_instance.user.email
            resource=booking_instance.resource.resource_name
            print(heirarchy_list[booking_instance.curr_index])
            print(request.user.email)
            if request.user.is_authenticated:
                
                if request.user.email==heirarchy_list[booking_instance.curr_index]:
                    print("ikde")
                    # RequestDeniededMail(email,resource,date)
                    booking_instance.delete()
                    return Response({"message": "Request denied successfully"}, status=status.HTTP_200_OK)
                
                elif request.user==booking_instance.user:
                    
                    booking_instance.delete()
                    return Response({"message": "Request Deleted successfully"}, status=status.HTTP_200_OK)    
                


        except:
            return Response({"message": "User is not authenticated or does not have the required role."}, status=403)

        
# class ViewRequests(APIView):
#     def get(self,request, *args,**kwargs):
#         # print(request.user.numericRoleLevel)
#         if request.user.is_authenticated and request.user.numericRoleLevel>=2:
#             all_bookings = Booking.objects.all()
#             bookings_with_userperms = [booking for booking in all_bookings if request.user.email==booking.resource.userperms[booking.curr_index]]
#             serialized_bookings = []
        
#             for booking in bookings_with_userperms:
#                 serialized_booking = {
#                     'start_time': booking.start_time,
#                     'end_time': booking.end_time,
#                     'id': booking.booking_id,
#                 }
#                 serialized_bookings.append(serialized_booking)

#             return JsonResponse({
#                 'status': 200,
#                 'message': 'Showing details',
#                 # 'booking_allowed': e,
#                 'bookings': serialized_bookings
#             })
        
#         else:
#             return Response({
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': 'Permission denied'
#                 })




class PendingRequests(APIView):
    def get(self,request, *args,**kwargs):
        if request.user.is_authenticated :

            email=request.user.email
            bookings=Booking.objects.all()
            
            requests=[]
            for booking in bookings:
                print(booking)
                if email in booking.resource.userperms:
                    index=booking.resource.userperms.index(email)
                    if booking.curr_index==index:
                        startt_time=booking.start_time.time().strftime("%H:%M")
                        endd_time=booking.end_time.time().strftime("%H:%M")
                        booking_inst={
                            'Request by':booking.user.email,
                            'Resource':booking.resource.resource_name,
                            'booking_id' : booking.booking_id,
                            'Date':booking.date,
                            'Timing':f"{startt_time}-{endd_time}"
                            # 'Start_time':booking.start_time.time(),
                            # 'End_time':booking.end_time.time(),
                        }
                        requests.append(booking_inst)
            
            
            return Response({
                'message':'Pending Requests',
                'data':requests

            })
        else:
            return Response({
                'message':'Permission Denied',
            })


class UserRequests(APIView):
    def get(self, request, *args, **kwargs):
        print(request.user)
        if request.user.is_authenticated:
            print(request.user)
            try:
                # print("Herr")
                bookings = Booking.objects.filter(user=request.user)
                # print(booking)
                requests = []

                for booking in bookings:
                    print(booking)
                    startt_time=booking.start_time.time().strftime("%H:%M")
                    endd_time=booking.end_time.time().strftime("%H:%M")
                    booking_inst={
                        'Request by':booking.user.email,
                        'Resource':booking.resource.resource_name,
                        'booking_id' : booking.booking_id,
                        'Date':booking.date,
                        'Timing':f"{startt_time}-{endd_time}",
                        'index': booking.curr_index,
                        'length': len(booking.resource.userperms) + 1,
                        'completed': booking.all_true,
                    }
                    requests.append(booking_inst)

                return Response({
                    'message': 'User Details',
                    'data' : requests
                })
            except Booking.DoesNotExist:
                return Response({
                    'message': 'No booking found for this user'
                    # 'data' : ''
                })
        else:
            return Response({
                'message': 'User not authenticated'
                # 'data' : ''
            })

# class CancelRequests(APIView):
#     def get(self,request,booking_id, *args,**kwargs):
#         booking=Booking.objects.get(pk=booking_id)
#         if request.user.is_authenticated and request.user==booking.user:
#             # print(request.user.email)
#             # booking = Booking.objects.get(pk==booking_id)
#             booking.delete()

#             date=booking.date
#             email=booking.user.email
#             resource=booking.resource.resource_name
           
#             return Response({
#                 'message':'Request Deleted',
#                 # 'data':requests

#             })
#         else:
#             return Response({
#                 'message':'permission Denied',
#             })
        
class UserInfo(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(request.user.email)
            user_details={
                        'Username':request.user.first_name+''+request.user.last_name,
                        'email':request.user.email,
                        'organization': request.user.organization,
                        'Role':request.user.numericRoleLevel,
                        'is_admin':request.user.is_admin,
                        
                    }
            return JsonResponse({
                'status': 200,
                'message': 'Showing details',
                'userDetails': user_details
            })
        else:
            return JsonResponse({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Login Required'
            })
        
        
