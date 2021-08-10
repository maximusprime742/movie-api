from django.urls import path  # , include
#  from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import StreamDetailAV, WatchListAV,\
                                    WatchDetailAV, StreamPlatformAV


urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>', WatchDetailAV.as_view(), name='movie-details'),
    path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    path('stream/<int:pk>', StreamDetailAV.as_view(), name='stream-details')
]
