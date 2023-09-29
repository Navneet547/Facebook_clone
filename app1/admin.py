from django.contrib import admin
from .models import *

# Register your models here.
# @admin.register(UserProfile)
# class userprofileadmin(admin.ModelAdmin):
# 	list_display=('first_name','last_name','username','email','password')

admin.site.register(Profile)
admin.site.register(mypost)
admin.site.register(LikePost)
admin.site.register(FollowersCount)