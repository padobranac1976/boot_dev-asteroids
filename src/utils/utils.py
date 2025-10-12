import os
from utils.constants import *

def update_high_score(new_score):
    high_score = get_high_score()
    high_score_dir = HIGH_SCORE_LOCATION.split("/")[0]
    if not os.path.exists(high_score_dir):
        os.mkdir(high_score_dir)
    with open(HIGH_SCORE_LOCATION, 'w') as f:
        f.write(str(max(high_score, new_score)))
            
def get_high_score():
    current_high_score = 0
    if os.path.exists(HIGH_SCORE_LOCATION):
        with open(HIGH_SCORE_LOCATION) as f:
            current_high_score = f.read()
    
    return int(current_high_score)