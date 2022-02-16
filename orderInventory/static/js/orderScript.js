var addedItemList = {};
var countItem = 0;
var addedIngredient = {};
document.addEventListener("DOMContentLoaded",()=>{

    // try{
    //     document.getElementById('editBtn').onclick = function (){
    //         document.getElementById("detail-view").style.display = 'none';
    //         document.getElementById("edit-view").style.display = 'block';
    //     }
    //
    // }
    // catch (e){
    //     console.log("Edit View Error : " + e);
    // }

    // try{
    //
    // // document.querySelectorAll(".text").forEach(p => {
    // //     p.onclick = function () {
    // //         console.log("Data Fetched ");
    // //         let getId = p.dataset.itemid;
    // //         let qI = p.dataset.queryitem;
    // //         document.getElementById("item-list-box").style.display = "none";
    // //         document.getElementById("add-item-form").style.display = "inline-block";
    // //
    // //         // if (getId != undefined){
    // //         //     fetch(`/orderInventory/detail?queryItem=${qI}&queryId=${getId}`)
    // //         //         .then(responce => responce.json())
    // //         //         .then(data => {
    // //         //             console.log("Fetch Data :- "+ data);
    // //         //             console.log("Type :"+ typeof(data));
    // //         //             console.log("Type :"+ JSON.stringify(data));
    // //         //             if ( typeof(data) == 'object'){
    // //         //                 temp = data;
    // //         //             }
    // //         //             else
    // //         //             {
    // //         //             temp = JSON.parse(data);
    // //         //             }
    // //         //             console.log("Temp :- "+temp);
    // //         //             temp.forEach(data => {
    // //         //                 document.getElementById("itemID").defaultValue = parseFloat(getId);
    // //         //                 document.getElementById("editFromHeading").innerText = data.fields.ItemName;
    // //         //                 console.log("Data :- "+JSON.stringify(data.fields));
    // //         //                 setData(data.fields,qI);
    // //         //             })
    // //         //
    // //         //         })
    // //         //         // .catch(error => {
    // //         //         //     console.log("Custom Error :- "+error)
    // //         //         // })
    // //         // }
    // //
    // //     }
    // //
    // //     document.querySelectorAll("#editeBtn").forEach(btn=>{
    // //         btn.onclick = function (){
    // //             console.log(this.parentElement);
    // //             let h1 = this.parentElement.querySelector('h2').innerText;
    // //             let ul = this.parentElement.querySelectorAll('li');
    // //             console.log(h1);
    // //             console.log(ul);
    // //             console.log(this.parentElement.dataset.itemid);
    // //             console.log(document.querySelector("#itemID").defaultValue);
    // //             document.querySelector("#itemID").defaultValue = parseInt(this.parentElement.dataset.itemid);
    // //             // console.log(ul.children[1].innerText);
    // //
    // //
    // //             let updateField = document.getElementById("ingredient-list-from");
    // //             document.getElementById("editFromHeading").innerText = h1;
    // //             updateField.innerHTML = "";
    // //             console.log("Temp li Data");
    // //             ul.forEach(li=>{
    // //                 console.log(li);
    // //             updateField.innerHTML += `<div class="form-element-box">
    // //                                     <label for=${li.dataset.ingredientid} class="from-lable">${li.children[0].innerText}</label>
    // //                                     <div class="form-control">
    // //                                         <input type="number" required class="from-element" name=${li.dataset.ingredientid} value="${li.children[1].innerText}" id=${li.children[0].innerText} placeholder="Requeied ${li.children[0].innerText} in KG ">
    // //                                     </div>
    // //                                 </div>`;
    // //             })
    // //             document.getElementById("item-list-box").style.display = "none";
    // //             document.getElementById("add-item-form").style.display = "inline-block";
    // //         }
    // //     })
    // // })
    // //
    // // document.getElementById("closeEditBtn").onclick = function () {
    // //     console.log("BtnClick");
    // //     document.getElementById("item-list-box").style.display = "inline-block";
    // //     document.getElementById("add-item-form").style.display = "none";
    // //     return false;
    // // }
    //
    // // document.querySelectorAll("#add").forEach(btn=>{
    // //     btn.onclick = function (){
    // //         let data = new Object();
    // //         data[temp] = "t1";
    // //         let st = "/orderInventory/PlaceOrder?";
    // //         arr = btn.parentElement.children[1].querySelectorAll("input");
    // //         arr.forEach(input=>{
    // //             st += `${input.name}=${input.value}&`;
    // //             console.log(input.name);
    // //             console.log(input.value);
    // //         })
    // //
    // //         console.log("From Data"+st);
    // //         console.log("From Submited");
    // //         return false;
    // //     }
    // // })
    //
    // }
    // catch(e){
    //     console.log("Erro  :- "+e);
    // }

    //function of Detail Page
    try {

        let div = document.querySelectorAll(".item-name-text");
        console.log("Drop Down");
        console.log(div);
        div.forEach(item => {
            console.log("Called");
            item.onclick = function () {
                div.forEach(itm => {
                    itm.parentElement.parentElement.style.height = "60px";

                    if(itm.parentElement.parentElement.querySelector(".arrow svg") != undefined){
                        itm.parentElement.parentElement.querySelector(".arrow svg").innerHTML = `<path d="M16.293 9.293 12 13.586 7.707 9.293l-1.414 1.414L12 16.414l5.707-5.707z"></path>`;
                    }
                })
                console.log("|height :- " + item.parentElement.parentElement.style.height);
                console.log("|condition :- " + (item.parentElement.parentElement.style.height == "60px"));
                if (item.parentElement.parentElement.style.height == "60px") {
                    console.log("of condition");
                    console.log("Parent Element");
                    console.log(item.parentElement.parentElement);
                    item.parentElement.parentElement.style.height = "auto";
                    try{
                        item.parentElement.parentElement.querySelector(".arrow svg").innerHTML = `<path d="m6.293 13.293 1.414 1.414L12 10.414l4.293 4.293 1.414-1.414L12 7.586z"></path>`;
                    }
                    catch (e) {
                        console.log("Delete Btn Enable");
                    }
                }
                else {
                    item.parentElement.style.height = "60px";
                    console.log("ElseCondition");
                }
            }
        }) ;

    }
    catch (e) {
        console.log("AddItem Page Elements");
    }

    //Add Item Function
    try{
        document.querySelectorAll('.delete').forEach(div=>{
            console.log(div.children[0].innerText);
            addedItemList[div.dataset.itemid] = div.children[0].innerText;
        })
        updateOrderItemList();

        updateAvelableItem();

    }
    catch (e) {
        console.log("AddItemFuncitonality Called");
    }
})


