var temp = "";
var addedIngredient ={};
document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".pdf").forEach(pdf => {
        pdf.onclick = function () {
            console.log(pdf.children[0]);
            pdf.children[0].height = "720px";
            pdf.children[0].width = "1200px";
        }
    });


    document.querySelectorAll(".text").forEach(btn => {
        btn.onclick = function () {

            // console.log(btn.dataset);
            let getId = btn.dataset.itemid;
            let qI = btn.dataset.queryitem;
            console.log("Id :- "+getId);
            console.log("queryName :- "+qI);

            if (getId !== undefined){
                fetch(`/orderInventory/detail?queryItem=${qI}&queryId=${getId}`)
                    .then(responce => responce.json())
                    .then(data => {
                        console.log("Fetch Data :- "+ data);
                        console.log("Type :"+ typeof(data));
                        console.log("Type :"+ JSON.stringify(data));
                        if ( typeof(data) == 'object'){
                            temp = data;
                        }
                        else
                        {
                        temp = JSON.parse(data);
                        }
                        console.log("Temp :- "+temp);
                        if(qI === "order_one"){
                            temp.forEach(data => {
                                console.log(data.fields);
                            })
                        }
                        else{
                            temp.forEach(data => {
                                console.log(data.fields);
                                if(qI === "item_one"){
                                    console.log("Item Update Call");
                                    let tempInput = document.createElement("input");
                                    tempInput.name = "ItemId";
                                    tempInput.defaultValue = getId;
                                    tempInput.style.display = "none";
                                    document.getElementById("newIngredientHidden").appendChild(tempInput);
                                    setDataFromUpdateItem(data.fields,getId);
                                }
                                else{
                                    if(document.getElementById("updateElementID") !== undefined){
                                        document.getElementById("updateElementID").defaultValue = getId;
                                    }
                                    setData(data.fields,qI);
                                }
                            })
                        }

                    })
                    // .catch(error => {
                    //     console.log("Custom Error :- "+error)
                    // })
            }

            let tmp = document.getElementById("toolbox");
            if(tmp !== undefined){
                tmp.style.display = "none";
            }
        }
    })

    try{
        document.querySelectorAll("#deleteFromItems").forEach(p=>{
            p.onsubmit = function (){
                if(confirm("Do you really want to Delete This ?")){
                    return true
                }
                return false
            }
        })
    }
    catch (e) {
        console.log("No Item Found")
    }

    try{
        IngredientListUpdate();
    }
    catch (e) {
        console.log("newly Added  update Listner");
    }
})

document.querySelectorAll(".edit").forEach(btn=>{
    btn.onclick = function (){
        document.getElementById('updateBox').style.display = "inline-block";
        document.getElementById('detailBox').style.display = "none";
    }
})


document.querySelectorAll(".newItem").forEach(btn=>{
    btn.onclick = function (){
        addedIngredient = {};
        IngredientListUpdate();
        let tmp = document.getElementById("toolbox");
        if(tmp !== undefined){
            tmp.style.display = "none";
        }
        document.getElementById("newItemBox").style.display = "block";
        document.getElementById("single-section").style.display = "none";

        if(document.getElementById("multi-section") !== undefined){
            document.getElementById("multi-section").style.display = "none";
        }
    }
})

document.querySelectorAll(".cancel-btn").forEach(btn => {
    btn.onclick = function (){
        let tmp = document.getElementById("toolbox");
        if(tmp !== undefined){
            tmp.style.display = "grid";
        }
        console.log("log Entry");
        document.getElementById("single-section").style.display = "block";
        document.getElementById("newItemBox").style.display = "none";


        //clear edit Item data onclick on cancel
        try{
            addedIngredient = {};
            document.getElementById("add-New-ingredient-form").style.display = "none";
            document.getElementById("ingredient-list-box").style.display = "inline-block";
            // document.getElementById("newItem").action = "/orderInventory/ItemsNew/";
            document.getElementById("newIngredientHidden").innerHTML = "";
            document.getElementById("newItemSubmitBtn").value = "Create";
            document.getElementById("updateItemId").defaultValue = "";
            document.getElementById("name").value = "";
            document.getElementById("itemIngredients").innerHTML = "";
            document.getElementById("add-ingredient-form").style.display = "none";
            document.getElementById("ingredient-list-box").style.display = "inline-block";
        }
        catch (e){
            console.log("Close btn for Edit Items");
        }

        try{
            document.getElementById('detailBox').style.display = "inline-block";
            document.getElementById('updateBox').style.display = "none";
            document.getElementById("multi-section").style.display = "none";
        }
        catch (e) {
            console.log("Error :- " + e);
        }

        return false
    }
})


