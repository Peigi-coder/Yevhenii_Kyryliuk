const API = 'http://127.0.0.1:5000/api';
<small>${b.published_date || '-'} | ${b.pages} stron</small><br>
<button onclick="editBook(${b.id})">Edytuj</button>
<button onclick="deleteBook(${b.id})">Usuń</button>`;
root.appendChild(div);
});
}


async function saveBook(){
const id = document.getElementById('bookId').value;
const payload = {
title: document.getElementById('title').value,
author: document.getElementById('author').value,
published_date: document.getElementById('published_date').value || null,
pages: parseInt(document.getElementById('pages').value || 0)
genre: document.getElementById('genre').value || '',
rating: parseFloat(document.getElementById('rating').value || 0)
};
if(!payload.title || !payload.author){alert('Wpisz tytuł i autora');return;}
if(id){await fetch(`${API}/books/${id}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});}
else {await fetch(`${API}/books`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});}
clearForm();
loadBooks();
}


async function deleteBook(id){
if(confirm('Usunąć książkę?')){
await fetch(`${API}/books/${id}`,{method:'DELETE'});
loadBooks();
}
}


async function editBook(id){
const res = await fetch(`${API}/books/${id}`);
const b = await res.json();
document.getElementById('bookId').value = b.id;
document.getElementById('title').value = b.title;
document.getElementById('author').value = b.author;
document.getElementById('published_date').value = b.published_date || '';
document.getElementById('pages').value = b.pages;
document.getElementById('genre').value = b.genre || '';
document.getElementById('rating').value = b.rating || '';
}


function clearForm(){
document.getElementById('bookId').value = '';
document.getElementById('title').value = '';
document.getElementById('author').value = '';
document.getElementById('published_date').value = '';
document.getElementById('pages').value = '';
document.getElementById('genre').value = '';
document.getElementById('rating').value = '';
}


document.getElementById('saveBtn').addEventListener('click', saveBook);
document.getElementById('clearBtn').addEventListener('click', clearForm);
window.addEventListener('load', loadBooks);
