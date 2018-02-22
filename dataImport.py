import tbapy
import time
#key for the district
from absl.logging import use_absl_handler

DISTRICT_KEY = '2017fim'
YEAR = 2017

def get_tba_data(weeks = range(10), start_time = 0, end_time = time.time(), use_all_events = False, district = DISTRICT_KEY, year = YEAR):

    tba = tbapy.TBA('LhxxYeNje0x2oOcMs4d2DTp45We5fTLHek2MNaDzd0v5WqrvbwBtDJaa8I47YfqA')

    print("Loading event data...")
    #get events
    #events = tba.team_events(TEAM_NUM ,YEAR ,simple=True)
    if use_all_events:
        events = tba.events(year=year)
    else:
        events = tba.district_events(district)
    event_ids = []
    for e in events:
        if e['week'] in weeks or (e['week'] == None and 0 in weeks):
            event_ids.append(e['key'])
    print("Loading match data...")
    matches = []

    for event_c in event_ids:
        event_matches = tba.event_matches(event_c)
        week = tba.event(event_c)['week']
        event_data = []
        for mat in event_matches:
            actual_time = mat['actual_time']
            if actual_time > start_time and actual_time < end_time:
                event_data.append({'blue':mat['alliances']['blue']['team_keys'], 'red':mat['alliances']['red']['team_keys'],\
                       'scores':(mat['alliances']['blue']['score'],mat['alliances']['red']['score']),\
                       'week':week})
        matches += event_data

    #get teams
    print('Loading team data...')
    team_nums = get_tba_teams(use_all_events, district)
    return team_nums, matches

def get_tba_teams(use_all_events = False, district = DISTRICT_KEY, year = YEAR):
    tba = tbapy.TBA('LhxxYeNje0x2oOcMs4d2DTp45We5fTLHek2MNaDzd0v5WqrvbwBtDJaa8I47YfqA')
    if use_all_events:
        teams = []
        for i in range(50):
            teams = teams + tba.teams(i, simple=True)
    else:
        teams = tba.district_teams(district, simple=True)
    team_nums = [t['key'] for t in teams]
    return team_nums