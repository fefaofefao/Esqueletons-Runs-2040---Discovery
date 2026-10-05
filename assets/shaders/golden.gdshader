// Variante Golden: paleta dourada por luminância + brilho que percorre o sprite
// a cada 2 s. Vale para qualquer espécie e estágio (não há sprites dourados).
shader_type canvas_item;

// Tempo controlado pelo script (respeita o 2x do jogo).
uniform float t = 0.0;
// Região do quadro dentro da textura, em UV (x, y, largura, altura).
uniform vec4 region = vec4(0.0, 0.0, 1.0, 1.0);

void fragment() {
	vec4 c = texture(TEXTURE, UV);
	float l = dot(c.rgb, vec3(0.299, 0.587, 0.114));
	vec3 dark = vec3(0.42, 0.23, 0.06);
	vec3 mid = vec3(0.96, 0.70, 0.18);
	vec3 light = vec3(1.0, 0.97, 0.72);
	vec3 g = l < 0.5 ? mix(dark, mid, l * 2.0) : mix(mid, light, (l - 0.5) * 2.0);
	// contornos escuros continuam escuros
	g = mix(c.rgb, g, smoothstep(0.12, 0.22, l));
	vec2 local = (UV - region.xy) / max(region.zw, vec2(0.0001));
	float pos = fract(t / 2.0) * 2.4 - 0.6;
	float band = 1.0 - smoothstep(0.0, 0.10, abs(local.x + local.y * 0.5 - pos));
	g += vec3(band * 0.55);
	COLOR = vec4(g, c.a);
}
