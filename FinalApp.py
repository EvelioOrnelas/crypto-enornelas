import PySimpleGUI as sg
import configparser, pathlib, time, requests, urllib, cloudscraper, io
from pathlib import Path
from coinbase.wallet.client import Client
from PIL import Image
import json

def make_win1():
    layout = [  #[sg.Menu(menu_def, tearoff=True, pad=(10, 10))],
                [sg.Text('Config file: ', size=(15, 1)), sg.InputText(key='_FILEBROWSE_', enable_events=True), sg.FileBrowse(target='_FILEBROWSE_'), sg.Button('Profile', key='userInfo', enable_events=True)],
                [sg.Column([[sg.Text('Portfolio', font=("Verdana", 30))]], justification='center')],
                [sg.Text('_'  * 90)],
                [sg.Text('Your balance')],
                [sg.Text('', key='AccountName', enable_events=True, font=('Verdana', 21))],
                [sg.Text('', key='Bitcoin', enable_events=True), sg.Text('', key='balAmount', enable_events=True)],
                [sg.Text('', key='BuyPrice', enable_events=True)],
                [sg.Text('', key='SellPrice', enable_events=True)],
                [sg.Output(size=(90, 1), background_color='black', text_color='white')]]
    return sg.Window('Coinbase GUI', layout, resizable=True, finalize=True)
def make_win2():
    layout = [  [sg.Column([[sg.Image(data=png_data, key="-ArtistAvatarIMG-")]], justification='center')],
                [sg.Text('Name: ', size=(15, 1)), sg.Text(name)],
                [sg.Text('Email: ', size=(15, 1)), sg.Text(email)],
                [sg.Text('Currency: ', size=(15, 1)), sg.Text(currency)],
                [sg.Text('State: ', size=(15, 1)), sg.Text(state)]]
    return sg.Window('Profile', layout, resizable=True, finalize=True)

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

# url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/BTC_Logo.svg/1200px-BTC_Logo.svg.png'
# response = requests.get(url, stream=True)
# response.raw.decode_content = True
# img_box = response.raw.read()
# img_box.thumbnail((50, 50))

window1, window2 = make_win1(), None
while True:
    window, event, values = sg.read_all_windows()
    if(event == '_FILEBROWSE_'):
        try:
            infile = str(values['_FILEBROWSE_'])
            config=getConfig(infile)
            print('Got configuration file!')
            coinbasesecret=str(config.get('coinbasesecret',''))
            coinbasekey=str(config.get('coinbasekey',''))
            assert(len(coinbasesecret)!=0)
            assert(len(coinbasekey)!=0)
            client = Client(api_key=coinbasekey, api_secret=coinbasesecret)
            auser = client.get_accounts()
            json_dump = json.dumps(auser)
            json_object = json.loads(json_dump)
            amount = ''
            aname = ''
            acurrency = ''
            for each in json_object['data']:
                if each['name'] == 'BTC Wallet':
                    #print(each['name'])
                    amount = each['native_balance']['amount']
                    aname = each['balance']['amount']
                    acurrency = each['balance']['currency']
            window.Element('AccountName').Update('$' + amount)
            window.Element('Bitcoin').Update('Bitcoin')
            window.Element('balAmount').Update(aname + ' ' + acurrency)
            databuy = client.get_buy_price(currency_pair = 'BTC-USD')
            datasell = client.get_sell_price(currency_pair = 'BTC-USD')
            window.Element('BuyPrice').Update('Buy price: ' + databuy.amount)
            window.Element('SellPrice').Update('Sell price: ' + datasell.amount)
        except:
            print("Invalid coinbase configuration file")
            time.sleep(3)
            break
    if event == 'userInfo':
        try:
            user = client.get_current_user()
            avatar = user.avatar_url
            name = user.name
            email = user.email
            currency = user.native_currency
            state = user.state
            jpg_data = (
            cloudscraper.create_scraper(
                browser={"browser": "firefox", "platform": "windows", "mobile": False}
            )
            .get(avatar)
            .content
            )
            pil_image = Image.open(io.BytesIO(jpg_data))
            png_bio = io.BytesIO()
            pil_image.save(png_bio, format="PNG")
            png_data = png_bio.getvalue()
            window2 = make_win2()
        except:
            print('Choose configuration file first!')
    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        if window == window2:       # if closing win 2, mark as closed
            window2 = None
        elif window == window1:     # if closing win 1, exit program
            break
    if event == 'Close':
        window2.close()
window.close()