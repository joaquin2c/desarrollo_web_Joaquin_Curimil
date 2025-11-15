function getFecha(fecha){
    let newDate = new Date(fecha);
    let newFormat=newDate.toISOString().split('T')[0];
    return newFormat
}

function getNota(nota){
    if(nota==0)
        return "-"
    else
        return parseFloat(nota.toFixed(2));
}

function show_evals(id){
    openModal(id);
    sessionStorage.setItem("id_aviso", id);
}

function getCTE(cantidad,tipo,edad,um){
    let new_tipo=tipo;
    let newUm;
    let extra;
    if(cantidad>1){
        new_tipo=new_tipo+"s"
    }

    if(um=="a"){
        newUm="año";
        extra="s";
    }
    else{
        newUm="mes";
        extra="es";
    }

    if(edad>1){
        newUm=newUm+extra
    }
    return cantidad+" "+new_tipo+" "+edad+" "+newUm;
}


async function getAvisos(id) {
    const url="http://localhost:8080/avisos/all";
    const nota=document.getElementById(`nota${id}`);
    let prev_nota=0;
    if (nota)
        prev_nota=nota.innerText;
    try{
        const response=await fetch(url);
        if(!response.ok){
            throw new Error("Response status :${response.status}");
        }

        const obj = await response.json();

        const table =document.getElementById("tablaAvisos");
        if(obj.length >0){
            const myElement =document.getElementById("listaAvisos");
            myElement.style.display="flex";
            table.innerHTML="";
        }
        let filas= "<tr>\n"+
                "   <td><b>ID</b></td>\n"+
                "   <td><b>Fecha <br> Publicación</b></td>\n"+
                "   <td><b>Sector</b></td>\n"+
                "   <td><b>Cantidad Tipo <br>Edad</b></td>\n"+
                "   <td><b>Comuna</b></td>\n"+
                "   <td><b>Nota</b></td>\n"+
                "   <td></td>\n"+
                "   </tr>"
        for(let i=0;i<obj.length;i++){
            filas= filas + 
                    "<tr><td>"+obj[i].id+
                    "</td><td>"+getFecha(obj[i].fechaIngreso)+
                    "</td><td>"+obj[i].sector+
                    "</td><td>"+getCTE(obj[i].cantidad,obj[i].tipo,obj[i].edad,obj[i].unidadMedida)+
                    "</td><td>"+obj[i].comuna+"</td><td id='nota"+obj[i].id+"'>"+
                    getNota(obj[i].nota)+"</td><td>"+ 
                    "<button onclick=show_evals("+obj[i].id+")>Evaluar</button>"+"</td></tr>"
        }
        table.innerHTML=filas;
    } catch(error){
        console.log(error.message);
    }

    if(nota){
        const nota=document.getElementById(`nota${id}`);
        post_nota=nota.innerText;
        if(post_nota>prev_nota){
            console.log("aumento");
            nota.className="inc-nota";
        }
        else if(post_nota<prev_nota){
            console.log("disminuir");
            nota.className="dec-nota"
        }
        else{
            console.log("mantener");
            nota.className="stay-nota"
        }

    }
}

async function agregarNota(nota,aviso_id){
    const response=await fetch("http://localhost:8080/post-nota",{
        method:"POST",
        headers:{
            "Content-Type":"application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({nota:nota,aviso_id:aviso_id})
    });
    if(!response.ok){
        throw new Error(`POST Response status: ${response.status}`);
    }     
    getAvisos(aviso_id);
}

function paintStars(stars,max){
    for (let i = 0; i < max+1; i++)
        stars[i].style.color="rgba(245, 194, 28, 1)";

    for (let i = max+1; i < 7; i++)
        stars[i].style.color="rgba(58, 58, 58, 0.25)";
}

document.addEventListener("DOMContentLoaded",function(){
    getAvisos(-1);
});
for (let i = 0; i < 7; i++) {
    stars[i].addEventListener("mouseover",function(){
        paintStars(stars,i);
    })

    stars[i].addEventListener("click",function(){
        const id_aviso = sessionStorage.getItem('id_aviso');
        modal.style.display = "none";
        agregarNota(i+1,id_aviso);
        paintBlackStars(stars)
    })
};
