from rest_framework import serializers
from .models import Label, Note, Trash_Bin


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    label = LabelSerializer()

    class Meta:
        model = Note
        fields = '__all__'


class TrashBinSerializer(serializers.ModelSerializer):
    note = NoteSerializer(read_only=True)
    label = LabelSerializer(read_only=True)
    
    class Meta:
        model = Trash_Bin
        fields = '__all__'
    