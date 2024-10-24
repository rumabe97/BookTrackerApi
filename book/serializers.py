from rest_framework import serializers

from book.models import Book
from shared.Filters import CustomFilterSet
from shared.googleBookApi import fetch_book_data_from_google_books


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CreateBookSerializer(serializers.ModelSerializer):
    idGoogle = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Book
        fields = ['idGoogle', 'status']

    def create(self, validated_data):
        idGoogle = validated_data.get('idGoogle')
        book_data = fetch_book_data_from_google_books(idGoogle)

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
