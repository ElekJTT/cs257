/*
 * billboard.js
 * Ariana Borlak, Elek Thomas-Toth
 */

window.onload = initialize;

function initialize() {
    loadYearSongs();
    //
    // let element = document.getElementById('author_selector');
    // if (element) {
    //     element.onchange = onAuthorsSelectionChanged;
    // }
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

function loadYearSongs() {
    let url = getAPIBaseURL() + '/year/<year>';

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

// function onAuthorsSelectionChanged() {
//     let authorID = this.value;
//     let url = getAPIBaseURL() + '/books/author/' + authorID;
//
//     fetch(url, {method: 'get'})
//
//     .then((response) => response.json())
//
//     .then(function(books) {
//         let tableBody = '';
//         for (let k = 0; k < books.length; k++) {
//             let book = books[k];
//             tableBody += '<tr>'
//                             + '<td>' + book['title'] + '</td>'
//                             + '<td>' + book['publication_year'] + '</td>'
//                             + '</tr>\n';
//         }
//
//         // Put the table body we just built inside the table that's already on the page.
//         let booksTable = document.getElementById('books_table');
//         if (booksTable) {
//             booksTable.innerHTML = tableBody;
//         }
//     })
//
//     .catch(function(error) {
//         console.log(error);
//     });
// }

