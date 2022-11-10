/*
 * billboard.js
 * Ariana Borlak, Elek Thomas-Toth
 */

window.onload = initialize;

function initialize() {
    loadYearSongs();
    loadYearsSelector();
    
    let element = document.getElementById('Search_param');
    if (element) {
        element.onchange = onParameterChanged;
    }
}

// Returns the base URL of the API, onto which endpoint
// components can be appended.
function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}

function loadYearsSelector() {
    let url = getAPIBaseURL() + '/years';

    fetch(url, {method:'get'})

    .then((response) => response.json())

    .then(function(songs_years) {
      let yearSelectorBody = '';
      for (let i = 0; i < songs_years.length; i++) {
          let year = songs_years[i];
          yearSelectorBody += '<option value="' + year['year'] + '">';
      }
      let yearSelector = document.getElementById('year_selector');
      if (yearSelector) {
        yearSelector.innerHTML = yearSelectorBody;
      }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function loadYearSongs() {
    let url = getAPIBaseURL() + '/years/<year>';

    // Send the request to the books API /years/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of year dictionaries, use it to build
    // an HTML table displaying the song titles and authors.
    .then(function(songs) {
        // Add the <option> elements to the <select> element
        let yearBody = '';
        for (let k = 0; k < songs.length; k++) {
            let song = songs[k];
            yearBody += '<li>'
                     + song['title'] + ' by ' + song['artist_name']
                     + ', rank ' + song['rank']
                     + '</li>\n';
        }

        let list = document.getElementById('yearSongs');
        if (list) {
            list.innerHTML = yearBody;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

function onParameterChanged() {
    let element = document.getElementById('Search_param');
    if (!element) {
        return;
    }
    let search_parameter = element.value; 

    element.innerHTML(search_parameter)


}

