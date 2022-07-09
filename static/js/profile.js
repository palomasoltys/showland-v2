const followBtn = document.querySelector('#follow-user');
if (followBtn) {
  followBtn.addEventListener('click', (evt) => {
    evt.preventDefault();
    console.log(followBtn.value);

    userToFollow = { userID: followBtn.value };

    fetch(`/profile/${userToFollow.userID}/friend/update_follow`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userToFollow),
    })
      .then((response) => response.text())
      .then((data) => {
        if (followBtn.innerText == 'Follow') {
          followBtn.innerText = 'Unfollow';
        } else {
          followBtn.innerText = 'Follow';
        }
      });
  });
}
