'use strict';

// 1. Modal: Kirjautumistoiminnot
document.getElementById('login-button').addEventListener('click', function () {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  if (username && password) {

      login(username, password);


  } else {
    alert('Anna sekä käyttäjänimi että salasana.');
  }

  async function login(username, password) {

      const response = await fetch(`http://127.0.0.1:5000/api/login?name=${username}&password=${password}`);
      console.log("debug1")

      if (!response.ok) {
          alert("No game found with given name or password.")
          window.location.href = 'kirjaudu.html'
      }
      else {
          const result = await response.json()

          var test = result.status[1];
          // console.log(test)

          sessionStorage.setItem('game_id', test) // game id
        window.location.href = 'peli.html'; // Siirrytään pääsivulle

      }

  }
});


// 2. Leaflet: Kartan näyttö
const map = L.map('map', { tap: false }).setView([60, 24], 7);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
}).addTo(map);


// 3. Ohje-painikkeen toiminta
document.getElementById('about-button').addEventListener('click', function () {
  alert('Tavoitteenasi on lentää ympäristöystävällisesti ja oppia samalla lentomatkailun vaikutuksista.');
});
//4.rekisteröitymiseen


document.getElementById('registerbtn').addEventListener('click', async function() {
    register()
})
async function register() {
    const name = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (name.length < 4 || password.length < 4) {
        alert("Name and password must be at least4 characters long.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/register?name=${name}&password=${password}`);
        const result = await response.json();

        if (response.ok) {
            sessionStorage.setItem('game_id', result)
            alert(`Succesfully registered!`);
            window.location.href = 'peli.html'; // Siirrytään pääsivulle

        } else {
            alert(`Virhe: ${result.error}`);
        }
    } catch (error) {
        alert("Check API connection.");
    }
}
