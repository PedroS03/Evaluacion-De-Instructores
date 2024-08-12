function validarSeleccionInstructor() {
    const instructorSeleccionado = document.querySelector('input[name="opcion"]:checked');
    if (instructorSeleccionado) {
      const idInstructor = instructorSeleccionado.id.replace('instructor', '');
      console.log(`¡Redireccionando al formulario de preguntas para el instructor ${idInstructor}!`);
      window.location.href = `preguntas.html?instructor=${idInstructor}`;
    } else {
      alert('Debe seleccionar un instructor para continuar.');
    }
  }
  