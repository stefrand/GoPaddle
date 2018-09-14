##
##Created by Stef Rand, 2018, powered by American Whitewater's amazing site
##


##Begin Program

##import modules
import urllib

import bs4

import csv

import time

from bs4 import BeautifulSoup

from urllib.request import Request, urlopen


##begin program, welcome user, orient user
print()
print("* * Welcome to Go Paddle! * *")
print('* *  Powered by AmericanWhitewater.org  * *')
print()
print()
print('This program searches for currently runnable rivers by state and rapid level.')
print("You can then get river URLs and save your results to your computer.")
print()
print("Let's get started!")
print()

##dictionary of state names and abbreviations
state_dict = {'AL':'Alabama', 'AK':'Alaska', 'AZ':'Arizona', 'AR':'Arkansas', 'CA':'California', 'CO':'Colorado', 'CT':'Connecticut', 'DC':'Washington DC', 'DE':'Delaware', 'FL':'Florida', 'GA':'Georgia', 'HI':'Hawaii', 'ID':'Idaho', 'IL':'Illinois', 'IN':'Indiana', 'IA':'Iowa', 'KS':'Kansas', 'KY':'Kentucky', 'LA':'Louisiana', 'ME':'Maine', 'MD':'Maryland', 'MA':'Massachusetts', 'MI':'Michigan', 'MN':'Minnesota', 'MS':'Mississippi', 'MO':'Missouri', 'MT':'Montana', 'NE':'Nebraska', 'NV':'Nevada', 'NH':'New Hampshire', 'NJ':'New Jersey', 'NM':'New Mexico', 'NY':'New York', 'NC':'North Carolina', 'ND':'North Dakota', 'OH':'Ohio', 'OK':'Oklahoma', 'OR':'Oregon', 'PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 'SD':'South Dakota', 'TN':'Tennessee', 'TX':'Texas', 'UT':'Utah', 'VT':'Vermont', 'VA':'Virginia', 'WA':'Washington', 'WV':'West Virginia', 'WI':'Wisconsin', 'WY':'Wyoming'}

user_choice = ''

##begin search code
while user_choice != 'quit':
    print()
    ##Get user input for state and make sure output is the state abbreviation for the url
    def find_state():
        user_input = input('Please enter the US state you would like to go paddling in today: ')
        for key in state_dict:
            while user_input not in state_dict.keys() and user_input not in state_dict.values():
                print('Sorry, that is not a state I recognize. Pleae try again!')
                print()
                user_input = input('Please enter the US state you would like to go paddling in today: ')
            if user_input == key:
                return key
            elif user_input == state_dict[key]:
                return key

    ##call the function to get the state            
    state = find_state()

    ##define the URL and change the header to get around urllib block
    req = Request('https://www.americanwhitewater.org/content/River/state-summary/state/'+ state +'/', headers={'User-Agent': 'Mozilla/5.0'})

    ##request to open the url
    webpage = urlopen(req).read()

    ##parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(webpage, 'html.parser')

    ##create dictionary for all runnable rivers rivers in state
    river_dict = {}

    ##process soup to pull out id as key and list of river info as value, save to river_dict
    for each in soup.find_all('tr'):
        river_url = str(each.find('a', href=True))
        river_id = river_url.split('/')
        final_id = ''.join(river_id[-3:-2])
        river = each.text.strip()
        ##add only runnable rivers to state_dict
        if 'Runnable' in river and state in river:
            river_dict[final_id] = river.split('\n')


    ##Begin user output portion of program
    

    ##dictionary to save user output from the following functions
    user_rivers = {}        

    ##function to parse max difficulty level for river_output
    def river_max_diff(river_diff):
        if river_diff == 'I' or river_diff == 'II' or river_diff == 'III' or river_diff == 'IV' or river_diff == 'V':
            return river_diff
        elif '+' and '(' in river_diff:
            max_diff = river_diff.strip(')').split('(')
            return max_diff[-1]
        elif '+' in river_diff and '-' not in river_diff:
            max_diff = river_diff.strip('+')
            return max_diff
        elif '-' in river_diff and '(' not in river_diff:
            max_diff = river_diff.split('-')
            return max_diff[-1]
        elif '(' in river_diff:
            max_diff = river_diff.strip(')').split('(')
            return max_diff[-1]
        else:
            return ''

    ##prompt before user input of river difficulty in river_output function       
    print()
    print('What is the highest level of rapid difficulty you would like to paddle today?')
    print()

    
    ##function to search river_dict by difficulty, print output, save output to new dict called user_rivers
    def river_output():
        user_diff = input('Please enter I, II, III, IV, or V:  ') 
        print()
        print()
        print('--Search Results--')
        for key in river_dict:
            river_names = river_dict[key][0]
            sub_names = river_dict[key][3]
            sub_names_also = river_dict[key][4]
            river_diff = river_dict[key][5]
            river_diff_also = river_dict[key][6]
            flow_rate = river_dict[key][7]
            flow_rate_also = river_dict[key][8]
            flow_change = river_dict[key][9],
            flow_change_also = river_dict[key][10]
            flow_change_also_also = river_dict[key][11]
            relative_runn = river_dict[key][12]
            ##call functions for max river difficulty level
            max_diff = river_max_diff(river_diff)
            max_diff_also = river_max_diff(river_diff_also)
            river_link = "https://www.americanwhitewater.org/content/River/detail/id/"+key+"/"
            ##iterate to match user difficulty and max difficulty level, stripping some pesky '+'s that would not go away
            if user_diff == max_diff.strip('+') or user_diff == max_diff_also.strip('+'):
                if river_dict[key] != '':
                    print()
                    print('-- ',river_names,'-', sub_names, sub_names_also)
                    print('Water level:',flow_rate, flow_rate_also,' Difficulty:',river_diff, river_diff_also)
                    user_rivers[key] = river_names, sub_names, sub_names_also, flow_rate, flow_rate_also, river_link
                else:
                    pass
            else:
                pass
            
    ##call river_dict search and output function
    river_output()


    ##Give user option of seeing https links for rivers in user_rivers on screen
    def link_search():
        print()
        print()
        link_request = input('Want to see a link to one of these rivers? Enter "yes" or "no": ')
        while link_request == 'yes':
            print()
            user_input = input('Enter the name of the river: ')
            for key in user_rivers:
                if user_input in user_rivers[key][0]:
                    print()
                    print(user_rivers[key][0],'-',user_rivers[key][1], user_rivers[key][2])
                    print(user_rivers[key][5])
                else:
                    pass
            print()
            link_request = input('Would you like to see the URL for another river? Enter "yes" or "no": ')

    ##call link search function        
    link_search()

    
    ##Give user option to save user_rivers as a csv file
    print()
    print()
    print('Would you like to save your search results to a csv file?')
    print('* * Important! * *')
    print('This function will write over any existing versions of "river_search.csv"!')
    print()
    save_file = input('Please enter "yes" to save or "no" to pass:  ')
    if save_file == 'yes':
        with open('river_search.csv', 'w') as csvfile:
            fieldnames = ['river_name', 'sub_name', 'sub_name_2', 'flow_rate', 'flow_rate_2', 'river_link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for key in user_rivers:
                writer.writerow({'river_name': user_rivers[key][0], 'sub_name': user_rivers[key][1], 'sub_name_2': user_rivers[key][2], 'flow_rate': user_rivers[key][3], 'flow_rate_2': user_rivers[key][4], 'river_link': user_rivers[key][5]})
        time.sleep(1)
        print()
        print('Done! "river_search.csv" has been saved to your current directory')
        print()


    ##User option to quit program or continue with new state search
    print()
    user_choice = input('If you are done, type "quit", or hit enter to search again: ')


##Say goodbye to user
print()
print("Thank you for using Go Paddle!")
print('See you on the river!')
time.sleep(1)        

##End program        

