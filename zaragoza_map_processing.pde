String [ ] imFiles = {"mapa.png"};
PImage [ ] im = new PImage[1];
int def=1;
float [ ] V = new float [100];
float [ ] px = new float [100];
float [ ] py = new float [100];
float Vt;
String [ ] lines;
float [ ] lista = new float [100];
int [] px0 = {602,537,625,749,553,728,425,700};
int [] py0 = {105,238,287,357,406,117,285,138};

void setup(){
  for(int i=0; i<1; i++){
    im[i]=loadImage(imFiles[i]);
  }
  size(1051,658);
}

void draw(){
    String[] lines = loadStrings("C:/Users/Usuario/Desktop/Python/datos.txt");
    float [] lista = float(split(lines[0], ' '));
    image(im[0],0,0,1051,658);
    noStroke();
    for(int y=0; y<658; y+=def){
      for(int x=0; x<1051; x+=def){
        for(int i=0; i<8; i++){
           V[i]=4000*lista[2+i*3]/pow(sqrt(sq(px0[i]-x)+sq(py0[i]-y)),0.4);
           Vt+=V[i];
        }
        fill(int(map(Vt,400,1000,0,255)),int(map(Vt,200,1000,0,65)),0,150);
        rect(x,y,def,def);
      Vt=0;
    }
  }
}