//Add Item Functions
function updateOrderItemList() {

    document.querySelectorAll(".delete").forEach(btn=>{
        btn.onclick = function (){
            console.log("Bin Btn Click ");
            let itemId = this.dataset.itemid;
            console.log(this);
            console.log(itemId);
            document.querySelector(`#hiddenInput input[value="${itemId}"]`).remove();
            this.remove();

            document.querySelector("#avalable-items").innerHTML += `
                <div class="suggetion-list-item">
                    <p class="text" data-itemid="${itemId}" data-queryItem="item_one">${addedItemList[itemId]}
                    </p>
                    <button class="add button-remove">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                            <path d="M15 2.013H9V9H2v6h7v6.987h6V15h7V9h-7z"></path>
                        </svg>
                    </button>
                </div>
            `;

            delete addedItemList[itemId];
            // if(confirm("Do you really want to Delete this Order ?")){
            //     let itemId = btn.parentElement.parentElement.dataset.itemid;
            //     let orderId = btn.parentElement.parentElement.parentElement.dataset.orderid;
            //     console.log(itemId);
            //     console.log(orderId);
            //     console.log(addedItemList.pop(itemId));
            // }
            // else{
            //     alert("You Go in Else Part");
            // }
            updateAvelableItem();
        }
    })

    updateAvelableItem();
}



//Support Function for tracking addable item into order List
//it also add event listner to all P tag for adding into Order Item
function updateAvelableItem(){
    document.querySelectorAll("#item-list-box .suggetion-list-item p").forEach(p=>{

        let id = p.dataset.itemid
        if(id in addedItemList){
            p.parentElement.remove();
        }
    })

    document.querySelectorAll(".text").forEach(p=>{
        p.onclick = function () {
            console.log("Button CLick");
            const itemId = this.dataset.itemid;
            let itemName = this.innerHTML;

            addedItemList[itemId] = itemName;

            let input= document.createElement("input");
            input.type = "text";
            input.name = `itemID${itemId}`;
            input.defaultValue = itemId
            input.style.display = "none";

            document.querySelector("#hiddenInput").append(input);

            // addedItemList.push(itemId);

            this.parentElement.remove();

            document.querySelector("#orderItems").innerHTML += `
            <div class="suggetion-list-item delete" data-itemid="${itemId}">
                <p class="text_style">${itemName}
                </p>
                <button class="add button-remove" type="button" role="button">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                    <path d="M6 7H5v13a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7H6zm4 12H8v-9h2v9zm6 0h-2v-9h2v9zm.618-15L15 2H9L7.382 4H3v2h18V4z"></path>
                    </svg>
                </button>
            </div>
            `;

            updateOrderItemList()
        }
    });

}


