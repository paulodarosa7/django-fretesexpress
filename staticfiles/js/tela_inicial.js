document.addEventListener("deviceready", function() {

    // Pede permissão de localização (Android 6+)
    cordova.plugins.diagnostic.requestLocationAuthorization(function(status) {
        if (status === cordova.plugins.diagnostic.permissionStatus.GRANTED ||
            status === cordova.plugins.diagnostic.permissionStatus.GRANTED_WHEN_IN_USE) {

            console.log("Permissão concedida");

            // Inicializa mapa
            const map = L.map('map').setView([-24.9555, -53.4552], 5);

            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
                subdomains: 'abcd',
                maxZoom: 20
            }).addTo(map);

            // Ícone do usuário
            const ponto = L.divIcon({
                className: 'icone-localizacao',
                iconSize: [32, 32],
                iconAnchor: [16, 16]
            });

            let userMarker = null;

            // Atualiza posição do usuário
            function atualizarPosicao(position) {
                if (!position || !position.coords) return;

                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                if (!userMarker) {
                    userMarker = L.marker([lat, lon], { icon: ponto }).addTo(map);
                    map.setView([lat, lon], 16); // centraliza apenas na primeira vez
                    console.log("Marcador criado");
                } else {
                    userMarker.setLatLng([lat, lon]);
                }
            }

            // Tratamento de erro
            function erroPosicao(err) {
                if (err) {
                    console.error(`ERRO(${err.code}): ${err.message}`);
                } else {
                    console.error("Erro desconhecido ao tentar obter posição");
                }
            }

            // Verifica se geolocalização está disponível
            if (navigator.geolocation) {
               // Pegando posição rápida (aproximada)
                navigator.geolocation.getCurrentPosition(
                    function(pos) {
                        atualizarPosicao(pos); // marcador aparece rápido
                        // Agora começa a atualização contínua com alta precisão
                        navigator.geolocation.watchPosition(
                            atualizarPosicao,
                            erroPosicao,
                            { enableHighAccuracy: true, maximumAge: 0, timeout: 60000 } // 60s
                        );
                                            },
                    erroPosicao,
                    { enableHighAccuracy: false, maximumAge: 5000, timeout: 5000 }
                );
            } else {
                alert("Geolocalização não é suportada por este dispositivo.");
            }

        } else {
            alert("Permissão de localização não concedida");
        }
    }, function(error) {
        console.error("Erro ao pedir permissão: " + error);
    });

}, false);