// Recuperar las preguntas de Local Storage
let preguntas = JSON.parse(localStorage.getItem('preguntas')) || [];

// Función para mostrar las preguntas existentes
function mostrarPreguntas() {
  const listaPreguntas = document.getElementById('preguntas-list');
  listaPreguntas.innerHTML = '';

  preguntas.forEach((pregunta) => {
    const li = document.createElement('li');
    li.textContent = `${pregunta.id}. ${pregunta.pregunta}`;

    // Agregar escala de calificación
    const escalaCalificacion = document.createElement('div');
    escalaCalificacion.classList.add('rating-scale');

    for (let i = 1; i <= 5; i++) {
      const radioInput = document.createElement('input');
      radioInput.type = 'radio';
      radioInput.name = `calificacion-${pregunta.id}`;
      radioInput.value = i;

      const labelInput = document.createElement('label');
      labelInput.textContent = i;
      labelInput.appendChild(radioInput);

      escalaCalificacion.appendChild(labelInput);
    }

    li.appendChild(escalaCalificacion);
    listaPreguntas.appendChild(li);
  });
}

// Escuchar mensajes de la ventana de administración
window.addEventListener('message', function(event) {
    mostrarPreguntas();
});

// Mostrar las preguntas iniciales
mostrarPreguntas();