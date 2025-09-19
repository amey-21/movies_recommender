from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f1b0cc62f033a845bc068c1d0b5ee82e&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    recommended = []
    posters = []
    urls = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
        urls.append(f"https://www.themoviedb.org/movie/{movie_id}")
    return recommended, posters, urls

@app.route('/', methods=['GET', 'POST'])
def index():
    movie_titles = movies['title'].values
    if request.method == 'POST':
        selected_movie = request.form['movie']
        names, posters, urls = recommend(selected_movie)
        return render_template('recommendations.html', movie=selected_movie, names=names, posters=posters, urls=urls)
    return render_template('index.html', movie_list=movie_titles)

# if __name__ == '__main__':
    # app.run(port = 8000, debug=True)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # fallback for local
    app.run(host="0.0.0.0", port=port)
