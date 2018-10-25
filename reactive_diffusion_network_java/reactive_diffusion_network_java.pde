import java.util.Arrays;
import java.io.FileWriter;

Cell[][] cells;

int LENGTH = 50;

void setup() {

    size(50, 50);
    colorMode(HSB);
    
    cells = new Cell[LENGTH][LENGTH];
    
    for (int y = 0; y < LENGTH; y++) {
      for (int x = 0; x < LENGTH; x++) {
        
        float u = 1.0;
        float v = 0.0;
        
        if (x > LENGTH * 0.5 - 5 && x < LENGTH * 0.5 + 5 &&
            y > LENGTH * 0.5 - 5 && y < LENGTH * 0.5 + 5) {
            
              v = 1.0;
        }
        
        Cell cell = new Cell(x, y, u, v);
        cells[y][x] = cell;
      }
    }
    
    
    for (int y = 0; y < LENGTH; y++) {
      for (int x = 0; x < LENGTH; x++) {
        
        Cell cell = cells[y][x];
        
        int next_x = abs((x + 1) % LENGTH);
        int prev_x = abs((x - 1) % LENGTH);
        int next_y = abs((y + 1) % LENGTH);
        int prev_y = abs((y - 1) % LENGTH);

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
  
    System.out.println(frameRate);

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
 
 void keyPressed() {
 
     if (key == 's') {
       write();
     }
 
 }
 
 void write() {
 
  PrintWriter output = createWriter("." + File.separator + "output" + File.separator + String.valueOf(frameCount) + ".csv"); 
     
  for (int y = 0; y < LENGTH; y++) {
    for (int x = 0; x < LENGTH; x++) {
      Cell cell = cells[y][x];
      String text = String.format("%d,%d,%f", x, y, cell.get_raw_h());
      output.println(text);
    }
  }
 
  output.flush();
  output.close();
 }
