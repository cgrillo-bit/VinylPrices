# Importing Regex to strip the album ID values from the returned list
import re
# Importing flask for proxy server
from flask import Flask

# discogs API that we will use to pull vinyl listings and vinyl prices
import discogs_client
# To ensure it doesn't throqwxUBFiDzxw an exception upon connecting
from discogs_client.exceptions import HTTPError

# Discogs price is going to ask the user for the artist and album title of
# What album they are searching. It then queries Discogs and only searching
# for type LP which is a vinyl in this case
# It then appends the first page of results to our discogs album list which holds all relevant album information
# We then use regex to filter out everything that isn't the actual ID which we will pass to our scraper
# Since the Discogs API does not support pulling active market prices
import discogs_scrape

# The index 0 of the return will be the master release
MASTER_RELEASE = 0
# the index of 1 the return will be the non-master release
RELEASE = 1


def discogs_authentication():

    consumer_key = 'xVnWfYiwvqIXRIcrUOIT'
    consumer_secret = 'mBSmOMuVRCSTUioBOTSQKvMwtlsVjPrH'
    user_agent = 'console_collection/1.0'

    discogs_object = discogs_client.Client(user_agent)
    # Setting consumer and consumer secret keys with the API
    discogs_object.set_consumer_key(consumer_key, consumer_secret)
    # Generating the authorization url for users to connect their account
    token, secret, url = discogs_object.get_authorize_url()

    # Printing out oAuth tokens that are for this specific user
    print('---Request Token---')
    print(f' *oauth_token = {token}')
    print(f' *oauth_token_secret = {secret}')
    print('---End request Token Information---')
    print('\n')

    # input control loop so the user has to enter y to move forward, as entering no means they have not gone to the
    # Authorization link provided
    accepted = 'n'
    while accepted.lower() != 'y':
        accepted = input(f'Did you authorize the transaction from {url} [y/n] : ')

    oauth_verifier = input('Verification Code : ')

    # Try except being built to confirm the access token given from discogs is avalid so the user may be authenticated
    try:
        access_token, access_secret = discogs_object.get_access_token(oauth_verifier)

    except HTTPError:
        print('Unable to authenticate.')


    # Grabs active user information
    active_user = discogs_object.identity()

    # Prints confirmed and authorized user information
    print('User Information')
    print(f'user = {active_user.username}')
    print(f'name = {active_user.name}\n')

    print(
        'Authorization process complete - Future uses of collection application will be signed in using authorization tokens above.\n')

    return discogs_object


# The discogs search function takes in the discogs API object along with the album and the artist the user
# is searching for. It will use the discogs api functionality search to find a reference ID of the master release
# of a record. Then it will return this in a list called discogs album list, it will later pass this reference list
# to the scraper which will pull current market prices.

def discogs_search(discogs_object, artist, album):
    unfiltered_list = []
    filtered_album_list = []
    artist_input = artist
    album_input = album
    # choice = input('Do you want to read about this artist and album or search prices? (enter prices or read) ')
    album_search = discogs_object.search(album_input, artist=artist_input, type='LP')
    '''try:
        unfiltered_list = album_search.page(1)
    except:
        print('Sorry, this album cannot be found please attempt another search')

    pattern = '([0-9]+[0-9])'
    matches = re.findall(pattern, str(unfiltered_list))
    for result in matches:
     filtered_album_list.append(int(result))'''

    return artist, album


def activate_scraper(master_id):

    price_list, album_found = discogs_scrape.find_prices(master_id)
    value_list = discogs_scrape.price_structure(price_list)
    average_vinyl_price = discogs_scrape.generate_average_price(value_list)

    return average_vinyl_price, album_found


# our main so to say, it calls the authenticate method as all searches through the Discogs APi must be an authennticated
# User
def main_client():
    application_running = True
    discogs_object = discogs_authentication()
    print('Welcome to Chris\' PyVinyl search. Searching for vinyls is annoying. So I made this!')
    artist_input = input('Please enter an artist to get started: ')
    print(f'Okay the artist you want to find is {artist_input}')
    album_input = input('Please enter the album you are looking for: ')
    reference_id = discogs_search(discogs_object, artist_input, album_input)
    master_id = reference_id[MASTER_RELEASE]
    average_price, album = activate_scraper(master_id)
    print(f'The average price for {album} is {average_price:.2f}')


    #print(f' {average_price}, {album_found}')

main_client()
