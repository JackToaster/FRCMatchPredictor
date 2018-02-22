import numpy as np
import dataImport

from keras.models import Sequential
from keras.layers import Dense, Activation

ENSEMBLE_SIZE = 10


def get_x_y(matches, teams):
    num_teams = len(teams)

    # input to network
    x = []
    for m in matches:
        blue_sparse_data = [0] * num_teams
        red_sparse_data = [0] * num_teams
        for team in m['blue']:
            blue_sparse_data[teams.index(team)] = 1

        for team in m['red']:
            red_sparse_data[teams.index(team)] = 1

        match_data = blue_sparse_data + red_sparse_data + [m['week']]

        x.append(match_data)

    # output of network
    y = [(float(m['scores'][0]),  float(m['scores'][1])) for m in matches]

    return np.array(x), np.array(y)

def create_model(input_size):
    #create
    model = Sequential()
    model.add(Dense(50, input_dim=input_size, activation='softplus'))
    model.add(Dense(10, activation='softplus'))
    model.add(Dense(2, activation='linear'))
    #compile
    model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])
    return model

def validation_acc(y_true, y_pred):
    point_err = (abs(y_pred[0] - y_true[0]) + abs(y_pred[1] - y_true[1]))# / (y_true[0] + y_pred[1])
    #if (y_true[0] > y_true[1]) == (y_pred[0] > y_pred[1]):
    #    return point_err
    #else:
    #    return 2 * point_err
    return point_err


# load the data
teams, matches = dataImport.get_tba_data([0], use_all_events=True, year=2018, district='2018fim')
#_, verify_matches = dataImport.get_tba_data([2], start_time=1489862503)


# convert the data to training data
x, y = get_x_y(matches, teams)
#val_x, val_y = get_x_y(verify_matches, teams)


input_size = len(x[0])


for i in range(ENSEMBLE_SIZE):
    model = create_model(input_size)

    print('Model created, starting training')

    #model.fit(x,y,batch_size=100,epochs=900,validation_data=(val_x, val_y))
    model.fit(x, y, batch_size=100, epochs=900)

    model.save('models/model' + str(i) + '.h5')

