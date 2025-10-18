// Ações Enviadas JS (Dropdown Funcional)

const modal = document.getElementById('profile-modal');
const openBtn = document.getElementById('open-profile');
// Não precisamos mais do closeBtn, pois o menu fecha ao clicar fora/toggle.

// --- 1. Alterna o menu (abre/fecha) ao clicar no botão ---
if (openBtn && modal) {
    openBtn.addEventListener('click', (event) => {
        // Usa .toggle() para alternar entre mostrar/esconder
        modal.classList.toggle('hidden');
        // Impede que o clique no botão se propague e feche imediatamente (veja o item 2)
        event.stopPropagation();
        console.log("Botão Perfil Clicado! Classe 'hidden' alternada.");
    });

    // --- 2. Fecha o menu ao clicar em qualquer lugar fora dele (e do botão) ---
    document.addEventListener('click', (event) => {
        // Verifica se o clique foi dentro do contêiner do modal
        const isClickInsideModalContainer = modal.contains(event.target);

        // Se o menu está aberto E o clique não foi dentro do menu, feche-o.
        if (!isClickInsideModalContainer && !modal.classList.contains('hidden')) {
            modal.classList.add('hidden');
            console.log("Fechando dropdown: clique fora.");
        }
    });
} else {
    console.error("Erro: Elemento 'profile-modal' ou 'open-profile' não encontrado no DOM.");
}
// -----------------------------
// Dropdown de Perfil
// -----------------------------
const profileBtn = document.getElementById('open-profile');
const profileModal = document.getElementById('profile-modal');

if (profileBtn && profileModal) {
    // Abre ou fecha o dropdown ao clicar no botão
    profileBtn.addEventListener('click', () => {
        profileModal.classList.toggle('hidden');
    });

    // Fecha o dropdown ao clicar fora
    window.addEventListener('click', (e) => {
        if (!profileModal.contains(e.target) && e.target !== profileBtn) {
            profileModal.classList.add('hidden');
        }
    });
}
