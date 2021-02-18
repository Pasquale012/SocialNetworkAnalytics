from datetime import date
from typing import Match
from django.db import models
from django.db.models.fields import DateField

class Profile(models.Model):
    username = models.CharField(max_length=200)
    followees = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    nDatePostSaved = models.CharField(max_length=200, default="")
    totalLikes = models.BigIntegerField(default=0)
    totalComments = models.BigIntegerField(default=0)
    postContacts = models.IntegerField(default=0)
    allPost = models.IntegerField(default=0)
    isPrivate = models.BooleanField(default=False)
    avgPositiveSentiment = models.FloatField(null=True)
    avgNeutralSentiment = models.FloatField(null=True)
    avgNegativeSentiment = models.FloatField(null=True)
    def __str__(self) -> str:
        return self.username

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    uriPost = models.CharField(max_length=200)
    bioPost = models.CharField(max_length=2000, default="No Bio")
    taggedUser = models.CharField(max_length=200, default="No Tagged User")
    nLikes = models.IntegerField(default=0)
    nComments = models.IntegerField(default=0)
    nCommentsCount= models.IntegerField(default=0)
    datePost = models.DateField(default=date.today)
    avgPositiveSentiment = models.FloatField(null=True)
    avgNeutralSentiment = models.FloatField(null=True)
    avgNegativeSentiment = models.FloatField(null=True)

    class Meta:
        # sort by "the date" in descending order unless
        # overridden in the query with order_by()
        ordering = ['-datePost']

    def __str__(self) -> str:
        return str(self.id) + " " +self.uriPost + " " + self.bioPost

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_social = models.BigIntegerField(default=0)
    comment_text =  models.CharField(max_length=500)
    owner= models.CharField(max_length=200, default="No owner")
    sentiment = models.CharField(max_length=20, default="Not Analyzed")
    positive = models.FloatField(null=True)
    negative = models.FloatField(null=True)
    neutral = models.FloatField(null=True)
    language = models.CharField(max_length=200, default="No Language")
    likesCount = models.IntegerField(default=0)
    
    class Meta:
        # sort by "the date" in ascending order unless
        # overridden in the query with order_by()
        ordering = ['-likesCount']

    def __str__(self) -> str:
        return self.comment_text

class All_Social_Id(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    an_id_social = models.BigIntegerField(default=0)

