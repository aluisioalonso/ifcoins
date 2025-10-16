document.addEventListener('DOMContentLoaded', function() {
    // 1. OBTENÇÃO DOS ELEMENTOS PELO ID
    var modal = document.getElementById("modalCadastroAcao");
    var btnAbrir = document.getElementById("abrirModalCadastro");
    var btnFechar = document.getElementById("fecharModalCadastro");

    // ======================================================
    // 2. FUNÇÃO DE ABRIR A MODAL
    // ======================================================
    if (btnAbrir && modal) {
        btnAbrir.addEventListener('click', function() {
            // Define o display como 'block' para o CSS mostrar a modal
            modal.style.display = "block";
            // Tira o foco do botão após o clique para melhor UX
            this.blur();
        });
    }

    // ======================================================
    // 3. FUNÇÃO DE FECHAR A MODAL PELO 'X'
    // ======================================================
    if (btnFechar && modal) {
        btnFechar.addEventListener('click', function() {
            modal.style.display = "none";
        });
    }

    // ======================================================
    // 4. FUNÇÃO DE FECHAR A MODAL AO CLICAR FORA (WINDOW CLICK)
    // ======================================================
    window.addEventListener('click', function(event) {
        // Checa se o elemento clicado (event.target) é o fundo da modal
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    // Se a modal ainda não abrir, verifique no console do navegador (F12)
    // se o arquivo "menuacoes.js" está sendo carregado sem erros 404.
});

function confirmarexcluir() {
    const confirmar = confirm("Tem certeza que deseja excluir esta ação?");
    if (!confirmar){
        event.preventDefault();
    }


}
