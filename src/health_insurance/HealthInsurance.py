import pickle
import pandas as pd


class HealthInsurance(object):
    def __init__(self):
        self.homepath              = 'features/'
        #self.homepath = '/home/gutto/Repos/Insurance-Cross-Sell/src/features/'
        self.age_scaler             = pickle.load(open(self.homepath + 'age_scaler.pkl', 'rb'))
        self.annual_premium_scaler  = pickle.load(open(self.homepath + 'annual_premium_scaler.pkl', 'rb'))
        self.vintage_scaler         = pickle.load(open(self.homepath + 'vintage_scaler.pkl', 'rb'))

    def data_cleaning(self, df1):
        df1 = df1.loc[:, ~ df1.columns.duplicated()]
        
        cols_name = ['id', 'gender', 'age', 'region_code', 'policy_sales_channel', 'driving_license',
                     'vehicle_age', 'vehicle_damage', 'previously_insured', 'annual_premium', 'vintage',
                     'response']

        df1 = df1[cols_name]
        
        return df1

    def feature_engineering(self, df2):
        df2['vehicle_age'] = df2['vehicle_age'].apply(lambda x: 'over_2_years' if x == '> 2 Years' else 
                                                            'between_1_2_year' if x == '1-2 Year' else 
                                                            'below_1_year')

        return df2
      
    def data_preparation(self, df3):
        df3 = pd.get_dummies(df3, prefix = ['car_age'], columns = ['vehicle_age'])

        question_ohe    = {'No': 0, 'Yes': 1}
        gender_ohe      = {'Male': 0, 'Female': 1}
        
        df3.loc[:, 'gender'] = df3['gender'].map(gender_ohe)
        df3.loc[:, 'vehicle_damage'] = df3['vehicle_damage'].map(question_ohe)

        for col in ['region_code', 'policy_sales_channel']:
            fe_encoding = (df3.groupby(col).size())/len(df3)
            df3.loc[:, col] = df3[col].map(fe_encoding)

        df3['age'] = self.age_scaler.fit_transform(df3[['age']].values)
        df3['annual_premium'] = self.annual_premium_scaler.fit_transform(df3[['annual_premium']].values)
        df3['vintage'] = self.vintage_scaler.fit_transform(df3[['vintage']].values)

        cols_selected = ['annual_premium', 'vintage', 'gender','age', 'region_code', 'vehicle_damage',
                         'previously_insured', 'policy_sales_channel']
        
        return df3[cols_selected]

    def get_prediction(self, model, data, test_data):
        predictions = model.predict_proba(test_data)
        data['score'] = predictions[:, 1].tolist()

        return data.to_json(orient = 'records', date_format = 'iso')
