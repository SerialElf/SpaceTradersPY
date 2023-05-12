## Imports
import requests
import json
import traceback
from tkinter import *
from elfsecret import agents

##grab the tokens
##Variable Declares
token = agents.get('SerialElf_0004')
active_agent = "SerialElf_0004"
headers = {
    'Authorization': f"Bearer {token}"
}

##init window
main = Tk(screenName="Space Traders")
main.geometry('600x400')
main.title("Space Traders")
display = Text(main, width=550, height=20)
display.pack(side='bottom')
label=Label(main)
label.pack(side='bottom')
##container for button row
top = Frame(main)
top.pack(side=TOP)
agent_field = Text(top, width=15, height=1)
agent_field.pack(side=RIGHT)
agent_field.insert(END, active_agent)

def key_check(dic, key):
    if key in dic.keys():
        print("key found")
        return TRUE
    else:
        print("key not found")
        return FALSE

def update_token():
    field = agent_field.get("1.0",'end-1c') ##-1c stops it from adding a newline
    present = key_check(agents, field)
    if present == TRUE:
        active_agent = field 
        token = agents.get(active_agent) ##why doesn't this throw an exception whenthe agent isn't in the secrets?
        return TRUE
    else:
        return "No such agent found, please check your entry or register that symbol"

def iterate_main_text(a,b):
    display.delete("1.0","end")

    #x is data, y is meta
    for x,y in a.items():

        ##For some reason these all have to be seperate, fuck me as to why
        display.insert(END, x)
        display.insert(END, " : ")
        display.insert(END, y)
        display.insert(END, "\n")
def post_main_text(a):
    display.delete("1.0","end")
    display.insert(END, a)
##fleet data pull
def fleet_pull():
    success = update_token()
    label.config(text="Fleet Data")
    ##grab the json
    response = requests.get('https://api.spacetraders.io/v2/my/ships/', headers=headers)
    print("Pull Fleet Data\nStatus:", response.status_code)
    data = json.loads(response.text)

    ##breakdown the json
    ships = data['data'][0] ##if you don't at the [0] it's a list and EVERYTHING IS BAD
    meta = data['meta']
    print(type(ships))

    ##shove the data into the box
    if success == TRUE:
        iterate_main_text(ships,meta)
    else:
        post_main_text(success)
    
    return "Fleet Data",ships,meta ##future proofing, doesn't do anything rn 5/12/2023

def agent_pull():
    success = update_token()
    label.config(text="Agent Data")
    response = requests.get('https://api.spacetraders.io/v2/my/agent', headers=headers)
    print("Pull Agent Data\nStatus:", response.status_code)

    data = json.loads(response.text)
    agent = data['data']
    print(data)
    if success == TRUE:
        iterate_main_text(agent,"NULL")
    else:
        post_main_text(success)
    
    return "Agent Data",agent
def agent_register():
    return "fuck you"

def system_pull():
    success = update_token()
    response = requests.get('https://api.spacetraders.io/v2/systems', headers=headers)
    print("Pull System Data\nStatus:", response.status_code)

    data = json.loads(response.text)
    systems = data['data'][0]
    meta = data['meta']
    print(systems)
    if success == TRUE:
        iterate_main_text(systems,meta)
    else:
        post_main_text(success)

    return "System List",systems,meta

##button logic
check_fleet = Button(top, text="Check Fleet", command = fleet_pull)
check_agent = Button(top, text="Check Agent", command = agent_pull)
check_systems = Button(top, text="Check Systems", command = system_pull)
## pack the buttons
check_fleet.pack(in_=top, side=LEFT)
check_agent.pack(in_=top, side=LEFT)
check_systems.pack(in_=top, side=LEFT)

main.mainloop()