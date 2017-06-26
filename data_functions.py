'''
Created on Oct 13, 2016

@author: Carlos Garcia - carlos@carlosgarcia.co
'''


def male_female_child(passenger):
    # Take the Age and Sex
    age, sex = passenger
    # Compare the age, otherwise leave the sex
    if age < 16:
        return 'child'
    else:
        return sex


def survived_couples(columns, args):
    survived, cabin = columns
    if survived == 1:
        if str(cabin) == 'nan':
            return '---'
        elif cabin in args:
            return 'YES!!!'
        else:
            args.append(cabin)
            return 'maybe'
        
    else:
        return ':('
