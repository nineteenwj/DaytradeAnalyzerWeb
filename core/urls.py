"""
Define URL patterns for the core app.
This app includes both the presentation and trading views.
"""
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.analysis import views as analysis_views
from core.trading import views as trading_views
from core.login import views as login_views
from core import views as index_views

urlpatterns = [
    path('admin/', auth_views.LoginView.as_view(), name='admin'),
    path('login/', login_views.login_view, name='login'),
    path('register/', login_views.register_user, name='register'),
    path('reset_password/', login_views.reset_password, name='reset_password'),
    path('', index_views.dashboard_view, name='index'),
    path("update/<str:ticker>/", index_views.update_stock, name="update_stock"),
    path('stock_info/<str:ticker_code>/', index_views.stock_info_view, name='stock_info_view'),
    #path('', analysis_views.analysis_index, name='index'),
    path('swing_buy_strategy/', trading_views.swing_buy_strategy_view, name='swing_buy_strategy'),
    # Opening Buy Strategy page
    path("opening_buy_strategy/", trading_views.opening_buy_strategy_view, name="opening_buy_strategy"),
    path("opening_auto_simulation/", trading_views.opening_auto_simulation, name="opening_auto_simulation"),
    path("query_stock_data/", trading_views.query_stock_data, name="query_stock_data"),
    path("calculate_profitloss/", trading_views.calculate_profitloss, name="calculate_profitloss"),
    #path('home/', include('core.stocklist.urls')),
]
