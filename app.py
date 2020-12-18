from flask import Flask, render_template, url_for, request
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json

app = Flask(__name__)


def get_print_link(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    searched_word = 'Print'
    results = soup.body.find_all(string=re.compile(
        '.*{0}.*'.format(searched_word)), recursive=True)
    return results[0].parent['href']


def get_ingredients_from_link(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # recipe_name = soup.find_all('h3', 'wprm-recipe-name')[0].text.strip()
    recipe_name = 'test'
    ingredients = soup.find_all('li', "wprm-recipe-ingredient")
    all_ingredients = []

    for i in ingredients:
        try:
            amount = i.find_all("span", "wprm-recipe-ingredient-amount")
            amount = amount[0].text

        except:
            amount = 'no amount'

        try:
            unit = i.find_all("span", "wprm-recipe-ingredient-unit")
            unit = unit[0].text

        except:
            unit = 'no unit'

        try:
            name = i.find_all("span", "wprm-recipe-ingredient-name")
            name = name[0].text

        except:
            name = 'no name'

        all_ingredients.append({'url': url,
                                'recipe_name': recipe_name,
                                'amount': amount,
                                'unit': unit,
                                'name': name})

    return all_ingredients


def add_ingredients_to_dictionary(formatted_ingredient, shopping_list):
    #     print(formatted_ingredient)
    ingredient = formatted_ingredient['name']
    amount = formatted_ingredient['amount']
    unit = formatted_ingredient['unit']
    amount_unit = "{}({})".format(amount, unit)
    if ingredient in shopping_list:
        shopping_list[ingredient] = shopping_list[ingredient] + \
            ' + ' + amount_unit
    else:
        shopping_list[ingredient] = amount_unit
    return shopping_list


def get_ingredients_flask(my_input):
    print_links = []
    for blog in my_input:
        print_links.append(get_print_link(blog))

    not_working = []
    all_ingredients = []
    for link in print_links:
        ingredients = get_ingredients_from_link(link)
        if len(ingredients) == 0:
            not_working.append(link)
        else:
            all_ingredients.append(ingredients)

    results_flattened = [
        item for sublist in all_ingredients for item in sublist]
    shopping_list = {}
    my_list = [add_ingredients_to_dictionary(
        x, shopping_list) for x in results_flattened]
    # for site in not_working:
    # print('So sorry, working on getting info from', site)
    return shopping_list


def run_the_thing(input):
    try:
        recipe_links = json.loads(input)
        return get_ingredients_flask(recipe_links)
    except:
        return "Oh shoot! Something is broken! "


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # get `content` from form
        task_content = request.form['content']
        gobs_program = run_the_thing(task_content)
        return render_template('result.html', passed=gobs_program)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
