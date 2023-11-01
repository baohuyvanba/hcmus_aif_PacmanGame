#Display and Game|
#----------------/
import sys
import pygame
import pygame.freetype
import timeit
import random

import map_txt_reading as readmap
import map_txt_builder as buildmap
import astar_search as astar
import agent as ag
import localsearch as ls
from constant_value import *

class pacman_game:
    #INIT ---------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        pygame.init()
        #Setup window frame
        self.screen  = pygame.display.set_mode((s_display_W, s_display_H)) #pygame.NOFRAME
        self.caption = pygame.display.set_caption(s_display_caption, s_display_iconpath)

        #Load Font
        self.font    = pygame.freetype.Font(s_font_path, 16)

        #Load Display Stage
        self.mainmenu_bg  = pygame.image.load(s_display_bg)
        self.button_shade = pygame.image.load(s_button_shade)
        self.about_bg     = pygame.image.load(s_display_ab)
        self.level_bg     = pygame.image.load(s_display_lv)
        self.map_bg       = pygame.image.load(s_display_pm)
        self.gameplay_bg  = pygame.image.load(s_display_gp)

        # Victory / GameOver Stage
        self.game_victory_bg  = pygame.image.load(s_display_victory)
        self.game_gameover_bg = pygame.image.load(s_display_gameover)

        #Button shade
        self.map_playbutton_shade = pygame.image.load(s_button_shade_mapplay)
        self.map_before_shade     = pygame.image.load(s_button_shade_map_before)
        self.map_after_shade      = pygame.image.load(s_button_shade_map_after)

        #Game play function / button shade
        self.button_playhome_shade = pygame.image.load(s_button_shade_playhome)
        self.button_playhome       = pygame.image.load(s_button_shade_playhome_clean)
        self.button_playsped_shade = pygame.image.load(s_button_shade_playsped)
        self.button_playsped       = pygame.image.load(s_button_shade_playsped_clean)
        self.button_playsped_inner = pygame.image.load(s_button_inner_playsped)
        self.score_blank           = pygame.image.load(s_score_blank)

        #Stage, Mouse and FPS Control
        self.stage = s_display_home
        self.clock = pygame.time.Clock()
        self.mouse = None

        #MAP FUNCTION
            #Map index
        self.map_index = 0
            #Build map:
        for map_level in s_map_txt_path:
            for map in map_level:
                img_path = r'Resources/Game Display/map/lv' + map[22] + r'_m' + map[27] + r'.png'
                buildmap.create_maze_image(map, img_path)
            #Load first map
        self.map = pygame.image.load(s_map_gra_path[1-1][0])

        #Game logic
        self.score = 0
        self.level = 1
        self.speed = 1

        #Game time
        self.time_algorithm = 0
        self.time_play      = 0


    #GAME RUNNING ------------------------------------------------------------------------------------------------------------------------------------------------
    def run(self):
        while True:
            #Main Menu
            if self.stage == s_display_home:
                #set default
                self.level = 1
                self.score = 0
                self.map_index = 0
                self.speed = 1
                #Load and display home stage
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
                #Show gameplay stage
                self.playgame_display()
                #Set Score_value to default and Start Game
                self.score = 0
                #Show Score text
                text_surf, text_rect = self.font.render("Score", s_color_while)
                self.screen.blit(text_surf, s_pos_score)
                pygame.display.update(s_pos_score)
                #Show Speed button
                text_sped, text_rect = self.font.render("1x", s_color_while)
                self.screen.blit(text_sped, s_pos_speedvalue)
                pygame.display.update(s_pos_speedvalue)
                #
                #run game
                if self.level == 1:
                    self.pacman_lv1()
                elif self.level == 2:
                    self.pacman_lv2()
                elif self.level == 3:
                    self.pacman_lv3()
                elif self.level == 4:
                    self.pacman_lv4()
                #
            #Victory Stage
            elif self.stage == s_display_f_vic:
                self.game_victory_screen()
                self.game_victory_action()
                pygame.display.update()
            #Game Over Stage
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
        self.map = pygame.image.load(s_map_gra_path[self.level - 1][self.map_index])
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

    # GAME LEVEL PLAY --------------------------------------------------------------------------------------------------

    #Play Game Display
    def playgame_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.gameplay_bg, (0, 0))
        #LOAD MAP
        self.screen.blit(self.map, (20, 40))
        pygame.display.update()

    #Play Game Action===================================================================================================
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
                        self.speed = 4
                        pygame.display.update(self.screen.blit(self.button_playsped_inner, (549, 664)))
                        text_sped, text_rect = self.font.render("4x", s_color_while)
                        self.screen.blit(text_sped, s_pos_speedvalue)
                        pygame.display.update(s_pos_speedvalue)
                    elif self.speed == 4:
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

    # Level 1-----------------------------------------------------------------------------------------------------------
    def pacman_lv1(self):
        graph_map, pacman_pos, food_pos = readmap.map_level1(s_map_txt_path[self.level-1][self.map_index])

        start = timeit.default_timer()
        #Run A*
        pathway = astar.astar_search(graph_map, pacman_pos, food_pos)
        #
        self.time_algorithm = timeit.default_timer() - start

        #Call Pacman
        pacman = ag.Pacman(self, pacman_pos)
        pacman.pacman_call()
        #Call Food
        food = ag.Food(self, food_pos)
        food.food_display()
        #Call Monster: No

        start = timeit.default_timer()
        #Have pathway to goal
        if pathway is not None:
            print(pathway)
            #Set pathway, score(0)
            goal = pathway[-1]
            pathway_togoal = pathway[1:-1]
            self.pacman_scoring(0)
            pygame.time.delay(500)
            go_home = 0
            #Go
            for loc in pathway_togoal:
                pacman.pacman_control(loc)
                self.pacman_scoring(s_score_move)
                pygame.time.delay(s_time_delay//self.speed)
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
                self.time_play = timeit.default_timer() - start
                self.stage = s_display_f_vic
            else:
                self.stage = s_display_home
        #Have no pathway to goal
        else:
            self.stage = s_display_f_ove

    # Level 2-----------------------------------------------------------------------------------------------------------
    def pacman_lv2(self):
        graph_map, pacman_pos, food_pos, monsters_pos_list = readmap.map_level2(s_map_txt_path[self.level-1][self.map_index], True)
        start = timeit.default_timer()
        #Run A*
        pathway = astar.astar_search(graph_map, pacman_pos, food_pos)
        #
        self.time_algorithm = timeit.default_timer() - start

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

        start = timeit.default_timer()
        if pathway is not None:
            # Set pathway, score(0)
            goal = pathway[-1]
            pathway_togoal = pathway[1:-1]
            self.pacman_scoring(0)
            pygame.time.delay(500)

            #Go
            for loc in pathway_togoal:
                pacman.pacman_control(loc)
                self.pacman_scoring(s_score_move)
                pygame.time.delay(s_time_delay // self.speed)
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
                self.time_play = timeit.default_timer() - start
                self.stage = s_display_f_vic
            else:
                self.stage = s_display_home

        #No possible pathway exists with monster is considered as wall. So, just go and die X.X, 100% game over
        else:
            #Build again without fake wall
            graph_map, pacman_pos, food_pos, monsters_pos_list = readmap.map_level2(s_map_txt_path[self.level - 1][self.map_index], False)
            start = timeit.default_timer()
            #Run A*
            pathway = astar.astar_search(graph_map, pacman_pos, food_pos)
            #
            self.time_algorithm = timeit.default_timer() - start

            self.time_play = -1
            if pathway is not None:
                # Set pathway, score(0)
                goal = pathway[-1]
                pathway_togoal = pathway[1:-1]
                self.pacman_scoring(0)
                pygame.time.delay(500)

                # Go
                for loc in pathway_togoal:
                    pacman.pacman_control(loc)
                    self.pacman_scoring(s_score_move)
                    pygame.time.delay(s_time_delay // self.speed)
                    # Detect event during playing game
                    if self.play_get_action():
                        go_home = 1
                        break
                    else:
                        go_home = 0

                    if loc in monsters_pos_list:
                        break

                # Go to goal (if possible)
                if go_home != 1:
                    pygame.time.delay(2000)
                    self.stage = s_display_f_ove
                else:
                    self.stage = s_display_home
            else:
                self.stage = s_display_f_ove

    # Level 3-----------------------------------------------------------------------------------------------------------
    def pacman_lv3(self):
        cells, map_graph, pacman_cell, food_cell_list, monsters_cell_list = readmap.map_level3(s_map_txt_path[self.level-1][self.map_index])

        # Call Pacman
        pacman = ag.Pacman(self, pacman_cell.position, pacman_cell)
        pacman.pacman_call()
        # Call Food
        foods = [ag.Food(self, food_cell.position, food_cell) for food_cell in food_cell_list]
        for foo in foods:
            foo.food_display()
        # Call Monster
        monsters = [ag.Monster(self, monster_cell.position, monster_cell) for monster_cell in monsters_cell_list]
        for mons in monsters:
            mons.monster_call()

        start = timeit.default_timer()
        #Scan for the first time
        pacman.scan_radar(map_graph)
        #
        self.time_algorithm = timeit.default_timer() - start

        #Go
        go_home = 0     #go to home stage
        catch   = 0     #catch by monster
        start_play = timeit.default_timer()
        while True:
            #Is Pacman going back to get food, which have position saved in Pacman's memory.
            is_backtracking = False
            #Pacman's previous cell
            pacman_pre_cell = pacman.cell

            #Get out current cell
            pacman.cell.out_pacman()
            #Scan map
            pacman.scan_radar(map_graph)

            if not pacman.check_detected_food() and not pacman.check_food():
                #No detected_food in memory and no food in visibility area
                pacman.cell = pacman.back_track(map_graph)
                is_backtracking = True
            else:
                # Pacman moves with heuristic local search:
                start = timeit.default_timer()
                #
                pacman.cell = ls.local_search(cells, map_graph, pacman.cell)
                #
                self.time_algorithm += timeit.default_timer() - start

            pacman.cell.in_pacman()
            pacman.pacman_control(pacman.cell.position)
            self.pacman_scoring(s_score_move)

            if not is_backtracking:
                pacman.add_path(pacman_pre_cell)

            #Check if Monsters've got Pacman's heart <3
            for monster in monsters:
                if pacman.cell.position == monster.cell.position:
                    pygame.time.delay(5000)
                    self.stage = s_display_f_ove
                    catch = 1
                    break
            if catch:
                break

            # Pacman eats Food?
            for food in foods:
                if food.cell.position == pacman.cell.position:
                    foods.remove(food)
                    self.pacman_scoring(s_score_gift)
                    for i in range(len(pacman.detected_food)):
                        if pacman.detected_food[i] == pacman.cell:
                            pacman.detected_food.remove(pacman.detected_food[i])
                            pacman.path_to_detected_food.remove(pacman.path_to_detected_food[i])
                            break

            #Monsters's moving around.
            for monster in monsters:
                monster_old_cell = monster.cell

                monster.cell.out_monster()

                next_cell = monster.initial_cell                                                #Gán tạm thời: bước tiếp theo là qua về vị trí ban đầu
                if monster.cell.position == monster.initial_cell.position:                      #Nếu Monster đang ở vị trí ban đầu thì cho nó đi các cell lân cận
                    around_cell_list = monster.get_around_cells_of_initial_cell(map_graph)
                    next_cell_index = random.randint(0, len(around_cell_list) - 1)
                    next_cell = around_cell_list[next_cell_index]

                monster.cell = next_cell
                monster.cell.in_monster()
                monster.monster_control(monster.cell.position)

                if monster_old_cell.food_here():
                    temp_food = ag.Food(self, monster_old_cell.position, monster_old_cell)
                    temp_food.food_display()

            # Monsters catch Pacman
            for monster in monsters:
                if pacman.cell.position == monster.cell.position:
                    pygame.time.delay(5000)
                    self.stage = s_display_f_ove
                    catch = 1
                    break
            if catch:
                break

            # Pacman win
            if len(foods) == 0:
                pygame.time.delay(200)
                self.time_play = timeit.default_timer() - start_play
                self.stage = s_display_f_vic
                go_home = 0
                break

            pygame.time.delay(s_time_delay // self.speed)

            #Game play action
            if self.play_get_action():
                go_home = 1
                break

        if go_home:
            self.stage = s_display_home

    # Level 4-----------------------------------------------------------------------------------------------------------
    def pacman_lv4(self):
        cells, map_graph, ori_map_graph, pacman_cell, food_cell_list, monsters_cell_list = readmap.map_level4(s_map_txt_path[self.level - 1][self.map_index])

        # Call Pacman
        pacman = ag.Pacman(self, pacman_cell.position, pacman_cell)
        pacman.pacman_call()

        # Call Food
        foods = [ag.Food(self, food_cell.position, food_cell) for food_cell in food_cell_list]
        for food in foods:
            food.food_display()

        # Call Monster
        monsters = [ag.Monster(self, monster_cell.position, monster_cell) for monster_cell in monsters_cell_list]
        for mons in monsters:
            mons.monster_call()

        # Scan for the first time
        pacman.scan_radar(map_graph)

        # Go
        go_home = 0  # go to home stage
        catch = 0    # catch by monster
        while True:
            # Is Pacman going back to get food, which have position saved in Pacman's memory.
            is_backtracking = False
            # Pacman's previous cell
            pacman_pre_cell = pacman.cell

            # Get out current cell
            pacman.cell.out_pacman()
            # Scan map
            pacman.scan_radar(map_graph)

            if not pacman.check_detected_food() and not pacman.check_food() and not pacman.check_monster():
                # No detected_food in memory and no food in visibility area
                pacman.cell = pacman.back_track(map_graph)
                is_backtracking = True
            else:
                # Pacman moves with heuristic local search:
                pacman.cell = ls.local_search(cells, map_graph, pacman.cell)

                # Nowhere to go
                if pacman.cell is None:
                    self.stage = s_display_f_ove
                    break

            pacman.cell.in_pacman()
            pacman.pacman_control(pacman.cell.position)
            self.pacman_scoring(s_score_move)

            if not is_backtracking:
                pacman.add_path(pacman_pre_cell)

            # Check if Monsters've got Pacman's heart <3
            for monster in monsters:
                if pacman.cell.position == monster.cell.position:
                    pygame.time.delay(200)
                    self.stage = s_display_f_ove
                    catch = 1
                    break
            if catch:
                break

            # Pacman eats Food?
            for food in foods:
                if food.cell.position == pacman.cell.position:
                    foods.remove(food)
                    self.pacman_scoring(s_score_gift)
                    for i in range(len(pacman.detected_food)):
                        if pacman.detected_food[i] == pacman.cell:
                            pacman.detected_food.remove(pacman.detected_food[i])
                            pacman.path_to_detected_food.remove(pacman.path_to_detected_food[i])
                            break

            # Monsters move
            for monster in monsters:
                monster_old_cell = monster.cell
                monster.cell.out_monster()

                next_cell_list = astar.astar_search(ori_map_graph, monster.cell.position, pacman.cell.position)
                next_cell = next_cell_list[1]
                around_cell_list = monster.get_around_cells(map_graph)
                for cell in around_cell_list:
                    if cell.position == next_cell:
                        monster.cell = cell
                        break

                monster.cell.in_monster()
                monster.monster_control(monster.cell.position)

                if monster_old_cell.food_here():
                    temp_food = ag.Food(self, monster_old_cell.position, monster_old_cell)
                    temp_food.food_display()

            # Monsters catch Pacman
            for monster in monsters:
                if pacman.cell.position == monster.cell.position:
                    pygame.time.delay(200)
                    self.stage = s_display_f_ove
                    catch = 1
                    break
            if catch:
                break

            # Pacman win
            if len(foods) == 0:
                pygame.time.delay(200)
                self.stage = s_display_f_vic
                go_home = 0
                break

            pygame.time.delay(250 // self.speed)

            # Game play action
            if self.play_get_action():
                go_home = 1
                break

        if go_home:
            self.stage = s_display_home

    #Scoring------------------------------------------------------------------------------------------------------------
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

        score_font = pygame.freetype.Font(r'Resources/Font/Product_Sans_Regular.otf', 40)
        text_score, text_rect_score = score_font.render(str(self.score), s_color_while)
        text_rect_score.center = (300, 450)
        self.screen.blit(text_score, text_rect_score)
        #
        print(self.time_algorithm)
        print(self.time_play)
        #
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