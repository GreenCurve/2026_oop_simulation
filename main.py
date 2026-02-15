
# Our class OOP project here

import string 
import random
import sys    
import time   
import os

if os.name == 'nt':
    os.system('color')

class Lifeform:
    
    def __init__(self, location = None):
        self.location = location
        self._r = 225
        self._g = 0
        self._b = 0
        self.symbol = random.choice(string.ascii_letters)
        
    def act(self, map):
        self.move(map)
    
    def move(self, map):
        x_offset =random.randint(-1, 1)
        y_offset =random.randint(-1, 1)
        new_x = (self.location.x+x_offset) % (len(map.cells))
        new_y = (self.location.y+y_offset) % (len(map.cells))
        if not map.cells[new_x][new_y].inhabitant:
            self.location.inhabitant = None
            self.location = map.cells[new_x][new_y]
            map.cells[new_x][new_y].inhabitant = self
    
    def eat(self, map):
        """
        Docstring for eat
        INSERT BEHAVIOR HERE
        """
        pass

    def reproduce(self, map):
        """
        Docstring for reproduce
        INSERT BEHAVIOR HERE
        """
        pass

    def die(self, map):
        """
        Docstring for die
        INSERT BEHAVIOR HERE
        """
        pass
            
    
    def render(self):
        return(self.symbol,self._r,self._g,self._b)
    
class Grass(Lifeform):
    """
    Docstring for Grass
    INSERT BEHAVIOR HERE
    """
    pass

class Sheep(Lifeform):
    """
    Docstring for Sheep
    INSERT BEHAVIOR HERE
    """
    pass

class Wolf(Lifeform):
    """
    Docstring for Wolf
    INSERT BEHAVIOR HERE
    """
    pass

class Map:
    
    def __init__(self, n = 10):
        self.size = n
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
                bg_red, bg_green, bg_blue = 20, 70, 20
                bg_code = f"\x1b[48;2;{bg_red};{bg_green};{bg_blue}m"
            render = f"{bg_code}\x1b[1m\x1b[38;2;{red};{green};{blue}m{symbol}\x1b[0m"
            return render

class Simulation:
    
    def __init__(self, timestep = 0.125, iterations = 3, map_size = 10,lifeform_count = 5):
        self._dynamic_terminal = DynamicTerminal(map_size+2)
        self.max_iter = iterations
        self.time_step = timestep
        self.current_iter = 0
        self.terminated = False
        self.lifeform_count = lifeform_count
        self.map_size = map_size
        self.map = Map(map_size)
        self.lifeforms = list()
        self.setup()
        
    def setup(self):
        for i in range(0,self.lifeform_count):
            x = random.randint(0, self.map_size-1) 
            y = random.randint(0, self.map_size-1)
            new_life = Lifeform(self.map.cells[x][y])
            self.lifeforms.append(new_life)
            self.map.cells[x][y].inhabitant = new_life
        
        
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
        for lifeform in self.lifeforms:
            lifeform.act(self.map)
        for cell_row in self.map.cells.values():
            for cell in cell_row.values():
                if not cell.vegetation:
                    chance = random. randint(0, 100)
                    if chance > 66:
                        cell.vegetation = True
    
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
    sim = Simulation(iterations=50,map_size = 30,lifeform_count = 10,timestep=1)
    while(not sim.terminated):
        sim.step()
