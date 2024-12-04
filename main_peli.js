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

    load_game_data(map);


});

async function portInfo(){
    alert("Yahoo")
}

async function load_game_data(map) {
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
    // check if game over!

    console.log(game_data)

    if (game_data.diamond == 1 && game_data.location === game_data.starting_airport) {
        window.location.href = "end_page.html";
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/check_accessible_airports?game_id=${game_id}`);
        if (!response.ok) {
            throw new Error(response.status);
        }
        const data = await response.json();
        const airports = data.status;

        // Check if the map instance is valid
        if (!map || typeof map.addLayer !== 'function') {
            throw new Error("Invalid map instance");
        }

        airports.forEach(airport => {
            if (!airport.latitude_deg || !airport.longitude_deg) {
                console.error(`Invalid coordinates for airport: ${airport.ident}`);
                return;
            }

            let markerColor;
            let port_ident = airport.ident;
            console.log(port_ident, game_data.location, game_data.starting_airport)
            if (port_ident == game_data.location) {
                markerColor = 'green';
            } else if (port_ident == game_data.starting_airport) {
                console.log(port_ident, game_data.location, game_data.starting_airport)
                markerColor = 'red';
            } else {
                markerColor = 'blue'; // Default or unknown status
            }

            const customIcon = L.divIcon({
                className: 'custom-marker',
                html: `<div style="background-color: ${markerColor}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid black;"></div>`,
                iconSize: [20, 20]
            });

            // Add marker to map
            L.marker([airport.latitude_deg, airport.longitude_deg], { icon: customIcon })
                .addTo(map)
                .on('click', portInfo);
        });
    } catch (error) {
        console.error("Failed to load airport data:", error);
    }

    // check if current airports lootbox is opened, if yes, disable button and say "opened"

    var box_info =  await fetch(`http://127.0.0.1:5000/api/get_airport_information?icao_code=${game_data.location}&game_id=${game_id}`);
    if (!box_info.ok) {
        throw new Error(box_info.status);
    }
    const port_data = await box_info.json()
    var box_status = port_data[0]['lootbox_status']
    if (box_status === 1) {
        var btn = document.getElementById('open_btn')
        btn.disabled = "true";
        btn.style.background = "grey"
        btn.style.hover = "none"
        btn.innerText = "Already opened"
    }
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
    alert(game_data)
    location.reload()

}

async function refuel() {
    const fuel_amount = document.getElementById('fuelamount').value;
    console.log(fuel_amount)

        const response = await fetch(`http://127.0.0.1:5000/api/refuel?game_id=${game_id}&amount=${fuel_amount}`);
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
    location.reload()
}