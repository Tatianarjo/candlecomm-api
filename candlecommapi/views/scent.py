"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from candlecommapi.models import Scent, scent


class ScentView(ViewSet):
    """CandleComm scents"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single scent

        Returns:
            Response -- JSON serialized scent
        """
        try:
            scent = Scent.objects.get(pk=pk)
            serializer = ScentSerializer(scent, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all scents

        Returns:
            Response -- JSON serialized list of scents
        """
        scents = Scent.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = ScentSerializer(
            scents, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle  operations
        Returns:
            Response -- JSON serialized event instance
        """
        scents = Scent.objects.create(
            scent=request.data["scent"]
        )
        serializer = CreateScentSerializer(scents)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ScentSerializer(serializers.ModelSerializer):
    """JSON serializer for scents

    Arguments:
        serializers
    """
    class Meta:
        model = Scent
        fields = ('id', 'fragrance')

class CreateScentSerializer(serializers.ModelSerializer):
    """JSON serializer for scents

    Arguments:
        serializers
    """
    class Meta:
        model = Scent
        fields = ('id', 'fragrance')