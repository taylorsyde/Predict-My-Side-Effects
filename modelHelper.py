import numpy as np
import pickle
import pandas as pd
from sklearn.neighbors import KDTree

class ModelHelper():
    def __init__(self):

        pass

    def makePredictions(age_group, sex, other_meds, history, prior_vax, allergies, vax_name, vax_dose):
        # print(self)
        print(age_group)
        print(sex)
        print(other_meds)
        print(history)
        print(prior_vax)
        print(allergies)
        print(vax_name)
        print(vax_dose)
        # print(temp)

        features_np = ['OTHER_MEDS', 'HISTORY', 'PRIOR_VAX', 'ALLERGIES', 'F', 'M', 'JANSSEN', 'MODERNA', 'PFIZER',
                    'VAX_DOSE_SERIES_1', 'VAX_DOSE_SERIES_2', '18-25', '26-35', '36-45', '46-55', '56-65', '66-75', '76-85', '86-95',
                    '96 +']

        user_input = np.zeros(len(features_np))

        age_idx = features_np.index(f'{age_group}')
        sex_idx = features_np.index(f'{sex}')
        vax_idx = features_np.index(f'{vax_name}')
        dose_idx = features_np.index(f'VAX_DOSE_SERIES_{vax_dose}')


        user_input[0] = other_meds
        user_input[1] = history
        user_input[2] = prior_vax
        user_input[3] = allergies
        user_input[sex_idx] = 1
        user_input[vax_idx] = 1
        user_input[dose_idx] = 1
        user_input[age_idx] = 1


        input_pred = [user_input]

        print("input_pred", input_pred)

        # with open("final_regression_model.sav", "rb") as f:
        #     model = pickle.load(f)
        # #     # print('hello')

        with open("final_regression_model.sav", "rb") as f:
            model = pickle.load(f)
        
        # Data File
        data = "Resources/FINAL_CLEAN_FILE.csv"
        # read to dataframe
        data_df = pd.read_csv(data)

        # Create Features by dropping columns we do not need (or already have in feature format)
        X = data_df.drop(['VAERS_ID', 'SYMPTOM','ASSIGNED_GROUP','SEVERITY_LEVEL','HOSPITAL', 'DIED', 'L_THREAT', 'CUR_ILL', 'VAX_SITE_LA', 'VAX_SITE_RA', 'AGE_YRS', 'AGE_GROUP'], axis=1)

        print(X.columns)

        pred = model.predict(input_pred)

        # 5 people closest to user 1
        tree = KDTree(X)
        dist, ind = tree.query([user_input], k=200)

        #convery ndarry to list 
        like_users = ind[0].tolist()
        # indices of closest neighbors
        # print(like_users)  

        # save nearest 200 neighbors symptoms as list for wordcloud
        predicted_symptoms = data_df[['ASSIGNED_GROUP','SEVERITY_LEVEL']].iloc[like_users]
        predicted_symptoms = predicted_symptoms.value_counts()
        print("LOOK HERE")
        predicted_symptoms.head()

        dirty_dict = predicted_symptoms.to_dict()

        words = []
        for key in dirty_dict:
            x = {'x': key[0], 'value': dirty_dict[key], 'category': key[1]}
            words.append(x)
    
        # words

        # # Return 50 closest symptoms for those nearest neighbors
        # tree = KDTree(self.X)
        # dist, ind = tree.query([user_input], k=50)

        # #convery ndarry to list 
        # like_users = ind[0].tolist()
        # print(like_users)  # indices of closest neighbors

        # # save nearest neighbors symptoms as list for wordcloud
        # get_symptoms = self.data_df['ASSIGNED_GROUP'].iloc[like_users].tolist()
        # symptom_array = np.array(get_symptoms)
        # nearest_symptoms = np.unique(symptom_array)
        
        # #convert list to string and generate
        # unique_string=(" ").join(nearest_symptoms)

        return pred, words


if __name__ == "__main__":
    mh = ModelHelper()
    results = mh.makePredictions('36-45','F',1, 1, 1, 1, 'PFIZER', '2')
    print(results)
    print('test3')
    

