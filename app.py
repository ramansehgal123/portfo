from flask import Flask, render_template, url_for, request, redirect
import random
from bs4 import BeautifulSoup
app = Flask(__name__)
import csv


@app.route('/')
def my_home():
    
    return render_template('./index.html')

@app.route('/thankyou.html')
def thankyou():
    iframe_src = "./static/storyline_package/story.html"  # Replace with your HTML package URL or path
    return render_template('thankyou.html', iframe_src=iframe_src)

@app.route('/process_value', methods=['POST'])
def process_value():
    value = request.form['value']
    print(type(value))
    soup = BeautifulSoup(value, 'html.parser')
    div_elements = soup.find_all('div', attrs={'data-acc-text': True})

    elements = str(div_elements)

    print(elements)
        
    # Do something with the value, such as printing it
    #print("Received value:", value)
    return elements
    


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email}, {subject}, {message}')

def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return 'did not save to database'
    else:
        return 'something went wrong. try again!'


# @app.route('/favicon.ico')
# def blog():
#     return 'There are my thoughts on blogs'


if __name__ == '__main__':
    app.run(debug=True)
