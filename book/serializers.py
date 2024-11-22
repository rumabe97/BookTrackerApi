from datetime import datetime

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
        if 'publishedDate' in book_data:
            original_date = book_data['publishedDate']
            print(original_date)
            book_data['publishedDate'] = self.parse_published_date(original_date)
        if book_data:
            validated_data.update(book_data)

        return super().create(validated_data)

    def to_representation(self, data):
        return BookSerializer(context=self.context).to_representation(data)

    def parse_published_date(self, published_date):
        try:
            if len(published_date) == 4 and published_date.isdigit():
                return datetime(int(published_date), 1, 1)
            return datetime.strptime(published_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            return datetime(datetime.now().year, 1, 1)


class BookFilterSet(CustomFilterSet):
    class Meta:
        model = Book
        fields = [
            'status',
        ]
