from django.http import JsonResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView

from book.models import Book
from book.serializers import BookSerializer, BookFilterSet, CreateBookSerializer
from shared.Filters import GenericViewSetWithFilters
from shared.googleBookApi import search_newest_books, fetch_books_data_from_google_books
from shared.mixins import DynamicSerializersMixin, APIKeyPermission
from django_filters import rest_framework as filters


@extend_schema_view(
    list=extend_schema(description='Get paginated list of books.'),
    create=extend_schema(description='Create a new book.', responses={200: BookSerializer}),
    destroy=extend_schema(description='Delete a book.'),
)
class BookViewSet(DynamicSerializersMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSetWithFilters,
                  RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilterSet
    filter_backends = (filters.DjangoFilterBackend,)

    serializer_classes_by_action = {
        'create': CreateBookSerializer,
    }

    @action(methods=['patch'], detail=True, url_path='update_status', url_name="update_book_status")
    def update_status(self, request, pk=None):
        book = Book.objects.get(pk=pk)
        book.status = request.data.get('status', book.status)
        book.save()
        serializer = BookSerializer(book, many=False)
        return JsonResponse(serializer.data, safe=False)

    @action(methods=['get'], detail=False, url_path='get_newest_relevance', url_name="get_newest_relevance")
    def get_newest_relevance(self, request):
        subject = request.query_params.get('subject', 'fiction')
        order = request.query_params.get('order', 'newest')
        page = int(request.query_params.get('page', 1))
        max_results = int(request.query_params.get('max_results', 10))
        start_index = (page - 1) * max_results
        books = search_newest_books(subject, order, start_index, max_results)
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(methods=['get'], detail=False, url_path='search_google_api', url_name="search_google_api")
    def search_google_api(self, request):
        title = request.query_params.get('title', None)
        author = request.query_params.get('author', None)
        page = int(request.query_params.get('page', 1))
        max_results = int(request.query_params.get('max_results', 10))
        start_index = (page - 1) * max_results
        books = fetch_books_data_from_google_books(title, author, start_index, max_results)
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)

    # def get_permissions(self):
    #     return [APIKeyPermission()]
