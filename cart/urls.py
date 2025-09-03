from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartModalView.as_view(), name='cart_modal'),
    path('add/<slug:slug>/', views.AddCartView.as_view(), name='add_to_cart'),
    path('update/<int:item_id>/',
         views.UpdateCartItemView.as_view(), name='update_item'),
    path('remove/<int:item_id>/',
         views.RemoveCartItemView.as_view(), name='remove_item'),
    path('count/', views.CartCountView.as_view(), name='cart_count'),
    path('clear/', views.CartClearView.as_view(), name='cart_clear'),
    path('summary/', views.SummaryCartView.as_view(), name='cart_summary'),
]
