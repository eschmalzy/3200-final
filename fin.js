var applyButton = document.getElementById('apply-button');
var name = document.getElementById('name').value;
var age = document.getElementById('age').value;
var guest = document.getElementById('guest').value;
var dayOfWeek = new Date().getDay();

applyButton.onclick = function (){
  sendTicket(function(){
    document.getElementById('name').value = "";
    document.getElementById('age').value = "";
    document.getElementById('guest').value = "";
    getNewestTicket();
  },function() {
    alert("Unable to send ticket.")
  });
}

function printTickets(ticket){
  var lst = document.getElementById('ticket-list');
  var c = document.querySelector("#ticket");
  li = c.content.querySelectorAll("li");
  li[0].innerHTML = "Name: "+ticket['name']+"</br>Age: "+ticket['age']+"</br>Guest: "+ticket['guest'];
  console.log(ticket["token"]);
  if(ticket["token"] == dayOfWeek){
    li[0].style.backgroundColor = "#FFD700";
  } else{
    li[0].style.backgroundColor = "#fff";
  }
  var clone = document.importNode(c.content, true);
  lst.appendChild(clone);
}

var sendTicket = function(success, failure){
  var post = new XMLHttpRequest();
    post.onreadystatechange = function (){
      if (post.readyState == XMLHttpRequest.DONE){
        if (post.status == 403){
          alert("The Oompa Loompas have already received your ticket. Please try again tomorrow.");
        } else if (post.status >= 200 && post.status < 400) {
          success();
        } else {
          failure();
        }
      }
    };
    var name = document.getElementById('name').value;
    var age = document.getElementById('age').value;
    var guest = document.getElementById('guest').value;
  post.open("POST", "http://localhost:8080/tickets");
  post.withCredentials = true;
  post.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  post.send("name="+name+"&age="+age+"&guest="+guest);
};

var getNewestTicket = function(){
  var request = new XMLHttpRequest();
  request.onreadystatechange = function (){
    if (request.readyState == XMLHttpRequest.DONE){
      if (request.status >= 200 && request.status < 400) {
        tickets = JSON.parse(request.responseText);
        printTickets(tickets[tickets.length - 1]);
      } else {
        console.error("Couldn't load tickets!");
      }
    }
  };

request.open("GET", "http://localhost:8080/tickets");
request.withCredentials = true;
request.send();
}

//on page load populate the list
  var request = new XMLHttpRequest();
  request.onreadystatechange = function (){
    if (request.readyState == XMLHttpRequest.DONE){
      if (request.status >= 200 && request.status < 400) {
        tickets = JSON.parse(request.responseText);
        for (var i = 0, len = tickets.length; i <len; i++){
          printTickets(tickets[i]);
        }
      } else {
        console.error("Couldn't load tickets!");
      }
    }
  };
request.open("GET", "http://localhost:8080/tickets");
request.withCredentials = true;
request.send();
