from django.urls import path

from . import views

app_name = "inventory"
urlpatterns = [
    path('', views.index,name="home"),
    path('Ingredient/', views.ingredientHome ,name="ingredient"),
    path('IngredientNew/', views.newIngredient ,name="new_ingredient"),
    path('IngredientUpdate/', views.updateIngredient,name="update_ingredient"),
    path('IngredientDelete/', views.deleteIngredient,name="delete_ingredient"),
    path('Items/', views.itemsHome, name="items"),
    path('ItemsNew/', views.newItems, name="new_items"),
    path('ItemsUpdate/', views.updateItems, name="update_items"),
    path('ItemsDelete/', views.deleteItems, name="delete_items"),
    path('Store/', views.storeHome, name="store"),
    path('StoreNew/', views.newStore, name="new_store"),
    path('StoreUpdate/', views.updateStore, name="update_store"),
    path('StoreDelete/', views.deleteStore, name="delete_store"),
    path('Order/', views.orderHome, name="order"),
    path('OrderDetail/<int:OrderID>/', views.orderDetail, name="orderDetail"),
    path('OrderNew/', views.orderNewTemplate, name="orderNew"),
    path('OrderNewCreate/', views.orderNewCreate, name="orderNewCreate"),
    path('OrderAddItems/', views.orderAddItems, name="orderAddItems"),
    path('OrderDeleteItems/', views.orderDeleteItem, name="orderDeleteItems"),
    path('OrderEdit/<int:id>', views.orderEditTemplate, name="orderEdit"),
    path('OrderPrintOptions/<int:orderId>', views.orderPrint, name="orderPrint"),
    path('OrderPrintData/<int:orderId>/<str:dataType>', views.orderPrintData, name="orderPrintData"),
    path('detail/', views.getDetail, name="getInfo"),
    path('detailAll/', views.getAllDetail, name="getInfoAll"),
    path('test1/', views.test1, name="test"),
    path('pdf1/', views.pdfGenration1, name="pdfView"),
    path('pdfHtmlView1/', views.pdfHtmlView, name="htmlView"),
]
