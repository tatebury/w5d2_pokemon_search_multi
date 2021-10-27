
   
from flask import render_template, request
import requests
from app import app
from .form import PokeNameForm

@app.route('/')
def home():
    return render_template('home.html.j2')

# @app.route('/login', methods=['GET','POST'])
# def login():
#     form = PokeNameForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         #do Login stuff
#         email = request.form.get("email").lower()
#         password = request.form.get("password")
#         if email in app.config.get("REGISTERED_USERS") and \
#             password == app.config.get("REGISTERED_USERS").get(email).get('password'):
#             return f"Login success Welcome {app.config.get('REGISTERED_USERS').get(email).get('name')}"
#         error_string = "Invalid Email password combo"
#         return render_template('login.html.j2', error = error_string, form=form)

#     return render_template('login.html.j2', form=form)

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    form = PokeNameForm()
    poke_list = requests.get("https://pokeapi.co/api/v2/pokemon/")
    if request.method == 'POST':
        names = request.form.get('name').split(',')
        pokemon_info = []
        for name in names:
            name = name.strip().lower()
            url = f'https://pokeapi.co/api/v2/pokemon/{name}'
            response = requests.get(url)
            if response.ok:
                #request worked
                if not response.json():
                    return "We had an error loading your pokemon likely the name is not in the pokemon database"
                pokemon = response.json()

                single_poke={
                    'name': pokemon['name'],
                    'base_xp': pokemon['base_experience'],
                    'hp': pokemon['stats'][0]['base_stat'],
                    'defense': pokemon['stats'][2]['base_stat'],
                    'attack': pokemon['stats'][1]['base_stat'],
                    'url': pokemon['sprites']['front_shiny']
                }
                pokemon_info.append(single_poke)

            
            else:
                return "Houston We have a problem"
                # The request fail

        return render_template('pokemon.html.j2', pokemon=pokemon_info, form=form)     
        

    return render_template('pokemon.html.j2', form=form)