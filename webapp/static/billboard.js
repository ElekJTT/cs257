/*
 * billboard.js
 * Ariana Borlak, Elek Thomas-Toth
 */

window.onload = initialize;

function initialize() {
    loadYearSongs();
    loadResults();
    loadYearsSelector();
    loadSongLyrics();
    loadArtistSongs();

    let parameters = document.getElementById('Search_param');
    if (parameters) {
        parameters.onchange = onParameterChanged;
    }

    let search_button = document.getElementById('Search_button')
    if(search_button) {
        search_button.onclick = onSearch;
    }

 
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
    if(window.location.pathname == '/'){
        var selected_year = 2015;
    } else {
        var selected_year = window.location.pathname.slice(-4);
    }
    

    fetch(url, {method:'get'})

    .then((response) => response.json())

    .then(function(songs_years) {
      let yearSelectorBody = '';
      for (let i = 0; i < songs_years.length; i++) {
          let year = songs_years[i];
          yearSelectorBody += '<option value="'+ year['year'] + '"'
          if(year['year'] == selected_year) {
            yearSelectorBody += ' selected'
          }
          yearSelectorBody += '>'
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

  let url = getBaseURL() + 'top100/' + year;

  window.location.replace(url);
}

function loadYearSongs() {
    let url = window.location;

    if (url == getBaseURL()) {
      url = getAPIBaseURL() + '/top100/2015';
    } else {
      url = getAPIBaseURL() + window.location.pathname;
    }

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(songs) {
        let yearBody = '';
        for (let k = 0; k < songs.length; k++) {
            let song = songs[k];
            yearBody += '<li><a href="/artist/' + song['artist_name'] + '/song/' + song['title'] + '">'
                     + song['title'] + '</a>' + ' by ' + '<a href ="/artist/' + song['artist_name'] + '">' + song['artist_name']
                     + '</a>' + ', rank ' + song['rank']
                     + '</li>\n';
        }

        let yearList = document.getElementById('yearSongs');
        if (yearList) {
            yearList.innerHTML = yearBody;
        }

    })
    .catch(function(error) {
        console.log(error);
    });
}

function loadResults() {

    let url = getAPIBaseURL() + window.location.pathname;

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
                resultsBody += '<li><a href="/artist/' + result['artist_name'] + '/song/' + result['title'] + '">'
                         + result['title'] + '</a>' + ' by ' + '<a href ="/artist/' + result['artist_name'] + '">' + result['artist_name']
                         + '</a>'
                         + '</li>\n';
            } else {
                resultsBody += '<li><a href ="/artist/' + result['artist_name'] + '">'
                    + result['artist_name']
                    + '</a></li>\n';
            }
        }

        let list = document.getElementById('Results');
        if (list) {
            list.innerHTML = resultsBody;
        }
    })
}

function loadSongLyrics() {
    let url = getAPIBaseURL() + window.location.pathname;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(song_info) {
        let lyricsBody = '';
        let song = song_info[0];
        lyricsBody += song['lyrics'];

        let lyricList = document.getElementById('songLyrics');
        if (lyricList) {
            lyricList.innerHTML = lyricsBody;
        }
    })
    .catch(function(error) {
        console.log(error);
    });
}

function loadArtistSongs() {
    let url_helper = window.location.pathname;
    let url = getAPIBaseURL() + url_helper;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(song_list) {
      let artistBody = '';
      for (let k = 0; k < song_list.length; k++) {
          let song = song_list[k];
          artistBody += '<li><a href="' + url_helper + '/song/' + song['title'] + '">'
                   + song['title'] + '</a>'
                   + ', rank ' + song['rank'] + ' in ' + song['year']
                   + '</li>\n';
      }

      let artistList = document.getElementById('artistSongs');
      if (artistList) {
          artistList.innerHTML = artistBody;
      }

    })
    .catch(function(error) {
        console.log(error);
    });
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