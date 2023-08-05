#pragma once

#include "Python.hpp"

#include "ContextMember.hpp"

#include "TextureFilter.hpp"

struct MGLTexture3D : public MGLContextMember {
	int texture_obj;

	int width;
	int height;
	int depth;

	int components;

	int samples;

	bool floats;

	MGLTextureFilter * filter;

	bool repeat_x;
	bool repeat_y;
	bool repeat_z;
};

extern PyTypeObject MGLTexture3D_Type;

MGLTexture3D * MGLTexture3D_New();
void MGLTexture3D_Invalidate(MGLTexture3D * texture);
