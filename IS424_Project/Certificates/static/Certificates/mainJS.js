document.addEventListener("DOMContentLoaded",()=>{

 if(document.title == "Menu"){
    const ew = document.querySelector("#homeselect");

    
     ew.style.color = "white";
     ew.style.fontWeight = "bold";
     
 }
 else if(document.title == "View"){
    const ew = document.querySelector("#viewselect");

     ew.style.color = "white";
     ew.style.fontWeight = "bold";

 }
 else if(document.title == "Add"){
    const ew = document.querySelector("#addselect");

     ew.style.color = "white";
     ew.style.fontWeight = "bold";
 }
 else if(document.title == "Update"){
    const ew = document.querySelector("#updateselect");

     ew.style.color = "white";
     ew.style.fontWeight = "bold";
 }
 else if(document.title == "Delete"){
    const ew = document.querySelector("#deleteselect");


     ew.style.color = "white";
     ew.style.fontWeight = "bold";
 }



});


