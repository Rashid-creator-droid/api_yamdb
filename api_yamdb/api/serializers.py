from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoryListField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return CategorySerializer(value).data


class GenreListField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return GenreSerializer(value).data


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreListField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = CategoryListField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    description = serializers.CharField(
        required=False,
    )

    class Meta:
        model = Title
        fields = '__all__'
