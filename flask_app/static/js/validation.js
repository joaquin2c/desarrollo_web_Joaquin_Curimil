//LUGAR

const validateSelect = (select) => {
  if(!select) return false;
  return true
}


const validateSector = (sector) => {
  if (!sector) return true;
  let lengthValid = sector.trim().length <= 100;
  return lengthValid;
}


const validateName = (name) => {
  if(!name) return false;
  let lengthValidmin = name.trim().length >= 3 ;
  let lengthValidmax = name.trim().length <= 200  ;
  
  return lengthValidmin && lengthValidmax;
}

//CONTACTOS

const validateEmail = (email) => {
  if (!email) return false;
  let lengthValid = email.trim().length < 100;

  // validamos el formato
  let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
  let formatValid = re.test(email);

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return true;
  // validación de longitud
  let lengthValid = phoneNumber.trim().length >= 8;

  // validación de formato
  let re = /^\+\d{1,3}\.\d{8}$/;
  let formatValid = re.test(phoneNumber);

  return lengthValid && formatValid;
};

const validateRequiredContacto = (contactoInput) => {
  const data_select=contactoInput.children[1].value;
  if (!data_select) return false; // Validar que haya elegido un medio de contacto
  const data_input=contactoInput.children[2].value;
  if (!data_input) return false; //Validar que haya puesto información de contacto
  
  return validateContacto(data_input); //Validar tamaño input
};

const validateContacto = (contactoInput) => {
  let minLengthValid = contactoInput.trim().length >= 4;
  let maxLengthValid = contactoInput.trim().length <= 50;
  return minLengthValid && maxLengthValid;
};

const validateContactos = (contactos) => {
  if(actual_contact_number>5) return false; //Que no sean más de cinco contactos
  const all_contacts=Array.from(contactos.children);
  const required_contact=all_contacts[0];
  const optionals_contacts=all_contacts.slice(1,5);
  if (!validateRequiredContacto(required_contact))
    return false;
  for (const contact of optionals_contacts){
    const data_select=contact.children[1].value;
    const data_input=contact.children[2].value;
    if(data_select && !validateContacto(data_input)){//Si tiene algun medio opcional, debe agregar la
      return false;                                  //informacion correspondiente, o cambiarle a ninguna
    }
  }
  return true;
}


//INFO MASCOTA

const validateInteger = (entero) => {
  if(!entero) return false; //Que no este vacio
  const numEntero=Number(entero);
  if(!numEntero) return false; //Que sea Entero
  let valueValid = numEntero >= 1;
  return valueValid;
}



const validateFecha = (fecha) => {
  if(!fecha) return false;

  const num_fecha= new Date(fecha);
  if (num_fecha=="Invalid Date") return false; //Revisa si tiene formato de fecha
  
  const num_now= new Date(now);
  const dif_time=num_fecha.getTime()-num_now.getTime();
  let timeValid = dif_time >= 0;
  return timeValid;
}


const validateFoto = (file) => {
  // validación del número de archivos
  let lengthValid = 1 == file.length;
  
  // validación del tipo de archivo
  let typeValid = true;
  // el tipo de archivo debe ser "image/<foo>" o "application/pdf"
  for (const fileu of file) {
    let fileFamily = fileu.type.split("/")[0];
    typeValid &&= fileFamily == "image" || fileu.type == "application/pdf";
  }
  return lengthValid && typeValid;
}

const validateRequiredFoto = (file) => {
  if (file.length==0) return false;
  return validateFoto(file);
}

const validateOptionalFoto = (files) => {
  for (const file of files){
    if(file.length>0 && !validateFoto(file))
      return false;
  }
  return true;
}

