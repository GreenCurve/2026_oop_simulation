
# Our class OOP project here

import string 
import random
import sys    
import time   
import os

if os.name == 'nt':
    os.system('color')

class Lifeform:
    
    def __init__(self, location = None,init_energy = 0):
        self.energy = 0
        self.location = location
        self._r = 225
        self._g = 0
        self._b = 0
        self.symbol = random.choice(string.ascii_letters)
        self.repr_tresh = 4000
        self.sus_cost = 500
        
    def act(self,map):
        self.energy -= self.sus_cost
        if self.energy < 0:
            self.die(map)
            return
        self.move(map)
        if self.energy>self.repr_tresh:
            self.reproduce(map)
    
    def move(self, map):
        x_offset =random.randint(-1, 1)
        y_offset =random.randint(-1, 1)
        new_x = (self.location.x+x_offset) % (len(map.cells))
        new_y = (self.location.y+y_offset) % (len(map.cells))
        if not map.cells[new_x][new_y].inhabitant:
            self.location.inhabitant = None
            self.location = map.cells[new_x][new_y]
            map.cells[new_x][new_y].inhabitant = self
    
    def eat(self, map, lifeform):
        """
        Docstring for eat
        INSERT BEHAVIOR HERE
        """
        self.energy += lifeform.energy
        lifeform.die(map)

    def reproduce(self, map):
        """
        Docstring for reproduce
        INSERT BEHAVIOR HERE
        """
        x_offset =random.randint(-1, 1)
        y_offset =random.randint(-1, 1)
        new_x = (self.location.x+x_offset) % (len(map.cells))
        new_y = (self.location.y+y_offset) % (len(map.cells))
        if not map.cells[new_x][new_y].inhabitant:
            self.energy= self.energy/2
            offspring = type(self)(map.cells[new_x][new_y],init_energy = self.energy)
            map.cells[new_x][new_y].inhabitant = offspring
            map.lifeforms.append(offspring)

        

    def die(self, map):
        """
        Docstring for die
        INSERT BEHAVIOR HERE
        """
        self.location.erase_lifeform(self)
        try:
            index = map.lifeforms.index(self)
            map.lifeforms.pop(index)
        except ValueError:
            pass

        del self
        
            
    
    def render(self):
        return(self.symbol,self._r,self._g,self._b)
    
class Grass(Lifeform):
    """
    Docstring for Grass
    INSERT BEHAVIOR HERE
    """
    def __init__(self,location,init_energy = 1000):
        super().__init__(location = location)
        self._r = 20
        self._g = 70
        self._b = 20
        self.symbol = '#'
        self.energy = init_energy



class Sheep(Lifeform):
    """
    Docstring for Sheep
    INSERT BEHAVIOR HERE
    """

    def __init__(self,location,init_energy = 1000):
        super().__init__(location = location)
        self._r = 100
        self._g = 100
        self._b = 200
        self.symbol = 'O'
        self.energy = init_energy


    def move(self,map):
        super().move(map = map)
        if self.location.vegetation:
            self.eat(map,self.location.vegetation)


class Wolf(Lifeform):
    """
    Docstring for Wolf
    INSERT BEHAVIOR HERE
    """
    def __init__(self,location,init_energy = 1000):
        super().__init__(location = location)
        self._r = 200
        self._g = 100
        self._b = 100
        self.symbol = 'X'
        self.energy = init_energy
        self.sus_cost = 30
        self.repr_tresh = 10000

    def move(self,map):
        x_offset = random.randint(-1, 1)
        y_offset = random.randint(-1, 1)
        new_x = (self.location.x+x_offset) % (len(map.cells))
        new_y = (self.location.y+y_offset) % (len(map.cells))
        target_cell = map.cells[new_x][new_y]
        
        if target_cell.inhabitant and type(target_cell.inhabitant) != type(self):
            prey = target_cell.inhabitant
            self.location.inhabitant = None
            self.location = target_cell
            target_cell.inhabitant = self
            self.eat(map, prey)
        elif not target_cell.inhabitant:
            self.location.inhabitant = None
            self.location = target_cell
            target_cell.inhabitant = self



