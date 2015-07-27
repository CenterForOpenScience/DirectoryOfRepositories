from dor.models import Repository, Taxonomy, Standards, ContentType, Journal, Certification, UserProfile
from dor.serializers import (UserSerializer, RepositorySerializer,
                             TaxonomySerializer, StandardsSerializer,
                             ContentTypeSerializer, JournalSerializer,
                             CertificationSerializer)
from dor.permissions import IsOwnerOrReadOnly, CanCreateOrReadOnly
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.shortcuts import render_to_response, RequestContext, get_object_or_404
from sub_form import UserSubmissionForm, RepoSubmissionForm, ContentSubmissionForm, StandardSubmissionForm, TaxSubmissionForm, AnonymousRepoSubmissionForm, CertificationSubmissionForm, JournalSubmissionForm
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
    queryset = Journal.objects.all().filter(is_visible=True)
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


class CertificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer


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
    search_fields = ['name', 'alt_names',
                     'description', 'remarks',
                     'hosting_institution',
                     'institution_country',
                     'accepted_taxonomy__obj_name',
                     'accepted_content__obj_name',
                     'db_certifications__obj_name']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def validate(form):
    taxes = form.data.get("accepted_taxonomy")
    if not taxes:
        return form
    form.data._mutable = True
    form.data.setlist("accepted_taxonomy", taxes.strip('[]').split(','))
    form.data._mutable = False
    return form

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))


def login(request):
    if request.user.is_authenticated():
        return render_to_response('index.html', context_instance=RequestContext(request))
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c, context_instance=RequestContext(request))


