from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('about/', views.About.as_view(), name="about"), # <- new route
    path('parks/', views.ParksList.as_view(), name="parks_list"),
    path('parks/new/', views.ParkCreate.as_view(), name="park_create"),
    path('parks/<int:pk>/', views.ParkDetail.as_view(), name="park_detail"),
    path('parks/<int:pk>/update',views.ParkUpdate.as_view(), name="park_update"),
    path('parks/<int:pk>/delete',views.ParkDelete.as_view(), name="park_delete"),
    path('parks/<int:pk>/sites/new/', views.SiteCreate.as_view(), name="site_create"),
    path('favoritelists/<int:pk>/sites/<int:site_pk>/', views.FavoritelistSiteAssoc.as_view(), name="favoritelist_site_assoc"),
    path('accounts/signup/', views.Signup.as_view(), name="signup")
]
