from django.urls import path
from django.contrib.auth.views import LoginView
from .views import LoginView,homeview,registerview
from .views import *
from .views import Custom404View
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('',LoginView.as_view(),name='login'),
	path('register/',registerview.as_view(),name='register'),
	path('home/',homeview.as_view(),name='home'),
	path('profile/',profileview.as_view(),name='profile'),
	path('editprofile/',editprofileview.as_view(),name="editprofile"),
	path('addpost/',addpostform_view.as_view(),name="addpost"),
	path('deletepost/<int:id>/',deletepost.as_view(),name="deletepost"),
	path('logout/',logoutview.as_view(),name='logout'),
	path('404/', Custom404View.as_view(), name='custom_404'),
]
handler404 = Custom404View.as_view()

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)