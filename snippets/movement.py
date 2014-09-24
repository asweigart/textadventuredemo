#! python3
"""
Text Adventure Demo by Al Sweigart (al@inventwithpython.com)

This program is a small text-adventure game that demonstrates the cmd
and textwrap Python modules. You can find other tutorials like this at
http://inventwithpython.com/blog

The tutorial for this game program is located at: TODO
The github repo for this program is at: TODO


This tutorial does not use classes and object-oriented programming
in order to make it simpler to understand for new programmers. Although
you can see how using dictionaries-in-dictionaries to structures your
data quickly gets unwieldy.

The same goes for using global variables and functions such as inventory,
location, and moveDirection(). These are fine for a small program,
but if you ever want to extend the game they can become burdensome to
work with. But if you are starting out with a toy project, they're fine.
"""


"""
First, we will create some data structures for our game world.

The town looks something like this:

        +---------+    +---------+
        | Thief   O    | Bakery  |
        | Guild   |    |         |
+------++------O--+    +----O----+
| Used |
|Anvils|        Town Square     +--------+
|      O                        |Obs Deck|
+------++----O----+    +----O----/  /
        | Black-  O    | Wizard /  /
        | smith   |    | Tower    /
        +---------+    +---------+
"""


"""
These constant variables are used because if I mistype them, Python will
immediately throw up an error message since no variable with the typo
name will exist. If we mistyped the strings, the bugs that it produces
would be harder to find.
"""
DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
UP = 'up'
DOWN = 'down'
GROUND = 'ground'
SHOP = 'shop'
GROUNDDESC = 'grounddesc'
SHORTDESC = 'shortdesc'
LONGDESC = 'longdesc'
TAKEABLE = 'takeable'
EDIBLE = 'edible'
DESCWORDS = 'descwords'

SCREEN_WIDTH = 80

"""
The game world data is stored in a dictionary (which itself has dictionaries
and lists). Python's normal rules of indentation are suspended when typing out
a dictionary value until it encounters the closing curly brace, which is
helpful for us to make the dictionary value readable.

Each dictionary value inside the world variable is a different area in the
game world. The key is a string (i.e. 'Town Square') that is the reference
name of the location. It will also be displayed as the title of the area.

The value is another dictionary, which has keys 'desc', 'north', 'south',
'east', 'west', 'up', 'down', 'shop', and 'ground'. We use the constant
variables (e.g. DESC, NORTH, etc.) instead of strings in case we make
typos.

DESC is a text description of the area. SHOP, if it exists, is a list of
items that can be bought at this area. (We don't implement money in this
program, so everything is free.) GROUND is a list of items that are on
the ground in this area. The directions (NORTH, SOUTH, UP, etc.) are the
areas that exist in that direction.
"""
worldRooms = {
    'Town Square': {
        DESC: 'The town square is a large open space with a fountain in the center. Streets lead in all directions.',
        NORTH: 'North Y Street',
        EAST: 'East X Street',
        SOUTH: 'South Y Street',
        WEST: 'West X Street',
        GROUND: ['Welcome Sign', 'Fountain']},
    'North Y Street': {
        DESC: 'The northern end of Y Street has really gone down hill. Pot holes are everywhere, as are stray cats, rats, and wombats.',
        WEST: 'Thief Guild',
        EAST: 'Bakery',
        SOUTH: 'Town Square',
        GROUND: ['Do Not Take Sign Sign']},
    'Thief Guild': {
        DESC: 'The Thief Guild is a dark den of unprincipled types. You clutch your purse (though several other people here would like to clutch your purse as well).',
        SOUTH: 'West X Street',
        EAST: 'North Y Street',
        GROUND: ['Lock Picks', 'Silly Glasses']},
    'Bakery': {
        DESC: 'The delightful smell of meat pies fills the air, making you hungry. The baker flashes a grin, as he slides a box marked "Not Human Organs" under a table with his foot.',
        WEST: 'North Y Street',
        SOUTH: 'East X Street',
        SHOP: ['Meat Pie', 'Donut', 'Bagel'],
        GROUND: ['Shop Howto']},
    'West X Street': {
        DESC: 'West X Street is the rich section of town. So rich, they paved the streets with gold. This probably was not a good idea. The thief guild opened up the next day.',
        NORTH: 'Thief Guild',
        EAST: 'Town Square',
        SOUTH: 'Blacksmith',
        WEST: 'Used Anvils Store',
        GROUND: []},
    'Used Anvils Store': {
        DESC: 'The anvil store has anvils of all types and sizes, each previously-owned but still in servicable condition. However, due to a bug in the way this game is designed, you can buy anvils like any other item and walk around, but if you drop them they cannot be picked up since their TAKEABLE value is set to False. The code should be changed so that it\'s not possible for shops to sell items with TAKEABLE set to False.',
        EAST: 'West X Street',
        SHOP: ['Anvil'],
        GROUND: ['Anvil', 'Anvil', 'Anvil', 'Anvil']},
    'East X Street': {
        DESC: 'East X Street. It\'s like X Street, except East.',
        NORTH: 'Bakery',
        WEST: 'Town Square',
        SOUTH: 'Wizard Tower',
        GROUND: []},
    'Blacksmith': {
        DESC: 'The blacksmith loudly hammers a new sword over her anvil. Swords, axes, butter knives all line the walls of her workshop, available for a price.',
        NORTH: 'West X Street',
        EAST: 'South Y Street',
        SHOP: ['Sword', 'War Axe', 'Chainmail T-Shirt'],
        GROUND: ['Anvil', 'Shop Howto']},
    'South Y Street': {
        DESC: 'The Christmas Carolers of South Y Street are famous for all legally changing their name to Carol. They are also famous for singing year-round, in heavy fur coats and wool mittens, even in the summer. That\'s dedication to their craft!',
        NORTH: 'Town Square',
        WEST: 'Blacksmith',
        GROUND: []},
    'Wizard Tower': {
        DESC: 'Zanny magical antics are afoot in the world-famous Wizard Tower. Cauldrons bubble, rats talk, and books float midair in this center of magical discovery.',
        NORTH: 'East X Street',
        UP: 'Observation Deck',
        GROUND: ['Crystal Ball', 'Floating Book', 'Floating Book']},
    'Observation Deck': {
        DESC: 'You can see the entire town from the top of the Wizard Tower. Everybody looks like ants, especially the people transformed into ants by the wizards of the tower!',
        DOWN: 'Wizard Tower',
        UP: 'Magical Escalator to Nowhere',
        GROUND: ['Telescope']},
    'Magical Escalator to Nowhere': {
        DESC: 'No matter how much you climb the escalator, it doesn\'t seem to be getting you anywhere.',
        UP: 'Magical Escalator to Nowhere',
        DOWN: 'Observation Deck',
        GROUND: []},
    }

