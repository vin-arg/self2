from django.urls import path
from .views import item_list, item_entry, item_add, item_edit, item_cart, item_transactions

urlpatterns = [
    path("items/", item_list, name="item_list"),
    path("item/<int:num>", item_entry, name="item_entry"),
    path("item/add", item_add, name="item_add"),
    path("item/edit/<int:num>", item_edit, name="item_edit"),
    path("cart", item_cart, name="item_cart"),
    path("transactions", item_transactions, name="item_transactions"),
]