from django.core import serializers

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt


from weasyprint import HTML, CSS
from xhtml2pdf import pisa
from django.template.loader import get_template, render_to_string
from django.conf import settings
import tempfile

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
    print(order)
    return render(request, 'index.html', {
        "toolbar": True,
        "putPlus": True,
        "active": "home",
        "data": order,
        "heading": "Recent Files",
    })

#####################################################
################# Store Functions  #################
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
        # new_category.save()

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

        print("After Category :- ", update_category)
        # update_category.save()

    return redirect('inventory:category')


def deleteCategory(request):
    """
        Delete Category Data to Database
        input :- Accept only Category Id
        output : Redirect to list of Category
    """
    if request.method == "POST":
        print("Delete Post For Category Method")
        print("Data :", request.POST.get("deleteElementId"))  # retrieve StoreId From Submitted Form
        deleteCategory = models.Category.objects.get(id=request.POST.get("deleteElementId"))

        print("Delete Element :- ", deleteCategory)
        # print("After :- ",ingre)
        # deleteCategory.delete()

    return redirect('inventory:category')


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
        print(request.POST)
        print("data", request.POST.get("categoryId"))
        print("data", request.POST.get("name"))
        ingre = models.IngredientIndividual(name=request.POST.get("name"),category_id=request.POST.get("categoryId"))
        print("New Ingredient")
        ingre.save()
        if request.POST.get("json") == "1":
            print("Return JSON")
            return JsonResponse({
                "status" : 200,
                "newIngredientId":ingre.id
            })
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
        ingre.category_id = request.POST.get("categoryId")
        print("category :- ")
        print(ingre.category)

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


def newItems(request):
    """
        Add New Item to Database
        input :- Takes Series for form data named as ingredientId{i} and value{i} with addidtional argument of
        new item name
    """
    if request.method == "POST":
        print("Submitted Data")
        print(request.POST)

        itemId = request.POST.get("ItemId")
        print("itemId ", itemId)

        tempList = []

        # Get Item if it's Exist else create New
        if itemId == "":
            # New Item Created
            Item = models.ItemIndividual(name=request.POST.get("name"), type_id=request.POST.get("type"))
            Item.save()
        else:
            # update Item Fetch
            print(itemId)
            Item = models.ItemIndividual.objects.get(id=itemId)
            Item.name = request.POST.get("name")
            Item.type_id = request.POST.get("type")
            Item.save()
            print(Item)
            tempList = list(models.Items.objects.filter(itemId=Item))
            print("Before Deleting")
            print(tempList)
            print(len(tempList))


        for key, value in request.POST.items():
            # if "ingredientId" in key:
            #     print("New Item Entry :- ")
            #     newItemEntry = models.Items(itemId=Item, ingredientId_id=value)
            #     print(newItemEntry)

            if "ingredientId" in key:
                try:
                    tempIngredient = models.Items.objects.get(itemId=Item,ingredientId_id=value)
                    if tempIngredient in tempList:
                        # print("Ingredient Found")
                        tempList.remove(tempIngredient)
                except:
                    print("New Item Entry :- ")
                    tempIngredient = models.Items(itemId=Item,ingredientId_id=value)
                    # print("update Item Entry :- ")
                    print(tempIngredient)
                    tempIngredient.save()

        print("After Deleting")
        print(tempList)
        print(len(tempList))

        # Ingredient Deleted From Items
        for i in tempList:
            print("Delete items")
            print(i)
            i.delete()

    else:
        print(request.GET)
    return redirect('inventory:items')

