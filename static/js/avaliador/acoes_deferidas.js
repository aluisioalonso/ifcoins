// Menu Principal JS

// Modal do perfil
const modal = document.getElementById('profile-modal');
const openBtn = document.getElementById('open-profile');
const closeBtn = document.getElementById('close-profile');

// Lógica para abrir e fechar o modal do perfil
openBtn.addEventListener('click', () => modal.classList.remove('hidden'));
closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

// A navegação para 'ações enviadas' e 'ações deferidas'
// FOI REMOVIDA daqui e colocada diretamente no HTML usando a tag <a>.