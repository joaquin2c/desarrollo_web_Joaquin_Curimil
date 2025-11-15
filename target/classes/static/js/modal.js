let modal = document.getElementById("modal");

// Get the <span> element that closes the modal
let span = document.getElementsByClassName("close")[0];
let id_aviso = document.getElementById("id_aviso");

let stars=[]
for(let i = 1; i < 8; i++) {
    stars.push(document.getElementById(`star${i}`));
}

function paintBlackStars(stars){
    for (let i = 0; i < 7; i++)
        stars[i].style.color="rgba(58, 58, 58, 0.25)";
}

const openModal = (id) => {
  modal.style.display = "block";
  id_aviso.innerHTML=id;

}

// When the user clicks on <span> (x), close the modal
span.onclick = () => {
  paintBlackStars(stars);
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
modal.onclick = (event) => {
  if (event.target == modal) {
    paintBlackStars(stars);
    modal.style.display = "none";
  }
}