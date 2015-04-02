from dor.models import Repository, Taxonomy, Standards, ContentType, Journal
from dor.serializers import UserSerializer, RepositorySerializer, TaxonomySerializer, StandardsSerializer, ContentTypeSerializer, JournalSerializer
from dor.permissions import IsOwnerOrReadOnly, CanCreateOrReadOnly
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext, get_object_or_404
from sub_form import RepoSubmissionForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from itertools import chain
from django.contrib import auth
from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
import json


@api_view(('GET',))
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
                          CanCreateOrReadOnly, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', 'repos_endorsed__name',
                     'repos_endorsed__standards__name']

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
                          CanCreateOrReadOnly, ]

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
                          IsOwnerOrReadOnly, ]
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
        return render_to_response('index.html', context_instance=RequestContext(request))
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c, context_instance=RequestContext(request))


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
        return render_to_response('index.html', context_instance=RequestContext(request))
    else:
        invalid_log = "Incorrect username or password, please try again."
        args = {}

        args['invalid_message'] = invalid_log
        return render_to_response('login.html', args, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return render_to_response('index.html', context_instance=RequestContext(request))


def repository_list(request):
    taxes = Taxonomy.objects.all()
    # standards = Standards.objects.all()
    content_types = ContentType.objects.all()
    repos = Repository.objects.all()
    journals = Journal.objects.all()

    args = {}
    args.update(csrf(request))

    args['repos'] = repos
    args['taxes'] = taxes
    # args['standards'] = standards
    args['content_types'] = content_types
    args['journals'] = journals

    return render_to_response('search.html', args, context_instance=RequestContext(request))

def repositorySearch(request):
    if request.POST:
        search_text = request.POST['search_text']
    else:
        search_text = ''

    journal_list = []

    repos = Repository.objects.filter(name__contains=search_text)
    taxonomies = Repository.objects.filter(accepted_taxonomy__name__contains=search_text)
    content_types = Repository.objects.filter(accepted_content__name__contains=search_text)
    journals_filter = Journal.objects.filter(name__contains=search_text)
    journals = Journal.objects.all()

    if journals_filter:
        for jour in journals_filter:
            for jour_repo in jour.repos_endorsed.all():
                journal_list.append(jour_repo)

    final_result = list(set(chain(repos, taxonomies, journal_list, content_types)))

    args = {}
    args.update(csrf(request))

    args['repos'] = final_result
    args['journals'] = journals

    return render_to_response('ajax_search.html', args, context_instance=RequestContext(request))

def repositoryFilter(request):
    if request.POST:
        filtered_text = request.POST['filter_text']
    else:
        filtered_text = []

    json_text = json.loads(filtered_text)
    tag_list = []
    for tag_pairs in json_text:
        tag_list.append(tag_pairs)

    tax_filter_qs = Repository.objects.all()
    journal_list_qs = []

    if tag_list != [{}]:
        for tuples in tag_list:
            if tuples['type'] == "taxonomy-dropdown":
                tax_filter_qs = tax_filter_qs.filter(accepted_taxonomy__name=tuples['tag'])
            if tuples['type'] == "content-dropdown":
                tax_filter_qs = tax_filter_qs.filter(accepted_content__name=tuples['tag'])
            if tuples['type'] == "journal-dropdown":
                current_journal = Journal.objects.filter(name=tuples['tag'])
                for jour_repos in current_journal.values('repos_endorsed'):
                    for current_repos in tax_filter_qs.filter(id=jour_repos['repos_endorsed']):
                        journal_list_qs.append(current_repos)
                tax_filter_qs = Repository.objects.filter(id__in=[j_repo.id for j_repo in journal_list_qs])
    tax_repos = list(tax_filter_qs)

    args = {}
    args.update(csrf(request))

    args['repos'] = tax_repos
    args['journals'] = Journal.objects.all()

    return render_to_response('ajax_search.html', args, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def endorse(request):
    endorsed_repo = request.POST.get('repo_id', '')
    journal_id = request.POST.get('jour_id', '')

    r = Repository.objects.get(pk=endorsed_repo)
    j = Journal.objects.get(pk=journal_id)
    j.save()

    if r in j.repos_endorsed.all():
        j.repos_endorsed.remove(r)
    else:
        j.repos_endorsed.add(r)

    return HttpResponse(endorsed_repo)

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

    return render_to_response('submission.html', args, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def manage(request):
    repos = Repository.objects.all()

    args = {}
    args.update(csrf(request))

    args['repos'] = repos
    return render_to_response('manage.html', args, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def approve_embargo(request):
    approved_repo = request.POST.get('repo_id', '')

    r = Repository.objects.get(pk=approved_repo)

    if r.allows_embargo_period:
        r.allows_embargo_period = False
        r.save()
    else:
        r.allows_embargo_period = True
        r.save()

    return HttpResponse(approved_repo)

@login_required(login_url='/login/')
def manage_repo(request, pk):
    repo_instance = get_object_or_404(Repository, pk=pk)
    form = RepoSubmissionForm(instance=repo_instance)
    if request.POST:
        form = RepoSubmissionForm(request.POST, instance=repo_instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/manage/')
        else:
            args = {}
            args.update(csrf(request))

            args['form'] = form
            return render_to_response('manage_repo.html', args, context_instance=RequestContext(request))

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['repo'] = Repository.objects.get(pk=pk)

    return render_to_response('manage_repo.html', args, context_instance=RequestContext(request))
