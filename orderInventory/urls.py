from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "inventory"
urlpatterns = [
    path('', views.index,name="home"),
    path('Category/', views.categoryHome, name="category"),
    path('CategoryNew/', views.newCategory, name="new_category"),
    path('CategoryUpdate/', views.updateCategory, name="update_category"),
    path('CategoryDelete/', views.deleteCategory, name="delete_category"),

    path('Ingredient/', views.ingredientHome ,name="ingredient"),
    path('IngredientNew/', views.newIngredient ,name="new_ingredient"),
    path('IngredientUpdate/', views.updateIngredient,name="update_ingredient"),
    path('IngredientDelete/', views.deleteIngredient,name="delete_ingredient"),

    path('Items/', views.itemsHome, name="items"),
    path('ItemNew/', views.newItems, name="new_items"),
    path('ItemEdit/<int:id>', views.editItems, name="edit_items_template"),
    path('ItemLock/<int:id>', views.lockItem, name="lock_item"),
    path('ItemsDelete/', views.deleteItems, name="delete_items"),

    path('ConfirmOrderList/', views.orderHome, name="orderList"),
    path('OrderDetail/<int:OrderID>/', views.orderDetail, name="orderDetail"),
    path('Order/', views.orderNewCreate, name="orderNewCreate"),
    path('OrderAddItems/', views.orderAddItems, name="orderAddItems"),

    path('OrderEdit/<int:id>', views.orderEditTemplate, name="orderEdit"),
    path('OrderDelete/', views.deleteOrder, name="delete_order"),
    path('OrderLock/<int:OrderId>', views.lockOrder, name="lock_order"),


    path('OrderPrintOptions/<int:orderId>', views.orderPrint, name="orderPrint"),
    path('OrderPrintData/<int:orderId>/<str:dataType>', views.orderPrintData, name="orderPrintData"),
    path('detail/', views.getDetail, name="getInfo"),

    path('OrderList/', views.clientTalks, name="clientTalksList"),

    path('test1/', views.test1, name="test"),
    path('test2/<int:OrderId>', views.test2, name="test2"),
    path('pdf1/', views.pdfGenration1, name="pdfView"),
    path('pdfHtmlView1/', views.pdfHtmlView, name="htmlView"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Demostrate Urls
#     - test1
#     - itemDetail/<int:id>
#     - test2/<int:orderId> //Check Detail about Items
#