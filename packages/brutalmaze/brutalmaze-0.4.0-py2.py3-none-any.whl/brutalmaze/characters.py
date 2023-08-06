# -*- coding: utf-8 -*-
# characters.py - module for hero and enemy classes
# This file is part of brutalmaze
#
# brutalmaze is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# brutalmaze is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with brutalmaze.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2017 Nguyễn Gia Phong

__doc__ = 'brutalmaze module for hero and enemy classes'

from collections import deque
from math import atan, atan2, sin, pi
from random import choice, randrange, shuffle
from sys import modules

import pygame
from pygame.mixer import Sound
from pygame.time import get_ticks

from .constants import *
from .misc import sign, cosin, randsign, regpoly, fill_aapolygon, choices, play
from .weapons import Bullet


class Hero:
    """Object representing the hero.

    Attributes:
        surface (pygame.Surface): the display to draw on
        x, y (int): coordinates of the center of the hero (in pixels)
        angle (float): angle of the direction the hero pointing (in radians)
        color (tuple of pygame.Color): colors of the hero on different HPs
        R (int): circumradius of the regular triangle representing the hero
        next_heal (int): the tick that the hero gains back healing ability
        next_beat (int): the tick to play next heart beat
        next_strike (int): the tick that the hero can do the next attack
        slashing (bool): flag indicates if the hero is doing close-range attack
        firing (bool): flag indicates if the hero is doing long-range attack
        dead (bool): flag indicates if the hero is dead
        spin_speed (float): speed of spinning (in frames per slash)
        spin_queue (float): frames left to finish spinning
        wound (float): amount of wound
        sfx_heart (Sound): heart beat sound effect
    """
    def __init__(self, surface, fps):
        self.surface = surface
        w, h = self.surface.get_width(), self.surface.get_height()
        self.x, self.y = w >> 1, h >> 1
        self.angle, self.color = pi / 4, TANGO['Aluminium']
        self.R = (w * h / sin(pi*2/3) / 624) ** 0.5

        self.next_heal = self.next_beat = self.next_strike = 0
        self.slashing = self.firing = self.dead = False
        self.spin_speed = fps / HERO_HP
        self.spin_queue = self.wound = 0.0

        self.sfx_heart = Sound(SFX_HEART)

    def update(self, fps):
        """Update the hero."""
        if self.dead:
            self.spin_queue = 0.0
            return
        old_speed, time = self.spin_speed, get_ticks()
        self.spin_speed = fps / (HERO_HP-self.wound**0.5)
        self.spin_queue *= self.spin_speed / old_speed
        if time > self.next_heal:
            self.wound -= HEAL_SPEED / self.spin_speed / HERO_HP
            if self.wound < 0: self.wound = 0.0
        if time > self.next_beat:
            self.sfx_heart.play()
            self.next_beat = time + MIN_BEAT*(2 - self.wound/HERO_HP)

        if self.slashing and time >= self.next_strike:
            self.next_strike = time + ATTACK_SPEED
            self.spin_queue = randsign() * self.spin_speed
        if abs(self.spin_queue) > 0.5:
            self.angle += sign(self.spin_queue) * pi / 2 / self.spin_speed
            self.spin_queue -= sign(self.spin_queue)
        else:
            # Follow the mouse cursor
            x, y = pygame.mouse.get_pos()
            self.angle = atan2(y - self.y, x - self.x)
            self.spin_queue = 0.0
        trigon = regpoly(3, self.R, self.angle, self.x, self.y)
        fill_aapolygon(self.surface, trigon, self.color[int(self.wound)])

    def resize(self):
        """Resize the hero."""
        w, h = self.surface.get_width(), self.surface.get_height()
        self.x, self.y = w >> 1, h >> 1
        self.R = (w * h / sin(pi*2/3) / 624) ** 0.5


