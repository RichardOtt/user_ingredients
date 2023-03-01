from flask import Flask, request, render_template
from flask.json import jsonify
import json
import random

app = Flask(__name__)
#app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

@app.route('/', methods=['GET'])
def gen_json():
    protein = ['beef', 'chicken', 'shrimp', 'tofu']
    veg = ['onion', 'broccoli', 'potato', 'rice',
           'pumpkin', 'celery', 'carrot', 'peas', 'spinach',
           'tomato', 'mushroom', 'cabbage', 'cauliflower']
    spice = ['garlic', 'ginger', 'salt', 'cumin', 'paprika',
             'cinnamon', 'thyme']

    ingredients = []
    # 75% will have one random protein
    if random.random() < 0.75:
        pick = random.randint(0, len(protein)- 1)
        ingredients.append(protein[pick])

    # 1 to 3 veg, equal prob
    n_veg = random.randint(1,3)
    ingredients.extend(random.sample(veg, n_veg))

    # 0 to 2 spice, equal prob
    n_spice = random.randint(0,2)
    ingredients.extend(random.sample(spice, n_spice))

    # allow excluded ingredient
    # 1/3 have an ingredient excluded
    # need to be sure it's _not_ in the ingredients
    # going to be lazy, if it picks one present we'll just skip
    exclude = []
    if random.random() < 0.33:
        ex = random.sample(protein + veg + spice, 1)[0]
        if ex not in ingredients:
            exclude.append(ex)

    # get a random person out of the list of 100
    with open('static/people.json') as f:
        people = json.load(f)
        
    person = people[random.randint(0, len(people)-1)]

    person['include'] = ingredients

    if exclude:
        person['exclude'] = exclude

    return jsonify(person)
