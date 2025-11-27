# 🚚 FretesExpress

O **FretesExpress** é um aplicativo híbrido desenvolvido para facilitar a conexão entre motoristas e clientes que precisam solicitar serviços de frete, de forma rápida, intuitiva e eficiente.

O aplicativo conta com uma interface maneira, simples e prática, permitindo que o usuário cadastre, visualize e gerencie pedidos de transporte diretamente pelo celular.

Além disso, o **FretesExpress** abre espaço para **MEIs, autônomos e profissionais independentes** que desejam oferecer serviços de transporte de cargas para outras pessoas, tornando o processo mais acessível e confiável.

---

## 📱 Tecnologias Utilizadas

_Removido por enquanto: Apache Cordova → para empacotar o código web em aplicativo mobile._
_Removido por enquanto: Android Studio → utilizado como emulador e ambiente de testes._

HTML5, CSS3 e JavaScript → responsáveis pela interface e lógica da aplicação.
Django/Python → Responsável pelo backend e as rotas do aplicativo.
SQLite → até o momento será o banco de dados utilizado.
LEAFLET → Responsável pela coleta da geolocalização.
Mapbox → Responsável por traçar a rota entre dois pontos (caminho do frete).

---

## ⚙️ Funcionalidades

* 🔑 **Tela de login e cadastro** para solicitantes e motoristas.
* 📱 **Telas principais já criadas** para interação do usuário.
* 🗺️ **Geolocalização em tempo real**, utilizando a API open-source [Leaflet](https://leafletjs.com/), que permite visualizar a localização aproximada e exata do smartphone diretamente no mapa.
*  **Traçar rotas entre dois endereços**, utilizando a API do [Mapbox](https://www.mapbox.com/), que permite entregar rotas entre dois pontos no mapa, calculando tempo e distância.
* 🎨 **Interface responsiva e otimizada** para dispositivos móveis, garantindo boa experiência tanto em smartphones quanto em tablets.
* 📑 **Navbar interativa** com os menus de edição de perfil, início (redireciona a página incial) meus fretes (fretes solicitados e disponíveis) e logout.
* 📤 **Solicitação de Fretes** com API do Mapbox para autocompletar endereços e realizar o traçado da rota, o usuário insere os dados e salva no banco de dados, calculando o preço da entrega e enviando aos freteiros.
* 📥 **Recebimento de Fretes** para os freteiros cadastrados, na qual existe uma lista com todos os fretes solicitados e o freteiro escolhe aceitá-lo e depois poderá recusá-lo.
* 🔄 **Opção para editar e cancelar fretes** exclusivamente para os solicitantes.
* 💱 **Cálculo de rotas** utilizando propriedades de entrega da ANTT (Agência Nacional de Transportes Terrestres).
* 🔏 **Opção para desenvolvedores** manipular dados do banco de dados.


---

## 🛠️ Status do Projeto

🚧 Em desenvolvimento – Funcionalidade de negociação de preço entre motorista e usuário, tendo em vista que já realizamos o cálculo do frete.
  * Integrar imagens do produto que vai ser fretado. E integrar Foto de Perfil do motorista e solicitante.
---

Última modificação:
Integração do calculo do frete na def calcular_frete()
