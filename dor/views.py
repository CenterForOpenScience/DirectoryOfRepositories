from dor.models import Repository, Taxonomy, Standards, ContentType, Journal
from dor.serializers import UserSerializer, RepositorySerializer, TaxonomySerializer, StandardsSerializer, ContentTypeSerializer, JournalSerializer
from dor.permissions import IsOwnerOrReadOnly, CanCreateOrReadOnly
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext, get_object_or_404
from sub_form import RepoSubmissionForm, ContentSubmissionForm, StandardSubmissionForm, TaxSubmissionForm, AnonymousRepoSubmissionForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from itertools import chain
from django.contrib import auth
from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from treebeard.models import Node
import json


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'repos': reverse('repo-list', request=request, format=format)
    })


class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.filter(is_visible=True)
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
    queryset = Repository.objects.filter(is_visible=True)
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


def submit(request, title):
    if request.user.is_authenticated():
        if title == 'Repositories':
            if request.POST:
                form = RepoSubmissionForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/manage/'+title+'/')
            else:
                form = RepoSubmissionForm()

        elif title == 'Data-Types':
            if request.POST:
                form = ContentSubmissionForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/manage/'+title+'/')
            else:
                form = ContentSubmissionForm()

        # elif title == 'Standards':
        #     if request.POST:
        #         form = StandardSubmissionForm(request.POST)
        #         if form.is_valid():
        #             form.save()
        #             return HttpResponseRedirect('/manage/'+title+'/')
        #     else:
        #         form = StandardSubmissionForm()

        elif title == 'Taxonomies':
            if request.POST:
                form = TaxSubmissionForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/manage/'+title+'/')
            else:
                form = TaxSubmissionForm()
        else:
            return HttpResponseRedirect('/manage/')
    else:
        if title == 'Repositories':
            if request.POST:
                form = AnonymousRepoSubmissionForm(request.POST)
                if form.is_valid():
                    form.save()

                    return render_to_response('search.html', {"submitted_note": "Successfully submitted the repository."}, context_instance=RequestContext(request))
            else:
                form = AnonymousRepoSubmissionForm()
        else:
            return HttpResponseRedirect('/search/')

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['title'] = title
    args['taxes'] = Taxonomy.get_annotated_list()

    return render_to_response('submit.html', args, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def manage(request):
    return render_to_response('manage.html', context_instance=RequestContext(request))


@login_required(login_url='/login/')
def manage_group(request, title):

    if title == 'Repositories':
        groups = Repository.objects.all()
        this_title = 'Repositories'
    elif title == 'Data-Types':
        groups = ContentType.objects.all()
        this_title = 'Data-Types'
    # elif title == 'Standards':
    #     groups = Standards.objects.all()
    #     this_title = 'Standards'
    elif title == 'Taxonomies':
        groups = Taxonomy.objects.all()
        this_title = 'Taxonomies'
    else:
        return HttpResponseRedirect('/manage/')

    annotated_list = Taxonomy.get_annotated_list()

    args = {}
    args.update(csrf(request))

    args['groups'] = groups
    args['title'] = this_title
    args['taxes'] = annotated_list

    return render_to_response('manage_template.html', args, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def approve_embargo(request):
    approved_repo_list = request.POST.get('repo_id_list', '')

    json_text = json.loads(approved_repo_list)
    id_list = []
    for id_item in json_text:
        id_list.append(id_item)

    for id_repo in id_list:
        r = Repository.objects.get(pk=id_repo)

        if r.embargoed:
            r.embargoed = False
            r.save()
        else:
            r.embargoed = True
            r.save()

    return HttpResponse(id_list)

@login_required(login_url='/login/')
def manage_form(request, title, pk):

    if title == 'Repositories':
        this_title = 'Repositories'
        repo_instance = get_object_or_404(Repository, pk=pk)
        group = Repository.objects.get(pk=pk)
        form = RepoSubmissionForm(instance=repo_instance)
        if request.POST:
            form = RepoSubmissionForm(request.POST, instance=repo_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/manage/'+title+"/")
            else:
                args = {}
                args.update(csrf(request))

                args['form'] = form
                return render_to_response('submit.html', args, context_instance=RequestContext(request))
    elif title == 'Data-Types':
        this_title = 'Data-Types'
        content_instance = get_object_or_404(ContentType, pk=pk)
        group = ContentType.objects.get(pk=pk)
        form = ContentSubmissionForm(instance=content_instance)
        if request.POST:
            form = ContentSubmissionForm(request.POST, instance=content_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/manage/'+title+"/")
            else:
                args = {}
                args.update(csrf(request))

                args['form'] = form
                return render_to_response('submit.html', args, context_instance=RequestContext(request))
    # elif title == 'Standards':
    #     this_title = 'Standards'
    #     standard_instance = get_object_or_404(Standards, pk=pk)
    #     group = Standards.objects.get(pk=pk)
    #     form = StandardSubmissionForm(instance=standard_instance)
    #     if request.POST:
    #         form = StandardSubmissionForm(request.POST, instance=standard_instance)
    #         if form.is_valid():
    #             form.save()
    #             return HttpResponseRedirect('/manage/'+title+"/")
    #         else:
    #             args = {}
    #             args.update(csrf(request))
    #
    #             args['form'] = form
    #             return render_to_response('submit.html', args, context_instance=RequestContext(request))
    elif title == 'Taxonomies':
        this_title = 'Taxonomies'
        tax_instance = get_object_or_404(Taxonomy, pk=pk)
        group = Taxonomy.objects.get(pk=pk)
        form = TaxSubmissionForm(instance=tax_instance)
        if request.POST:
            form = TaxSubmissionForm(request.POST, instance=tax_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/manage/'+title+"/")
            else:
                args = {}
                args.update(csrf(request))

                args['form'] = form
                return render_to_response('submit.html', args, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/manage/'+title+'/')

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['group'] = group
    args['title'] = this_title

    return render_to_response('submit.html', args, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def delete_item(request):
    selected_group = request.POST.get('selected_group', '')
    deleted_group_list = request.POST.get('deleted_group_list', '')

    json_text = json.loads(deleted_group_list)
    id_list = []
    for id_item in json_text:
        id_list.append(id_item)

    if selected_group == "Repositories":
        for repo_id in id_list:
            Repository.objects.filter(id=repo_id).delete()
        return HttpResponse("Repository Success")
    elif selected_group == "Data-Types":
        for repo_id in id_list:
            ContentType.objects.filter(id=repo_id).delete()
        return HttpResponse("Data-Type Success")
    elif selected_group == "Taxonomies":
        for repo_id in id_list:
            Taxonomy.objects.filter(id=repo_id).delete()
        return HttpResponse("Taxonomy Success")
    # elif selected_group == "Standards":
    #     for repo_id in id_list:
    #         Standards.objects.filter(id=repo_id).delete()
    #     return HttpResponse("Standards Success")
    else:
        return HttpResponse("Wrong Group")


def add_data_type(request):
    if request.POST:
        data_type_value = request.POST['data_type_value']
    else:
        data_type_value = ''

    new_data = ContentType.create(data_type_value)
    new_data.save()

    response_data = {}
    response_data['id'] = new_data.id
    response_data['name'] = new_data.name

    return HttpResponse(json.dumps(response_data), content_type="application/json")