from flask import Flask, request, render_template
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    ingredients = request.form.get('ingredients').lower()
    app_id = 'APP_ID'
    app_key = 'APP_KEY'
    base_url = 'https://api.edamam.com/search'
    params = {
        'q': ingredients,
        'app_id': app_id,
        'app_key': app_key,
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        matched_recipes = [(hit['recipe']['label'], hit['recipe']['url'], hit['recipe'].get('ingredientLines')) for hit
                           in data['hits']]
        return render_template('results.html', recipes=matched_recipes)
    else:
        return "Error: Unable to fetch recipes"


@app.route('/recipe/<int:index>')
def show_recipe(index):
    recipes = request.args.get('recipes', None)
    if recipes:
        recipes = eval(recipes)
        if 0 <= index < len(recipes):
            recipe = recipes[index]
            recipe_label = recipe[0]
            recipe_url = recipe[1]
            ingredients = recipe[2]
            return render_template('recipe.html', recipe_label=recipe_label, recipe_url=recipe_url,
                                   ingredients=ingredients)
    return "Error: Recipe not found"


if __name__ == '__main__':
    app.run(debug=True)
