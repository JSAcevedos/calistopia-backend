//ANIMACION BOTON MENU
document.querySelector(".menu__hamburguesa").addEventListener("click", animacionBarrasMenu);

var line1__barra = document.querySelector(".line1__menu-hamburguesa");
var line2__barra = document.querySelector(".line2__menu-hamburguesa");
var line3__barra = document.querySelector(".line3__menu-hamburguesa");
var aside = document.querySelector(".menuLateral");

function animacionBarrasMenu(){
    line1__barra.classList.toggle("activeline1__menu-hamburguesa");
    line2__barra.classList.toggle("activeline2__menu-hamburguesa");
    line3__barra.classList.toggle("activeline3__menu-hamburguesa");
}

//ABRIR - CERRAR MENU
const $openClose = document.getElementById("open-close"),
    $aside = document.getElementById("aside");

$openClose.addEventListener("click",()=>{
    $aside.classList.toggle("desplegar");
})
