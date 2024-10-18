from rest_framework.routers import DefaultRouter

from book.views import BookViewSet

router = DefaultRouter()
router.register('', BookViewSet, basename='book')

urlpatterns = router.urls