//##########################################################
//                      New Item Functions
//##########################################################

//Functions to Display New Item From
document.getElementById("newItemBtn").onclick = function (){
    IngredientListUpdate();
    console.log("New Item From");
    document.getElementById("newItemBox").style.display = "block";
    document.getElementById("orderBox").style.display = "none";
}

document.getElementById("closeItemBtn").onclick = function (){
    document.getElementById("orderBox").style.display = "block";
    document.getElementById("newItemBox").style.display = "none";
    cleanUpNewItemData();
}

//Value Cleanup For New Item
function cleanUpNewItemData(){
    document.getElementById("newIngredientHidden").innerHTML="";
    document.getElementById("itemIngredients").innerHTML = "";
    document.getElementById("itemNameInput").value = null;
    document.getElementById("typeId").value = null;

}

//This will add Ingredient of Item in Input list As well as Visual Display
function addItemIngredient(addBtn){

    console.log(addBtn);
    let id = addBtn.dataset.ingredientid;
    let ingredient =  addBtn.innerHTML;
    console.log("Ingredient Name :- ",ingredient);
    console.log("Ingredient Id :- ", id);

    //Add Ingredient to Item form list
    const input = document.createElement("input");
    input.type = "number";
    input.name = `ingredientId${id}`;
    input.defaultValue = id;
    input.style.display = "none";

    addedIngredient[id] = ingredient

    document.getElementById("newIngredientHidden").appendChild(input);


    //add ingredient to visual list of Item ingredient
    document.getElementById("itemIngredients").innerHTML += `
        <div class="suggetion-list-item" data-ingredientId="${id}" id="delete">
            <p class="text_style editIngredients"  data-queryItem="item_one">${ingredient}</p>
            <button class="add button-remove" type="button" role="button">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path d="M6 7H5v13a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7H6zm4 12H8v-9h2v9zm6 0h-2v-9h2v9zm.618-15L15 2H9L7.382 4H3v2h18V4z"></path>
                </svg>
            </button>
        </div>
    `;
    IngredientListUpdate();
    scrollTOEnd("#itemIngredients");
}


//this Function add delete event listener to all Newly added Ingredients
function ItemIngredientUpdate(){

    document.querySelectorAll("#delete").forEach(btn=>{
        btn.onclick = async function (){
            let tt = this.dataset.ingredientid;
            this.remove();

            document.querySelector(`input[name="ingredientId${tt}"]`).remove();

            document.querySelector("#available-ingredient").innerHTML += `
                <div class="suggetion-list-item">
                    <p class="text_style addIngredients" data-ingredientId="${tt}" data-queryItem="ingredient_one">${addedIngredient[tt]}
                    </p>
                    <button class="add button-remove" role="button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                            <path d="M15 2.013H9V9H2v6h7v6.987h6V15h7V9h-7z"></path>
                        </svg>
                    </button>
                </div>
            `;
            delete addedIngredient[tt];
            IngredientListUpdate();
        }
    });
}

//Update Available Ingredient List by removing added Ingredient from list
// depended Function
//      ItemIngredientUpdate
//      addItemIngredient
function IngredientListUpdate(){
    document.querySelectorAll("#ingredient-list-box .addIngredients").forEach(p=>{
        let tt = p.dataset.ingredientid;
        if(tt in addedIngredient){
            console.log("Display None");
            console.log(tt);
            p.parentElement.remove();
        }
    })


    //add Event Listener("Add to Item") to a ingredient to available Ingredient List
    let addIngredient = document.querySelectorAll(".addIngredients");
    if(addIngredient.length !== 0){

        addIngredient.forEach(p=>{
            p.onclick = function (){
                console.log(p.dataset.ingredientid);
                addItemIngredient(p);
                ItemIngredientUpdate();

            }
        })

    }

}

