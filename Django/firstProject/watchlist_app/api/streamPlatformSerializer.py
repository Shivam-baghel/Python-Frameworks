
from rest_framework import serializers
from watchlist_app.models import StreamPlatform
from watchlist_app.api.serializers import WatchlistSerializer


class streamPlatformSerializer(serializers.ModelSerializer):
    
    # many= True for showing multiple movie list
    watchlist = WatchlistSerializer(many=True, read_only=True)
    class Meta:
        
        model = StreamPlatform
        fields = "__all__"
        