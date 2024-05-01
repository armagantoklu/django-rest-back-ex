from django.urls import path
from .views import MakaleApiView, MakaleDetailApiView, GazeteciApiView, GazeteciDetailApiView

urlpatterns = [
    path('makale', MakaleApiView.as_view(), name='makaleler'),
    path('gazeteci', GazeteciApiView.as_view(), name='gazeteci'),
    path('gazeteci/<int:pk>', GazeteciDetailApiView.as_view(), name='gazeteci_detay'),
    path('makale/<int:pk>', MakaleDetailApiView.as_view(), name='makale_detay'),

]
