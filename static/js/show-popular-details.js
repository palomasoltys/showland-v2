'use-strict';

const showTitle = document.querySelector('#show-title').innerText;
const showYear = document.querySelector('#show-year').innerText;
const showPosterPath = document.querySelector('#show-poster-path').src;
const showOverview = document.querySelector('#show-overview').innerText;
const showID = document.querySelector('#show-id').innerText;

const commentFormShow = document.querySelector('#comment-form-show');
commentFormShow.addEventListener('submit', (evt) => {
  evt.preventDefault();
  console.log(showOverview);
  const select = document.querySelector('#rate-show');
  const showRate = select.options[select.selectedIndex].value;
  const showComment = document.querySelector('#comment-show').value;

  const showInformation = {
    title: showTitle,
    year: showYear,
    poster_path: showPosterPath,
    overview: showOverview,
    imdb_id: showID,
    user_rate: showRate,
    user_comment: showComment,
  };

  fetch(`/media/popular/shows/details/${showID}/comment`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(showInformation),
  })
    .then((response) => response.json())
    .then((comment) => {
      alert('Your comment was submited!');
      let commentDiv;

      commentDiv = document.querySelector('.comment-div');

      if (!commentDiv) {
        commentDiv = document.createElement('div');
        commentDiv.setAttribute('id', `${comment.comment_id}`);
        commentDiv.setAttribute('class', 'comment-div');
      }

      commentDiv.insertAdjacentHTML(
        'afterbegin',
        `<div id="${comment.comment_id}" class="comment-block"><a href="/profile/${comment.user_id}/friend" id="show-user-fullname-p">${comment.user_name}</a> <p id="show-review-p">${comment.review}</p> <p id="show-comment-p">${comment.comment}</p> <p id="number-likes-${comment.comment_id}-p">${comment.total_likes}</p> <button type="button" id="delete${comment.comment_id}" value="${comment.comment_id}" class="btn btn-outline-danger delete-comment-btn">Delete</button>         <button type="button" id="comment${comment.comment_id}-user${comment.user_id}" value="${comment.comment_id}" class="btn btn-outline-danger like-btn">Like</button> </div>`,
      );

      no_comment = document.querySelector('#no-comment');
      if (no_comment) {
        no_comment.style.display = 'none';
      }

      const newLikeBtn = document.getElementById(
        `comment${comment.comment_id}-user${comment.user_id}`,
      );
      const newDeleteBtn = document.getElementById(
        `delete${comment.comment_id}`,
      );

      newLikeBtn.addEventListener('click', saveLike);
      newDeleteBtn.addEventListener('click', saveDelete);
    });
});

function saveLike(evt) {
  evt.preventDefault();

  const likeCommentId = evt.target.value;

  const userEmail = document.querySelector('#session-user-email').innerText;

  const likeInformation = {
    userEmail: userEmail,
    commentID: likeCommentId,
  };

  fetch(`/media/popular/shows/details/${likeCommentId}/update_like`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(likeInformation),
  })
    .then((response) => response.text())
    .then((data) => {
      if (evt.target.innerText == 'Like') {
        evt.target.innerText = 'Unlike';
      } else {
        evt.target.innerText = 'Like';
      }
      document.querySelector(`#number-likes-${likeCommentId}-p`).innerHTML =
        data;
    });
}

function likeComment() {
  const likeButton = document.querySelectorAll('.like-btn');
  for (const btn of likeButton) {
    btn.addEventListener('click', (evt) => {
      saveLike(evt, btn);
    });
  }
}

const saveForLaterBtn = document.querySelectorAll('.save-for-later-btn');
for (const laterBtn of saveForLaterBtn) {
  laterBtn.addEventListener('click', (evt) => {
    evt.preventDefault();

    const mediaID = laterBtn.value;
    const userEmail = document.querySelector('#session-user-email').innerText;
    console.log(userEmail);

    const saveForLaterData = {
      mediaID: mediaID,
      userEmail: userEmail,
      title: showTitle,
      year: showYear,
      poster_path: showPosterPath,
      overview: showOverview,
      imdb_id: mediaID,
    };

    fetch(`/media/popular/movies/details/${mediaID}/save_for_later`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(saveForLaterData),
    })
      .then((response) => response.text())
      .then((data) => {
        alert(`Your Save for Later list was updated!`);
        console.log(data);
        if (laterBtn.innerText == 'Save for Later') {
          laterBtn.innerText = 'Remove from List';
        } else {
          laterBtn.innerText = 'Save for Later';
        }
      });
  });
}

function deleteComment() {
  const deleteCommentBtn = document.querySelectorAll('.delete-comment-btn');
  for (const deleteBtn of deleteCommentBtn) {
    deleteBtn.addEventListener('click', (evt) => {
      evt.preventDefault();
      saveDelete(evt);
    });
  }
}

function saveDelete(evt) {
  evt.preventDefault();

  const deleteCommentID = evt.target.value;
  fetch(`/media/popular/movies/details/${deleteCommentID}/delete_comment`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(deleteCommentID),
  })
    .then((response) => response.text())
    .then((user_id_who_commented) => {
      comment = document.getElementById(`${deleteCommentID}`);

      comment.remove();

      commentBlock = document.querySelector('#comment-container');

      if (commentBlock.innerText === '') {
        commentBlock.insertAdjacentHTML(
          'afterend',
          '<p id="no-comment"><i>Be the first one to comment</i></p>',
        );
      }
    });
}
likeComment();
deleteComment();
