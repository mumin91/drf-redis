import redis
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase


class ValuesTests(APITestCase):
    redis_instance = redis.Redis(host=settings.REDIS_HOST,
                                 port=settings.REDIS_PORT, )
    factory = APIRequestFactory()

    def test_get_all_values(self):
        """
        Check if get data works properly
        """
        self.redis_instance.flushdb()
        self.redis_instance.flushall()

        self.redis_instance.set('name1', 'mumin')

        url = reverse('values')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.redis_instance.flushdb()
        self.redis_instance.flushall()

    def test_get_specific_values(self):
        """
        Check if get with parameter data works properly
        """
        self.redis_instance.flushdb()
        self.redis_instance.flushall()
        self.redis_instance.set('name1', 'mumin')
        self.redis_instance.set('name2', 'rahman')

        response = self.client.get('/values?keys=name1,name2', content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content_type, "application/json")

        self.redis_instance.flushdb()
        self.redis_instance.flushall()

    def test_get_specific_values_partial(self):
        """
        Check if get with extra parameter works properly
        """
        self.redis_instance.flushdb()
        self.redis_instance.flushall()
        self.redis_instance.set('name1', 'mumin')

        response = self.client.get('/values?keys=name1,name2')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("application/json", response.content_type)

        self.redis_instance.flushdb()
        self.redis_instance.flushall()

    def test_post_values(self):
        """
        Check if post data works properly
        """
        url = reverse('values')
        data = {'name': 'bristi', 'name3': 'mishu'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.redis_instance.flushdb()
        self.redis_instance.flushall()

    def test_patch_values(self):
        """
        Check if patch data works properly
        """
        self.redis_instance.flushdb()
        self.redis_instance.flushall()
        self.redis_instance.set('name1', 'mumin')
        url = reverse('values')
        response = self.client.patch(url, data={"name1": "rinu"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.redis_instance.flushdb()
        self.redis_instance.flushall()
