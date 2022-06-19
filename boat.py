import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import texture_loader
from OBJLoader import ObjFileLoader
import os

def getFileContents(filename):
    p = os.path.join(os.getcwd(), "shader", filename)
    return open(p, 'r').read()
VertexShaderContent = getFileContents("vertex.shader")
FragmentShaderContent = getFileContents("fragment.shader")
    
def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

if not glfw.init():
    raise Exception("glfw can not be initialized!")

window = glfw.create_window(800, 600, "My OpenGL window", None, None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")


glfw.set_window_pos(window, 2, 2)

glfw.set_window_size_callback(window, window_resize)

glfw.make_context_current(window)


boat_indices, boat_buffer = ObjFileLoader.model_loader("last1.obj")
water_indices, water_buffer = ObjFileLoader.model_loader("water1.obj")

shader = compileProgram(compileShader(VertexShaderContent, GL_VERTEX_SHADER), compileShader(FragmentShaderContent, GL_FRAGMENT_SHADER))


VAO = glGenVertexArrays(2)
VBO = glGenBuffers(2)
glBindVertexArray(VAO[0])

glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, boat_buffer.nbytes, boat_buffer, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, boat_buffer.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, boat_buffer.itemsize * 8, ctypes.c_void_p(127152))

glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, boat_buffer.itemsize * 8, ctypes.c_void_p(127152))
glEnableVertexAttribArray(2)

glBindVertexArray(VAO[1])

glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, water_buffer.nbytes, water_buffer, GL_STATIC_DRAW)


glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, water_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, water_buffer.itemsize * 8, ctypes.c_void_p(127152))

glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, water_buffer.itemsize * 8, ctypes.c_void_p(127152))
glEnableVertexAttribArray(2)
textures = glGenTextures(2)
texture_loader("wood.jpg", textures[0])
texture_loader("ocean.jpg", textures[1])

glUseProgram(shader)
glClearColor(0, 0, 0, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
water_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -5, -10]))
boat_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-4, 0, 0]))

view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)



def move_x(obj,speed):
    obj = pyrr.matrix44.create_from_translation(pyrr.Vector3([speed * glfw.get_time(),0, 0]))
    return obj

def move_z(obj,speed):
    obj = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,speed * glfw.get_time(),0]))
    return obj

def move_y(obj,speed):
    obj = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,0,speed * glfw.get_time()]))
    return obj
    

while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_y = pyrr.Matrix44.from_y_rotation(20)
    model = pyrr.matrix44.multiply(rot_y, water_pos)

    
    boat_pos = move_x(boat_pos,1)
    print(boat_pos)

    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(boat_indices))

    rot_y = pyrr.Matrix44.from_y_rotation(90)
    model = pyrr.matrix44.multiply(rot_y, boat_pos)
    
    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(water_indices))
 
  

    glfw.swap_buffers(window)

glfw.terminate()

