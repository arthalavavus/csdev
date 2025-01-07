function parseMana(str) {
    return str.split(/\s*({\w*})\s*/g).filter(Boolean);
}
async function afficherCartes()
{
    
    let contenu_json = [];

        fetch('https://api.scryfall.com/cards/search?q=e:ltr lang:fr&format=json&order=set&unique=prints%20')
        .then(response=> response.json())
        .then(donnee => {
            for (carte of donnee.data)  { 
                contenu_json.push(carte.printed_name);
                contenu_json.push(carte.image_uris);
        
            }
    
            console.log(contenu_json);
    });
}

    