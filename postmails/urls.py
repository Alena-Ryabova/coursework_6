from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

from postmails import views
from postmails.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView

app_name = 'postmails'


urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>', cache_page(60)(MailingDetailView.as_view()), name='mailing'),
    path('mailing_create', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)