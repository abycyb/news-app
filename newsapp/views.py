from .models import *
from django.db.models import Count
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render,redirect

from django.db.models.functions import Coalesce
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View, ListView, CreateView,TemplateView
from rest_framework.views import APIView
from django.conf import settings
import requests

from newsapi import NewsApiClient
from newscatcherapi import NewsCatcherApiClient

# xJXaCON3LJSMd1pyfnZp4xaa783KJJEZoRfnjf75AK8
# newscatcherapi = NewsCatcherApiClient(x_api_key=settings.NEWS_API_SECRET_KEY)
# newsapi = NewsApiClient(api_key='b1067e8c0436442ca73495ac65360bbe')

class NewsAPI(APIView):
    def get(self,request):
        # search = request.GET.get('search',"")
        # querystring = {"q":search,"lang":"en","sort_by":"relevancy","page":"1"}
        # headers = {
        #     "x-api-key": settings.NEWS_API_SECRET_KEY
        #     }
        # all_articles = newscatcherapi.get_search(
        #     q='AI',
        #     lang='en',
        #     countries='CA',
        #     page_size=100
        # )
        response = requests.request("GET", settings.NEWS_API_URL)
        response = response.json()
        return JsonResponse({'status':response['results'][:3]})


# class Indexview(View):
#     def get(self,request):
#         news = News.objects.all()
#         return render(request,'index.html',{'news':news})

import csv
# ZF2YLDZX4M0CO0SD

class Chart(View):
    def get(self,request):
        CSV_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=15min&slice=year1month1&apikey=ZF2YLDZX4M0CO0SD'

        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            data = list(cr) 
            values = [row[1:] for row in data[3::4]]  # Extract values from alternating lists, skipping the header

                           
        return render(request,'chart.html', {'data': values})
    
class Indexview(View):
    def get(self,request):
        CSV_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=15min&slice=year1month1&apikey=ZF2YLDZX4M0CO0SD'

        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            data = list(cr) 
            values = [row[1:] for row in data[4::5]]  # Extract values from alternating lists, skipping the header


        response = requests.request("GET", settings.NEWS_API_URL+"?limit=10&offset=90")
        response = response.json()       
        user = UserProfile.objects.get(pk=2)
        for i in response['results']:
            if i['id'] not in Interacted_News.objects.values_list('news_id', flat=True):
                news = Interacted_News(
                    user = user, 
                    news_id=i['id']
                    )
                news.save()
        return render(request,'index.html',{'news':response['results'],'data': values})


class Newsview(View):
    def get(self,request,pk):
        url = f"{settings.NEWS_API_URL}{pk}"

        response = requests.request("GET", url)
        response = response.json()

        filtered_news = Interacted_News.objects.filter(news_id=pk)
        print(filtered_news)
        user = UserProfile.objects.get(user=request.user)

        news_all = Interacted_News.objects.all()
        news = news_all.annotate(newsvote_count=Coalesce(Count('interacted_users'), 0)).order_by('-newsvote_count')
        
        popular_url = f"{settings.NEWS_API_URL}{pk}"
        count=0
        li = []
        for i in news:
            count +=1
            related_news_id = i.news_id
            popular_url = f"{settings.NEWS_API_URL}{related_news_id}"

            response1 = requests.request("GET", popular_url)
            response2 = response1.json()
            li.append(response2)
            if count==5:
                break

        comments = New_Comment.objects.filter(news_comment__news_id=pk)
        comment = comments.annotate(vote_count=Coalesce(Count('voted_comment'), 0)).order_by('-vote_count')
        
        subcomment = New_Subcomment.objects.filter(comment__news_comment__news_id=pk)
        
        return render(request,'single_page.html',{'response':response,'popular':li,'user':user,'news':news,'filter':filtered_news,'comment':comment,'subcomment':subcomment})


