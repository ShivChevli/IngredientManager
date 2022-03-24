from django.core import serializers

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt

from weasyprint import HTML, CSS

from django.template.loader import get_template, render_to_string
from django.conf import settings
import tempfile

from django_weasyprint import WeasyTemplateResponse

import encodings
from . import models
from datetime import datetime
import json
import io


####################################################
# Try WeasyPrint Library For Generating PDF
####################################################

# Create your views here.


# Main Functions that render template

@cache_control(max_age=3600)
def index(request):
    """
        Display Recent Orders list
    """
    order = models.OrderIndividual.objects.filter(deliveryDate__gte=datetime.now()).order_by("deliveryDate")
    return render(request, 'index.html', {
        "toolbar": True,
        "putPlus": True,
        "active": "home",
        "data": order,
        "heading": "Recent Files",
    })


#####################################################
################# Category Functions  #################
#####################################################

@cache_control(max_age=3600)
def categoryHome(request):
    """
        Display List of Category
    """
    category = models.Category.objects.all()
    return render(request, 'category.html', {
        "toolbar": True,
        "putPlus": True,
        "active": "category_tab",
        "data": category,
        "queryItem": "category_one",
        "heading": "Category",
    })


def newCategory(request):
    """
        Add new Category DAta to Database
        input :- Accept all Necessary data from User through Form
        output : Redirect to list of Category
    """
    print("New Category")
    if request.method == "POST":
        new_category = models.Category()
        new_category.name = request.POST.get("name")
        print("After Category :- ", new_category)
        new_category.save()

    return redirect('inventory:category')


def updateCategory(request):
    """
        Update Category Data to Database
        input :  Accept Name and  Id
        output : Redirect to list of Category
    """
    print("update Category")
    if request.method == "POST":
        update_category = models.Category.objects.get(id=request.POST.get("updateElementID"))
        # retrieve Category updated data from user
        update_category.name = request.POST.get("name")

        # print("After Category :- ", update_category)
        update_category.save()

    return redirect('inventory:category')


# not Access using UI We have to give give direct URL
def deleteCategory(request):
    """
        Delete Category Data to Database
        input :- Accept only Category Id
        output : Redirect to list of Category
    """
    msg = "Invalid Category ID"
    if request.method == "GET":
        # print("Delete Category Method")
        deleteCategory = models.Category.objects.get(id=request.GET.get("deleteElementId"))

        print("Delete Element :- ", deleteCategory)
        deleteCategory.delete()
        msg = f"Category {deleteCategory.name} with Id {deleteCategory.id} is Deleted Successfully"

    return JsonResponse({
        "Status": 200,
        "Message": msg,
    })


#####################################################
############ Ingredient Functions  #################
#####################################################

@cache_control(max_age=3600)
def ingredientHome(request):
    """
        Display list of Ingredient
    """
    ingredients = models.IngredientIndividual.objects.all()
    category = models.Category.objects.all()
    return render(request, 'ingredient.html', {
        "toolbar": True,
        "putPlus": True,
        "active": "ingredient",
        "data": ingredients,
        "Category": category,
        "queryItem": "ingredient_one",
        "heading": "Ingredients",
    })


@csrf_exempt
def newIngredient(request):
    """
        Add new IIngredient Data to Database
        input :- Accept all Necessary data for new Ingredient from User through Form
        output : Redirect to list of Ingredient
    """
    if request.method == "POST":
        ingre = models.IngredientIndividual(name=request.POST.get("name"), category_id=request.POST.get("categoryId"))
        ingre.save()
        if request.POST.get("json") == "1":
            return JsonResponse({
                "status": 200,
                "newIngredientId": ingre.id
            })
    return redirect('inventory:ingredient')


def updateIngredient(request):
    """
        Update IIngredient Data to Database
        input :- Accept all Necessary data from User through Form along with Ingredient ID
        output : Redirect to list of Ingredient
    """
    if request.method == "POST":
        ingre = models.IngredientIndividual.objects.get(id=request.POST.get("updateElementID"))
        ingre.name = request.POST.get("name")
        ingre.category_id = request.POST.get("categoryId")
        ingre.save()
    return redirect('inventory:ingredient')