"""
This is the index of all possible items in the game world. Note that These
key-value pairs are more like blueprints than actual items. The actual
items exist in the GROUND value in an area's entry in the world variable.

The GROUNDDESC value is a short string that displays in the area's description.
The SHORTDESC value is a short string that will be used in sentences like, "You
drop X." or "You buy X."
The LONGDESC value is displayed when the player looks at the item.
The TAKEABLE Boolean value is True if the player can pick up the item and put
it in their inventory.
The DESCWORDS value is a list of strings that can be used in the player's
commands. For example, if this is ['welcome', 'sign'] then the player can type
a command such as "take sign" or "look welcome".
The TAKEABLE value is True if the item can be picked up off the ground. If
this key doesn't exist, it defaults to True.
The EDIBLE value is True if the item can be eaten. If this key doesn't exist,
it defaults to False.
"""
worldItems = {
    'Welcome Sign': {
        GROUNDDESC: 'A welcome sign stands here.',
        SHORTDESC: 'a welcome sign',
        LONGDESC: 'The welcome sign reads, "Welcome to this text adventure demo. You can type "help" for a list of commands to use. Be sure to check out Al\'s cool programming books at http://inventwithpython.com"',
        TAKEABLE: False,
        DESCWORDS: ['welcome', 'sign']},
    'Do Not Take Sign Sign': {
        GROUNDDESC: 'A sign stands here, not bolted to the ground.',
        SHORTDESC: 'a sign',
        LONGDESC: 'The sign reads, "Do Not Take This Sign"',
        DESCWORDS: ['sign']},
    'Fountain': {
        GROUNDDESC: 'A bubbling fountain of green water.',
        SHORTDESC: 'a fountain',
        LONGDESC: 'The water in the fountain is a bright green color. Is that... gatorade?',
        TAKEABLE: False,
        DESCWORDS: ['fountain']},
    'Sword': {
        GROUNDDESC: 'A sword lies on the ground.',
        SHORTDESC: 'a sword',
        LONGDESC: 'A longsword, engraved with the word, "Exkaleber"',
        DESCWORDS: ['sword', 'exkaleber', 'longsword']},
    'War Axe': {
        GROUNDDESC: 'A mighty war axe lies on the ground.',
        SHORTDESC: 'a war axe',
        LONGDESC: 'The mighty war axe is made with antimony impurities from a fallen star, rendering it surpassingly brittle.',
        DESCWORDS: ['axe', 'war', 'mighty']},
    'Chainmail T-Shirt': {
        GROUNDDESC: 'A chainmail t-shirt lies wadded up on the ground.',
        SHORTDESC: 'a chainmail t-shirt',
        LONGDESC: 'The chainmail t-shirt has a slogan and arrow engraved on the front: "I\'m with Stupid"',
        DESCWORDS: ['chainmail', 'chain', 'mail', 't-shirt', 'tshirt', 'stupid']},
    'Anvil': {
        GROUNDDESC: 'The blacksmith\'s anvil, far too heavy to pick up, rests in the corner.',
        SHORTDESC: 'an anvil',
        LONGDESC: 'The black anvil has the word "ACME" engraved on the side.',
        TAKEABLE: False,
        DESCWORDS: ['anvil']},
    'Lock Picks': {
        GROUNDDESC: 'A set of lock picks lies on the ground.',
        SHORTDESC: 'a set of lock picks',
        LONGDESC: 'A set of fine picks for picking locks.',
        DESCWORDS: ['lockpicks', 'picks', 'set']},
    'Silly Glasses': {
        GROUNDDESC: 'A pair of those silly gag glasses with the nose and fake mustache rest on the ground.',
        SHORTDESC: 'a pair of silly fake mustache glasses',
        LONGDESC: 'These glasses have a fake nose and mustache attached to them. The perfect disguise!',
        DESCWORDS: ['glasses', 'silly', 'fake', 'mustache']},
    'Meat Pie': {
        GROUNDDESC: 'A suspicious meat pie rests on the ground.',
        SHORTDESC: 'a meat pie',
        LONGDESC: 'A meat pie. It tastes like chicken.',
        EDIBLE: True,
        DESCWORDS: ['pie', 'meat']},
    'Bagel': {
        GROUNDDESC: 'A bagel rests on the ground. (Gross.)',
        SHORTDESC: 'a bagel',
        LONGDESC: 'It is a donut-shaped bagel.',
        EDIBLE: True,
        DESCWORDS: ['bagel']},
    'Donut': {
        GROUNDDESC: 'A donut rests on the ground. (Gross.)',
        SHORTDESC: 'a donut',
        LONGDESC: 'It is a bagel-shaped donut.',
        EDIBLE: True,
        DESCWORDS: ['donut']},
    'Crystal Ball': {
        GROUNDDESC: 'A glowing crystal ball rests on a small pillow.',
        SHORTDESC: 'a crystal ball',
        LONGDESC: 'The crystal ball swirls with mystical energy, forming the words "Answer Unclear. Check Again Later."',
        DESCWORDS: ['crystal', 'ball']},
    'Floating Book': {
        GROUNDDESC: 'A magical book floats here.',
        SHORTDESC: 'a floating book',
        LONGDESC: 'This magical tomb doesn\'t have a lot of pictures in it. Boring!',
        DESCWORDS: ['book', 'floating']},
    'Telescope': {
        GROUNDDESC: 'A telescope is bolted to the ground.',
        SHORTDESC: 'a telescope',
        LONGDESC: 'Using the telescope, you can see your house from here!',
        TAKEABLE: False,
        DESCWORDS: ['telescope']},
    'README Note': {
        GROUNDDESC: 'A note titled "README" rests on the ground.',
        SHORTDESC: 'a README note',
        LONGDESC: 'The README note reads, "Welcome to the text adventure demo. Be sure to check out the source code to see how this game is put together."',
        EDIBLE: True,
        DESCWORDS: ['readme', 'note']},
    'Shop Howto': {
        GROUNDDESC: 'A "Shopping HOWTO" note rests on the ground.',
        SHORTDESC: 'a shopping howto',
        LONGDESC: 'The note reads, "When you are at a shop, you can type "list" to show what is for sale. "buy <item>" will add it to your inventory, or you can sell an item in your inventory with "sell <item>". (Currently, money is not implemented in this program.)',
        EDIBLE: True,
        DESCWORDS: ['howto', 'note', 'shop']},
    }

