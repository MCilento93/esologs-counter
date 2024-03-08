#
# ESOLOGS API V1 Readocs
# ----------------------
# https://www.esologs.com/v1/docs/#!/Reports/reports_user_userName_get
#
# EXAMPLE OF REQUESTS
# -------------------
#     + Zones (bosses id, see zones.json)
#     https://www.esologs.com/v1/zones?api_key={API_KEY}
#     + Fights (@users, kill last boss, difficulties)
#     https://www.esologs.com/v1/report/fights/AjDv37CYqFynXpGc?api_key={API_KEY} 


### IMPORTING
import os, requests, json, datetime
from bs4 import BeautifulSoup


### GLOBALS
API_KEY = os.environ['API_KEY']
VERBOSE = True


### CLASSES
class Boss():
  
    def __init__(self,zone):
        if   zone in ('Aetherian Archive','AA'):
            self.id   = 4
            self.name = 'The Mage'
        elif zone in ('Hel Ra Citadel','HRC'):
            self.id   = 8
            self.name = 'The Warrior'
        elif zone in ('Sanctum Ophidia','SO'):
            self.id   = 12
            self.name = 'The Serpent'
        elif zone in ('Maw of Lorkhaj','MOL'):
            self.id   = 15
            self.name = 'Rakkhat'
        elif zone in ('The Halls of Fabrication','HOF'):
            self.id   = 20
            self.name = 'Assembly General'
        elif zone in ('Asylum Sanctorium','AS'):
            self.id   = 23
            self.name = 'Saint Olms the Just'
        elif zone in ('Cloudrest','CR'):
            self.id   = 27
            self.name = "Z'Maja"
        elif zone in ('Sunspire','SS'):
            self.id   = 45
            self.name = 'Nahviintaas'
        elif zone in ("Kyne's Aegis",'KA'):
            self.id   = 48
            self.name = 'Lord Falgravn'
        elif zone in ('Rockgrove','RG'):
            self.id   = 51
            self.name = 'Xalvakka'
        elif zone in ('Dreadsail Reef','DSR'):
            self.id   = 54
            self.name = 'Tideborn Taleria'
        elif zone in ("Sanity's Edge",'SE'):
            self.id   = 57
            self.name = 'Ansuul the Tormentor'
        else:
            self.id   = None
            self.name = None
        
class Zone:

    @staticmethod
    def get_zone_json(api_call=False):
        if api_call:
            # API call to retrieve information on all zones
            url = f'https://www.esologs.com/v1/zones?api_key={API_KEY}'
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        else:
            # to avoid API call
            f = open('zones.json')
            zones = json.load(f)
            f.close()
            return zones

    @staticmethod
    def scrape_zone_json():
        zone_json = Zone.get_zone_json()
        scrape_result = []
        for zone in zone_json:
            name = zone['name']
            encounters = zone['encounters']
            final_boss_id = encounters[-1]['id']
            final_boss_name = encounters[-1]['name']
            scrape_result.append({'name':name,
                                 'final_boss_id':final_boss_id,
                                 'final_boss_name':final_boss_name})
        return scrape_result
        
    def __init__(self,name):
        self.is_valid = True
        self.name = name                # string name of the zone (complete or abbreviated)
                
        if   name in ('Aetherian Archive','AA'):
            self.name_short = 'AA'
            self.final_boss_id   = 4
            self.final_boss_name = 'The Mage'
        elif name in ('Hel Ra Citadel','HRC'):
            self.name_short = 'HRC'
            self.final_boss_id   = 8
            self.final_boss_name = 'The Warrior'
        elif name in ('Sanctum Ophidia','SO'):
            self.name_short = 'SO'
            self.final_boss_id   = 12
            self.final_boss_name = 'The Serpent'
        elif name in ('Maw of Lorkhaj','MOL'):
            self.name_short = 'MOL'
            self.final_boss_id   = 15
            self.final_boss_name = 'Rakkhat'
        elif name in ('The Halls of Fabrication','HOF'):
            self.name_short = 'HOF'
            self.final_boss_id   = 20
            self.final_boss_name = 'Assembly General'
        elif name in ('Asylum Sanctorium','AS'):
            self.name_short = 'AS'
            self.final_boss_id   = 23
            self.final_boss_name = 'Saint Olms the Just'
        elif name in ('Cloudrest','CR'):
            self.name_short = 'CR'
            self.final_boss_id   = 27
            self.final_boss_name = "Z'Maja"
        elif name in ('Sunspire','SS'):
            self.name_short = 'SS'
            self.final_boss_id   = 45
            self.final_boss_name = 'Nahviintaas'
        elif name in ("Kyne's Aegis",'KA'):
            self.name_short = 'KA'
            self.final_boss_id   = 48
            self.final_boss_name = 'Lord Falgravn'
        elif name in ('Rockgrove','RG'):
            self.name_short = 'RG'
            self.final_boss_id   = 51
            self.final_boss_name = 'Xalvakka'
        elif name in ('Dreadsail Reef','DSR'):
            self.name_short = 'DSR'
            self.final_boss_id   = 54
            self.final_boss_name = 'Tideborn Taleria'
        elif name in ("Sanity's Edge",'SE'):
            self.name_short = 'SE'
            self.final_boss_id   = 57
            self.final_boss_name = 'Ansuul the Tormentor'
        else:
            self.is_valid = False
            self.name_short = None
            self.final_boss_id   = None
            self.name = None

    def check_if_final_boss(self,boss_id):
        if boss_id == self.final_boss_id:
            return True
        else:
            return False

