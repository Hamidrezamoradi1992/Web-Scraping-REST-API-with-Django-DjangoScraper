from rest_framework import serializers

from apps.carolerApi.models import Category, Music


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class MusicSerializers(serializers.ModelSerializer):
    music_category = CategorySerializers(many=True, read_only=True)

    class Meta:
        model = Music
        fields = (
        'id','title_album','time_music','url_detail_page', 'title_music', 'actor_name', 'url_picture', 'link_downloads_128', 'link_downloads_300', 'music_category')

