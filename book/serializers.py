from rest_framework import serializers

from book.models import Book
from shared.Filters import CustomFilterSet
from shared.googleBookApi import fetch_book_data_from_google_books


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'status']

    def create(self, validated_data):
        title = validated_data.get('title')
        author = validated_data.get('author')

        book_data = fetch_book_data_from_google_books(title, author)

        if book_data:
            validated_data.update(book_data)

        return super().create(validated_data)

    def to_representation(self, data):
        return BookSerializer(context=self.context).to_representation(data)


class BookFilterSet(CustomFilterSet):
    class Meta:
        model = Book
        fields = [
            'status',
        ]
