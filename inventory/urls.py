from django.urls import path
from . import views


app_name = 'inventory'
urlpatterns = [
    path('', views.devices, name='index'),
    path('devices/', views.devices, name='devices'),
    path('parts/', views.parts, name='parts'),
    path('boms/', views.BOMList.as_view(), name='boms'),
    path('edit_bom/', views.edit_bom, name='edit_bom'),
    path('edit_bom/<int:blueprint_id>', views.edit_bom, name='edit_bom'),
    path('blueprints/', views.blueprints, name='blueprints'),
    path('inventory/', views.InventoryList.as_view(), name='inventory'),
    path('delete/<str:context>/<int:rec_id>', views.delete_record, name='delete_record'),
    path('remainder/', views.remainder, name='remainder'),
    path('part_details/<int:part_id>', views.part_details, name='part_details'),
    path('delete_bom_record/<int:blueprint_id>/<int:rec_id>', views.delete_bom_record, name='delete_bom_record'),
    path('part_update/<int:pk>', views.PartUpdate.as_view(), name='part_update'),

]

