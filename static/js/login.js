const roleSelect = document.getElementById('role');
const emailContainer = document.getElementById('emailContainer');
const emailUser = document.getElementById('emailUser');
const emailDomain = document.getElementById('emailDomain');
const loginForm = document.getElementById('loginForm');

emailContainer.classList.add('hidden');
emailUser.value = '';
emailUser.placeholder = '';
emailDomain.textContent = '';

roleSelect.addEventListener('change', () => {
    if (!roleSelect.value) {
        emailContainer.classList.add('hidden');
        emailUser.value = '';
        emailUser.placeholder = '';
        emailDomain.textContent = '';
    } else {
        emailContainer.classList.remove('hidden'); // mostra a caixa
        emailUser.value = '';
        emailUser.placeholder = 'Digite seu usuário';
        if (roleSelect.value === 'mestre') {
            emailDomain.textContent = '@ifpb.edu.br';
        } else if (roleSelect.value === 'aluno') {
            emailDomain.textContent = '@academico.ifpb.edu.br';
        }
    }
});

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