"""
These variables track where the player is and what is in their inventory.
The value in the location variable will always be a key in the world variable
and the value in the inventory list will always be a key in the worldItems
variable.
"""
location = 'Town Square' # start in town square
inventory = ['README Note', 'Sword', 'Donut'] # start with blank inventory
showFullExits = True

import cmd, textwrap

def displayLocation(loc):
    """A helper function for displaying an area's description and exits."""
    # Print the room name.
    print(loc)
    print('=' * len(loc))

    # Print the room's description (using textwrap.wrap())
    print('\n'.join(textwrap.wrap(worldRooms[loc][DESC], SCREEN_WIDTH)))

    # Print all the items on the ground.
    if len(worldRooms[loc][GROUND]) > 0:
        print()
        for item in worldRooms[loc][GROUND]:
            print(worldItems[item][GROUNDDESC])

    # Print all the exits.
    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
        if direction in worldRooms[loc].keys():
            exits.append(direction.title())
    print()
    if showFullExits:
        for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
            if direction in worldRooms[location]:
                print('%s: %s' % (direction.title(), worldRooms[location][direction]))
    else:
        print('Exits: %s' % ' '.join(exits))


def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global location

    if direction in worldRooms[location]:
        print('You move to the %s.' % direction)
        location = worldRooms[location][direction]
        displayLocation(location)
    else:
        print('You cannot move in that direction')


# TEMPORARY CODE:
while True:
    displayLocation(location)
    response = input()
    if response == 'quit':
        break
    if response in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
        moveDirection(response)