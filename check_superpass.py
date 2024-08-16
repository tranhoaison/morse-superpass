import requests
import csv
import time
# Replace with your OpenSea API key
api_key = 'your_api_key'
base_url_nfts = "https://api.opensea.io/api/v2/chain/ethereum/account/{wallet_address}/nfts"
base_url_traits = "https://api.opensea.io/api/v2/chain/ethereum/contract/{contract_address}/nfts/{token_id}"

def get_nfts_for_wallet(wallet_address, collection_slug, limit=50):
    url = f"{base_url_nfts}?collection={collection_slug}&limit={limit}"
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }
    time.sleep(0.5)
    print(f"Fetching NFTs for wallet: {wallet_address}")
    try:
        response = requests.get(url.format(wallet_address=wallet_address), headers=headers)
        response.raise_for_status()
        nfts = response.json().get('nfts', [])
        token_info = [(nft.get('identifier'), nft.get('contract')) for nft in nfts]
        print(f"Found {len(token_info)} NFTs for wallet: {wallet_address}")
        return token_info
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data for wallet {wallet_address}: {e}')
        return []

def get_traits_for_token(contract_address, token_id):
    url = base_url_traits.format(contract_address=contract_address, token_id=token_id)
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }
    time.sleep(1)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        nft_data = response.json()
        traits = nft_data.get('nft', {}).get('traits', [])
        return traits
    except requests.exceptions.RequestException as e:
        print(f'Error fetching traits for token ID {token_id}: {e}')
        return []

def get_superpass_codes(traits):
    for trait in traits:
        if trait.get('trait_type') == 'Rarity':
            value = trait.get('value')
            if value == 'Lil Pup':
                return 1
            elif value == 'Rare Pooch':
                return 2
            elif value == 'Epic Canine':
                return 2
            elif value == 'Legendary Hound':
                return 3
            elif value == 'Mythical Breed':
                return 4
    return 0

def process_wallets(wallet_csv_path, collection_slug):
    print(f"Processing wallets from file: {wallet_csv_path}")
    total_superpass_codes = 0
    
    with open(wallet_csv_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            wallet_address = row[0]  # Assuming wallet addresses are in the first column
            print(f"\nProcessing wallet: {wallet_address}")
            token_info = get_nfts_for_wallet(wallet_address, collection_slug)
            
            for token_id, contract_address in token_info:
                traits = get_traits_for_token(contract_address, token_id)
                superpass_code = get_superpass_codes(traits)
                total_superpass_codes += superpass_code
                print(f'Wallet: {wallet_address}, Token ID: {token_id}, Superpass Code: {superpass_code}')
    
    print(f'\nTotal Superpass Codes: {total_superpass_codes}')

# Path to your CSV file containing wallet addresses
wallet_csv_path = 'nft_holders.csv'
# Replace with your actual collection slug
collection_slug = 'morse-lab'

# Process each wallet and print results
process_wallets(wallet_csv_path, collection_slug)
