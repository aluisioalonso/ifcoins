function validarLogin(event) {
    event.preventDefault();

    const usuario = document.getElementById("usuario").value.trim();
    const senha = document.getElementById("senha").value.trim();
    const mensagemErro = document.getElementById("mensagem-erro");

    // Exemplo de login fixo (ajuste no backend depois)
    if (usuario === "admin" && senha === "1234") {
        mensagemErro.classList.add("hidden");
        // Redireciona para o painel administrativo
        window.location.href = "/adm/admin";
    } else {
        mensagemErro.classList.remove("hidden");
    }
}
