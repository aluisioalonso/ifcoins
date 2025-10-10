const forms = document.querySelectorAll('.aprovarForm');
forms.forEach(form => {
    form.addEventListener('submit', function(e){
        const valor = this.querySelector('input[name="valor"]').value;
        if (!valor || valor <= 0) {
            e.preventDefault();
            alert("Informe um valor de IFCONS válido.");
        }
    });
});

const rejeitarLinks = document.querySelectorAll('a.rejeitar');
rejeitarLinks.forEach(link => {
    link.addEventListener('click', function(e){
        e.preventDefault();
        if (confirm("Deseja realmente rejeitar essa ação?")) {
            window.location.href = link.href;
        }
    });
});