# No Longer Need of this funtionn it was added with New ingredient from
def updateItems(request):
    """
        Update Item Data
        input :- accept same data as new items Just addition about item_id which need to update
    """
    if request.method == "POST":
        itemId = request.POST.get("ItemId")
        updateItem = models.ItemIndividual.objects.get(id=itemId)

        tempList = list(models.Items.objects.filter(itemId=updateItem))
        print("Before Deleting")
        print(tempList)
        print(len(tempList))


        for key, value in request.POST.items():
            if "ingredientId" in key:
                try:
                    tempIngredient = models.Items.objects.get(itemId=updateItem,ingredientId_id=value)
                    if tempIngredient in tempList:
                        # print("Ingredient Found")
                        tempList.remove(tempIngredient)
                except:
                    # print("Ingredient Does Not Exist")
                    tempIngredient = models.Items(itemId=updateItem,ingredientId_id=value)
                    # print("update Item Entry :- ")
                    # print(tempIngredient)
                    # tempIngredient.save()

        print("After Deleting")
        print(tempList)
        print(len(tempList))

        # Ingredient Deleted From Items
        for i in tempList:
            print(i)

    return redirect('inventory:items')


def deleteItems(request):
    """
        Function To delete Items in Single click
        input : Thought fromItem id
    """
    if request.method == "POST":
        itemIndividual = models.ItemIndividual.objects.get(id=request.POST.get('itemID'))
        items = models.Items.objects.filter(itemId=itemIndividual)
        print("items Name :- ")
        print(itemIndividual)
        print("Item's Ingredients ")
        for i in items:
            print(items)
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
    temp = getOrderDetail(OrderID)
    itemList = models.ItemIndividual.objects.all()
    print("Order Details")
    print(temp)
    return render(request, "order.html", {
        # "toolbar": True,
        "putPlus": True,
        "ItemList": itemList,
        "active": "order",
        "data": temp,
        # "mapData": mapObj,
        "queryItem": "order_one",
        "heading": "Order",
    })

# No longer Needed This Functions
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
        print(request.POST)
        if request.POST.get("orderID") == "":
            order = models.OrderIndividual()
        else:
            orderId = request.POST.get("orderID")
            order = models.OrderIndividual.objects.get(id=orderId)
            temp  = getOrderDetail(orderId)

        tempaddress = request.POST.get("address")
        print("Address :- ",tempaddress.strip())
        order.name = request.POST.get("name")
        order.numberOfPerson = request.POST.get("numPerson")
        order.email = request.POST.get("eamil")
        order.mobileNumber = request.POST.get("mobileNo")
        order.address = tempaddress.strip()
        order.deliveryDate = request.POST.get("dataTime")
        order.save()

        print("Order ")
        print(order)
    else:
        # // New Order Blank Form
        return render(request, 'orderNew.html', {
            "active": "order",
            "heading": "Create",
        })

    return render(request, 'orderAddItems.html', {
        "ItemList": itemList,
        "orderFor": order.name,
        "orderID": order.id,
        "data": temp,
        "active": "order",
        "queryItem": "order_one",
    })


def orderAddItems(request):

    print("From data")
    print(request.POST)
    print("Order Items")
    orderId = request.POST.get("orderID")

    temp = list(models.Order.objects.filter(orderId_id=orderId))
    print("Temp List")
    print(temp)

    for k,v in request.POST.items():
        if "itemID" in k:
            try:
                tempItem = models.Order.objects.get(orderId_id=orderId,orderItem_id=v,deletedAt=None)
                print("Object Found")
                print(tempItem)
                # if tempItem.deletedAt != None:
                #     tempItem.deletedAt = None
                #     tempItem.save()
                # tempItem.deletedAt = datetime.now()
                temp.remove(tempItem)
            except:
                tempItem = models.Order(orderId_id=orderId,orderItem_id=v)
                tempItem.save()
                print("Except Block")
                print(v)
                # pass

    print("New Added Items")
    for i in temp:
        print(i)
        i.deletedAt = datetime.now()
        i.save()

    return redirect('inventory:orderDetail', orderId)


#  No longer Needed
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


def orderPrint(request, orderId):
    print("Order Id ", orderId)
    storeOrder, storeList = getPrintData(orderId)
    print(storeOrder)
    return render(request, "pdf/pdfPresentetor.html", {
        "orderName": models.OrderIndividual.objects.get(id=orderId).name,
        "storeList": storeList,
        "orderId" : orderId,
        "active" : "order",
    })


