from datetime import date
from django.core.paginator import Paginator
from django.db.models.functions import Coalesce
from polls.models import All_Social_Id, Comments, Post, Profile
from django.db.models import Avg
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from typing import Reversible
from django.db.models.aggregates import Sum
from django.http import response, request
import requests, json, datetime, re, logging
from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader
from instaloader.structures import TopSearchResults
from instaloader.exceptions import LoginRequiredException


import instaloader

logger = logging.getLogger(__name__)
#FUNCTION_APP = "http://localhost:7071/api/SentimentFNAPP"
FUNCTION_APP = "https://socialanalyticsfnapp.azurewebsites.net/api/Sentiment?code=tN39Nh2QJ2VnvT0o19Mk8sakUiBXTCIIMvWds3NH721s7e9TrFlnhQ=="
L = instaloader.Instaloader()

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lastest_profile_list'

    def get_queryset(self):
        return Profile.objects.order_by('-followers')


class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'polls/profile.html'

def index_Page_Error(request):
    context = {
        'lastest_profile_list' : Profile.objects.order_by('-followers'),
        'profilo_non_trovato' : True
    }
    
    return render(request, 'polls/post.html', context)

def getPostPage(request, pk):
    nuoviCommenti=False
    totaleNuoviCommenti = 0
    limit = 1
    postDB = get_object_or_404(Post, pk=pk)
    if(postDB.comments_set.count() > 0):
        try:
            post = instaloader.Post.from_shortcode(L.context, postDB.uriPost)
        except LoginRequiredException: 
                L.login("socialanalysiscld", "progettocloud123.")
                post = instaloader.Post.from_shortcode(L.context, postDB.uriPost)

        if post.likes != postDB.nLikes:
            postDB.totalLikes = post.likes
        if postDB.nCommentsCount != post.comments:
            #totaleNuoviCommenti = post.comments - postDB.nComments
            nuoviCommenti = True
        postDB.save()
        context = {
            "post": postDB,
            "nuoviCommenti": nuoviCommenti,
            #"totNuoviCommenti": totaleNuoviCommenti
        }
        return render(request, 'polls/post.html', context)
    else :
        postDB = Post.objects.get(id=pk)
        L.login("socialanalysiscld", "progettocloud123.")
        post = instaloader.Post.from_shortcode(L.context, postDB.uriPost)          
        allComments = post.get_comments()
        ids = list()
        for comment in allComments:
            if limit <= 100:
                if(remove_emoji(comment.text) != ''):       
                    if limit <= 100:    
                        All_Social_Id(post=postDB, an_id_social=comment.id).save()
                        Comments(post=postDB, id_social=comment.id, comment_text=comment.text if len(comment.text) < 200 else comment.text[:200] , owner = comment.owner.username, likesCount = comment.likes_count).save()
                        ids.append(comment.id)
                        #parameter = "&idComm="+str(comment.id)
                        #print(FUNCTION_APP+parameter)
                        #requests.post(FUNCTION_APP+parameter)
                        limit = limit + 1
            else:
                break
        
        payload = "&ids="+str(ids)

        requests.post(FUNCTION_APP+payload)

        if postDB.nComments != post.comments :
            postDB.nComments = post.comments
        postDB.nCommentsCount += limit
        if postDB.nCommentsCount != postDB.nComments:
            nuoviCommenti = True
        if post.likes != postDB.nLikes:
            postDB.totalLikes = post.likes
        totPosSentComm = Comments.objects.filter(post_id = postDB.id).exclude(sentiment = "Not Analyzed").aggregate(Sum('positive'))['positive__sum']
        totNeutralSentComm = Comments.objects.filter(post_id = postDB.id).exclude(sentiment = "Not Analyzed").aggregate(Sum('neutral'))['neutral__sum']
        totNegativeSentComm = Comments.objects.filter(post_id = postDB.id).exclude(sentiment = "Not Analyzed").aggregate(Sum('negative'))['negative__sum']
        totDivComm = Comments.objects.filter(post_id = postDB.id).exclude(sentiment = "Not Analyzed").count()
        #print(totSentComm)
        #print(totDivComm)
        postDB.avgPositiveSentiment = totPosSentComm/totDivComm if totDivComm != 0 and totPosSentComm != None else 0 
        postDB.avgNeutralSentiment = totNeutralSentComm/totDivComm if totDivComm != 0 and totNeutralSentComm != None else 0 
        postDB.avgNegativeSentiment = totNegativeSentComm/totDivComm if totDivComm != 0 and totNegativeSentComm != None else 0 
        postDB.save()
        L.close()
        context={
            "post" : postDB,
            "nuoviCommenti" : nuoviCommenti

        }
        return render(request, "polls/post.html", context)


