"use strict";
function helloworld() {
  let hello = "Hello world";
  alert(hello);
}
function data_analysis(url,data){
    let xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.onreadystatechange = function(){
   if (xhr.readyState==4 && xhr.status==200)

      alert("такс, ответ с сервера: "+ xhr.response.user)
   }
    xhr.open('GET', url,true);
    xhr.send("hi server");
}