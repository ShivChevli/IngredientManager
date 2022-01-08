var temp = "";
var ingredientCount = 0;

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

            if (getId != undefined){
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
                                        document.getElementById("updateElementID").value = getId;
                                        document.getElementById("deleteElementId").value = getId;
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
            if(tmp != undefined){
                tmp.style.display = "none";
            }
        }
    })
    let addIngredient = document.querySelectorAll(".addIngredients");

    if(addIngredient.length !== 0){
        ingredientCount = 0;
        addIngredient.forEach(p=>{
            p.onclick = function (){

                document.getElementById("editFromHeading").innerText = p.innerText;
                document.getElementById("id").innerText = p.dataset.ingredientid;
                console.log(p.dataset.ingredientid);
                document.getElementById("add-ingredient-form").style.display = "inline-block";
                document.getElementById("ingredient-list-box").style.display = "none";
                document.getElementById("defaultValue").focus();
            }
        })

        let addBtn = document.getElementById("addBtn");
        let closeEditBtn = document.getElementById("closeEditBtn");
        if(closeEditBtn !== null){
            closeEditBtn.onclick = function (){
                document.getElementById("defaultValue").value = "";
                document.getElementById("ingredient-list-box").style.display = "inline-block";
                document.getElementById("add-ingredient-form").style.display = "none";
                return false;
            }
        }
        if(addBtn !== null){
        addBtn.onclick = function (){
            console.log("Button Submit");

            document.getElementById("closeEditBtn").style.display = "inline-block";
            addItemIngredient(addBtn);
            ItemIngredientUpdate();

            return false;
        }

        document.querySelector("#defaultValue").onkeyup = function (key) {
                console.log(key.key);
                if(key.key == "Enter"){
                    console.log("Enter Entered");
                }
        }


    }
    }

    //Delete element in Store and Ingredient Form
    try{
        document.getElementById("deleteFrom").onsubmit = function (){
            console.log("data :-");
            if(confirm("Do you Sure want to Delete this Item ?")){
                return true;
            }
            else{
                 return false;
            }
            return false;
        }
    }
    catch (e) {
        console.log('This Is Not From Extended Template');
    }

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
})

document.querySelectorAll(".edit").forEach(btn=>{
    btn.onclick = function (){
        document.getElementById('updateBox').style.display = "inline-block";
        document.getElementById('detailBox').style.display = "none";
    }
})


document.querySelectorAll(".newItem").forEach(btn=>{
    btn.onclick = function (){
        let tmp = document.getElementById("toolbox");
        if(tmp != undefined){
            tmp.style.display = "none";
        }
        document.getElementById("newItemBox").style.display = "block";
        document.getElementById("single-section").style.display = "none";

        if(document.getElementById("multi-section") != undefined){
            document.getElementById("multi-section").style.display = "none";
        }
    }
})

