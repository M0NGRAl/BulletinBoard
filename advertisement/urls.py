from django.contrib import admin
from django.urls import path, include
from .views import (AdvertisementList, AdvertisementDetail, AdvertisementCreate,
                    AdvertisementUpdate, AdvertisementDelete, ResponseList, ResponseCreate, subscribe_to_categories)

urlpatterns = [
    path('advertisements/', AdvertisementList.as_view(), name = 'advertisement_list'),
    path('advertisement/<int:pk>/', AdvertisementDetail.as_view(), name = 'advertisement_detail'),
    path('advertisement/create/', AdvertisementCreate.as_view(), name = 'advertisement_create'),
    path('advertisement/update/<int:pk>/', AdvertisementUpdate.as_view(), name = 'advertisement_update'),
    path('advertisement/delete/<int:pk>/', AdvertisementDelete.as_view(), name = 'advertisement_delete'),
    path('advertisement/create_response/<int:pk>/', ResponseCreate.as_view(), name = 'response_create'),
    path('responses/', ResponseList.as_view(), name = 'responses'),
    path('advertisement/subscription', subscribe_to_categories, name = 'subscription')
    ]
