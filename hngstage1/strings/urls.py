from django.urls import path
from .views import StringListCreateView, StringDetailView, NaturalLanguageFilterView

urlpatterns = [
    path('', StringListCreateView.as_view(), name='string-list-create'),
    path('filter-by-natural-language', NaturalLanguageFilterView.as_view(), name='string-natural-language-filter'),
    path('<path:string_value>', StringDetailView.as_view(), name='string-detail'),
]
