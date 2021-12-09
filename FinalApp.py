import PySimpleGUI as sg
import configparser, pathlib, time, requests, urllib, cloudscraper, io
from pathlib import Path
from coinbase.wallet.client import Client
from PIL import Image

sg.theme('DarkAmber')
def make_win1():
    layout = [  #[sg.Menu(menu_def, tearoff=True, pad=(10, 10))],
                [sg.Text('Config file: ', size=(15, 1)), sg.InputText(key='_FILEBROWSE_', enable_events=True), sg.FileBrowse(target='_FILEBROWSE_')],
                [sg.Button('Get User Info', key='userInfo', enable_events=True), sg.Button('Get Account Info', key='Account', enable_events=True)],
                [sg.Output(size=(110, 30), background_color='black', text_color='white')]]
    return sg.Window('Coinbase GUI', layout, resizable=True, finalize=True)

def getConfig(file):
    fd = open(file,"r")
    data = fd.read()
    fd.close()
    config=configparser.ConfigParser()
    config.read_string(f"""
    [default]
    {data}
    """
    )
    return config['default']

window1, window2 = make_win1(), None
while True:
    window, event, values = sg.read_all_windows()
    infile = str(values['_FILEBROWSE_'])
    if(event == '_FILEBROWSE_'):
        try:
            config=getConfig(infile)
            print('Got configuration file!')
            coinbasesecret=str(config.get('coinbasesecret',''))
            coinbasekey=str(config.get('coinbasekey',''))
            assert(len(coinbasesecret)!=0)
            assert(len(coinbasekey)!=0)
            client = Client(api_key=coinbasekey, api_secret=coinbasesecret)
            user = client.get_current_user()
            print(user)
        except:
            print("Invalid coinbase configuration file")
            time.sleep(3)
            break
    if event == sg.WIN_CLOSED or event == 'Exit': 
        window.close()
        if window == window2:       # if closing win 2, mark as closed
            window2 = None
        elif window == window1:     # if closing win 1, exit program
            break
    if event in (window2, 'Exit'):
        window2.close()
window.close()