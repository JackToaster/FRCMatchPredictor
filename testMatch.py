import numpy as np
import dataImport
from keras.models import load_model

import plotter

ENSEMBLE_SIZE = 2

def ensemble_predict(ensemble, teams, blue_teams, red_teams, week_num):
    #Generate input data
    num_teams = len(teams)
    blue_sparse_data = [0] * num_teams
    red_sparse_data = [0] * num_teams
    try:
        for team in blue_teams:
            blue_sparse_data[teams.index(team)] = 1

        for team in red_teams:
            red_sparse_data[teams.index(team)] = 1
    except(ValueError):
        print('Couldn\'t find team')
        return []

    match_data = np.array([blue_sparse_data + red_sparse_data + [week_num]])
    #list of outputs
    out_scores = []
    for model in ensemble:
        out_scores.append(model.predict(match_data))
    ret_scores = []
    for score in out_scores:
        ret_scores.append((score[0][0], score[0][1]))
    return ret_scores

print('Loading teams...')
teams = dataImport.get_tba_teams()
print('Loading models...')
ensemble = []
for i in range(ENSEMBLE_SIZE):
    ensemble.append(load_model('models/model' + str(i) + '.h5'))
    print('loaded #' + str(i + 1) + ' of ' + str(ENSEMBLE_SIZE))

while True:
    b1 = input("Blue 1:")
    b2 = input("Blue 2:")
    b3 = input("Blue 3:")
    r1 = input("Red 1 :")
    r2 = input("Red 2 :")
    r3 = input("Red 3 :")
    w  = input("Week #:")
    score_pred = ensemble_predict(ensemble, teams, [b1, b2, b3],[r1,r2,r3], w)
    score_pred = score_pred + ensemble_predict(ensemble, teams, [r1, r2, r3], [b1, b2, b3], w)

    print('Scores predicted by ensemble model:')
    for score in score_pred:
        print('Blue: ' + str(score[0]) + ', Red: ' + str(score[1]))
    plotter.two_box_plot([score[0] for score in score_pred], [score[1] for score in score_pred])
    print('')