document.querySelectorAll(".cancel-btn").forEach(btn => {
    btn.onclick = function (){
        let tmp = document.getElementById("toolbox");
        if(tmp != undefined){
            tmp.style.display = "grid";
        }
        console.log("log Entry");
        document.getElementById("single-section").style.display = "block";
        document.getElementById("newItemBox").style.display = "none";


        //clear edit Item data onclick on cancel
        try{
            document.getElementById("newItem").action = "/orderInventory/ItemsNew/";
            document.getElementById("newIngredientHidden").innerHTML = "";
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

function setDataFromUpdateItem(data,queryID){

    document.getElementById("itemIngredients").innerHTML = "";
    ingredientCount = 0;

    console.log("setDataFromUpdateItem Call ");
    console.log(data);

    // document.getElementById("newItem").action = "/orderInventory/IngredientUpdate/";


    document.getElementById("name").value = data.ItemName;
    let id = 0;
    for(let i in data.ingredient){

            for(let j in data.ingredient[i]) {

                if(j === "id"){
                    id = data.ingredient[i][j];
                }
                else{

                    document.getElementById("itemIngredients").innerHTML += `
                    <div class="suggetion-list-item">
                        <p class="text_style editIngredients"  data-queryItem="item_one" ><span>${j}</span>  : <span>${data.ingredient[i][j]}</span> Kg <span style="display: none">${id}</span></p>
                        <button class="add button-remove" type="button" role="button" id="delete">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                            <path d="M6 7H5v13a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7H6zm4 12H8v-9h2v9zm6 0h-2v-9h2v9zm.618-15L15 2H9L7.382 4H3v2h18V4z"></path>
                            </svg>
                        </button>
                    </div>
                `;

                const input = document.createElement("input");
                input.type = "number";
                input.name = `ingredientId${ingredientCount}`;
                input.defaultValue = `${id}`;
                input.style.display = "none";

                const Ingredentvalue = document.createElement("input");
                Ingredentvalue.name = `value${ingredientCount}`;
                Ingredentvalue.type = "number";
                Ingredentvalue.defaultValue = `${data.ingredient[i][j]}`;
                Ingredentvalue.style.display = "none";

                document.getElementById("newIngredientHidden").appendChild(input);
                document.getElementById("newIngredientHidden").appendChild(Ingredentvalue);
                ingredientCount++;
            }
        }
    }

    document.getElementById("single-section").style.display = "none";
    document.getElementById("newItemBox").style.display = "block";

    const input = document.createElement("input");
    console.log("INput Field Data :- " + queryID );
    input.type = "number";
    input.defaultValue = parseInt(queryID);
    input.name = `updateItemId`;
    input.style.display = "none";

    document.getElementById("newIngredientHidden").appendChild(input);
    document.getElementById("newItem").action = "/orderInventory/ItemsUpdate/";

    ItemIngredientUpdate();

    return false;
}

function setData(data,queryitem){
    console.log("Query Item :"+queryitem);
    let ul = document.querySelector(".detail-list");
    ul.innerHTML = "";
    let updateForm = document.getElementById("updateField");
    console.log("Set Data Method called");
    console.log(data);
    for(let item in data){
        if(data[item] != null){
            // if(item === "createdAt"){
            //     // let d = new Date(data[item])
            //     // document.getElementById(item).value = d.toISOString().substring(0,16);
            // }
            // // else if(typeof(data[item]) == "object"){
            // //     addFields(data[item]);
            // // }
            // else{
                try{
                    document.getElementById(item).value = data[item];
                }
                catch(e){
                    console.log("Catch Block : "+item+" field Does not Exists")
                }
            // }

            // forDetails Display
            let li = document.createElement("li");
            if(item == "orderAt"){
                li.innerHTML = `<span>${item.toUpperCase() } : </span> ${findSore(data[item])}`;
            }
            else if(item == "createdAt"){

            }
            else if(typeof(data[item]) == 'object'){
                let table = creatTable(data[item])
                let span1 = document.createElement("span");
                span1.innerHTML = item.toUpperCase();
                let span2 = document.createElement("span");
                span2.appendChild(table);
                li.appendChild(span1);
                li.appendChild(span2);
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
        if (op[i].value == id){
            return op[i].innerText;
        }
    }
}

function creatTable(data){
    console.log("Data : "+JSON.stringify(data));
    let table = document.createElement("table");
    table.classList.add("detail-table");
    data.forEach(div=>{
        for(let key in div){
                table.innerHTML += `<tr>
                                        <td>${key}</td>
                                        <td>${div[key]}</td>
                                    </tr>`;
        }
    })
    return table;
}


//this Funtion add event listner to all Newly added Ingredients
function ItemIngredientUpdate(){

    document.querySelectorAll(".editIngredients").forEach(btn=>{
        btn.onclick = function (){
            let p = this.parentElement.querySelectorAll("span");
            console.log(p[0].innerText);
            console.log(p[1].innerText);
            console.log(p[2].innerText);
            this.parentElement.remove();
            ingredientCount--;
            document.querySelector(`input[name="value${ingredientCount}"]`).remove();
            document.querySelector(`input[name="ingredientId${ingredientCount}"]`).remove();
            document.getElementById("editFromHeading").innerText = p[0].innerText;
            document.getElementById("defaultValue").value = parseFloat(p[1].innerText);
            document.getElementById("id").innerText = p[2].innerText;

            document.getElementById("closeEditBtn").style.display = "none";
            document.getElementById("ingredient-list-box").style.display = "none";
            document.getElementById("add-ingredient-form").style.display = "inline-block";
        }
    });

    document.querySelectorAll("#delete").forEach(btn=>{
        btn.onclick = function (){
            console.log("Ingredient Deleted");
            if(confirm("Do you want to Realy Delete This Item ?")){
                this.parentElement.remove();
                ingredientCount--;
                document.querySelector(`input[name="value${ingredientCount}"]`).remove();
                document.querySelector(`input[name="ingredientId${ingredientCount}"]`).remove();
            }
        }
    });

}

//This will add Ingredient of Item in Input list As well as Visual Display
function addItemIngredient(addBtn){
    let id = addBtn.parentElement.querySelector('#id').innerText;
    console.log("Id : "+ id);
    let item = addBtn.parentElement.querySelector('input').value;
    let ingredientName = addBtn.parentElement.querySelector("#editFromHeading").innerText;
    const input = document.createElement("input");
    input.type = "number";
    input.name = `ingredientId${ingredientCount}`;
    input.defaultValue = id;
    input.style.display = "none";

    const Ingredentvalue = document.createElement("input");
    Ingredentvalue.name = `value${ingredientCount}`;
    Ingredentvalue.type = "number";
    Ingredentvalue.defaultValue = item;
    Ingredentvalue.style.display = "none";

    document.getElementById("newIngredientHidden").appendChild(input);
    document.getElementById("newIngredientHidden").appendChild(Ingredentvalue);
    ingredientCount++;
    document.getElementById("itemIngredients").innerHTML += `
        <div class="suggetion-list-item ">
            <p class="text_style editIngredients"  data-queryItem="item_one" data-defaultValue="${item}"><span>${ingredientName}</span>  : <span>${item}</span> Kg<span style="display: none">${id}</span> </p>
            <button class="add button-remove" data-quantity="${item}" type="button" role="button" id="delete">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path d="M6 7H5v13a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7H6zm4 12H8v-9h2v9zm6 0h-2v-9h2v9zm.618-15L15 2H9L7.382 4H3v2h18V4z"></path>
                </svg>
            </button>
        </div>
    `;

    addBtn.parentElement.querySelector('input').value = "";
    document.getElementById("ingredient-list-box").style.display = "inline-block";
    document.getElementById("add-ingredient-form").style.display = "none";

}
function addFields(data){
    let updateField = document.getElementById("updateField");
    data.forEach(div=>{
            for(let key in div){
            console.log("Key : "+key+"\nValue :- "+div[key]);
                updateField.innerHTML += `<div class="form-element-box">
                                        <label for=${key} class="from-lable">${key}</label>
                                        <div class="form-control">
                                            <input type="number" required class="from-element" value="${div[key]}" name=${key} id=${key} placeholder="Enter ${key} value">
                                        </div>
                                    </div>`;
        }
    })
}


function createSuggestions(data) {

    let div = document.createElement("div");
    div.classList.add("suggetion-list-item");
    div.innerHTML = `\
        <p class='text'>${data}</p>\
        <button class='add button-remove' >\
            <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>\
                <path d='M15 2.013H9V9H2v6h7v6.987h6V15h7V9h-7z'></path>\
            </svg>\
        </button >`;
    document.querySelector(".suggetion-container").appendChild(div);
}

function createListItem(data) {
    let div = document.createElement("div");
    div.classList.add("suggetion-list-item");
    div.innerHTML = `\
        <p class='text'>${data}</p>\
        <button class='add button-remove' >\
            <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>\
                <path d="m18.988 2.012 3 3L19.701 7.3l-3-3zM8 16h3l7.287-7.287-3-3L8 13z"></path>
                <path
                    d="M19 19H8.158c-.026 0-.053.01-.079.01-.033 0-.066-.009-.1-.01H5V5h6.847l2-2H5c-1.103 0-2 .896-2 2v14c0 1.104.897 2 2 2h14a2 2 0 0 0 2-2v-8.668l-2 2V19z">
                </path>
            </svg>\
        </button >`;
    document.querySelector(".single-container").appendChild(div);
}

function createRecentList(data) {
    let div = document.createElement("div");
    div.classList.add("suggetion-list-item");
    div.innerHTML = `\
        <p class='text'>${data}</p>\
        <button class='add button-remove' >\
            <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>\
                <path d="M2.165 19.551c.186.28.499.449.835.449h15c.4 0 .762-.238.919-.606l3-7A.998.998 0 0 0 21 11h-1V8c0-1.103-.897-2-2-2h-6.655L8.789 4H4c-1.103 0-2 .897-2 2v13h.007a1 1 0 0 0 .158.551zM18 8v3H6c-.4 0-.762.238-.919.606L4 14.129V8h14z"></path>\
            </svg>\
        </button >`;
    document.querySelector(".single-container").appendChild(div);
}

function createFormElement(type, name, lable = "", id = "") {
    let div = document.createElement("div");
    div.classList.add("form-element-box");
    let formDiv = document.createElement("div");
    formDiv.classList.add("form-control");
    formDiv.innerHTML = `<input type="${type}" class="from-element" name="${name}">`;
    if (lable != "") {
        let l = document.createElement('label');
        l.classList.add('from-lable');
        l.innerHTML = lable;
        div.appendChild(l);
        l.id = id;
    }
    div.appendChild(formDiv);
    document.querySelector(".section2").appendChild(div);
}