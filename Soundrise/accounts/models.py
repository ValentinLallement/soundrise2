import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count 
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=500, default="https://t4.ftcdn.net/jpg/05/17/53/57/360_F_517535712_q7f9QC9X6TQxWi6xYZZbMmw5cnLMr279.jpg")
    profile_free_text = models.CharField(max_length=500, default="Welcome to my profile")
    tel = models.CharField(max_length=20, null=False, blank=False, default='none')
    mail_pro = models.EmailField(max_length=30, blank=True)
    darkTheme = models.BooleanField(default=True)
    rank = models.CharField(default='basic', max_length=30)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    like_number = models.IntegerField(default=0)


    def subscription_count(self):
        return self.followers.count()

    def subscriber_count(self):
        return self.following.count()

    def get_follower_count(self):
        return self.followers.count()
    
    def get_following_count(self):
        return self.following.count()

    def is_followed_by_user(self, user):
        return self.followers.filter(id=user.id).exists()

    def liked_beats_count(self):
        return self.liked_beats.count()



from django.contrib.auth import get_user_model

class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_messages')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    title=models.CharField(max_length=30,blank=True)
    participants = models.ManyToManyField(get_user_model(), related_name='conversations')
    messages = models.ManyToManyField(Message, blank=True)
    
   
    def get_other_participant(self, user):
        """
        Returns the other participant in the conversation besides the given user.

        Args:
            user: The current user object.

        Returns:
            The other participant object (e.g., User instance).
        """

        participants = self.participants.all()
        if participants.count() == 2:
            other_participant = participants.exclude(pk=user.pk).first()
            return other_participant
        else:
            # Handle cases with more or less than 2 participants (optional)
            raise ValueError("Conversation must have exactly two participants")
    
    def clean(self):
        """
        Validates that the conversation has exactly two participants.
        """

        if self.participants.count() ==1:
            raise ValidationError('Conversation must have exactly two participants')
        return super().clean()
    
    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

        if self.participants.count() == 1:
            raise ValidationError("A conversation must have exactly two participants.")

