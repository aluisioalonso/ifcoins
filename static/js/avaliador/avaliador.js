document.addEventListener("DOMContentLoaded", () => {
  const btnOpen = document.getElementById("open-profile");
  const modal = document.getElementById("modal-perfil");
  const btnClose = document.getElementById("close-modal");

  if (btnOpen) {
    btnOpen.addEventListener("click", () => {
      modal.classList.remove("hidden");
    });
  }

  if (btnClose) {
    btnClose.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }

  // Fecha o modal se clicar fora dele
  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.add("hidden");
    }
  });
});
