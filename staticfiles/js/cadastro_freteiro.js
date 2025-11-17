const btnContinuar = document.getElementById("btnContinuar");
const telaCadastro1 = document.getElementById("telaCadastro1");
const telaCadastro2 = document.getElementById("telaCadastro2");

telaCadastro2.classList.add("hidden");

btnContinuar.addEventListener("click", (e) => {
  e.preventDefault();

  // valida apenas os campos obrigatórios da tela 1
  const camposTela1 = telaCadastro1.querySelectorAll("input[required]");
  let valido = true;

  camposTela1.forEach((input) => {
    if (!input.checkValidity()) {
      input.reportValidity();
      valido = false;
    }
  });

  if (!valido) return;

  // se estiver tudo certo, muda de tela
  telaCadastro1.classList.add("hidden");
  telaCadastro2.classList.remove("hidden");
});