//function for Item Tab
function setDataFromUpdateItem(data,queryID){

    document.getElementById("itemIngredients").innerHTML = "";

    console.log("setDataFromUpdateItem Call ");

    document.getElementById("name").value = data.ItemName;
    console.log("Type value  :- "+ data.type);
    if(data.type == null){
        console.log("value is Null :- "+ data.type);
    }
    else{
        document.getElementById("typeId").value = data.type;
    }
    for(let i in data.ingredient){

            for(let j in data.ingredient[i]) {

                  document.getElementById("itemIngredients").innerHTML += `
                    <div class="suggetion-list-item" data-ingredientId="${j}" id="delete">
                        <p class="text_style editIngredients"  data-queryItem="item_one" >${data.ingredient[i][j]}</p>
                        <button class="add button-remove" type="button" role="button">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                            <path d="M6 7H5v13a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7H6zm4 12H8v-9h2v9zm6 0h-2v-9h2v9zm.618-15L15 2H9L7.382 4H3v2h18V4z"></path>
                            </svg>
                        </button>
                    </div>
                `;

                  addedIngredient[j] = data.ingredient[i][j];
                const input = document.createElement("input");
                input.type = "number";
                input.name = `ingredientId${j}`;
                input.defaultValue = `${j}`;
                input.style.display = "none";

                document.getElementById("newIngredientHidden").appendChild(input);

            }
    }

    document.getElementById("single-section").style.display = "none";
    document.getElementById("newItemBox").style.display = "block";

    document.getElementById("updateItemId").defaultValue = queryID;

    console.log("Submit Btn");
    console.log(document.getElementById("newItemSubmitBtn").value = "Update");

    ItemIngredientUpdate();
    IngredientListUpdate();
    scrollTOEnd("#itemIngredients");

    return false;
}

//Add new Ingredient From Item Page
try{

    document.querySelector("#closeEditBtn").onclick = function (){
        document.getElementById("ingredient-list-box").style.display = "inline-block";
        document.getElementById("add-New-ingredient-form").style.display = "none";

        let tt = document.getElementById("newIngredientFrom");
        tt.element[0].value= 0;
        tt.element[1].value = "";
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

//Set data for Category and Ingredient
function setData(data,queryitem){

    let ul = document.querySelector(".detail-list");
    ul.innerHTML = "";
    for(let item in data){
        if(data[item] != null && item !== "createdAt"){
            try{
                document.getElementById(item).value = data[item];
            }
            catch(e){
                console.log("Catch Block : "+item+" field Does not Exists")
            }

            // forDetails Display
            let li = document.createElement("li");
            if(item === "category"){
                console.log("Category set");
                li.innerHTML = `<span>${item.toUpperCase() } : </span> ${findSore(data[item])}`;
            }
            else {
                li.innerHTML = `<span>${item.toUpperCase() } : </span> ${data[item]}`;
            }
            ul.appendChild(li);
        }
    }
    document.getElementById("multi-section").style.display = "block";
    document.getElementById("single-section").style.display = "none";

}

function findSore(id){
    op = document.querySelector(`select`).options;
    for(let i=0;i<op.length;i++){
        if (parseInt(op[i].value) === id){
            return op[i].innerText;
        }
    }
}

//this Function add delete event listener to all Newly added Ingredients
function ItemIngredientUpdate(){

    document.querySelectorAll("#delete").forEach(btn=>{
        btn.onclick = function (){
            let tt = this.dataset.ingredientid;
            this.remove();
            console.log("Ingredient Deleted",addedIngredient[tt]);
            document.querySelector(`input[value="${tt}"]`).remove();

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

function IngredientListUpdate(){
    //Supportive Function

    //Remove Ingredient Which is already in Item
    document.querySelectorAll("#ingredient-list-box .addIngredients").forEach(p=>{
        let tt = p.dataset.ingredientid;
        if(tt in addedIngredient){
            p.parentElement.remove();
        }
    })


    //add Event Listener("Add to Item") to a ingredient to available Ingredient List
    let addIngredient = document.querySelectorAll(".addIngredients");
    if(addIngredient.length !== 0){

        addIngredient.forEach(p=>{
            p.onclick = function (){

                addItemIngredient(p);
                ItemIngredientUpdate();

            }
        })

    // ==============================================================================
    //  =====================================   delete From Functionality
    // ==============================================================================

        // let addBtn = document.getElementById("addBtn");
        // let closeEditBtn = document.getElementById("closeEditBtn");
        // if(closeEditBtn !== null){
        //     closeEditBtn.onclick = function (){
        //         document.getElementById("defaultValue").value = "";
        //         document.getElementById("ingredient-list-box").style.display = "inline-block";
        //         document.getElementById("add-ingredient-form").style.display = "none";
        //         return false;
        //     }
        // }
        // if(addBtn !== null){
        // addBtn.onclick = function (){
        //     console.log("Button Submit");
        //
        //     document.getElementById("closeEditBtn").style.display = "inline-block";
        //     // addItemIngredient(addBtn);
        //     // ItemIngredientUpdate();
        //
        //     return false;
        // }
    // }

    }

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