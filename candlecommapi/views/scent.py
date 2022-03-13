"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from candlecommapi.models import Scent


class ScentView(ViewSet):
    """Level up scents"""

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

class ScentSerializer(serializers.ModelSerializer):
    """JSON serializer for scents

    Arguments:
        serializers
    """
    class Meta:
        model = Scent
        fields = ('id', 'fragrance')