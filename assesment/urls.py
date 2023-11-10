from django.urls import path
from .views import upload_csv, reverse_compliment

urlpatterns = [
    path('', upload_csv, name='upload_csv'),
    path('reverse_compliment/', reverse_compliment, name='reverse_compliment'),
]