# class Newsview(View):
#     def get(self,request,pk):
#         filtered_news = News.objects.filter(pk=pk)
#         user = UserProfile.objects.get(user=request.user)
#         news_all = News.objects.all()
#         news = news_all.annotate(newsvote_count=Coalesce(Count('voted_users'), 0)).order_by('-newsvote_count')
#         comments = Comment.objects.filter(news_comment__pk=pk)
#         comment = comments.annotate(vote_count=Coalesce(Count('voted_comment'), 0)).order_by('-vote_count')
#         subcomment = Subcomment.objects.filter(comment__news_comment__pk=pk)
#         return render(request,'single_page.html',{'user':user,'news':news,'filter':filtered_news,'comment':comment,'subcomment':subcomment})


class CommentaddView(View):
    def post(self,request):
        data = request.POST.get('input_comment')
        id = request.POST.get('news_id')
        file = request.FILES.get('file')
        user_profile= UserProfile.objects.get(user=request.user.id)
        news = Interacted_News.objects.get(id=id)
        new_comment = New_Comment(
            user = user_profile,
            news_comment = news,
            content = data,
            image = file
        )
        new_comment.save()
        return JsonResponse({'status':True},safe=True)


class SubcommentaddView(View):
    def post(self,request):
        data = request.POST.get('input_comment')
        id = request.POST.get('comm_id')
        file = request.FILES.get('file')
        user_profile= UserProfile.objects.get(user=request.user.id)
        new_comment = New_Comment.objects.get(pk=id)
        new_sub_comment = New_Subcomment(
            user = user_profile,
            comment = new_comment,
            content = data,
            image = file,
        )
        new_sub_comment.save()

        return JsonResponse({'status':True})
    

class UpdateVote(View):
    def post(self,request):
        vote = request.POST.get('vote')
        pk = request.POST.get('news_id')
        print(vote,pk,'****************************')

        news_obj = Interacted_News.objects.get(news_id=pk)
        x = news_obj.interacted_users.values_list('id', flat=True)
        if x:
            for i in x:
                if i != request.user.id or vote=='down':
                    if vote == 'up':
                        news_obj.interacted_users.add(request.user)
                    elif vote == 'down':
                        news_obj.interacted_users.remove(request.user)
                    news_obj.save()
                    return JsonResponse({'updated_votes':news_obj.interacted_users.count()})
        else:        
            if vote == 'up':
                news_obj.interacted_users.add(request.user)
            elif vote == 'down':
                news_obj.interacted_users.remove(request.user)
            news_obj.save()
            return JsonResponse({'updated_votes':news_obj.interacted_users.count()})                  


class CommentVote(View):
    def post(self,request):
        vote = request.POST.get('vote')
        comm_id = request.POST.get('comm_id')
        comment_obj = New_Comment.objects.get(pk=comm_id)
        if vote == 'up':
            comment_obj.voted_comment.add(request.user)
        elif vote == 'down':
            comment_obj.voted_comment.remove(request.user)
        comment_obj.save()
        return JsonResponse({'comment_votes':comment_obj.voted_comment.count()},safe=False)



    

class SignUpView(View):
    def post(self,request):
        username = request.POST.get('register-username')
        email = request.POST.get('register-email')
        image = request.POST.get('register-image')
        password1 = request.POST.get('register-password1')
        password2 = request.POST.get('register-password2')
        if password1 == password2:
            userr = User.objects.create(
                username=username,
                email=email,
            )
            userr.set_password(password1)
            userr.save()              
            user_profile = UserProfile(user=userr,image=image)
            user_profile.save()
            return redirect("index")
        else:
            return redirect('index')


class SignInView(View):

    def post(self, request, *args, **kwargs):
        username = request.POST.get("signin-username")
        password = request.POST.get("signin-password")
        userr = authenticate(
            username= username,
            password = password
        )
        if userr is not None:
            login(request, userr)
            return redirect("index")
        else:
            return redirect("index")


class SignOutView(View):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')

