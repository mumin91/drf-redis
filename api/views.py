from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.conf import settings
import redis

# Connect to Redis instance
redis_instance = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, )


class ValueList(APIView):

    @staticmethod
    def get(request, format=None) -> Response:
        try:
            keys = request.GET.get('keys')
            values = {}

            # if 'keys' parameter available and not empty make a list from its values
            if keys is not None:
                keys_list = [key.strip() for key in str(keys).split(',')]
                # loop over the list of given keys
                # if the key is available get the value and reset the ttl to 5 minutes
                for key in keys_list:
                    if redis_instance.exists(key):
                        values[key] = redis_instance.get(key)
                        redis_instance.expire(name=key, time=300)
            else:
                for key in redis_instance.keys("*"):
                    values[key.decode("utf-8")] = redis_instance.get(key.decode("utf-8"))

            response = {
                'values': values,
            }
            if not values:
                response['message'] = "No value found"
            else:
                response['message'] = "Value list"

        except Exception as e:

            return Response({"message": "dsf"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content_type="application/json")

        return Response(response, status=status.HTTP_200_OK, content_type="application/json")

    @staticmethod
    def post(request, format=None) -> Response:
        try:
            values = json.loads(request.body)
            keys = list(values.keys())

            for key in keys:
                # Do nothing if the key is already in Redis store
                if redis_instance.exists(key):
                    pass
                else:
                    redis_instance.set(key, values[key], ex=300)
            return Response({"message": "Values added successfully"},
                            status=status.HTTP_201_CREATED,
                            content_type="application/json")
        except:
            return Response({"message": "Error found"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content_type="application/json")

    @staticmethod
    def patch(request, format=None) -> Response:
        try:
            values = json.loads(request.body)

            # Modify the value only if the key is available in the store
            for key in list(values.keys()):
                redis_instance.set(key, values[key], ex=300, xx=True)

        except Exception as e:
            return Response({"message": e},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content_type="application/json")

        return Response({"message": "Values updated"}, status=status.HTTP_204_NO_CONTENT,
                        content_type="application/json")
