from django.shortcuts import render,redirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from picturepuzzle.models import user_level,puzzle
import datetime

# Create your views here.

@login_required(login_url='/picpuzzle/login')
def index(request):

	username = request.user.username
	cur_level = user_level.objects.get(user=request.user)

	if cur_level.level > puzzle.objects.all().count() :
		return render_to_response('picturepuzzle/congratz.html',{'user':request.user})
		


	cur_puzzle = puzzle.objects.get(id=cur_level.level)



	if request.method=='POST':
		answer = request.POST.get('answer','')
		if answer == cur_puzzle.solution:
			cur_level.level = cur_level.level+1
			cur_level.save()
			return redirect('/picpuzzle')

	
	error = {'has_error':False}
	
	


	return render_to_response('picturepuzzle/pichome.html',{'puzzle':cur_puzzle},RequestContext(request))


@login_required(login_url='/picpuzzle/login')
def Leaderboard(request):
	userlist = user_level.objects.order_by('-level','Time')
	
	return render_to_response('picturepuzzle/leaderboard.html',{'userlist':userlist})



def Login(request):
	error = {'has_error':False}

	if request.method == 'POST':
		# print('I am here!')
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		# print(username,password)
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('/picpuzzle')

	return render_to_response('picturepuzzle/login.html',{'error':error},RequestContext(request))

	

def Logout(request):

	# cur_level = user_level.objects.get(user=request.user)
	# print(cur_level.user.username)
	# cur_level.Time=datetime.datetime.now()
	# cur_level.save()
	
	logout(request)
	return redirect('/picpuzzle')



def Signup(request):
	error = {'has_error':False}

	if request.method == 'POST':
		username = request.POST.get('username','')
		email = request.POST.get('email','')
		password = request.POST.get('password','')
		name = request.POST.get('name','')

		if username=='' or password=='' or email=='' or name=='':
			return redirect('/picpuzzle/signup')

		
		try:

			user = User.objects.create_user(username=username,first_name=name,email=email,password=password)
			user.save()
		except Exception as e:
			return redirect('/picpuzzle/signup',error='Username exists!')
		user=authenticate(username=username,password=password)
		login(request,user)
		user_level.objects.create(user=user,level=1)
		return redirect('/picpuzzle')




	return render_to_response('picturepuzzle/signup.html',{'error':error},RequestContext(request))