def deleteIngredient(request):
    """
        Delete Ingredient from database
        input :- Accept Ingredient Id from User
        output :- Redirect To Ingredient List
    """
    msg = "Invalid Ingredient ID"
    if request.method == "GET":
        print("Delete Ingredient Method")
        print("Data :", request.GET.get("deleteElementId"))
        ingre = models.IngredientIndividual.objects.get(id=request.GET.get("deleteElementId"))

        msg = f"Ingredient {ingre.name} with Id {ingre.id} is Deleted Successfully"
        ingre.delete()

    # return redirect('inventory:ingredient')
    return JsonResponse({
        "Status": 200,
        "Message": msg,
    })


#####################################################
############ Items Functions  #################
#####################################################


@cache_control(max_age=3600)
def itemsHome(request):
    """
        Display List of Items
    """
    items = models.ItemIndividual.objects.all()
    ingredients = models.IngredientIndividual.objects.all()
    category = models.Category.objects.all()
    return render(request, 'items.html', {
        "toolbar": True,
        "putPlus": True,
        "active": "items",
        "data": items,
        "options": ingredients,
        "Category": category,
        "queryItem": "item_one",
        "heading": "Items",
    })


@csrf_exempt
def newItems(request):
    """
        Add New Item to Database
        input :- Takes Series for form data named as ingredientId{i} and value{i} with addidtional argument of
        new item name
    """
    if request.method == "POST":

        bjson = request.POST.get("json")
        itemId = request.POST.get("ItemId")
        tempList = []

        # Get Item if it's Exist else create New
        if itemId == "":
            # New Item Created
            Item = models.ItemIndividual(name=request.POST.get("name"), type_id=request.POST.get("type"))
            Item.save()
        else:
            # update Item Fetch
            Item = models.ItemIndividual.objects.get(id=itemId)
            Item.name = request.POST.get("name")
            Item.type_id = request.POST.get("type")
            Item.modifyAt = datetime.now()
            Item.save()
            tempList = list(models.Items.objects.filter(itemId=Item))

        for key, value in request.POST.items():

            if "ingredientId" in key:
                try:
                    tempIngredient = models.Items.objects.get(itemId=Item, ingredientId_id=value)
                    if tempIngredient in tempList:
                        tempList.remove(tempIngredient)
                except:
                    tempIngredient = models.Items(itemId=Item, ingredientId_id=value)
                    tempIngredient.save()

        # Ingredient Deleted From Items
        for i in tempList:
            i.delete()

        if bjson == "true":
            return JsonResponse({
                "Status": 200,
                "msg": "Data Received",
                "data": {
                    "name": Item.name,
                    "id": Item.id
                }
            })

    else:
        print("Access of New Item Using Get Method")

    return redirect('inventory:items')


def deleteItems(request):
    """
        Function To delete Items in Single click
        input : Thought fromItem id
    """
    if request.method == "POST":
        print("Item Delete Called")
        itemIndividual = models.ItemIndividual.objects.get(id=request.POST.get('itemID'))
        items = models.Items.objects.filter(itemId=itemIndividual)
        for i in items:
            i.delete()
        itemIndividual.delete()

    return redirect('inventory:items')


#####################################################
############ Order Functions  #################
#####################################################


@cache_control(max_age=3600)
def orderHome(request):
    """
        display list of all order list from past
    """
    order = models.OrderIndividual.objects.all().order_by("-createdAt")
    return render(request, 'orderList.html', {
        "toolbar": True,
        "putPlus": True,
        "active": "order",
        "data": order,
        "queryItem": "order_one",
        "heading": "Order",
    })


@cache_control(max_age=3600)
def orderDetail(request, OrderID):
    """
        Display Detail of Query order in Editing mode
        input :- Accept OrderId as it's url parameter
        output :- Render Edit order Template along with data
    """
    print(OrderID)
    temp = getOrderDetail(OrderID)
    # print(temp)
    itemList = models.ItemIndividual.objects.all()

    return render(request, "order.html", {
        # "toolbar": True,
        "putPlus": True,
        "ItemList": itemList,
        "active": "order",
        "data": temp,
        "queryItem": "order_one",
        "heading": "Order",
    })


