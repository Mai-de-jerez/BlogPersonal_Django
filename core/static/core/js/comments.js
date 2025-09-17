// comments/static/comments/js/comments.js

document.addEventListener('DOMContentLoaded', () => {
    // Seleccionamos todos los botones de respuesta
    const replyButtons = document.querySelectorAll('.reply-button');

    replyButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();

            // Escondemos todos los formularios de respuesta que puedan estar abiertos
            document.querySelectorAll('.reply-form').forEach(form => {
                form.style.display = 'none';
            });

            // Buscamos el elemento `<li>` que contiene el comentario actual
            const commentItem = e.target.closest('li.comment');           
            // Buscamos el formulario de respuesta dentro de ese elemento `<li>`
            const replyForm = commentItem.querySelector('.reply-form');
            const commentButtons = commentItem.querySelector('.comment-buttons');
            
            // Si encontramos el formulario, lo mostramos y rellenamos los datos
            if (replyForm) {
                replyForm.style.display = 'block';

                if (commentButtons) {                // 
                    commentButtons.style.display = 'none';
                }

                // Obtenemos el ID y el autor del comentario padre
                const commentId = e.target.getAttribute('data-comment-id');
                const commentAuthorName = commentItem.querySelector('.comment-author .url').textContent;

                // Rellenamos el campo oculto con el ID del comentario padre
                const parentIdInput = replyForm.querySelector('.parent-id-input');
                if (parentIdInput) {
                    parentIdInput.value = commentId;
                }

                // Actualizamos el nombre del autor al que se está respondiendo
                const replyAuthorSpan = replyForm.querySelector('.reply-author');
                if (replyAuthorSpan) {
                    replyAuthorSpan.textContent = commentAuthorName;
                }

                // Enfocamos el campo de texto del formulario
                const textarea = replyForm.querySelector('textarea');
                if (textarea) {
                    textarea.focus();
                }
            }
        });
    });

    

    // Manejamos el botón de cancelar
    document.querySelectorAll('.cancel-reply').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const replyForm = e.target.closest('.reply-form');
            if (replyForm) {
                replyForm.style.display = 'none';
     

            // Volvemos a mostrar los botones del comentario correspondiente
            const commentItem = replyForm.closest('li.comment');
            const commentButtons = commentItem.querySelector('.comment-buttons');
            if (commentButtons) {
                commentButtons.style.display = 'block';
                }
            }
        });
    });

    // Maneja el clic en el enlace para enviar el formulario
    document.querySelectorAll('.submit-reply').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const form = e.target.closest('form');
            if (form) {
                form.submit();
            }
        });
    });
});
