from flask import Flask, render_template_string, request, redirect, url_for
import re

# Initialize the Flask application
app = Flask(__name__)

# Sample recipe data stored in a dictionary
# Each recipe has a unique key (recipe_id) and contains name, ingredients list, and instructions
recipes = {
    "midnight-ramen": {
        "name": "Midnight Ramen",
        "ingredients": ["instant ramen", "egg", "green onions", "hot sauce"],
        "instructions": "1. Boil water\n2. Cook noodles\n3. Add toppings"
    }
}

# HTML Templates as strings
# Instead of using separate template files, this app uses template strings with Flask's render_template_string
# The base_template_start contains the opening HTML, head, styles, and beginning of the body
base_template_start = '''
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Recipe Website{% endblock %}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        header {
            margin-bottom: 20px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }
        nav a {
            margin-right: 15px;
            text-decoration: none;
            color: #0066cc;
        }
        .recipe-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .recipe-card {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            text-align: center;
        }
        form div {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input, textarea, select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background-color: #0066cc;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <header>
        <h1>Recipe Collection</h1>
        <nav>
            <a href="{{ url_for('index') }}">Home</a>
            <a href="{{ url_for('add_recipe') }}">Add Recipe</a>
        </nav>
    </header>
    
    <main>
'''

# The base_template_end contains the closing tags for the main content and HTML document
base_template_end = '''
    </main>
</body>
</html>
'''

# Custom Jinja2 filter to convert newlines to HTML line breaks
# This allows multiline text like instructions to display properly in HTML
@app.template_filter('nl2br')
def nl2br(value):
    return value.replace('\n', '<br>')

# Routes Definition
# Route for the homepage
@app.route('/')
def index():
    # HTML content for the home page showing a grid of recipe cards
    content = '''
    <h2>Our Recipes</h2>
    
    <div class="recipe-grid">
        {% for recipe_id, recipe in recipes.items() %}
            <div class="recipe-card">
                <h3>{{ recipe.name }}</h3>
                <a href="{{ url_for('recipe', recipe_id=recipe_id) }}">View Recipe</a>
            </div>
        {% endfor %}
    </div>
    '''
    
    # Combine the template parts (start + content + end) to create the full HTML page
    full_template = base_template_start + content + base_template_end
    # Render the template, passing in the recipes dictionary
    return render_template_string(full_template, recipes=recipes)

# Route for viewing a specific recipe by its ID
@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    # Get the recipe data from the recipes dictionary using the recipe_id
    recipe_data = recipes.get(recipe_id)
    # If the recipe doesn't exist, return a 404 error
    if not recipe_data:
        return "Recipe not found", 404
        
    # HTML content for the recipe detail page
    content = '''
    <h2>{{ recipe.name }}</h2>
    
    <section>
        <h3>Ingredients</h3>
        <ul>
            {% for ingredient in recipe.ingredients %}
                <li>{{ ingredient }}</li>
            {% endfor %}
        </ul>
    </section>
    
    <section>
        <h3>Instructions</h3>
        <p>{{ recipe.instructions|nl2br }}</p>
    </section>
    
    <a href="{{ url_for('index') }}">Back to All Recipes</a>
    '''
    
    # Combine the template parts
    full_template = base_template_start + content + base_template_end
    # Render the template, passing in the specific recipe data
    return render_template_string(full_template, recipe=recipe_data)

# Route for adding a new recipe
# Handles both GET (display form) and POST (process form submission) requests
@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    # If the request is a form submission (POST)
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        # Split ingredients by newline to create a list
        ingredients = request.form['ingredients'].split('\n')
        instructions = request.form['instructions']
        
        # Create a URL-friendly ID from the recipe name
        # Remove special characters and replace spaces with hyphens
        recipe_id = re.sub(r'[^\w\s]', '', name.lower()).replace(' ', '-')
        
        # Add the new recipe to the recipes dictionary
        recipes[recipe_id] = {
            'name': name,
            'ingredients': ingredients,
            'instructions': instructions
        }
        
        # Redirect to the newly created recipe page
        return redirect(url_for('recipe', recipe_id=recipe_id))
    
    # If the request is GET, display the form to add a new recipe
    content = '''
    <h2>Add a New Recipe</h2>
    
    <form method="post">
        <div>
            <label for="name">Recipe Name:</label>
            <input type="text" id="name" name="name" required>
        </div>
        
        <div>
            <label for="ingredients">Ingredients (one per line):</label>
            <textarea id="ingredients" name="ingredients" rows="5" required></textarea>
        </div>
        
        <div>
            <label for="instructions">Instructions:</label>
            <textarea id="instructions" name="instructions" rows="5" required></textarea>
        </div>
        
        <button type="submit">Add Recipe</button>
    </form>
    '''
    
    # Combine the template parts
    full_template = base_template_start + content + base_template_end
    # Render the template
    return render_template_string(full_template)

# Run the application if this file is executed directly
# The debug=True parameter enables debug mode, showing detailed error messages
# and automatically reloading the server when code changes
if __name__ == '__main__':
    app.run(debug=True)