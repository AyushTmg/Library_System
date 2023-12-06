from rest_framework_nested import routers
from .views import *

router = routers.DefaultRouter()
router.register('profile',ProfileViewSet, basename='profile')
router.register('genre',GenreViewset, basename='genre')
router.register('book',BookViewSet, basename='book')
router.register('borrow',BorrowViewSet,basename='book_borrow')
router.register('return',ReturnBookViewSet,basename='book_return')

book_router=routers.NestedDefaultRouter(router,'book',lookup='book')
book_router.register('images',BookImageViewSet,basename='book_image')
book_router.register('review',ReviewViewSet,basename='book_review')
book_router.register('reservation',ReservationViewSet,basename='book_reservation')

book_review_router=routers.NestedDefaultRouter(book_router,'review',lookup='review')
book_review_router.register('reply',ReplyViewSet,basename='book_review_reply')


urlpatterns = router.urls+book_router.urls+book_review_router.urls