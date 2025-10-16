function confirmarAprovacao(event) {
    const confirmar = confirm("Deseja realmente aprovar este avaliador?");
    if (!confirmar) {
        event.preventDefault();
    }
}

function confirmarRejeicao(event) {
    const confirmar = confirm("Tem certeza que deseja rejeitar e excluir este avaliador?");
    if (!confirmar) {
        event.preventDefault();
    }
}
