from flask import Flask,render_template,request,send_file
from data_cleaning import clean_words
from save_contributed_data import Contribution,CheckURL
from check_news import Check


app = Flask(__name__)

C = Check()
Con = Contribution("dataset/contributed_dataset/contributed_data.csv")
Curl = CheckURL()

#TODO Change in Home page
@app.route('/')
def index():
    return render_template('home.html', title = 'Home')

@app.route('/home',)
def home():
    return render_template('home.html',title ='Home')

@app.route('/predict', methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        model = request.form['model']
        news = request.form['news']
        cleaned_news = clean_words(news)
        if (not (cleaned_news and not cleaned_news.isspace())):
            return render_template('home.html', title='Home', enteredmodel=model, prediction=None)

        elif cleaned_news:
            if model == "Logistic Regression":
                ans = C.lr(news)
                return render_template('home.html', title='Home', prediction=ans,
                                       enteredmodel=model, enterednews=news)
            elif model == "Decision Tree Classifier":
                ans = C.dtc(news)
                return render_template('home.html', title='Home', prediction=ans,
                                       enteredmodel=model, enterednews=news)
            elif model == "Gradient Boosting Classifier":
                ans = C.gbc(news)
                return render_template('home.html', title='Home', prediction=ans,
                                       enteredmodel=model, enterednews=news)
            elif model == "Random Forest Classifier":
                ans = C.rfc(news)
                return render_template('home.html', title='Home', prediction=ans,
                                       enteredmodel=model, enterednews=news)
        else:
            return render_template('home.html', prediction=None)


#TODO Change in Contribution page
@app.route('/contribute-data',)
def contribute_data():
    return render_template('contribute-data.html',title = 'Contribute Data')

@app.route('/contribute-data', methods=['POST','GET'])
def contribute():
    if request.method == 'POST':
        contributor_ip = request.remote_addr
        contributed_news = request.form['contributednews']
        contributed_news_source = request.form['contributednewssource']
        contributed_label = request.form['contributedlabel']
        # print(contributed_label)
        # print(contributed_label,contributed_news_source,contributed_news)
        if contributed_news and contributed_news_source and contributed_label != "None":
            if Curl.is_url(contributed_news_source):
                url = Curl.get_url()
                Con.open_csv()
                Con.add_to_csv(contributed_news, contributed_label, url, contributor_ip)
                Con.close_csv()
                return render_template('contribute-data.html', title='Contribute Data', response='Successfully Saved')
            else:
                return render_template('contribute-data.html', title='Contribute Data',     lastcontributednews=contributed_news,
                                       lastcontributedlabel=contributed_label,response='Invalid Source')
        else:
            return render_template('contribute-data.html', title='Contribute Data', lastcontributednews=contributed_news,
                                   lastcontributednewssource=contributed_news_source,
                                   response='Missing Fields')

#TODO Change in Working page
@app.route('/how-it-works')
def workflow():
    return render_template('how-it-works.html',title = 'How It Works?')

#TODO Change in Jupyter Notebook page
@app.route('/jupyter-notebook')
def jupyter_notebook():
    return render_template('jupyter-notebook.html',title = 'Jupyter Notebook')

#TODO Change in Report page
@app.route('/project-report')
def project_report():
    return render_template('project-report.html',title = 'Project Report')

#TODO Change Admin page
@app.route('/admin')
def admin():
    return render_template('admin.html',title = 'Admin')

#TODO Change in About page
@app.route('/about')
def about():
    return render_template('about.html',title = 'About')

@app.route('/download')
def download_file():
	path = "dataset/contributed_dataset/contributed_data.csv"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)

@app.route('/upload', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f"trained_models/{f.filename}")
        return render_template("admin.html", name = f.filename)



if __name__ == '__main__':
    app.run(debug=True)