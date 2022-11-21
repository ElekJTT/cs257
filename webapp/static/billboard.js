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

//helper function that returns the base url of the window
function getBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/';
    return baseURL;
}

//retrieves all the years in the database to populate the year dropdown
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

//retrieves the top songs from a particular year
function loadYearSongs() {
    let url = window.location;

    if (url == getBaseURL()) {
      //sets the home page to display songs from 2015
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
            //creates links to the song and artist pages
            yearBody += '<li><a href="/artist/' + song['artist_name'] + '/song/' + song['title'] + '">'
                     + song['title'] + '</a>' + ' by ' + '<a href ="/artist/' + song['artist_name'] + '">' + song['artist_name']
                     + '</a>' + ', Rank ' + song['rank']
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

//retrieves the results of a search
function loadResults() {
    let url = getAPIBaseURL() + window.location.pathname;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(results) {
        let resultsBody = '';
        for (let k = 0; k < results.length; k++) {
            let result = results[k];
            if (result['title']) {
                //If the search option is songs or lyrics, creates links for the song and artist pages
                resultsBody += '<li><a href="/artist/' + result['artist_name'] + '/song/' + result['title'] + '">'
                         + result['title'] + '</a>' + ' by ' + '<a href ="/artist/' + result['artist_name'] + '">' + result['artist_name']
                         + '</a>'
                         + '</li>\n';
            } else {
                //Else creates links for the artist pages
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

//retrieves the lyrics of a song
function loadSongLyrics() {
    let url = getAPIBaseURL() + window.location.pathname;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(song_info) {
        let song = song_info[0];
        let lyricsBody = song['lyrics'];
        let artistBody = song['artist_name'];

        //Creates links to the song and artist pages
        let songArtistBody = '';
        songArtistBody += '<a href="/artist/' + song['artist_name'] + '/song/' + song['title'] + '">'
                 + song['title'] + '</a>' + ' by ' + '<a href ="/artist/' + song['artist_name'] + '">' + song['artist_name']
                 + '</a>\n';

        let lyricList = document.getElementById('songLyrics');
        let songArtist = document.getElementById('songArtist');
        if (lyricList) {
            lyricList.innerHTML = lyricsBody;
        }
        if (songArtist) {
            songArtist.innerHTML = songArtistBody;
        }
    })
    .catch(function(error) {
        console.log(error);
    });
}

//retrieves all the songs by a particular artist
function loadArtistSongs() {
    let url_helper = window.location.pathname;
    let url = getAPIBaseURL() + url_helper;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(song_list) {
      let artistBody = '';
      for (let k = 0; k < song_list.length; k++) {
          //creates links to the song and year pages
          let song = song_list[k];
          artistBody += '<li><a href="' + url_helper + '/song/' + song['title'] + '">'
                   + song['title'] + '</a>'
                   + ', <a href="/top100/' + song['year'] + '">' + song['year'] + '</a>' + ' Rank ' + song['rank']
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