document.addEventListener('DOMContentLoaded', () => {
    const aprovarLinks = document.querySelectorAll('a.aprovar');
    aprovarLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const nome = link.parentElement.textContent.split('-')[0].trim();
            if (confirm(`Deseja aprovar o mestre ${nome}?`)) {
                window.location.href = link.href;
            }
        });
    });

    const rejeitarLinks = document.querySelectorAll('a.rejeitar');
    rejeitarLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const nome = link.parentElement.textContent.split('-')[0].trim();
            if (confirm(`Deseja rejeitar o mestre ${nome}?`)) {
                window.location.href = link.href;
            }
        });
    });
});
