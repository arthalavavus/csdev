// Ajoute un écouteur d'événement 'click' au bouton avec l'id 'button'
document.getElementById('button').addEventListener('click', function() {
    // Sélectionne le conteneur où les cartes Pokémon seront affichées
    const container = document.querySelector('.conteneur');
    // Sélectionne le template HTML pour la carte Pokémon
    const template = document.getElementById('card-template');

    // Boucle pour créer 100 cartes Pokémon
    for (let i = 1; i <= 100; i++) {
        // Appel à l'API Pokémon pour récupérer les informations sur chaque Pokémon
        fetch(`https://pokeapi.co/api/v2/pokemon-species/${i}/`)
        .then(response => response.json()) // Convertit la réponse en JSON
        .then(data => {
            // Trouve le nom français du Pokémon dans les données de l'API
            let frenchName = data.names.find(name => name.language.name === "fr").name;

            // Crée une copie du template pour chaque Pokémon
            let clone = document.importNode(template.content, true);
            // Sélectionne et définit l'image de la carte Pokémon
            let img = clone.querySelector('.card-img');
            img.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/${i}.svg`;
            // Sélectionne et définit le nom de la carte Pokémon
            let name = clone.querySelector('.pokemon-name');
            name.textContent = `Nom: ${frenchName}`;
            // Sélectionne et définit le numéro de la carte Pokémon
            let number = clone.querySelector('.pokemon-number');
            number.textContent = `Numéro: ${i}`;
            // Ajoute la carte au conteneur
            container.appendChild(clone);
        });
    }

    // Masque le bouton après le clic
    this.style.display = 'none';
});