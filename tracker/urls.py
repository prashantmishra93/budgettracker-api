from django.urls import path
from .views import (
    RegisterView, LoginView, UserDetailView, CategoryListView, BudgetListView, EntryListView, 
    EntrySummaryView, GetBudgetsView, EntryCreateView, CategoryCreateView, AllUserView, 
    DeleteCategoryView, DeleteBudgetView, DeleteTransactionView, GetCategoryByIdView, 
    UpdateCategoryView
)

urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("allUsers", AllUserView.as_view(), name="allUsers"),
    path("detail", UserDetailView.as_view(), name="detail"),
    path('categories', CategoryListView.as_view(), name='categories'),
    path('deleteCategory', DeleteCategoryView.as_view(), name='delete-category'),
    path('getByIdCategory', GetCategoryByIdView.as_view(), name='get-category'),
    path('updateCategory', UpdateCategoryView.as_view(), name='update-category'),
    path('addCategories', CategoryCreateView.as_view(), name='addCategories'),
    path('addBudget', BudgetListView.as_view(), name='addBudget'),
    path('getEntries', EntryListView.as_view(), name='get_entries'),
    path('deleteTransaction', DeleteTransactionView.as_view(), name='deleteTransaction'),
    path('deleteBudget', DeleteBudgetView.as_view(), name='deleteBudget'),
    path('entriesSummary', EntrySummaryView.as_view(), name='entries_summary'),
    path('entries', EntryCreateView.as_view(), name='entries'),
    path('getBudgets', GetBudgetsView.as_view(), name='get_budgets'),
]