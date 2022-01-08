from django.core import serializers

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt

from xhtml2pdf import pisa
from django.template.loader import get_template

import encodings
from . import models
import json
import io

# Create your views here.


# Main Functions that render template

@cache_control(max_age=3600)
def index(request):
    """
        Display Recent Orders list
    """
    order = models.OrderIndividual.objects.all()
    print(order)
    return render(request, 'index.html', {
        "toolbar": True,
        "putPlus": True,
        "active": "home",
        "data": order,
        "heading": "Recent Files",
    })


@cache_control(max_age=3600)
def ingredientHome(request):
    """
        Display list of Ingredient
    """
    ingredients = models.IngredientIndividual.objects.all()
    store = models.Store.objects.all()
    return render(request, 'ingredient.html', {
        "toolbar": True,
        "putPlus": True,
        "active": "ingredient",
        "data": ingredients,
        "Store": store,
        "queryItem": "ingredient_one",
        "heading": "Ingredients",
    })


@cache_control(max_age=3600)
def itemsHome(request):
    """
        Display List of Items
    """
    items = models.ItemIndividual.objects.all()
    ingredients = models.IngredientIndividual.objects.all()
    store = models.Store.objects.all()
    return render(request, 'items.html', {
        "toolbar": True,
        "putPlus": True,
        "active": "items",
        "data": items,
        "options": ingredients,
        "Store": store,
        "queryItem": "item_one",
        "heading": "Items",
    })


@cache_control(max_age=3600)
def storeHome(request):
    """
        Display List of Stores
    """
    store = models.Store.objects.all()
    return render(request, 'store.html', {
        "toolbar": True,
        "putPlus": True,
        "active": "store",
        "data": store,
        "queryItem": "store_one",
        "heading": "Store",
    })


