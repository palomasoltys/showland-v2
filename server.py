"""Server for ShowLand app"""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import requests
import json
import os
import google.oauth2.id_token as google_id_token
import google.auth.transport.requests as google_requests


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask(__name__)
app.secret_key = "you-shouldnt-know"
app.jinja_env.undefined = StrictUndefined

GOOGLE_CLIENT_ID = "369785474126-1uk5r5412uojj84mks2ro2ghu4ggi599.apps.googleusercontent.com"

@app.route('/')
def homepage():
    """Display homepage"""

    if 'user_email' in session:
        user = crud.get_user_by_email(session['user_email'])
        print(session['user_email'])
        return render_template('homepage.html', user=user)
    else:
        return render_template('homepage.html')



@app.route('/media')
def all_medias():
    """Display all medias"""
    return render_template('medias.html')

@app.route('/media/popular/movies')
def all_popular_movies():
    """Display all popular movies"""
    tmdb_api_key = os.environ['TMDB_API_KEY']
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/popular?api_key={tmdb_api_key}&language=en-US&page=1")
    data = response.json()
    return data

@app.route('/media/popular/shows')
def all_popular_shows():
    """Display the most popular shows from TMDB API"""
    tmdb_api_key = os.environ['TMDB_API_KEY']
    response = requests.get(
        f"https://api.themoviedb.org/3/tv/popular?api_key={tmdb_api_key}&language=en-US&page=1")
    data = response.json()
    return data    



@app.route('/media/popular/shows/details/<tmdb_id>')
def get_popular_shows(tmdb_id):
    """Display the details of a specific show from TMDB API"""

    tmdb_api_key = os.environ['TMDB_API_KEY']
    url = f'https://api.themoviedb.org/3/tv/{tmdb_id}?api_key={tmdb_api_key}&language=en-US'

    response = requests.get(url)
    data = response.json()

    show = {'show_title': data['original_name'],
            'show_release_date': data['first_air_date'], 
            'show_poster_path': data['poster_path'], 
            'show_overview': data['overview'], 
            'show_id': data['id']}

    show_info = crud.get_media_by_imdb_id(str(show['show_id']))
    user = crud.get_user_by_email(session['user_email'])

    return render_template('show_popular_details.html', show=show, show_info=show_info, user=user )


@app.route('/media/popular/movies/details/<tmdb_id>')
def get_popular_movie(tmdb_id):
    """Display the details of a specific movie from TMDB API"""


    tmdb_api_key = os.environ['TMDB_API_KEY']
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={tmdb_api_key}&language=en-US'

    response = requests.get(url)
    data = response.json()
    movie = {'movie_title': data['original_title'], 
             'movie_release_date': data['release_date'], 
             'movie_poster_path': data['poster_path'], 
             'movie_overview': data['overview'], 
             'movie_id': data['id'], 
             'movie_imdb_id': data['imdb_id'] }

    movie_info = crud.get_media_by_imdb_id(str(movie['movie_id']))

    user = None
    if 'user_email' in session:
        user = crud.get_user_by_email(session['user_email'])

    return render_template('movie_popular_details.html', movie=movie, movie_info=movie_info, user=user )

@app.route('/media/popular/movies/details/<imdb_id>/comment', methods=['POST'])
def comment_movie(imdb_id):
    """Submit a comment for a specific movie from TMDB API and save both on the database"""


    movie_title = request.json.get('title')
    movie_year = request.json.get('year')
    movie_poster_path = request.json.get('poster_path')
    movie_overview = request.json.get('overview')
    movie_imdb_id = request.json.get('imdb_id')
    movie_rate = request.json.get('user_rate')
    movie_comment = request.json.get('user_comment')


    user = crud.get_user_by_email(session['user_email'])
    movie = crud.get_media_by_imdb_id(imdb_id)
    if movie:
        user_comment = crud.create_comment(
                            comment=movie_comment,
                            review=movie_rate, 
                            user_id=user.user_id, 
                            media_id=movie.media_id)
        print(user_comment)                    
        db.session.add(user_comment)
        db.session.commit()
    else:
        media_to_db = crud.create_media(
                            media_type='movie', 
                            title=movie_title, 
                            overview=movie_overview, 
                            poster_path=movie_poster_path, 
                            imdb_id=movie_imdb_id)
        print(media_to_db)                   
        db.session.add(media_to_db)
        db.session.commit()      

        user_comment = crud.create_comment(
                            comment=movie_comment, 
                            review=movie_rate, 
                            user_id=user.user_id, 
                            media_id=media_to_db.media_id)

        db.session.add(user_comment)
        db.session.commit()
    
    comment_id = user_comment.comment_id
    total_likes = crud.get_like_numbers_by_comment_id(comment_id)

    comment_by_user = {
                        "comment_id": comment_id,
                        "comment": user_comment.comment,
                        "review": user_comment.review,
                        "user_name": user_comment.user.full_name,
                        "user_id": user_comment.user_id,
                        "media_id": user_comment.media_id,
                        "total_likes": total_likes
                        }

    return comment_by_user