document.getElementById("newItemFrom").onsubmit = function (){


    let l = this.elements;
    console.log(this.elements.length);
    let pera = `name=${l["name"].value}&type=${l["type"].value}&json=true&ItemId=`;
    for(let i=0;i<l.length;i++){
        if(l[i].type === "number"){
            console.log(l[i]);
            console.log(l[i].value);
            console.log(l[i].name);
            pera += `&${l[i].name}=${l[i].value}`;
        }
    }
    pera = pera.replace(" ","+");
    console.log(pera);
    fetch(`/orderInventory/ItemsNew/`,{
            method : "POST",
            headers: {
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
            },
            credentials: 'include',
            body : pera
        })
        .then(response => response.json())
            .then(data=>{
                console.log("data");
                console.log(data.data);

                const itemId = data.data.id;
                let itemName = data.data.name;
                console.log(this);
                console.log(this.dataset.itemid);
                addedItemList[itemId] = itemName;

                let input= document.createElement("input");
                input.type = "text";
                input.name = `itemID${itemId}`;
                input.defaultValue = itemId
                input.style.display = "none";

                document.querySelector("#hiddenInput").append(input);

                // addedItemList.push(itemId);

                document.querySelector("#orderItems").innerHTML += `
                <div class="suggetion-list-item delete" data-itemid="${itemId}">
                    <p class="text_style">${itemName}
                    </p>
                    <button class="add button-remove" type="button" role="button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                        <path d="M6 7H5v13a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7H6zm4 12H8v-9h2v9zm6 0h-2v-9h2v9zm.618-15L15 2H9L7.382 4H3v2h18V4z"></path>
                        </svg>
                    </button>
                </div>
                `;

                updateOrderItemList()
            })

        console.log(document.getElementById("newItemBox"));
        document.getElementById("orderBox").style.display = "block";
        document.getElementById("newItemBox").style.display = "none";
        cleanUpNewItemData();
    return false;
}


//##########################################################
//                      New Ingredient Functions
//##########################################################

//Add new Ingredient From Item Page
try{

    document.querySelector("#closeEditBtn").onclick = function (){

        let tt = document.getElementById("newIngredientFrom");
        tt.elements[0].value= "";
        tt.elements[1].value= 0;

        document.getElementById("ingredient-list-box").style.display = "inline-block";
        document.getElementById("add-New-ingredient-form").style.display = "none";
    }

    //Add new Ingredient From Item Page
    document.querySelector("#addNewIngredientBtn").onclick = function () {
        document.querySelector("#ingredient-list-box").style.display = "none";
        document.querySelector("#add-New-ingredient-form").style.display = "inline-block";
    }

    document.querySelector("#newIngredientFrom").onsubmit = function () {
        console.log("New Ingredient From Submitted  ");
        categoryId=this.elements[1].value;
        name = this.elements[0].value;
        fetch('/orderInventory/IngredientNew/',{
            method : "POST",
            headers: {
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
            },
            credentials: 'include',
            body : `name=${name}&categoryId=${categoryId}&json=1`
        })
            .then(response => response.json())
            .then(data=>{
                console.log("data");
                console.log(data);

                addedIngredient[data.newIngredientId] = name;

                document.getElementById("itemIngredients").innerHTML += `
                    <div class="suggetion-list-item" data-ingredientId="${data.newIngredientId}" id="delete">
                        <p class="text_style editIngredients"  data-queryItem="item_one" >${name}</p>
                        <button class="add button-remove" type="button" role="button">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                            <path d="M6 7H5v13a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7H6zm4 12H8v-9h2v9zm6 0h-2v-9h2v9zm.618-15L15 2H9L7.382 4H3v2h18V4z"></path>
                            </svg>
                        </button>
                    </div>
                `;

                const input = document.createElement("input");
                input.type = "number";
                input.name = `ingredientId${data.newIngredientId}`;
                input.defaultValue = `${data.newIngredientId}`;
                input.style.display = "none";

                document.getElementById("newIngredientHidden").appendChild(input);

                ItemIngredientUpdate();

            })

        document.querySelector("#ingredient-list-box").style.display = "inline-block";
        document.querySelector("#add-New-ingredient-form").style.display = "none";


        this.elements[1].value = 0;
        this.elements[0].value = "";
        // document.querySelector("#newIngredientFrom");
        return false;
    }
}
catch (e) {
    console.log("This function is for item page");
}


function scrollTOEnd(element_selector){
    //Utility Function
    //Function To scroll at End of element
    //Input :- Query Selector
    //return :- Void
    try{
        let tmp = document.querySelector(element_selector);
        tmp.scrollTo(0,tmp.scrollHeight);
    }
    catch (e) {
        console.error("Wrong Query Selector");
    }
}