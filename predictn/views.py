from django.http import HttpResponse

from django.shortcuts import render
from django.template import loader

import pandas as pd
import numpy as np

from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
import math

from plotly.graph_objs import Scatter
from plotly.graph_objs import Bar

# Create your views here.

def index(request):

    df2 = pd.read_csv('unitedndf.csv')
    #ftiacs = df2['FTIACS']

    # model N with only housing and reservations
    # X and y from df2 is 2015 to 2021 data
    X = df2[['Housing', 'Reservations', 'S5']].values
    y = df2['FTIACs'].values
    years = df2['Year'].values

    # X2 and y2 from df is 2022 data
    X2 = df2.loc[df2['Year'] == 2022, ['Housing', 'Reservations', 'S5']]
    model = LinearRegression().fit(X,y)
    y2 = math.floor(model.predict(X2))

    df2.loc[df2['Year']==2022, ['FTIACs']] = y2

    df2['Year'] = [str(2015+i) for i in df2.index] # explicitly change

    color_discrete_sequence = ['mediumslateblue']*len(df2)
    color_discrete_sequence[-1] = '#ec7c34'
    

    fig = px.bar(df2, x='Year', y='FTIACs',
             color = 'Year',
             color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    
    plot_div = plot(fig, output_type='div')

    context = {
        'plot_div' : plot_div,
        "y2" : y2
    }


    return render(request, 'index.html', context)

def course(request, course_num):
    course_num = ' '.join(course_num.split('_'))
    year = 2022
    

    df = pd.read_csv('predictn/uwcm.csv')
    df = df[df['Course'] == course_num]
    df = df[np.logical_or(df['Semester'] == year, df['Semester'] == 'Fall 2021')]

##############
    
    df_N = pd.read_csv('unitedndf.csv')
    df_showrate = pd.read_csv('predictn/Showrate_Orientation_clean.csv')

###############

    course = df['Course']
    session = df_showrate['SESSION']
    weeks = list(range(7,24)) #Week numbers 7-23
    week = 23
   
    '''PREDICT W'''
    #all the following for loops collect the values needed for prediction from the right place
    for i in df.index:
##        if (str(year) in df.at[i, 'Semester']) and df.at[i, 'Course'] == course:
            w7 = df.at[i, 'Week 7']
            w_n = df.at[i, 'Week '+str(week)]
    for i in range(len(df_showrate['SESSION'])):
##        if df_showrate.at[i, 'SESSION'] == session:
            s_k = df_showrate.at[i, 'CUMULATIVE_'+str(year)]
    for i in range(len(df_N['Year'])):
##        if df_N.at[i, 'Year'] == year:
            N = df_N.at[i, 'FTIACs']

    w23 = (((w_n - w7)/s_k) * N) + w7

###############
    


    #inputs for course and year -- easily changable
    course = course_num
    year_curr = year

    #gets data for num seats available(current year), num seats taken (current & previous year)
    for i in df.index:
##        if (str(year_curr) in df.at[i, 'Semester']) and df.at[i, 'Course'] == course:
            seatNum = df.at[i, 'Seats']
            taken_curr = list(df.loc[i, 'Week 7':'Week 10']) ##Only takes weeks 7-10 for 
##        if ("Fall 2021" in df.at[i, 'Semester']) and df.at[i, 'Course'] == course:
            taken_prev = list(df.loc[i, 'Week 7':])

    #make weeks 0-30 (extra long for length of h-lines to extend entire graph)
    weeks = list(range(30))
    weeks = [str(i) for i in weeks]

    #make 2D list that holds equal length lists for seats taken (both years)
    taken = [[np.nan]*len(weeks), [np.nan]*len(weeks)]
    for i in range(7,len(weeks)):
        try: taken[0][i] = taken_prev[i-7]
        except: pass
        try: taken[1][i] = taken_curr[i-7]
        except: pass

    #make prediction and available seats into usable lists to plot
    pred = [w23]*len(weeks) #TODO: get current year week 23 prediction
    seats = [seatNum]*len(weeks)

    #if prediction > seat cap bar is red, if prediction 90%->cap bar is orange, otherwise its green
    if pred[0] >= seatNum: color='red'
    elif pred[0] >= (seatNum*0.9): color='orange'
    else: color='green'


    graphs = []
    graphs.append(
        go.Scatter(x=weeks, y=seats, mode='lines', name='Number of Seats Offered')
        )
    graphs.append(
        go.Scatter(x=weeks, y=pred, mode='lines', name='Week 23 Prediction')
        )
    graphs.append(
        go.Bar(x=weeks, y=taken[1], name='Fall 2022 Taken Seats', marker_color='blue')
        )
    graphs.append(
        go.Bar(x=weeks, y=taken[0], name='Fall 2021 Taken Seats', marker_color='tan')
        )
    layout = {
        'title': 'Seats Filled vs. Cap',
        'xaxis_title': 'Week Number',
        'yaxis_title': 'Number of Students',
        'hovermode' : 'x unified',
        'legend' : dict(orientation='h', yanchor='bottom', y=1),
        'xaxis_range' : [6.5,23.5],
        'xaxis' : dict(fixedrange=True),
        'yaxis' : dict(fixedrange=True)
        }


    plot_div = plot({'data': graphs, 'layout': layout},
                    output_type='div')
    val = '%.0f'%(pred[0])
    
    context = {
        "plot_div" : plot_div,
        "course_num" : course_num,
        "pred" : val
        }

    return render(request, 'course.html', context)


