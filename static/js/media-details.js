'use-strict';

const mediaTitle = document.querySelector('#media-title').innerText;
const mediaYear = document.querySelector('#media-year').innerText;
const mediaPosterPath = document.querySelector('#media-poster-path').src;
const mediaOverview = document.querySelector('#media-overview').innerText;
const mediaID = document.querySelector('#media-id').innerText;
const mediaType = document.querySelector('#media-type').innerText;

const commentForm = document.querySelector('#comment-form');
commentForm.addEventListener('submit', (evt) => {
  evt.preventDefault();

  const select = document.querySelector('#rate-media');
  const mediaRate = select.options[select.selectedIndex].value;
  const mediaComment = document.querySelector('#comment-media').value;

  const mediaInformation = {
    title: mediaTitle,
    year: mediaYear,
    poster_path: mediaPosterPath,
    overview: mediaOverview,
    imdb_id: mediaID,
    user_rate: mediaRate,
    user_comment: mediaComment,
    media_type: mediaType,
  };

  fetch(`/media/details/${mediaID}/comment`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(mediaInformation),
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
        commentDiv.setAttribute('class', 'row');
      }
      const r = comment.review;
      console.log(typeof r);
      if (comment.review == 1) {
        comment.review = '⭐';
      } else if (comment.review == 2) {
        comment.review = '⭐⭐';
      } else if (comment.review == 3) {
        comment.review = '⭐⭐⭐';
      } else if (comment.review == 4) {
        comment.review = '⭐⭐⭐⭐';
      } else {
        comment.review = '⭐⭐⭐⭐⭐';
      }

      commentDiv.insertAdjacentHTML(
        'afterbegin',
        `<div id="${comment.comment_id}" class="comment-block col-4"><div class="comment-item p-3">
        <a href="/profile/${comment.user_id}/friend" id="media-user-fullname-p">${comment.user_name}</a> 
        <p id="media-review-p" class="comment-p">${comment.review}</p> 
        <p id="media-comment-p" class="comment-p">${comment.comment}</p> 
        <p id="number-likes-${comment.comment_id}-p" class="comment-p n-likes">${comment.total_likes}</p> 
        <button type="button" id="comment${comment.comment_id}-user${comment.user_id}" value="${comment.comment_id}" class="btn btn-outline-danger like-btn btn-action">Like</button>
        <button type="button" id="delete${comment.comment_id}" value="${comment.comment_id}" class="btn btn-outline-danger delete-comment-btn btn-action">Delete</button> 
        </div></div>`,
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
      console.log(newDeleteBtn.value);
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

  fetch(`/media/details/${likeCommentId}/update_like`, {
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

    const saveForLaterData = {
      mediaID: mediaID,
      userEmail: userEmail,
      title: mediaTitle,
      year: mediaYear,
      poster_path: mediaPosterPath,
      overview: mediaOverview,
      imdb_id: mediaID,
      media_type: mediaType,
    };

    fetch(`/media/details/${mediaID}/save_for_later`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(saveForLaterData),
    })
      .then((response) => response.text())
      .then((data) => {
        alert(`Your Save for Later list was updated!`);

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
  console.log(evt.target.value);
  const deleteCommentID = evt.target.value;

  fetch(`/media/details/${deleteCommentID}/delete_comment`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(deleteCommentID),
  })
    .then((response) => response.text())
    .then((user_id_who_commented) => {
      comment = document.getElementById(`${deleteCommentID}`);
      console.log(comment);
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
