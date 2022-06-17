import pygame
from pygame.locals import *


class MainUI:
    start = None
    exit = None
    mouse = None

    @staticmethod
    def show_main_board(surface, difficulty):

        color = (255, 255, 255)
        font_color = (0, 0, 0)

        width, height = 500, 300
        pos = (((surface.get_width() / 2) / 2) + 15, 320)

        font_file = "./assets/fonts/SpaceMission.otf"

        font = pygame.font.Font(font_file, 110)
        menu_font = pygame.font.Font(font_file, 33)
        l_font = pygame.font.Font("./assets/fonts/EvilEmpire.ttf", 30)

        space_font = font.render("SPACE", True, color)
        shooter_font = font.render("SHOOTER", True, color)
        start_font = menu_font.render("START", True, font_color)
        exit_font = menu_font.render("EXIT", True, font_color)
        levels_font = l_font.render("Select Difficulty: (Press)  e - Easy,  m - Medium,  h - Hard", True, color)
        difficulty_font = l_font.render(f"Chosen: {difficulty}", True, color)

        main_rect = pygame.Rect(pos, (width, height))
        MainUI.start = start_rect = pygame.Rect((main_rect.left + 150, main_rect.top + 60), (200, 45))
        MainUI.exit = exit_rect = pygame.Rect((main_rect.left + 150, start_rect.bottom + 50), (200, 45))

        bg_img = pygame.image.load("./assets/images/PNG/main_screen_bg.jpg")
        bg_img = pygame.transform.scale(bg_img, (surface.get_width(), surface.get_height()))
        surface.blit(bg_img, (0, 0))

        pygame.draw.rect(surface, color, main_rect, width=-1, border_radius=12)
        pygame.draw.rect(surface, color, start_rect, border_top_left_radius=12, border_bottom_right_radius=12)
        pygame.draw.rect(surface, color, exit_rect, border_top_left_radius=12, border_bottom_right_radius=12)

        surface.blit(space_font, (98, 70))
        surface.blit(shooter_font, (420, 137))
        surface.blit(start_font, (((start_rect.x + (start_rect.width // 2) // 2) - 2), start_rect.y + 8))
        surface.blit(exit_font, ((exit_rect.x + ((exit_rect.width // 2) // 2)) + 16, exit_rect.y + 8))
        surface.blit(levels_font, (215, exit_rect.bottom + 200))
        surface.blit(difficulty_font, (surface.get_width() // 2, exit_rect.bottom + 240))

        MainUI.mouse = mouse_pos = pygame.mouse.get_pos()

        if start_rect.x <= mouse_pos[0] <= start_rect.right and 370 <= mouse_pos[1] <= 416:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        elif exit_rect.x <= mouse_pos[0] <= exit_rect.right and exit_rect.y <= mouse_pos[1] <= exit_rect.bottom:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    @staticmethod
    def start_event(event):
        if event.type == MOUSEBUTTONDOWN:
            if MainUI.start.collidepoint(MainUI.mouse):
                return True

    @staticmethod
    def exit_event(event):
        if event.type == MOUSEBUTTONDOWN:
            if MainUI.exit.collidepoint(MainUI.mouse):
                return True
