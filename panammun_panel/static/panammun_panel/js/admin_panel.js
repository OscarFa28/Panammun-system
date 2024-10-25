function showVoucher(voucherUrl) {
    console.log("Voucher URL: ", voucherUrl);
    var popupWindow = window.open("", "VoucherPopup", "width=600,height=400,scrollbars=yes");
    
    if (popupWindow) {
        var htmlContent = `
            <!DOCTYPE html>
            <html>
            <head>
                <title>Comprobante</title>
                <style>
                    img {
                        max-width: 100%;
                        height: auto;
                    }
                </style>
            </head>
            <body>
                <img src="${voucherUrl}" alt="Comprobante">
            </body>
            </html>
        `;
        
        popupWindow.document.write(htmlContent);
        popupWindow.document.close();
    } else {
        alert("No se pudo abrir la ventana emergente. Por favor, verifica las configuraciones del navegador.");
    }
}
function getCSRFToken() {
    return window.csrfToken; 
}

const forms = document.querySelectorAll('.user-change'); 

forms.forEach((form) => {
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
                text: 'Actualizado.',
                confirmButtonColor: 'var(--primary-100)',
                color: 'var(--text-100)',
                background: 'var(--bg-100)',
            }).then(() => {
                window.location.reload(); 
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
});