def getProfile(request, pk):
    p = get_object_or_404(Profile, pk=pk)
    #L = instaloader.Instaloader()
    newValue=0
    newPost=False
    totNuoviPost = 0
    result=[]
    thisYear=False
    profile = instaloader.Profile.from_username(L.context, p.username)
    if p.followers != profile.followers:
        if p.followers < profile.followers:
            newValue = profile.followers - p.followers
            p.followers = profile.followers
        elif p.followers > profile.followers:
            newValue =  profile.followers - p.followers
            p.followers = profile.followers
    if p.allPost != profile.mediacount:
        totNuoviPost = profile.mediacount - p.allPost
        newPost = True
    p.save()
    if p.isPrivate is False:
        if profile.is_private:
            p.isPrivate = True
            p.save()
            result = postDates(p)
        else:
            post = Post.objects.filter(profile_id = p.id)
            avgPositive = post.aggregate(Sum('avgPositiveSentiment'))['avgPositiveSentiment__sum']
            avgNeutral = post.aggregate(Sum('avgNeutralSentiment'))['avgNeutralSentiment__sum']
            avgNegative = post.aggregate(Sum('avgNegativeSentiment'))['avgNegativeSentiment__sum']
            countSENTok = post.exclude(avgPositiveSentiment = None).count()
            p.avgPositiveSentiment = avgPositive/countSENTok if avgPositive != 0 and countSENTok != 0 else 0
            p.avgNeutralSentiment = avgNeutral/countSENTok if avgNeutral != 0 and countSENTok != 0 else 0
            p.avgNegativeSentiment = avgNegative/countSENTok if avgNegative != 0 and countSENTok != 0 else 0
            p.save()
            result=[]
            result = postDates(p)
    elif p.isPrivate is True:
        if profile.is_private:
            result = postDates(p)
        else:
            p.isPrivate=False
            result = postDates(p)
            p.save()
    
    if str(datetime.now().year) not in result:
        thisYear = True
    
    

    paginator = Paginator(post, 200)

    page_number = request.GET.get('page')
    if page_number is None:
        page_obj = paginator.get_page(1)
    else:
        page_obj = paginator.get_page(page_number)

    context={
        'profile': p,
        'dateMancanti': result,
        'newOrLostFollowers': newValue,
        'newPost': newPost,
        'UltimoAnnoOK': thisYear,
        'totNuoviPost': totNuoviPost,
        'averangeLikes': round(p.totalLikes/p.postContacts,2) if p.postContacts!=0 else 0,
        'averangeComments':round(p.totalComments/p.postContacts, 2) if p.postContacts!=0 else 0,
        #'averangeSentiment': round(avg/countSENTok, 2) if avg != None and countSENTok != 0 else 0.0,
        'post_page': page_obj
    }

    return render(request, "polls/profile.html", context)

def postDates(p):
    lastYear =datetime.now().year
    ALL = [str(lastYear), str(lastYear-1), str(lastYear-2), str(lastYear-3), str(lastYear-4), str(lastYear-5), str(lastYear-6), str(lastYear-7), str(lastYear-8)] 
    dateDB = p.nDatePostSaved.split(", ")
    lostDate=[]

    if p.isPrivate is True:
        return "NOTALL"

    for date in ALL:
        if date not in dateDB:
            lostDate.append(date)
        
    if(len(lostDate) == 0):
        return "ALL"
    

    
    return lostDate