class Fight:

    def __init__(self,fight_dict):
        if fight_dict.get('difficulty'): # is a boss
            self.is_valid = True
            self.id = fight_dict['id']
            self.boss_id = fight_dict['boss']
            self.boss_name = fight_dict['name']
            self.zone = Zone(fight_dict['zoneName'])
            self.kill = fight_dict['kill']
            self.difficulty_id = fight_dict['difficulty']
            self.assign_difficulty()
        else:
            self.is_valid = False # trash pull
        
    def is_final_boss(self):
        if self.boss_id == self.zone.final_boss_id:
            return True
        else:
            return False

    def assign_difficulty(self):
        if self.difficulty_id == 120:
            self.difficulty = 'Normal'
            self.difficulty_prefix = 'n'
            self.difficulty_suffix = ''
        elif self.difficulty_id == 121:
            self.difficulty = 'Veteran'
            self.difficulty_prefix = 'v'
            self.difficulty_suffix = ''
        elif self.difficulty_id == 122:
            self.difficulty = 'Hard Mode'
            self.difficulty_prefix = 'v'
            self.difficulty_suffix = 'HM'
        elif self.difficulty_id == 123:
            self.difficulty = 'Veteran+1'
            self.difficulty_prefix = 'v'
            self.difficulty_suffix= '+1'
        elif self.difficulty_id == 124:
            self.difficulty = 'Veteran+2'
            self.difficulty_prefix = 'v'
            self.difficulty_suffix = '+2'
        elif self.difficulty_id == 125:
            self.difficulty = 'Veteran+3'
            self.difficulty_prefix = 'v'
            self.difficulty_suffix = '+3'

    def get_summary(self):
        return f"Zone: {self.difficulty_prefix}{self.zone.name_short}{self.difficulty_suffix} - {self.boss_name} (kill = {str(self.kill)})"


class Log:
    
    def __init__(self,url):
        self.url = url    # complete url of the log 
        self.code = self.url.split('/')[-1] # code = final chunk of link
        self.request_url=f"https://www.esologs.com/v1/report/fights/{self.code}?api_key={API_KEY}"
        self.response = requests.get(self.request_url)
        if self.response.status_code == 200:
            self.is_valid = True
            self.json = self.response.json()
        else:
            self.is_valid = False
            self.json = None
        self.datetime = self.get_datetime()
        self.datetime_str = self.datetime.strftime('%Y/%m/%d')
        self.title = self.get_title()

    def get_datetime(self):
        if self.is_valid:
            start_UNIX = self.json['start']
            return datetime.datetime.fromtimestamp(int(start_UNIX)/1000) # datetime

    def get_title(self):
        if self.is_valid:
            return self.json['title']
            
    def get_last_pull_kills(self):

        if not self.is_valid:
            return []
            
        fights = self.json['fights']
        last_pull_kills = []

        if VERBOSE:
            print(f'\nAnalyzing fights for the log {self.url} ({self.datetime_str}):')
            
        for fight in fights:
            
            if fight.get('difficulty') == None: # is a trash pull
                if VERBOSE:
                    print(f'    (Trash pull found {fight})')
                continue
            else: 
                fight_obj = Fight(fight)
                if fight_obj.is_final_boss() and fight_obj.kill: # compare boss id and if last pull
                    last_pull_kills.append(fight_obj)
                    if VERBOSE:
                        print(f'   Found successful last pull kill {fight_obj.get_summary()}')
                else:
                    if VERBOSE:
                        print(f'    (Boss fight found {fight_obj.get_summary()}')
                        
        return last_pull_kills
        
if __name__ == '__main__':
    
    # TEST 1: Get information on final trial bosses
    print('Comparing zones information:')
    zones_json = Zone.scrape_zone_json() # current values from ESOlogs
    for zone in zones_json:
        name = zone['name']
        zone_obj = Zone(name)            # zones under analysis
        try:
            print(f"   @{name} ({zone_obj.name_short}) the final boss is {zone_obj.final_boss_name} (id = {zone_obj.final_boss_id})")
        except:
            print(f'   This zone will not be analyzed: {zone}')
        
    # TEST 2: Open log
    # no. 2 pull CR     https://www.esologs.com/reports/1BNtTCKAa9HQhGyq
    # no. 1 pull SS     https://www.esologs.com/reports/dZp6g1RhL3KTmJDt
    # no. 0 pull MOL    https://www.esologs.com/reports/2zt4PWF89A6qxcXn
    log01 = Log('https://www.esologs.com/reports/1BNtTCKAa9HQhGyq')
    log01.get_last_pull_kills()
    
    log02 = Log('https://www.esologs.com/reports/dZp6g1RhL3KTmJDt')
    log02.get_last_pull_kills()

    log03 = Log('https://www.esologs.com/reports/2zt4PWF89A6qxcXn')
    log03.get_last_pull_kills()