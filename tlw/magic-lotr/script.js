function parseMana(str) {
    return str.split(/\s*({\w*})\s*/g).filter(Boolean);
}
async function afficherCartes()
{
    let contenu_json = [];
    fetch('https://api.scryfall.com/cards/search?q=e:ltr&format=json&order=set&unique=prints%20lang:fr')
    .then(response=> response.json())
    .then(donnee => {
        for (carte of donnee.data)  {
            contenu_json.push(carte.printed_name);
        }
        console.log(contenu_json);
    });
}

    