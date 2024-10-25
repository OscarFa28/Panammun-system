document.getElementById('user-form').addEventListener('submit', function(event) {
    var password = document.getElementById('password').value;
    var password2 = document.getElementById('password2').value;
    if (password !== password2) {
        alert('Las contraseñas no coinciden');
        event.preventDefault();
    }
});
function getCSRFToken() {
    return window.csrfToken; 
  }

const form = document.getElementById('user-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            });

            if (!response.ok) {
              const result = await response.json();
              
              Swal.fire({
                  icon: 'error',
                  title: 'Error',
                  text: Object.values(result).flat().join(', ') || 'Hubo un problema al procesar tu solicitud.',
                  confirmButtonColor: 'var(--primary-100)',
                  color: 'var(--text-100)',
                  background: 'var(--bg-100)',
              });
              return;
          }

            const result = await response.json();
            
            
            Swal.fire({
                icon: 'success',
                title: 'Éxito',
                text: 'Se ha registrado.',
                confirmButtonColor: 'var(--primary-100)',
                color: 'var(--text-100)',
                background: 'var(--bg-100)',
            }).then(() => {
                window.location.href = '/login/';
            });

        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error.message || 'Hubo un problema al procesar tu solicitud.',
                confirmButtonColor: 'var(--primary-100)',
                color: 'var(--text-100)',
                background: 'var(--bg-100)',
            });
        }
      });