Da = 1.0
Db = 0.5
f  = 0.0545
k  = 0.062
dt = 1

kf = k + f

class Cell():

    def __init__(self, x, y, u, v):
        
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.u_calculated = 1
        self.v_calculated = 0
        self.neighbors = []
        self.r_neighbors = []

    def calculate(self):
        
        u_lap, v_lap = self.get_laplacian()
        
        self.u_calculated = self.u + (Da * u_lap - self.u * self.v * self.v + f * (1.0 - self.u)) * dt
        self.v_calculated = self.v + (Db * v_lap + self.u * self.v * self.v - kf * self.v) * dt
        
        self.u_calculated = constrain(self.u_calculated, 0, 1)
        self.v_calculated = constrain(self.v_calculated, 0, 1)
        
    def get_laplacian(self):
                
        u_sum, v_sum = -self.u, -self.v
        for (n, r) in zip(self.neighbors, self.r_neighbors):
            u_sum += n.u * r
            v_sum += n.v * r
            
        return u_sum, v_sum

    def update(self):
        
        self.u = self.u_calculated
        self.v = self.v_calculated