@cache_control(max_age=3600)
def orderHome(request):
    """
        display list of all order list from past
    """
    order = models.OrderIndividual.objects.all()
    print(order)
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
        Display Detail of Query order in Editing moed
        input :- Accept OrderId as it's url parameter
        output :- Render Edit order Template along with data
    """
    temp,mapObj = getOrderDetail(OrderID)
    itemList = models.ItemIndividual.objects.all()
    print(temp)
    return render(request, "order.html", {
        # "toolbar": True,
        "putPlus": True,
        "ItemList": itemList,
        "active": "order",
        "data": temp,
        "mapData": mapObj,
        "queryItem": "order_one",
        "heading": "Order",
    })

def orderNewTemplate(request):
    return render(request, 'orderNew.html',{
        "active": "order",
        "heading": "Create",
    })

def orderEditTemplate(request,id):
    order = models.OrderIndividual.objects.get(id=id)
    return render(request, 'orderNew.html', {
        "data":order,
        "active": "order",
        "orderID": id,
        "heading": "Edit",
    })

@csrf_exempt
def orderNewCreate(request):
    """
        this Funciton do two thing edit Order And Create New Order
        this Logic depend on it's input parameter
        if orderID != "" then edite
    """
    itemList = models.ItemIndividual.objects.all()
    temp = dict()
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("orderID") == "":
            order = models.OrderIndividual()
        else:
            orderId = request.POST.get("orderID")
            order = models.OrderIndividual.objects.get(id=orderId)
            temp , mapObj = getOrderDetail(orderId)

        tempaddress = request.POST.get("address")
        print("Address :- ",tempaddress.strip())
        order.name = request.POST.get("name")
        order.numberOfPerson = request.POST.get("numPerson")
        order.email = request.POST.get("eamil")
        order.mobileNumber = request.POST.get("mobileNo")
        order.address = tempaddress.strip()
        order.deliveredAt = request.POST.get("dataTime")
        order.save()

        print("Order ")
        print(order)
    else:
        return redirect("inventory:order")

    return render(request, 'orderAddItems.html', {
        "ItemList": itemList,
        "orderFor": order.name,
        "orderID": order.id,
        "data": temp,
        "active": "order",
        "queryItem": "order_one",
    })


@csrf_exempt
def orderAddItems(request):

    data = json.loads(request.body)
    print(data)
    print("Order Items")
    orderId = data["orderID"]
    itemId = data["itemID"]
    t = models.Order.objects.filter(orderId_id=orderId,itemId__itemId_id=itemId)
    if len(t) == 0:
        print("New Items")
        for key,value in data.items():
            if key != "orderID" and key != "itemID":
                temp = models.Order()
                print("Key :- ",key,"\nValue :",value)
                temp.orderId_id = orderId
                tempItem = models.Items.objects.get(itemId_id=itemId,ingredientId_id=key)
                print("Selected ITem :- ",tempItem)
                temp.itemId = tempItem
                temp.quantity = value
                print(temp)
                temp.save()
    else:
        print("Edit Items")
        for key,value in data.items():
            if key != "orderID" and key != "itemID":
                tempItem = models.Items.objects.get(itemId_id=itemId,ingredientId_id=key)
                temp = models.Order.objects.get(orderId_id=orderId,itemId=tempItem)
                print("Key :- ",key,"\nValue :",value)
                print("Selected ITem :- ",tempItem)
                temp.quantity = value
                print(temp)
                temp.save()

    return JsonResponse({
        "msg": "Data received",
        "status": 200,
        "id" : temp.id,
    })


@csrf_exempt
def orderDeleteItem(request):
    res = {}
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get("orderId"))
        print(request.POST.get("itemId"))
        order = models.Order.objects.filter(orderId_id=request.POST.get("orderId"),itemId__itemId_id=request.POST.get("itemId"))
        print("Order Data")
        print(order)
        for i in order:
            print(i)
            i.delete()
        res["msg"] = "data Received"
    else:
        return redirect('inventory:order')

    return JsonResponse(res)



def orderPrint(request,orderId):
    print("Order Id ", orderId)
    # res = dict()
    # storeList = []
    # storeOrder = list()
    # storeOrderList = list()
    # tempOrderData = models.Order.objects.filter(orderId_id=orderId)
    # count = -1
    # for i in tempOrderData:
    #     t1 = i.itemId.ingredientId.orderAt
    #     if t1 not in storeList:
    #         storeList.append(t1)
    #         storeOrder.append(
    #             {
    #                 "id": t1.id,
    #                 "name": t1.name,
    #                 "data": storeOrderList
    #             }
    #         )
    #         count = count +1
    #     t2 = {
    #         "name": i.itemId.ingredientId.name,
    #         "value": i.quantity,
    #     }
    #     print(storeOrder[count]["data"].append(t2))
    #     print(t1.name)
    #     print(i.quantity)
    #
    storeOrder, storeList = getPrintData(orderId)
    print(storeOrder)
    return render(request, "pdf/pdfPresentetor.html", {
        "orderName": models.OrderIndividual.objects.get(id=orderId).name,
        "storeList": storeList,
        "orderId" : orderId
    })



def orderPrintData(request, orderId, dataType):

    if dataType != "main":
        print(orderId)
        print(dataType)
        storeDetails = models.Store.objects.get(id=dataType)
        (data, storeList) = getPrintData(orderId,dataType)

        return render(request, "pdf/pdf1.html", {
            "data":data,
            "storeData": storeDetails,
            "date" : models.OrderIndividual.objects.get(id=orderId).deliveredAt
        })


    orderDetail = models.OrderIndividual.objects.get(id=orderId)
    tempOredrData = models.Order.objects.filter(orderId_id=orderId)
    orderData = list()
    print(tempOredrData)
    tempDict = {}
    itemIdList = []
    for i in tempOredrData:
        if i.itemId.itemId not in itemIdList:
            itemIdList.append(i.itemId.itemId)

        tempDict[i.itemId.itemId.id] = tempDict.get(i.itemId.itemId.id, [])
        tempDict[i.itemId.itemId.id].append({
            "name":i.itemId.ingredientId.name,
            "value" : i.quantity
        })
    for i in itemIdList:
        orderData.append({
            "itemId": i.id,
            "ItemName": i.name,
            "ItemData" : tempDict[i.id]
        })
    print("Item ID List ")
    print(itemIdList)
    print("Items Detail List")
    print(tempDict)
    print("Order data List")
    print(orderData)

    return render(request, 'pdf/pdf2.html',{
        "msg" : "main Method",
        "orderDetail": {
            "id":orderDetail.id,
            "name":orderDetail.name,
            "address":orderDetail.address,
            "date": orderDetail.deliveredAt,
            "mo_number":orderDetail.mobileNumber,
            "numberOfPerson":orderDetail.numberOfPerson
        },
        "orderdata": orderData
    })


#####################################################
############ Ingredient Functions  #################
#####################################################

def newIngredient(request):
    """
        Add new IIngredient Data to Database
        input :- Accept all Necessary data for new Ingredient from User through Form
        output : Redirect to list of Ingredient
    """
    if request.method == "POST":
        print("data", request.POST.get("storeId"))
        print("data", request.POST.get("name"))
        ingre = models.IngredientIndividual(name=request.POST.get("name"), orderAt_id=request.POST.get("storeId"))
        print(ingre)
        ingre.save()
    return redirect('inventory:ingredient')


def updateIngredient(request):
    """
        Update IIngredient Data to Database
        input :- Accept all Necessary data from User through Form along with Ingredient ID
        output : Redirect to list of Ingredient
    """
    if request.method == "POST":
        print("Update Post Method")
        print("updateElementID", request.POST.get("updateElementID"))
        print("data", request.POST.get("name"))
        ingre = models.IngredientIndividual.objects.get(id=request.POST.get("updateElementID"))
        print("Before :- ", ingre)
        ingre.name = request.POST.get("name")
        store = models.Store.objects.get(id=request.POST.get("storeId"))
        print("Store :- ", store)
        ingre.orderAt = store

        print("After :- ", ingre)
        ingre.save()
    return redirect('inventory:ingredient')


def deleteIngredient(request):
    """
        Delete Ingredient from database
        input :- Accept Ingredient Id from User
        output :- Redirect To Ingredient List
    """
    if request.method == "POST":
        print("Delete Post Method")
        print("Data :", request.POST.get("deleteElementId"))
        ingre = models.IngredientIndividual.objects.get(id=request.POST.get("deleteElementId"))

        print("Before :- ", ingre)
        ingre.delete()

    return redirect('inventory:ingredient')


#####################################################
################# Store Functions  #################
#####################################################

def newStore(request):
    """
        Add new Store DAta to Database
        input :- Accept all Necessary data from User through Form
        output : Redirect to list of Store
    """
    print("New Store")
    if request.method == "POST":
        new_store = models.Store()
        new_store.name = request.POST.get("name")
        new_store.address = request.POST.get("address")
        new_store.emailAddress = request.POST.get("emailAddress")
        new_store.mobileNumber = request.POST.get("mobileNumber")
        print("After Store :- ", new_store)
        new_store.save()

    return redirect('inventory:store')


def updateStore(request):
    """
        Update Store Data to Database
        input : Accept all Necessary data from User through Form along with Store Id
        output : Redirect to list of Store
    """
    print("update Store")
    if request.method == "POST":
        update_store = models.Store.objects.get(id=request.POST.get("updateElementID"))
        # retrieve store updated data from user
        update_store.name = request.POST.get("name")
        update_store.address = request.POST.get("address")
        update_store.emailAddress = request.POST.get("emailAddress")
        update_store.mobileNumber = request.POST.get("mobileNumber")
        print("After Store :- ", update_store)
        update_store.save()

    return redirect('inventory:store')


def deleteStore(request):
    """
        Delete Store Data to Database
        input :- Accept only Store Id
        output : Redirect to list of Store
    """
    if request.method == "POST":
        print("Delete Post For Store Method")
        print("Data :", request.POST.get("deleteElementId"))  # retrieve StoreId From Submitted Form
        deleteStore = models.Store.objects.get(id=request.POST.get("deleteElementId"))

        print("Delete Element :- ", deleteStore)
        # print("After :- ",ingre)
        deleteStore.delete()

    return redirect('inventory:store')


#####################################################
############ Items Functions  #################
#####################################################

def newItems(request):
    """
        Add New Item to Database
        input :- Takes Series for form data named as ingredientId{i} and value{i} with addidtional argument of
        new item name
    """
    if request.method == "POST":
        temp = 0
        tempIngredient = None
        newItem = models.ItemIndividual(name=request.POST.get("name"))
        newItem.save()

        for key, value in request.POST.items():
            if "ingredientId" in key:
                temp = 1
                tempIngredient = models.IngredientIndividual.objects.get(id=value)

            elif temp == 1:
                newItemEntry = models.Items(itemId=newItem, ingredientId=tempIngredient, defaultValue=value)
                print("New Item Entry :- ")
                print(newItemEntry)
                newItemEntry.save()
                temp = 0
    else:
        print(request.GET)
    return redirect('inventory:items')


def updateItems(request):
    """
        Update Item Data
        input :- accept same data as new items Just addition about item_id which need to update
    """
    if request.method == "POST":
        itemId = request.POST.get("ItemId");
        updateItem = models.ItemIndividual.objects.get(id=itemId)

        temp = models.Items.objects.filter(itemId=updateItem)
        for i in temp:
            print(i)
            # i.delete()

        for key, value in request.POST.items():
            if "ingredientId" in key:
                temp = 1
                try:
                    tempIngredient = models.Items.objects.get(itemId=updateItem,ingredientId_id=value)
                except:
                    print("User Does Not Exesist")
                    tempIngredient = models.Items(itemId=updateItem,ingredientId_id=value)


            elif temp == 1:
                tempIngredient.defaultValue = value
                print("update Item Entry :- ")
                print(tempIngredient)
                tempIngredient.save()
                temp = 0

    return redirect('inventory:items')


def deleteItems(request):
    """
        Function To delete Items in Single click
        input : Thought fromItem id
    """
    if request.method == "POST":
        itemIndividual = models.ItemIndividual.objects.get(id=request.POST.get('itemID'))
        items = models.Items.objects.filter(itemId=itemIndividual)
        for i in items:
            i.delete()
        itemIndividual.delete()
    return redirect('inventory:items')




# Fountain to Experiment with PDF Generation
def pdfGenration1(request):
    data = models.IngredientIndividual.objects.all()

    template_path = 'pdf/pdf1.html'
    context = {'data': data}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # code for download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # code from Display
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(io.BytesIO(html.encoding('utf-8')),
        dest=response,encoding="binary")

    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def pdfHtmlView(request):
    data = models.IngredientIndividual.objects.all()

    template = get_template('pdf/pdf1.html')
    html = template.render({"data": data})

    header = {
        "content_type": 'text/html',
        "Content-Disposition": 'attachment; filename="report.pdf"'
    }
    response = HttpResponse(html, headers=header)
    # print(request)
    # request['Content-Disposition'] = 'attachment; filename="report.pdf"'
    print(response)

    # return response
    return render(request, 'pdf/pdf1.html', {
        "data": data
    })


def getDetail(request):
    if request.method == "GET":
        data = request.GET.get("queryItem")
        data_id = request.GET.get("queryId")
        if data == "ingredient_one":
            temp = models.IngredientIndividual.objects.filter(id=data_id)
            res = serializers.serialize("json", temp)
            print(res)
        elif data == "item_one":
            l = list()
            data = dict()
            l.append(data)
            temp = list(models.Items.objects.filter(itemId=data_id))
            print(temp)
            if len(temp) > 0:
                data["fields"] = dict()
                data["fields"]["ItemName"] = models.ItemIndividual.objects.get(id=temp[0].itemId.id).name
                data["fields"]["ingredient"] = list()
                print("Return Json : ", data)
                for i in temp:
                    print(i.ingredientId.id)
                    print(models.IngredientIndividual.objects.get(id=i.ingredientId.id))
                    key = models.IngredientIndividual.objects.get(id=i.ingredientId.id)
                    data["fields"]["ingredient"].append({"id": i.ingredientId.id, key.name: i.defaultValue})
                # res = serializers.serialize("json", l)
            res = l
            print(res)
        elif data == "store_one":
            temp = models.Store.objects.filter(id=data_id)
            res = serializers.serialize("json", temp)
            print(res)
        elif data == 'order_one':
            temp = dict()
            fields = dict()
            print("data : ", data)
            items = list()
            ingredients = list()
            order = models.OrderIndividual.objects.get(id=data_id)
            orderItems = models.Order.objects.filter(orderId=data_id)
            print(orderItems)
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
            print(res)
        else:
            res = {
                "message": "None Empty Error",
                "data": ""
            }
    else:
        return redirect("inventory:ingredient")

    return JsonResponse(res, safe=False)


def getAllDetail(request):
    if request.method == "GET":
        data = request.GET.get("queryItem")
        data_id = request.GET.get("queryId")
        if data == "ingredient_all":
            temp = models.IngredientIndividual.objects.all()
            res = serializers.serialize("json", temp)
            print(res)
        elif data == "store_all":
            temp = models.Store.objects.all()
            res = serializers.serialize("json", temp)
            print(res)
        else:
            res = {
                "message": "None Empty Error",
                "data": ""
            }
    else:
        return redirect("inventory:ingredient")

    return JsonResponse(res, safe=False)


def test1(request):
    if request.method == "POST":
        print(request.POST)
    else:
        print(request.GET)
    return render(request, "form.html")


def getOrderDetail(OrderID):

    mapObject = {}
    t1 = models.IngredientIndividual.objects.all()
    for i in t1:
        mapObject[i.id] = i.name
    print("Map Object :- ")
    print(mapObject)
    print(OrderID)
    temp = dict()
    fields = dict()
    items = list()
    ingredients = list()
    order = models.OrderIndividual.objects.get(id=OrderID)
    orderItems = models.Order.objects.filter(orderId=OrderID)
    print(orderItems)
    lastName = ""
    if len(orderItems) > 1:
        for i in orderItems:
            if i.itemId.itemId.id not in items:
                print(i)
                items.append(i.itemId.itemId.id)
                if len(items) > 1:
                    fields[items[-2]] = {
                        "name": lastName,
                        "ingredient": ingredients
                    }
                    ingredients = []
            ingredients.append(
                {
                    "id": models.IngredientIndividual.objects.get(id=i.itemId.ingredientId.id).id,
                    "name": models.IngredientIndividual.objects.get(id=i.itemId.ingredientId.id).name,
                    "quantity": i.quantity,
                }
            )
            lastName = i.itemId.itemId.name
        fields[items[-1]] = {
                        "name": lastName,
                        "ingredient": ingredients
                    }
    print("fiedls :- ", fields)
    temp["orderId"] = order.id
    temp["orderName"] = order.name
    temp["mobileNumber"] = order.mobileNumber
    temp["numberOfPerson"] = order.numberOfPerson
    temp["address"] = order.address
    temp["email"] = order.email
    temp["fields"] = fields
    temp["deliverDate"] = order.deliveredAt
    temp["createdAt"] = order.createdAt

    return temp, mapObject


# //Suportive Funtions
def getPrintData(orderId,storeId=-1):
    storeList = []
    storeOrder = list()
    storeOrderList = list()
    tempOrderData = models.Order.objects.filter(orderId_id=orderId)
    count = -1
    if storeId == -1:
        for i in tempOrderData:
            t1 = i.itemId.ingredientId.orderAt
            if t1 not in storeList:
                storeList.append(t1)
                storeOrder.append(
                    {
                        "id": t1.id,
                        "name": t1.name,
                        "data": storeOrderList
                    }
                )
                count = count + 1
            t2 = {
                "name": i.itemId.ingredientId.name,
                "value": i.quantity,
            }
            print(storeOrder[count]["data"].append(t2))
            print(t1.name)
            print(i.quantity)
    else:
        for i in tempOrderData:
            t1 = i.itemId.ingredientId.orderAt
            if t1.id == int(storeId):
                print("if Condition")
                print(str(i.itemId.ingredientId.name).encode('utf-8').decode())
                storeOrder.append({
                    "name": str(i.itemId.ingredientId.name).encode('utf-8').decode(),
                    "value": i.quantity,
                })


    return storeOrder,storeList