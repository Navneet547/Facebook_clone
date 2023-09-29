
from django.shortcuts import render, HttpResponse,redirect,get_object_or_404
from django.views import View
from app1.models import Profile,mypost
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ObjectDoesNotExist

class registerview(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if cpassword == password:
            # Create a new user instance
            user = User(first_name=first_name, last_name=last_name, username=username, email=email)
            
            # Set and hash the password using set_password
            user.set_password(password)
            
            # Save the user object
            user.save()

            return redirect('login')
        else:
            return render(request, 'register.html', {'alert': "Password does not match"})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, 'login.html', {"alert1": "**Wrong email or password**"})


class logoutview(View):
	def get(self,request):
	    request.session.clear()
	    return redirect('login')

#...................after login pages is here...................................#
#...............................................................................#

from django.views.generic import TemplateView

class Custom404View(TemplateView):
    template_name = '404.html'

class homeview(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        user_profile = get_object_or_404(User, username=request.user.username)
        try:
            profile_details = Profile.objects.get(user=user_profile)
        except Profile.DoesNotExist:
            profile_details = None
        allpost = mypost.objects.all()
        context = {
            'user_profile': user_profile,
            'profile_details': profile_details,
            'allpost': allpost,
        }
        
        return render(request, "home.html", context)


class profileview(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        user_profile = None
        profile_details = None
        user_post = None 
        try:
            user_profile = User.objects.get(username=request.user.username)
            user_post = mypost.objects.filter(user=user_profile)
            post_id=mypost.objects.all()
            profile_details = Profile.objects.get(user=user_profile)
        except User.DoesNotExist:
            user_profile = None
            profile_details = None
            user_post = None
        except ObjectDoesNotExist:
            profile_details = None

        context = {
            'user_profile': user_profile,
            'user_post': user_post,
            'profile_details': profile_details,
            'post_id':post_id,
        }
        return render(request, 'profile.html', context)

class editprofileview(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile(user=user)
            profile.save()
        return render(request, 'editprofile.html', {'user_profile': profile})

    def post(self, request):
        user = request.user
        bio = request.POST['bio']
        profile_picture = request.FILES['profile_picture']
        location = request.POST['location']

        # Check if a profile already exists for the user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile(user=user)

        # Update the profile with the new data
        profile.bio = bio
        profile.profile_picture = profile_picture
        profile.location = location
        profile.save()

        return redirect("profile")

class addpostform_view(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        return render(request, 'addpostform.html')

    def post(self, request):
        user = request.user
        photo = request.FILES.get('photo') 
        description = request.POST.get('description')  

        # Check if required fields are provided
        if photo and description:
            # Create and save the new post
            new_post = mypost(user=user, photo=photo, description=description)
            new_post.save()
            return redirect("profile") 
        else:
            # Handle the case where required fields are missing
            return render(request, 'addpostform.html', {'error_message': 'Please provide both photo and description'})
    
class deletepost(View):
    @method_decorator(login_required(login_url='login'))
    def get(self,request,id):
        post=mypost.objects.get(id=id)
        post.delete()
        return redirect('profile')


		