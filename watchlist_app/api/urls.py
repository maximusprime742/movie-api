from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import StreamDetailAV, WatchListAV,\
                                    WatchDetailAV, StreamPlatformAV,\
                                    ReviewList, ReviewDetail, ReviewCreate,\
                                    StreamPlatformVS


router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>', WatchDetailAV.as_view(), name='movie-details'),

    path('', include(router.urls)),

    # path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>', StreamDetailAV.as_view(), name='stream-details'),

    path('review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>', ReviewDetail.as_view(), name='review-details'),

    path('stream/<int:pk>/review-create', ReviewCreate.as_view(),\
         name='review-create'),
    path('stream/<int:pk>/review', ReviewList.as_view(), name='review-list'),
    path('stream/review/<int:pk>', ReviewDetail.as_view(),\
         name='review-detail'),
]
