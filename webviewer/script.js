// UI Settings

let settings = {};
settings.cellSize = 6;
settings.culture_color_transparency = 0;
settings.culture_color_transparency_hover = 0.9;

// settings.culture_color_transparency = 0.80;
// settings.culture_color_transparency_hover = 0.20;

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


let culture_colors = shuffle(CSS_COLOR_NAMES);

culture_colors = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f"].concat(culture_colors);



////////////////////////////////////////////////////////////

let cvs = get("cvs");
let ctx = cvs.getContext("2d");
let terrain_map = world_data.terrain_map;
let culture_map = world_data.culture_map;

let ui = {};
ui.culture_hover = false;
ui.culture_click = false;

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
  cvs.addEventListener('click', mapClick);
  cvs.addEventListener('mousemove', mapHover);

  drawMap();

}


function drawMap()
{
  ctx.clearRect(0,0,cvs.width, cvs.height);
  for_map(terrain_map, function(tile_id, x, y){

    colorSquare(x,y, tyle2color[tile_id])
  })

  for_map(culture_map, function(culture_id, x, y){

    if(culture_id > 0)
    {
      if(ui.culture_hover == culture_id)
      {
        //colorSquare(x,y, "#7FFFD4",settings["culture_color_transparency_hover"])
        colorSquare(x,y, culture_colors[culture_id],settings["culture_color_transparency_hover"])
      }
      else
      {
        colorSquare(x,y, culture_colors[culture_id],settings["culture_color_transparency"])
      }

    }

  })


  if(ui.culture_hover)
  {
    cvs.style.cursor = "pointer";
  }
  else
  {
    cvs.style.cursor = "default";
  }

}

function colorSquare(x,y,color,a)
{
  if(a == "undefined")a=1;

  ctx.globalAlpha = a;
  ctx.fillStyle = color;
  ctx.fillRect(x*settings.cellSize,y*settings.cellSize,settings.cellSize, settings.cellSize);
  ctx.globalAlpha = 1;
}


function getCoords(e, boxSize)
{
    return{
      x:Math.floor(e.offsetX / boxSize),
      y:Math.floor(e.offsetY / boxSize)
      }
}

function getCultureFromCoord(coords)
{
  if(coords.y < 0 || coords.x < 0) return false;

  if(culture_map[coords.y][coords.x] > 0)
  {
    return culture_map[coords.y][coords.x];
  }
  else
  {
    return false;
  }
}


function mapClick(e)
{
  let coords= getCoords(e, settings.cellSize);
  ui.culture_click = getCultureFromCoord(coords);
  drawMap();
}

function mapHover(e)
{
  let coords= getCoords(e, settings.cellSize);
  ui.culture_hover = getCultureFromCoord(coords);
  drawMap();

  if(ui.culture_hover!= 0)
  {
    get("country_name").innerHTML = world_data["culture_names"][ui.culture_hover-1]
  }
  else
  {
    get("country_name").innerHTML = "";
  }


}


init();
