function parseMana(str) {
    return str.split(/\s*({\w*})\s*/g).filter(Boolean);
}
async function afficherCartes()
{
    let url ='https://api.scryfall.com/cards/search?q=e:ltr lang:fr&format=json&order=set&unique=prints%20'
    let contenu_json = [];
    let has_more = true    
    fetch(url)
        .then(response=> response.json())
        .then(donnee => { let template = document.querySelector("#card-template");
            let grid = document.querySelector("#grid-container");
            for (carte of donnee.data)  { 
                let clone = document.importNode(template.content, true); // clone le template
                let newContent = clone.firstElementChild.innerHTML // remplace {{modèle}}
                    .replace(/{{texte}}/g, carte.printed_name) // et {{lieux}} par
                    .replace(/{{img}}/g, carte.image_uris.normal)
                clone.firstElementChild.innerHTML = newContent;
                grid.appendChild(clone)
}
        
            
            has_more = donnee.has_more
            url = donnee.next_page
            console.log(contenu_json);
    });
}

    