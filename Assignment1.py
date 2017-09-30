# -*- coding: utf-8 -*-

import csv
import random

print "If you're looking for a poor excuse of a pokemon game, look no further!"
print "Let's battle \n"

list = []
type = []
dict = {}
class Assignment1:
    f = open('Pokemon.csv', 'r') #Open Pokemon dataset
    csv_f = csv.reader(f)
    for row in csv_f:
        list.append(row[0]) #Add number associated to each pokemon to a list
        type.append(row[2]) #Add the pokemon type to another list
        dict[int(list[int(row[0])])] = row[1] #Add the names of each pokemon as the value of each key (the number of the pokemon)
    
#Ask user to input two pokemon
    def play(prompt):
        try:
            pokemon1 = raw_input(prompt)
            playerPokemon = dict.values()[int(pokemon1)] #Receive the name of the pokemon
            playerType = type[int(pokemon1)] #Receive the type of the pokemon
            print "You chose " + playerPokemon
            raw_input()
            print playerPokemon + " is a " + playerType + " type"
            raw_input()
        except ValueError: #If user enters a symbol that's not a number
            print "That's not a number!"
        except IndexError: #If user enters a number not between 1 and 251
            print "That's not between 1 and 251!"

        computerChoice = random.randrange(1,252) #Random number generated from 1 to 251
        computerPokemon = dict.values()[computerChoice] #Give computer random pokemon name
        computerType = type[int(computerChoice)] #Give computer random pokemon type
        print "I choose " + computerPokemon
        raw_input()
        print computerPokemon + " is a " + computerType + " type"
        raw_input()

        #Is super effective against
        #NORMAL:
        #FIGHTING: Ice, Steel, Normal, Dark, Rock
        #FLYING: Fighting, Bug, Grass
        #POISON: Grass, Fairy
        #GROUND: Steel, Poison, Rock, Fire 
        #ROCK: Ice, Fire, Flying, Bug
        #BUG: Psychic, Dark, Grass
        #GHOST: Psychic
        #STEEL: Rock, Dragon, Fairy, Ice
        #FIRE: Grass, Ice, Steel, Bug
        #WATER: Ground, Fire, Rock
        #GRASS: Ground, Water, Rock
        #ELECTRIC: Water, Flying
        #PSYCHIC: Fighting, Poison
        #ICE: Grass, Dragon, Ground, Flying
        #DRAGON: Dragon
        #DARK: Ghost, Psychic
        #FAIRY: Dragon, Dark, Fighting

        ################################################
        ## A bunch of logic to determine the winner of##
        ## this poorly made pokemon battle program.   ##
        ## This was torture.                          ##
        ################################################
        
        if playerType == 'Fighting':
            if computerType == 'Ice' or computerType == 'Steel' or computerType == 'Normal' or computerType == 'Dark' or computerType == 'Rock':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        elif playerType == 'Flying':
            if computerType == 'Fighting' or computerType == 'Bug' or computerType == 'Grass':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        elif playerType == 'Poison':
            if computerType == 'Grass' or computerType == 'Fairy':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        if playerType == 'Ground':
            if computerType == 'Steel' or computerType == 'Poison' or computerType == 'Rock' or computerType == 'Fire':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        if playerType == 'Rock':
            if computerType == 'Ice' or computerType == 'Fire' or computerType == 'Flying' or computerType == 'Bug':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        if playerType == 'Bug':
            if computerType == 'Psychic' or computerType == 'Dark' or computerType == 'Grass':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        if playerType == 'Ghost':
            if computerType == 'Psychic':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!" 
        if playerType == 'Steel':
            if computerType == 'Rock' or  computerType == 'Dragon' or computerType == 'Fairy' or computerType == 'Ice':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        if playerType == 'Fire':
            if computerType == 'Grass' or computerType == 'Ice' or computerType == 'Steel' or computerType == 'Bug':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        if playerType == 'Water':
            if computerType == 'Fire' or computerType == 'Ground' or computerType == 'Rock':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        if playerType == 'Grass':
            if computerType == 'Ground' or computerType == 'Water' or computerType == 'Rock':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        if playerType == 'Electric':
            if computerType == 'Water' or computerType == 'Flying':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        if playerType == 'Psychic':
            if computerType == 'Fighting' or computerType == 'Poison':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        if playerType == 'Ice':
            if computerType == 'Grass' or computerType == 'Dragon' or computerType == 'Ground' or computerType == 'Flying':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        if playerType == 'Dark':
            if computerType == 'Ghost' or computerType == 'Psychic':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        if playerType == 'Fairy':
            if computerType == 'Dragon' or computerType == 'Dark' or computerType == 'Fighting':
                print playerPokemon + " has an advantage over " + computerPokemon
            else:
                print "The pokemon battle and it's a tie!"
        else:
            if computerType == 'Fighting':
                if playerType == 'Ice' or playerType == 'Steel' or playerType == 'Normal' or playerType == 'Dark' or playerType == 'Rock':
                    print computerPokemon + " has an advantage over " + playerPokemon
                
            if computerType == 'Flying':
                if playerType == 'Fighting' or playerType == 'Bug' or playerType == 'Grass':
                    print computerPokemon + " has an advantage over " + playerPokemon
                
            if computerType == 'Poison':
                if playerType == 'Grass' or playerType == 'Fairy':
                    print computerPokemon + " has an advantage over " + playerPokemon
                
            if computerType == 'Ground':
                if playerType == 'Steel' or playerType == 'Poison' or playerType == 'Rock' or playerType == 'Fire':
                    print computerPokemon + " has an advantage over " + playerPokemon
                
            if computerType == 'Rock':
                if playerType == 'Ice' or playerType == 'Fire' or playerType == 'Flying' or playerType == 'Bug':
                    print computerPokemon + " has an advantage over " + playerPokemon
              
            if computerType == 'Bug':
                if playerType == 'Psychic' or playerType == 'Dark' or playerType == 'Grass':
                    print computerPokemon + " has an advantage over " + playerPokemon
               
            if computerType == 'Ghost':
                if playerType == 'Psychic':
                    print computerPokemon + " has an advantage over " + playerPokemon
                
            if computerType == 'Steel':
                if playerType == 'Rock' or playerType == 'Dragon' or playerType == 'Fairy' or playerType == 'Ice':
                    print computerPokemon + " has an advantage over " + playerPokemon
                
            if computerType == 'Fire':
                if playerType == 'Grass' or playerType == 'Ice' or playerType == 'Steel' or playerType == 'Bug':
                    print computerPokemon + " has an advantage over " + playerPokemon
                else:
                    print "The pokemon battle and it's a tie!"
            if computerType == 'Water':
                if playerType == 'Fire' or playerType == 'Ground' or playerType == 'Rock':
                    print computerPokemon + " has an advantage over " + playerPokemon
                
            if computerType == 'Grass':
                if playerType == 'Ground' or playerType == 'Water' or playerType == 'Rock':
                    print computerPokemon + " has an advantage over " + playerPokemon
               
            if computerType == 'Electric':
                if playerType == 'Water' or playerType == 'Flying':
                    print computerPokemon + " has an advantage over " + playerPokemon
                
            if computerType == 'Psychic':
                if playerType == 'Fighting' or playerType == 'Poison':
                    print computerPokemon + " has an advantage over " + playerPokemon
                
            if computerType == 'Ice':
                if playerType == 'Grass' or playerType == 'Dragon' or playerType == 'Ground' or playerType == 'Flying':
                    print computerPokemon + " has an advantage over " + playerPokemon
            if computerType == 'Dark':
                if playerType == 'Ghost' or playerType == 'Psychic':
                    print computerPokemon + " has an advantage over " + playerPokemon
            if computerType == 'Fairy':
                if playerType == 'Dragon' or playerType == 'Dark' or playerType == 'Fighting':
                    print computerPokemon + " has an advantage over " + playerPokemon
            
    play("Pick a number between 1 and 251 ")

    
#f.close()
print "Thanks for playing!"

if __name__ == '__main__':
    Assignment1()
