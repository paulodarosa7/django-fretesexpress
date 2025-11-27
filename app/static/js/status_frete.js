// ======================================================
// CONFIGURAÇÃO DO MAPBOX
// ======================================================
const MAPBOX_TOKEN = 'pk.eyJ1Ijoid3Vlc2xleW1heCIsImEiOiJjbWk4MmFxZnYwN210Mmxvc2Y4b25kaDdkIn0.KlU45qR_UwafsiKxPy2y_A';

// ======================================================
// PEGA OS ENDEREÇOS DO TEMPLATE DJANGO (JÁ RENDERIZADOS)
// ======================================================
const enderecoColeta = JSON.parse(document.getElementById("endereco-coleta").textContent);
const enderecoEntrega = JSON.parse(document.getElementById("endereco-entrega").textContent);

// ======================================================
// FUNÇÃO PARA PEGAR LAT/LONG COM MAPBOX GEOCODING
// ======================================================
async function buscarCoordenadas(endereco) {
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(
        endereco
    )}.json?country=br&limit=1&access_token=${MAPBOX_TOKEN}`;

    const res = await fetch(url);
    const data = await res.json();

    if (!data.features || data.features.length === 0) {
        console.error("Endereço não encontrado:", endereco);
        return null;
    }

    const [lng, lat] = data.features[0].center;

    return { lat, lng };
}

// ======================================================
// INICIALIZA O MAPA E A ROTA
// ======================================================
async function iniciarMapa() {

    // 1) Geocodifica os endereços
    const origem = await buscarCoordenadas(enderecoColeta);
    const destino = await buscarCoordenadas(enderecoEntrega);

    if (!origem || !destino) {
        alert("Não foi possível localizar os endereços no mapa.");
        return;
    }

    // 2) Inicializa o mapa centralizado entre os dois pontos
    const map = L.map("map", { zoomControl: false }).setView([origem.lat, origem.lng], 13);

    // 3) Camada do mapa
      L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
        attribution: "&copy; OpenStreetMap contributors &copy; CARTO",
        subdomains: "abcd",
        maxZoom: 20
    }).addTo(map);

                // colocar o icone de localização padrao do app
                    const userIcon = L.divIcon({
                    className: "icone-localizacao",
                    iconSize: [32, 32],
                    iconAnchor: [16, 16]
                    });


    // 4) Renderiza a rota com OSRM
    var rota = L.Routing.control({
        waypoints: [
            L.latLng(origem.lat, origem.lng),
            L.latLng(destino.lat, destino.lng)
        ],
        router: L.Routing.osrmv1({
            serviceUrl: "https://router.project-osrm.org/route/v1" // servidor gratuito OSRM
        }),
        lineOptions: {
            styles: [
                { color: "#ffc400", weight: 6, opacity: 1 }
            ]
        },
        createMarker: function (i, waypoint) {
            return L.marker(waypoint.latLng, { icon: userIcon }).bindPopup(
                i === 0 ? "📍 Origem" : "🏁 Destino"
            );
        },
        addWaypoints: false,
        draggableWaypoints: false
    }).addTo(map);

    
rota.on('routesfound', function(e) {
    var summary = e.routes[0].summary;
    const distanciaKm = summary.totalDistance / 1000;
    const tempoMin = Math.round(summary.totalTime % 3600 / 60);
    const custo = distanciaKm * 2;

    // Atualiza na página
    document.getElementById('distancia').textContent = `Distância: ${distanciaKm.toFixed(2)} km`;
    document.getElementById('tempo').textContent = `Tempo: ${tempoMin} minutos`;
    document.getElementById('custo').textContent = `Custo: R$ ${custo.toFixed(2)}`;

    // Envia para o Django
    fetch(`/frete/${freteId}/salvar-rota/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') 
        },
        body: JSON.stringify({
            origem: '{{ frete.endereco_coleta }}',
            destino: '{{ frete.endereco_entrega }}',
            distancia: distanciaKm.toFixed(2),
            custo: custo.toFixed(2),
            tempoMinutos: tempoMin
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            console.log('Rota salva no banco!');
        } else {
            console.error('Erro ao salvar rota:', data.error);
        }
    });
});

// Executa ao abrir a página
iniciarMapa();
