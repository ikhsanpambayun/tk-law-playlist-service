from urllib import response
from django.shortcuts import get_object_or_404, render
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Playlist
from .serializers import PlaylistSerializer

import requests

# Create your views here.

url_verify = 'http://34.168.241.7/api/verify/'

class ManagePlaylist(APIView):

    def get(self, request):
        context = {}
        try:
            headers = {'Authorization':request.headers['Authorization']}
            r = requests.post(url_verify, headers=headers)
            if r.status_code == 200:
                if request.query_params:
                    qp = request.query_params
                    try:
                        id = int(qp['id'][0])
                        playlist = Playlist.objects.filter(id=id)
                        if playlist:
                            serializer = PlaylistSerializer(playlist[0])
                            context = serializer.data
                            return Response(context, status=200)
                        else:
                            context['detail'] = 'Playlist not found'
                            return Response(context, status=404)
                    except:
                        try:
                            username = qp['username']
                            cache_name = 'playlist-' + username
                            if cache.get(cache_name):
                                context = cache.get(cache_name)
                                print('hit cache')
                            else:
                                playlist = Playlist.objects.filter(username=username)
                                serializer = PlaylistSerializer(playlist, many=True)
                                context = serializer.data
                                cache.set(cache_name, serializer.data)
                                print('hit db')
                            return Response(context, status=200)
                        except Exception as e:
                            context['detail'] = 'Bad request'
                            return Response(context, status=400)
                else:
                    context['detail'] = 'Bad request'
                    return Response(context, status=400)
            else:
                context['detail'] = 'Unauthorized'
                return Response(context, status=401)
        except:
            context['detail'] = 'Unauthorized'
            return Response(context, status=401)

    def put(self, request):
        context = {}
        try:
            headers = {'Authorization':request.headers['Authorization']}
            r = requests.post(url_verify, headers=headers)
            if r.status_code == 200:
                playlist = Playlist.objects.filter(id=request.data['id'])
                if playlist:
                    playlist = playlist[0]
                    new_url = request.data['videos']
                    urls = playlist.videos['urls']
                    if new_url in urls:
                        context['detail'] = 'Video already exist'
                        return Response(context, status=400)
                    else:
                        urls.append(new_url)
                        playlist.videos['urls'] = urls
                        playlist.save()
                        serializer = PlaylistSerializer(playlist)
                        return Response(serializer.data, status=200)
                else:
                    context['detail'] = 'Playlist not found'
                    return Response(context, status=404)
            else:
                context['detail'] = 'Unauthorized'
                return Response(context, status=401)
        except:
            context['detail'] = 'Unauthorized'
            return Response(context, status=401)

    def post(self, request):
        context = {}
        try:
            headers = {'Authorization':request.headers['Authorization']}
            r = requests.post(url_verify, headers=headers)
            if r.status_code == 200:
                data = request.data
                url = data['videos']
                videos = {'urls':[url]}
                data['videos'] = videos
                serializer = PlaylistSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    context = serializer.data
                    return Response(context, status=200)
                else:
                    context['detail'] = 'Bad request'
                    return Response(context, status=400)
            else:
                context['detail'] = 'Unauthorized'
                return Response(context, status=401)
        except:
            context['detail'] = 'Unauthorized'
            return Response(context, status=401)
            
    def delete(self, request):
        context = {}
        try:
            headers = {'Authorization':request.headers['Authorization']}
            r = requests.post(url_verify, headers=headers)
            if r.status_code == 200:
                if request.query_params:
                    qp = request.query_params
                    try:
                        id = int(qp['id'][0])
                        video = qp['video']
                        playlist = Playlist.objects.filter(id=id)
                        if playlist:
                            playlist = playlist[0]
                            urls = playlist.videos['urls']
                            if video in urls:
                                urls.remove(video)
                                playlist.videos['urls'] = urls
                                playlist.save()
                                context['detail'] = 'Video deleted'
                                return Response(context, status=200)
                            else:
                                context['detail'] = 'Video not found in playlist'
                                return Response(context, status=404)
                        else:
                            context['detail'] = 'Playlist not found'
                            return Response(context, status=404)
                    except:
                        try:
                            id = int(qp['id'][0])
                            playlist = Playlist.objects.filter(id=id)
                            if playlist:
                                playlist = playlist[0]
                                playlist.delete_update()
                                context['detail'] = 'Playlist deleted'
                                return Response(context, status=200)
                            else:
                                context['detail'] = 'Playlist not found'
                                return Response(context, status=404)
                        except:
                            context['detail'] = 'Bad request'
                            return Response(context, status=400)
                else:
                    context['detail'] = 'Bad request'
                    return Response(context, status=400)
            else:
                context['detail'] = 'Unauthorized'
                return Response(context, status=401)
        except:
            context['detail'] = 'Unauthorized'
            return Response(context, status=401)

class GetPlaylistAll(APIView):

    def get(self, request):
        context = {}
        try:
            headers = {'Authorization':request.headers['Authorization']}
            r = requests.post(url_verify, headers=headers)
            if r.status_code == 200:
                playlist = Playlist.objects.all()
                serializer = PlaylistSerializer(playlist, many=True)
                return Response(serializer.data)
            else:
                context['detail'] = 'Unauthorized'
                return Response(context, status=401)
        except:
            context['detail'] = 'Unauthorized'
            return Response(context, status=401)