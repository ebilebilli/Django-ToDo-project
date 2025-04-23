from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.views import APIView, status, Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction

from .models import Note, Label, Trash_Bin
from .serializers import *
from utils.permission import HeHasPermission
from utils.pagination import CustomPagination


class LabelListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]
    pagination_class = CustomPagination

    def get(self, request):
        user = request.user
        page = request.query_params.get('page', '1')
        page_size = request.query_params.get('page_size', '10')
        cache_key = f'label_list_{user.id}_page_{page}_size_{page_size}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        pagination = self.pagination_class()
        labels = Label.objects.filter(is_trashed=False).order_by('-created_at')
        if labels.exists():
            result_page = pagination.paginate_queryset(labels, request) 
            serializer = LabelSerializer(result_page, many=True)
            paginated_response = pagination.get_paginated_response(serializer.data).data
            cache.set(cache_key, paginated_response, timeout=60*5)
            return Response(paginated_response, status=status.HTTP_200_OK)
        
        cache.set(cache_key, {'message': 'There are no labels'}, timeout=60*5)
        return Response({'message': 'There are no labels'}, status=status.HTTP_404_NOT_FOUND)
    

class LabelDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def get(self, request, label_id):
        user = request.user
        cache_key = f'label_detail_{label_id}_user_{user.id}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        label = get_object_or_404(Label.objects.filter(is_trashed=False), id=label_id)
        serializer = LabelSerializer(label, many=False)
        cache.set(cache_key, serializer.data, timeout=60*5)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, label_id):
        user = request.user
        label = get_object_or_404(Label.objects.filter(is_trashed=False), id=label_id)
        serializer = LabelSerializer(label, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateLabelAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def post(self, request):
        user = request.user
        data = request.data
        serializer = LabelSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MoveLabelToTrashAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def post(self, request, label_id):
        user = request.user
        label = get_object_or_404(Label, id=label_id)
        with transaction.atomic():
            label.is_trashed = True
            label.save()
            trash_bin = Trash_Bin.objects.get_or_create(label=label, user=user)
            trash_bin.full_clean()
            return Response({'message': 'Label moved to trash successfully'})


class NoteListForLabelAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]
    pagination_class = CustomPagination

    def get(self, request, label_id):
        user = request.user
        page = request.query_params.get('page', '1')
        page_size = request.query_params.get('page_size', '10')
        cache_key = f'label_{label_id}_note_list_{user.id}_page_{page}_size_{page_size}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        pagination = self.pagination_class()
        label = get_object_or_404(Label.objects.filter(is_trashed=False), id=label_id)
        notes = Note.objects.filter(is_trashed=False, label=label).order_by('-created_at','is_pinned')
        if notes.exists():
            result_page = pagination.paginate_queryset(notes, request)
            serializer = NoteSerializer(result_page, many=True)
            paginated_response = pagination.get_paginated_response(serializer.data).data
            cache.set(cache_key, paginated_response, timeout=60*5)
            return Response(paginated_response, status=status.HTTP_200_OK)
        
        cache.set(cache_key, {'message': 'There are no notes'}, timeout=60*5)
        return Response({'message': 'There are no notes'}, status=status.HTTP_404_NOT_FOUND)
        

class NoteListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]
    pagination_class = CustomPagination

    def get(self, request):
        user = request.user
        page = request.query_params.get('page', '1')
        page_size = request.query_params.get('page_size', '10')
        cache_key = f'note_list_{user.id}_page_{page}_size_{page_size}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        pagination = self.pagination_class()
        notes = Note.objects.filter(is_trashed=False).order_by('-created_at')
        if notes.exists():
            result_page = pagination.paginate_queryset(notes, request)
            serializer = NoteSerializer(result_page, many=True)
            paginated_response = pagination.get_paginated_response(serializer.data).data
            cache.set(cache_key, paginated_response, timeout=60*5)
            return Response(paginated_response, status=status.HTTP_200_OK)
        
        cache.set(cache_key, {'message': 'There are no notes'}, timeout=60*5)
        return Response({'message': 'There are no notes'}, status=status.HTTP_404_NOT_FOUND)
    

class NoteDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def get(self, request, note_id):
        user = request.user
        cache_key = f'note_detail_{note_id}_user_{user.id}'
        cached_data = cache.get(cache_key)

        note = get_object_or_404(Note.objects.filter(is_trashed=False), id=note_id)
        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, note_id):
        if 'is_pinned' in request.data:
            return Response({'message': 'You cannot change pin in this endpoint'},status=status.HTTP_400_BAD_REQUEST)

        note = get_object_or_404(Note.objects.filter(is_trashed=False), id=note_id)   
        serializer = NoteUpdateSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotePinChangeAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def patch(self, request, note_id):
        note = get_object_or_404(Note.objects.filter(is_trashed=False), id=note_id)
        pin_limit = 10
        pinned_count = Note.objects.filter(user=request.user, is_pinned=True, is_trashed=False).count()
        if pinned_count >= pin_limit:
            return Response({'error': f'Pin limit {pin_limit} exceeded'},status=status.HTTP_400_BAD_REQUEST)
                
        serializer = NotePinSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateNoteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def post(self, request):
        user=request.user
        data = request.data
        serializer = NoteSerializer(data=data, many=False)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MoveNoteToTrashAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def post(self, request, note_id):
        user = request.user
        note = get_object_or_404(Note, id=note_id)
        with transaction.atomic():
            note.is_trashed = True
            note.save()
            trash_bin = Trash_Bin.objects.get_or_create(note=note, user=user)
            trash_bin.full_clean()
            return Response({'message': 'Note moved to trash successfully'})


class TrashBinLabelListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        queryset = Trash_Bin.objects.filter(is_trashed=True).order_by('-deleted_at')
        label_title = request.query_params.get('label')
        if label_title:
            queryset = queryset.filter(label__title__iexact=label_title)

        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(queryset, request)
        serializer = TrashBinSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)


class LabelInTrashDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def get(self, request, label_id):
        label=get_object_or_404(Label.objects.filter(is_trashed=True), id=label_id)
        serializer = LabelSerializer(label, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, label_id):
        label = get_object_or_404(Label.objects.filter(is_trashed=True), id=label_id)
        with transaction.atomic():
            label.is_trashed=False
            label.save()
            Trash_Bin.objects.filter(label=label).delete()
            return Response({'message': 'Label restored successfully'}, status=status.HTTP_200_OK)


class TrashBinNoteListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        queryset = Trash_Bin.objects.filter(is_trashed=True).order_by('-deleted_at')
        note_title = request.query_params.get('note')  
        if note_title:
            queryset = queryset.filter(note__title__iexact=note_title)  
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(queryset, request)
        serializer = TrashBinSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)


class NoteInTrashDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def get(self, request, note_id):
        note=get_object_or_404(Note.objects.filter(is_trashed=True), id=note_id)
        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, note_id):
        note = get_object_or_404(Note.objects.filter(is_trashed=True), id=note_id)
        trash_bin = get_object_or_404(Trash_Bin, note=note)
        with transaction.atomic():
            note.is_trashed=False
            if trash_bin.label:
                note.label = trash_bin.label
            else:
                note.label = None
            note.save()
            Trash_Bin.objects.filter(note=note).delete()
            return Response({'message': 'Note restored successfully'}, status=status.HTTP_200_OK)
