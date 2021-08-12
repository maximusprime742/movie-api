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


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='pass123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name='Netflix', about='streaming', website='www.netflix.com')
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title='Example', description='ex dest', active=True)

    def test_watchlist_create(self):
        data = {
            'platform': self.stream,
            'title': 'Example',
            'description': 'ex desc',
            'active': True,
        }
        res = self.client.post(reverse('movie-list'), data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        res = self.client.get(reverse('movie-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_watchlist_ind(self):
        res = self.client.get(reverse('movie-details', args=(self.watchlist.id,)))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title, 'Example')


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='pass123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name='Netflix', about='streaming', website='www.netflix.com')
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title='Example', description='ex dest', active=True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream, title='Example2', description='ex dest2', active=True)
        self.review = models.Review.objects.create(review_user=self.user, rating=5, description='fantastic', watchlist=self.watchlist2, active=True)

    def test_review_create(self):
        data = {
            'review_user': self.user,
            'rating': 5,
            'description': 'awesome',
            'watchlist': self.watchlist,
            'active': True
        }
        res = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            'review_user': self.user,
            'rating': 5,
            'description': 'awesome',
            'watchlist': self.watchlist,
            'active': True
        }
        self.client.force_authenticate(user=None)
        res = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            'review_user': self.user,
            'rating': 4,
            'description': 'awesome - u',
            'watchlist': self.watchlist,
            'active': False
        }
        res = self.client.put(reverse('review-details', args=(self.review.id,)), data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        res = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_review_ind(self):
        res = self.client.get(reverse('review-list', args=(self.review.id,)))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_review_ind_delete(self):
        res = self.client.delete(reverse('review-details', args=(self.review.id,)))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        res = self.client.get('/watch/reviews/?username' + self.user.username)
        self.assertEqual(res.status_code, status.HTTP_200_OK)