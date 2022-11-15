/*
 * billboard.js
 * Ariana Borlak, Elek Thomas-Toth
 */

window.onload = initialize;

function initialize() {
    loadYearSongs();
    loadResults();
    loadYearsSelector();

    let parameters = document.getElementById('Search_param');
    if (parameters) {
        parameters.onchange = onParameterChanged;
    }

    let search_button = document.getElementById('Search_button')
    if(search_button) {
        search_button.onclick = onSearch;
    }

    // let search_bar = document.getElementById('Search_bar')
    // if(search_bar){
    //     search_bar.onsubmit = onSearch;
    // }

    let years = document.getElementById('year_selector');
    if (years) {
        years.onchange = onYearsSelected;
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

function getBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/';
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
          yearSelectorBody += '<option value="'+ year['year'] + '">'
                           + year['year']
                           + '</option>\n';
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

function onYearsSelected() {
  let element = document.getElementById('year_selector');
  if (!element) {
    return;
  }
  let year = element.value;

  location.href = getBaseURL() + '/years/' + year;

  fetch(location.href, {method: 'get'})

  .then((response) => response.json())

  .then(function(songs_years) {
    let
  })
}

function loadYearSongs() {
    if(!document.getElementById('Year_to_get')){
        return;
    }
    let year = document.getElementById('Year_to_get').innerHTML
    let url = getAPIBaseURL() + '/years/' + year;

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

function loadResults() {
    let option = 'artists';
    if(document.getElementById('Option')){
        option = document.getElementById('Option').innerHTML;
    } else {
        return;
    }
    let search_text = 'a';
    if( document.getElementById('Search_text')){
        search_text = document.getElementById('Search_text').innerHTML;
    } else {
        return;
    }
    let url = getAPIBaseURL() + '/search/' + option + '/' + search_text;

    // Send the request to the books API /years/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of year dictionaries, use it to build
    // an HTML table displaying the song titles and authors.
    .then(function(results) {
        // Add the <option> elements to the <select> element
        let resultsBody = '';
        for (let k = 0; k < results.length; k++) {
            let result = results[k];
            if (result['title']) {
                resultsBody += '<li>'
                        + result['title'] + ' by ' + result['artist_name']
                        + '</li>\n';
            } else {
                resultsBody += '<li>'
                    + result['artist_name']
                    + '</li>\n';
            }
        }

        let list = document.getElementById('Results');
        if (list) {
            list.innerHTML = resultsBody;
        }
    })
}





//makes it so the search parameters can be changed
function onParameterChanged() {
    let element = document.getElementById('Search_param');
    if (!element) {
        return;
    }
    let search_parameter = element.value;
    element.innerHTML(search_parameter);
}

function onSearch(){
    let element = document.getElementById('Search_bar');
    if(!element.value) {
        return;
    }
    let search_text = element.value;
    let search_parameter = document.getElementById('Search_param').value;

    let url = '' + getBaseURL() + 'search/' + search_parameter + '/' + search_text;
    window.location.replace(url);


}