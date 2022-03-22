"""View module for handling requests about games"""
from operator import truediv
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from candlecommapi.models import Candle, Scent, JarColor, Profile, Upload


class CandleView(ViewSet):
    """Candle Comm candle"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized candle instance
        """

        # Uses the token passed in the `Authorization` header
        profile = Profile.objects.get(user=request.auth.user)
               

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        candle = Candle()
        candle.profile = profile
        candle.candle_name = request.data["candle_name"]
        import pdb
        pdb.set_trace()
        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `gameTypeId` in the body of the request.
        # scent = Scent.objects.get(pk=request.data["scent"])
        # scent = request.data["scent"]
        
        # candle.scent = scent
        jar_color = JarColor.objects.get(pk=request.data["jar_color"])
        candle.jar_color = jar_color
        # upload = Upload.objects.get(pk=request.data["upload"])
        # candle.upload = upload
      
        # user_profile.rolle.add(self.cleaned_data['rolle'])

        # Try to save the new candle to the database, then
        # serialize the candle instance as JSON, and send the
        # JSON as a response to the client request
        try:
            candle.save()
            # for scent in request.data["scent"]:
            scents = Scent.objects.filter(pk__in=request.data['scent'])
            candle.scent.set(scents)
            serializer = CandleSerializer(candle, context={'request': request})
            return Response(serializer.data)
# tags = Tag.objects.filter(pk__in=request.data['tags']

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single candle

        Returns:
            Response -- JSON serialized candle instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/candles/2
            #
            # The `2` at the end of the route becomes `pk`
            candle = Candle.objects.get(pk=pk)
            serializer = CandleSerializer(candle, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a candle

        Returns:
            Response -- Empty body with 204 status code
        """
        profile = Profile.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        candle = Candle(pk=pk)
        candle.profile = profile
        candle.candle_name = request.data["candle_name"]
        
        
        
        scent = Scent.objects.get(pk=request.data["scent"])
        candle.scent = scent
        jar_color = JarColor.objects.get(pk=request.data["jar_color"])
        candle.jar_color = jar_color
        candle.save()
        # upload = Upload.objects.get(pk=request.data["upload"])
        # candle.upload = upload

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            candle = Candle.objects.get(pk=pk)
            candle.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Candle.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        candles = Candle.objects.all()
        profile = Profile.objects.get(user=request.auth.user)
        

        # Support filtering games by type
        #    http://localhost:8000/candles?type=1
        #
        # That URL will retrieve all tabletop games
        #game_type = self.request.query_params.get('type', None)
        if profile is not None:
            candles = candles.filter(profile__id=profile.id)

        serializer = CandleSerializer(
            candles, many=True, context={'request': request})
        return Response(serializer.data)

class CandleScentSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    class Meta:
        model = Scent
        fields = ('id','fragrance')
        depth = 1

class CandleSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    scent=CandleScentSerializer(many=True)
    class Meta:
        model = Candle
        fields = ('id', 'candle_name', 'scent', 'profile', 'jar_color', 'upload')
        depth = 1