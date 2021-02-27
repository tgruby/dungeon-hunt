const renderCanvas = document.getElementById("renderingCanvas");
const ctx = renderCanvas.getContext('2d');
renderCanvas.width = window.innerWidth;
renderCanvas.height = window.innerHeight;
renderCanvas.style["left"] = 0;
renderCanvas.style["top"] = 0;
renderCanvas.style["position"] = "absolute";

const blurCanvas = document.getElementById("blurCanvas");
const bcCtx = blurCanvas.getContext('2d');
blurCanvas.width = window.innerWidth;
blurCanvas.height = window.innerHeight;
blurCanvas.style["left"] = 0;
blurCanvas.style["top"] = 0;
blurCanvas.style["position"] = "absolute";

var gravityX = 0;       // global direction on x axis
var gravityY = 0.05;    // global direction on y axis

var foutain = 0;        // if 0, fountain is off, if 1 it is on

var pCreationInterval = 15;   // interval of particles creation in milliseconds
var intervalTimer;            // timer using the interval

var pSizeDecrease = 0.98;     // size decrease ratio for particles
var pSizeVariation = 2;       // size variation of fuses glow for flickering effect
var pSpeedDecrease = 0.95;    // speed decrease ratio for particles and fuses

var blastRadius = Math.min(window.innerWidth, window.innerHeight)/2;  // size of the explosion for rockets, depending on window size
var launchXspeed = window.innerWidth/200;     // x speed of fuses on launch, depending on window width
var launchYspeed = window.innerHeight/150;    // y speed of fuses on launch, depending on window height

// color collection for the fuses
const fuseColors = [
  "#ff3d3d",
  "#ff9824",
  "#fffb0a",
  "#81ff3d",
  "#3dffd8",
  "#3d64ff",
  "#913dff",
  "#ff3dc5"
];

const darkSpark = "#d66800";    // color of the sparks for rockets that didnt explode
const brightSpark = "#fffed9";  // color of the sparks for the fuses

var fuseArray = [];
var particlesArray = [];


// a fuse is a point from which particles will be drawn
class Fuse{
  // constructor
  constructor(type, x, y, dirX, dirY, size, color, pCount, lifeSpan, children){
    this.type = type;
    this.x = x;
    this.y = y;
    this.dirX = dirX;
    this.dirY = dirY;
    this.size = size;
    this.color = color;
    this.pCount = pCount;
    this.lifeSpan = lifeSpan;
    this.children = children;
  }

