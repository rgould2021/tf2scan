import requests

# API Keys
STEAM_API_KEY = 'AA4CC06B9DA0790167532214823AAF92'
BACKPACK_TF_API_KEY = '66b663ed3c2e70c8fa0417a3'

# Steam API Endpoints
STEAM_PLAYER_SUMMARY_URL = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
STEAM_PLAYER_HOURS_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"

# Backpack.tf API Endpoints
BACKPACK_TF_PRICE_URL = "https://backpack.tf/api/IGetPrices/v4"
BACKPACK_TF_USER_URL = "https://backpack.tf/api/IGetUsers/v3"

def get_player_hours(steam_id):
    params = {
        'key': STEAM_API_KEY,
        'steamids': steam_id
    }
    response = requests.get(STEAM_PLAYER_SUMMARY_URL, params=params)
    player_data = response.json().get('response', {}).get('players', [])[0]
    
    if not player_data:
        return None
    
    params = {
        'key': STEAM_API_KEY,
        'steamid': steam_id,
        'include_appinfo': True,
        'include_played_free_games': False,
        'appids_filter': [440]  # TF2 AppID
    }
    response = requests.get(STEAM_PLAYER_HOURS_URL, params=params)
    games = response.json().get('response', {}).get('games', [])
    
    for game in games:
        if game['appid'] == 440:
            return game['playtime_forever'] / 60  # Convert minutes to hours
    
    return 0

def get_inventory_value(steam_id):
    params = {
        'key': BACKPACK_TF_API_KEY,
        'steamid': steam_id,
        'appid': 440  # TF2 AppID
    }
    response = requests.get(f'https://backpack.tf/api/inventory/{steam_id}/values', params=params)
    inventory_value = response.json().get('value', 0)
    market_value = response.json().get('market_value', 0)
    
    return inventory_value, market_value

def get_item_prices():
    params = {
        'key': BACKPACK_TF_API_KEY,
        'appid': 440  # TF2 AppID
    }
    response = requests.get(BACKPACK_TF_PRICE_URL, params=params)
    prices = response.json().get('response', {}).get('items', {})
    
    return prices

def get_user_info(steam_id):
    params = {
        'key': BACKPACK_TF_API_KEY,
        'steamids': steam_id
    }
    response = requests.get(BACKPACK_TF_USER_URL, params=params)
    user_data = response.json().get('response', {}).get('players', [])[0]
    
    return user_data

def display_player_info(steam_id):
    hours_played = get_player_hours(steam_id)
    inventory_value, market_value = get_inventory_value(steam_id)
    user_info = get_user_info(steam_id)
    
    print(f"Player: {user_info.get('name')}")
    print(f"Hours Played: {hours_played} hours")
    print(f"Inventory Value: {inventory_value} ref")
    print(f"Market Value: ${market_value}")
    print(f"Profile URL: {user_info.get('avatar')}")

if __name__ == "__main__":
    steam_ids = ['76561198067247729', '76561198043283911']  # Replace with the Steam IDs you want to scan
    
    for steam_id in steam_ids:
        display_player_info(steam_id)
