## Imports
import requests
import json
import traceback
from tkinter import *
try:
    from elfsecret import agents
except:
    agents = dict()
##grab the tokens
##Variable Declares
try:
    active_agent = list(agents.keys())[0]
    token = agents.get(active_agent)
except:
    active_agent = NONE
    token = NONE

headers = {
    'Authorization': f"Bearer {token}"
}

##init window
main = Tk(screenName="Space Traders")
main.geometry('600x400')
main.title("Space Traders")
display = Text(main, width=200, height=20)
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
        return TRUE,TRUE
    else:
        return FALSE,"No such agent found, please check your entry or register that symbol"

def iterate_main_text(a):
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
    success,stext = update_token()
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
        iterate_main_text(ships)
    else:
        post_main_text(stext)
    
    return "Fleet Data",ships,meta ##future proofing, doesn't do anything rn 5/12/2023

def agent_pull():
    success,stext = update_token()
    label.config(text="Agent Data")
    response = requests.get('https://api.spacetraders.io/v2/my/agent', headers=headers)
    print("Pull Agent Data\nStatus:", response.status_code)

    data = json.loads(response.text)
    agent = data['data']
    print(data)
    if success == TRUE:
        iterate_main_text(agent)
    else:
        post_main_text(stext)
    
    return "Agent Data",agent
def agent_register():
    field = agent_field.get("1.0",'end-1c')
    present = key_check(agents, field) ##really glad I defined this now
    if present == FALSE: ##I just stole this from the APIs
        headers = {
            'Content-Type': 'application/json',
        }
        json_data = {
            'symbol': field,
            'faction': 'DOMINION',
        }
        response = requests.post('https://api.spacetraders.io/v2/register', headers=headers, json=json_data)
        print(response.status_code)
        data = json.loads(response.text)
        if response.status_code == 201: ##201 is successful registration
            agentdata = data['data']
            temptoken = agentdata['token']
            agents[field]=temptoken
            iterate_main_text(agents)
            secret = open('elfsecret.py', 'w')
            new_secret="agents = "
            new_secret += str(agents)
            secret.write(str(new_secret))
            print(data,type(data))
        elif response.status_code == 422:
            error = response.status_code,"\nThis entry already exists and is not in our records\n a unique symbol is required"
            post_main_text(error)
        else:
            error = response.status_code,"\nan error was encountered"
            post_main_text(error)
    else:
        post_main_text("Agent already exists in our database")
def system_pull():
    success,stext = update_token()
    response = requests.get('https://api.spacetraders.io/v2/systems', headers=headers)
    print("Pull System Data\nStatus:", response.status_code)

    data = json.loads(response.text)
    systems = data['data'][0]
    meta = data['meta']
    print(systems)
    if success == TRUE:
        iterate_main_text(systems)
    else:
        post_main_text(stext)

    return "System List",systems,meta

##button logic
check_fleet = Button(top, text="Check Fleet", command = fleet_pull)
check_agent = Button(top, text="Check Agent", command = agent_pull)
check_systems = Button(top, text="Check Systems", command = system_pull)
register_agent = Button(top, text="Register Agent", command = agent_register)
## pack the buttons
check_fleet.pack(side=LEFT)
check_agent.pack(side=LEFT)
check_systems.pack(side=LEFT)
register_agent.pack(side=LEFT)

main.mainloop()