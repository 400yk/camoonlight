from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from ca.models import UserProfile, Program, Package, Tracking, Article
from ca.forms import UserProfileForm, UserForm
from django.views import generic
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView
from haystack.forms import FacetedSearchForm
import simplejson as json

# Global constant
MAX_PROGRAM = 10 # Max number of programs that can be shown in the result list

def home(request):
    context = RequestContext(request)
    return render_to_response('ca/home.html', context)


def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit = False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                print "Profile photo uploaded."

            profile.save()

            # ManyToMany relationships can't be added until after the model object is saved
            selected_fav_programs = profile_form.cleaned_data['fav_program']
            if selected_fav_programs:
                profile.fav_program = selected_fav_programs
            selected_packages = profile_form.cleaned_data['packages']
            if selected_packages:
                for package in selected_packages:
                    tracking = Tracking.objects.get_or_create(package = package, user = profile)
                    print tracking
                    tracking[0].save()

            profile.save()
            registered = True
            # Deal with the favorite programs

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response('ca/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
        }, context)

def user_login(request):
    context = RequestContext(request)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return HttpResponseRedirect('/ca/')
            else:
                return HttpResponse('Your account has been disabled')
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return render_to_response("ca/login.html", {'bad_details': True}, context)
    else:
        return render_to_response('ca/login.html', {'bad_details': False}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/ca/')

@login_required
def profile(request):
    context = RequestContext(request)
    user = request.user
    profile = UserProfile.objects.get(user = user)
    return render_to_response('ca/profile.html', {'profile': profile, 'user': user}, context)

@login_required
def edit_profile(request):
    context = RequestContext(request)
    user = request.user
    if user.is_authenticated():
        profile = UserProfile.objects.get(user = user)

        if request.method == "POST":

            print request.FILES
            update_user_form = UserForm(request.POST, instance = user)
            update_profile_form = UserProfileForm(request.POST, request.FILES, instance = profile)
            if update_user_form.is_valid():
                if update_profile_form.is_valid():
                    user = update_user_form.save()
                    user.set_password(user.password)
                    profile = update_profile_form.save(commit = False)
                    selected_fav_programs = update_profile_form.cleaned_data['fav_program']
                    selected_packages = update_profile_form.cleaned_data['packages']
                    # TODO: remove tracking for not_selected_packages
                    # TODO: highlight packages, fav_programs that are already selected before
                    profile.fav_program = selected_fav_programs
                    if 'picture' in request.FILES:
                        profile.picture = request.FILES['picture']
                        print "Profile photo updated."

                    # Manually save M2M through relationship
                    for package in selected_packages:
                        tracking = Tracking.objects.get_or_create(package = package, user = profile)
                        print tracking
                        tracking[0].save()
                    user.save()
                    profile.save()
                    print "Update profile successful"
                    # Redirect to profile page
                    return render_to_response("ca/profile.html", {
                        'user': user,
                        'profile': profile,
                        }, context)
        else:
            update_user_form = UserForm(instance = user)
            update_profile_form = UserProfileForm(instance = profile, initial = {'packages': [p.id for p in profile.packages.all()]})

        return render_to_response('ca/edit_profile.html', {
                    'profile': profile,
                    'user': user,
                    'edituser': update_user_form,
                    'editprofile': update_profile_form,
                    },
                context)
    else:
        # TODO: Your session has timed out!
        pass 

# Helper function for program_search()
# TODO: delete duplicate search, add second category
def search_program(starts_with = {}):
    program_list = []
    if starts_with:
        filterargs = {}
        for k, v in starts_with.iteritems():
            if v:
                # Ignore case
                filterargs['{0}__{1}'.format(k, 'icontains')] = v

        if filterargs:
            program_list = Program.objects.filter(**filterargs)
        else:
            program_list = Program.objects.all()
    else:
        program_list = Program.objects.all()

    return program_list

def program_search(request):
    context = RequestContext(request)
    starts_with = {}
    programs_list = []

    field_list = ['name']
    if request.method == "GET":
        for field in field_list:
            starts_with[field] = request.GET['search_' + field]
    else:
        for field in field_list:
            starts_with[field] = request.POST['search_' + field]

    program_list = search_program(starts_with)
    # Limit the number of program to be rendered to HTML
    if MAX_PROGRAM > 0:
        if len(program_list) > MAX_PROGRAM:
            limit_program_list = program_list[:MAX_PROGRAM]
        else:
            limit_program_list = program_list

    # Save the whole resulted program_list to session, to be used by categories for subsetting
    # First convert to JSON object

    # Get the categories
    # max number of sub-categories that can be shown
    max_counts = 6
    top_counts = []

    return render_to_response('ca/program_search.html', {'program_list': limit_program_list}, context)

@login_required
def program_detail(request, program_id):
    context = RequestContext(request)
    if program_id:
        program = Program.objects.get(pk = program_id)
    return render_to_response('ca/program_detail.html', {
        'program': program,
        }, context)

# Simple view of one article
def articles(request):
    context = RequestContext(request)
    return render_to_response('ca/articles.html', {
        'articles': Article.objects.all(),
        }, context)

def article_detail(request, article_id):
    context = RequestContext(request)
    if article_id: 
        article = Article.objects.get(pk = article_id)
    return render_to_response('ca/article_detail.html', {
        'article': article,
        }, context)

def search_haystack(request):
    if request.method == "GET" and request.GET['search_name']:
        program = SearchQuerySet().autocomplete(content_auto=request.GET.get('search_name',''))[:5]
        # program is of SearchResult class, need to call .object to retrieve its field
        suggestions = [p.object for p in program]
    else: 
        suggestions = None
    # Make sure return a JSON object, not a bare list
    # Otherwise would be vulnerable to an XSS attack.
    """
    suggestions_json = json.dumps({
        'program_list': suggestions
        })
    """
    return render_to_response('ca/program_search.html', {
        'program_list': suggestions,
        })
    # return HttpResponse(suggestions_json, content_type = 'application/json')

@login_required
def add_fav_program(request):
    if request.method == "GET":
        program_id = request.GET['program_id']
        program = Program.objects.get(pk = program_id)
        user = request.user
        # Add program_id to the user fav_program field
        profile = UserProfile.objects.get(user = user)
        profile.fav_program.add(program)
        profile.save()
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@login_required
def rm_fav_program(request):
    if request.method == "GET":
        program_id = request.GET['program_id']
        user = request.user
        profile = UserProfile.objects.get(user = user)
        program = Program.objects.get(pk = program_id)
        profile.fav_program.remove(program)
        profile.save()
        return HttpResponse(True)
    else:
        return HttpResponse(False)
