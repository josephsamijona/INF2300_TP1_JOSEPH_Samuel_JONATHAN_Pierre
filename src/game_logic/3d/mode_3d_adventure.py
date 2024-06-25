import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GLU import gluPerspective, gluLookAt
import numpy as np
import ctypes

# Vertex Shader
vertex_shader = """
#version 330
in vec3 position;
in vec3 normal;
in vec2 texcoords;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
out vec3 fragNormal;
out vec2 fragTexcoords;
void main() {
    fragNormal = normal;
    fragTexcoords = texcoords;
    gl_Position = projection * view * model * vec4(position, 1.0);
}
"""

# Fragment Shader
fragment_shader = """
#version 330
in vec3 fragNormal;
in vec2 fragTexcoords;
uniform sampler2D texture1;
uniform vec3 lightDirection;
out vec4 outColor;
void main() {
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * vec3(1.0, 1.0, 1.0);
    
    vec3 norm = normalize(fragNormal);
    float diff = max(dot(norm, -lightDirection), 0.0);
    vec3 diffuse = diff * vec3(1.0, 1.0, 1.0);
    
    vec3 result = (ambient + diffuse) * texture(texture1, fragTexcoords).rgb;
    outColor = vec4(result, 1.0);
}
"""

def create_shader_program():
    program = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )
    return program

def generate_terrain(size, scale, height_scale):
    vertices = []
    normals = []
    texcoords = []
    for i in range(size):
        for j in range(size):
            x = (i - size // 2) * scale
            y = (j - size // 2) * scale
            z = (np.sin(i * 0.1) + np.sin(j * 0.1)) * height_scale
            vertices.append([x, y, z])
            normals.append([0.0, 0.0, 1.0])
            texcoords.append([i / size, j / size])
    vertices = np.array(vertices, dtype=np.float32)
    normals = np.array(normals, dtype=np.float32)
    texcoords = np.array(texcoords, dtype=np.float32)

    indices = []
    for i in range(size - 1):
        for j in range(size - 1):
            indices.append(i * size + j)
            indices.append((i + 1) * size + j)
            indices.append((i + 1) * size + (j + 1))
            indices.append(i * size + j)
            indices.append((i + 1) * size + (j + 1))
            indices.append(i * size + (j + 1))
    indices = np.array(indices, dtype=np.uint32)

    return vertices, normals, texcoords, indices

def load_texture(texture_path):
    texture = pygame.image.load(texture_path)
    texture_data = pygame.image.tostring(texture, "RGB", True)
    width, height = texture.get_size()

    glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

def init():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

def main():
    init()
    shader = create_shader_program()

    vertices, normals, texcoords, indices = generate_terrain(50, 0.2, 1.0)

    VBO = glGenBuffers(3)
    glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
    glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
    
    glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
    glBufferData(GL_ARRAY_BUFFER, texcoords.nbytes, texcoords, GL_STATIC_DRAW)
    
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    
    load_texture("texture.jpg")

    glUseProgram(shader)
    glUniform1i(glGetUniformLocation(shader, "texture1"), 0)

    projection = glGetUniformLocation(shader, "projection")
    view = glGetUniformLocation(shader, "view")
    model = glGetUniformLocation(shader, "model")
    lightDirection = glGetUniformLocation(shader, "lightDirection")

    glUniform3f(lightDirection, 0.0, 0.0, -1.0)

    clock = pygame.time.Clock()
    angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        angle += 1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        projection_matrix = gluPerspective(45, 800 / 600, 0.1, 50.0)
        view_matrix = gluLookAt(0, -5, -10, 0, 0, 0, 0, 1, 0)
        model_matrix = np.identity(4, dtype=np.float32)
        model_matrix = np.dot(model_matrix, [
            [np.cos(np.radians(angle)), 0, np.sin(np.radians(angle)), 0],
            [0, 1, 0, 0],
            [-np.sin(np.radians(angle)), 0, np.cos(np.radians(angle)), 0],
            [0, 0, 0, 1]
        ])

        glUniformMatrix4fv(projection, 1, GL_FALSE, projection_matrix)
        glUniformMatrix4fv(view, 1, GL_FALSE, view_matrix)
        glUniformMatrix4fv(model, 1, GL_FALSE, model_matrix)

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

        glEnableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, ctypes.c_void_p(0))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
