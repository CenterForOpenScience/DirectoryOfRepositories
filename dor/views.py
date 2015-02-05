from dor.models import Repository, Taxonomy, Standards, ContentType, Journal
from dor.serializers import UserSerializer, RepositorySerializer, TaxonomySerializer, StandardsSerializer, ContentTypeSerializer, JournalSerializer
from dor.permissions import IsOwnerOrReadOnly, CanCreateOrReadOnly
from django.contrib.auth.models import User
<<<<<<< HEAD
from django.shortcuts import render_to_response, RequestContext
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import generics, permissions, viewsets
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
=======
from rest_framework import generics, permissions, renderers, viewsets, filters
>>>>>>> 09be62039b94d649a17ae6b4c72b459790d1dbdd
from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view, detail_route, renderer_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
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


class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class ExtraListView(ExtraContext, ListView):
    pass

def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def submission(request):
    return render_to_response('submission.html', {}, content_type=RequestContext(request))