  // when the fuse has reached its lifespan
  die(){
    if(this.children > 0){
      let color;
      let color1;
      let color2;
      let type;
      let type1;
      let type2;
      let pCount;
      let dirX;
      let dirY;
      let lifeSpan;
      let radiusFactor;
      let innerFusesProportion = 0.7;
      let size = 4;
      // if this is a rocket that didnt explode yet
      if(this.type <10){
        switch(this.type){
          case 0: // same as case 1
          case 1: // monocolor, no sparks
            color = fuseColors[Math.floor(Math.random() * fuseColors.length)];
            type = 10 + Math.floor(Math.random()*5);
            pCount = 0;
            for(let i = 0; i < this.children; i++){
              dirX = Math.random() * blastRadius;
              dirY = blastRadius - dirX;
              radiusFactor = Math.random();
              lifeSpan = 100 + Math.random()*50;
              fuseArray.push(new Fuse(type, this.x, this.y, radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirX), radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirY), size, color, pCount, lifeSpan, 1));
            }
            break;
          case 2: // same as case 3
          case 3: // monocolor, with sparks
            color = fuseColors[Math.floor(Math.random() * fuseColors.length)];
            type = 15 + Math.floor(Math.random()*5);
            pCount = 1;
            for(let i = 0; i < this.children; i++){
              dirX = Math.random() * blastRadius;
              dirY = blastRadius - dirX;
              radiusFactor = Math.random();
              lifeSpan = 100 + Math.random()*50;
              fuseArray.push(new Fuse(type, this.x, this.y, radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirX), radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirY), size, color, pCount, lifeSpan, 1));
            }
            break;
          case 4: // bicolor, sparks in
            color1 = fuseColors[Math.floor(Math.random() * fuseColors.length)];
            color2 = fuseColors[Math.floor(Math.random() * fuseColors.length)];
            type1 = 10 + Math.floor(Math.random()*5);
            type2 = 15 + Math.floor(Math.random()*5);
            for(let i = 0; i < this.children; i++){
              dirX = Math.random() * blastRadius;
              dirY = blastRadius - dirX;
              lifeSpan = 100 + Math.random()*50;
              if(Math.random() > innerFusesProportion){
                // outer fuses
                radiusFactor = Math.random()*0.2 + 0.8;
                color = color1;
                type = type1;
                pCount = 0;
              }
              else{
                // inner fuses
                radiusFactor = Math.random()*0.6;
                color = color2;
                type = type2;
                pCount = 1;
              }
              fuseArray.push(new Fuse(type, this.x, this.y, radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirX), radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirY), size, color, pCount, lifeSpan, 1));
            }
            break;
          case 5: // bicolor, sparks out
            color1 = fuseColors[Math.floor(Math.random() * fuseColors.length)];
            color2 = fuseColors[Math.floor(Math.random() * fuseColors.length)];
            type1 = 15 + Math.floor(Math.random()*5);
            type2 = 10 + Math.floor(Math.random()*5);
            for(let i = 0; i < this.children; i++){
              dirX = Math.random() * blastRadius;
              dirY = blastRadius - dirX;
              lifeSpan = 100 + Math.random()*50;
              if(Math.random() > innerFusesProportion){
                // outer fuses
                radiusFactor = Math.random()*0.2 + 0.8;
                color = color1;
                type = type1;
                pCount = 1;
              }
              else{
                // inner fuses
                radiusFactor = Math.random()*0.6;
                color = color2;
                type = type2;
                pCount = 0;
              }
              fuseArray.push(new Fuse(type, this.x, this.y, radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirX), radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirY), size, color, pCount, lifeSpan, 1));
            }
            break;
          case 6: // multicolor, no sparks
            type = 10 + Math.floor(Math.random()*5);
            pCount = 0;
            for(let i = 0; i < this.children; i++){
              color = fuseColors[Math.floor(Math.random() * fuseColors.length)];
              dirX = Math.random() * blastRadius;
              dirY = blastRadius - dirX;
              radiusFactor = Math.random();
              lifeSpan = 100 + Math.random()*50;
              fuseArray.push(new Fuse(type, this.x, this.y, radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirX), radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirY), size, color, pCount, lifeSpan, 1));
            }
            break;
          case 7: // multicolor, all sparks
            type = 15 + Math.floor(Math.random()*5);
            pCount = 1;
            for(let i = 0; i < this.children; i++){
              color = fuseColors[Math.floor(Math.random() * fuseColors.length)];
              dirX = Math.random() * blastRadius;
              dirY = blastRadius - dirX;
              radiusFactor = Math.random();
              lifeSpan = 100 + Math.random()*50;
              fuseArray.push(new Fuse(type, this.x, this.y, radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirX), radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirY), size, color, pCount, lifeSpan, 1));
            }
            break;
          case 8: // multicolor, sparks in
            type1 = 10 + Math.floor(Math.random()*5);
            type2 = 15 + Math.floor(Math.random()*5);
            for(let i = 0; i < this.children; i++){
              dirX = Math.random() * blastRadius;
              dirY = blastRadius - dirX;
              lifeSpan = 100 + Math.random()*50;
              if(Math.random() > innerFusesProportion){
                // outer fuses
                radiusFactor = Math.random()*0.2 + 0.8;
                color = fuseColors[Math.floor(Math.random() * fuseColors.length)];
                type = type1;
                pCount = 0;
              }
              else{
                // inner fuses
                radiusFactor = Math.random()*0.6;
                color = brightSpark;
                type = type2;
                pCount = 1;
              }
              fuseArray.push(new Fuse(type, this.x, this.y, radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirX), radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirY), size, color, pCount, lifeSpan, 1));
            }
            break;
          case 9: // multicolor, sparks out
            type1 = 15 + Math.floor(Math.random()*5);
            type2 = 10 + Math.floor(Math.random()*5);
            for(let i = 0; i < this.children; i++){
              dirX = Math.random() * blastRadius;
              dirY = blastRadius - dirX;
              lifeSpan = 100 + Math.random()*50;
              if(Math.random() > innerFusesProportion){
                // outer fuses
                radiusFactor = Math.random()*0.2 + 0.8;
                color = brightSpark;
                type = type1;
                pCount = 1;
              }
              else{
                // inner fuses
                radiusFactor = Math.random()*0.6;
                color = fuseColors[Math.floor(Math.random() * fuseColors.length)];
                type = type2;
                pCount = 0;
              }
              fuseArray.push(new Fuse(type, this.x, this.y, radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirX), radiusFactor*(Math.round(Math.random())*2 - 1)*Math.sqrt(dirY), size, color, pCount, lifeSpan, 1));
            }
            break;
          default: //impossible to reach
        }
      }
      // if this is a fuse
      else if (this.type < 20){
        // even type will die with flickering sparks
        // odd type will either die doing nothing
        // or randomly change direction if type is = 0%3
        color = this.color;
        type =  this.type + 10;
        pCount = (type%2 == 0) ? 1 : 0 ;
        size = (type%2 == 0 || type%3 == 0) ? 0 : this.size*0.7 ;
        lifeSpan = 40 + Math.random()*10;
        dirX = (type%2 == 0) ? this.dirX : Math.random()*16 - 8;
        dirY = (type%2 == 0) ? this.dirY : Math.random()*16 - 8;
        fuseArray.push(new Fuse(type, this.x, this.y, dirX, dirY, size, color, pCount, lifeSpan,0));
      }
    }
  }

  // update
  update(){
    this.x += this.dirX;
    this.y += this.dirY;
    if(this.type > 9){
      this.dirX *= pSpeedDecrease;
      this.dirY *= pSpeedDecrease;
    }
    this.dirX += gravityX;
    this.dirY += gravityY;
    this.lifeSpan -= 1;
    this.draw();
  }

  draw(){
    if(this.size >= 1){
      // thats a fuse
      if(this.type < 10){
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI*2, false);
        ctx.fillStyle = this.color;
        ctx.fill();

        // if the fuse explodes, drawing a light for one frame
        if(this.lifeSpan == 0){
          bcCtx.beginPath();
          bcCtx.arc(this.x, this.y, 20 + Math.random()*pSizeVariation, 0, Math.PI*2, false);
          bcCtx.fillStyle = brightSpark;
          bcCtx.fill();
        }
      }
      else{
        // drawing fuse heart
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size/2, 0, Math.PI*2, false);
        ctx.fillStyle = brightSpark;
        ctx.fill();

        // drawing fuse glow
        bcCtx.beginPath();
        bcCtx.arc(this.x, this.y, this.size + Math.random()*pSizeVariation, 0, Math.PI*2, false);
        bcCtx.fillStyle = this.color;
        bcCtx.fill();
      }
    }
  }
}

