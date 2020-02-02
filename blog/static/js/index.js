"use strict";
//метод работающий с представлением -  которое формирует запросы к бд и возвращает ответ
function data_analysis(form) {
  let url = "editor/result";
  let xhr = new XMLHttpRequest();
  let elem = document.getElementById("data_set");
  xhr.responseType = "json";
  alert(form.value);
  let i = 0;
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4 && xhr.status == 200)
      //elem.style.background = 'red';
      //alert("такс, ответ с сервера: "+ xhr.response.data);
      do {
        elem.innerHTML += xhr.response.data[i] + "<br>";
        i++;
      } while (xhr.response.data[i]);
  };

  xhr.open("GET", url, true);
  xhr.send("hi server");
}

//пустой метод для теста работы некоторых функций
function hello(user) {
  try {
    alert("цифра" + user);
  } catch (err) {
    alert("ok");
  }
}

//функция добавления книги в личную библиотеку
function add_to_basket(url) {
  url = document.location.pathname + "test_view";
  let xhr = new XMLHttpRequest();
  var formData = new FormData();
  formData.append("username", "johndoe");
  formData.append("id", 123456);
  //xhr.responseType = "json";
  xhr.responseType = "text";
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4 && xhr.status == 200) {
      alert("Добавлено в библиотеку");
    }
  };

  xhr.open("POST", url, true);
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  xhr.send(formData);
}

function getCookie(name) {
  // метод формирования csrf токена для защиты от межсайтовых запросов

  var cookieValue = null;
  var i = 0;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (i; i < cookies.length; i++) {
      var cookie = cookies[i];
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
var csrftoken = getCookie("csrftoken");

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}

function getсookie(name) {
  let matches = document.cookie.match(
    new RegExp(
      "(?:^|; )" +
        name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") +
        "=([^;]*)"
    )
  );
  return matches ? decodeURIComponent(matches[1]) : undefined;
}
