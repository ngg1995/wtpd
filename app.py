import numpy as np
import pandas as pd
import os
import json
import time

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

if not os.path.exists('responses'):
    os.makedirs('responses')

# Table structure

table = pd.DataFrame({
    "Direct": {
        "Low":"pl", 
        "High":"ph", 
        "Medium":None, 
        "Uncertain":"pu"
        },
    "Risk": {
        "Low":"rl", 
        "High":"rh", 
        "Medium":"rb", 
        "Uncertain":"ru"
    },
    "Number+Risk": {
        "Low":"nrl", 
        "High":"nrh", 
        "Medium":"nrb",
        "Uncertain":None
        },
    "Number": {
        "Low":"nl", 
        "High":"nh", 
        "Medium":"nb",
        "Uncertain":None
        },
    "Verbose": {
        "Low":"vl", 
        "High":"vh", 
        "Medium":"vb", 
        "Uncertain":"vu"
        }
})

print(table)

def select_frames():
    rng = np.random.default_rng()

    # Initialize the set to store selected values
    selected_values = set()

    # Select a value from each row
    for r,row in table.iterrows():
        c = rng.choice(table.columns)
        while table.loc[r,c] is None:
            c = rng.choice(table.columns)
        selected_values.add((r,c))

    # select value from each columm
    for c,col in table.T.iterrows():
        r = rng.choice(table.index)
        while table.loc[r,c] is None:
            r = rng.choice(table.index)
        selected_values.add((r,c))

    # make upto 10 values
    while len(selected_values) <10:
        r = rng.choice(table.index)
        c = rng.choice(table.columns)
        if table.loc[r,c] is not None:
            selected_values.add((r,c))
                    
    return selected_values


def make_templates(selected_values):
    path = [f"{table.loc[r,c]}" for r,c in selected_values]
    p = lambda ref: f"location.href='#p{ref}'"
    d = lambda ref: f"location.href='#d{ref}'"
    links = {
        'patient_start': p(path[0]),
    }
    for frame in table.to_numpy().ravel():
        if frame in path:
            i = path.index(frame)
            if i == 0:
                links[f'p{frame}_back'] = "location.href='#patient-screening'"
            else:
                links[f'p{frame}_back'] = p(path[i-1])

            if i == len(path)-1:
                links[f'p{frame}_next'] = "location.href='#retro1'"
            else:
                links[f'p{frame}_next'] = p(path[i+1])
        else:
            links[f'p{frame}_back'] = "location.href='#home"
            links[f'p{frame}_next'] = "location.href='#home"

    return links
# frames = select_frames()
# print(frames)
# print(make_templates(frames))

# path = make_templates([(r,c) for r in table.index for c in table.columns if table.loc[r,c] is not None])


@app.route('/')
def home():
    frames = select_frames()
    print(frames)
    path = make_templates(frames)
    return render_template('/index.html',**path)

@app.route('/all')
def showall():
    path = make_templates([(r,c) for r in table.index for c in table.columns if table.loc[r,c] is not None])
    print(path)
    return render_template('/index.html',**path)

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json  # Retrieve JSON data from the POST request
    print(f"Received form data: {data}")
    # Get current Unix time as a string
    unix_time = str(int(time.time()))
    
    # Define the path to save the response
    file_path = os.path.join('responses', f'{unix_time}.json')
    
    # Write the data to a JSON file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({"status": "success", "received_data": data})


if __name__ == "__main__":
    app.run(port=8000, debug=True)
