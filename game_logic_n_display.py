#Display and Game|
#----------------/
import sys
import pygame
import pygame.freetype
import timeit

import map_txt_reading as readmap
import astar_search as astar
import agent as ag
from constant_value import *

class pacman_game:
    #INIT ---------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        pygame.init()
        #Setup window frame
        self.screen  = pygame.display.set_mode((s_display_W, s_display_H)) #pygame.NOFRAME
        self.caption = pygame.display.set_caption(s_display_caption, s_display_iconpath)
        self.font    = pygame.freetype.Font(r'Resources/Product_Sans_Regular.otf', 16)

        #Load Display Stage
        self.mainmenu_bg  = pygame.image.load(s_display_bg)
        self.button_shade = pygame.image.load(s_button_shade)
        self.about_bg     = pygame.image.load(s_display_ab)
        self.level_bg     = pygame.image.load(s_display_lv)
        self.map_bg       = pygame.image.load(s_display_pm)
        self.gameplay_bg  = pygame.image.load(s_display_gp)
        self.map_playbutton_shade = pygame.image.load(s_button_shade_mapplay)
        self.map_before_shade     = pygame.image.load(s_button_shade_map_before)
        self.map_after_shade      = pygame.image.load(s_button_shade_map_after)

        #Game play function
        self.button_playhome_shade = pygame.image.load(s_button_shade_playhome)
        self.button_playhome       = pygame.image.load(s_button_shade_playhome_clean)
        self.button_playsped_shade = pygame.image.load(s_button_shade_playsped)
        self.button_playsped       = pygame.image.load(s_button_shade_playsped_clean)
        self.button_playsped_inner = pygame.image.load(s_button_inner_playsped)
        self.score_blank           = pygame.image.load(s_score_blank)

        #Victory / GameOver
        self.game_victory_bg  = pygame.image.load(s_display_victory)
        self.game_gameover_bg = pygame.image.load(s_display_gameover)

        #Stage. Mouse and FPS Control
        self.stage = s_display_home
        self.clock = pygame.time.Clock()
        self.mouse = None

        #Load Map
        self.map_index = 0
        self.map = pygame.image.load(s_map_gra_path[self.map_index])

        #Game logic
        self.score = 0
        self.level = 1
        self.speed = 1


    #GAME RUNNING ------------------------------------------------------------------------------------------------------------------------------------------------
    def run(self):
        while True:
            #Main Menu
            if self.stage == s_display_home:
                self.mainmenu_display()
                self.mainmenu_get_action()
            #About
            elif self.stage == s_display_about:
                self.aboutinfo_display()
                self.about_get_action()
            #Pick Level
            elif self.stage == s_display_play:
                self.picklevel_display()
                self.level_get_action()
            #Pick Map
            elif self.stage == s_display_map:
                self.pickmap_display()
                self.map_get_action()
            #Play Game
            elif self.stage == s_display_game:
                self.playgame_display()
                #Set Value to default and Start Game
                self.score = 0
                #Text
                text_surf, text_rect = self.font.render("Score", s_color_while)
                self.screen.blit(text_surf, s_pos_score)
                pygame.display.update(s_pos_score)
                #Speed
                text_sped, text_rect = self.font.render("1x", s_color_while)
                self.screen.blit(text_sped, s_pos_speedvalue)
                pygame.display.update(s_pos_speedvalue)
                #
                if self.level == 1:
                    self.pacman_lv1()
                elif self.level == 2:
                    self.pacman_lv2()
                elif self.level == 3:
                    self.pacman_lv3()
                elif self.level == 4:
                    self.pacman_lv4()
            elif self.stage == s_display_f_vic:
                self.game_victory_screen()
                self.game_victory_action()
                pygame.display.update()
            elif self.stage == s_display_f_ove:
                self.game_gameover_screen()
                self.game_gameover_action()
                pygame.display.update()

            self.clock.tick(s_display_fps)

    #DISPLAY STAGE (Menu, About, Level)---------------------------------------------------------------------------------

    #Display Main_Menu
    def mainmenu_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.mainmenu_bg, (0, 0))
        pygame.display.update()

    #Display About
    def aboutinfo_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.about_bg, (0, 0))
        pygame.display.update()

    #Display Level picking
    def picklevel_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.level_bg, (0, 0))
        pygame.display.update()

    #Display Map picking
    def pickmap_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.map_bg, (0,0))
        self.show_map_option()
        pygame.display.update()

    def show_map_option(self):
        self.map = pygame.image.load(s_map_gra_path[self.map_index])
        pygame.display.update(self.screen.blit(pygame.transform.scale(self.map, (350, 375)), (125, 162)))

    # STAGE ACTION (Menu, About, Level)---------------------------------------------------------------------------------

    #Main_Screen Action
    def mainmenu_get_action(self):
        for event in pygame.event.get():
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if x and y
                if 220 <= self.mouse[0] <= 380 and 350 <= self.mouse[1] <= 410:
                    self.stage = s_display_play
                elif 220 <= self.mouse[0] <= 380 and 440 <= self.mouse[1] <= 500:
                    self.stage = s_display_about
                elif 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
                    pygame.quit()
                    sys.exit()
            # Quit game :<
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()

        #Create Button Shade
        if 220 <= self.mouse[0] <= 380 and 350 <= self.mouse[1] <= 410:
            self.screen.blit(self.button_shade, (220, 350))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 440 <= self.mouse[1] <= 500:
            self.screen.blit(self.button_shade, (220, 440))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
            self.screen.blit(self.button_shade, (220, 530))
            pygame.display.update()

    # About_Screen Action
    def about_get_action(self):
        for event in pygame.event.get():
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
                    self.stage = s_display_home
            # Quit game :<
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()

        # Create Button Shade
        if 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
            #self.screen.blit(self.button_shade, (220, 530))
            pygame.display.update(self.screen.blit(self.button_shade, (220, 530)))

    #Level_Screen Action
    def level_get_action(self):
        for event in pygame.event.get():
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Back
                if 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
                    self.stage = s_display_home
                #Level 1
                elif 220 <= self.mouse[0] <= 380 and 170 <= self.mouse[1] <= 230:
                    self.stage = s_display_map
                    self.level = 1
                #Level 2
                elif 220 <= self.mouse[0] <= 380 and 260 <= self.mouse[1] <= 320:
                    self.stage = s_display_map
                    self.level = 2
                #Level 3
                elif 220 <= self.mouse[0] <= 380 and 350 <= self.mouse[1] <= 410:
                    self.stage = s_display_map
                    self.level = 3
                #Level 4
                elif 220 <= self.mouse[0] <= 380 and 440 <= self.mouse[1] <= 500:
                    self.stage = s_display_map
                    self.level = 4
            # Quit game :<
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()

        # Create Button Shade
        if 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
            self.screen.blit(self.button_shade, (220, 530))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 170 <= self.mouse[1] <= 230:
            self.screen.blit(self.button_shade, (220, 170))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 260 <= self.mouse[1] <= 320:
            self.screen.blit(self.button_shade, (220, 260))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 350 <= self.mouse[1] <= 410:
            self.screen.blit(self.button_shade, (220, 350))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 440 <= self.mouse[1] <= 500:
            self.screen.blit(self.button_shade, (220, 440))
            pygame.display.update()

    #Map_Screen Action
    def map_get_action(self):
        for event in pygame.event.get():
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Play
                if 251 <= self.mouse[0] <= 349 and 555 <= self.mouse[1] <= 603:
                    self.stage = s_display_game
                #Before
                elif 186 <= self.mouse[0] <= 234 and 555 <= self.mouse[1] <= 603:
                    if self.map_index == 0:
                        self.map_index = 4
                    else:
                        self.map_index -= 1
                #After
                elif 366 <= self.mouse[0] <= 414 and 555 <= self.mouse[1] <= 603:
                    if self.map_index == 4:
                        self.map_index = 0
                    else:
                        self.map_index += 1
                #Back
                elif 251 <= self.mouse[0] <= 349 and 625 <= self.mouse[1] <= 673:
                    self.stage = s_display_play
            # Quit game
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()

        # Create Button Shade
        if 251 <= self.mouse[0] <= 349 and 555 <= self.mouse[1] <= 603:
            pygame.display.update(self.screen.blit(self.map_playbutton_shade, (250, 554)))
        elif 186 <= self.mouse[0] <= 234 and 555 <= self.mouse[1] <= 603:
            pygame.display.update(self.screen.blit(self.map_before_shade, (185, 554)))
        elif 366 <= self.mouse[0] <= 414 and 555 <= self.mouse[1] <= 603:
            pygame.display.update(self.screen.blit(self.map_after_shade, (365, 554)))
        elif 251 <= self.mouse[0] <= 349 and 625 <= self.mouse[1] <= 673:
            pygame.display.update(self.screen.blit(self.map_playbutton_shade, (250, 624)))

    # GAME LEVEL PLAY -------------------------------------------------------------------------------------------------

    #Play Game Display
    def playgame_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.gameplay_bg, (0, 0))
        #LOAD MAP
        self.screen.blit(self.map, (20, 40))
        pygame.display.update()

    #Play Game Action
    def play_get_action(self):
        #Detect event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Home button
                if 480 <= self.mouse[0] <= 540 and 661 <= self.mouse[1] <= 681:
                    self.stage = s_display_home
                #Speed button
                elif 550 <= self.mouse[0] <= 580 and 661 <= self.mouse[1] <= 681:
                    #change game speed (change delay time)
                    if self.speed == 1:
                        self.speed = 2
                        pygame.display.update(self.screen.blit(self.button_playsped_inner, (549, 664)))
                        text_sped, text_rect = self.font.render("2x", s_color_while)
                        self.screen.blit(text_sped, s_pos_speedvalue)
                        pygame.display.update(s_pos_speedvalue)
                    elif self.speed == 2:
                        self.speed = 1
                        pygame.display.update(self.screen.blit(self.button_playsped_inner, (549, 664)))
                        text_sped, text_rect = self.font.render("1x", s_color_while)
                        self.screen.blit(text_sped, s_pos_speedvalue)
                        pygame.display.update(s_pos_speedvalue)


        #Create button shade
        self.mouse = pygame.mouse.get_pos()
        if 480 <= self.mouse[0] <= 540 and 661 <= self.mouse[1] <= 681:
            pygame.display.update(self.screen.blit(self.button_playhome_shade, (479, 660)))
        elif 550 <= self.mouse[0] <= 580 and 661 <= self.mouse[1] <= 681:
            pygame.display.update(self.screen.blit(self.button_playsped_shade, (549, 660)))
        else:
            pygame.display.update(self.screen.blit(self.button_playhome, (479, 660)))
            pygame.display.update(self.screen.blit(self.button_playsped, (549, 660)))

        if self.stage == s_display_home:
            return True
        return False

    # Level 1
    def pacman_lv1(self):
        graph_map, pacman_pos, food_pos = readmap.map_level1(s_map_txt_path[self.level-1][self.map_index])
        start = timeit.default_timer()
        pathway = astar.astar_search(graph_map, pacman_pos, food_pos)
        end = timeit.default_timer()
        print('Time: ', end - start)
        #Call Pacman
        pacman = ag.Pacman(self, pacman_pos)
        pacman.pacman_call()
        #Call Food
        food = ag.Food(self, food_pos)
        food.food_display()
        #Call Monster
            #Nothing to call :v
        #Set pathway, score(0)
        goal = pathway[-1]
        pathway_togoal = pathway[1:-1]
        self.pacman_scoring(0)
        pygame.time.delay(500)

        #Go
        for loc in pathway_togoal:
            pacman.pacman_control(loc)
            self.pacman_scoring(s_score_move)
            pygame.time.delay(250//self.speed)
            #Detect event during playing game
            if self.play_get_action():
                go_home = 1
                break
            else:
                go_home = 0

        #Go to goal (if not pressed go home button)
        if go_home != 1:
            food.food_disappear()
            pacman.pacman_control(goal)
            self.pacman_scoring(s_score_gift)
            pygame.time.delay(2000)
            self.stage = s_display_f_vic
        else:
            self.stage = s_display_home

    # Level 2
    def pacman_lv2(self):
        graph_map, pacman_pos, food_pos, monsters_pos_list = readmap.map_level2(s_map_txt_path[self.level-1][self.map_index])
        pathway = astar.astar_search(graph_map, pacman_pos, food_pos)

        # Call Pacman
        pacman = ag.Pacman(self, pacman_pos)
        pacman.pacman_call()
        # Call Food
        food = ag.Food(self, food_pos)
        food.food_display()
        # Call Monster
        monsters = [ag.Monster(self, pos) for pos in monsters_pos_list]
        for mons in monsters:
            mons.monster_call()
        # Set pathway, score(0)
        goal = pathway[-1]
        pathway_togoal = pathway[1:-1]
        self.pacman_scoring(0)
        pygame.time.delay(500)

        # Go
        for loc in pathway_togoal:
            pacman.pacman_control(loc)
            self.pacman_scoring(s_score_move)
            pygame.time.delay(250 // self.speed)
            # Detect event during playing game
            if self.play_get_action():
                go_home = 1
                break
            else:
                go_home = 0

        # Go to goal (if not pressed go home button)
        if go_home != 1:
            food.food_disappear()
            pacman.pacman_control(goal)
            self.pacman_scoring(s_score_gift)
            pygame.time.delay(2000)
            self.stage = s_display_f_vic
        else:
            self.stage = s_display_home


    # Level 3
    def pacman_lv3(self):
        print('ha3')

    # Level 4
    def pacman_lv4(self):
        print('ha4')

    #Scoring
    def pacman_scoring(self, score):
        #Write
        self.score += score
        if self.stage == s_display_game:
            pygame.display.update(self.screen.blit(self.score_blank, (s_pos_scorevalue[0], s_pos_scorevalue[1])))
            text_score, text_rect_score = self.font.render(str(self.score), s_color_while)
            self.screen.blit(text_score, s_pos_scorevalue)
            pygame.display.update(s_pos_scorevalue)


    #FINISH ------------------------------------------------------------------------------------------------------------
    def game_victory_screen(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.game_victory_bg, (0, 0))
        score_font = pygame.freetype.Font(r'Resources/Product_Sans_Regular.otf', 40)
        text_score, text_rect_score = score_font.render(str(self.score), s_color_while)
        text_rect_score.center = (300, 450)
        self.screen.blit(text_score, text_rect_score)
        pygame.display.update()

    def game_victory_action(self):
        for event in pygame.event.get():
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Back
                if 251 <= self.mouse[0] <= 349 and 625 <= self.mouse[1] <= 673:
                    self.stage = s_display_home
            # Quit game
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()

        # Create Button Shade
        if 251 <= self.mouse[0] <= 349 and 625 <= self.mouse[1] <= 673:
            pygame.display.update(self.screen.blit(self.map_playbutton_shade, (250, 624)))

    def game_gameover_screen(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.game_gameover_bg, (0, 0))
        pygame.display.update()

    def game_gameover_action(self):
        for event in pygame.event.get():
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Back
                if 251 <= self.mouse[0] <= 349 and 625 <= self.mouse[1] <= 673:
                    self.stage = s_display_home
            # Quit game
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()

        # Create Button Shade
        if 251 <= self.mouse[0] <= 349 and 625 <= self.mouse[1] <= 673:
            pygame.display.update(self.screen.blit(self.map_playbutton_shade, (250, 624)))