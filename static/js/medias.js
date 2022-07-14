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
      let year = d.release_date;
      year = year.slice(0, 4);
      const id = d.id;
      const movie = `<div>
                      <div class="slide">
                        <div>
                        <a href="/media/popular/movies/details/${id} id="movie-details-${id}">${title}</a>
                          <p class="year">${year}</p>
                        </div>
                        <div class="slide-img"> 
                          <img src="https://image.tmdb.org/t/p/w300${poster_path}">
                        </div>  
                      </div>
                      </div>`;
      document
        .querySelector('.popular-movies')
        .insertAdjacentHTML('beforeend', `<div class="col-4">${movie}</div>`);
    }
    let slider = tns({
      container: '.my-slider-movies',
      slideBy: '3',
      speed: 400,
      nav: false,
      autoplay: true,
      controls: false,
      autoplayButtonOutput: false,
      // autoWidth: true,
      responsive: {
        1600: {
          items: 2,
          gutter: 20,
        },
        1024: {
          items: 2,
          gutter: 20,
        },
        768: {
          items: 1,
          gutter: 20,
        },
        480: {
          items: 1,
        },
      },
    });
  });

// // Receiving data from the API and displaying the most popular shows
fetch('/media/popular/shows')
  .then((response) => response.json())
  .then((data) => {
    for (const d of data.results) {
      const title = d.name;
      const poster_path1 = d.poster_path;
      let poster_path = `https://image.tmdb.org/t/p/w300${poster_path1}`;
      let year = d.first_air_date;
      const id = d.id;
      year = year.slice(0, 4);

      if (poster_path.includes('https://image.tmdb.org/t/p/w300null')) {
        poster_path =
          'https://imgc.artprintimages.com/img/print/epicstockmedia-sunset-waterfall-amazing-nature-landscape_u-l-q19ye1d0.jpg';
      }

      const show = `<div>
                      <div class="slide">
                        <div> 
                        <a href="/media/popular/shows/details/${id} id="show-details-${id}">${title}</a> 
                          <p class="year">${year}</p> 
                        </div>
                        <div class="slide-img">  
                          <img src="${poster_path}">
                        </div>
                      </div>
                    </div>  `;

      document
        .querySelector('.popular-shows')
        .insertAdjacentHTML('beforeend', `<div class="col-4">${show}</div>`);
    }
    let slider = tns({
      container: '.my-slider-shows',
      slideBy: '2',
      speed: 400,
      nav: false,
      autoplay: true,
      controls: false,
      autoplayButtonOutput: false,
      // autoWidth: true,
      responsive: {
        1600: {
          items: 2,
          gutter: 20,
        },
        1024: {
          items: 2,
          gutter: 20,
        },
        768: {
          items: 1,
          gutter: 20,
        },
        480: {
          items: 1,
        },
      },
    });
  });
