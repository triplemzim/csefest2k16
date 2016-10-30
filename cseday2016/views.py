from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpRequest
from django.core.context_processors import csrf
from django.template.context_processors import request
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.db.models import Q

from datetime import datetime
from random import randint
from urllib.request import urlopen
from contextlib import closing

import cgi
import json
import math
import sys
import requests

from .forms import VerificationForm, PasswordChangeForm
from cseday2016.models import User, UserProfile, Post,Profileposts,Block,Location
from cseday2016.forms import RegistrationForm,UpdateProfileForm



#view functions
def index(request):
    """
    loads the initial web page showing the client the basic view of the website
    if the user is logged in then redirects the user to Newsfeed
    :param request: the HTMLRequest
    :return: either the index.html template if the user is not logged in
            or newsfeed if the user is logged in
    """
    context = RequestContext(request)
    error = {'has_error':False}
    return render_to_response('index.html', {'error':error}, context)

'''
def aboutus(request):
    """
    The about us page of the site. Contains the information about the site creators.
    login is not required
    :param request:the HTMLRequest
    :return:renders the 'aboutus.html' page
    """
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    return render_to_response('aboutus.html', {}, context)


@login_required(login_url='/testshare/')
def updateinfo(request):
    """
    A page containing the update info form
    :param request:the HTMLRequest
    :return: if the user is not logged in,it redirects to the index page
             else if the user is not verified,it redirects to 'verification.html'
             else if the request method is GET,it shows an update form
             else it writes updated info in database and redirects to 'profile.html'
    """
    context = RequestContext(request)
    user_profile = request.user.userprofile
    if user_profile.verification_status == 'p':
        return HttpResponseRedirect(reverse('verification'))
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    else:
        if request.method=='POST':
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.about_me=request.POST.get('aboutme')
            userprofile.user.email=request.POST.get('email')

            if request.FILES.get('profile_photo'):
                uploaded_file = request.FILES.get('profile_photo')
                #print(uploaded_file.name)
                parts=uploaded_file.name.split(".")
                #print(parts)
                joinstring=""+request.user.username+'_'+'.'+parts[len(parts)-1]
                uploaded_file.name = joinstring
                userprofile.picture= uploaded_file

            userprofile.save()
            return HttpResponseRedirect(reverse('profile',kwargs={'user_id':request.user.id}))
        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.
        return render_to_response('updateinfo.html', {}, context)


@login_required(login_url='/testshare/')
def profile(request,user_id):
    """
    A page showing the profile of the requested user id
    :param request: the HTMLRequest
    :param user_id: the requested user id
    :return: if the user is not logged in,it redirects to the index page
             else if the user is not verified,it redirects to 'verification.html'
             else if the requesting user is blocked by the requested user or has blocked requested user,an error page is shown
             else shows user profile with his/her info and posts on
    """
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.

    context = RequestContext(request)
    user_profile = request.user.userprofile
    if user_profile.verification_status == 'p':
        return HttpResponseRedirect(reverse('verification'))
    #username = UserProfile.objects.get(user=request.user)
    else:
        username = UserProfile.objects.get(user=User.objects.get(id=user_id))
        requested_user_prof=UserProfile.objects.get(user=request.user)
        block_possible_1=Block.objects.filter(blocker=username,blocked=requested_user_prof)
        block_possible_2=Block.objects.filter(blocked=username,blocker=requested_user_prof)
        if len(block_possible_1)+len(block_possible_2)>0:
            return  HttpResponseRedirect(reverse('nopermission'))
        posts = Post.objects.filter(post_maker=username)
        today = datetime.now()
        toplabel = today.strftime('%B')

        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.

        post_count=Post.objects.filter(post_maker=username).count()

        profilepostlist=[]
        for post in posts:
            profpost=Profileposts()
            profpost.post_info=post
            choice = int(randint(0,1))
            if choice ==1:
                leftPost = '<div class="col-sm-6 padding-right arrow-right wow fadeInLeft" data-wow-duration="1000ms" data-wow-delay="300ms">'
                leftPost = cgi.escape(leftPost,quote=True)
                profpost.alignment = leftPost
            else:
                rightPost = '<div class=\"col-sm-6\"> <br> </div> <div class=\"col-sm-6 padding-left arrow-left wow fadeInRight\" data-wow-duration=\"1000ms\" data-wow-delay=\"300ms\"\>'
                rightPost = cgi.escape(rightPost,quote=True)
                profpost.alignment = rightPost
            profilepostlist.append(profpost)
            #print(profpost.alignment)
        #print(profilepostlist)
        #print(username.about_me)
        #randlist=[int(randint(0,1)) for i in xrange(post_count)]

        #zipped=zip(posts,randlist)
        #print(zipped)
        blocks=[]
        #print(request.user.id ,int(user_id))
        if request.user.id == int(user_id):
            #print("yes")
            blocks=Block.objects.filter(blocker=username)
        #print(blocks)
        return render_to_response('profile.html', {'posts':profilepostlist,'label':toplabel,'userprofile':username,'blocks':blocks}, context)

@login_required(login_url='/testshare/')
def profile_by_name(request,user_name):
    """
    A page showing the profile of the requested user

    :param request:the HTMLRequest
    :param user_name:the requested user id

    :return:if the user is not logged in,it redirects to the index page
            else if the user is not verified,it redirects to 'verification.html'
            else if the requesting user is blocked by the requested user or has blocked requested user,an error page is shown
            else shows user profile with his/her info and posts on

    """
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    user_profile = request.user.userprofile
    if user_profile.verification_status == 'p':
        return HttpResponseRedirect(reverse('verification'))    #username = UserProfile.objects.get(user=request.user)
    else:
        username = UserProfile.objects.get(user=User.objects.get(username=user_name))
        requested_user_prof=UserProfile.objects.get(user=request.user)
        block_possible_1=Block.objects.filter(blocker=username,blocked=requested_user_prof)
        block_possible_2=Block.objects.filter(blocked=username,blocker=requested_user_prof)
        if len(block_possible_1)+len(block_possible_2)>0:
            return  HttpResponseRedirect(reverse('nopermission'))

        posts = Post.objects.filter(post_maker=username)
        today = datetime.now()
        toplabel = today.strftime('%B')

        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.

        post_count=Post.objects.filter(post_maker=username).count()

        profilepostlist=[]
        for post in posts:
            profpost=Profileposts()
            profpost.post_info=post
            choice = int(randint(0,1))
            if choice ==1:
                leftPost = '<div class="col-sm-6 padding-right arrow-right wow fadeInLeft" data-wow-duration="1000ms" data-wow-delay="300ms">'
                leftPost = cgi.escape(leftPost,quote=True)
                profpost.alignment = leftPost
            else:
                rightPost = '<div class=\"col-sm-6\"> <br> </div> <div class=\"col-sm-6 padding-left arrow-left wow fadeInRight\" data-wow-duration=\"1000ms\" data-wow-delay=\"300ms\"\>'
                rightPost = cgi.escape(rightPost,quote=True)
                profpost.alignment = rightPost
            profilepostlist.append(profpost)
         #   print(profpost.alignment)
        #print(profilepostlist)
        #print(username.about_me)
        #randlist=[int(randint(0,1)) for i in xrange(post_count)]

        #zipped=zip(posts,randlist)
        #print(zipped)
        blocks=[]
        #print(request.user.username ,str(user_name))
        if request.user.username == str(user_name):
         #   print("yes")
            blocks=Block.objects.filter(blocker=username)
        #print(blocks)

        return render_to_response('profile.html', {'posts':profilepostlist,'label':toplabel,'userprofile':username,'blocks':blocks}, context)

def about(request):
    """
    The about us page of the site. Contains the information about the site creators.
    login is not required
    :param request:the HTMLRequest
    :return:renders the 'about.html' page
    """

    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!


    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('about.html', {}, context)


def register(request):
    """
    The registration page renderer
    :param request:The HTMLRequest
    :return: if the request method is POST,registers the ser
            else it just shows the registration form
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_temp = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            userprofile=UserProfile(user=user_temp)
            userprofile.save()
        #    print(userprofile.user.username)
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            #print(request.POST.get('next'))
            return redirect('/testshare/newsfeed/')
        else:
            error = {'has_error':True, 'message':'invalid input'}
            return HttpResponseRedirect('/testshare/',{'error':error})

    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'index.html',
        variables,
    )


def user_login(request):
    """
    User login renderer
    :param request: The HTMLRequest
    :return: if the user is authenticated,redirects him to newsfeed
            else redirects him to this page again
    """
    context = RequestContext(request)
    logout(request)

    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if (request.POST.get('next') == ''):
                    return redirect('/testshare/newsfeed/')
                return redirect(request.POST.get('next'))
        error = {'has_error':True,'message':'Username Password do not match'}
        return render_to_response('index.html', {'error': error}, context_instance=RequestContext(request))


@login_required(login_url='/testshare/')
def newsfeed(request):
    """
    The newsfeed renderer
    :param request: The HTMLRequest
    :return:  if the user is not logged in,it redirects to the index page
             else if the user is not verified,it redirects to 'verification.html'
             else if the request method is GET,it loads the newsfeed
             else it posts status and uploads photo(optionally)

    """
    context = RequestContext(request)
    #req_loc=get_random_location()
    #print('The request location data is')
    #print('Location name ',req_loc.location_name,' longitude ',req_loc.location_long,' latitude ',req_loc.location_lat,' ')
    #minlat=(req_loc.location_lat)-10.00
    #maxlat=(req_loc.location_lat)+10.00
    #minlong=(req_loc.location_long)-10.00
    #maxlong=(req_loc.location_long)+10.00


    user_profile = request.user.userprofile
    if user_profile.verification_status == 'p':
        return HttpResponseRedirect(reverse('verification'))
    else:
        #remote host part
        req_loc_dict=get_location(get_ip_address(request))
        if str(req_loc_dict['region_name'])== '':
            req_loc_dict['region_name']=req_loc_dict['country_name']

        req_loc= Location(location_name=str(req_loc_dict['region_name']),location_lat=req_loc_dict['latitude'],location_long=req_loc_dict['longitude'])
        proximity_range=get_proximity_range(req_loc_dict,10,10)
        minlat=proximity_range['min_lat']
        maxlat=proximity_range['max_lat']
        minlong=proximity_range['min_long']
        maxlong=proximity_range['max_long']
        place=req_loc.location_name
        place_lat=req_loc.location_lat
        place_long=req_loc.location_long
        print('minlat ',minlat,'maxlat',maxlat,'minlong',minlong,'maxlong ',maxlong)
        posts=Post.objects.all()
        allblocklist=[]
        allblocklist=find_blocks(request)
        #loc_range=is_near(req_loc.location_lat,req_loc.location_long)
        #print(loc_range)
        #posts=Post.objects.filter(post_location__location_lat__lte=loc_range[0],post_location__location_lat__gte=loc_range[1],post_location__location_long__lte=loc_range[2],post_location__location_long__gte=loc_range[3]).exclude(Q(post_maker__in=allblocklist))
        #|Q(post_location__location_lat__lt= req_loc.location_lat,post_location__location_long__lt= req_loc.location_long))
        #posts=Post.objects.exclude(Q(post_maker__in=allblocklist))
    #    posts=Post.objects.filter(post_location__location_lat__lte=req_loc.location_lat, post_location__location_long__lte=req_loc.location_long).exclude(Q(post_maker__in=allblocklist))
        posts=Post.objects.filter(post_location__location_lat__lte=maxlat,post_location__location_lat__gte=minlat, post_location__location_long__lte=maxlong,post_location__location_long__gte=minlong).exclude(Q(post_maker__in=allblocklist))

        if request.POST:
         #   print(request.POST.get('status'))
            #get random location
            req_loc.save()

            post_location=req_loc
            #print(post_location.location_name)
            post_maker=UserProfile.objects.get(user=request.user)
            post_text=request.POST.get('status')
            post_time=datetime.now()
            post=Post(post_maker=post_maker,post_text=post_text,post_time=post_time,post_sharecount=0,post_location=post_location)
            if request.FILES.get('post_photo'):
                uploaded_file = request.FILES.get('post_photo')
          #      print(uploaded_file.name)
                parts=uploaded_file.name.split(".")
                #print(parts)
                joinstring=""+post_maker.user.username+'_'+str(post_time)+'.'+parts[len(parts)-1]
                uploaded_file.name = joinstring
                post.post_photo = uploaded_file

            post.save()

        return render_to_response('newsfeed.html', {'posts':posts,'place':place,'place_lat':place_lat,'place_long':place_long}, context)


# Use the login_required() decorator to ensure only those logged in can access the view.

@login_required(login_url='/testshare/')
def user_logout(request):
    """
    Destroys the session
    :param request: The HTMLRequest
    :return: logs out the user
    """
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/testshare/')

@login_required(login_url='/testshare/')
def spread(request,post_id):
    """
    Spreads the post of a user within the range
    :param request:The HTMLRequest
    :param post_id: the post id
    :return:  if the user is not logged in,it redirects to the index page
             else if the user is not verified,it redirects to 'verification.html'
             else if the requesting user is blocked by the requested user or has blocked requested user,an error page is shown
            else spreads the post and redirects to newsfeed page

    """
    context = RequestContext(request)
    user_profile = request.user.userprofile
    if user_profile.verification_status == 'p':
        return HttpResponseRedirect(reverse('verification'))
    else:
        spreadedpost=Post.objects.get(pk=post_id)
        spreadedpost.post_sharecount+=1
        spreadedpost.save()

        req_loc_dict=get_location(get_ip_address(request))
        if str(req_loc_dict['region_name'])== '':
            req_loc_dict['region_name']=req_loc_dict['country_name']

        req_loc= Location(location_name=str(req_loc_dict['region_name']),location_lat=req_loc_dict['latitude'],location_long=req_loc_dict['longitude'])
        req_loc.save()
        newpost=Post()
        newpost.post_location=req_loc
        print(newpost.post_location.location_name)
        newpost.post_maker=UserProfile.objects.get(user=request.user)
        newpost.post_text=spreadedpost.post_text
        newpost.post_photo=spreadedpost.post_photo
        newpost.post_sharecount=0
        newpost.post_sharedfrom=spreadedpost
        newpost.post_time=datetime.now()

        newpost.save()
        return HttpResponseRedirect(reverse('newsfeed'))

@login_required(login_url='/testshare/')
def post(request,post_id):

    """
    Shows the post of a user within the range
    :param request:The HTMLRequest
    :param post_id: the post id
    :return:  if the user is not logged in,it redirects to the index page
             else if the user is not verified,it redirects to 'verification.html'
             else if the requesting user is blocked by the requested user or has blocked requested user,an error page is shown
            else shows the post
    """
    context = RequestContext(request)
    user_profile = request.user.userprofile
    if user_profile.verification_status == 'p':
        return HttpResponseRedirect(reverse('verification'))
    else:
        post=Post.objects.get(id=post_id)

        username=post.post_maker
        requested_user_prof=UserProfile.objects.get(user=request.user)
        block_possible_1=Block.objects.filter(blocker=username,blocked=requested_user_prof)
        block_possible_2=Block.objects.filter(blocked=username,blocker=requested_user_prof)
        if len(block_possible_1)+len(block_possible_2)>0:
            return  HttpResponseRedirect(reverse('nopermission'))

        return render_to_response('post.html', {'post':post}, context)


@login_required(login_url='/testshare/')
def block(request,user_id):
    """
    Blocks the requested user id
    :param request: The HTMLRequest
    :param user_id: the desired blocked user id
    :return: blocks the user id
    """
    context = RequestContext(request)
    user_profile = request.user.userprofile
    if user_profile.verification_status == 'p':
        return HttpResponseRedirect(reverse('verification'))
    else:
        who_blocked=UserProfile.objects.get(user=request.user)
        who_got_blocked=UserProfile.objects.get(user=User.objects.get(id=user_id))
        block_when=datetime.now()
        block= Block(blocker=who_blocked,blocked=who_got_blocked,block_time=block_when)
        block.save()
        return HttpResponseRedirect(reverse('profile',kwargs={'user_id':request.user.id}))

@login_required(login_url='/testshare/')
def unblock(request,user_id):
    """
    Unblocks the requested user id
    :param request: The HTMLRequest
    :param user_id: the desired blocked user id
    :return: Unblocks the user id

    """
    context = RequestContext(request)
    user_profile = request.user.userprofile
    if user_profile.verification_status == 'p':
        return HttpResponseRedirect(reverse('verification'))
    else:
        who_blocked=UserProfile.objects.get(user=request.user)
        who_got_blocked=UserProfile.objects.get(user=User.objects.get(id=user_id))

        blockrecord= Block.objects.filter(blocker=who_blocked,blocked=who_got_blocked)
        blockrecord.delete()
        return HttpResponseRedirect(reverse('profile',kwargs={'user_id':request.user.id}))

@login_required(login_url='/testshare/')
def find_blocks(request):
    """
    returns the blocklist of user along with the list of people who blocked the user
    :param request: The HTMLRequest
    :return: A list containing the users the requested user blocked or vice versa
    """
    context = RequestContext(request)
    user_profile = request.user.userprofile
    if user_profile.verification_status == 'p':
        return HttpResponseRedirect(reverse('verification'))
    else:
        request_user_profile=UserProfile.objects.get(user=request.user)
        #print(request_user_profile.user.username)

        not_block_list=[]
        not_block_list_1=[]
        not_block_list_2=[]

        temp_block_list_1=Block.objects.filter(Q(blocker=request_user_profile)).values_list('blocked',flat=True)
        temp_block_list_2=Block.objects.filter(Q(blocked=request_user_profile)).values_list('blocker',flat=True)
        not_block_list_1.extend(temp_block_list_1)
        not_block_list_2.extend(temp_block_list_2)

        not_block_list=not_block_list_1+not_block_list_2
        return not_block_list

def nopermission(request):
    """
    Shows the no permission paged in case of block
    :param request: The HTMLRequest
    :return:  if the user is not logged in,it redirects to the index page
             else if the user is not verified,it redirects to 'verification.html'
             else show the no permission page with message
    """
       # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    user_profile = request.user.userprofile
    if user_profile.verification_status == 'p':
        return HttpResponseRedirect(reverse('verification'))
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    else:

        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.
        return render_to_response('nopermission.html', {}, context)



@login_required(login_url='/testshare/')
def verification(request):
    requesting_user_profile = request.user.userprofile
    if request.method == 'POST':
        verification_form = VerificationForm(request.POST)
        if verification_form.is_valid():
            verification_code_input = verification_form.cleaned_data['verification_code']
            if verification_code_input == requesting_user_profile.verification_code:
                requesting_user_profile.verification_status = 'A'
                requesting_user_profile.save()
                return HttpResponseRedirect(reverse('newsfeed'))
            else:
                error = {'has_error': True,
                         'message': 'The code you entered does not match with the code in your email',
                         'type': 'code does not match'}
                return render(request, 'verification.html', {'form': verification_form,
                                                             'user_profile': requesting_user_profile,
                                                             'error': error})
        else:
            error = {'has_error': True,
                     'message': 'The code you entered is invalid',
                     'type': 'code does not match'}
            return render(request, 'verification.html', {'form': verification_form,
                                                         'user_profile': requesting_user_profile,
                                                         'error': error})
    else:
        verification_form = VerificationForm()
        print(verification_form)
        print("hello")
        error = {'has_error': False}
        return render(request, 'verification.html', {'form': verification_form,
                                                     'user_profile': requesting_user_profile,
                                                     'error': error})

'''