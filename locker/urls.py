from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_document, name='upload'),
    path('download/<int:doc_id>/', views.download_document, name='download'),
    path('delete/<int:doc_id>/', views.delete_document, name='delete'),
    path('preview/<int:doc_id>/', views.preview_document, name='preview'),
    path('stream/pdf/<int:doc_id>/', views.stream_pdf, name='stream_pdf'),
    path("documents/bulk-delete/confirm/", views.bulk_delete_confirm, name="bulk_delete_confirm"),
    path("documents/bulk-delete/", views.bulk_delete, name="bulk_delete"),
    path('document/<int:pk>/edit/', views.edit_document, name='edit'),


]