class Map:
    
    def __init__(self,lifeform_count, n = 10,):
        self.size = n
        self.lifeform_count = lifeform_count
        self.lifeforms = []
        self.cells = dict()
        for i in range(0,self.size):
            self.cells[i] = dict()
            for j in range(0,self.size):
                self.cells[i][j] = Cell(i,j)
                
    def render(self):
        render_str = ""
        for i in range(0,self.size):
            render_str += "\n"
            for j in range(0,self.size):
                render_str += self.cells[i][j].render() + " "
        return(render_str)

    def setup(self):
        for i in range(0,self.lifeform_count):
            x = random.randint(0, self.size-1) 
            y = random.randint(0, self.size-1)
            new_life = Sheep(self.cells[x][y])
            self.lifeforms.append(new_life)
            self.cells[x][y].inhabitant = new_life

        for i in range(0,self.lifeform_count):
            x = random.randint(0, self.size-1) 
            y = random.randint(0, self.size-1)
            new_life = Wolf(self.cells[x][y])
            self.lifeforms.append(new_life)
            self.cells[x][y].inhabitant = new_life
    
class Cell:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "."
        self.inhabitant = None
        self.vegetation = None
        
    def render(self):
            symbol, red, green, blue = '.', 225, 225, 255
            if (self.inhabitant):
                symbol, red, green, blue = self.inhabitant.render()
            bg_code = ""
            if self.vegetation:
                grass_symbol, bg_red, bg_green, bg_blue = self.vegetation.render()
                bg_code = f"\x1b[48;2;{bg_red};{bg_green};{bg_blue}m"
            render = f"{bg_code}\x1b[1m\x1b[38;2;{red};{green};{blue}m{symbol}\x1b[0m"
            return render
    
    def erase_lifeform(self,lifeform):
        if self.vegetation == lifeform:
            self.vegetation = None
        if self.inhabitant == lifeform:
            self.inhabitant = None

class Simulation:
    
    def __init__(self, timestep = 0.125, iterations = 3, map_size = 10,lifeform_count = 5):
        self._dynamic_terminal = DynamicTerminal(map_size+2)
        self.max_iter = iterations
        self.time_step = timestep
        self.current_iter = 0
        self.terminated = False
        self.lifeform_count = lifeform_count
        self.map_size = map_size
        self.map = Map(self.lifeform_count, map_size)
        self.map.setup()
              
        
    def step(self):
        if self.current_iter < self.max_iter:
            self.current_iter += 1
            self.update()
            self.render()
        else:
            self.terminated = True
            print(f"The simulation has terminated after {self.current_iter} iterations.")
            
    def update(self):
        time.sleep(self.time_step)

        for cell_row in self.map.cells.values():
            for cell in cell_row.values():
                if not cell.vegetation:
                    chance = random. randint(0, 100)
                    if chance > 90:
                        new_veg = Grass(cell)
                        cell.vegetation = new_veg

        for lifeform in self.map.lifeforms:
            lifeform.act(self.map)

    
    def render(self):
        self._dynamic_terminal.render(["Round " + str(self.current_iter),self.map.render()],self.map_size+2)
        
class DynamicTerminal:
    """The dynamic termin provides an interface to repaint multiple rows in the terminal and animate the simulation"""

    def __init__(self,nrows = 12):
        for i in range(0,nrows):
            print("")

    def move_cursor_up(self, lines: int):
        """Move cursor up <lines> lines."""
        sys.stdout.write(f'\x1b[{lines}A')   # ESC[<n>A
        sys.stdout.flush()

    def rewrite_lines(self, new_lines):
        """Write <new_lines> starting at the current cursor position."""
        sys.stdout.write('\n'.join(new_lines) + '\n')
        sys.stdout.flush()

    def clear_line(self):
        """Clear the entire current line (ESC[2K)."""
        sys.stdout.write('\x1b[2K')
        sys.stdout.flush()

    def render(self, text, nrows):
        self.move_cursor_up(nrows)
        self.clear_line()
        self.rewrite_lines(text)
        
if __name__ == "__main__":
    sim = Simulation(iterations=10000,map_size = 30,lifeform_count = 10,timestep=0.125)
    while(not sim.terminated):
        sim.step()