def orderEditTemplate(request, id):
    order = models.OrderIndividual.objects.get(id=id)
    return render(request, 'orderNew.html', {
        "data": order,
        "active": "order",
        "orderID": id,
        "heading": "Edit",
    })


# Use for create New order or Update Order
def orderNewCreate(request):
    """
        this Funciton do two thing edit Order And Create New Order
        this Logic depend on it's input parameter
        if orderID != "" then edite
    """
    itemList = models.ItemIndividual.objects.all()
    temp = dict()
    if request.method == "POST":
        # Submitted From Actions
        if request.POST.get("orderID") == "":
            order = models.OrderIndividual()
        else:
            orderId = request.POST.get("orderID")
            order = models.OrderIndividual.objects.get(id=orderId)
            temp = getOrderDetail(orderId)

        tempaddress = request.POST.get("address")
        order.name = request.POST.get("name")
        order.numberOfPerson = request.POST.get("numPerson")
        order.email = request.POST.get("eamil")
        order.mobileNumber = request.POST.get("mobileNo")
        order.address = tempaddress.strip()
        order.deliveryDate = request.POST.get("dataTime")
        order.save()

    else:
        # // New Order Blank Form
        return render(request, 'orderNew.html', {
            "active": "order",
            "heading": "Create",
        })

    IngredientOption = models.IngredientIndividual.objects.all();

    return render(request, 'orderAddItems.html', {
        "ItemList": itemList,
        "orderFor": order.name,
        "orderID": order.id,
        "data": temp,
        "active": "order",
        "queryItem": "order_one",
        "options": IngredientOption,
    })


def orderAddItems(request):
    orderId = request.POST.get("orderID")
    temp = list(models.Order.objects.filter(orderId_id=orderId))

    for k, v in request.POST.items():
        if "itemID" in k:
            try:
                tempItem = models.Order.objects.get(orderId_id=orderId, orderItem_id=v, deletedAt=None)
                temp.remove(tempItem)
            except:
                tempItem = models.Order(orderId_id=orderId, orderItem_id=v)
                tempItem.save()

        for i in temp:
            i.deletedAt = datetime.now()
        i.save()

    return redirect('inventory:orderDetail', orderId)


def orderPrint(request, orderId):
    storeOrder, storeList = getPrintData(orderId)

    return render(request, "pdf/pdfPresentetor.html", {
        "orderName": models.OrderIndividual.objects.get(id=orderId).name,
        "storeList": storeList,
        "orderId": orderId,
        "active": "order",
    })


