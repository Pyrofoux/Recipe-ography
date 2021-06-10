// UI Settings

let settings = {};
settings.cellSize = 6;

// WATER = 1
// GRASSLAND = 2
// DESERT = 3
// JUNGLE = 4
// MOUNTAIN = 5
// SNOW = 6

let tyle2color =
[
  "black", //NOT USED
  "#03358C", // WATER
  "#099c06", //GRASSLAND
  "#ffe563",  //DESERT
  "#084d4d",  //JUNGLE
  "brown",  //MOUNTAIN
  "#d4faf8",  //SNOW
];



let cvs = get("cvs");
let ctx = cvs.getContext("2d");
let terrain_map = world_data.terrain_map[world_data.terrain_map.length-1];

function for_map(matrix, callback)
{
  for(let y = 0; y < world_data.terrain_height; y++)
  {
    for(let x = 0; x < world_data.terrain_width; x++)
    {
      callback(matrix[y][x],x,y)
    }
  }
}


function init()
{

  cvs.width = settings.cellSize*world_data.terrain_width;
  cvs.height = settings.cellSize*world_data.terrain_height;
  for_map(terrain_map, function(value, x, y){

    colorSquare(x,y, tyle2color[value])

  })
}


function colorSquare(x,y,color,a)
{
  if(!a)a=1;

  ctx.globalAlpha = a;
  ctx.fillStyle = color;
  ctx.fillRect(x*settings.cellSize,y*settings.cellSize,settings.cellSize, settings.cellSize);
}


init()
