# Author : Xi Chen
import sys
import argparse
import json
from urllib2 import urlopen


def get_countries():
    # return a list of countries that is available
    url = "http://api.population.io:80/1.0/countries"

    try:
        data_from_server = urlopen(url).read()
        string_from_server = data_from_server.decode('utf-8')
        root_word_list = json.loads(string_from_server)

    except Exception as e:
        # Problems with network access or JSON parsing.
        return []
    root_word_list = root_word_list["countries"]
    return root_word_list

def get_life_expectancy(country,gender,age,date):
    # Calculate remaining life expectancy of a person with given sex, country, and age at a given point in time.
    # get_life_expectancy(China,male,49y2m,2001-05-11)
    # Calculates the remaining life expectancy of a Chinese male, who on May 11, 2001 was 49 years and two months old.

    base_url = "http://api.population.io:80/1.0/life-expectancy/remaining/{0}/{1}/{2}/{3}/"
    url = base_url.format(gender,country,date,age)

    try:
        data_from_server = urlopen(url).read()
        string_from_server = data_from_server.decode('utf-8')
        root_word_list = json.loads(string_from_server)

    except Exception as e:
        # Problems with network access or JSON parsing.
        return []
    return root_word_list


def main(args):
    if args.action == 'expect':
        root_words = get_life_expectancy(args.country,args.gender,args.age,args.date)
        # if root_words is empty, then there is an error
        if (not root_words):
            print("Invalid argument,either age or date is in wrong format. Or network problem")
        else:
        # printout the result
            print("life-expectancy is: " + str(root_words["remaining_life_expectancy"]))

    elif args.action == 'listcountries':
        countries = get_countries()
        # if countries is empty, then there is an error
        if (not countries):
            print("Network Error, please try again")
        else:
            for country in countries:
            	print(country)
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get pupulation info from the World Population API')

    parser.add_argument('action',
                        metavar='action',
                        help='action to perform on the word ("expect" or "listcountries")',
                        choices=['expect', 'listcountries'])

    parser.add_argument('country',
                        nargs = '?',
                        metavar='country',
                        default = 'China',
                        help='Choose a country from a given choice. Optional. default: China',
                        choices=['France', 'Fiji', 'Australia', 'China', 'Germany', 'Greece'])

    parser.add_argument('date',
                        nargs = '?',
                        metavar='date',
                        default = '1996-09-12',
                        help='formate XXXX-XX-XX, year-month-day, Optional. default: 1996-09-12')
    parser.add_argument('gender',
                        nargs = '?',
                        metavar='gender',
                        default = 'female',
                        help='Choose from femal or male. Optional',
                        choices=['male','female'])     		
    parser.add_argument('age',
                        nargs = '?',
                        metavar='age',
                        default = '19y2m',
                        help='formate XXyXm, for example 49y2m. Optional. Default: 19y2m'
                        )
                           
    args = parser.parse_args()
    main(args)
