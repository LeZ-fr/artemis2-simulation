from ursina import *
from datetime import datetime, timedelta

app = Ursina()

# camera and screen settings
window.color = color.black
Text.default_resolution *= 2
paused = True # we start the simulation paused, the user can unpause it by pressing space
camera = EditorCamera()
camera.orthographic = True
camera.fov = 10
camera.position = (1, 1, -60)

# mission settings
mission_start = datetime(2026, 4, 2, 0, 35, 0)
simulation_time = 0  # seconds since launch
time_scale_sim = 10   # 1 sec real = 10 sec sim

# add the earth
earth = Entity(
    model='sphere',
    texture='./earth.jpg',
    scale=1.5
)
# define the rotation factor according to the real rotation of the earth and the moon (the earth rotates on itself 97 times faster than the moon)
earth_rotation_factor = 97.0

# add the moon
moon = Entity(
    model='sphere',
    texture='./moon.jpg',
    scale=0.7
)
moon_orbit_speed = 0.01
moon_orbit_radius = 15.0
moon_rotation_speed = 0.5

# make the moon look at the earth
moon.look_at(earth)

# add the rocket
rocket_speed = 0.2
rocket_orbit_radius = 2.0

rocket = Entity(
    model='sphere',
    color=color.white,
    scale=0.3
)

# add the rocket trail
trail_points = []

trail = Entity(
    model=Mesh( # we create a custom mesh for the trail with the point we define in the traikl_points list
        vertices=trail_points,
        mode='line',
        thickness=1.0
    ),
    color=color.white
)

# display the earth at the middle of the screen
earth.position = (1,1)

# display the moon 
moon.position = (
    earth.position[0] + moon_orbit_radius * cos(simulation_time * moon_orbit_speed),
    earth.position[1] + moon_orbit_radius * sin(simulation_time * moon_orbit_speed)
)

# make the rocket start at the left of the earth
rocket.position = (
    earth.x - earth.scale_x / 2, # we start the rocket at the left of the earth by taking the x position of the earth and subtracting half of its scale (its radius) to it
    earth.y,
    earth.z
)

# add a text in the top left corner to display informations
info_text = Text(
    text='',
    position=(
        -window.aspect_ratio / 2 + 0.2,
        0.40
    ),
    origin=(0,0),
    scale=1.2,
    color=color.white
)

# set the content of the text
info_text.text = (
        f'Date : {mission_start.strftime("%d/%m/%Y")}\n'
        f'Hours : {mission_start.strftime("%H:%M:%S")}\n'
        f'Earth distance : 0.00\n'
        f'Rocket speed : 0.00'
)

# function to pause and unpause the simulation
def set_pause(value):
    global paused
    paused = value
    application.time_scale = 0 if value else 1

# pause the simulation when space is pressed (automatically called if a key is pressed)
def input(key):
    if key == 'space':
        set_pause(not paused)

# function to update the text on the top left with the current date, time, distance to earth and rocket speed
def update_info_text():
    global simulation_time

    # we compute the current date and time of the simulation by adding the simulation time to the mission start time
    # timedelta is a function from the datetime module that allows us to add a certain amount of time to a datetime object (in this case, we add the simulation time in seconds to the mission start time)
    sim_datetime = mission_start + timedelta(seconds=simulation_time) 

    # we compute the distance between the rocket and the earth using the distance function from Ursina
    distance_to_earth = distance(rocket.position, earth.position)

    info_text.text = (
        f"Date : {sim_datetime.strftime('%d/%m/%Y')}\n" # we display only the day, month and year of the simulation date
        f"Hours : {sim_datetime.strftime('%H:%M:%S')}\n" # we display only the hours, minutes and seconds of the simulation date
        f"Earth distance : {distance_to_earth:.2f}\n"
        f"Rocket speed : {rocket_speed:.2f}"
    )

# update loop automatically called by Ursina
def update():

    # check if the simulation is paused
    if paused:
        return 

    global simulation_time
    simulation_time += time.dt * 10.0 # we multiply the time by 10 to make the simulation faster (1 second in real life is 10 seconds in the simulation)


    # rotate the earth by 50 degrees after each frame (time.dt is the time between the current frame and the previous one)
    global moon_rotation_speed, earth_rotation_factor
    earth_rotation_speed = moon_rotation_speed * earth_rotation_factor # the earth rotates on itself 97 times faster than the moon
    earth.rotation_y += earth_rotation_speed * time.dt

    # move the moon around the earth
    global moon_orbit_speed, moon_orbit_radius
    moon.position = (
        earth.position[0] + moon_orbit_radius * cos(simulation_time * moon_orbit_speed),
        earth.position[1] + moon_orbit_radius * sin(simulation_time * moon_orbit_speed)
    )

    """
    # move the rocket around the earth
    global rocket_speed, rocket_orbit_radius
    rocket.position = (
        earth.position[0] + rocket_orbit_radius * cos(simulation_time * rocket_speed),
        earth.position[1] + rocket_orbit_radius * sin(simulation_time * rocket_speed)
    )
    """
    
    # add the current position of the rocket to the trail points
    trail_points.append(rocket.position)

    # if there is at least 2 points in the trail, update the trail model with the new points and generate the model to display it
    if len(trail_points) >= 2:
        trail.model.vertices = trail_points
        trail.model.generate()
    
    # update the text on the top left
    update_info_text()
    

app.run()
