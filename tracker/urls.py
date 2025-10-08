from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, CategoryListView, BudgetListView, EntryListView, EntrySummaryView, GetBudgetsView, EntryCreateView

urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("me", UserDetailView.as_view(), name="me"),
    path('categories', CategoryListView.as_view(), name='categories'),
    path('budgets', BudgetListView.as_view(), name='budgets'),
    path('getEntries', EntryListView.as_view(), name='get_entries'),
    path('entriesSummary', EntrySummaryView.as_view(), name='entries_summary'),
    path('entries', EntryCreateView.as_view(), name='entries'),
    path('getBudgets', GetBudgetsView.as_view(), name='get_budgets'),
]