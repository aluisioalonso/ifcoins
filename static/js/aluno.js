document.getElementById('acaoForm').addEventListener('submit', function(e) {
    const descricao = document.getElementById('descricao').value;
    if (!descricao) {
        e.preventDefault();
        alert("Selecione uma ação antes de enviar.");
    }
});