// --- VALIDADORES ---
const validateForm = () => {

  let myForm = document.forms["formulario"];
  let regionInput = myForm["region"].value;
  let comunaInput = myForm["comuna"].value;
  let sectorInput = myForm["sector"].value;

  let nombreInput = myForm["nombre"].value;
  let emailInput = myForm["email"].value;
  let celularInput = myForm["celular"].value;
  let contactosInput = document.getElementById("div-contacts");
  
  let tipoInput = myForm["tipo"].value;
  let cantidadInput = myForm["cantidad"].value;
  let edadInput = myForm["edad"].value;
  let unidadInput = myForm["unidad"].value;
  let fechaInput = myForm["fecha"].value;
  let fotoInput1 = myForm["foto1"].files;
  let fotoInput2 = myForm["foto2"].files;
  let fotoInput3 = myForm["foto3"].files;
  let fotoInput4 = myForm["foto4"].files;
  let fotoInput5 = myForm["foto5"].files;

  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  //DONDE

  if (!validateSelect(regionInput)) {
    setInvalidInput("Region");
  }

  if (!validateSelect(comunaInput)) {
    setInvalidInput("Comuna");
  }

  if (!validateSector(sectorInput)) {
    setInvalidInput("Sector");
  }

  //CONTACTO
  if (!validateName(nombreInput)) {
    setInvalidInput("Nombre");
  }

  if (!validateEmail(emailInput)) {
    setInvalidInput("Email");
  }

  if (!validatePhoneNumber(celularInput)) {
    setInvalidInput("Celular");
  }
  
  if (!validateContactos(contactosInput)) {
    setInvalidInput("Contacto(s)");
  }
    
  //MASCOTA
  if (!validateSelect(tipoInput)) {
    setInvalidInput("Tipo de mascota  ");
  }

  if (!validateInteger(cantidadInput)) {
    setInvalidInput("Cantidad");
  }  

  if (!validateInteger(edadInput)) {
    setInvalidInput("Edad");
  }  

  if (!validateSelect(unidadInput)) {
    setInvalidInput("Unidad medida edad");
  }  
  
  if (!validateFecha(fechaInput)) {
    setInvalidInput("Fecha disponible para entrega");
  }  

  if (!validateRequiredFoto(fotoInput1)) {
    setInvalidInput("Foto");
  }  
  if (!validateOptionalFoto([fotoInput2,fotoInput3,fotoInput4,fotoInput5])) {
    setInvalidInput("Foto Opcionales");
  }  

  // finalmente mostrar la validación
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");

  if (!isValid) {
    validationListElem.textContent = "";
    // agregar elementos inválidos al elemento val-list.
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }
    // establecer val-msg
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    // aplicar estilos de error
    validationBox.style.backgroundColor = "#ffdddd";
    validationBox.style.borderLeftColor = "#f44336";

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  } else {
    /*
    // Ocultar el formulario
    myForm.style.display = "none";

    // establecer mensaje de éxito
    validationMessageElem.innerText = "¡Formulario válido! ¿Está seguro que desea agregar este aviso de adopción?";
    validationListElem.textContent = "";

    // aplicar estilos de éxito
    validationBox.style.backgroundColor = "#ddffdd";
    validationBox.style.borderLeftColor = "#4CAF50";

    // Agregar botones para enviar el formulario o volver
    let submitButton = document.createElement("button");
    submitButton.innerText = "Sí, estoy seguro";
    submitButton.style.marginRight = "10px";
    submitButton.addEventListener("click", () => {
      validationBox.hidden = true;
      document.getElementById("send-box").hidden = false;
      document.getElementById("intro").hidden = true; 
    });

    let backButton = document.createElement("button");
    backButton.innerText = "No, no estoy seguro, quiero volver al formulario";
    backButton.addEventListener("click", () => {
      // Mostrar el formulario nuevamente
      myForm.style.display = "block";
      validationBox.hidden = true;
    });

    validationListElem.appendChild(submitButton);
    validationListElem.appendChild(backButton);

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
    */   
    let loginForm = document.getElementById("new_aviso");
    loginForm.submit();

  }
};


const dateFormat = (fecha) => {
  const year = fecha.getFullYear();
  const month = (fecha.getMonth() + 1).toString().padStart(2, '0');
  const day = fecha.getDate().toString().padStart(2, '0');
  const hour = fecha.getHours().toString().padStart(2, '0');
  const minute = fecha.getMinutes().toString().padStart(2, '0');


  const avalible_time = `${year}-${month}-${day}T${hour}:${minute}`;
  return avalible_time;
}

const updateDate = () => {
  now.setHours(now.getHours() + 3); //3 horas extras
  now=dateFormat(now);
  let document_Date = document.getElementById('fecha');
  document_Date.value = now; //La fecha de prellenado es la actual más 3 horas. 
  document_Date.min = now; //La fecha no debe ser menor a la de prellenado. 
}

var now=new Date();