'use strict';

// 1. Modal: Kirjautumistoiminnot
document.getElementById('login-button').addEventListener('click', function () {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  if (username && password) {

      const result = login(username, password);
      if (typeof(result) == null ){
          alert("Käyttäjänimi tai salasana on väärin.")
      }
      else {
          login()
          window.location.href = 'peli.html'; // Siirrytään pääsivulle
      }

  } else {
    alert('Anna sekä käyttäjänimi että salasana.');
  }

  async function login(username, password) {

      const response = await fetch(`http://127.0.0.1:5000/api/login?name=${username}&password=${password}`);

      if (!response.ok) {
          alert("durr something went wrong", response.status)
      }
      else {
          const result = await response.json()
          console.log(result)
          sessionStorage.setItem('game_id', result)

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
async function register() {
    const name = document.getElementById('register-name').value;
    const password = document.getElementById('register-password').value;

    if (name.length < 4 || password.length < 4) {
        alert("Nimen ja salasanan tulee olla vähintään 4 merkkiä pitkiä.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/register?name=${name}&password=${password}`);
        const result = await response.json();

        if (response.ok) {
            sessionStorage.setItem('game_id', result)
            alert(`Rekisteröinti onnistui! Pelin ID: ${result}`);
            window.location.href = 'peli.html'; // Siirrytään pääsivulle

        } else {
            alert(`Virhe: ${result.error}`);
        }
    } catch (error) {
        alert("Virhe rekisteröinnissä. Tarkista API:n yhteys.");
    }
}
