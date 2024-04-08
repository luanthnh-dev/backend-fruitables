from django.urls import path
from products import views

urlpatterns = [
    path("category/", views.CategoryAPIView.as_view()),
    path("category/<slug:id_slug>/", views.CategoryDetailAPIView.as_view()),

    path("product/<slug:product_id_slug>/images/",
         views.ProductImageAPIView.as_view()),
    path("product/<slug:product_id_slug>/images/<slug:id_slug>/",
         views.ProductImageDetailAPIView.as_view()),

    path("product/<slug:product_id_slug>/comments/",
         views.ProductCommentAPIView.as_view()),
    path("product/<slug:product_id_slug>/comments/<slug:id_slug>/",
         views.ProductCommentDetailAPIView.as_view()),

    path("product/", views.ProductViewAPI.as_view()),
    path("product/<slug:id_slug>/", views.ProductDetailAPIView.as_view()),
    path("latest-products/", views.LatestProductsAPIView.as_view()),
    path("top-rated-products/", views.TopRatedProductsAPIView.as_view()),
    path("review-products/", views.ReviewProductsAPIView.as_view()),
]
