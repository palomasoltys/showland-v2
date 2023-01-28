
![Logo](https://i.ibb.co/tq6GHtm/Showland-logo-black.png)




ShowLand is a web application where you can comment, like and review your favorite movie or tv show. You can also follow your friends and check out their activity, and lastly but not least you can add movies and shows to your saved for later list.




## Technologies Used

- Backend: Python, Flask, SQL, PostgreSQL, SQLAlchemy;
- Frontend: JavaScript, HTML, CSS, Bootstrap, Jinja
- API's: Movie Alternative Database, TMDB, Google OAuth 2.0


## Features

 - [📹 Full video walk-through](https://youtu.be/EaUxAB7juAc)
### Login and Sign Up
- Users can start by creating an account or log in with google sign in, which helps to easily manage user authentication. This feature was integrated using Google OAuth 2.0.
![Login](https://i.ibb.co/2Z3ZXjV/Screen-Shot-2023-01-27-at-8-47-02-PM.png)
### Homepage 
![Homepage](https://i.ibb.co/Kx4vfKQ/Screen-Shot-2023-01-27-at-8-47-39-PM.png)
### Most Popular Movies and Series
- The TMDB API was used for the most popular movies and series feature making the app more dynamic.
![Popular-movies](https://i.ibb.co/hdhJ1WG/Screen-Shot-2023-01-27-at-8-47-55-PM.png)
### Search for a specific media    
- The Movie Database Alternative API was used to search a media by the title. 
![Search](https://i.ibb.co/Mptj2zn/Screen-Shot-2023-01-27-at-8-48-16-PM.png)
### Comment, Like and Delete Comments, Save for Later
- If the user is logged in, they can leave a comment as well as save it to watch later. 
- For these features, a POST request is made and the media information is stored in the PostgreSQL database, reducing the number of API calls, which improves the performance of the app.
![Comment](https://i.ibb.co/pL49SW2/Screen-Shot-2023-01-27-at-8-48-36-PM.png)

![Comment2](https://i.ibb.co/nbCbkBB/Screen-Shot-2023-01-27-at-8-49-07-PM.png)
- For more interaction, a like and a delete button were implemented within the comment.
- For the like, I queried the database using SQLAlchemy to determine if a user had already liked a comment and toggle the button between "Like" and "Unlike" accordingly. Then, when the user clicks the button, an AJAX call is used to update the number of likes without refreshing the page.
- Similarly, for the delete button, the database is checked to see if there are likes related to the comment, and if there are, the like is deleted first, then the comment itself.
![Like](https://i.ibb.co/prYjy2T/Screen-Shot-2023-01-27-at-8-50-12-PM.png)
### Profile
- In their profiles, users can see all their activities as well as their friends' activities, if they follow them.
![Profile](https://i.ibb.co/hR1gKw5/Screen-Shot-2023-01-27-at-8-51-12-PM.png)

![Save-for-later](https://i.ibb.co/7JyH182/Screen-Shot-2023-01-27-at-8-51-28-PM.png)

![Friends](https://i.ibb.co/ww4R92D/Screen-Shot-2023-01-27-at-8-51-57-PM.png)



## Future Improvements

- My long-term goal with this project is to recreate the front end with React by creating components and reusing them, which would help maintain a consistent code style and overall maintainability.