class Enemy:
    """Object representing an enemy.

    Attributes:
        maze (Maze): the maze
        x, y (int): coordinates of the center of the enemy (in grids)
        angle (float): angle of the direction the enemy pointing (in radians)
        color (str): enemy's color name
        awake (bool): flag indicates if the enemy is active
        next_strike (int): the tick that the enemy can do the next attack
        move_speed (float): speed of movement (in frames per grid)
        offsetx, offsety (integer): steps moved from the center of the grid
        spin_speed (float): speed of spinning (in frames per slash)
        spin_queue (float): frames left to finish spinning
        wound (float): amount of wound
        sfx_slash (Sound): sound effect indicating close-range attack damage
    """
    def __init__(self, maze, x, y, color):
        self.maze = maze
        self.x, self.y = x, y
        self.maze.map[x][y] = ENEMY
        self.angle, self.color = pi / 4, color

        self.awake = False
        self.next_strike = 0
        self.move_speed = self.maze.fps / ENEMY_SPEED
        self.offsetx = self.offsety = 0
        self.spin_speed = self.maze.fps / ENEMY_HP
        self.spin_queue = self.wound = 0.0

        self.sfx_slash = Sound(SFX_SLASH_HERO)

    def get_pos(self):
        """Return coordinate of the center of the enemy."""
        x, y = self.maze.get_pos(self.x, self.y)
        step = self.maze.distance * HERO_SPEED / self.maze.fps
        return x + self.offsetx*step, y + self.offsety*step

    def place(self, x=0, y=0):
        """Move the enemy by (x, y) (in grids)."""
        self.x += x
        self.y += y
        self.maze.map[self.x][self.y] = ENEMY

    def wake(self):
        """Wake the enemy up if it can see the hero.

        Return None if the enemy is already awake, True if the function
        has just woken it, False otherwise.
        """
        if self.awake: return None
        startx = starty = MIDDLE
        stopx, stopy, distance = self.x, self.y, self.maze.distance
        if startx > stopx: startx, stopx = stopx, startx
        if starty > stopy: starty, stopy = stopy, starty
        dx = (self.x-MIDDLE)*distance + self.maze.centerx - self.maze.x
        dy = (self.y-MIDDLE)*distance + self.maze.centery - self.maze.y
        mind = cosin(abs(atan(dy / dx)) if dx else 0) * distance
        def get_distance(x, y): return abs(dy*x - dx*y) / (dy**2 + dx**2)**0.5
        for i in range(startx, stopx + 1):
            for j in range(starty, stopy + 1):
                if self.maze.map[i][j] != WALL: continue
                x, y = self.maze.get_pos(i, j)
                if get_distance(x - self.maze.x, y - self.maze.y) <= mind:
                    return False
        self.awake = True
        play(self.maze.sfx_spawn, self.maze.get_distance(*self.get_pos()),
             self.get_angle() + pi)
        return True

    def fire(self):
        """Return True if the enemy has just fired, False otherwise."""
        if self.maze.hero.dead: return False
        x, y = self.get_pos()
        if (self.maze.get_distance(x, y) > FIRANGE*self.maze.distance
            or get_ticks() < self.next_strike
            or (self.x, self.y) in AROUND_HERO or self.offsetx or self.offsety
            or randrange((self.maze.hero.slashing+self.maze.isfast()+1) * 3)):
            return False
        self.next_strike = get_ticks() + ATTACK_SPEED
        self.maze.bullets.append(
            Bullet(self.maze.surface, x, y, self.get_angle() + pi, self.color))
        return True

    def move(self, speed=ENEMY_SPEED):
        """Return True if it has just moved, False otherwise."""
        if self.offsetx:
            self.offsetx -= sign(self.offsetx)
            return True
        if self.offsety:
            self.offsety -= sign(self.offsety)
            return True
        if get_ticks() < self.next_strike: return False

        self.move_speed = self.maze.fps / speed
        directions = [(sign(MIDDLE - self.x), 0), (0, sign(MIDDLE - self.y))]
        shuffle(directions)
        directions.append(choice(ADJACENT_GRIDS))
        if self.maze.hero.dead: directions = choice(ADJACENT_GRIDS),
        for x, y in directions:
            if (x or y) and self.maze.map[self.x + x][self.y + y] == EMPTY:
                self.offsetx = round(x * (1 - self.move_speed))
                self.offsety = round(y * (1 - self.move_speed))
                self.maze.map[self.x][self.y] = EMPTY
                self.place(x, y)
                return True
        return False

    def get_slash(self):
        """Return the enemy's close-range damage."""
        d = self.maze.slashd - self.maze.get_distance(*self.get_pos())
        wound = d / self.maze.hero.R
        return wound if wound > 0 else 0.0

    def slash(self):
        """Return the enemy's close-range damage per frame."""
        wound = self.get_slash() / self.spin_speed
        if self.spin_queue: self.maze.hit_hero(wound, self.color)
        return wound

    def get_angle(self, reversed=False):
        """Return the angle of the vector whose initial point is
        the center of the screen and terminal point is the center of
        the enemy.
        """
        x, y = self.get_pos()
        return atan2(y - self.maze.y, x - self.maze.x)

    def draw(self):
        """Draw the enemy."""
        radious = self.maze.distance/SQRT2 - self.awake*2
        square = regpoly(4, radious, self.angle, *self.get_pos())
        color = TANGO[self.color][int(self.wound)] if self.awake else FG_COLOR
        fill_aapolygon(self.maze.surface, square, color)

    def update(self):
        """Update the enemy."""
        if self.awake:
            self.spin_speed, tmp = self.maze.fps / ENEMY_HP, self.spin_speed
            self.spin_queue *= self.spin_speed / tmp
            if not self.spin_queue and not self.fire() and not self.move():
                self.spin_queue = randsign() * self.spin_speed
                if not self.maze.hero.dead:
                    play(self.sfx_slash, self.get_slash(), self.get_angle())
            if abs(self.spin_queue) > 0.5:
                self.angle += sign(self.spin_queue) * pi / 2 / self.spin_speed
                self.spin_queue -= sign(self.spin_queue)
            else:
                self.angle, self.spin_queue = pi / 4, 0.0
        if self.awake or get_ticks() >= self.maze.next_move: self.draw()

    def hit(self, wound):
        """Handle the enemy when it's attacked."""
        self.wound += wound

    def die(self):
        """Handle the enemy's death."""
        if self.awake:
            self.maze.map[self.x][self.y] = EMPTY
            if self.maze.enemy_weights[self.color] > MINW + 1.5:
                self.maze.enemy_weights[self.color] -= 1.5
        else:
            self.maze.map[self.x][self.y] = WALL