#Post.objects.filter(profile_id=p.id).order_by('-datePost')

def insert(request): # aggiungere la data da cui scaricare i post
    usernameP = request.POST['name']
    dateREQ = request.POST.getlist('checkYear') #prendo tutte le date dalla request
    date=[]
    lastYear =datetime.now().year
    if "ALL" in  dateREQ: #controllo se nell'array c'è ALL quindi tutte le date
        date = [str(lastYear), str(lastYear-1), str(lastYear-2), str(lastYear-3), str(lastYear-4), str(lastYear-5), str(lastYear-6), str(lastYear-7), str(lastYear-8)] #inizializzo l'array con tutte le date possibili
    else:
        for dateX in dateREQ:
            date.append(dateX) 
    check = checkIfExistInDB(usernameP) #controllo che l'utente che sto cercando sia già nel Db
    if(check == False): # NON C'è
        #L = instaloader.Instaloader()
        try:
            profile = instaloader.Profile.from_username(L.context, usernameP)
        except instaloader.ProfileNotExistsException:
            context={
                'lastest_profile_list' : Profile.objects.order_by('-followers'),
                'profilo_non_trovato' : True
            }
            return render(request, "polls/index.html", context)
        q=""
        if(profile.is_private is False):
            q = Profile(username=profile.username, followees=profile.followees, followers=profile.followers, nDatePostSaved=getStringDate(date), allPost=profile.mediacount, isPrivate=False) #INSERISCO TUTTO CON LA DATA PASSATA DALLA REQUEST
            q.save()
            dataPost=[]
            for data in date:
                dataPost = savePost(usernameP, data)  
                if dataPost[2] != 0 :
                    q.totalLikes = q.totalLikes + dataPost[0]
                    q.totalComments += dataPost[1]
                    q.postContacts += dataPost[2]
                    q.save()
        else:
            q = Profile(username=profile.username, followees=profile.followees, followers=profile.followers, allPost=profile.mediacount, isPrivate=True).save() #INSERISCO TUTTO CON LA DATA PASSATA DALLA REQUEST
        L.close()
    elif(check == True):
        p = Profile.objects.get(username=usernameP)
        if p.isPrivate : #se quello che prendo dal DB è privato controllo se lo è ancora
            #L = instaloader.Instaloader()
            profile = instaloader.Profile.from_username(L.context, usernameP)
            if profile.is_private is False: #il profilo non è più privato
                p.isPrivate = False
                dates = []
                dateDB = p.nDatePostSaved.split(", ") 
                for dateToInsert in date:
                    if dateToInsert not in dateDB:
                        p.nDatePostSaved = p.nDatePostSaved + str(dateToInsert) + ", "
                        dates.append(dateToInsert)
                print(p.nDatePostSaved)
                if len(dates) > 0:
                    for data in dates:
                        dataPost = savePost(usernameP, data)
                        if dataPost[2] != 0 :
                            p.totalLikes = p.totalLikes + dataPost[0]
                            p.totalComments += dataPost[1]
                            p.postContacts += dataPost[2]
                            p.save()
        else:
            dates = []
            dateDB = p.nDatePostSaved.split(", ") 
            for dateToInsert in date:
                if dateToInsert not in dateDB:
                    p.nDatePostSaved = p.nDatePostSaved + str(dateToInsert) + ", "
                    dates.append(dateToInsert)
                if len(dates) > 0:
                    for data in dates:
                        dataPost = savePost(usernameP, data)
                        if dataPost[2] != 0 :
                            p.totalLikes = p.totalLikes + dataPost[0]
                            p.totalComments += dataPost[1]
                            p.postContacts += dataPost[2]
                            p.save()
        p.save()
    return response.HttpResponseRedirect(reverse('polls:index'))

