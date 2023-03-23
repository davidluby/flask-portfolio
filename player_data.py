

"""
# All statistics taken from and property of Basketball-Reference.com
# Link: https://www.basketball-reference.com/
#
# Author: David Luby
# Date created: 2/10/2023
#
# This script is under construction
"""

# Package imports
from bs4 import BeautifulSoup
import requests
import json


"""
 # This function takes a player's full name and returns the corresponding
 # URL from Basketball-Reference.com
"""
def find_player(full_name):


    # Handle input for URL assembly
    first, last = full_name.lower().split()
    first_of_last = last[0]

    if len(last) >= 5:
        first_five_last = last[0:5]
    else:
        first_five_last = last
    
    first_two_first = first[0:2]



    # Iterate similar URL's until matched
    count = 0
    flag = False
    while (count <= 3) and (flag == False):
        count += 1
        page_number = str(count)


        # Assemble page URL
        url = ('https://www.basketball-reference.com/players/' + first_of_last
                + '/' + first_five_last + first_two_first + '0' + page_number
                + '.html')



        # Create page soup, verify page exists, check match condition
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        check_page = soup.h1

        data = []
        if check_page.get_text() == "Page Not Found (404 error)":
            data.append("Try again. No player was found.")
            break

        else:
            # Exit loop on matching first name
            page_name = check_page.span.get_text()
            page_first, page_last = page_name.split()

            if first == page_first.lower():
                flag = True
                data.append(page_name)


    return(flag, data, soup)


"""
 # This function takes a player page soup and returns the corresponding
 # player's statistics from Basketball-Reference.com
"""
def get_data(flag, data, soup):

    if flag == False:
        pass

    else:
        # Initialize list of ID tags to parse soup
        id_names = ["meta", "age", "team_id", "pos", "mp_per_g", "fg_pct", "fg3_pct",
                "trb_per_g", "ast_per_g", "stl_per_g", "blk_per_g",
                "tov_per_g", "pts_per_g"]
    

        for id in id_names:
            if id == "meta":
                picture = soup.find("div", {"class","media-item"})
                data.append(picture.find("img")["src"])
            else:
                current_season = soup.find("tr", {"id":"per_game.2023"})
                data.append(current_season.find("td", {"data-stat":id}).get_text())

    return data


# This function parses soup, appends to a list, and returns JSON data
def format_json(data):
    card_keys = ['cardId', 'deckId', 'name', 'pic', 'age', 'team', 'pos', 'min',
                'fg', 'thr', 'reb', 'ast', 'stl', 'blk', 'tov', 'ppg']

    dict = {}
    i = -1
    for keys in card_keys:
        i += 1
        if i < 2:
            dict[keys] = "null"
        else:
            dict[keys] = data[i-2]
    
    out = json.dumps(dict)

    return(out)

# Main method
def main(name):
    flag, data, soup = find_player(name)
    stats = get_data(flag, data, soup)
    out = format_json(stats)
    return (out)


if __name__ == '__main__':

    print(main('lebron james'))

