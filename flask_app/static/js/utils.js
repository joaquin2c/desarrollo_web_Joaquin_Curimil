var actual_contact_number=1;
var amount_fotos=1;

const updateContacto = (contact_number) => {

  const id_label="contact"+contact_number;
  const id_select="select-contact"+contact_number;
  const contactoSelect = document.getElementById(id_select);
  const contactoLabel = document.getElementById(id_label);
  
  if (contactoSelect.value !== "") {
      contactoLabel.style.display = "block";
  } else {
      contactoLabel.style.display = "none";
  }
};



const updateContacto1 = () => updateContacto(1);
const updateContacto2 = () => updateContacto(2);
const updateContacto3 = () => updateContacto(3);
const updateContacto4 = () => updateContacto(4);
const updateContacto5 = () => updateContacto(5);


const addNewContact = () => {
  if (actual_contact_number<5){
    actual_contact_number+=1;
    const id_div_contacto="div-contact"+(actual_contact_number);
    const contactodiv = document.getElementById(id_div_contacto);
    contactodiv.style.display = "block";
  }
};

const addNewFoto = () => {
  if (amount_fotos<5){
    amount_fotos+=1;
    const id_div_foto="div-foto"+(amount_fotos);
    const fotodiv = document.getElementById(id_div_foto);
    fotodiv.style.display = "block";
  }
};

const getInfoRow = (row) => {
  const row_info=[];
  row.childNodes.forEach(rowdata => {
    if (rowdata.nodeName=="TD"){
      row_info.push(rowdata); 
    }
  });
  return row_info;
};


const zoomImg = (img) => {
  document.getElementById("foto-btn-foto-container").hidden = false;
  document.getElementById("foto-btn-foto-container").style.display = "grid";
  document.getElementById("body-list").style.backgroundColor = "black";
  document.getElementById("img-zoom").src = img.src;
  document.getElementById("row-data-container").hidden = true;
  document.getElementById("row-data-container").style.display = "none";
  if (img.src.split('/').pop()=="Dracula.jpeg"){
    let audio = new Audio('static/uploads/Dracula.mp3');
    audio.play();
  }

}



const listRowOpen = (row) => {
  const row_info=getInfoRow(row);
  document.getElementById("list_all").hidden = true;
  document.getElementById("row-data-container").hidden = false;
  document.getElementById("row-data-container").style.display = "flex";
  
  document.getElementById("fecha-pub").innerHTML=row_info[0].textContent;
  document.getElementById("fecha-ent").innerHTML=row_info[1].textContent;
  document.getElementById("comuna").innerHTML=row_info[2].textContent;
  document.getElementById("sector").innerHTML=row_info[3].textContent;
  document.getElementById("cte").innerHTML=row_info[4].textContent;
  document.getElementById("nombre-cont").innerHTML=row_info[5].textContent;
  document.getElementById("tot-foto").src=row_info[6].childNodes[0].src;
  return row_info;
};


const btnUnzoomImg = (id) => {
  window.location.href = `/listado/${id}`; 
  
}


const goToIndex =() => {
  window.location.assign("/")
}

const goToAviso =(id) => {
        window.location.href = `/listado/${id}`; 
    }

const goToImg =(id_aviso, id_img) => {
        window.location.href = `/listado/${id_aviso}/imgs?id=${id_img}`;
  }

    
