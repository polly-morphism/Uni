from data import dataset
from task1 import *

import plotly
import plotly.graph_objs as go


#Вивести стовпчикову діаграму: у кого сколько шансов вылететь
def yourchances(name):
    subj = dataset[name]
    chances = len(subj) * 10
    if 'Mathematical Analysis' in subj or chances>100:
        return 100
    return chances
plotly.offline.plot({'data':[go.Bar(x=list(dataset), y=list(map(yourchances, dataset)))]})
