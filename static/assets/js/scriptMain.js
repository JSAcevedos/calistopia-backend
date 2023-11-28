// FILTRO EJERCICIOS

const filterButton = document.querySelector('.filter__form');
const exerciseList = document.querySelector('.grid');

filterButton.addEventListener('submit', e => {
    e.preventDefault();

    const name = document.querySelector('.filter__form__name');
    const group = document.querySelector('.filter__form__group');
    const level = document.querySelector('.filter__form__level');
    const search = [name.value, group.value, level.value];

    Array.from(exerciseList.children)
    .filter( item => {
        return search.every(i => item.className.toLowerCase().includes(i.toLowerCase()));
    })
    .forEach(
        result => {
            result.classList.remove('hidden');
        }
    );

    Array.from(exerciseList.children)
    .filter( item => {
        return !search.every(i => item.className.toLowerCase().includes(i.toLowerCase()));
    })
    .forEach(
        result => {
            result.classList.add('hidden');
        }
    );
    
});