def insertInProfile(request, profile): # aggiungere la data da cui scaricare i post
    p = Profile.objects.get(username=profile)
    #L = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(L.context, p.username)
    except LoginRequiredException: 
        L.login("socialanalysiscld", "progettocloud123.")
        profile = instaloader.Profile.from_username(L.context, p.username)
    #
    #L = instaloader.Instaloader()
    
    #profile = instaloader.Profile.from_username(L.context, p.username)
    if p.isPrivate is False:
        if profile.is_private:
            p.isPrivate = True
            p.save()
            result = postDates(p)
        else: 
            dateREQ = request.POST.getlist('checkYear') #prendo tutte le date dalla request
            date=[]
            for dateX in dateREQ:
                date.append(dateX) 

            dates = []
            dateDB = p.nDatePostSaved.split(", ") 
            for dateToInsert in date:
                if dateToInsert not in dateDB:
                    p.nDatePostSaved = p.nDatePostSaved + str(dateToInsert) + ", "
                    dates.append(dateToInsert)
            if len(dates) > 0:
                for data in dates:
                    dataPost = savePost(p.username, data)
                    if dataPost[2] != 0 :
                        p.totalLikes = p.totalLikes + dataPost[0]
                        p.totalComments += dataPost[1]
                        p.postContacts += dataPost[2]
                        p.save()
            result = postDates(p)
    elif p.isPrivate is True:
        if profile.is_private:
            result = postDates(p)
        else:
            p.isPrivate=False
            result = postDates(p)
            p.save()

    context = {
        'profile' : p,
        'dateMancanti': result,
        'averangeLikes': round(p.totalLikes/p.postContacts,2) if p.postContacts!=0 else 0,
        'averangeComments':round(p.totalComments/p.postContacts, 2) if p.postContacts!=0 else 0 
    }
    return response.HttpResponseRedirect(reverse('polls:profile', args=(p.id,)))

def updateNewPost(request, profile):
    p = Profile.objects.get(username=profile)
    try:
        profile = instaloader.Profile.from_username(L.context, p.username)
    except LoginRequiredException: 
        L.login("socialanalysiscld", "progettocloud123.")
        profile = instaloader.Profile.from_username(L.context, p.username)

    p.allPost = profile.mediacount

    postFirst = Post.objects.filter(profile_id = p.id).first()
    likes = 0
    comments = 0
    counterpost=0
    SINCE = datetime(postFirst.datePost.year, 12, 31)
    UNTIL = datetime(postFirst.datePost.year, postFirst.datePost.month, postFirst.datePost.day)
    listURI = Post.objects.values_list('uriPost', flat = True).filter(profile_id = p.id)
    for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, profile.get_posts())):
        if post.shortcode not in listURI:
            likes += post.likes
            comments += post.comments
            counterpost += 1
            uriPost = post.shortcode
            bio = post.caption
            Post(profile=Profile.objects.get(username=p.username), uriPost=uriPost,  bioPost=bio if bio is not None and len(bio) <= 1500 else "No Bio", nLikes=post.likes, nComments=post.comments, datePost=post.date).save()

    if counterpost != 0 :   
        p.totalLikes = p.totalLikes + likes
        p.totalComments += comments
        p.postContacts += counterpost
        p.save()
    return response.HttpResponseRedirect(reverse('polls:profile', args=(p.id,)))


def getStringDate(dates):
    dataF = ""
    for data in dates:
        dataF += str(data) +", "

    return dataF

def checkIfExistInDB(usernameP):
    if Profile.objects.filter(username=usernameP).exists():
        return True
    else:
        return False

