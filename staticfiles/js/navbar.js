// static/js/menu.js
(function () {
  function log(msg) {
    console.log('[navbar.js] ' + msg);
  }

  document.addEventListener('DOMContentLoaded', function () {
    const menuBtn = document.getElementById('menu-btn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('menu-overlay');
    const voltarBtn = document.getElementById('sidebar-back'); // <-- ADICIONADO

    log('DOM ready.');

    if (!menuBtn || !sidebar) {
      log('IDs não encontrados.');
      return;
    }

    // função de abrir/fechar
    function toggle() {
      const active = sidebar.classList.toggle('active');
      sidebar.setAttribute('aria-hidden', !active);

      if (overlay) {
        overlay.style.display = active ? 'block' : 'none';
        overlay.setAttribute('aria-hidden', !active);
      }

      // ---- NOVO: esconder/mostrar o hambúrguer ----
      menuBtn.style.display = active ? 'none' : 'block';

      log('toggle -> sidebar active=' + active);
    }

    menuBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      toggle();
    });

    // Clicar no overlay fecha
    if (overlay) {
      overlay.addEventListener('click', function () {
        sidebar.classList.remove('active');
        sidebar.setAttribute('aria-hidden', 'true');
        overlay.style.display = 'none';
        overlay.setAttribute('aria-hidden', 'true');

        // retorna o hambúrguer
        menuBtn.style.display = 'block';

        log('fechado via overlay');
      });
    }

    // Esc fecha
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && sidebar.classList.contains('active')) {
        sidebar.classList.remove('active');
        if (overlay) {
          overlay.style.display = 'none';
          overlay.setAttribute('aria-hidden', 'true');
        }

        // retorna o hambúrguer
        menuBtn.style.display = 'block';

        log('fechado via ESC');
      }
    });

    // NOVO: botão voltar fecha o menu
    if (voltarBtn) {
      voltarBtn.addEventListener('click', function () {
        sidebar.classList.remove('active');
        if (overlay) {
          overlay.style.display = 'none';
          overlay.setAttribute('aria-hidden', 'true');
        }

        // retorna o hambúrguer
        menuBtn.style.display = 'block';

        log('fechado via voltar');
      });
    }

    // Links dentro do menu fecham
    sidebar.addEventListener('click', function (e) {
      const target = e.target;
      if (target.tagName === 'A' || target.closest('a')) {
        sidebar.classList.remove('active');
        if (overlay) {
          overlay.style.display = 'none';
          overlay.setAttribute('aria-hidden', 'true');
        }

        // volta o hambúrguer
        menuBtn.style.display = 'block';

        log('fechado via clique em link');
      }
    });

    if (overlay) overlay.style.display = 'none';
  });
})();
