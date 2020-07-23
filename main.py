import pandas as pd 
from datetime import datetime, timedelta   
from matplotlib import pyplot as plt
import telegram

def time_to_sec(time_str):
    return sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time_str.split(":"))))

def cronjob():    
    labels = []
    times = []
    colorset = []
    data = pd.read_csv("data.csv", index_col ="startDate") 
    df = data.loc[["2020-07-22"], ["diff" , "color"]] 
    print(df)

    totaldiff = pd.Series(df['diff']).tolist() 
    print(totaldiff)
    t = timedelta()
    for i in totaldiff:
        (h, m, s) = i.split(':')
        d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        t += d
    print("total "+str(t))
    totaltime = str(t)

    colors = pd.Series(df["color"]).tolist() 
    colors = set(colors)
    print(colors)
    for color in colors:
        if color == 1:
            colorset.append('purple')
        if color == 8:
            colorset.append('grey')
        if color == 9:
            colorset.append('violet')
        if color == 10:
            colorset.append('green')
        if color == 11:
            colorset.append('red')


    df.set_index("color", inplace =True)
    for i1 in colors:
        d = df.loc[[i1]]
        print(d)
        diff = pd.Series(d['diff']).tolist() 
        print(diff)
        t = timedelta()
        for i in diff:
            (h, m, s) = i.split(':')
            d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            t += d
        print(i1, str(t))
        times.append(time_to_sec(str(t))) 
        labels.append(str(t))

    print(times , labels)
    titles = totaltime + " of 12:00:00 hrs is Displaying"
    plt.pie(times, labels = labels,colors = colorset ,autopct='%1.2f%%')
    plt.title(titles)
    plt.savefig('activity.png')
    plt.show()
    bot = telegram.Bot('758389493:AAExlM5jAb1OvyG9ZBYXyPzbnaO2SslQUWo')
    bot.send_photo(chat_id='582942300', photo=open('activity.png', 'rb'))
