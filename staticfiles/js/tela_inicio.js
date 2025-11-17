const btnUsuario = document.getElementById("btnUsuario");
const btnMotorista = document.getElementById("btnMotorista");


btnUsuario.addEventListener("click", () => {
  btnUsuario.classList.add("active");
  btnMotorista.classList.remove("active");
  

  window.location.href = 'tela_user.html';

});

btnMotorista.addEventListener("click", () => {
  btnMotorista.classList.add("active");
  btnUsuario.classList.remove("active");


  window.location.href = 'tela_motorista.html';

});