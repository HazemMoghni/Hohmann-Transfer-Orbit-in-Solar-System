GM = 1000
dt = 0.01

class Planet:
    
    def __init__(self, pos = vector(10,10,0), color = color.red, radius = 1):
        
        self.obj = sphere(pos = pos, color = color, radius = radius)
        self.torus = ring(radius = mag(self.obj.pos), axis = vector(0,0,1), thickness = 0.1*self.obj.radius, color=self.obj.color)
        self.circular()
        
    def circular(self):
        self.dist = mag(self.obj.pos)
        tangent = vector(-self.obj.pos.y, self.obj.pos.x, 0)/self.dist

        speed = sqrt(GM / self.dist)

        self.vel = speed*tangent

    def move(self):
        self.acc = -GM * self.obj.pos/mag(self.obj.pos)**3
        self.vel += self.acc * dt
        self.obj.pos += self.vel * dt

class Spaceship:

    def __init__(self, pos = vector(5,5,0), size = vector(8,8,8), make_trail= False):
        
        self.obj = box(pos = pos, size = size, make_trail = make_trail, trail_type="curve", interval=100)
        self.lbl = label(text = "at rest", pos = vector(0,-60,0))

        
        self.prepare_launch = False
        self.in_flight = False
        
        self.circular()

    def circular(self):
        self.dist = mag(self.obj.pos)
        tangent = vector(-self.obj.pos.y, self.obj.pos.x, 0)/self.dist
        speed = sqrt(GM/self.dist)

        self.vel = speed * tangent

    def move(self):
        self.acc = -GM *self.obj.pos/mag(self.obj.pos)**3
        self.vel += self.acc * dt
        self.obj.pos += self.vel * dt

        if self.prepare_launch and self.launch_window():
            self.launch()
            self.prepare_launch = False
            self.in_flight = True
            self.obj.make_trail = True

        if self.in_flight:
            if abs(mag(self.obj.pos-self.dest.obj.pos)) < self.dest.obj.radius:
                self.obj.pos = self.dest.obj.pos
                self.in_flight = False
                self.prepare_launch = False
                self.circular()
                
                self.obj.make_trail = False
                print("arrived")
                self.obj.clear_trail()
                self.lbl.text = "arrived at " + self.dest_name
  
    def set_launch_window(self, arg):
        if self.in_flight == False:
            self.dest = arg.dest
            self.dest_name = arg.text
            a = (mag(self.obj.pos) + mag(self.dest.obj.pos))/2
            r = mag(self.dest.obj.pos)
            self.phi = ((180.0*(a/r)**1.5)) %(360.0)

            if self.phi < 180.0:
                self.theta = 180.0 - self.phi
            if self.phi > 180.0:
                self.theta = 540.0 - self.phi

            self.prepare_launch = True
            self.in_flight = False
            print('phi=', self.phi)
            print('theta=', self.theta)
            self.lbl.text = "Waiting for \n launch window for \n" + self.dest_name

    def launch_window(self):
        if abs(sudut(self.obj.pos, self.dest.obj.pos) - self.theta) <0.1:
            self.lbl.text = "Flying to "+ self.dest_name
            return True

    def launch(self):
        r = mag(self.obj.pos)
        a = (r + mag(self.dest.obj.pos))/2
        speed = sqrt(GM * (2/r - 1/a))
        tangent = vector(-self.obj.pos.y, self.obj.pos.x, 0)/mag(self.obj.pos)
        self.vel = speed * tangent

def sudut(a, b):

    theta = acos( dot(a, b) /(mag(a)*mag(b))) *180.0/pi

    s = cross(a, b)
    if s.z < 0:
        theta = 360.0 - theta
        
    return theta

scene = canvas(width = 600, height = 400, title = "<h2>Hohmann Transfer Orbit</h2>")
teks = """This simulation shows a spaceship travelling between the planets in a Hohmann Transfer Orbit!
Click on any button under the display for demonstration."""
scene.append_to_title(teks)

sun = sphere(radius = 10, color=color.orange)

p1 = Planet(pos = vector(20, 0, 0), radius = 5, color =vector(50,0,20))
p2 = Planet(pos = vector(50, 0, 0), color = vector(255,255,51), radius = 5)
p3 = Planet(pos = vector(100, 0, 0), color = vector(0,0,100), radius = 8)
p4 = Planet(pos = vector(170, 0, 0), color = vector(100,0,0), radius = 6)

ship = Spaceship(pos = p3.obj.pos)
ship.lbl.pos = vector(0, -150, 0)

btn1 = button(text = 'Mercury', bind = ship.set_launch_window, dest = p1)
scene.append_to_title("\t")

btn2 = button(text = 'Venus', bind = ship.set_launch_window, dest = p2)
scene.append_to_title("\t")

btn3 = button(text = 'Earth', bind = ship.set_launch_window, dest = p3)
scene.append_to_title("\t")

btn4 = button(text = 'Mars', bind = ship.set_launch_window, dest = p4)
scene.append_to_title("\t")

scene.append_to_title("\n")

sphere(pos=vector(300,0,0),texture="https://images.pexels.com/photos/956981/milky-way-starry-sky-night-sky-star-956981.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",radius=1000,shininess=1)

while True:
    rate(1000)
    p1.move()
    p2.move()
    p3.move()
    p4.move()

    ship.move()


# This was created by Riddhi (from India), Mehedi (from Bangladesh), Nayana, and Hazem Hasan (me!) durine their time in the Youth in Physics Summer Program