def orderPrintData(request, orderId, dataType):

    mapObj = {
        "1": "Dairy Product",
        "2": "Vegetable",
        "3": "Exotic",
        "4": "kariyana",
        "5": "other",
    }
    print("Main")
    orderDetail = models.OrderIndividual.objects.get(id=orderId)

    d = orderDetail.deliveryDate.strftime("%d/%m/%Y")
    tt1 = orderDetail.deliveryDate.strftime("%H")
    print("Timimg")
    if int(tt1) < 15:
        tt1 = True
        print("Morning")
    else:
        tt1 = False
        print("Evening")

    if dataType == "main":
            (data, storeList) = getPrintData(orderId)
            tempOredrData = models.Order.objects.filter(orderId_id=orderId)
            orderData = list()
            print(tempOredrData)
            print("Data :- ")
            print(data)


            return render(request, 'pdf/pdf3.html',{
                "msg" : "main Method",
                "orderDetail": {
                    "id":orderDetail.id,
                    "name":orderDetail.name,
                    "address":orderDetail.address,
                    "date": orderDetail.deliveryDate,
                    "mo_number":orderDetail.mobileNumber,
                    "numberOfPerson":orderDetail.numberOfPerson
                },
                "orderdata": data,
                "date": d,
                "time": tt1,
                "category": "main",
                "jsonData" : json.dumps(data),
            })

    if dataType == "client":

        tempData = models.Order.objects.filter(orderId_id=orderId)
        temp = models.Type.objects.all()
        data = {}
        for i in temp:
            data[i.type] = list()

        for i in tempData:
            data[i.orderItem.type.type].append(i.orderItem.name)

        print("Data :- ")
        print(data)

        return render(request, 'pdf/pdf1.html', {
            "msg": "main Method",
            "orderDetail": orderDetail,
            "orderdata": data,
            "time": tt1,
            "date": orderDetail.deliveryDate,
            "category": "main",
            "jsonData": json.dumps(data),
        })

    print(orderId)
    print("Main :- ")
    print(dataType)
    (data, storeList) = getPrintData(orderId, dataType)

    print("OrderId ")
    print(dataType)
    print(mapObj[dataType])

    d = orderDetail.deliveryDate.strftime("%d/%m/%Y")
    tt1 = orderDetail.deliveryDate.strftime("%H")
    print("Timimg")
    if int(tt1) < 15:
        tt1 = True
        print("Morning")
    else:
        tt1 = False
        print("Evening")

    return render(request, "pdf/pdf3.html", {
        # "data":data,
        "orderdata": data,
        "date": d,
        "time" : tt1,
        "category": mapObj[dataType],
        "jsonData": json.dumps(data),
    })


