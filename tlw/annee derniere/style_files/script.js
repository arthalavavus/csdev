function parseMana(str) {
    return str.split(/\s*({\w*})\s*/g).filter(Boolean);
}

async function afficherCartes() {

    const symbols = await getSymbols();
    const cardTemplate = document.getElementById('card-template');
    const gridContainer = document.getElementById('grid-container');

    let has_more = true;
    let cartes = [];
    let uri = "https://api.scryfall.com/cards/search?format=json&order=set&q=e%3Altr+lang%3Afr&unique=prints"
    while (has_more) {
        const response = await fetch(uri);
        if (!response.ok) {
            throw new Error(`Erreur API OpenWeatherMap: ${response.statusText}`);
        }
        const data = await response.json();
        has_more = data['has_more'];
        uri = data['next_page'];
        data['data'].forEach(element => {
            cartes.push(element);
        });
    }

    if (!cardTemplate || !gridContainer) {
        console.error("Modèle ou conteneur de tours manquant dans le HTML");
        return;
    }

    cartes.forEach(carte => {
        const clone = document.importNode(cardTemplate.content, true);
        clone.querySelector(".card-img").src = carte.image_uris.normal;
        clone.querySelector(".card p").textContent = carte.printed_name;
        parseMana(carte.mana_cost).forEach(mana => {
            const img = document.createElement("img");
            img.src = symbols[mana];
            img.alt = mana;
            img.classList.add("mana");
            clone.querySelector(".card").appendChild(img);
        });

        gridContainer.appendChild(clone);
    });
}

async function getSymbols() {
    const uri = 'https://api.scryfall.com/symbology'
    let symbols = {};
    let has_more = true;
    while (has_more) {
        const response = await fetch(uri);
        if (!response.ok) {
            throw new Error(`Erreur API OpenWeatherMap: ${response.statusText}`);
        }
        const data = await response.json();
        has_more = data['has_more'];
        data['data'].forEach(symbol => {
            if (!(symbol.symbol in Object.keys(symbols))) {
                symbols[symbol.symbol] = symbol.svg_uri;
            }
        });
    }
    return symbols
}

window.addEventListener('DOMContentLoaded', async () => {
    await afficherCartes();
})