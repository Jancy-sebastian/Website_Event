from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.generics import ListAPIView
from rest_framework import status,permissions,filters
from datetime import datetime , timedelta
from django.contrib.auth import authenticate ,login , logout
from django.db.models import Q



class EventListView(ListAPIView):   #fectch all the events 
  
    permission_classes=(permissions.IsAuthenticated,) #allow only authenticated users
    queryset = EventDetails.objects.all()   
    serializer_class = EventSerializer 
    template_name="event_create.html"
    filter_backends = [filters.SearchFilter]
    search_fields = ['^slug']

    def get_queryset(self):
        initial_date = EventDetails.objects.first().created_on #fetching all the details according to created_on
        current_date = datetime.now() - timedelta(days = 1)   # Calculating past dates  for one day
        return EventDetails.objects.filter(~Q(start_date__date__range=[initial_date.date(),current_date.date()]))
 
   

class EventFilter(ListAPIView):   # filtering the events according to startdate , enddate and category
    serializer_class = EventSerializer 
    template_name="event_create.html"
    def get_queryset(self):
        start_date =  datetime.strptime(self.kwargs['startdate'],"%m-%d-%Y")  #strptime creates a datetime object from the given string
        end_date =  datetime.strptime(self.kwargs['enddate'],"%m-%d-%Y")
        category = self.kwargs['category'].lower()   
        initial_date = EventDetails.objects.first().created_on 
        current_date = datetime.now() - timedelta(days = 1)
        return EventDetails.objects.filter(Q(start_date__date__range=[start_date.date(),end_date.date()],categories=category) & ~Q(start_date__date__range=[initial_date.date(),current_date.date()]))



class Login(APIView):  #login api

    permission_classes=(permissions.AllowAny,)  
    def get(self,request):
        try:      
            return Response(data={"data":"True"},status=status.HTTP_202_ACCEPTED,template_name="login_registration.html")
        except:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_400_BAD_REQUEST)


    def post(self,request):  
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user_data = User.objects.filter(username=username).exists()  #checking username already exit or not
            
            if not user_data:  #if not it will return a message that this user is not a valid user
                
                return Response(data={"data":"False","message":"Invalid Username"},status=status.HTTP_400_BAD_REQUEST)
            
            data = User.objects.filter(username=username,password=password).exists()  #checking whether username and password already exit
            
            if data ==  True:  
                user = User.objects.get(username=username,password=password)
                return Response(data={"data":"True"},status=status.HTTP_202_ACCEPTED)
            return Response(data={"data":"False","message":"Invalid password"},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):  #logout api
    def post(self,request):
        try:
            logout(request)
            return Response(data={"data":"True"},status=status.HTTP_202_ACCEPTED)
        except:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_400_BAD_REQUEST)


class Registeration(APIView):   #Api for registration
    permission_classes=(permissions.AllowAny,)  #adding permission
    def post(self, request):

        try:
            data = User.objects.filter(username=request.data.get('username')).exists()   #checking whether the username exists or not
            
            if data:       #if exists it will return message user already exists
                return Response(data={"data":"False","message":" User already exists"},status=status.HTTP_400_BAD_REQUEST)
            serializer =UserSerializer(data=request.data)   # else create a new user
            if serializer.is_valid():    # checking whether serializer is valid or not
                serializer.save(is_staff=True)
                
                print(serializer.errors)
                return Response(data={"data":"True","message":"User successfully registered please login"},status=status.HTTP_201_CREATED)
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_400_BAD_REQUEST)    
        except Exception as e:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_400_BAD_REQUEST)



class Likeapi(APIView):
    def post(self,request):
        try:
            event_id = request.data.get('event_id')
            action = request.data.get('action')
            event_obj = EventDetails.objects.get(id=event_id)   #filtering according to event id
            if action =='like':               
                event_obj.like.add(request.user)
                event_obj.dislike.remove(request.user)
            else:
                event_obj.dislike.add(request.user)
                event_obj.like.remove(request.user)
                  

            return Response(data={"data":"True"},status=status.HTTP_202_ACCEPTED)
        except:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_400_BAD_REQUEST)

