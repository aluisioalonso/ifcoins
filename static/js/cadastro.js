const roleSelect = document.getElementById('role');
const emailContainer = document.getElementById('emailContainer');
const emailUser = document.getElementById('emailUser');
const emailDomain = document.getElementById('emailDomain');
const cadastroForm = document.getElementById('cadastroForm');

emailContainer.classList.add('hidden');

roleSelect.addEventListener('change', () => {
    if (!roleSelect.value) {
        emailContainer.classList.add('hidden');
    } else {
        emailContainer.classList.remove('hidden');
        if (roleSelect.value === 'mestre') {
            emailDomain.textContent = '@ifpb.edu.br';
        } else if (roleSelect.value === 'aluno') {
            emailDomain.textContent = '@academico.ifpb.edu.br';
        }
    }
});

cadastroForm.addEventListener('submit', (e) => {
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
    // Pode enviar fullEmail para o backend
});