def orderPrintData(request, orderId, dataType):
    mapObj = {
        "1": "Dairy_Product",
        "2": "Vegetable",
        "3": "Exotic",
        "4": "kariyana",
        "5": "other",
    }

    orderDetail = models.OrderIndividual.objects.get(id=orderId)

    d = orderDetail.deliveryDate.strftime("%d/%m/%Y")
    tt1 = orderDetail.deliveryDate.strftime("%H")

    if int(tt1) < 15:
        tt1 = True
    else:
        tt1 = False

    if dataType == "main":
        (data, storeList) = getPrintData(orderId)

        # to Create PDF at Client Side

        # return render(request, 'pdf/pdf3.html', {
        #     "msg": "main Method",
        #     "orderDetail": {
        #         "id": orderDetail.id,
        #         "name": orderDetail.name,
        #         "address": orderDetail.address,
        #         "date": orderDetail.deliveryDate,
        #         "mo_number": orderDetail.mobileNumber,
        #         "numberOfPerson": orderDetail.numberOfPerson
        #     },
        #     "orderdata": data,
        #     "date": d,
        #     "time": tt1,
        #     "category": "main",
        #     "jsonData": json.dumps(data),
        # })

        # to Create PDF at Server Side
        context = {
            "msg": "main Method",
            "orderDetail": {
                "id": orderDetail.id,
                "name": orderDetail.name,
                "address": orderDetail.address,
                "date": orderDetail.deliveryDate,
                "mo_number": orderDetail.mobileNumber,
                "numberOfPerson": orderDetail.numberOfPerson
            },
            "orderdata": data,
            "date": d,
            "time": tt1,
            "title": "Main PDF",
            "category": "main",
            "jsonData": json.dumps(data),
        }
        return pdfGenration1(request, context)

    if dataType == "client":

        tempData = models.Order.objects.filter(orderId_id=orderId)
        temp = models.Type.objects.all()
        data = {}
        for i in temp:
            data[i.type] = list()

        for i in tempData:
            data[i.orderItem.type.type].append(i.orderItem.name)

        # Create Pdf at Client Side

        # return render(request, 'pdf/pdf1.html', {
        #     "msg": "main Method",
        #     "orderDetail": orderDetail,
        #     "orderdata": data,
        #     "time": tt1,
        #     "date": orderDetail.deliveryDate,
        #     "category": "main",
        #     "jsonData": json.dumps(data),
        # })

        # TO Create PDF at Server Side
        context = {
            "msg": "main Method",
            "orderDetail": orderDetail,
            "orderdata": data,
            "time": tt1,
            "title": "Client Pdf",
            "date": orderDetail.deliveryDate,
            "category": "main",
            "jsonData": json.dumps(data),
        }

        return pdfGenration1(request, context, True)

    (data, storeList) = getPrintData(orderId, dataType)

    # Create PDF at Client Side

    # return render(request, "pdf/pdf3.html", {
    #     "orderdata": data,
    #     "date": d,
    #     "time": tt1,
    #     "category": mapObj[dataType],
    #     "jsonData": json.dumps(data),
    # })

    # To create PDF at server side
    context = {
        "orderdata": data,
        "date": d,
        "time": tt1,
        "title": mapObj[dataType],
        "category": mapObj[dataType],
        "jsonData": json.dumps(data),
    }

    file_name = orderDetail.name + "_" + mapObj[dataType] + ".pdf"
    print(file_name)
    return pdfGenration1(request, context, file_name=file_name)


# Function to PDF Generation
def pdfGenration1(request, context, client_pdf=False, file_name="file.pdf"):
    template_path = 'pdf/Demo.html'

    # code for download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    header = {
        "content-type": 'application/pdf',
        "Content-Disposition": context["title"],
    }
    if file_name == "file.pdf":
        file_name = context["title"] + ".pdf"
        print(file_name)

    if client_pdf:
        return WeasyTemplateResponse(request=request, filename=file_name, template='pdf/Demo1.html',
                                     attachment=False,
                                     headers=header, context=context)

    return WeasyTemplateResponse(request=request, filename=file_name, template=template_path, attachment=False,
                                 headers=header, context=context)


def pdfHtmlView(request):
    data = models.IngredientIndividual.objects.all()

    template = get_template('pdf/pdf1.html')
    html = template.render({"data": data})

    header = {
        "content_type": 'text/html',
        "Content-Disposition": 'attachment; filename="report.pdf"'
    }
    response = HttpResponse(html, headers=header)

    print(response)

    # return response
    return render(request, 'pdf/pdf1.html', {
        "data": data
    })


