beacons = { }
users = { }
zone_radius = [ 60, 100, 150 ];
zone_color = [ 'red', 'blue', 'green']
canvas_size = { x:1, y:1 }
basis_size = { x:600,y:492 }

function create_zone_div(zone_index, x, y, scaleX, scaleY){

    draw_x = x-zone_radius[zone_index];
    draw_y = y-zone_radius[zone_index];

    var new_beacon_div = document.createElement('div');
    new_beacon_div.style.position = 'absolute';
    new_beacon_div.style.left = (draw_x * scaleX) + 'px';
    new_beacon_div.style.top = (draw_y * scaleY) + 'px';

    new_beacon_div.style.width = ((zone_radius[zone_index] * 2) * scaleX) + 'px';
    new_beacon_div.style.height = ((zone_radius[zone_index] * 2) * scaleY) + 'px';

    if(zone_index > 0)
        new_beacon_div.style.border = (zone_radius[zone_index] - zone_radius[zone_index-1]) * scaleX+'px solid '+zone_color[zone_index];
    else
        new_beacon_div.style.background = zone_color[zone_index];
    new_beacon_div.style.zIndex = 4;
    new_beacon_div.style.opacity = 0.33;
    new_beacon_div.style.borderRadius ='50%';

    return new_beacon_div;
}

function create_zone_text_div(zone_index, user_names, x, y, scaleX, scaleY){

    var draw_x = x-zone_radius[zone_index] + 20;
    var draw_y = y//-zone_radius[zone_index];

    var new_beacon_div = document.createElement('div');
    new_beacon_div.style.position = 'absolute';
    new_beacon_div.style.left = (draw_x * scaleX) + 'px';
    new_beacon_div.style.top = (draw_y * scaleY) + 'px';

    new_beacon_div.style.width = ((zone_radius[zone_index] * 2) * scaleX) + 'px';
    new_beacon_div.style.height = ((zone_radius[zone_index] * 2) * scaleY) + 'px';

    new_beacon_div.style.zIndex = 5
    new_beacon_div.style.borderRadius ='50%';

    new_beacon_div.innerHTML = user_names.length;
    new_beacon_div.style.fontWeight = 'bold';
    new_beacon_div.style.color =  'white';
    new_beacon_div.style.textShadow = '-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000';

    return new_beacon_div;
}

function create_zone_beacon_div(zone_index, baecon_id, x, y, scaleX, scaleY){
    var beacon_size = 20;

    draw_x = x - beacon_size;
    draw_y = y - beacon_size;

    var new_beacon_div = document.createElement('div');
    new_beacon_div.style.position = 'absolute';
    new_beacon_div.style.left = (draw_x * scaleX) + 'px';
    new_beacon_div.style.top = (draw_y * scaleY) + 'px';

    new_beacon_div.style.width = ((beacon_size * 2) * scaleX) + 'px';
    new_beacon_div.style.height = ((beacon_size * 2) * scaleY) + 'px';

    new_beacon_div.style.zIndex = 5;
    new_beacon_div.style.borderRadius ='50%';
    new_beacon_div.style.textAlign = 'center';
    new_beacon_div.style.verticalAlign = 'middle';
    new_beacon_div.style.background = 'blue';

    new_beacon_div.innerHTML = 'B ' + baecon_id;
    new_beacon_div.style.fontWeight = 'blue';
    new_beacon_div.style.color =  'white';
    new_beacon_div.style.textShadow = '-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000';

    return new_beacon_div;
}

function create_user_div(zone_index, user_name, order, x, y, scaleX, scaleY){

    var user_radius = 200;
    var zone_distance = zone_radius[zone_index];

    draw_x = x - Math.cos(3.14 * 2 * (order / 20)) * zone_distance;
    draw_y = y - Math.sin(3.14 * 2 * (order / 20)) * zone_distance;

    var new_beacon_div = document.createElement('div');
    new_beacon_div.style.position = 'absolute';
    new_beacon_div.style.left = (draw_x * scaleX) + 'px';
    new_beacon_div.style.top = (draw_y * scaleY) + 'px';

    new_beacon_div.style.width = ((user_radius * 2) * scaleX) + 'px';
    new_beacon_div.style.height = ((user_radius * 2) * scaleY) + 'px';

    new_beacon_div.style.zIndex = 6

    new_beacon_div.innerHTML = '['+user_name+']';
    new_beacon_div.style.color =  'black';
    new_beacon_div.style.textShadow = '-1px -1px 0 #FFF, 1px -1px 0 #FFF, -1px 1px 0 #FFF, 1px 1px 0 #FFF';

    return new_beacon_div;
}