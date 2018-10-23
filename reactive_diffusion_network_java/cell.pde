import java.util.ArrayList;
import java.util.List;

static float Da = 1.0;
static float Db = 0.5;
static float f  = 0.0545;
static float k  = 0.062;
static float dt = 1;
static float kf = k + f;


class Cell {
  
  int x, y;
  float u, v, u_calculated, v_calculated;
  List<Cell> neighbors = new ArrayList<Cell>();
  List<Float> r_neighbors = new ArrayList<Float>();
  
  public Cell(int x, int y, float u, float v) {
  
     this.x = x;
     this.y = y;
     this.u = u;
     this.v = v;
     this.u_calculated = 1.0;
     this.v_calculated = 0.0;
  }
  
  public void calculate() {
    
    float[] lap = this.get_laplacian();
    float u_lap = lap[0];
    float v_lap = lap[1];
    
    this.u_calculated = this.u + (Da * u_lap - this.u * this.v * this.v + f * (1.0 - this.u)) * dt;
    this.v_calculated = this.v + (Db * v_lap + this.u * this.v * this.v - kf * this.v) * dt;

    this.u_calculated = constrain(this.u_calculated, 0.0, 1.0);
    this.v_calculated = constrain(this.v_calculated, 0.0, 1.0);
  }
  
  public void update() {
  
    this.u = this.u_calculated;
    this.v = this.v_calculated;
  }
  
  private float[] get_laplacian() {

    float u_sum = -this.u;
    float v_sum = -this.v;
    for (int i = 0; i < this.neighbors.size(); i++) {

       Cell n  = this.neighbors.get(i);
       float r = this.r_neighbors.get(i);
       u_sum += n.u * r;
       v_sum += n.v * r;
    }
    
    return new float[]{u_sum, v_sum};
  }

}
