from flask import Flask, render_template, request
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

rf_model = pickle.load(open("random_forest_model.pkl","rb"))
standard_scaler = pickle.load(open("standard_scaler.pkl","rb"))
numeric_input = ['age','bmi','children']
app = Flask(__name__)

@app.route('/')
def home():

    return render_template("index.html")


@app.route('/recommend',  methods=["POST"])
def recommend():
    age = request.form.get('age')
    bmi = request.form.get('bmi')
    children = request.form.get('children')
    region = request.form.get("region").lower()
    gender = request.form.get("gender").lower()
    smoker = request.form.get("smoker").lower()

    def result(age, bmi, children, smoker, gender, region):
        if smoker=="yes":
            smoker_val=1
        else:
            smoker_val=0
        
        if region=="northeast":
            ne = 1
            nw = 0
            se = 0
            sw = 0
            
        elif region=='northwest':
            ne = 0
            nw = 1
            se = 0
            sw = 0
            
        elif region=='southeast':
            ne = 0
            nw = 0
            se = 1
            sw = 0
            
        elif region=='southwest':
            ne = 0
            nw = 0
            se = 0
            sw = 1
        
        if gender=='male':
            gender_val=1
        else:
            gender_val=0
        
        new = {
        'age': age,
        'bmi': bmi,
        'children': children,
        'smoker_val': smoker_val,
        'sex_val': gender_val,
        'northeast': ne,
        'northwest': nw,
        'southeast': se,
        'southwest': sw
        }
        new = pd.DataFrame([new])
        new[numeric_input] = standard_scaler.transform(new[numeric_input])
        return rf_model.predict(new)

    print(age, bmi, children, smoker, gender, region)
    ans=round(result(age, bmi, children, smoker, gender, region)[0], 2)
    return render_template("index.html", ans=ans)


if __name__=="__main__":
    app.run(debug=True)