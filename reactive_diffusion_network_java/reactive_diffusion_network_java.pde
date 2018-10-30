import java.util.Arrays;
import java.io.FileWriter;

Cell[][] cells;

int LENGTH = 400;
int UNIT_LENGTH = 100;
int NUM_INITIAL_ATTRACTORS = 50;

void setup() {

    size(400, 400);
    colorMode(HSB);
    frameRate(120);

    cells = new Cell[LENGTH][LENGTH];
    
    ArrayList<ArrayList<Integer>> attractors = new ArrayList<ArrayList<Integer>>();
    for (int i = 0; i < NUM_INITIAL_ATTRACTORS; i++) {
      ArrayList<Integer> attractor = new ArrayList<Integer>();
      
      attractor.add(Integer.valueOf(int(random(0, LENGTH))));
      attractor.add(Integer.valueOf(int(random(0, LENGTH))));

      attractors.add(attractor);
    }
    
    for (int y = 0; y < LENGTH; y++) {
      for (int x = 0; x < LENGTH; x++) {
        
        float u = 1.0;
        float v = 0.0;
        
        boolean is_attracted = false;
        for (ArrayList<Integer> attractor: attractors) {
          
          int ax = attractor.get(0);
          int ay = attractor.get(1);

          if (x > ax - 5 && x < ax + 5 && y > ay - 5 && y < ay + 5) {
            is_attracted = true;
          }
        }
        
        if (is_attracted) {
        
            v = 1.0;
        }      
        
        for (int i = 0; i < 1; i++) {
          if (x > random(LENGTH) - 5 && x < random(LENGTH) + 5 &&
              y > random(LENGTH) - 5 && y < random(LENGTH) + 5) {
              
                v = 1.0;
          }        
        }
        
        Cell cell = new Cell(x, y, u, v);
        cells[y][x] = cell;
      }
    }
    
    
    
    for (int y = 0; y < LENGTH; y++) {
      for (int x = 0; x < LENGTH; x++) {
        
        Cell cell = cells[y][x];
        
        int next_x = (x + 1) % LENGTH;
        int prev_x = x > 0 ? (x - 1) % LENGTH : LENGTH - 1;
        int next_y = (y + 1) % LENGTH;
        int prev_y = y > 0 ? (y - 1) % LENGTH : LENGTH - 1;

        Cell c1 = cells[next_y][x];
        Cell c2 = cells[prev_y][x];
        Cell c3 = cells[y][next_x];
        Cell c4 = cells[y][prev_x];
        Cell c5 = cells[next_y][next_x];
        Cell c6 = cells[next_y][prev_x];
        Cell c7 = cells[prev_y][next_x];
        Cell c8 = cells[prev_y][prev_x];
        
        cell.neighbors.addAll(Arrays.asList(c1, c2, c3, c4, c5, c6, c7, c8));
        cell.r_neighbors.addAll(Arrays.asList(0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05));      
      }
    }
}

void draw() {  

    for (int y = 0; y < LENGTH; y++) {
      for (int x = 0; x < LENGTH; x++) {
        Cell cell = cells[y][x];
        cell.calculate();
      }
    }
    
    loadPixels();
    for (int y = 0; y < LENGTH; y++) {
      for (int x = 0; x < LENGTH; x++) {
        Cell cell = cells[y][x];
        cell.update();
        pixels[x + y * LENGTH] = color(cell.get_h(), 255, 255);    
      }
    }
    updatePixels();
    
    int num = int(floor(LENGTH / float(UNIT_LENGTH)));

    loadPixels();
    for (int y = 0; y < LENGTH; y++) {
      for (int x = 0; x < LENGTH; x++) {
        Cell cell = cells[y][x];
        cell.update();
        pixels[x + y * LENGTH] = color(cell.get_h(), 255, 255);
        
        int offset_x = int(floor(float(x) / UNIT_LENGTH));
        int offset_y = int(floor(float(y) / UNIT_LENGTH));
        
        int i = offset_x + offset_y * num;
        
        int new_x = x - offset_x * UNIT_LENGTH;
        int new_y = y - offset_y * UNIT_LENGTH;
        
        if (i == index) {
          pixels[new_x + new_y * LENGTH] = color(cell.get_h(), 255, 255);      
        }
      }
    }
    updatePixels();
}

 

 void mousePressed() {
   
   for (int y = mouseY-5; y <= mouseY+5; y++) {
     for (int x = mouseX-5; x <= mouseX+5; x++) {
       int xx = abs((x + 1) % LENGTH);
       int yy = abs((y + 1) % LENGTH);
       Cell cell = cells[yy][xx];
       cell.v = 1;
     }
   }  
 }
 
 int index = 0;
 
 void keyPressed() {
 
     if (key == 's') {
       write();
     } else {
       index = Integer.valueOf(key - 49);
     }
     
     
 
 }
 
 void write() {
 
  ArrayList<PrintWriter> writers = new ArrayList<PrintWriter>();
  
  for (int i = 0; i < (LENGTH * LENGTH) / (UNIT_LENGTH * UNIT_LENGTH); i++) {
  
    PrintWriter output = createWriter("." + File.separator + "output" + File.separator + String.valueOf(frameCount) + File.separator + String.valueOf(i) + ".csv"); 
    writers.add(output);
  }
  
  int num = int(floor(LENGTH / float(UNIT_LENGTH)));
  
  for (int y = 0; y < LENGTH; y++) {
    for (int x = 0; x < LENGTH; x++) {

      int offset_x = int(floor(float(x) / UNIT_LENGTH));
      int offset_y = int(floor(float(y) / UNIT_LENGTH));
      
      int i = offset_x + offset_y * num;
      PrintWriter output = writers.get(i);
    
      Cell cell = cells[y][x];
      String text = String.format("%d,%d,%f", x - offset_x * UNIT_LENGTH, y - offset_y * UNIT_LENGTH, cell.get_raw_h());
      output.println(text);
    }
  }
 
  for (PrintWriter output: writers) {
    output.flush();
    output.close();  
  }

  
  save("." + File.separator + "output" + File.separator + String.valueOf(frameCount) + ".png");
 }