@app.route('/media/popular/shows/details/<imdb_id>/comment', methods=['POST'])
def comment_show(imdb_id):
    """Submit a comment for a specific show from TMDB API and save both on the database"""


    show_title = request.json.get('title')
    show_year = request.json.get('year')
    show_poster_path = request.json.get('poster_path')
    show_overview = request.json.get('overview')
    show_imdb_id = request.json.get('imdb_id')
    show_rate = request.json.get('user_rate')
    show_comment = request.json.get('user_comment')

    user = crud.get_user_by_email(session['user_email'])
    show = crud.get_media_by_imdb_id(imdb_id)
    if show:
        user_comment = crud.create_comment(
                            comment=show_comment,
                            review=show_rate, 
                            user_id=user.user_id, 
                            media_id=show.media_id)
        print(user_comment)                    
        db.session.add(user_comment)
        db.session.commit()
    else:
        show_to_db = crud.create_media(
                            media_type='series', 
                            title=show_title, 
                            overview=show_overview, 
                            poster_path=show_poster_path, 
                            imdb_id=show_imdb_id)
                    
        db.session.add(show_to_db)
        db.session.commit()      

        user_comment = crud.create_comment(
                            comment=show_comment, 
                            review=show_rate, 
                            user_id=user.user_id, 
                            media_id=show_to_db.media_id)

        db.session.add(user_comment)
        db.session.commit()

    comment_id = user_comment.comment_id
    total_likes = crud.get_like_numbers_by_comment_id(comment_id)

    comment_by_user = {
                        "comment_id": comment_id,
                        "comment": user_comment.comment,
                        "review": user_comment.review,
                        "user_name": user_comment.user.full_name,
                        "user_id": user_comment.user_id,
                        "media_id": user_comment.media_id,
                        "total_likes": total_likes
                        }

    return comment_by_user



@app.route('/media/popular/movies/details/<comment_id>/update_like', methods=['POST'])
def like_comment_popular_movie(comment_id):
    """Like/Unlike a comment and update in the database (TMDB API)"""

    # user_id = request.json.get('userID')
    logged_in_user = crud.get_user_by_email(request.json.get('userEmail'))
    user_id = logged_in_user.user_id
    print("\n"*5)
    print("User ID", user_id)
   # like_id = request.json.get('likeID')

    like_by_id = crud.get_like_by_comment_user_id(comment_id=comment_id, user_id=user_id)
    print("Like exists?", like_by_id)
    print("\n"*5)

    if like_by_id:
        db.session.delete(like_by_id)  
    else:      
        like = crud.create_like(user_id=user_id, 
                            comment_id=comment_id)    
        db.session.add(like)
    db.session.commit()

    number_likes = crud.get_like_numbers_by_comment_id(comment_id)

    # if the like exists for that comment, delete it from the datavase, else add the like to the db.

    return str(number_likes)


@app.route('/media/popular/shows/details/<comment_id>/update_like', methods=['POST'])
def like_comment_popular_show(comment_id):
    """Like/Unlike a comment and update in the database (TMDB API)"""

    # user_id = request.json.get('userID')
    logged_in_user = crud.get_user_by_email(request.json.get('userEmail'))
    user_id = logged_in_user.user_id
    print("\n"*5)
    print("User ID", user_id)
   # like_id = request.json.get('likeID')

    like_by_id = crud.get_like_by_comment_user_id(comment_id=comment_id, user_id=user_id)
    print("Like exists?", like_by_id)
    print("\n"*5)

    if like_by_id:
        db.session.delete(like_by_id)  
    else:      
        like = crud.create_like(user_id=user_id, 
                            comment_id=comment_id)    
        db.session.add(like)
    db.session.commit()

    number_likes = crud.get_like_numbers_by_comment_id(comment_id)
    print(number_likes)

    # if the like exists for that comment, delete it from the datavase, else add the like to the db.

    return str(number_likes)


