from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import requires_csrf_token

from cseday2016.form_message import SubmitMessage
from cseday2016.models import Contact


def index(request):
    """
    loads the initial web page showing the client the basic view of the website
    if the user is logged in then redirects the user to Newsfeed
    :param request: the HTMLRequest
    :return: either the index.html template if the user is not logged in
            or newsfeed if the user is logged in
    """
    print("\nIn Index method\n")
    if(request.method == 'POST'):
        print("The form has been posted")
        name = request.POST.get('name', 'Undefined')
        email = request.POST.get('email', 'Undefined')
        message = request.POST.get('message', 'Undefined')
        print(name, email, message)
        Contact.objects.create(name=name, email=email, message=message)

    context = RequestContext(request)
    error = {'has_error': False}
    return render_to_response('index.html', {'error': error}, context)


# def submit(request):
#     print("\n\nIn submit method\n\n")

#     error = {'has_error': False}
#     # form = SubmitMessage(request.POST)
#     # if form.is_valid():
#     #     return render_to_response('index.html',{},context_instance = RequestContext(request))
#     # else:
# return render_to_response('index.html', {'error': error},
# context=RequestContext(request))

    # if(request.method == 'POST'):
    #     print("The form has been posted")
    # # context = RequestContext(request)
    # error = {'has_error': False}
    # return render(request, 'index.html', {'error': error})
