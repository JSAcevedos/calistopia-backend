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

//ARRAY RUTINA 

const exercise = document.querySelectorAll('.ejercicio_catalogo');
const routine = document.querySelector('.ejercicio_rutina');
const routineCurrent = routine.cloneNode(true);
const routineId = routine.classList[1];
const routineTemp = document.querySelectorAll('.ejercicio_rutina_elemento');
const sendButton = document.querySelector('.ejercicio_rutina_button_modificar');
const currentTitle = document.querySelector('.ejercicio_rutina_input_titulo').getAttribute('value');
const loading = document.querySelector('.filter_h3');
let titles = [];
const characteristicsCurrent = document.querySelectorAll('.campo_ejercicio');
let descriptionCurrent = [];

characteristicsCurrent.forEach( item => {
    if(item.value){
        descriptionCurrent.push(item.value);
    }
});

routineTemp.forEach(child => {
    titles.push(child.children[0].children[2].children[0].textContent);
});

const generateElement = (imagen, nombre, grupo) => {

    let newElement = 
    `<div class="ejercicio_rutina_elemento">
        <div class="ejercicio ejercicio_layout">
            <a class="ejercicio_rutina_elemento_cerrar" href="">
                <img class="ejercicio__imagen_cerrar ${nombre} delete" src="https://cdn-icons-png.flaticon.com/128/6276/6276642.png" alt="imagen ejercicio">
            </a>
            <img class="ejercicio__imagen" src="${imagen}" alt="imagen ejercicio">
            <div class="ejercicio__informacion">
                <p class="ejercicio__nombre nombre_ejercicio_rutina">${nombre}</p>
                <p class="ejercicio__musculo">${grupo}</p>
            </div>
        </div>

        <div class="param_ejercicio">
            <div class="campo">
                <label class="campo_nombre_series">Series</label>
                <input class="campo_ejercicio" type="number" min="0" max="100" pattern="\d{1,3}" inputmode="numeric">
            </div>

            <div class="campo">
                <label>Repeticiones</label>
                <input class="campo_ejercicio" type="number" min="0" max="100" pattern="\d{1,3}" inputmode="numeric">
            </div>

            <div class="campo">
                <label class="campo_nombre_descanso">Descanso(Min)</label>
                <input class="campo_ejercicio" type="number" min="0" max="100" pattern="\d{1,3}" inputmode="numeric">
            </div>
        </div>
    </div>`;

    if (titles.includes(nombre)) {
        alert("Este ejercicio ya se encuentra en la rutina");
    } else {
        routine.innerHTML += newElement;
        titles.push(nombre);
    }

};


exercise.forEach((element) => {
    
    const button = element.children[1];
    const imagen = element.children[0].children[0].getAttribute('src');
    const nombre = element.children[0].children[1].children[0].textContent;
    const grupo = element.children[0].children[1].children[1].textContent;
    
    button.addEventListener('click', e => {
        generateElement(imagen, nombre, grupo);
    });
});

routine.addEventListener('click', e => {

    e.preventDefault();

    if(e.target.classList.contains('delete')) {
        e.target.parentElement.parentElement.parentElement.remove();
        const i = titles.indexOf(e.target.parentElement.parentElement.children[2].children[0].textContent);
        titles.splice(i, 1);
    }
});

sendButton.addEventListener('click', e => {

    const title = document.querySelector('.ejercicio_rutina_input_titulo');

    
    if(!title.value){
        return alert("Debes asignar un nombre a la rutina");
    }
    
    if(!titles[0]){
        return alert("Debes agregar ejercicios");
    }
    
    let characteristics = document.querySelectorAll('.campo_ejercicio');
    let description = [];
    
    characteristics.forEach( item => {
        if(item.value){
            description.push(item.value);
        }else{
            characteristics = [];
        }
    });
    
    if (!characteristics[0]){
        alert("Debes completar la información de todos los ejercicios");
        return;
    }

    const isEqual = JSON.stringify(description) == JSON.stringify(descriptionCurrent) && routine.isEqualNode(routineCurrent) && title.value == currentTitle;

    if(isEqual){
        alert('No has hecho cambios en tu rutina');
        return;
    }
    
    const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const requestObj = new XMLHttpRequest();
    requestObj.onreadystatechange = function () {
        if(this.readyState == 4 && this.status == 200){
            alert('Rutina modificada con exito!');
            loading.textContent = "Buscar por:";
            location.href=`/routines/${routineId}/`;
        }
    }

    requestObj.open("POST", '/routine/modify/'+routineId+'/');
    requestObj.setRequestHeader('X-CSRFToken', csrftoken);
    const formData = new FormData();
    formData.append('title',title.value);
    formData.append('routine',titles);
    formData.append('description',description);
    loading.textContent = "Cargando...";
    requestObj.send(formData);

})