@app.route('/media/popular/movies/details/<imdb_id>/save_for_later', methods=['POST'])
def save_for_later_movie(imdb_id):
    """Add/Remove movie (TMDB API) to/from Save for Later database"""

    logged_in_user = crud.get_user_by_email(request.json.get('userEmail'))
    user_id = logged_in_user.user_id
    
    if crud.get_media_by_imdb_id(imdb_id) == None:
        media_title = request.json.get('title')
        media_poster_path = request.json.get('poster_path')
        media_overview = request.json.get('overview')
        media_imdb_id = request.json.get('imdb_id')
 
        
        media_to_db = crud.create_media(
                        media_type='movie', 
                        title=media_title, 
                        overview=media_overview, 
                        poster_path=media_poster_path, 
                        imdb_id=media_imdb_id)
               
        db.session.add(media_to_db)
        db.session.commit()  

    media = crud.get_media_by_imdb_id(imdb_id)

    save_later_by_media_user_id = crud.get_save_for_later_by_media_user_id(user_id, media.media_id)

    if save_later_by_media_user_id:
        db.session.delete(save_later_by_media_user_id)
    else:
        save_for_later = crud.create_save_for_later(user_id=user_id, media_id=media.media_id)    
        db.session.add(save_for_later)

    db.session.commit()    

    return 'success'


@app.route('/media/popular/shows/details/<imdb_id>/save_for_later', methods=['POST'])
def save_for_later_show(imdb_id):
    """Add/Remove show (TMDB API) to/from Save for Later database"""

    logged_in_user = crud.get_user_by_email(request.json.get('userEmail'))
    user_id = logged_in_user.user_id
    print(user_id)
    if crud.get_media_by_imdb_id(imdb_id) == None:
        media_title = request.json.get('title')
        media_poster_path = request.json.get('poster_path')
        media_overview = request.json.get('overview')
        media_imdb_id = request.json.get('imdb_id')

        
        media_to_db = crud.create_media(
                        media_type='series', 
                        title=media_title, 
                        overview=media_overview, 
                        poster_path=media_poster_path, 
                        imdb_id=media_imdb_id)
               
        db.session.add(media_to_db)
        db.session.commit()  

    media = crud.get_media_by_imdb_id(imdb_id)

    save_later_by_media_user_id = crud.get_save_for_later_by_media_user_id(user_id, media.media_id)

    if save_later_by_media_user_id:
        db.session.delete(save_later_by_media_user_id)
    else:
        save_for_later = crud.create_save_for_later(user_id=user_id, media_id=media.media_id)    
        db.session.add(save_for_later)

    db.session.commit()    

    return 'success'


@app.route('/media/popular/movies/details/<comment_id>/delete_comment', methods=['POST'])
def delete_comment_popular_movie(comment_id):


    comment = crud.get_comment_by_id(comment_id)
    user_who_commented = comment.user
    user_id_who_commented = str(user_who_commented.user_id)
   
    crud.delete_comment_by_id(comment_id)


    return user_id_who_commented

@app.route('/media/popular/shows/details/<comment_id>/delete_comment', methods=['POST'])
def delete_comment_popular_show(comment_id):


    comment = crud.get_comment_by_id(comment_id)
    user_who_commented = comment.user
    user_id_who_commented = str(user_who_commented.user_id)
   
    crud.delete_comment_by_id(comment_id)


    return user_id_who_commented    

@app.route('/search')
def search_media():
    """Search a media using Rapid API (IMDB)"""

    url = "https://movie-database-alternative.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": os.environ['RAPID_API_KEY'],
        "X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com"
    }
    searched_media = request.args.get("s")
    query_string = {"s": searched_media, "r": "json", "page": "1"}
    response = requests.request(
        "GET", url, headers=headers, params=query_string)
    data = response.json()

   # session[searched_media] = data['Search']

    return data


