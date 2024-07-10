from openai import OpenAI
import keyboard
import random

client = OpenAI(
    api_key="sk-proj-MfQUU6kDUqNSxpmi7q9ET3BlbkFJbM27VwUuRHqM4qi2ePKh"

)


def prettyness(lol):
    system_data = [
        {"role": "system",
         "content": "An adventurer is fighting a giant rat with a sword. Write a description for an attack when prompted with the type of the attack, who is attacking and amount of damage."},
        {"role": "user", "content": lol}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=system_data
    )

    assistant_response = response.choices[0].message.content
    system_data.append({"role": "assistant", "content": assistant_response})
    print(assistant_response)


# map variables
map = [['#', '#', '#', '#', '#'],
       ['#', '#', '#', '#', '#'],
       ['#', '#', 'H', '#', 'E'],
       ['#', '#', '#', '#', '#'],
       ['#', '#', '#', '#', '#']
       ]
playercords = [2, 2]
playerinv = [[], [], [], [], []]
playerState = "map"

# fighting variables
level = 1
playerHealth = 100
playerStam = 100
enemyStam = 100
enemyHealth = 10
enemyAttack = 5
playerAttack = 10
running = True
checke = False


def left():
    movePlayer(0, -1)


def right():
    movePlayer(0, 1)


def up():
    movePlayer(-1, 0)


def down():
    movePlayer(1, 0)


# def map():
#
def updateMap():
    clear = lambda: print("\033c", end="", flush=True)
    for y in range(5):
        print(map[y])


def movePlayer(moveX, moveY):
    try:
        global checke
        if map[playercords[0] + moveX][playercords[1] + moveY] == "E":
            global encounter
            encounter = [playercords[0] + moveX, playercords[1] + moveY]
            checke = True
        else:
            map[playercords[0] + moveX][playercords[1] + moveY] = "H"

            map[playercords[0]][playercords[1]] = "#"

            updateMap()

            playercords[0] += moveX
            playercords[1] += moveY
    except:
        map[playercords[0]][playercords[1]] = "H"
        updateMap()
        return


# end map section

# combat starts here
def enemyhit():
    global enemyAttack
    global enemyHealth
    global enemyStam
    global playerHealth
    path = random.randint(1, 3)
    match path:
        case 1:
            damage = (enemyAttack + (enemyAttack * (random.randint(-10, 10) / 100)))
            playerHealth -= damage
            prettyness('rat quick attack' + str(damage))
        case 2:
            if enemyStam <= 35:
                enemyStam += 10
                prettyness('rat recovers 10 stamina')
            else:
                damage = (enemyAttack * 1.75 + (enemyAttack * (random.randint(-20, 20) / 100)))
                playerHealth -= damage
                prettyness('rat heavy attack' + str(damage))
                enemyStam -= 20
        case 3:
            enemyStam += 10
            prettyness('rat recovers 10 stamina')


def attack():
    global enemyHealth
    damage = (playerAttack + (playerAttack * (random.randint(-10, 10) / 100)))
    enemyHealth -= damage
    prettyness('adventurer quick attack' + str(damage))
    print(str(playerHealth) + "                  " + str(enemyHealth))
    print(str(playerStam) + "                  " + str(enemyStam))
    enemyhit()


def heavyattack():
    global enemyHealth
    global playerStam
    damage = (playerAttack * 1.75 + (playerAttack * (random.randint(-20, 20) / 100)))
    enemyHealth -= damage
    prettyness('adventurer Heavy attack' + str(damage))
    playerStam -= 10
    print(str(playerHealth) + "                  " + str(enemyHealth))
    print(str(playerStam) + "                  " + str(enemyStam))
    enemyhit()


def recover():
    global playerStam
    playerStam += 10
    print(str(playerHealth) + "                  " + str(enemyHealth))
    print(str(playerStam) + "                  " + str(enemyStam))
    enemyhit()


def combat():
    global playerHealth
    global enemyHealth
    global playerState
    keyboard.add_hotkey('a', attack)
    keyboard.add_hotkey('s', heavyattack)

    print(str(playerHealth) + "                  " + str(enemyHealth))
    print(str(playerStam) + "                  " + str(enemyStam))
    while playerState == "combat":

        if playerHealth <= 0:
            global running
            playerState = 'map'
            print("You Died")
            running = False
        if enemyHealth <= 0:
            global encounter
            global enemyAlive
            spawn()
            map[encounter[0]][encounter[1]] = '#'
            global checke
            checke = False

            keyboard.unhook_all_hotkeys()
            prettyness("The hero manages to vanquish the rat in in one final burst of effort")
            playerState = 'map'

            updateMap()


def spawn():
    x = random.randint(0, 4)
    y = random.randint(0, 4)
    if map[x][y] == "#":
        map[x][y] = 'E'
    else:
        spawn()


def mapload():
    keyboard.add_hotkey('a', left)
    keyboard.add_hotkey('d', right)
    keyboard.add_hotkey('w', up)
    keyboard.add_hotkey('s', down)
    global playerState
    while playerState == 'map':
        if checke == True:
            keyboard.unhook_all_hotkeys()
            playerState = 'combat'


updateMap()
while running:
    if playerState == "map":
        mapload()
    if playerState == 'combat':
        combat()