// launching a fuse, direction and duration are defined here
function launchFuse(type){
  // launching a rocket that will explode later
  if(type < 10){
    color = "#ff9900";
    pCount = 0.3;
    size = 1;
    children = 140;
    speedX = Math.random()*launchXspeed - launchXspeed/2;
    speedY = -launchYspeed - Math.random()*launchYspeed/5;
    lifeSpan = 160;
  }
  // launching a fuse
  else if(type < 20){
    color = fuseColors[Math.floor(Math.random() * fuseColors.length)];
    pCount = (type < 15) ? 0 : 1 ;
    size = 5;
    children = 1;
    speedX = Math.random()*launchXspeed*6 - launchXspeed*3;
    speedY = -launchYspeed*2 - Math.random()*launchYspeed*1.5;
    lifeSpan = 120;
  }
  fuseArray.push(new Fuse(type, renderCanvas.width/2, renderCanvas.height, speedX, speedY, size, color, pCount, lifeSpan, children));
}

// remove dead fuses
function removeFuses(){
  newFuseArray = [];
  for(let i = 0; i < fuseArray.length; i++){
    // keeping only fuses that didnt reach a lifeSpan of 0, making the others die
    if(fuseArray[i].lifeSpan > 0){
      newFuseArray.push(fuseArray[i]);
    }
    else{
      fuseArray[i].die();
    }
  }
  fuseArray = newFuseArray;
}


