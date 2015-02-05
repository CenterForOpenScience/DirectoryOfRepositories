__author__ = 'huynh'

from models import Repository
from serializers import RepositorySerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response


class RepoList(APIView):
    def get(self,request,format=None):
        repos = Repository.objects.all()
        serialized_repos = RepositorySerializer(repos, many=True)
        return Response(serialized_repos.data)

class RepoDetail(APIView):
    def get_object(self, pk):
        try:
            return Repository.objects.get(pk=pk)
        except Repository.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        repo = self.get_object(pk)
        serialized_repo = RepositorySerializer(repo)
        return Response(serialized_repo.data)