class Chameleon(Enemy):
    """Object representing an enemy of Chameleon.

    Additional attributes:
        visible (int): the tick until which the Chameleon is visible
    """
    def __init__(self, maze, x, y):
        Enemy.__init__(self, maze, x, y, 'Chameleon')
        self.visible = 0

    def wake(self):
        """Wake the Chameleon up if it can see the hero."""
        if Enemy.wake(self) is True:
            self.visible = get_ticks() + 1000//ENEMY_SPEED

    def draw(self):
        """Draw the Chameleon."""
        if (not self.awake or self.spin_queue
            or get_ticks() < max(self.visible, self.maze.next_move)):
            Enemy.draw(self)

    def hit(self, wound):
        """Handle the Chameleon when it's attacked."""
        self.visible = get_ticks() + 1000//ENEMY_SPEED
        Enemy.hit(self, wound)


class Plum(Enemy):
    """Object representing an enemy of Plum."""
    def __init__(self, maze, x, y):
        Enemy.__init__(self, maze, x, y, 'Plum')

    def clone(self, other):
        """Turn the other enemy into a clone of this Plum and return
        True if that enemy is also a Plum, otherwise return False.
        """
        if other.color != 'Plum': return False
        other.x, other.y, other.angle = self.x, self.y, self.angle
        other.awake, other.next_strike = True, self.next_strike
        other.offsetx, other.offsety = self.offsetx, self.offsety
        other.spin_queue, other.wound = self.spin_queue, self.wound
        return True


class ScarletRed(Enemy):
    """Object representing an enemy of Scarlet Red."""
    def __init__(self, maze, x, y):
        Enemy.__init__(self, maze, x, y, 'ScarletRed')

    def fire(self):
        """Scarlet Red doesn't shoot."""
        return False

    def move(self):
        return Enemy.move(self, ENEMY_SPEED * SQRT2)

    def slash(self):
        """Handle the Scarlet Red's close-range attack."""
        self.wound -= Enemy.slash(self)
        if self.wound < 0: self.wound = 0.0


def new_enemy(maze, x, y):
    """Return an enemy of a random type in the grid (x, y)."""
    color = choices(maze.enemy_weights)
    try:
        return getattr(modules[__name__], color)(maze, x, y)
    except AttributeError:
        return Enemy(maze, x, y, color)
