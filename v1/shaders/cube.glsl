#version 330

#if defined VERTEX_SHADER

// Model geometry
in vec3 in_position;
in vec3 in_normal;

// Per instance data
in vec3 in_offset;
//in vec3 in_color;

uniform mat4 m_model;
uniform mat4 m_camera;
uniform mat4 m_proj;
uniform float time;

out vec3 pos;
out vec3 normal;
out vec3 color;

void main() {
    mat4 m_view = m_camera * m_model;
    vec4 p = m_view * vec4(in_position + in_offset, 1.0);
    gl_Position =  m_proj * p;
    mat3 m_normal = mat3(m_view);
    normal = m_normal * normalize(in_normal);
    pos = p.xyz;
    color = vec3(0.5)+0.25*cos(time);
//    color = vec3(cos(log(in_offset)/2 + vec3(time)));
//    color = vec3(0.5+pow(in_offset.x, cos(time)),0.5-pow(log(cos(time)), in_offset.y),0.5*cos(time));
//    color = vec3(cos(time), cos(-time), tan(time));
//    color = in_color;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;

in vec3 pos;
in vec3 normal;
in vec3 color;

void main() {
    float l = dot(normalize(-pos), normalize(normal));
    fragColor = vec4(color*l, 1.0);
}
#endif
