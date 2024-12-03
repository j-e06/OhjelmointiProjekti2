'use strict';

const game_id = sessionStorage.getItem('game_id')
if (game_id == null) {
    alert("Sinun pitää kirjautua tai rekisteröityä!")
    window.location.href ='kirjaudu.html'
}

// Leaflet: Kartan näyttö
document.addEventListener('DOMContentLoaded', () => {
    const map = L.map('map').setView([60, 24], 6); // Suomen keskikohta, zoom 6
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    load_game_data();

    load_airports()



    async function load_airports(){
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/check_accessible_airports?game_id=${game_id}`);
            if (!response.ok) {
                throw new Error(response.status);
            }
            const data = await response.json()
            const airports = data.status
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

async function load_game_data() {
    const response = await fetch(`http://127.0.0.1:5000/api/game_details?game_id=${game_id}`);

    if (!response.ok) {
        throw new Error(response.status);
    }
    const data = await response.json()
    const game_data = data.status[0]
    // console.log(game_data)
    document.getElementById('player_name').textContent = game_data.name
    document.getElementById('location').textContent = game_data.location
    document.getElementById('starting_airport').textContent = game_data.starting_airport
    document.getElementById('money').textContent = game_data.money
    document.getElementById('fuel').textContent = game_data.fuel

}


async function open_lootbox() {
    const open_type = document.getElementById('lootbox-type').value;
    console.log(open_type)
    const response = await fetch(`http://127.0.0.1:5000/api/open_lootbox?game_id=${game_id}&open_type=${open_type}`);
    if(response.status === 400) {
        var dataa = await response.json()
        alert(dataa.status)
        return
    }
    else if (response.status !== 200) {
        throw new Error(response.status);
    }
    const data = await response.json()
    const game_data = data.status
    console.log(game_data)
}


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
