// Fonction JavaScript (game.js)
function btnClk(col, row) {
    // Obtenez le bouton par son ID
    var bouton = document.getElementById("BlockBtn" + col + "_" + row);

    // Changez le contenu du bouton avec le symbole de l'utilisateur
    bouton.innerHTML = bouton.getAttribute("data-symbol");

    // Désactivez le bouton pour qu'il ne puisse plus être cliqué
    bouton.disabled = true;

    // Autres actions à effectuer lors du clic du bouton...
    // Ajoutez votre logique de jeu ici
}
