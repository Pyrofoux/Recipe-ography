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
  "#734f30",  //MOUNTAIN
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

  drawMap(); //
  clearCountryInfo();

}


function drawMap(mouseCoords)
{

  //Terrain
  ctx.clearRect(0,0,cvs.width, cvs.height);
  for_map(terrain_map, function(tile_id, x, y){

    colorSquare(x,y, tyle2color[tile_id])
  });


  // Country highlighting
  for_map(culture_map, function(culture_id, x, y){

    if(culture_id > 0)
    {
      if(ui.culture_hover == culture_id || ui.culture_click == culture_id)
      {
        //colorSquare(x,y, "#7FFFD4",settings["culture_color_transparency_hover"])
        colorSquare(x,y, culture_colors[culture_id%culture_colors.length],settings["culture_color_transparency_hover"])
      }
      else
      {
        colorSquare(x,y, culture_colors[culture_id%culture_colors.length],settings["culture_color_transparency"])
      }

    }

  });


  if(ui.culture_hover || ui.culture_click)
  {
    binocular_img = get("binoculars_surprised");
  }
  else
  {
      binocular_img = get("binoculars");
  }

  if(mouseCoords)
  {
    ctx.drawImage(binocular_img, mouseCoords.x-binocular_img.width/2, mouseCoords.y-binocular_img.height/2);
  }


  // Before we had the binocular images
  /*
  if(ui.culture_hover)
  {
    cvs.style.cursor = "pointer";
  }
  else
  {
    cvs.style.cursor = "default";
  }*/

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
  let targetCulture = getCultureFromCoord(coords);
  if(ui.culture_click == targetCulture)
  {
    ui.culture_click = 0;
  }
  else
  {
    ui.culture_click = targetCulture;
  }
  let mouseCoords = {x:e.offsetX,y:e.offsetY};
  drawMap(mouseCoords);
}

function mapHover(e)
{
  let coords= getCoords(e, settings.cellSize);
  ui.culture_hover = getCultureFromCoord(coords);

  if(ui.culture_hover!= 0)
  {
    displayCountryInfo(ui.culture_hover-1);
  }
  else if(ui.culture_click!= 0)
  {
    displayCountryInfo(ui.culture_click-1);
  }
  else
  {
    clearCountryInfo();
  }

  let mouseCoords = {x:e.offsetX,y:e.offsetY};
  drawMap(mouseCoords);


}


function displayCountryInfo(cultureId)
{
  get("sidebar_content").style.display = "inline-block";
  get("startup_instructions").style.display = "none";

  recipe = world_data.recipes[cultureId];

  // Recipe Title
  get("country_name").innerHTML = capitalize(world_data["culture_names"][cultureId]);
  get("biome_name").innerHTML = capitalize(recipe.commonTileTypes[0]);
  get("dish_type").innerHTML = capitalize(recipe["recipe category"]);


  //Ingredients

  get("ingredients_list").innerHTML = recipe.ingredients.map(ingredient => "<li>"+add_tooltip(ingredient)+"</li>").join("");

  //Steps
  recipe_steps = recipe["recipe steps"];
  get("steps_list").innerHTML = recipe_steps.map(step => "<li>"+step+"</li>").join("");

  //Other info
  get("prep_time").innerHTML = recipe["prep time"];
  get("cook_time").innerHTML = recipe["cook time"];



}

function clearCountryInfo()
{
  get("sidebar_content").style.display = "none";
  get("startup_instructions").style.display = "inline-block";
}

function add_tooltip(sentence)
{
  words = sentence.split(" ");
  for(let i=0; i < sentence.length; i++)
  {
    entry = world_data.plantDictionary[words[i]];
    if(entry)
    {
      biome = entry[0];
      edibles = entry[1];
      parents = entry[2];
      words[i] = gen_tooltip(words[i], biome, edibles, parents);
    }
  }

  return words.join(" ");
}

function gen_tooltip(name, biome, edibles, parents)
{
  firstHalf = splitHalf(parents[0])[0];
  secondHalf = splitHalf(parents[1])[1];
  return `<span class="tooltip">${name}<span class="tooltiptext">From <i>${firstHalf}-</i> (${parents[0]}) and <i>-${secondHalf}</i> (${parents[1]}). Grows in the ${biome}.</span></span>`
}

function splitHalf(word)
{
  l = word.length;
  return [word.substr(0,Math.floor(l/2)), word.substr(Math.floor(l/2))];
}

function capitalize(string)
{
  return string[0].toUpperCase()+string.substr(1);
}

init();
