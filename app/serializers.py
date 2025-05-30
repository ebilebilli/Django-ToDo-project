from rest_framework import serializers
from .models import Label, Note, Trash_Bin


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    label = serializers.SlugRelatedField(queryset=Label.objects.filter(is_trashed=False), slug_field='title', required=True)

    class Meta:
        model = Note
        fields = '__all__'

class NoteUpdateSerializer(serializers.ModelSerializer):
    label = serializers.SlugRelatedField(queryset=Label.objects.filter(is_trashed=False), slug_field='title')

    class Meta:
        model = Note
        fields = '__all__'
        exclude = ['is_pinned']

class NotePinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['is_pinned']
        

class TrashBinSerializer(serializers.ModelSerializer):
    note = serializers.PrimaryKeyRelatedField(queryset=Note.objects.all())
    label = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all())
    
    class Meta:
        model = Trash_Bin
        fields = '__all__'
    