# Function to Experiment with PDF Generation
def pdfGenration1(request):
    data = models.IngredientIndividual.objects.all()

    template_path = 'pdf/Demo.html'
    context = {'data': data}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # code for download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # code from Display
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = render_to_string(template_path,context=context)
    print(template)
    html = HTML(string=template)
    from weasyprint.text.fonts import FontConfiguration

    font_config = FontConfiguration()

    # html.write_pdf(settings.MEDIA_ROOT+"/pdf_documents/demo1.pdf", font_config=font_config)
    result = html.write_pdf()

    from django_weasyprint import WeasyTemplateResponse
    # create a pdf
    # pisa_status = pisa.CreatePDF(io.BytesIO(html.encoding('utf-8')),
    #     dest=response,encoding="binary")

    # if error then show some funy view
    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')

    # response = HttpResponse(content_type='application/pdf;')
    # response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    # response['Content-Transfer-Encoding'] = 'binary'
    # # response["body"] = result
    # with tempfile.NamedTemporaryFile(delete=True) as output:
    #     output.write(result)
    #     output.flush()
    #     output = open(output.name, 'r')
    #     response.write(output.read())
    print("What id Return")
    print(WeasyTemplateResponse(request,html.write_pdf()))
    res = {
        "msg" : "Hello"
    }
    return JsonResponse(res)


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
            print("Item One Called")
            print(temp)

            data["fields"] = dict()
            data["fields"]["ItemName"] = models.ItemIndividual.objects.get(id=data_id).name
            temp100 = models.ItemIndividual.objects.get(id=data_id).type

            if temp100 == None or temp == "":
                data["fields"]["type"] = 0
            else:
                data["fields"]["type"] = temp100.id

            data["fields"]["ingredient"] = list()
            print("Return Json : ", data)

            if len(temp) > 0:
                for i in temp:
                    print(i.ingredientId.id)
                    print(models.IngredientIndividual.objects.get(id=i.ingredientId.id))
                    key = models.IngredientIndividual.objects.get(id=i.ingredientId.id)
                    data["fields"]["ingredient"].append({i.ingredientId.id : key.name})
                # res = serializers.serialize("json", l)
            res = l

            print(res)
        elif data == "category_one":
            temp = models.Category.objects.filter(id=data_id)
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

    print(OrderID)
    temp = dict()
    fields = list()
    items = list()
    order = models.OrderIndividual.objects.get(id=OrderID)
    orderItems = models.Order.objects.filter(orderId=OrderID,deletedAt=None)
    print(orderItems)
    lastName = ""
    for i in orderItems:
        items = []
        t1 = models.Items.objects.filter(itemId_id=i.orderItem.id)
        for j in t1:
            items.append({
                "id": j.ingredientId.id,
                "name": j.ingredientId.name
            })
        fields.append({
            "id" : i.orderItem.id,
            "name": i.orderItem.name,
            "ingredients": items
        })

    print("fiedls :- ", fields)
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
def getPrintData(orderId,storeId=-1):
    storeList = []
    storeOrder = list()
    storeOrderList = list()
    categoryList = []
    category = models.Category.objects.all()
    for i in category:
        categoryList.append({
            "id" : i.id,
            "name" : i.name,
        })
    tempOrderData = models.Order.objects.filter(orderId_id=orderId,deletedAt=None)
    count = -1
    print("Print Data Function")
    print("Category :- ")
    print(category)
    print("Order Data :- ")
    print(tempOrderData)
    ingredientList = []
    orderList = []
    count = 1
    if storeId == -1:
        for i in tempOrderData:
            ingredientList = []
            tempItem = models.Items.objects.filter(itemId_id=i.orderItem_id)
            print("Order Item ")
            print(tempItem)
            for j in tempItem:
                ingredientList.append(j.ingredientId.name)
            orderList.append({
                "number": count,
                "ItemName" : i.orderItem.name,
                "ingredient": ingredientList,
            })
            count = count +1
    else:
        for i in tempOrderData:
            tempItem = models.Items.objects.filter(itemId_id=i.orderItem_id,ingredientId__category_id=storeId)
            if len(tempItem) != 0:
                ingredientList = []
                for j in tempItem:
                    ingredientList.append(j.ingredientId.name)
                orderList.append({
                    "number": count,
                    "ItemName" : i.orderItem.name,
                    "ingredient": ingredientList,
                })
                count = count +1
    # if storeId == -1:
    #     for i in tempOrderData:
    #         t1 = i.itemId.ingredientId.orderAt
    #         if t1 not in storeList:
    #             storeList.append(t1)
    #             storeOrder.append(
    #                 {
    #                     "id": t1.id,
    #                     "name": t1.name,
    #                     "data": storeOrderList
    #                 }
    #             )
    #             count = count + 1
    #         t2 = {
    #             "name": i.itemId.ingredientId.name,
    #             "value": i.quantity,
    #         }
    #         print(storeOrder[count]["data"].append(t2))
    #         print(t1.name)
    #         print(i.quantity)
    # else:
    #     for i in tempOrderData:
    #         t1 = i.itemId.ingredientId.orderAt
    #         if t1.id == int(storeId):
    #             print("if Condition")
    #             print(str(i.itemId.ingredientId.name).encode('utf-8').decode())
    #             storeOrder.append({
    #                 "name": str(i.itemId.ingredientId.name).encode('utf-8').decode(),
    #                 "value": i.quantity,
    #             })


    return orderList,categoryList