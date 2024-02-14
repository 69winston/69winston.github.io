from riotwatcher import LolWatcher, ApiError
from flask import Flask, render_template, request
from riotwatcher import LolWatcher, ApiError

app = Flask(__name__)

api_key = 'RGAPI-785e9176-52a9-45b4-958e-bd52e97f8867'
lol_watcher = LolWatcher(api_key)
my_region = 'na1'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        summoner_name = request.form['summoner_name']
        option = request.form['option']

        if option == 'death_count':
            result = get_death_count(summoner_name)
        elif option == 'rank':
            result = get_rank(summoner_name)
        else:
            result = "Invalid option selected."

        return render_template('lolstats.html', result=result, summoner_name=summoner_name, option=option)

    return render_template('lolstats.html')

def get_death_count(summoner_name): #gets deaths and kills for provided username 
    

    me = lol_watcher.summoner.by_name(my_region, summoner_name) #searches for username

    my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id']) #gets stats for user

    
    account_id = me['puuid']

    matches = lol_watcher.match.matchlist_by_puuid("na1",account_id)

    deaths = 0
    kills = 0


    for match in matches:
        match_details = lol_watcher.match.by_id(my_region, match)
        index  = match_details['metadata']['participants'].index(account_id)
        deaths += match_details['info']['participants'][index]['deaths']
        kills += match_details['info']['participants'][index]['kills']

    return(f"  In the last 20 matches {summoner_name} has {kills} kills, but has died {deaths} times")

def get_rank(summoner_name): #gets rank for provided username
    me = lol_watcher.summoner.by_name(my_region, summoner_name)
    my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])

    print(my_ranked_stats)

    if my_ranked_stats:
            rank_info = my_ranked_stats[0]
            tier = rank_info['tier']
            rank = rank_info['rank']
            lp = rank_info['leaguePoints']
            return (f"{summoner_name} is in {tier} {rank} with {lp} LP.")
    else:
            return (f"{summoner_name} is not ranked.")
    

if __name__ == '__main__':
    app.run(debug=True)







    


