import requests
from bs4 import BeautifulSoup


def indianstate(states):
    r=requests.get('https://prsindia.org/covid-19/cases')#from this website we collect covid cases data of each state in india
    data=r.text
    soup=BeautifulSoup(data,"html.parser")
    datalist=''

    for tr in soup.findAll('tr'):
            datalist+=tr.getText('\n')
    datalist=datalist.split('\n')
    datalist=datalist[11:]
    # print(datalist)

    statelist=[]#to store the list of covid cases of each state
    a=5
    c=0

    for _ in range(36):
        statelist.append(datalist[c:a])
        c=a
        a+=5
    # print(statelist)
    # states=['Bihar','Delhi','Tamil Nadu','Andhra Pradesh','Kerala','Chhattisgarh','Karnataka',
    #         'Rajasthan']
    for state in statelist:
        stat=state[0].split()
        stat="".join(stat)
        states=states.split()
        states="".join(states)
        if stat.lower() == states.lower():
            return {'total' : state[1],'active' : state[2],'recovered' : state[3],'Death' : int(state[1])-int(state[2])-int(state[3])} 
            
            
