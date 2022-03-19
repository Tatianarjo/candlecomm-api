"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from candlecommapi.models import JarColor


class JarColorView(ViewSet):
    """Candle Comm games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        jar_color = JarColor()

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        jar_color.color = request.data["color"]
        

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `gameTypeId` in the body of the request.
        

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            jar_color.save()
            serializer = JarColorSerializer(jar_color, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single jar_color

        Returns:
            Response -- JSON serialized jar_color instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            jar_color = JarColor.objects.get(pk=pk)
            serializer = JarColorSerializer(jar_color, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        jar_color = JarColor.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        jar_color = JarColor.objects.get(pk=pk)
        jar_color.color = request.data["color"]
        jar_color.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            jar_color = JarColor.objects.get(pk=pk)
            jar_color.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except JarColor.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to jar_colors resource

        Returns:
            Response -- JSON serialized list of jar_colors
        """
        # Get all game records from the database
        jar_colors = JarColor.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/jarcolors?type=1
        #
        # That URL will retrieve all tabletop games
        # game_type = self.request.query_params.get('type', None)
        # if game_type is not None:
        #     games = games.filter(game_type__id=game_type)

        serializer = JarColorSerializer(
            jar_colors, many=True, context={'request': request})
        return Response(serializer.data)


class JarColorSerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializers
    """
    class Meta:
        model = JarColor
        fields = ( 'id', 'color')