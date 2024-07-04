import time

from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

# Load data
df = pd.read_csv('disasters.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    entities = df['Entity'].unique()
    if request.method == 'POST':
        entity = request.form['entity']
        century = request.form['century']
        return plot_data(entity, century)
    # time.sleep(2)
    return render_template('index.html', entities=entities)

def plot_data(entity, century):
    filtered_df = df[df['Entity'] == entity]

    if century == '20th':
        filtered_df = filtered_df[(filtered_df['Year'] >= 1900) & (filtered_df['Year'] <= 1960)]
    elif century == '21st':
        filtered_df = filtered_df[(filtered_df['Year'] >= 1961) & (filtered_df['Year'] <= 2017)]

    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df['Year'], filtered_df['Deaths'], marker='o')
    plt.title(f'{entity} Deaths Over Time')
    plt.xlabel('Year')
    plt.ylabel('Deaths')
    plt.grid(True)

    plot_filename = f'{entity}_{century}_plot.png'
    plot_path = os.path.join(app.config['UPLOAD_FOLDER'], plot_filename)
    # plot_path = os.path.join(app.config['UPLOAD_FOLDER'], )
    plt.savefig(plot_path)
    plt.close()
    time.sleep(2)
    # print("plot_path: ",plot_filename)
    table_data = filtered_df[['Year', 'Deaths']].to_dict(orient='records')

    return render_template('plot.html', entity=entity, plot_path=plot_filename,table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)
