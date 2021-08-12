from django.contrib.auth.models import User 
from django.urls import reverse

from rest_framework import response, status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='pass123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name='Netflix', about='streaming', website='www.netflix.com')

    def test_streamplatfrom_create(self):
        data = {
            'name': 'Netflix',
            'about': 'streaming',
            'website': 'www.netflix.com',
        }
        res = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        res = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        res = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(res.status_code, status.HTTP_200_OK)