const roleSelect = document.getElementById('role');
const emailContainer = document.getElementById('emailContainer');
const emailUser = document.getElementById('emailUser');
const emailDomain = document.getElementById('emailDomain');
const loginForm = document.getElementById('loginForm');

emailUser.value = '';
emailUser.placeholder = '';


loginForm.addEventListener('submit', (e) => {
    if (!roleSelect.value) {
        e.preventDefault();
        alert('Selecione seu perfil antes de preencher o e-mail.');
        roleSelect.focus();
        return;
    }
    if (!emailUser.value) {
        e.preventDefault();
        alert('Digite o nome do usuário antes do domínio.');
        emailUser.focus();
        return;
    }
    const fullEmail = emailUser.value + emailDomain.textContent;
    console.log('E-mail completo:', fullEmail);
});
