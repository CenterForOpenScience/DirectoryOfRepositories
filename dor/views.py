from dor.models import Repository, Taxonomy, Standards, ContentType, Journal
from dor.serializers import UserSerializer, RepositorySerializer, TaxonomySerializer, StandardsSerializer, ContentTypeSerializer, JournalSerializer
from dor.permissions import IsOwnerOrReadOnly, CanCreateOrReadOnly
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext
from sub_form import RepoSubmissionForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from itertools import chain
from django.db.models import Q
from django.contrib import auth
from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
import json

@api_view(('GET', ))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'repos': reverse('repo-list', request=request, format=format)
    })

class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,
                          CanCreateOrReadOnly,]
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', 'repos_endorsed__name', 'repos_endorsed__standards__name']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer


class StandardsViewSet(viewsets.ModelViewSet):
    queryset = Standards.objects.all()
    serializer_class = StandardsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,
                          CanCreateOrReadOnly,]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaxonomyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer



class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = [CanCreateOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,]
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', 'accepted_taxonomy__name',
                     'accepted_content__name']

    def perform_create(self, serializer):
       serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))


def login(request):
    if request.user.is_authenticated():
        return render_to_response('index.html')
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/invalid')


def invalid_login(request):
    if request.user.is_authenticated():
        return render_to_response('index.html')
    else:
        invalid_log = "Incorrect username or password, please try again."
        args = {}

        args['invalid_message'] = invalid_log
        return render_to_response('login.html', args)

@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return render_to_response('index.html')


def repository_list(request):
    taxes = Taxonomy.objects.all()
    standards = Standards.objects.all()
    content_types = ContentType.objects.all()
    repos = Repository.objects.all()

    args = {}
    args.update(csrf(request))

    args['repos'] = repos
    args['taxes'] = taxes
    args['standards'] = standards
    args['content_types'] = content_types

    return render_to_response('search.html', args)

def repositorySearch(request):
    if request.POST:
        search_text = request.POST['search_text']
    else:
        search_text = ''

    repos = Repository.objects.filter(name__contains=search_text)
    taxonomies = Repository.objects.filter(accepted_taxonomy__name=search_text)
    standard = Repository.objects.filter(standards__name=search_text)
    content_types = Repository.objects.filter(accepted_content__name=search_text)

    final_result = list(chain(repos, taxonomies, standard, content_types))

    args = {}
    args.update(csrf(request))

    args['repos'] = final_result

    return render_to_response('ajax_search.html', args)

def repositoryFilter(request):
    if request.POST:
        filtered_text = request.POST['filter_text']
    else:
        filtered_text = []

    json_text = json.loads(filtered_text)
    tag_list = []
    for tag in json_text["tags"]:
        tag_list.append(tag)

    tax_filter_qs = Q()
    standards_filter_qs = Q()
    content_filter_qs = Q()
    final_result = Q()

    for tag in tag_list:
        tax_filter_qs = tax_filter_qs | Q(accepted_taxonomy__name=tag)
    tax_repos = Repository.objects.filter(tax_filter_qs)

    for tag in tag_list:
        standards_filter_qs = standards_filter_qs | Q(standards__name=tag)
    standards_repos = Repository.objects.filter(standards_filter_qs)

    for tag in tag_list:
        content_filter_qs = content_filter_qs | Q(accepted_content__name=tag)
    content_repos = Repository.objects.filter(content_filter_qs)

    if not standards_repos and not content_repos:
        final_result = tax_repos

    elif not tax_repos and not standards_repos:
        final_result = content_repos

    elif not tax_repos and not content_repos:
        final_result = standards_repos

    elif not standards_repos:
        final_result = tax_repos & content_repos

    elif not content_repos:
        final_result = tax_repos & standards_repos

    elif not tax_repos:
        final_result = content_repos & standards_repos

    else:
        final_result = tax_repos & standards_repos & content_repos

    args = {}
    args.update(csrf(request))

    args['repos'] = final_result

    return render_to_response('ajax_search.html', args)


@login_required(login_url='/login/')
def submission(request):
    if request.POST:
        form = RepoSubmissionForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/search/')

    else:
        form = RepoSubmissionForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('submission.html', args)

@login_required(login_url='/login/')
def manage(request):
    return render_to_response('manage.html', {}, context_instance=RequestContext(request))