// particles
class Particle{
  constructor(x, y, dirX, dirY, size, color, type){
    this.x = x;
    this.y = y;
    this.dirX = dirX;
    this.dirY = dirY;
    this.size = size;
    this.color = color;
    this.type = type;
  }
  // method to draw each particle
  draw(){
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI*2, false);
    ctx.fillStyle = this.color;
    ctx.fill();
    // for trail sparks we draw a small glow
    if(this.type == 1){
      bcCtx.beginPath();
      bcCtx.arc(this.x, this.y, this.size*1.5, 0, Math.PI*2, false);
      bcCtx.fillStyle = this.color;
      bcCtx.fill();
    }
    // for flickering sparks we draw a slighly bigger glow
    else if(this.type == 2){
      bcCtx.beginPath();
      bcCtx.arc(this.x, this.y, this.size*3, 0, Math.PI*2, false);
      bcCtx.fillStyle = this.color;
      bcCtx.fill();
    }
  }
  // method to change position of particle
  update(){
    this.x += this.dirX;
    this.y += this.dirY;
    this.dirX += gravityX/4;
    this.dirY += gravityY/4;
    this.size *= pSizeDecrease;
    // draw particle
    this.draw();
  }
}


// create new particles out of fuses
function createParticles(){
  for(let i = 0; i < fuseArray.length; i++){
    // using random to create particles depending on pCount
    if(Math.random() < fuseArray[i].pCount){
      // for fuses that didnt explode yet
      if(fuseArray[i].type < 10){
        x = fuseArray[i].x;
        y = fuseArray[i].y;
        vX = Math.random()/3 - 0.33;
        vY = Math.random()/3;
        size = 1 + Math.random()/2;
        color = darkSpark;
        type = 0;
      }
      // for fuse that have a trail of sparks
      else if(fuseArray[i].type > 14 && fuseArray[i].type < 20){
        x = fuseArray[i].x;
        y = fuseArray[i].y;
        vX = Math.random()/5 - 0.1;
        vY = Math.random()/5;
        size = 1 + Math.random()/3;
        color = brightSpark;
        type = 1;
      }
      // for fuses that have flickering sparks around them
      else if(fuseArray[i].type > 19 && fuseArray[i].type%2 == 0){
        x = fuseArray[i].x + Math.random()*30 -15;
        y = fuseArray[i].y + Math.random()*30 -15;
        vX = Math.random()/5 - 0.1;
        vY = Math.random()/5 - 0.1;
        size = 0.8;
        color = brightSpark;
        type = 2;
      }
      particlesArray.push(new Particle(x, y, vX, vY, size, color, type));
    }
  }
}


// delete particles outside the canvas or too small
function deleteParticles(){
  var newPArray = [];
  for(let i = 0; i < particlesArray.length; i++){
    if(particlesArray[i].x > 0 && particlesArray[i].y > 0 && particlesArray[i].x < renderCanvas.width && particlesArray[i].y < renderCanvas.height && particlesArray[i].size > 0.6 ){
      newPArray.push(particlesArray[i]);
    }
  }
  particlesArray = newPArray;
}



// animation
function animate(){
  requestAnimationFrame(animate);
  ctx.clearRect(0,0,innerWidth, innerHeight);
  bcCtx.clearRect(0,0,innerWidth, innerHeight);
  for(let i = 0; i < fuseArray.length; i++){
    fuseArray[i].update();
  }
  for(let j = 0; j < particlesArray.length; j++){
    particlesArray[j].update();
  }
}


// create interval timer for particles and fuses creation/update/removal
function launchInterval(){
  clearInterval(intervalTimer);
  intervalTimer = setInterval(function(){
    // if fountain is active, launch a fuse
    if(foutain){launchFuse(10 + Math.floor(Math.random()*10));}
    removeFuses();
    createParticles();
    deleteParticles();
  }, pCreationInterval);
}

animate();
launchInterval();
