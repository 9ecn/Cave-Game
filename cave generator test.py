import pygame
import os
import noise
import random

class Grid:
	def __init__(self, screen_size, screen):
		self.screen_size = screen_size
		self.screen = screen
		self.tile_size = 4
		self.grid_size = (int(self.screen_size[0] / self.tile_size), int(self.screen_size[1] / self.tile_size))

		self.percentage = 48

		self.grid = self.generate_map()

	def apply_cellular_automaton(self):
		temp_grid = self.grid

		for y in range(self.grid_size[1]):
			for x in range(self.grid_size[0]):
				neighbor_wall_count = 0

				try:
					for j in range(-1, 2):
						for k in range(-1, 2):
							if y != j and x != k:
								if temp_grid[j + y][k + x] == 0:
									neighbor_wall_count += 1
				except:
					neighbor_wall_count += 1

				if neighbor_wall_count > 4:
					self.grid[y][x] = 0
				else:
					self.grid[y][x] = 1


	def generate_map(self):
		grid = []

		for y in range(int(self.screen_size[1] / self.tile_size)):
			row = []
			for x in range(int(self.screen_size[0] / self.tile_size)):
				height = round(noise.pnoise1(x * 0.1, repeat=99999999) * 5, 0)
				if random.randint(0,100) < self.percentage - height:
					row.append(1)
				else:
					row.append(0)
			grid.append(row)

		return grid

	def draw(self):
		pos = [0,0]

		for row in self.grid:
			pos[0] = 0
			for tile in row:
				if tile == 1:
					pygame.draw.rect(self.screen, (255,255,255), (pos[0], pos[1], self.tile_size, self.tile_size))
				if tile == 2:
					pygame.draw.rect(self.screen, (0,255,0), (pos[0], pos[1], self.tile_size, self.tile_size))

				pos[0] += self.tile_size
			pos[1] += self.tile_size


class Game:
	def __init__(self):
		self.screen_size = (720, 480)
		self.screen = pygame.display.set_mode(self.screen_size)
		self.bgcolor = (0,0,0)
		self.fps = 60
		self.clock = pygame.time.Clock()
		self.running = True

		self.grid = Grid(self.screen_size, self.screen)

	def loop_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.grid.apply_cellular_automaton()

	def update(self):
		pass

	def draw_display(self):
		self.screen.fill(self.bgcolor)

		self.grid.draw()

		pygame.display.flip()

	def run(self):
		while self.running:
			self.loop_events()
			self.draw_display()
			self.update()
			self.clock.tick(self.fps)
		pygame.quit()
		exit()

def main():
	os.environ["SDL_VIDEO_CENTERED"] = "1"
	pygame.init()
	game = Game()
	game.run()

if __name__ == "__main__":
    main()
