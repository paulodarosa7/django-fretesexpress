document.addEventListener("DOMContentLoaded", () => {

    const map = L.map('map', { zoomControl: false }).setView([-24.9555, -53.4552], 5);
    L.control.zoom({ position: 'topright' }).addTo(map);


    L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
        attribution: "&copy; OpenStreetMap contributors &copy; CARTO",
        subdomains: "abcd",
        maxZoom: 20
    }).addTo(map);

    const userIcon = L.divIcon({
        className: "icone-localizacao",
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    });

    let userMarker = null;
    let jaCentralizou = false;

    function atualizarPosicao(position) {
        if (!position?.coords) return;

        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        if (!userMarker) {
            userMarker = L.marker([lat, lon], { icon: userIcon }).addTo(map);
        } else {
            userMarker.setLatLng([lat, lon]);
        }

        if (!jaCentralizou) {
            map.setView([lat, lon], 16);
            jaCentralizou = true;
        }
    }

    function erroPosicao(error) {
        console.warn("Erro ao obter localização:", error.message);
    }

    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            pos => {
                atualizarPosicao(pos);

                navigator.geolocation.watchPosition(
                    atualizarPosicao,
                    erroPosicao,
                    {
                        enableHighAccuracy: true,
                        timeout: 20000,
                        maximumAge: 0
                    }
                );
            },
            erroPosicao,
            {
                enableHighAccuracy: true,
                timeout: 8000,
                maximumAge: 3000
            }
        );
    } else {
        alert("Seu navegador não suporta geolocalização.");
    }
});
    