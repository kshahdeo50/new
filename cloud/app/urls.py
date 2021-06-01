from django.urls import path
from app import views
urlpatterns = [
    path('', views.home),
    #path('product-detail/', views.product_detail, name='product-detail'),
    path('product-detail/',views.RdsView.as_view(),name = 'product-detail'),
    path('cart/', views.add_to_cart, name='add-to-cart'),
    #path('cart/',views.add_to_cart,name="add_to_cart"),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.IamView.as_view(), name='orders'),
    path('changepassword/', views.change_password, name='changepassword'),
    #path('mobile/', views.mobile, name='mobile'),
    path('mobile/',views.ProjectView.as_view(),name= "mobile"),
    path('mobile/registration',views.BillView.as_view()),
    path('mobile/order',views.IamView.as_view()),
    path('mobile/buy',views.buy_now),
    path('product-detail/cart',views.add_to_cart),
    
    
    path('login/', views.login, name='login'),
    #path('registration/', views.customerregistration, name='customerregistration')
    path('registration/',views.BillView.as_view(),name = 'customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('function/',views.function),
    ]   
