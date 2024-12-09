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



async function portInfo(e){

    document.getElementById('map').style.display = 'none';
    document.getElementById('myModal').style.display = 'block';

    const marker = e.target;
    const icao = marker.options.title;

    var airport_response =  await fetch(`http://127.0.0.1:5000/api/get_airport_information?icao_code=${icao}&game_id=${game_id}`);
    const airport_info = await airport_response.json()


    var current_icao = document.getElementById('location').textContent;

    var distance =  await fetch(`http://127.0.0.1:5000/api/distance?icao1=${current_icao}&icao2=${icao}`);

    const distances = await distance.json()

    document.getElementById('country').textContent = airport_info[0]['iso_country']
    document.getElementById('name').textContent = airport_info[0]['name']
    document.getElementById('icao').textContent = icao
    document.getElementById('distance').textContent = distances.status

    document.getElementById('fly').addEventListener('click', async function () {
        var fly_data = await fetch(`http://127.0.0.1:5000/api/fly_check?icao_code=${icao}&game_id=${game_id}`)
        const flyings = await fly_data.json()

        alert(flyings.status)

        location.reload()
    })

    document.getElementById('close').addEventListener('click', function() {
        document.getElementById('map').style.display = 'block';
        document.getElementById('myModal').style.display = 'none';
    })
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

    console.log(game_data)
    // check if we've won

    if (game_data.diamond == 1 && game_data.location === game_data.starting_airport) {
        await showEndPage(true)
    }




    // check if we've lost
    // losing is defined by not being able to open lootbox with money or fuel, and not being able to fly?


    try {
        const response = await fetch(`http://127.0.0.1:5000/api/get_airports?game_id=${game_id}`);
        console.log(response)
        if (!response.ok) {
            throw new Error(response.status);
        }
        const data = await response.json();
        const airports = data.status;
        console.log(airports)

        var min_distance = 0;

        for (var airport of airports) {
            if (!airport.latitude_deg || !airport.longitude_deg) {
                console.error(`Invalid coordinates for airport: ${airport.ident}`);
                return;
            }

            var airport_response = await fetch(`http://127.0.0.1:5000/api/get_airport_information?icao_code=${airport.ident}&game_id=${game_id}`);
            const airport_info = await airport_response.json()

            let dist = await fetch(`http://127.0.0.1:5000/api/distance?icao1=${game_data.location}&icao2=${airport.ident}`);

            let dist_info = await dist.json()
            //console.log(dist_info.status, game_data.fuel, game_data.money*2, game_data.fuel + game_data.money*2)
            console.log(game_data.fuel + game_data.money*2,  dist_info.status)
            if (dist_info.status != 0 && dist_info.status < min_distance) {
                console.log("test")
                let min_distance = dist_info.status;
            }


            let markerColor;
            let port_ident = airport.ident;
            if (port_ident == game_data.location) {
                markerColor = 'green';
            } else if (port_ident == game_data.starting_airport) {
                markerColor = 'red';
            } else if (airport_info[0].lootbox_status == 1) {
                markerColor = 'grey';
            } else {
                markerColor = 'blue'; // Default or unknown status
            }

            const customIcon = L.divIcon({
                className: 'custom-marker',
                html: `<div style="background-color: ${markerColor}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid black;"></div>`,
                iconSize: [20, 20]
            });

            // Add marker to map
            L.marker([airport.latitude_deg, airport.longitude_deg], {icon: customIcon, title: airport.ident})
                .addTo(map)
                .on('click', portInfo);

        }
    } catch (error) {
        console.error("Failed to load airport data:", error);
    }
    console.log(min_distance, game_data.fuel + game_data.money*2)
    if (min_distance > game_data.fuel + game_data.money*2) {
        console.log("aww, game over")
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


//endPage
async function showEndPage(isWinner) {
    const endPage = document.getElementById("endPage");
    document.getElementById('main-container').style.display = "none";
    // Päivitä otsikko ja kuva
    const title = document.getElementById("endPageTitle");
    const image = document.getElementById("endPageImage");


    const game_response = await fetch(`http://127.0.0.1:5000/api/game_details?game_id=${game_id}`);

    if (!game_response.ok) {
        throw new Error("shit")
    }

    var data = await game_response.json()

    var game_data = data.status[0]

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
    console.log(game_data, "yahoooo")
    document.getElementById("resultFuelUsed").textContent = game_data.fuel_used;
    document.getElementById("resultLootboxesOpened").textContent = game_data.lootboxes_opened;
    document.getElementById("resultFlightTaken").textContent = game_data.flights_taken;

    // Näytä loppusivu
    endPage.style.display = "flex";
}


