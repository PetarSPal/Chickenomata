#version 330

#if defined VERTEX_SHADER

uniform mat4 Mvp;

in vec3 in_vert;

void main() {
    gl_Position = Mvp
    * vec4(in_vert, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 f_color;
void main() {
    f_color = vec4(0.1, 0.1, 0.1, 1.0);
}
#endif