def savePost(q, dates):
    #L = instaloader.Instaloader()
    #L.login("SocialAnalysis010", "progettoreti2020")
    try:
        profile = instaloader.Profile.from_username(L.context, q)
    except LoginRequiredException: 
        L.login("socialanalysiscld", "progettocloud123.")
        profile = instaloader.Profile.from_username(L.context, q)
    SINCE = datetime(int(dates), 12, 31)
    UNTIL = datetime(int(dates), 1, 1)
    likes = 0
    comments = 0
    counterpost=0
    p = Profile.objects.get(username = q)
    listURI = Post.objects.values_list('uriPost', flat = True).filter(profile_id = p.id)
    for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, profile.get_posts())):
        if post.shortcode not in listURI:
            likes += post.likes
            comments += post.comments
            counterpost += 1
            uriPost = post.shortcode
            bio = post.caption
            Post(profile=Profile.objects.get(username=q), uriPost=uriPost,  bioPost=bio if bio is not None and len(bio) <= 1500 else "No Bio", nLikes=post.likes, nComments=post.comments, datePost=post.date).save()

    dataPost=[likes, comments, counterpost]
    return dataPost

def delete(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    profile.delete()
    return response.HttpResponseRedirect(reverse('polls:index'))


def updateNuoviCommenti(request, post_id):
        limit = 1
        postDB = Post.objects.get(id=post_id)
        L.login("socialanalysiscld", "progettocloud123.")

        try:
            post = instaloader.Post.from_shortcode(L.context, postDB.uriPost)
        except LoginRequiredException: 
                L.login("socialanalysiscld", "progettocloud123.")
                post = instaloader.Post.from_shortcode(L.context, postDB.uriPost) 
        all_id_socail = All_Social_Id.objects.values_list('an_id_social', flat=True)
        

        for comment in post.get_comments():
            if remove_emoji(comment.text) != '':       
                if comment.id not in all_id_socail:
                    if limit <= 100:
                        All_Social_Id(post=postDB, an_id_social=comment.id).save()
                        Comments(post=postDB, id_social=comment.id, comment_text=comment.text if len(comment.text) <= 200 else comment.text[:200], owner = comment.owner.username, likesCount = comment.likes_count).save()
                        parameter = "&idComm="+str(comment.id)
                        print(FUNCTION_APP+parameter)
                        requests.post(FUNCTION_APP+parameter)
                        limit += 1
                else:
                    comm = Comments.objects.get(id_social=comment.id)
                    if comm.likesCount != comment.likes_count:
                        comm.likesCount = comment.likes_count 
                    if comm.comment_text != comment.text:
                        comm.comment_text = comment.text
                        
                        parameter = "&idComm="+str(comment.id)
                        print(FUNCTION_APP+parameter)
                        requests.post(FUNCTION_APP+parameter)
                    comm.save()
            if limit > 100:
                break
        
        if postDB.nComments != post.comments:
            postDB.nComments = post.comments
        if limit > 1:
            postDB.nCommentsCount += limit
            totPosSentComm = Comments.objects.filter(post_id = postDB.id).exclude(sentiment = "Not Analyzed").aggregate(Sum('positive'))['positive__sum']
            totNeutralSentComm = Comments.objects.filter(post_id = postDB.id).exclude(sentiment = "Not Analyzed").aggregate(Sum('neutral'))['neutral__sum']
            totNegativeSentComm = Comments.objects.filter(post_id = postDB.id).exclude(sentiment = "Not Analyzed").aggregate(Sum('negative'))['negative__sum']
            totDivComm = Comments.objects.filter(post_id = postDB.id).exclude(sentiment = "Not Analyzed").count()
            postDB.avgPositiveSentiment = totPosSentComm/totDivComm if totDivComm != 0 and totPosSentComm != None else 0 
            postDB.avgNeutralSentiment = totNeutralSentComm/totDivComm if totDivComm != 0 and totNeutralSentComm != None else 0 
            postDB.avgNegativeSentiment = totNegativeSentComm/totDivComm if totDivComm != 0 and totNegativeSentComm != None else 0 
        if post.likes != postDB.nLikes:
            postDB.totalLikes = post.likes
        postDB.save()
        L.close()
        return response.HttpResponseRedirect(reverse('polls:post', args=(postDB.id,)))


def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)