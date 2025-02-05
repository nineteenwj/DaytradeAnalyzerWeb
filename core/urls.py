"""
Define URL patterns for the core app.
This app includes both the presentation and trading views.
"""
from django.urls import path
from core.analysis import views as analysis_views
from core.trading import views as trading_views

urlpatterns = [
    path('', analysis_views.analysis_index, name='index'),
    path('simulate/', trading_views.trading_index, name='simulate'),
]