def register(request):
    if request.POST:
        form = UserSubmissionForm(request.POST)
        form = validate(form)
        if form.is_valid():
            try:
                form.save()
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                user = auth.authenticate(username=username, password=password)
                log_req = request
                auth.login(log_req, user)
                if form.data['user_type'] == 'Repository Representative':
                    return HttpResponseRedirect('/submit/Repositories/')
                elif form.data['user_type'] == 'Journal Representative':
                    return HttpResponseRedirect('/submit/Journals/')
                else:
                    return HttpResponseRedirect('/')
            except ValidationError as e:
                form.errors.update({u'': e[0]})
    else:
        form = UserSubmissionForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('register.html', args, context_instance=RequestContext(request))


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
        filters = request.POST.getlist('filters[]')
    else:
        search_text = ''
        filters = []

    filter_classes = {}
    filter_classes['journal_list'] = []

    if 'r_name' in filters:
        filter_classes['repos'] = Repository.objects.filter(name__icontains=search_text)
    if 'r_tax' in filters:
        filter_classes['taxonomies'] = Repository.objects.filter(accepted_taxonomy__obj_name__icontains=search_text)
    if 'r_content' in filters:
        filter_classes['content_types'] = Repository.objects.filter(accepted_content__obj_name__icontains=search_text)
    if 'r_desc' in filters:
        filter_classes['description'] = Repository.objects.filter(description__icontains=search_text)
    if 'r_remarks' in filters:
        filter_classes['remarks'] = Repository.objects.filter(remarks__icontains=search_text)
    if 'r_certs' in filters:
        filter_classes['db_certifications'] = Repository.objects.filter(db_certifications__obj_name__icontains=search_text)
    if 'j_name' in filters:
        journals_filter = Journal.objects.filter(name__icontains=search_text)
        journals = Journal.objects.all()
        if journals_filter:
            for jour in journals_filter:
                for jour_repo in jour.repos_endorsed.all():
                    filter_classes['journal_list'].append(jour_repo)
    if 'j_endorsed' in filters:
        journals_filter = Journal.objects.filter(repos_endorsed__name__icontains=search_text)
        journals = Journal.objects.all()
        if journals_filter:
            for jour in journals_filter:
                for jour_repo in jour.repos_endorsed.all():
                    filter_classes['journal_list'].append(jour_repo)

    final_queryset = []
    for class_name in filter_classes:
        for item in filter_classes[class_name]:
            final_queryset.append(item)

    final_result = list(set(chain(final_queryset)))

    args = {}
    args.update(csrf(request))

    args['repos'] = final_result
    try:
        args['journals'] = journals
    except UnboundLocalError:
        args['journals'] = []

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
                tax_filter_qs = tax_filter_qs.filter(accepted_taxonomy__obj_name=tuples['tag'])
            if tuples['type'] == "content-dropdown":
                tax_filter_qs = tax_filter_qs.filter(accepted_content__obj_name=tuples['tag'])
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
    if title == 'Taxonomies':
            if request.POST:
                form = TaxSubmissionForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/submit/Repositories/')
            else:
                form = TaxSubmissionForm()
    elif request.user.is_authenticated():
        if title == 'Journals':
            if request.POST:
                form = JournalSubmissionForm(request.POST)
                form = validate(form)
                if form.is_valid():
                    form.save(user=request.user)
                    return HttpResponseRedirect('/manage/')
            else:
                form = JournalSubmissionForm()
        elif title == 'Repositories':
            if request.POST:
                form = RepoSubmissionForm(request.POST)
                form = validate(form)
                if form.is_valid():
                    form.save(user=request.user)
                    return HttpResponseRedirect('/manage/')
            else:
                form = RepoSubmissionForm()
        elif title == 'Data-Types':
            if request.POST:
                form = ContentSubmissionForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/manage/' + title + '/')
            else:
                form = ContentSubmissionForm()

        elif title == 'Certifications':
            if request.POST:
                form = CertificationSubmissionForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/manage/' + title + '/')
            else:
                form = CertificationSubmissionForm()

        # elif title == 'Standards':
        #     if request.POST:
        #         form = StandardSubmissionForm(request.POST)
        #         if form.is_valid():
        #             form.save()
        #             return HttpResponseRedirect('/manage/'+title+'/')
        #     else:
        #         form = StandardSubmissionForm()
        else:
            return HttpResponseRedirect('/manage/')
    else:
        if title == 'Repositories':
            if request.POST:
                form = AnonymousRepoSubmissionForm(request.POST)
                form = validate(form)
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
    args['taxes'] = Taxonomy.objects.annotate()

    return render_to_response('submit.html', args, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def manage(request):
    if request.user.is_staff:
        return render_to_response('manage.html', context_instance=RequestContext(request))

    profile = UserProfile.objects.get(user=request.user)
    if 'Repository' in profile.user_type:
        return HttpResponseRedirect('/manage/Repositories/')
    elif 'Journal' in profile.user_type:
        return HttpResponseRedirect('/manage/Journals/')
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def manage_group(request, title):
    args = {}
    args.update(csrf(request))

    args['staff'] = request.user.is_staff

    if title == 'Journals':
        if request.user.is_staff:
            args['groups'] = Journal.objects.all()
        else:
            args['groups'] = Journal.objects.filter(owner_id=request.user.id)
            args['repos'] = Repository.objects.filter(owner_id=request.user.id)
        args['title'] = 'Journals'
    elif title == 'Repositories':
        if request.user.is_staff:
            args['groups'] = Repository.objects.all()
        else:
            args['groups'] = Repository.objects.filter(owner_id=request.user.id)
        args['title'] = 'Repositories'
        args['taxes'] = Taxonomy.objects.annotate()
    elif title == 'Data-Types':
        if request.user.is_staff:
            args['groups'] = ContentType.objects.all()
        args['title'] = 'Data-Types'
    # elif title == 'Standards':
    #     args['groups'] = Standards.objects.all()
    #     args['title'] = 'Standards'
    elif title == 'Taxonomies':
        if request.user.is_staff:
            args['groups'] = Taxonomy.objects.all()
        args['title'] = 'Taxonomies'
    elif title == 'Certifications':
        if request.user.is_staff:
            args['groups'] = Certification.objects.all()
        args['title'] = 'Certifications'
    else:
        return HttpResponseRedirect('/')

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

    if title == 'Journals':
        this_title = 'Journals'
        journal_instance = get_object_or_404(Journal, pk=pk)
        group = Journal.objects.get(pk=pk)
        form = JournalSubmissionForm(instance=journal_instance)
        if request.POST:
            form = JournalSubmissionForm(request.POST, instance=journal_instance)
            form = validate(form)
            if form.is_valid():
                form.save(user=request.user)
                return HttpResponseRedirect('/manage/' + title + "/")
            else:
                args = {}
                args.update(csrf(request))

                args['form'] = form
                return render_to_response('submit.html', args, context_instance=RequestContext(request))
    elif title == 'Repositories':
        this_title = 'Repositories'
        repo_instance = get_object_or_404(Repository, pk=pk)
        group = Repository.objects.get(pk=pk)
        form = RepoSubmissionForm(instance=repo_instance)
        if request.POST:
            form = RepoSubmissionForm(request.POST, instance=repo_instance)
            form = validate(form)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/manage/' + title + "/")
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
            form = validate(form)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/manage/' + title + "/")
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
            form = validate(form)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/manage/' + title + "/")
            else:
                args = {}
                args.update(csrf(request))

                args['form'] = form
                return render_to_response('submit.html', args, context_instance=RequestContext(request))
    elif title == 'Certifications':
        this_title = 'Certifications'
        cert_instance = get_object_or_404(Certification, pk=pk)
        group = Certification.objects.get(pk=pk)
        form = CertificationSubmissionForm(instance=tax_instance)
        form = validate(form)
        if request.POST:
            form = CertificationSubmissionForm(request.POST, instance=cert_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/manage/' + title + "/")
            else:
                args = {}
                args.update(csrf(request))

                args['form'] = form
                return render_to_response('submit.html', args, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/manage/' + title + '/')

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['group'] = group
    args['staff'] = request.user.is_staff
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
    elif selected_group == "Certifications":
        for repo_id in id_list:
            Certification.objects.filter(id=repo_id).delete()
        return HttpResponse("Certification Success")
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

    new_data = ContentType(parent=None)
    new_data.save()
    new_data.obj_name = data_type_value
    new_data.save()

    response_data = {}
    response_data['id'] = new_data.id
    response_data['name'] = new_data.obj_name

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def add_cert(request):
    if request.POST:
        cert_value = request.POST['cert_value']
    else:
        cert_value = ''

    new_cert = Certification(parent=None)
    new_cert.save()
    new_cert.obj_name = cert_value
    new_cert.save()

    response_data = {}
    response_data['id'] = new_cert.id
    response_data['name'] = new_cert.obj_name

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def add_tax(request):
    if request.POST:
        tax_value = request.POST['tax_value']
    else:
        tax_value = ''

    try:
        tax_parent = Taxonomy.objects.get(id=request.POST['tax_parent'])
    except:
        tax_parent = Taxonomy.objects.get(id=1)  # 'All terms'

    new_tax = Taxonomy(parent=tax_parent)
    new_tax.save()
    new_tax.obj_name = tax_value
    new_tax.embargoed = True
    new_tax.save()

    response_data = {}
    response_data['id'] = new_tax.id
    response_data['name'] = new_tax.obj_name

    return HttpResponse(json.dumps(response_data), content_type="application/json")
