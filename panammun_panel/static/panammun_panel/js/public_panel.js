function getCSRFToken() {
    return window.csrfToken; 
}
function selectCountry(country, commitee, id){
    Swal.fire({
        title: '¿Estás segur@?',
        text: `Vas a elegir ${country} de ${commitee}`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: 'var(--accent-100)',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Confirmar',
        background: 'var(--primary-100)',
        color: 'var(--bg-100)'

      }).then((result) => {
        if (result.isConfirmed) {
            selectC(id)
        }
      });
}
function selectC(id) {
    fetch('/selectCountry/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ id: id }),
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Error en la selección');
            });
        }
        return response.json();
    })
    .then(data => {
        Swal.fire({
            icon: 'success',
            title: '¡Éxito!',
            text: data.message || 'País asignado exitosamente.',
            background: 'var(--primary-100)',
            color: 'var(--bg-100)',
            confirmButtonColor: 'var(--accent-100)'
        }).then(() => {
            location.reload();
        });
    })
    .catch(error => {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: error.message,
            background: 'var(--primary-100)',
            color: 'var(--bg-100)',
            confirmButtonColor: 'var(--accent-100)'
        }).then(() => {
            location.reload();
        });
    });
}