def getDetail(request):
    """
        Function For Get Detail using API
        Input :- queryItem( Def Query Type Item),
                 {
                    # valid values of parameter queryItem
                    ingredient_one : for Get detail About Ingredient
                    item_one : for get detail about Item
                    category_one : fr get detail about Category
                    order_one : to get drtail about order
                }
                 queryId( Id of Item which user want to get detail)
    """
    if request.method == "GET":
        data = request.GET.get("queryItem")
        data_id = request.GET.get("queryId")
        if data == "ingredient_one":
            temp = models.IngredientIndividual.objects.filter(id=data_id)
            res = serializers.serialize("json", temp)
        elif data == "item_one":
            l = list()
            data = dict()
            l.append(data)
            temp = list(models.Items.objects.filter(itemId=data_id))

            data["fields"] = dict()
            data["fields"]["ItemName"] = models.ItemIndividual.objects.get(id=data_id).name
            temp100 = models.ItemIndividual.objects.get(id=data_id).type

            if temp100 == None or temp == "":
                data["fields"]["type"] = 0
            else:
                data["fields"]["type"] = temp100.id

            data["fields"]["ingredient"] = list()

            if len(temp) > 0:
                for i in temp:
                    key = models.IngredientIndividual.objects.get(id=i.ingredientId.id)
                    data["fields"]["ingredient"].append({i.ingredientId.id: key.name})
            res = l

        elif data == "category_one":
            temp = models.Category.objects.filter(id=data_id)
            res = serializers.serialize("json", temp)
        elif data == 'order_one':
            temp = dict()
            fields = dict()
            items = list()
            ingredients = list()
            order = models.OrderIndividual.objects.get(id=data_id)
            orderItems = models.Order.objects.filter(orderId=data_id)
            for i in orderItems:
                if i.itemId.itemId.name not in items:
                    items.append(i.itemId.itemId.name)
                    if len(items) > 1:
                        fields[items[-2]] = ingredients
                        ingredients = []
                ingredients.append(
                    {
                        models.IngredientIndividual.objects.get(id=i.itemId.ingredientId.id).name: i.quantity
                    }
                )
            fields[items[-1]] = ingredients
            temp["orderName"] = order.name
            temp["fields"] = fields
            temp["orderAt"] = order.deliveredAt
            temp["createdAt"] = order.createdAt
            res = list()
            res.append(temp)
        else:
            res = {
                "message": "None Empty Error",
                "data": ""
            }
    else:
        return redirect("inventory:ingredient")

    return JsonResponse(res, safe=False)


def test1(request):
    """
        This function to test New functionality about trying new Technology
    """
    if request.method == "POST":
        print(request.POST)
    else:
        print(request.GET)
    return render(request, "form.html")


def getOrderDetail(OrderID):
    print(OrderID)

    temp = dict()
    fields = list()
    order = models.OrderIndividual.objects.get(id=OrderID)
    orderItems = models.Order.objects.filter(orderId=OrderID, deletedAt=None)
    print(orderItems)
    for i in orderItems:
        items = []
        t1 = models.Items.objects.filter(itemId_id=i.orderItem.id)
        for j in t1:
            items.append({
                "id": j.ingredientId.id,
                "name": j.ingredientId.name
            })
        fields.append({
            "id": i.orderItem.id,
            "name": i.orderItem.name,
            "ingredients": items
        })

    temp["orderId"] = order.id
    temp["orderName"] = order.name
    temp["mobileNumber"] = order.mobileNumber
    temp["numberOfPerson"] = order.numberOfPerson
    temp["address"] = order.address
    temp["email"] = order.email
    temp["fields"] = fields
    temp["deliverDate"] = order.deliveryDate
    temp["createdAt"] = order.createdAt

    return temp


# //Suportive Funtions
def getPrintData(orderId, storeId=-1):
    categoryList = []
    category = models.Category.objects.all()
    for i in category:
        categoryList.append({
            "id": i.id,
            "name": i.name,
        })
    tempOrderData = models.Order.objects.filter(orderId_id=orderId, deletedAt=None)
    orderList = []
    count = 1
    if storeId == -1:
        for i in tempOrderData:
            ingredientList = []
            tempItem = models.Items.objects.filter(itemId_id=i.orderItem_id)
            for j in tempItem:
                ingredientList.append(j.ingredientId.name)
            orderList.append({
                "number": count,
                "ItemName": i.orderItem.name,
                "ingredient": ingredientList,
            })
            count = count + 1
    else:
        for i in tempOrderData:
            tempItem = models.Items.objects.filter(itemId_id=i.orderItem_id, ingredientId__category_id=storeId)
            if len(tempItem) != 0:
                ingredientList = []
                for j in tempItem:
                    ingredientList.append(j.ingredientId.name)
                orderList.append({
                    "number": count,
                    "ItemName": i.orderItem.name,
                    "ingredient": ingredientList,
                })
                count = count + 1

    return orderList, categoryList
