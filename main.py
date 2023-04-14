# SEE IT IN ACTION! https://openai-story-to-image.chadallen.repl.co/
# https://github.com/chadallen/openai-story-to-image
# Coolest part about this was getting GPT4 to make the web UI look nice

from flask import Flask, render_template_string, request
import requests
import os

# Get API key
api_key = os.environ['api_key']

def generate_image(temperature):
    # Use GPT-3 to generate a description of a drawing with a fairy-tale flavor
    prompt = 'Here is the first sentence of an original fairy tale I just made up: Once upon a time,'
    model = 'davinci'

    response = requests.post('https://api.openai.com/v1/completions', json={
        "model": model,
        "prompt": prompt,
        "max_tokens": 500,
        "stop": '.',
        "temperature": float(temperature),
        "n": 1
    }, headers={'Authorization': f'Bearer {api_key}'})

    description = response.json()['choices'][0]['text'].strip()
    full_description = 'a story book illustration of ' + description

    # Use DALL-E 2 to generate an image based on the description
    url = 'https://api.openai.com/v1/images/generations'
    data = {"prompt": full_description, "model": "image-alpha-001"}
    response = requests.post(url, json=data, headers={'Authorization': f'Bearer {api_key}'})
    image_url = response.json()['data'][0]['url']

    return description, image_url

# Barebones Flask
app = Flask(__name__)

@app.template_filter('float')
def float_filter(value):
    return float(value)

@app.route('/', methods=['GET', 'POST'])
def index():
    temperature = 0.5
    if request.method == 'POST':
        temperature = request.form.get('temperature')
    description, image_url = generate_image(temperature)
    return render_template_string('''
        <!doctype html>
        <html lang="en">
          <head>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">

            <!-- Materialize CSS -->
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">

            <!-- Custom CSS -->
            <style>
                body {
                    font-family: 'Roboto', sans-serif;
                    background-color: #f5f5f5;
                }
                .container {
                    max-width: 960px;
                }
                .card {
                    margin-top: 50px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                .card img {
                    object-fit: cover;
                    height: 300px;
                }
                .loader {
                    border: 4px solid #f3f3f3;
                    border-radius: 50%;
                    border-top: 4px solid #3498db;
                    width: 40px;
                    height: 40px;
                    animation: spin 2s linear infinite;
                    margin: 0 auto;
                    display: none;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
            <script>
                function showLoader() {
                    document.getElementById("loader").style.display = "block";
                }
            </script>
            <title>Fairy Tale Image Generator</title>
          </head>
          <body>
            <div class="container">
                <div class="card">
                    
                        <img src="{{ image_url }}">
                  
                    <div class="card-content">
                        <span class="card-title">Once upon a time, {{ description }}</span>
                        <div class="input-field col s12">
                            <select name="temperature" id="temperature" form="form">
                                <option value="0.1" {% if temperature == 0.1 %}selected{% endif %}>0.1</option>
                                <option value="0.2" {% if temperature == 0.2 %}selected{% endif %}>0.2</option>
                                <option value="0.3" {% if temperature == 0.3 %}selected{% endif %}>0.3</option>
                                <option value="0.4" {% if temperature == 0.4 %}selected{% endif %}>0.4</option>
                                <option value="0.5" {% if temperature == 0.5 %}selected{% endif %}>0.5</option>
                                <option value="0.6" {% if temperature == 0.6 %}selected{% endif %}>0.6</option>
                                <option value="0.7" {% if temperature == 0.7 %}selected{% endif %}>0.7</option>
                                <option value="0.8" {% if temperature == 0.8 %}selected{% endif %}>0.8</option>
                                <option value="0.9" {% if temperature == 0.9 %}selected{% endif %}>0.9</option>
                            </select>
                            <label>Temperature</label>
                        </div>
                    </div>
                    <div class="card-action">
                        <form method="post" id="form">
                            <input type="submit" value="Generate another" class="btn" onclick="showLoader()">
                        </form>
                    </div>
                </div>
                <div id="loader" class="loader"></div>
            </div>

            <!-- Materialize JavaScript -->
            <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    var elems = document.querySelectorAll('select');
                    var instances = M.FormSelect.init(elems);
                });
            </script>
          </body>
        </html>
    ''', description=description, image_url=image_url, temperature=temperature)

app.run(host='0.0.0.0', port=81)
