// Simulación de base de datos
let preguntas = [];

// Función para crear una pregunta
function crearPregunta(event) {
  event.preventDefault();
  const textoPregunta = document.getElementById('pregunta').value;

  const pregunta = {
    id: preguntas.length + 1,
    pregunta: textoPregunta,
    calificacion: [], // Nuevo campo para la escala de calificación
  };

  preguntas.push(pregunta);
  document.getElementById('pregunta').value = '';
  mostrarPreguntas();

  // Almacenar la pregunta en Local Storage
  localStorage.setItem('preguntas', JSON.stringify(preguntas));
}

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

// Cargar preguntas del Local Storage al iniciar la página
window.addEventListener('DOMContentLoaded', () => {
  const preguntasAlmacenadas = localStorage.getItem('preguntas');
  if (preguntasAlmacenadas) {
    preguntas = JSON.parse(preguntasAlmacenadas);
    mostrarPreguntas();
  }
});


// Función para actualizar una pregunta
function actualizarPregunta(event) {
    event.preventDefault();
    const id = document.getElementById('pregunta-id').value;
    const nuevaPregunta = document.getElementById('nueva-pregunta').value; // corrected typo
    const preguntaActualizada = preguntas.find((pregunta) => pregunta.id === parseInt(id));
    if (preguntaActualizada) {
        preguntaActualizada.pregunta = nuevaPregunta;
        document.getElementById('pregunta-id').value = '';
        document.getElementById('nueva-pregunta').value = ''; // corrected typo
        mostrarPreguntas();
    } else {
        alert('Pregunta no encontrada');
    }

    // Almacenar la pregunta en Local Storage
    localStorage.setItem('preguntas', JSON.stringify(preguntas))
}

// Función para eliminar una pregunta
function eliminarPregunta(event) {
    event.preventDefault();
    const id = document.getElementById('pregunta-id-eliminar').value;
    preguntas = preguntas.filter((pregunta) => pregunta.id !== parseInt(id));
    document.getElementById('pregunta-id-eliminar').value = '';
    mostrarPreguntas();

    // Almacenar la pregunta en Local Storage
    localStorage.setItem('preguntas', JSON.stringify(preguntas))
}

// Eventos de los formularios
document.getElementById('crear-pregunta-form').addEventListener('submit', crearPregunta);
document.getElementById('actualizar-pregunta-form').addEventListener('submit', actualizarPregunta);
document.getElementById('eliminar-pregunta-form').addEventListener('submit', eliminarPregunta);