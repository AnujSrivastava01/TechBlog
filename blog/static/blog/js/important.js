console.log("First js");

let previews=document.getElementsByClassName('preview');
  Array.from(previews).forEach((element)=>{
      element.innerHTML=element.innerText;
  })

/*
function searchFun(){
    let searchtxt = document.getElementById("searchTxt").value.toUpperCase();
    let table = document.getElementsByClassName('homediv');
    let jumbo = document.getElementsByClassName('jumbotron'); 
    let postcon = document.getElementsByClassName('postcon'); 
    let desc = document.getElementsByClassName('desc');  
    let i, desctxt;
    for(i=0;i<desc.length;i++){
         desctxt = desc[i].textContent.toUpperCase();

         if(desctxt)
         {
            if(desctxt.indexOf(searchtxt) > -1)
            {
               jumbo[i].style.display = "block"; 
            }
            else
            {
                jumbo[i].style.display = "none"; 
            }
         }

    }
    
}
*/
