from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('login/', LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
	path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]