'use strict';

// const game_id = sessionStorage.getItem('game_id')
const game_id = 2;
console.log(game_id)
//if (game_id == null) {
//    alert("Sinun pitää kirjautua tai rekisteröityä!")
//    window.location.href ='kirjaudu.html'
//}


// Leaflet: Kartan näyttö
document.addEventListener('DOMContentLoaded', () => {
    const map = L.map('map').setView([60, 24], 6); // Suomen keskikohta, zoom 6
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);


    load_airports()

    async function load_airports(){
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/check_accessible_airports?game_id=${game_id}`);
            console.log(response)
            if (!response.ok) {
                throw new Error(response.status);
            }
            const data = await response.json()
            const airports = data.status
            console.log(airports)
            airports.forEach(airport => {
                L.marker([airport.latitude_deg, airport.longitude_deg])
                    .addTo(map)
                    .bindPopup('<strong>${airport.ident}</strong>')
            })

        } catch (error) {
            console.error("failed to load airport data:", error)
        }
    }
});


// Lootboxin avaus
async function openLootbox() {
    const gameId = document.getElementById('lootbox-game-id').value;
    const lootboxType = document.getElementById('lootbox-type').value;

    if (!gameId) {
        alert('Syötä pelin ID avataksesi lootboxin.');
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/lootbox?gameId=${gameId}&type=${lootboxType}`);
        const result = await response.json();

        if (response.ok) {
            alert(`Sait lootboxista: ${result.reward}`);
        } else {
            alert(`Virhe: ${result.error}`);
        }
    } catch (error) {
        alert('Virhe lootboxin avauksessa. Tarkista palvelimen yhteys.');
    }
}

// JavaScript for toggling the stats window
        const toggleButton = document.getElementById('toggleButton');
        const statsWindow = document.getElementById('statsWindow');
        const closeButton = statsWindow.querySelector('.close');

        // Show or hide the stats window when the button is clicked
        toggleButton.addEventListener('click', () => {
            if (statsWindow.style.display === 'none' || statsWindow.style.display === '') {
                statsWindow.style.display = 'block';
                toggleButton.textContent = 'Hide Stats';
            } else {
                statsWindow.style.display = 'none';
                toggleButton.textContent = 'Show Stats';
            }
        });

        // Close the stats window when the close button is clicked
        closeButton.addEventListener('click', () => {
            statsWindow.style.display = 'none';
            toggleButton.textContent = 'Show Stats';
        });
 // tilastot
    async function load_stats(){
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/game_details?game_id=${game_id}`);
            console.log(response)
            if (!response.ok) {
                throw new Error(response.status);
            }
            const data = await response.json()
            const stats = data.status
            console.log(stats)
            //


        } catch (error) {
            console.error("failed to load airport data:", error)
        }
    }

//endPage
function showEndPage(isWinner, results) {
    const endPage = document.getElementById("endPage");
    document.getElementById('main-container').style.display = "none";
    // Päivitä otsikko ja kuva
    const title = document.getElementById("endPageTitle");
    const image = document.getElementById("endPageImage");

    if (isWinner) {
        title.textContent = "Congratulations! You Won!";
        image.src = "endPage..png";
        image.alt = "You Won!";
    } else {
        title.textContent = "Game Over! You Lost!";
        image.src = "loser.png";
        image.alt = "You Lost!";
    }

    // Päivitä tulokset
    document.getElementById("resultFuelUsed").textContent = results.fuel_used;
    document.getElementById("resultLootboxesOpened").textContent = results.lootboxes_opened;
    document.getElementById("resultFlightTaken").textContent = results.flight_taken;

    // Näytä loppusivu
    endPage.style.display = "flex";
}
const endPage = document.getElementById("endPage");
endPage.style.display = "flex"; // Näkyviin ja keskitetään sisältö

