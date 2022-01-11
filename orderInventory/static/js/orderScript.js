var addedItemList = {};
var countItem = 0;
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

try{
    document.querySelectorAll(".text").forEach(p=>{
        p.onclick = function () {
            console.log("Button CLick");
            const itemId = this.dataset.itemid;
            let itemName = this.innerHTML;
            console.log(this);
            console.log(this.dataset.itemid);
            addedItemList[itemId] = itemName;
            // addedItemList[div.   dataset.itemid] = div.children[0].innerText;
            // Object.assign(addedItemList, {itemId: itemName})

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
            // let t =document.querySelectorAll("#add-item-form input");
            // let t1 =document.querySelectorAll("#add-item-form label");
            // console.log(t);
            // let id;
            // let data = {};
            // let dataDisplay = {};
            // for(let i=2;i<t.length;i++){
            //     dataDisplay[t[i].name] = {
            //         "name": t1[i-2].innerText,
            //         "value":t[i].value
            //     };
            // }
            //
            // console.log("Display Array :- ");
            // console.log(dataDisplay);
            //
            // t.forEach(t=>{
            //     data[t.name] = t.value;
            // })
            // console.log("Data Extracted : ");
            // console.log(data);
            //
            // //Send Data to Server to Add Item to Order
            // fetch('/orderInventory/OrderAddItems/',{
            //     method:"POST",
            //     body : JSON.stringify(data),
            //     headers : {
            //         "Content-type":"application/json; charset=UTF-8"
            //     }
            // }).then(responce => responce.json())
            // .then(data=>{
            //     console.log("Response Data :- ");
            //     console.log(data);
            //     console.log(id=data.id);
            // });
            //
            // let ItemData = "";
            // for( let key in dataDisplay){
            //     ItemData += `
            //         <li data-ingredientId="${key}"><label>${dataDisplay[key].name}</label> : <span>${dataDisplay[key].value}</span>  Kg </li>
            //         `;
            // }
            //
            // document.getElementById("orderItems").innerHTML += `
            //     <div class="item-box" data-itemid="${document.querySelector('#itemID').value}" >
            //         <h2 class="item-name">
            //             <span class="item-name-text">
            //                 ${document.getElementById("editFromHeading").innerText}
            //             </span>
            //             <span class="bin">
            //                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" >
            //                     <path d="M6 7H5v13a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7H6zm4 12H8v-9h2v9zm6 0h-2v-9h2v9zm.618-15L15 2H9L7.382 4H3v2h18V4z">
            //                     </path>
            //             </svg>
            //             </span>
            //         </h2>
            //         <ul class="ingredient-list">
            //             ${ItemData}
            //         </ul>
            //         <button class="button-remove button-style-1 edit-btn " type="button" role="button" id="editeBtn" > Edit </button>
            //     </div>
            // `;
            //
            // updateOrderItemList();
            // updateAvelableItem();
            //
            // document.getElementById("item-list-box").style.display = "inline-block";
            // document.getElementById("add-item-form").style.display = "none";
        }
    });
}
catch (e) {
    console.log("Add item to Order Function");
}


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
function updateAvelableItem(){
    document.querySelectorAll("#item-list-box .suggetion-list-item p").forEach(p=>{

        let id = p.dataset.itemid
        if(id in addedItemList){
            p.parentElement.style.display ="none";
        }
        else {
            p.parentElement.style.display = "grid";
        }
        // let temp = parseInt(p.dataset.itemid);
        // console.log("TEmp " +p.dataset.itemid);
        // console.log(temp in addedItemList);
        // console.log(typeof(temp));
        // console.log(temp.length);
        //
        // if(temp in addedItemList){
        //     p.parentElement.style.display = "none";
        // }
        // else {
        //     p.parentElement.style.display = "grid";
        // }
    })
}