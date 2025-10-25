"use strict";


let show_comments = (comments_response) =>{
  
  let comments_div = document.getElementById("comment-list");
  while (comments_div.firstChild) {
    comments_div.removeChild(comments_div.firstChild);
  }
  let botones_comment = document.getElementById("botones-comment");
  if (comments_response.length === 0) {
    let no_comment = document.createElement("h3");
    no_comment.innerText = "No hay comentarios, se el primero en comentar.";
    no_comment.className = "intro";
    comments_div.style.justifyContent = 'center';
    comments_div.appendChild(no_comment);
    sessionStorage.setItem("size_db",1);
    sessionStorage.setItem("page",1);
    botones_comment.hidden=true;
    botones_comment.style.display="none";
    return;
  }
  botones_comment.hidden=false;
    botones_comment.style.display="flex";
  let page_comment = document.getElementById("page-comment");
  let comentarios=comments_response["comentarios"]
  sessionStorage.setItem("size_db",comments_response["size_db"]);
  let ul = document.createElement("ul");
  comentarios.forEach(comment => {
    let li = document.createElement("li");
    let container = document.createElement("div");
    let nombre_div = document.createElement("div");
    let texto_div = document.createElement("div");
    let fecha_div = document.createElement("div");
    container.className = "list-container";
    nombre_div.className = "list-name";
    texto_div.className = "list-com";
    fecha_div.className = "list-fecha";
    nombre_div.innerText = comment["nombre"];
    fecha_div.innerText = comment["fecha"];
    texto_div.innerText = comment["texto"];
    container.append(nombre_div);
    container.append(fecha_div);
    container.append(texto_div);
    li.append(container);
    ul.append(li);
  });
  page_comment.innerText = ` ${sessionStorage.getItem("page")} / ${sessionStorage.getItem("size_db")}`;
  comments_div.appendChild(ul);
};


let fetchUrl = (url,function_show) => {
  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((jsonResponse) => { 
      function_show(jsonResponse["data"]); 
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      );
    });
};

let fetchSendComment = (url,comment_dict) => {
  fetch(url,{
    method:"POST",
    headers:{
      "Content-Type":"application/json"
    },
    body:JSON.stringify(comment_dict)
  })
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then((jsonResponse) => { 
    if(jsonResponse["valid"]){
      sendmessage(document.getElementById("comment-msg-send"),jsonResponse["time"]);
      
      //window.location.reload();;
    }
    else{
      errormessage(document.getElementById("comment-msg-send"),jsonResponse["error"]);
    }
  })
  .catch((error) => {
    console.error(
      "There has been a problem with your fetch operation:",
      error
    );
  });
};


let get_comentarios = () => {
  var id_value = window.location.pathname.split('/').at(-1);
  let page = sessionStorage.getItem("page");
  fetchUrl(`/get-comentarios/?id=${id_value}&page=${page}`,show_comments);
};


let errormessage = (comments_msg,invalidInputs) => {
  comments_msg.innerText = "Comentario no publicado.";
  comments_msg.className = "error";
  comments_msg.hidden=false;
  for (let input of invalidInputs) {
    let listElement = document.createElement("li");
    listElement.innerText = input;
    comments_msg.append(listElement);
  }
}

let sendmessage = (comments_msg,time) => {
  comments_msg.innerText = `Comentario publicado a las ${time}.`;
  comments_msg.className = "send";
  comments_msg.hidden=false;

  document.getElementById("new_comment-btn").disabled=true;
  setTimeout(() => {
    comments_msg.hidden=true;
    document.getElementById("new_comment").value = "";
    document.getElementById("new_comment_name").value = "";
    document.getElementById("new_comment-btn").disabled=false;
    let page = sessionStorage.getItem("page");
    get_comentarios(page)
  }, 2000);
}

const validateName = (name) => {
  if(!name) return false;
  let lengthValidmin = name.trim().length >= 3;
  let lengthValidmax = name.trim().length <= 80;
  
  return lengthValidmin && lengthValidmax;
}

const validateComment = (comment) => {
  if (!comment) return false;
  let lengthValidmin = comment.trim().length >= 5;
  let lengthValidmax = comment.trim().length <= 300;
  return lengthValidmin && lengthValidmax;
}

const validateForm = () => {
  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  }
  let name_input = document.getElementById("new_comment_name").value;
  let comment_input = document.getElementById("new_comment").value;
  if (!validateName(name_input)) {
    setInvalidInput("Error con el nombre.");
  }

  if (!validateComment(comment_input)) {
    setInvalidInput("Error con el comentario.");
  }

  let comments_msg = document.getElementById("comment-msg-send");
  //let msg = document.createElement("h3");
  if (!isValid) {
    errormessage(comments_msg,invalidInputs);
  }
  else{
    comments_msg.innerText = "Publicando comentario.";
    comments_msg.className = "wait";
    var id_value = window.location.pathname.split('/').at(-1);
    fetchSendComment("/post-comentario",{"name":name_input,"comment":comment_input,"aviso_id":id_value});
  }
}


const ChangePageComment =(plus) => {
    let newpage = Number(sessionStorage.getItem("page"))+plus;
    let sizedb = Number(sessionStorage.getItem("size_db"));
    if (newpage < 1 || newpage>sizedb){
      return;
    }
    sessionStorage.setItem("page",newpage);
    get_comentarios()
  } 



document.getElementById("new_comment-btn").addEventListener("click", validateForm);
sessionStorage.setItem("page",1);
get_comentarios();