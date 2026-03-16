import time
import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Anime Super Jump Stars")
font = pygame.font.SysFont("Arial", 24)



################################################################################################################

class Skills:
    def __init__(self, name, damage, spent, cooldown):
        self.name = name
        self.damage = damage
        self.spent = spent
        self.cooldown = cooldown
        self.last_use = 0


#note: the method will tell you if the skill can be used.

    def ready(self):
        now = time.time()
        return now - self.last_use >= self.cooldown

#note: the method that executes the attack.


    def use(self, user, target):

         if not self.ready():
             remaining = self.cooldown - (time.time() - self.last_use)
             print(f"{self.name} is on cooldown: {remaining:.1f}s")
             return

         if user.stand_energy < self.spent:
             print(f"{user.name} does not have enough Stand Energy!")
             return

         #spend energy
         user.stand_energy -= self.spent

         #apply damage
         damage_done = self.damage
         target.life -= damage_done

         #update cooldown
         self.last_use = time.time()

         print(f"{user.name} used {self.name}!")
         print(f"{target.name} received {damage_done} damage!")

#######################################################################################################################



def draw_skills(player):

    y = 500

    for skill in player.skills:

        if skill.ready():
            text = f"{skill.name} - READY"
        else:
            remaining = skill.cooldown - (time.time() - skill.last_use)
            text = f"{skill.name} - {remaining:.1f}s"

        skill_text = font.render(text, True, (255, 255, 255))
        screen.blit(skill_text, (50, y))

        y += 30





#################################################################################################################
class StandUser:

    def __init__(self, name, life,stand_energy, damage, skills):
        self.name = name
        self.life = life
        self.stand_energy = stand_energy
        self.damage = damage
        self.skills = skills

    def attack(self, target):


        damage_done = self.damage
        target.life -= damage_done

        print(f"{self.name} attacked {target.name}")
        print(f"{target.name} received {damage_done} damage!")

#################################################################################################################
def show_status(player, enemy):

    print("\n---------------------------")
    print(f"{player.name} - Life: {player.life} | Stand Energy: {player.stand_energy}")
    print(f"{enemy.name} - Life: {enemy.life}")
    print("---------------------------")
#################################################################################################################
def show_skills(player):

    print("\nSkills:")

    for i, skill in enumerate(player.skills):

        if skill.ready():
            status = "READY"
        else:
            remaining = skill.cooldown - (time.time() - skill.last_use)
            status = f"{remaining:.1f}s"

        print(f"{i+1} - {skill.name} (Energy: {skill.spent}) [{status}]")

    print("3 - Basic Attack")
#################################################################################################################
class FloatingText:

    def __init__(self, text, x, y,color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.timer = 60

    def update(self):
        self.y -= 1
        self.timer -= 1

    def draw(self):
        dmg_text = font.render(self.text, True, self.color)
        screen.blit(dmg_text, (self.x, self.y))

#################################################################################################################

#note Skills:

ora_ora = Skills("ORA ORA", 25, 6,3)
star_finger = Skills("Star Finger", 18, 6,7)

#note characters

jotaro = StandUser("Jotaro", 180,100, 17,[ora_ora, star_finger])
dio = StandUser("Dio", 190,160, 19, [])

##################################################################################################################
clock = pygame.time.Clock()





running = True

while running:

    clock.tick(60)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                jotaro.skills[0].use(jotaro,dio)

            if event.key == pygame.K_2:
                jotaro.skills[1].use(jotaro,dio)

            if event.key == pygame.K_SPACE:
                jotaro.attack(dio)

    screen.fill((0,0,0))

    #note Show Characters Name
    jotaro_text = font.render("Jotaro", True, (255, 255, 255))
    dio_text = font.render("Dio", True, (255, 255, 255))

    screen.blit(jotaro_text, (50, 20))
    screen.blit(dio_text, (550, 20))

    #note Lifebar
    draw_health_bar(50, 50, jotaro.life, jotaro.max_life)
    draw_health_bar(550, 50, dio.life, dio.max_life)
    draw_skills(jotaro)


    for text in floating_texts[:]:
        text.update()
        text.draw()

        if text.timer <= 0:
            floating_texts.remove(text)


    if dio.life > 0 and jotaro.life > 0:

        now = time.time()

        if now - last_enemy_attack >= enemy_cooldown:
            dio.attack(jotaro)
            last_enemy_attack = now



    if jotaro.life <= 0:
        print("Dio venceu!")
        running = False

    if dio.life <= 0:
        print("Jotaro venceu!")
        running = False

    pygame.display.update()