@app.route('/media/details/<imdb_id>')
def get_specific_media(imdb_id):
    """Makes an API request to get a specific media by its ID (IMDB)"""

    url = "https://movie-database-alternative.p.rapidapi.com/"

    query_string = {"r": "json", "i": imdb_id}

    headers = {
        "X-RapidAPI-Key": os.environ['RAPID_API_KEY'],
        "X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com"
    }
    response = requests.request(
        "GET", url, headers=headers, params=query_string)

    data = response.json()
    media_info = crud.get_media_by_imdb_id(imdb_id)

    if 'user_email' in session:
        user = crud.get_user_by_email(session['user_email'])
    else:
        user = False  


    media = {'title': data['Title'], 
             'year': data['Year'], 
             'poster_path': data['Poster'], 
             'overview': data['Plot'], 
             'imdb_id': data['imdbID'],
             'media_type': data['Type'] }


    return render_template('media_details.html', media=media, media_info=media_info, user=user)


@app.route('/media/details/<imdb_id>/save_for_later', methods=['POST'])
def save_for_later_media(imdb_id):
    """Add/Remove media (IMDB) to/from Save for Later database"""

    logged_in_user = crud.get_user_by_email(request.json.get('userEmail'))
    user_id = logged_in_user.user_id
    
    if crud.get_media_by_imdb_id(imdb_id) == None:
        media_title = request.json.get('title')
        media_poster_path = request.json.get('poster_path')
        media_overview = request.json.get('overview')
        media_imdb_id = request.json.get('imdb_id')
        media_type = request.json.get('media_type')
        
        media_to_db = crud.create_media(
                        media_type=media_type, 
                        title=media_title, 
                        overview=media_overview, 
                        poster_path=media_poster_path, 
                        imdb_id=media_imdb_id)
        print(media_to_db)                   
        db.session.add(media_to_db)
        db.session.commit()  

    media = crud.get_media_by_imdb_id(imdb_id)

    save_later_by_media_user_id = crud.get_save_for_later_by_media_user_id(user_id, media.media_id)

    if save_later_by_media_user_id:
        db.session.delete(save_later_by_media_user_id)
    else:
        save_for_later = crud.create_save_for_later(user_id=user_id, media_id=media.media_id)    
        db.session.add(save_for_later)

    db.session.commit()    

    return 'success'


@app.route('/media/details/<comment_id>/update_like', methods=['POST'])
def like_comment(comment_id):
    """Like/Unlike a comment and update in the database (IMDB)"""

    # user_id = request.json.get('userID')
    logged_in_user = crud.get_user_by_email(request.json.get('userEmail'))
    user_id = logged_in_user.user_id
    print("\n"*5)
    print("User ID", user_id)
   # like_id = request.json.get('likeID')

    like_by_id = crud.get_like_by_comment_user_id(comment_id=comment_id, user_id=user_id)
    print("Like exists?", like_by_id)
    print("\n"*5)

    if like_by_id:
        db.session.delete(like_by_id)  
    else:      
        like = crud.create_like(user_id=user_id, 
                            comment_id=comment_id)    
        db.session.add(like)
    db.session.commit()

    number_likes = crud.get_like_numbers_by_comment_id(comment_id)
    print(number_likes)

    # if the like exists for that comment, delete it from the datavase, else add the like to the db.

    return str(number_likes)


@app.route('/media/details/<comment_id>/delete_comment', methods=['POST'])    
def delete_comment(comment_id):

    comment = crud.get_comment_by_id(comment_id)
    user_who_commented = comment.user
    user_id_who_commented = str(user_who_commented.user_id)
    print(comment)
    crud.delete_comment_by_id(comment_id)


    return user_id_who_commented

@app.route('/media/details/')
def show_details():
    return render_template('media_details.html')

@app.route('/media/details/<media_id>/comment', methods=['POST'])
def comment_media(media_id):
    """Submit a comment for a specific show 
    from Rapid API (IMDB) and save both on the database"""

    media_title = request.json.get('title')
    media_year = request.json.get('year')
    media_poster_path = request.json.get('poster_path')
    media_overview = request.json.get('overview')
    media_imdb_id = request.json.get('imdb_id')
    media_rate = request.json.get('user_rate')
    media_comment = request.json.get('user_comment')
    media_type = request.json.get('media_type')

    user = crud.get_user_by_email(session['user_email'])
    media = crud.get_media_by_imdb_id(media_id)
    if media:
        user_comment = crud.create_comment(
                            comment=media_comment,
                            review=media_rate, 
                            user_id=user.user_id, 
                            media_id=media.media_id)
        db.session.add(user_comment)
        db.session.commit()
    else:
        media_to_db = crud.create_media(
                            media_type=media_type, 
                            title=media_title, 
                            overview=media_overview, 
                            poster_path=media_poster_path, 
                            imdb_id=media_imdb_id)
        print(media_to_db)                   
        db.session.add(media_to_db)
        db.session.commit()      

        user_comment = crud.create_comment(
                            comment=media_comment, 
                            review=media_rate, 
                            user_id=user.user_id, 
                            media_id=media_to_db.media_id)

        db.session.add(user_comment)
        db.session.commit()
    
    comment_id = user_comment.comment_id
    total_likes = crud.get_like_numbers_by_comment_id(comment_id)

    comment_by_user = {
                        "comment_id": comment_id,
                        "comment": user_comment.comment,
                        "review": user_comment.review,
                        "user_name": user_comment.user.full_name,
                        "user_id": user_comment.user_id,
                        "media_id": user_comment.media_id,
                        "total_likes": total_likes
                        }

    return comment_by_user


