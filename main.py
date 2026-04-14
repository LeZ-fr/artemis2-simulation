from ursina import *

app = Ursina()

camera.orthographic = True
camera.fov = 10
camera.position = (1, 1)
window.color = color.black
Text.default_resolution *= 2
paused = False

# add the earth
earth = Entity(
    model='sphere',
    texture='./earth.jpg',
    scale=2
)


# add the moon
moon = Entity(
    model='sphere',
    texture='./moon.jpg',
    scale=0.5
)

# display the earth at the middle of the screen
earth.position = (1,1)

# display the moon at the right of the earth
moon.position = (5,1)

# add camera controls
camera = EditorCamera()

def set_pause(value):
    global paused
    paused = value
    application.time_scale = 0 if value else 1

# pause the simulation when space is pressed (automatically called if a key is pressed)
def input(key):
    if key == 'space':
        set_pause(not paused)

# update loop automatically called by Ursina
def update():
    # check if the simulation is paused
    if paused:
        return 

    # rotate the moon by 50 degrees after each frame (time.dt is the time between the current frame and the previous one)
    moon_rotation_speed = 2.0
    moon.rotation_y += moon_rotation_speed * time.dt

    # rotate the earth by 50 degrees after each frame
    earth_rotation_speed = moon_rotation_speed * 97.0 # the earth rotates on itseld 97 times faster than the moon
    earth.rotation_y += earth_rotation_speed * time.dt

    # move the moon around the earth
    moon_orbit_speed = 0.1
    moon_orbit_radius = 4.0
    moon.position = (
        earth.position[0] + moon_orbit_radius * cos(time.time() * moon_orbit_speed),
        earth.position[1] + moon_orbit_radius * sin(time.time() * moon_orbit_speed)
    )
    
       
app.run()

