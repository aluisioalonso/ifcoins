// Menu Principal JS

// Modal do perfil
const modal = document.getElementById('profile-modal');
const openBtn = document.getElementById('open-profile');
const closeBtn = document.getElementById('close-profile');

openBtn.addEventListener('click', () => modal.classList.remove('hidden'));
closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

// Navegação para páginas de ações
document.getElementById('btn-enviadas').addEventListener('click', () => {
  window.location.href = 'acoes_enviadas.html';
});

document.getElementById('btn-deferidas').addEventListener('click', () => {
  window.location.href = 'acoes_deferidas.html';
});
#menu_principal.js