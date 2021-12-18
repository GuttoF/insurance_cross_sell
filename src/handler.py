import os
import pickle
import pandas as pd
from flask import Flask, request, Response
from health_insurance.HealthInsurance import HealthInsurance


#path = '/home/gutto/Repos/Insurance-Cross-Sell/src/model/'
path = 'model/'

# loading model
model = pickle.load(open(path + 'cross_sell.pkl', 'rb'))
print('Loaded!')

print('\n----- INITIALIZING SERVER -----\n')

# API
app = Flask(__name__)

@app.route('/predict', methods = ['POST'])
def healthinsurance_prediction():
    test_json = request.get_json()

    if test_json:
        if isinstance(test_json, dict): # unique example
            test_raw = pd.DataFrame(test_json, index = [0])
        else: # multiple examples
            test_raw = pd.DataFrame(test_json, columns = test_json[0].keys())
        
        # Healthinsurance class
        pipeline = HealthInsurance()

        # data cleaning
        df1 = pipeline.data_cleaning(test_raw)

        # feature_engineering
        df2 = pipeline.feature_engineering(df1)

        # data preparation
        df3 = pipeline.data_preparation(df2)

        # prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)
        
        return df_response

    else:
        return Response('{}', status = 200, mimetype = 'application/json')


if __name__ == '__main__':
    #app.run('0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0.', port = port)