@app.route('/login')
def login_page():
    """Show log in page"""

    if 'user_email' in session:
        user = crud.get_user_by_email(session['user_email'])
        user_id = user.user_id
        return redirect(f'/profile/{user_id}')
    else:    
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    """User log in"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user and password == user.password:
        flash(f'Hi, {user.full_name}')
        session['user_email'] = user.email
        return redirect('/')
    else:
        flash(f'Email or password incorrect')
        return redirect('login')

@app.route('/login/google-oauth', methods=['POST'])
def google_OAuth():

    GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
    
    # client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

    ID_TOKEN = request.form["credential"]

    # Verify that token comes in cookie and body, and they are the same
    csrf_token_cookie = request.cookies.get('g_csrf_token')
    if not csrf_token_cookie:
        print("***ERROR: No CSRF token in Cookie***")
    csrf_token_body = request.form.get('g_csrf_token')
    if not csrf_token_body:
        print("***ERROR: No CSRF token in post body***")
    if csrf_token_cookie != csrf_token_body:
        print("***ERROR: Failed to verify double submit cookie.")

    # The verify_oauth2_token function verifies the JWT signature, the aud claim, and the exp claim. 
    try:
        # Gets the decoded JWT using Google API client lib
        google_data = google_id_token.verify_oauth2_token(ID_TOKEN, google_requests.Request(), GOOGLE_CLIENT_ID)

        # ----- INTERNAL OPERATIONS ---
        # ID token is valid. Get the user's Google Account ID from the decoded token.
        password = google_data['sub'] # Will operate as password
        email = google_data['email'] # email
        full_name = google_data['given_name'] # full name

        user = crud.get_user_by_email(email)

        if user:
            flash(f"Hi, {full_name}")
            return redirect('/')
        else:
            user = crud.create_user(full_name=full_name,email=email, password=password)    
            db.session.add(user)
            db.session.commit()

        session['user_email'] = email

    except ValueError:
        # Invalid token
        print("****ERROR: Invalid Token*****")
        # pass
    return redirect("/login")

@app.route('/logout')
def logout():

    session.pop('user_email',None)
    flash("You're logged out!")
    return redirect('/')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')


@app.route('/signup', methods=["POST"])
def register_user():
    """Create a new user"""

    fullname = request.form.get("full_name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm-password")

    user = crud.get_user_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again.")
        return redirect('/signup')
    else:
        if password == confirm_password:
            user = crud.create_user(fullname, email, password)
            db.session.add(user)
            db.session.commit()
            flash("Account created! Please, log in.")
        else:
            flash("Password do not match. Try again.")
            return redirect('signup')

    return render_template('login.html')


@app.route('/profile/<user_id>')
def show_profile(user_id):
    """Show users profile"""

    user = crud.get_user_by_email(session['user_email'])
    user_id = user_id

    return render_template('profile.html', user=user)


@app.route('/profile/<user_id>/friend')
def show_friend_profile(user_id):
    """Show users profile"""

    friend_user = crud.get_user_by_id(user_id)
    logged_in_user = crud.get_user_by_email(session['user_email'])

    is_following = friend_user in logged_in_user.following

    return render_template('profile.html', user=friend_user, is_following=is_following)    

@app.route('/profile/<user_id>/friend/update_follow', methods=["POST"])
def update_followrs(user_id):

    logged_in_user = crud.get_user_by_email(session['user_email'])
    user_to_follow = crud.get_user_by_id(user_id)

    if user_to_follow in logged_in_user.following:
        logged_in_user.following.remove(user_to_follow)

    else:
        logged_in_user.following.append(user_to_follow)


    db.session.commit()

    return 'success'

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
