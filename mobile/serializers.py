from rest_framework import serializers
from mobile.models import OrderQarz, Snippet, LANGUAGE_CHOICES, STYLE_CHOICES, Aptekalar, Sotuvchilar, Dorilar, OrderQarzItem


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']




class AptekalarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aptekalar
        fields = ['id', "user", 'name', 'description']


class DorilarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dorilar
        fields = ['id', 'name', 'price', 'available']


class SotuvchilarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sotuvchilar
        fields = ['id', 'name']



class QarzdorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderQarz
        fields = ['id', 'dorilar', 'order', 'apteka', 'quantity', 'date', 'total']

    
class QarzdorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderQarz
        fields = ['id', 'dorilar', 'order', 'apteka', 'quantity', 'date', 'total']


class QarzdorHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderQarzItem
        fields = '__all__'
