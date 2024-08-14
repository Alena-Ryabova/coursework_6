from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

from postmails import views
from postmails.apps import PostmailsConfig
from postmails.views import (MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView,
                             MailingDeleteView, HomeView, ClientListView, ClientCreateView, ClientDetailView,
                             ClientUpdateView, ClientDeleteView, MessageListView, MessageCreateView, MessageDetailView,
                             MessageUpdateView, MessageDeleteView, LogListView)

app_name = PostmailsConfig.name

urlpatterns = [
                  path('', HomeView.as_view(), name='index'),
                  path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
                  path('mailing_detail/<int:pk>', cache_page(60)(MailingDetailView.as_view()), name='mailing_detail'),
                  path('mailing_create', MailingCreateView.as_view(), name='mailing_create'),
                  path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
                  path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
                  path('clients_list/', ClientListView.as_view(), name='clients_list'),
                  path('create/', ClientCreateView.as_view(), name='create'),
                  path('view/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='view'),
                  path('edit/<int:pk>/', ClientUpdateView.as_view(), name='edit'),
                  path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete'),
                  path('message_list/', MessageListView.as_view(), name='message_list'),
                  path('message_create/', MessageCreateView.as_view(), name='message_create'),
                  path('message_view/<int:pk>/', cache_page(60)(MessageDetailView.as_view()), name='message_detail'),
                  path('message_edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
                  path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
                  path('logs_list/', LogListView.as_view(), name='logs_list'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
