'use-strict';

// Display the media that the user searched on medias.html
const mediasIDs = [];
const searchMediaForm = document.querySelector('#search-media-form');
searchMediaForm.addEventListener('submit', (evt) => {
  evt.preventDefault();

  const searchQuery = document.querySelector('#search-btn').value;
  const queryString = new URLSearchParams({ s: searchQuery });
  //Receiving data from the search route on server.py and displaying the medias according to the query string
  fetch(`/search?${queryString}`)
    .then((response) => response.json())
    .then((data) => {
      document.querySelector('.media-response').innerHTML = '';
      if (data.Response === 'False') {
        document.querySelector('.media-response').innerHTML = 'Media not found';
      } else {
        for (const d of data.Search) {
          const title = d.Title;
          const poster_path = d.Poster;
          const year = d.Year;
          const id = d.imdbID;
          mediasIDs.push(id);
          const media = `<li><h2><a href="/media/details/${id}" id="media-details-${id}">${title}</a><p>${year}</p></h2><img src="${poster_path}"> </li>`;
          document
            .querySelector('.media-response')
            .insertAdjacentHTML(
              'beforeend',
              `<div class="col-4">${media}</div>`,
            );
        }
      }
    });
});

// Receiving data from the API and displaying the most popular movies
fetch('/media/popular/movies')
  .then((response) => response.json())
  .then((data) => {
    for (const d of data.results) {
      const title = d.title;
      const poster_path = d.poster_path;
      const year = d.release_date;
      const id = d.id;
      const movie = `<li><h2><a href="/media/popular/movies/details/${id} id="movie-details-${id}">${title}</a><p>${year}</p></h2> <img src="https://image.tmdb.org/t/p/w300${poster_path}" </li>`;
      document
        .querySelector('.popular-movies')
        .insertAdjacentHTML('beforeend', `<div class="col-4">${movie}</div>`);
    }
  });

// Receiving data from the API and displaying the most popular shows
fetch('/media/popular/shows')
  .then((response) => response.json())
  .then((data) => {
    for (const d of data.results) {
      const title = d.name;
      const poster_path1 = d.poster_path;
      let poster_path = `https://image.tmdb.org/t/p/w300${poster_path1}`;
      const year = d.first_air_date;
      const id = d.id;

      if (poster_path.includes('https://image.tmdb.org/t/p/w300null')) {
        poster_path =
          'https://imgc.artprintimages.com/img/print/epicstockmedia-sunset-waterfall-amazing-nature-landscape_u-l-q19ye1d0.jpg';
      }

      const show = `<li><h2><a href="/media/popular/shows/details/${id} id="show-details-${id}">${title}</a><p>${year}</p></h2> <img src="${poster_path}" </li>`;
      document
        .querySelector('.popular-shows')
        .insertAdjacentHTML('beforeend', `<div class="col-4">${show}</div>`);
    }
  });

// function send_movie_data_to_server(title, poster_path, year, overview, id) {
//   fetch(`/movies/${id}/details`, {
//     method: 'POST',
//     body: JSON.stringify({
//       title: title,
//       poster_path: poster_path,
//       year: year,
//       overview: overview,
//       id: id,
//     }),
//     headers: {
//       'Content-Type': 'application/json',
//     },
//   });
// }
