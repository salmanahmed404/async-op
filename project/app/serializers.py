from rest_framework import serializers

class FileSerializer(serializers.Serializer):
    """
    Serializer for the uploaded file
    """
    uploaded_file = serializers.FileField(use_url=False)
    