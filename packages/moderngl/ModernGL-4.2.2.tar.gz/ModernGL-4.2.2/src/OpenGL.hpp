#pragma once

#if defined(_WIN32) || defined(_WIN64)
#define GLAPI __stdcall
#else
#define GLAPI
#endif

#if defined(__x86_64__) || defined(_WIN64)
	typedef long long int GLsizeiptr;
	typedef long long int GLintptr;
#else
	typedef int GLsizeiptr;
	typedef int GLintptr;
#endif

typedef char GLbyte;
typedef char GLchar;
typedef double GLclampd;
typedef double GLdouble;
typedef float GLclampf;
typedef float GLfloat;
typedef int GLint;
typedef int GLsizei;
typedef long long int GLint64;
typedef short GLshort;
typedef struct __GLsync * GLsync;
typedef unsigned char GLboolean;
typedef unsigned char GLubyte;
typedef unsigned int GLbitfield;
typedef unsigned int GLenum;
typedef unsigned int GLuint;
typedef unsigned long long int GLuint64;
typedef unsigned short GLhalf;
typedef unsigned short GLushort;
typedef void GLvoid;

typedef void (* GLDEBUGPROC) (GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar * message, const void * userParam);

typedef GLvoid (GLAPI * PROC_glCullFace)(GLenum mode);
typedef GLvoid (GLAPI * PROC_glFrontFace)(GLenum mode);
typedef GLvoid (GLAPI * PROC_glHint)(GLenum target, GLenum mode);
typedef GLvoid (GLAPI * PROC_glLineWidth)(GLfloat width);
typedef GLvoid (GLAPI * PROC_glPointSize)(GLfloat size);
typedef GLvoid (GLAPI * PROC_glPolygonMode)(GLenum face, GLenum mode);
typedef GLvoid (GLAPI * PROC_glScissor)(GLint x, GLint y, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glTexParameterf)(GLenum target, GLenum pname, GLfloat param);
typedef GLvoid (GLAPI * PROC_glTexParameterfv)(GLenum target, GLenum pname, const GLfloat * params);
typedef GLvoid (GLAPI * PROC_glTexParameteri)(GLenum target, GLenum pname, GLint param);
typedef GLvoid (GLAPI * PROC_glTexParameteriv)(GLenum target, GLenum pname, const GLint * params);
typedef GLvoid (GLAPI * PROC_glTexImage1D)(GLenum target, GLint level, GLint internalformat, GLsizei width, GLint border, GLenum format, GLenum type, const GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glTexImage2D)(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLint border, GLenum format, GLenum type, const GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glDrawBuffer)(GLenum buf);
typedef GLvoid (GLAPI * PROC_glClear)(GLbitfield mask);
typedef GLvoid (GLAPI * PROC_glClearColor)(GLfloat red, GLfloat green, GLfloat blue, GLfloat alpha);
typedef GLvoid (GLAPI * PROC_glClearStencil)(GLint s);
typedef GLvoid (GLAPI * PROC_glClearDepth)(GLdouble depth);
typedef GLvoid (GLAPI * PROC_glStencilMask)(GLuint mask);
typedef GLvoid (GLAPI * PROC_glColorMask)(GLboolean red, GLboolean green, GLboolean blue, GLboolean alpha);
typedef GLvoid (GLAPI * PROC_glDepthMask)(GLboolean flag);
typedef GLvoid (GLAPI * PROC_glDisable)(GLenum cap);
typedef GLvoid (GLAPI * PROC_glEnable)(GLenum cap);
typedef GLvoid (GLAPI * PROC_glFinish)();
typedef GLvoid (GLAPI * PROC_glFlush)();
typedef GLvoid (GLAPI * PROC_glBlendFunc)(GLenum sfactor, GLenum dfactor);
typedef GLvoid (GLAPI * PROC_glLogicOp)(GLenum opcode);
typedef GLvoid (GLAPI * PROC_glStencilFunc)(GLenum func, GLint ref, GLuint mask);
typedef GLvoid (GLAPI * PROC_glStencilOp)(GLenum fail, GLenum zfail, GLenum zpass);
typedef GLvoid (GLAPI * PROC_glDepthFunc)(GLenum func);
typedef GLvoid (GLAPI * PROC_glPixelStoref)(GLenum pname, GLfloat param);
typedef GLvoid (GLAPI * PROC_glPixelStorei)(GLenum pname, GLint param);
typedef GLvoid (GLAPI * PROC_glReadBuffer)(GLenum src);
typedef GLvoid (GLAPI * PROC_glReadPixels)(GLint x, GLint y, GLsizei width, GLsizei height, GLenum format, GLenum type, GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glGetBooleanv)(GLenum pname, GLboolean * data);
typedef GLvoid (GLAPI * PROC_glGetDoublev)(GLenum pname, GLdouble * data);
typedef GLenum (GLAPI * PROC_glGetError)();
typedef GLvoid (GLAPI * PROC_glGetFloatv)(GLenum pname, GLfloat * data);
typedef GLvoid (GLAPI * PROC_glGetIntegerv)(GLenum pname, GLint * data);
typedef const GLubyte * (GLAPI * PROC_glGetString)(GLenum name);
typedef GLvoid (GLAPI * PROC_glGetTexImage)(GLenum target, GLint level, GLenum format, GLenum type, GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glGetTexParameterfv)(GLenum target, GLenum pname, GLfloat * params);
typedef GLvoid (GLAPI * PROC_glGetTexParameteriv)(GLenum target, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetTexLevelParameterfv)(GLenum target, GLint level, GLenum pname, GLfloat * params);
typedef GLvoid (GLAPI * PROC_glGetTexLevelParameteriv)(GLenum target, GLint level, GLenum pname, GLint * params);
typedef GLboolean (GLAPI * PROC_glIsEnabled)(GLenum cap);
typedef GLvoid (GLAPI * PROC_glDepthRange)(GLdouble near, GLdouble far);
typedef GLvoid (GLAPI * PROC_glViewport)(GLint x, GLint y, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glDrawArrays)(GLenum mode, GLint first, GLsizei count);
typedef GLvoid (GLAPI * PROC_glDrawElements)(GLenum mode, GLsizei count, GLenum type, const GLvoid * indices);
typedef GLvoid (GLAPI * PROC_glGetPointerv)(GLenum pname, GLvoid ** params);
typedef GLvoid (GLAPI * PROC_glPolygonOffset)(GLfloat factor, GLfloat units);
typedef GLvoid (GLAPI * PROC_glCopyTexImage1D)(GLenum target, GLint level, GLenum internalformat, GLint x, GLint y, GLsizei width, GLint border);
typedef GLvoid (GLAPI * PROC_glCopyTexImage2D)(GLenum target, GLint level, GLenum internalformat, GLint x, GLint y, GLsizei width, GLsizei height, GLint border);
typedef GLvoid (GLAPI * PROC_glCopyTexSubImage1D)(GLenum target, GLint level, GLint xoffset, GLint x, GLint y, GLsizei width);
typedef GLvoid (GLAPI * PROC_glCopyTexSubImage2D)(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint x, GLint y, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glTexSubImage1D)(GLenum target, GLint level, GLint xoffset, GLsizei width, GLenum format, GLenum type, const GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glTexSubImage2D)(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format, GLenum type, const GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glBindTexture)(GLenum target, GLuint texture);
typedef GLvoid (GLAPI * PROC_glDeleteTextures)(GLsizei n, const GLuint * textures);
typedef GLvoid (GLAPI * PROC_glGenTextures)(GLsizei n, GLuint * textures);
typedef GLboolean (GLAPI * PROC_glIsTexture)(GLuint texture);
typedef GLvoid (GLAPI * PROC_glDrawRangeElements)(GLenum mode, GLuint start, GLuint end, GLsizei count, GLenum type, const GLvoid * indices);
typedef GLvoid (GLAPI * PROC_glTexImage3D)(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLsizei depth, GLint border, GLenum format, GLenum type, const GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glTexSubImage3D)(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLenum type, const GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glCopyTexSubImage3D)(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLint x, GLint y, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glActiveTexture)(GLenum texture);
typedef GLvoid (GLAPI * PROC_glSampleCoverage)(GLfloat value, GLboolean invert);
typedef GLvoid (GLAPI * PROC_glCompressedTexImage3D)(GLenum target, GLint level, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth, GLint border, GLsizei imageSize, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glCompressedTexImage2D)(GLenum target, GLint level, GLenum internalformat, GLsizei width, GLsizei height, GLint border, GLsizei imageSize, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glCompressedTexImage1D)(GLenum target, GLint level, GLenum internalformat, GLsizei width, GLint border, GLsizei imageSize, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glCompressedTexSubImage3D)(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLsizei imageSize, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glCompressedTexSubImage2D)(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format, GLsizei imageSize, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glCompressedTexSubImage1D)(GLenum target, GLint level, GLint xoffset, GLsizei width, GLenum format, GLsizei imageSize, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glGetCompressedTexImage)(GLenum target, GLint level, GLvoid * img);
typedef GLvoid (GLAPI * PROC_glBlendFuncSeparate)(GLenum sfactorRGB, GLenum dfactorRGB, GLenum sfactorAlpha, GLenum dfactorAlpha);
typedef GLvoid (GLAPI * PROC_glMultiDrawArrays)(GLenum mode, const GLint * first, const GLsizei * count, GLsizei drawcount);
typedef GLvoid (GLAPI * PROC_glMultiDrawElements)(GLenum mode, const GLsizei * count, GLenum type, const GLvoid * const* indices, GLsizei drawcount);
typedef GLvoid (GLAPI * PROC_glPointParameterf)(GLenum pname, GLfloat param);
typedef GLvoid (GLAPI * PROC_glPointParameterfv)(GLenum pname, const GLfloat * params);
typedef GLvoid (GLAPI * PROC_glPointParameteri)(GLenum pname, GLint param);
typedef GLvoid (GLAPI * PROC_glPointParameteriv)(GLenum pname, const GLint * params);
typedef GLvoid (GLAPI * PROC_glBlendColor)(GLfloat red, GLfloat green, GLfloat blue, GLfloat alpha);
typedef GLvoid (GLAPI * PROC_glBlendEquation)(GLenum mode);
typedef GLvoid (GLAPI * PROC_glGenQueries)(GLsizei n, GLuint * ids);
typedef GLvoid (GLAPI * PROC_glDeleteQueries)(GLsizei n, const GLuint * ids);
typedef GLboolean (GLAPI * PROC_glIsQuery)(GLuint id);
typedef GLvoid (GLAPI * PROC_glBeginQuery)(GLenum target, GLuint id);
typedef GLvoid (GLAPI * PROC_glEndQuery)(GLenum target);
typedef GLvoid (GLAPI * PROC_glGetQueryiv)(GLenum target, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetQueryObjectiv)(GLuint id, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetQueryObjectuiv)(GLuint id, GLenum pname, GLuint * params);
typedef GLvoid (GLAPI * PROC_glBindBuffer)(GLenum target, GLuint buffer);
typedef GLvoid (GLAPI * PROC_glDeleteBuffers)(GLsizei n, const GLuint * buffers);
typedef GLvoid (GLAPI * PROC_glGenBuffers)(GLsizei n, GLuint * buffers);
typedef GLboolean (GLAPI * PROC_glIsBuffer)(GLuint buffer);
typedef GLvoid (GLAPI * PROC_glBufferData)(GLenum target, GLsizeiptr size, const GLvoid * data, GLenum usage);
typedef GLvoid (GLAPI * PROC_glBufferSubData)(GLenum target, GLintptr offset, GLsizeiptr size, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glGetBufferSubData)(GLenum target, GLintptr offset, GLsizeiptr size, GLvoid * data);
typedef GLvoid * (GLAPI * PROC_glMapBuffer)(GLenum target, GLenum access);
typedef GLboolean (GLAPI * PROC_glUnmapBuffer)(GLenum target);
typedef GLvoid (GLAPI * PROC_glGetBufferParameteriv)(GLenum target, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetBufferPointerv)(GLenum target, GLenum pname, GLvoid ** params);
typedef GLvoid (GLAPI * PROC_glBlendEquationSeparate)(GLenum modeRGB, GLenum modeAlpha);
typedef GLvoid (GLAPI * PROC_glDrawBuffers)(GLsizei n, const GLenum * bufs);
typedef GLvoid (GLAPI * PROC_glStencilOpSeparate)(GLenum face, GLenum sfail, GLenum dpfail, GLenum dppass);
typedef GLvoid (GLAPI * PROC_glStencilFuncSeparate)(GLenum face, GLenum func, GLint ref, GLuint mask);
typedef GLvoid (GLAPI * PROC_glStencilMaskSeparate)(GLenum face, GLuint mask);
typedef GLvoid (GLAPI * PROC_glAttachShader)(GLuint program, GLuint shader);
typedef GLvoid (GLAPI * PROC_glBindAttribLocation)(GLuint program, GLuint index, const GLchar * name);
typedef GLvoid (GLAPI * PROC_glCompileShader)(GLuint shader);
typedef GLuint (GLAPI * PROC_glCreateProgram)();
typedef GLuint (GLAPI * PROC_glCreateShader)(GLenum type);
typedef GLvoid (GLAPI * PROC_glDeleteProgram)(GLuint program);
typedef GLvoid (GLAPI * PROC_glDeleteShader)(GLuint shader);
typedef GLvoid (GLAPI * PROC_glDetachShader)(GLuint program, GLuint shader);
typedef GLvoid (GLAPI * PROC_glDisableVertexAttribArray)(GLuint index);
typedef GLvoid (GLAPI * PROC_glEnableVertexAttribArray)(GLuint index);
typedef GLvoid (GLAPI * PROC_glGetActiveAttrib)(GLuint program, GLuint index, GLsizei bufSize, GLsizei * length, GLint * size, GLenum * type, GLchar * name);
typedef GLvoid (GLAPI * PROC_glGetActiveUniform)(GLuint program, GLuint index, GLsizei bufSize, GLsizei * length, GLint * size, GLenum * type, GLchar * name);
typedef GLvoid (GLAPI * PROC_glGetAttachedShaders)(GLuint program, GLsizei maxCount, GLsizei * count, GLuint * shaders);
typedef GLint (GLAPI * PROC_glGetAttribLocation)(GLuint program, const GLchar * name);
typedef GLvoid (GLAPI * PROC_glGetProgramiv)(GLuint program, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetProgramInfoLog)(GLuint program, GLsizei bufSize, GLsizei * length, GLchar * infoLog);
typedef GLvoid (GLAPI * PROC_glGetShaderiv)(GLuint shader, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetShaderInfoLog)(GLuint shader, GLsizei bufSize, GLsizei * length, GLchar * infoLog);
typedef GLvoid (GLAPI * PROC_glGetShaderSource)(GLuint shader, GLsizei bufSize, GLsizei * length, GLchar * source);
typedef GLint (GLAPI * PROC_glGetUniformLocation)(GLuint program, const GLchar * name);
typedef GLvoid (GLAPI * PROC_glGetUniformfv)(GLuint program, GLint location, GLfloat * params);
typedef GLvoid (GLAPI * PROC_glGetUniformiv)(GLuint program, GLint location, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetVertexAttribdv)(GLuint index, GLenum pname, GLdouble * params);
typedef GLvoid (GLAPI * PROC_glGetVertexAttribfv)(GLuint index, GLenum pname, GLfloat * params);
typedef GLvoid (GLAPI * PROC_glGetVertexAttribiv)(GLuint index, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetVertexAttribPointerv)(GLuint index, GLenum pname, GLvoid ** pointer);
typedef GLboolean (GLAPI * PROC_glIsProgram)(GLuint program);
typedef GLboolean (GLAPI * PROC_glIsShader)(GLuint shader);
typedef GLvoid (GLAPI * PROC_glLinkProgram)(GLuint program);
typedef GLvoid (GLAPI * PROC_glShaderSource)(GLuint shader, GLsizei count, const GLchar * const* string, const GLint * length);
typedef GLvoid (GLAPI * PROC_glUseProgram)(GLuint program);
typedef GLvoid (GLAPI * PROC_glUniform1f)(GLint location, GLfloat v0);
typedef GLvoid (GLAPI * PROC_glUniform2f)(GLint location, GLfloat v0, GLfloat v1);
typedef GLvoid (GLAPI * PROC_glUniform3f)(GLint location, GLfloat v0, GLfloat v1, GLfloat v2);
typedef GLvoid (GLAPI * PROC_glUniform4f)(GLint location, GLfloat v0, GLfloat v1, GLfloat v2, GLfloat v3);
typedef GLvoid (GLAPI * PROC_glUniform1i)(GLint location, GLint v0);
typedef GLvoid (GLAPI * PROC_glUniform2i)(GLint location, GLint v0, GLint v1);
typedef GLvoid (GLAPI * PROC_glUniform3i)(GLint location, GLint v0, GLint v1, GLint v2);
typedef GLvoid (GLAPI * PROC_glUniform4i)(GLint location, GLint v0, GLint v1, GLint v2, GLint v3);
typedef GLvoid (GLAPI * PROC_glUniform1fv)(GLint location, GLsizei count, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glUniform2fv)(GLint location, GLsizei count, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glUniform3fv)(GLint location, GLsizei count, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glUniform4fv)(GLint location, GLsizei count, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glUniform1iv)(GLint location, GLsizei count, const GLint * value);
typedef GLvoid (GLAPI * PROC_glUniform2iv)(GLint location, GLsizei count, const GLint * value);
typedef GLvoid (GLAPI * PROC_glUniform3iv)(GLint location, GLsizei count, const GLint * value);
typedef GLvoid (GLAPI * PROC_glUniform4iv)(GLint location, GLsizei count, const GLint * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix2fv)(GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix3fv)(GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix4fv)(GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glValidateProgram)(GLuint program);
typedef GLvoid (GLAPI * PROC_glVertexAttrib1d)(GLuint index, GLdouble x);
typedef GLvoid (GLAPI * PROC_glVertexAttrib1dv)(GLuint index, const GLdouble * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib1f)(GLuint index, GLfloat x);
typedef GLvoid (GLAPI * PROC_glVertexAttrib1fv)(GLuint index, const GLfloat * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib1s)(GLuint index, GLshort x);
typedef GLvoid (GLAPI * PROC_glVertexAttrib1sv)(GLuint index, const GLshort * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib2d)(GLuint index, GLdouble x, GLdouble y);
typedef GLvoid (GLAPI * PROC_glVertexAttrib2dv)(GLuint index, const GLdouble * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib2f)(GLuint index, GLfloat x, GLfloat y);
typedef GLvoid (GLAPI * PROC_glVertexAttrib2fv)(GLuint index, const GLfloat * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib2s)(GLuint index, GLshort x, GLshort y);
typedef GLvoid (GLAPI * PROC_glVertexAttrib2sv)(GLuint index, const GLshort * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib3d)(GLuint index, GLdouble x, GLdouble y, GLdouble z);
typedef GLvoid (GLAPI * PROC_glVertexAttrib3dv)(GLuint index, const GLdouble * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib3f)(GLuint index, GLfloat x, GLfloat y, GLfloat z);
typedef GLvoid (GLAPI * PROC_glVertexAttrib3fv)(GLuint index, const GLfloat * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib3s)(GLuint index, GLshort x, GLshort y, GLshort z);
typedef GLvoid (GLAPI * PROC_glVertexAttrib3sv)(GLuint index, const GLshort * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4Nbv)(GLuint index, const GLbyte * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4Niv)(GLuint index, const GLint * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4Nsv)(GLuint index, const GLshort * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4Nub)(GLuint index, GLubyte x, GLubyte y, GLubyte z, GLubyte w);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4Nubv)(GLuint index, const GLubyte * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4Nuiv)(GLuint index, const GLuint * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4Nusv)(GLuint index, const GLushort * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4bv)(GLuint index, const GLbyte * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4d)(GLuint index, GLdouble x, GLdouble y, GLdouble z, GLdouble w);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4dv)(GLuint index, const GLdouble * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4f)(GLuint index, GLfloat x, GLfloat y, GLfloat z, GLfloat w);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4fv)(GLuint index, const GLfloat * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4iv)(GLuint index, const GLint * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4s)(GLuint index, GLshort x, GLshort y, GLshort z, GLshort w);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4sv)(GLuint index, const GLshort * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4ubv)(GLuint index, const GLubyte * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4uiv)(GLuint index, const GLuint * v);
typedef GLvoid (GLAPI * PROC_glVertexAttrib4usv)(GLuint index, const GLushort * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribPointer)(GLuint index, GLint size, GLenum type, GLboolean normalized, GLsizei stride, const GLvoid * pointer);
typedef GLvoid (GLAPI * PROC_glUniformMatrix2x3fv)(GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix3x2fv)(GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix2x4fv)(GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix4x2fv)(GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix3x4fv)(GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix4x3fv)(GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glColorMaski)(GLuint index, GLboolean r, GLboolean g, GLboolean b, GLboolean a);
typedef GLvoid (GLAPI * PROC_glGetBooleani_v)(GLenum target, GLuint index, GLboolean * data);
typedef GLvoid (GLAPI * PROC_glGetIntegeri_v)(GLenum target, GLuint index, GLint * data);
typedef GLvoid (GLAPI * PROC_glEnablei)(GLenum target, GLuint index);
typedef GLvoid (GLAPI * PROC_glDisablei)(GLenum target, GLuint index);
typedef GLboolean (GLAPI * PROC_glIsEnabledi)(GLenum target, GLuint index);
typedef GLvoid (GLAPI * PROC_glBeginTransformFeedback)(GLenum primitiveMode);
typedef GLvoid (GLAPI * PROC_glEndTransformFeedback)();
typedef GLvoid (GLAPI * PROC_glBindBufferRange)(GLenum target, GLuint index, GLuint buffer, GLintptr offset, GLsizeiptr size);
typedef GLvoid (GLAPI * PROC_glBindBufferBase)(GLenum target, GLuint index, GLuint buffer);
typedef GLvoid (GLAPI * PROC_glTransformFeedbackVaryings)(GLuint program, GLsizei count, const GLchar * const* varyings, GLenum bufferMode);
typedef GLvoid (GLAPI * PROC_glGetTransformFeedbackVarying)(GLuint program, GLuint index, GLsizei bufSize, GLsizei * length, GLsizei * size, GLenum * type, GLchar * name);
typedef GLvoid (GLAPI * PROC_glClampColor)(GLenum target, GLenum clamp);
typedef GLvoid (GLAPI * PROC_glBeginConditionalRender)(GLuint id, GLenum mode);
typedef GLvoid (GLAPI * PROC_glEndConditionalRender)();
typedef GLvoid (GLAPI * PROC_glVertexAttribIPointer)(GLuint index, GLint size, GLenum type, GLsizei stride, const GLvoid * pointer);
typedef GLvoid (GLAPI * PROC_glGetVertexAttribIiv)(GLuint index, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetVertexAttribIuiv)(GLuint index, GLenum pname, GLuint * params);
typedef GLvoid (GLAPI * PROC_glVertexAttribI1i)(GLuint index, GLint x);
typedef GLvoid (GLAPI * PROC_glVertexAttribI2i)(GLuint index, GLint x, GLint y);
typedef GLvoid (GLAPI * PROC_glVertexAttribI3i)(GLuint index, GLint x, GLint y, GLint z);
typedef GLvoid (GLAPI * PROC_glVertexAttribI4i)(GLuint index, GLint x, GLint y, GLint z, GLint w);
typedef GLvoid (GLAPI * PROC_glVertexAttribI1ui)(GLuint index, GLuint x);
typedef GLvoid (GLAPI * PROC_glVertexAttribI2ui)(GLuint index, GLuint x, GLuint y);
typedef GLvoid (GLAPI * PROC_glVertexAttribI3ui)(GLuint index, GLuint x, GLuint y, GLuint z);
typedef GLvoid (GLAPI * PROC_glVertexAttribI4ui)(GLuint index, GLuint x, GLuint y, GLuint z, GLuint w);
typedef GLvoid (GLAPI * PROC_glVertexAttribI1iv)(GLuint index, const GLint * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribI2iv)(GLuint index, const GLint * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribI3iv)(GLuint index, const GLint * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribI4iv)(GLuint index, const GLint * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribI1uiv)(GLuint index, const GLuint * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribI2uiv)(GLuint index, const GLuint * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribI3uiv)(GLuint index, const GLuint * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribI4uiv)(GLuint index, const GLuint * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribI4bv)(GLuint index, const GLbyte * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribI4sv)(GLuint index, const GLshort * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribI4ubv)(GLuint index, const GLubyte * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribI4usv)(GLuint index, const GLushort * v);
typedef GLvoid (GLAPI * PROC_glGetUniformuiv)(GLuint program, GLint location, GLuint * params);
typedef GLvoid (GLAPI * PROC_glBindFragDataLocation)(GLuint program, GLuint color, const GLchar * name);
typedef GLint (GLAPI * PROC_glGetFragDataLocation)(GLuint program, const GLchar * name);
typedef GLvoid (GLAPI * PROC_glUniform1ui)(GLint location, GLuint v0);
typedef GLvoid (GLAPI * PROC_glUniform2ui)(GLint location, GLuint v0, GLuint v1);
typedef GLvoid (GLAPI * PROC_glUniform3ui)(GLint location, GLuint v0, GLuint v1, GLuint v2);
typedef GLvoid (GLAPI * PROC_glUniform4ui)(GLint location, GLuint v0, GLuint v1, GLuint v2, GLuint v3);
typedef GLvoid (GLAPI * PROC_glUniform1uiv)(GLint location, GLsizei count, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glUniform2uiv)(GLint location, GLsizei count, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glUniform3uiv)(GLint location, GLsizei count, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glUniform4uiv)(GLint location, GLsizei count, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glTexParameterIiv)(GLenum target, GLenum pname, const GLint * params);
typedef GLvoid (GLAPI * PROC_glTexParameterIuiv)(GLenum target, GLenum pname, const GLuint * params);
typedef GLvoid (GLAPI * PROC_glGetTexParameterIiv)(GLenum target, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetTexParameterIuiv)(GLenum target, GLenum pname, GLuint * params);
typedef GLvoid (GLAPI * PROC_glClearBufferiv)(GLenum buffer, GLint drawbuffer, const GLint * value);
typedef GLvoid (GLAPI * PROC_glClearBufferuiv)(GLenum buffer, GLint drawbuffer, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glClearBufferfv)(GLenum buffer, GLint drawbuffer, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glClearBufferfi)(GLenum buffer, GLint drawbuffer, GLfloat depth, GLint stencil);
typedef const GLubyte * (GLAPI * PROC_glGetStringi)(GLenum name, GLuint index);
typedef GLboolean (GLAPI * PROC_glIsRenderbuffer)(GLuint renderbuffer);
typedef GLvoid (GLAPI * PROC_glBindRenderbuffer)(GLenum target, GLuint renderbuffer);
typedef GLvoid (GLAPI * PROC_glDeleteRenderbuffers)(GLsizei n, const GLuint * renderbuffers);
typedef GLvoid (GLAPI * PROC_glGenRenderbuffers)(GLsizei n, GLuint * renderbuffers);
typedef GLvoid (GLAPI * PROC_glRenderbufferStorage)(GLenum target, GLenum internalformat, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glGetRenderbufferParameteriv)(GLenum target, GLenum pname, GLint * params);
typedef GLboolean (GLAPI * PROC_glIsFramebuffer)(GLuint framebuffer);
typedef GLvoid (GLAPI * PROC_glBindFramebuffer)(GLenum target, GLuint framebuffer);
typedef GLvoid (GLAPI * PROC_glDeleteFramebuffers)(GLsizei n, const GLuint * framebuffers);
typedef GLvoid (GLAPI * PROC_glGenFramebuffers)(GLsizei n, GLuint * framebuffers);
typedef GLenum (GLAPI * PROC_glCheckFramebufferStatus)(GLenum target);
typedef GLvoid (GLAPI * PROC_glFramebufferTexture1D)(GLenum target, GLenum attachment, GLenum textarget, GLuint texture, GLint level);
typedef GLvoid (GLAPI * PROC_glFramebufferTexture2D)(GLenum target, GLenum attachment, GLenum textarget, GLuint texture, GLint level);
typedef GLvoid (GLAPI * PROC_glFramebufferTexture3D)(GLenum target, GLenum attachment, GLenum textarget, GLuint texture, GLint level, GLint zoffset);
typedef GLvoid (GLAPI * PROC_glFramebufferRenderbuffer)(GLenum target, GLenum attachment, GLenum renderbuffertarget, GLuint renderbuffer);
typedef GLvoid (GLAPI * PROC_glGetFramebufferAttachmentParameteriv)(GLenum target, GLenum attachment, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGenerateMipmap)(GLenum target);
typedef GLvoid (GLAPI * PROC_glBlitFramebuffer)(GLint srcX0, GLint srcY0, GLint srcX1, GLint srcY1, GLint dstX0, GLint dstY0, GLint dstX1, GLint dstY1, GLbitfield mask, GLenum filter);
typedef GLvoid (GLAPI * PROC_glRenderbufferStorageMultisample)(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glFramebufferTextureLayer)(GLenum target, GLenum attachment, GLuint texture, GLint level, GLint layer);
typedef GLvoid * (GLAPI * PROC_glMapBufferRange)(GLenum target, GLintptr offset, GLsizeiptr length, GLbitfield access);
typedef GLvoid (GLAPI * PROC_glFlushMappedBufferRange)(GLenum target, GLintptr offset, GLsizeiptr length);
typedef GLvoid (GLAPI * PROC_glBindVertexArray)(GLuint array);
typedef GLvoid (GLAPI * PROC_glDeleteVertexArrays)(GLsizei n, const GLuint * arrays);
typedef GLvoid (GLAPI * PROC_glGenVertexArrays)(GLsizei n, GLuint * arrays);
typedef GLboolean (GLAPI * PROC_glIsVertexArray)(GLuint array);
typedef GLvoid (GLAPI * PROC_glDrawArraysInstanced)(GLenum mode, GLint first, GLsizei count, GLsizei instancecount);
typedef GLvoid (GLAPI * PROC_glDrawElementsInstanced)(GLenum mode, GLsizei count, GLenum type, const GLvoid * indices, GLsizei instancecount);
typedef GLvoid (GLAPI * PROC_glTexBuffer)(GLenum target, GLenum internalformat, GLuint buffer);
typedef GLvoid (GLAPI * PROC_glPrimitiveRestartIndex)(GLuint index);
typedef GLvoid (GLAPI * PROC_glCopyBufferSubData)(GLenum readTarget, GLenum writeTarget, GLintptr readOffset, GLintptr writeOffset, GLsizeiptr size);
typedef GLvoid (GLAPI * PROC_glGetUniformIndices)(GLuint program, GLsizei uniformCount, const GLchar * const* uniformNames, GLuint * uniformIndices);
typedef GLvoid (GLAPI * PROC_glGetActiveUniformsiv)(GLuint program, GLsizei uniformCount, const GLuint * uniformIndices, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetActiveUniformName)(GLuint program, GLuint uniformIndex, GLsizei bufSize, GLsizei * length, GLchar * uniformName);
typedef GLuint (GLAPI * PROC_glGetUniformBlockIndex)(GLuint program, const GLchar * uniformBlockName);
typedef GLvoid (GLAPI * PROC_glGetActiveUniformBlockiv)(GLuint program, GLuint uniformBlockIndex, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetActiveUniformBlockName)(GLuint program, GLuint uniformBlockIndex, GLsizei bufSize, GLsizei * length, GLchar * uniformBlockName);
typedef GLvoid (GLAPI * PROC_glUniformBlockBinding)(GLuint program, GLuint uniformBlockIndex, GLuint uniformBlockBinding);
typedef GLvoid (GLAPI * PROC_glDrawElementsBaseVertex)(GLenum mode, GLsizei count, GLenum type, const GLvoid * indices, GLint basevertex);
typedef GLvoid (GLAPI * PROC_glDrawRangeElementsBaseVertex)(GLenum mode, GLuint start, GLuint end, GLsizei count, GLenum type, const GLvoid * indices, GLint basevertex);
typedef GLvoid (GLAPI * PROC_glDrawElementsInstancedBaseVertex)(GLenum mode, GLsizei count, GLenum type, const GLvoid * indices, GLsizei instancecount, GLint basevertex);
typedef GLvoid (GLAPI * PROC_glMultiDrawElementsBaseVertex)(GLenum mode, const GLsizei * count, GLenum type, const GLvoid * const* indices, GLsizei drawcount, const GLint * basevertex);
typedef GLvoid (GLAPI * PROC_glProvokingVertex)(GLenum mode);
typedef GLsync (GLAPI * PROC_glFenceSync)(GLenum condition, GLbitfield flags);
typedef GLboolean (GLAPI * PROC_glIsSync)(GLsync sync);
typedef GLvoid (GLAPI * PROC_glDeleteSync)(GLsync sync);
typedef GLenum (GLAPI * PROC_glClientWaitSync)(GLsync sync, GLbitfield flags, GLuint64 timeout);
typedef GLvoid (GLAPI * PROC_glWaitSync)(GLsync sync, GLbitfield flags, GLuint64 timeout);
typedef GLvoid (GLAPI * PROC_glGetInteger64v)(GLenum pname, GLint64 * data);
typedef GLvoid (GLAPI * PROC_glGetSynciv)(GLsync sync, GLenum pname, GLsizei bufSize, GLsizei * length, GLint * values);
typedef GLvoid (GLAPI * PROC_glGetInteger64i_v)(GLenum target, GLuint index, GLint64 * data);
typedef GLvoid (GLAPI * PROC_glGetBufferParameteri64v)(GLenum target, GLenum pname, GLint64 * params);
typedef GLvoid (GLAPI * PROC_glFramebufferTexture)(GLenum target, GLenum attachment, GLuint texture, GLint level);
typedef GLvoid (GLAPI * PROC_glTexImage2DMultisample)(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height, GLboolean fixedsamplelocations);
typedef GLvoid (GLAPI * PROC_glTexImage3DMultisample)(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth, GLboolean fixedsamplelocations);
typedef GLvoid (GLAPI * PROC_glGetMultisamplefv)(GLenum pname, GLuint index, GLfloat * val);
typedef GLvoid (GLAPI * PROC_glSampleMaski)(GLuint maskNumber, GLbitfield mask);
typedef GLvoid (GLAPI * PROC_glBindFragDataLocationIndexed)(GLuint program, GLuint colorNumber, GLuint index, const GLchar * name);
typedef GLint (GLAPI * PROC_glGetFragDataIndex)(GLuint program, const GLchar * name);
typedef GLvoid (GLAPI * PROC_glGenSamplers)(GLsizei count, GLuint * samplers);
typedef GLvoid (GLAPI * PROC_glDeleteSamplers)(GLsizei count, const GLuint * samplers);
typedef GLboolean (GLAPI * PROC_glIsSampler)(GLuint sampler);
typedef GLvoid (GLAPI * PROC_glBindSampler)(GLuint unit, GLuint sampler);
typedef GLvoid (GLAPI * PROC_glSamplerParameteri)(GLuint sampler, GLenum pname, GLint param);
typedef GLvoid (GLAPI * PROC_glSamplerParameteriv)(GLuint sampler, GLenum pname, const GLint * param);
typedef GLvoid (GLAPI * PROC_glSamplerParameterf)(GLuint sampler, GLenum pname, GLfloat param);
typedef GLvoid (GLAPI * PROC_glSamplerParameterfv)(GLuint sampler, GLenum pname, const GLfloat * param);
typedef GLvoid (GLAPI * PROC_glSamplerParameterIiv)(GLuint sampler, GLenum pname, const GLint * param);
typedef GLvoid (GLAPI * PROC_glSamplerParameterIuiv)(GLuint sampler, GLenum pname, const GLuint * param);
typedef GLvoid (GLAPI * PROC_glGetSamplerParameteriv)(GLuint sampler, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetSamplerParameterIiv)(GLuint sampler, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetSamplerParameterfv)(GLuint sampler, GLenum pname, GLfloat * params);
typedef GLvoid (GLAPI * PROC_glGetSamplerParameterIuiv)(GLuint sampler, GLenum pname, GLuint * params);
typedef GLvoid (GLAPI * PROC_glQueryCounter)(GLuint id, GLenum target);
typedef GLvoid (GLAPI * PROC_glGetQueryObjecti64v)(GLuint id, GLenum pname, GLint64 * params);
typedef GLvoid (GLAPI * PROC_glGetQueryObjectui64v)(GLuint id, GLenum pname, GLuint64 * params);
typedef GLvoid (GLAPI * PROC_glVertexAttribDivisor)(GLuint index, GLuint divisor);
typedef GLvoid (GLAPI * PROC_glVertexAttribP1ui)(GLuint index, GLenum type, GLboolean normalized, GLuint value);
typedef GLvoid (GLAPI * PROC_glVertexAttribP1uiv)(GLuint index, GLenum type, GLboolean normalized, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glVertexAttribP2ui)(GLuint index, GLenum type, GLboolean normalized, GLuint value);
typedef GLvoid (GLAPI * PROC_glVertexAttribP2uiv)(GLuint index, GLenum type, GLboolean normalized, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glVertexAttribP3ui)(GLuint index, GLenum type, GLboolean normalized, GLuint value);
typedef GLvoid (GLAPI * PROC_glVertexAttribP3uiv)(GLuint index, GLenum type, GLboolean normalized, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glVertexAttribP4ui)(GLuint index, GLenum type, GLboolean normalized, GLuint value);
typedef GLvoid (GLAPI * PROC_glVertexAttribP4uiv)(GLuint index, GLenum type, GLboolean normalized, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glMinSampleShading)(GLfloat value);
typedef GLvoid (GLAPI * PROC_glBlendEquationi)(GLuint buf, GLenum mode);
typedef GLvoid (GLAPI * PROC_glBlendEquationSeparatei)(GLuint buf, GLenum modeRGB, GLenum modeAlpha);
typedef GLvoid (GLAPI * PROC_glBlendFunci)(GLuint buf, GLenum src, GLenum dst);
typedef GLvoid (GLAPI * PROC_glBlendFuncSeparatei)(GLuint buf, GLenum srcRGB, GLenum dstRGB, GLenum srcAlpha, GLenum dstAlpha);
typedef GLvoid (GLAPI * PROC_glDrawArraysIndirect)(GLenum mode, const GLvoid * indirect);
typedef GLvoid (GLAPI * PROC_glDrawElementsIndirect)(GLenum mode, GLenum type, const GLvoid * indirect);
typedef GLvoid (GLAPI * PROC_glUniform1d)(GLint location, GLdouble x);
typedef GLvoid (GLAPI * PROC_glUniform2d)(GLint location, GLdouble x, GLdouble y);
typedef GLvoid (GLAPI * PROC_glUniform3d)(GLint location, GLdouble x, GLdouble y, GLdouble z);
typedef GLvoid (GLAPI * PROC_glUniform4d)(GLint location, GLdouble x, GLdouble y, GLdouble z, GLdouble w);
typedef GLvoid (GLAPI * PROC_glUniform1dv)(GLint location, GLsizei count, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glUniform2dv)(GLint location, GLsizei count, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glUniform3dv)(GLint location, GLsizei count, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glUniform4dv)(GLint location, GLsizei count, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix2dv)(GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix3dv)(GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix4dv)(GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix2x3dv)(GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix2x4dv)(GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix3x2dv)(GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix3x4dv)(GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix4x2dv)(GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glUniformMatrix4x3dv)(GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glGetUniformdv)(GLuint program, GLint location, GLdouble * params);
typedef GLint (GLAPI * PROC_glGetSubroutineUniformLocation)(GLuint program, GLenum shadertype, const GLchar * name);
typedef GLuint (GLAPI * PROC_glGetSubroutineIndex)(GLuint program, GLenum shadertype, const GLchar * name);
typedef GLvoid (GLAPI * PROC_glGetActiveSubroutineUniformiv)(GLuint program, GLenum shadertype, GLuint index, GLenum pname, GLint * values);
typedef GLvoid (GLAPI * PROC_glGetActiveSubroutineUniformName)(GLuint program, GLenum shadertype, GLuint index, GLsizei bufsize, GLsizei * length, GLchar * name);
typedef GLvoid (GLAPI * PROC_glGetActiveSubroutineName)(GLuint program, GLenum shadertype, GLuint index, GLsizei bufsize, GLsizei * length, GLchar * name);
typedef GLvoid (GLAPI * PROC_glUniformSubroutinesuiv)(GLenum shadertype, GLsizei count, const GLuint * indices);
typedef GLvoid (GLAPI * PROC_glGetUniformSubroutineuiv)(GLenum shadertype, GLint location, GLuint * params);
typedef GLvoid (GLAPI * PROC_glGetProgramStageiv)(GLuint program, GLenum shadertype, GLenum pname, GLint * values);
typedef GLvoid (GLAPI * PROC_glPatchParameteri)(GLenum pname, GLint value);
typedef GLvoid (GLAPI * PROC_glPatchParameterfv)(GLenum pname, const GLfloat * values);
typedef GLvoid (GLAPI * PROC_glBindTransformFeedback)(GLenum target, GLuint id);
typedef GLvoid (GLAPI * PROC_glDeleteTransformFeedbacks)(GLsizei n, const GLuint * ids);
typedef GLvoid (GLAPI * PROC_glGenTransformFeedbacks)(GLsizei n, GLuint * ids);
typedef GLboolean (GLAPI * PROC_glIsTransformFeedback)(GLuint id);
typedef GLvoid (GLAPI * PROC_glPauseTransformFeedback)();
typedef GLvoid (GLAPI * PROC_glResumeTransformFeedback)();
typedef GLvoid (GLAPI * PROC_glDrawTransformFeedback)(GLenum mode, GLuint id);
typedef GLvoid (GLAPI * PROC_glDrawTransformFeedbackStream)(GLenum mode, GLuint id, GLuint stream);
typedef GLvoid (GLAPI * PROC_glBeginQueryIndexed)(GLenum target, GLuint index, GLuint id);
typedef GLvoid (GLAPI * PROC_glEndQueryIndexed)(GLenum target, GLuint index);
typedef GLvoid (GLAPI * PROC_glGetQueryIndexediv)(GLenum target, GLuint index, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glReleaseShaderCompiler)();
typedef GLvoid (GLAPI * PROC_glShaderBinary)(GLsizei count, const GLuint * shaders, GLenum binaryformat, const GLvoid * binary, GLsizei length);
typedef GLvoid (GLAPI * PROC_glGetShaderPrecisionFormat)(GLenum shadertype, GLenum precisiontype, GLint * range, GLint * precision);
typedef GLvoid (GLAPI * PROC_glDepthRangef)(GLfloat n, GLfloat f);
typedef GLvoid (GLAPI * PROC_glClearDepthf)(GLfloat d);
typedef GLvoid (GLAPI * PROC_glGetProgramBinary)(GLuint program, GLsizei bufSize, GLsizei * length, GLenum * binaryFormat, GLvoid * binary);
typedef GLvoid (GLAPI * PROC_glProgramBinary)(GLuint program, GLenum binaryFormat, const GLvoid * binary, GLsizei length);
typedef GLvoid (GLAPI * PROC_glProgramParameteri)(GLuint program, GLenum pname, GLint value);
typedef GLvoid (GLAPI * PROC_glUseProgramStages)(GLuint pipeline, GLbitfield stages, GLuint program);
typedef GLvoid (GLAPI * PROC_glActiveShaderProgram)(GLuint pipeline, GLuint program);
typedef GLuint (GLAPI * PROC_glCreateShaderProgramv)(GLenum type, GLsizei count, const GLchar * const* strings);
typedef GLvoid (GLAPI * PROC_glBindProgramPipeline)(GLuint pipeline);
typedef GLvoid (GLAPI * PROC_glDeleteProgramPipelines)(GLsizei n, const GLuint * pipelines);
typedef GLvoid (GLAPI * PROC_glGenProgramPipelines)(GLsizei n, GLuint * pipelines);
typedef GLboolean (GLAPI * PROC_glIsProgramPipeline)(GLuint pipeline);
typedef GLvoid (GLAPI * PROC_glGetProgramPipelineiv)(GLuint pipeline, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glProgramUniform1i)(GLuint program, GLint location, GLint v0);
typedef GLvoid (GLAPI * PROC_glProgramUniform1iv)(GLuint program, GLint location, GLsizei count, const GLint * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform1f)(GLuint program, GLint location, GLfloat v0);
typedef GLvoid (GLAPI * PROC_glProgramUniform1fv)(GLuint program, GLint location, GLsizei count, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform1d)(GLuint program, GLint location, GLdouble v0);
typedef GLvoid (GLAPI * PROC_glProgramUniform1dv)(GLuint program, GLint location, GLsizei count, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform1ui)(GLuint program, GLint location, GLuint v0);
typedef GLvoid (GLAPI * PROC_glProgramUniform1uiv)(GLuint program, GLint location, GLsizei count, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform2i)(GLuint program, GLint location, GLint v0, GLint v1);
typedef GLvoid (GLAPI * PROC_glProgramUniform2iv)(GLuint program, GLint location, GLsizei count, const GLint * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform2f)(GLuint program, GLint location, GLfloat v0, GLfloat v1);
typedef GLvoid (GLAPI * PROC_glProgramUniform2fv)(GLuint program, GLint location, GLsizei count, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform2d)(GLuint program, GLint location, GLdouble v0, GLdouble v1);
typedef GLvoid (GLAPI * PROC_glProgramUniform2dv)(GLuint program, GLint location, GLsizei count, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform2ui)(GLuint program, GLint location, GLuint v0, GLuint v1);
typedef GLvoid (GLAPI * PROC_glProgramUniform2uiv)(GLuint program, GLint location, GLsizei count, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform3i)(GLuint program, GLint location, GLint v0, GLint v1, GLint v2);
typedef GLvoid (GLAPI * PROC_glProgramUniform3iv)(GLuint program, GLint location, GLsizei count, const GLint * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform3f)(GLuint program, GLint location, GLfloat v0, GLfloat v1, GLfloat v2);
typedef GLvoid (GLAPI * PROC_glProgramUniform3fv)(GLuint program, GLint location, GLsizei count, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform3d)(GLuint program, GLint location, GLdouble v0, GLdouble v1, GLdouble v2);
typedef GLvoid (GLAPI * PROC_glProgramUniform3dv)(GLuint program, GLint location, GLsizei count, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform3ui)(GLuint program, GLint location, GLuint v0, GLuint v1, GLuint v2);
typedef GLvoid (GLAPI * PROC_glProgramUniform3uiv)(GLuint program, GLint location, GLsizei count, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform4i)(GLuint program, GLint location, GLint v0, GLint v1, GLint v2, GLint v3);
typedef GLvoid (GLAPI * PROC_glProgramUniform4iv)(GLuint program, GLint location, GLsizei count, const GLint * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform4f)(GLuint program, GLint location, GLfloat v0, GLfloat v1, GLfloat v2, GLfloat v3);
typedef GLvoid (GLAPI * PROC_glProgramUniform4fv)(GLuint program, GLint location, GLsizei count, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform4d)(GLuint program, GLint location, GLdouble v0, GLdouble v1, GLdouble v2, GLdouble v3);
typedef GLvoid (GLAPI * PROC_glProgramUniform4dv)(GLuint program, GLint location, GLsizei count, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glProgramUniform4ui)(GLuint program, GLint location, GLuint v0, GLuint v1, GLuint v2, GLuint v3);
typedef GLvoid (GLAPI * PROC_glProgramUniform4uiv)(GLuint program, GLint location, GLsizei count, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix2fv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix3fv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix4fv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix2dv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix3dv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix4dv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix2x3fv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix3x2fv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix2x4fv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix4x2fv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix3x4fv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix4x3fv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix2x3dv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix3x2dv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix2x4dv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix4x2dv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix3x4dv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glProgramUniformMatrix4x3dv)(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLdouble * value);
typedef GLvoid (GLAPI * PROC_glValidateProgramPipeline)(GLuint pipeline);
typedef GLvoid (GLAPI * PROC_glGetProgramPipelineInfoLog)(GLuint pipeline, GLsizei bufSize, GLsizei * length, GLchar * infoLog);
typedef GLvoid (GLAPI * PROC_glVertexAttribL1d)(GLuint index, GLdouble x);
typedef GLvoid (GLAPI * PROC_glVertexAttribL2d)(GLuint index, GLdouble x, GLdouble y);
typedef GLvoid (GLAPI * PROC_glVertexAttribL3d)(GLuint index, GLdouble x, GLdouble y, GLdouble z);
typedef GLvoid (GLAPI * PROC_glVertexAttribL4d)(GLuint index, GLdouble x, GLdouble y, GLdouble z, GLdouble w);
typedef GLvoid (GLAPI * PROC_glVertexAttribL1dv)(GLuint index, const GLdouble * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribL2dv)(GLuint index, const GLdouble * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribL3dv)(GLuint index, const GLdouble * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribL4dv)(GLuint index, const GLdouble * v);
typedef GLvoid (GLAPI * PROC_glVertexAttribLPointer)(GLuint index, GLint size, GLenum type, GLsizei stride, const GLvoid * pointer);
typedef GLvoid (GLAPI * PROC_glGetVertexAttribLdv)(GLuint index, GLenum pname, GLdouble * params);
typedef GLvoid (GLAPI * PROC_glViewportArrayv)(GLuint first, GLsizei count, const GLfloat * v);
typedef GLvoid (GLAPI * PROC_glViewportIndexedf)(GLuint index, GLfloat x, GLfloat y, GLfloat w, GLfloat h);
typedef GLvoid (GLAPI * PROC_glViewportIndexedfv)(GLuint index, const GLfloat * v);
typedef GLvoid (GLAPI * PROC_glScissorArrayv)(GLuint first, GLsizei count, const GLint * v);
typedef GLvoid (GLAPI * PROC_glScissorIndexed)(GLuint index, GLint left, GLint bottom, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glScissorIndexedv)(GLuint index, const GLint * v);
typedef GLvoid (GLAPI * PROC_glDepthRangeArrayv)(GLuint first, GLsizei count, const GLdouble * v);
typedef GLvoid (GLAPI * PROC_glDepthRangeIndexed)(GLuint index, GLdouble n, GLdouble f);
typedef GLvoid (GLAPI * PROC_glGetFloati_v)(GLenum target, GLuint index, GLfloat * data);
typedef GLvoid (GLAPI * PROC_glGetDoublei_v)(GLenum target, GLuint index, GLdouble * data);
typedef GLvoid (GLAPI * PROC_glDrawArraysInstancedBaseInstance)(GLenum mode, GLint first, GLsizei count, GLsizei instancecount, GLuint baseinstance);
typedef GLvoid (GLAPI * PROC_glDrawElementsInstancedBaseInstance)(GLenum mode, GLsizei count, GLenum type, const GLvoid * indices, GLsizei instancecount, GLuint baseinstance);
typedef GLvoid (GLAPI * PROC_glDrawElementsInstancedBaseVertexBaseInstance)(GLenum mode, GLsizei count, GLenum type, const GLvoid * indices, GLsizei instancecount, GLint basevertex, GLuint baseinstance);
typedef GLvoid (GLAPI * PROC_glGetInternalformativ)(GLenum target, GLenum internalformat, GLenum pname, GLsizei bufSize, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetActiveAtomicCounterBufferiv)(GLuint program, GLuint bufferIndex, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glBindImageTexture)(GLuint unit, GLuint texture, GLint level, GLboolean layered, GLint layer, GLenum access, GLenum format);
typedef GLvoid (GLAPI * PROC_glMemoryBarrier)(GLbitfield barriers);
typedef GLvoid (GLAPI * PROC_glTexStorage1D)(GLenum target, GLsizei levels, GLenum internalformat, GLsizei width);
typedef GLvoid (GLAPI * PROC_glTexStorage2D)(GLenum target, GLsizei levels, GLenum internalformat, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glTexStorage3D)(GLenum target, GLsizei levels, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth);
typedef GLvoid (GLAPI * PROC_glDrawTransformFeedbackInstanced)(GLenum mode, GLuint id, GLsizei instancecount);
typedef GLvoid (GLAPI * PROC_glDrawTransformFeedbackStreamInstanced)(GLenum mode, GLuint id, GLuint stream, GLsizei instancecount);
typedef GLvoid (GLAPI * PROC_glClearBufferData)(GLenum target, GLenum internalformat, GLenum format, GLenum type, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glClearBufferSubData)(GLenum target, GLenum internalformat, GLintptr offset, GLsizeiptr size, GLenum format, GLenum type, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glDispatchCompute)(GLuint num_groups_x, GLuint num_groups_y, GLuint num_groups_z);
typedef GLvoid (GLAPI * PROC_glDispatchComputeIndirect)(GLintptr indirect);
typedef GLvoid (GLAPI * PROC_glCopyImageSubData)(GLuint srcName, GLenum srcTarget, GLint srcLevel, GLint srcX, GLint srcY, GLint srcZ, GLuint dstName, GLenum dstTarget, GLint dstLevel, GLint dstX, GLint dstY, GLint dstZ, GLsizei srcWidth, GLsizei srcHeight, GLsizei srcDepth);
typedef GLvoid (GLAPI * PROC_glFramebufferParameteri)(GLenum target, GLenum pname, GLint param);
typedef GLvoid (GLAPI * PROC_glGetFramebufferParameteriv)(GLenum target, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetInternalformati64v)(GLenum target, GLenum internalformat, GLenum pname, GLsizei bufSize, GLint64 * params);
typedef GLvoid (GLAPI * PROC_glInvalidateTexSubImage)(GLuint texture, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth);
typedef GLvoid (GLAPI * PROC_glInvalidateTexImage)(GLuint texture, GLint level);
typedef GLvoid (GLAPI * PROC_glInvalidateBufferSubData)(GLuint buffer, GLintptr offset, GLsizeiptr length);
typedef GLvoid (GLAPI * PROC_glInvalidateBufferData)(GLuint buffer);
typedef GLvoid (GLAPI * PROC_glInvalidateFramebuffer)(GLenum target, GLsizei numAttachments, const GLenum * attachments);
typedef GLvoid (GLAPI * PROC_glInvalidateSubFramebuffer)(GLenum target, GLsizei numAttachments, const GLenum * attachments, GLint x, GLint y, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glMultiDrawArraysIndirect)(GLenum mode, const GLvoid * indirect, GLsizei drawcount, GLsizei stride);
typedef GLvoid (GLAPI * PROC_glMultiDrawElementsIndirect)(GLenum mode, GLenum type, const GLvoid * indirect, GLsizei drawcount, GLsizei stride);
typedef GLvoid (GLAPI * PROC_glGetProgramInterfaceiv)(GLuint program, GLenum programInterface, GLenum pname, GLint * params);
typedef GLuint (GLAPI * PROC_glGetProgramResourceIndex)(GLuint program, GLenum programInterface, const GLchar * name);
typedef GLvoid (GLAPI * PROC_glGetProgramResourceName)(GLuint program, GLenum programInterface, GLuint index, GLsizei bufSize, GLsizei * length, GLchar * name);
typedef GLvoid (GLAPI * PROC_glGetProgramResourceiv)(GLuint program, GLenum programInterface, GLuint index, GLsizei propCount, const GLenum * props, GLsizei bufSize, GLsizei * length, GLint * params);
typedef GLint (GLAPI * PROC_glGetProgramResourceLocation)(GLuint program, GLenum programInterface, const GLchar * name);
typedef GLint (GLAPI * PROC_glGetProgramResourceLocationIndex)(GLuint program, GLenum programInterface, const GLchar * name);
typedef GLvoid (GLAPI * PROC_glShaderStorageBlockBinding)(GLuint program, GLuint storageBlockIndex, GLuint storageBlockBinding);
typedef GLvoid (GLAPI * PROC_glTexBufferRange)(GLenum target, GLenum internalformat, GLuint buffer, GLintptr offset, GLsizeiptr size);
typedef GLvoid (GLAPI * PROC_glTexStorage2DMultisample)(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height, GLboolean fixedsamplelocations);
typedef GLvoid (GLAPI * PROC_glTexStorage3DMultisample)(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth, GLboolean fixedsamplelocations);
typedef GLvoid (GLAPI * PROC_glTextureView)(GLuint texture, GLenum target, GLuint origtexture, GLenum internalformat, GLuint minlevel, GLuint numlevels, GLuint minlayer, GLuint numlayers);
typedef GLvoid (GLAPI * PROC_glBindVertexBuffer)(GLuint bindingindex, GLuint buffer, GLintptr offset, GLsizei stride);
typedef GLvoid (GLAPI * PROC_glVertexAttribFormat)(GLuint attribindex, GLint size, GLenum type, GLboolean normalized, GLuint relativeoffset);
typedef GLvoid (GLAPI * PROC_glVertexAttribIFormat)(GLuint attribindex, GLint size, GLenum type, GLuint relativeoffset);
typedef GLvoid (GLAPI * PROC_glVertexAttribLFormat)(GLuint attribindex, GLint size, GLenum type, GLuint relativeoffset);
typedef GLvoid (GLAPI * PROC_glVertexAttribBinding)(GLuint attribindex, GLuint bindingindex);
typedef GLvoid (GLAPI * PROC_glVertexBindingDivisor)(GLuint bindingindex, GLuint divisor);
typedef GLvoid (GLAPI * PROC_glDebugMessageControl)(GLenum source, GLenum type, GLenum severity, GLsizei count, const GLuint * ids, GLboolean enabled);
typedef GLvoid (GLAPI * PROC_glDebugMessageInsert)(GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar * buf);
typedef GLvoid (GLAPI * PROC_glDebugMessageCallback)(GLDEBUGPROC callback, const GLvoid * userParam);
typedef GLuint (GLAPI * PROC_glGetDebugMessageLog)(GLuint count, GLsizei bufSize, GLenum * sources, GLenum * types, GLuint * ids, GLenum * severities, GLsizei * lengths, GLchar * messageLog);
typedef GLvoid (GLAPI * PROC_glPushDebugGroup)(GLenum source, GLuint id, GLsizei length, const GLchar * message);
typedef GLvoid (GLAPI * PROC_glPopDebugGroup)();
typedef GLvoid (GLAPI * PROC_glObjectLabel)(GLenum identifier, GLuint name, GLsizei length, const GLchar * label);
typedef GLvoid (GLAPI * PROC_glGetObjectLabel)(GLenum identifier, GLuint name, GLsizei bufSize, GLsizei * length, GLchar * label);
typedef GLvoid (GLAPI * PROC_glObjectPtrLabel)(const GLvoid * ptr, GLsizei length, const GLchar * label);
typedef GLvoid (GLAPI * PROC_glGetObjectPtrLabel)(const GLvoid * ptr, GLsizei bufSize, GLsizei * length, GLchar * label);
typedef GLvoid (GLAPI * PROC_glBufferStorage)(GLenum target, GLsizeiptr size, const GLvoid * data, GLbitfield flags);
typedef GLvoid (GLAPI * PROC_glClearTexImage)(GLuint texture, GLint level, GLenum format, GLenum type, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glClearTexSubImage)(GLuint texture, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLenum type, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glBindBuffersBase)(GLenum target, GLuint first, GLsizei count, const GLuint * buffers);
typedef GLvoid (GLAPI * PROC_glBindBuffersRange)(GLenum target, GLuint first, GLsizei count, const GLuint * buffers, const GLintptr * offsets, const GLsizeiptr * sizes);
typedef GLvoid (GLAPI * PROC_glBindTextures)(GLuint first, GLsizei count, const GLuint * textures);
typedef GLvoid (GLAPI * PROC_glBindSamplers)(GLuint first, GLsizei count, const GLuint * samplers);
typedef GLvoid (GLAPI * PROC_glBindImageTextures)(GLuint first, GLsizei count, const GLuint * textures);
typedef GLvoid (GLAPI * PROC_glBindVertexBuffers)(GLuint first, GLsizei count, const GLuint * buffers, const GLintptr * offsets, const GLsizei * strides);
typedef GLvoid (GLAPI * PROC_glClipControl)(GLenum origin, GLenum depth);
typedef GLvoid (GLAPI * PROC_glCreateTransformFeedbacks)(GLsizei n, GLuint * ids);
typedef GLvoid (GLAPI * PROC_glTransformFeedbackBufferBase)(GLuint xfb, GLuint index, GLuint buffer);
typedef GLvoid (GLAPI * PROC_glTransformFeedbackBufferRange)(GLuint xfb, GLuint index, GLuint buffer, GLintptr offset, GLsizeiptr size);
typedef GLvoid (GLAPI * PROC_glGetTransformFeedbackiv)(GLuint xfb, GLenum pname, GLint * param);
typedef GLvoid (GLAPI * PROC_glGetTransformFeedbacki_v)(GLuint xfb, GLenum pname, GLuint index, GLint * param);
typedef GLvoid (GLAPI * PROC_glGetTransformFeedbacki64_v)(GLuint xfb, GLenum pname, GLuint index, GLint64 * param);
typedef GLvoid (GLAPI * PROC_glCreateBuffers)(GLsizei n, GLuint * buffers);
typedef GLvoid (GLAPI * PROC_glNamedBufferStorage)(GLuint buffer, GLsizeiptr size, const GLvoid * data, GLbitfield flags);
typedef GLvoid (GLAPI * PROC_glNamedBufferData)(GLuint buffer, GLsizeiptr size, const GLvoid * data, GLenum usage);
typedef GLvoid (GLAPI * PROC_glNamedBufferSubData)(GLuint buffer, GLintptr offset, GLsizeiptr size, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glCopyNamedBufferSubData)(GLuint readBuffer, GLuint writeBuffer, GLintptr readOffset, GLintptr writeOffset, GLsizeiptr size);
typedef GLvoid (GLAPI * PROC_glClearNamedBufferData)(GLuint buffer, GLenum internalformat, GLenum format, GLenum type, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glClearNamedBufferSubData)(GLuint buffer, GLenum internalformat, GLintptr offset, GLsizeiptr size, GLenum format, GLenum type, const GLvoid * data);
typedef GLvoid * (GLAPI * PROC_glMapNamedBuffer)(GLuint buffer, GLenum access);
typedef GLvoid * (GLAPI * PROC_glMapNamedBufferRange)(GLuint buffer, GLintptr offset, GLsizeiptr length, GLbitfield access);
typedef GLboolean (GLAPI * PROC_glUnmapNamedBuffer)(GLuint buffer);
typedef GLvoid (GLAPI * PROC_glFlushMappedNamedBufferRange)(GLuint buffer, GLintptr offset, GLsizeiptr length);
typedef GLvoid (GLAPI * PROC_glGetNamedBufferParameteriv)(GLuint buffer, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetNamedBufferParameteri64v)(GLuint buffer, GLenum pname, GLint64 * params);
typedef GLvoid (GLAPI * PROC_glGetNamedBufferPointerv)(GLuint buffer, GLenum pname, GLvoid ** params);
typedef GLvoid (GLAPI * PROC_glGetNamedBufferSubData)(GLuint buffer, GLintptr offset, GLsizeiptr size, GLvoid * data);
typedef GLvoid (GLAPI * PROC_glCreateFramebuffers)(GLsizei n, GLuint * framebuffers);
typedef GLvoid (GLAPI * PROC_glNamedFramebufferRenderbuffer)(GLuint framebuffer, GLenum attachment, GLenum renderbuffertarget, GLuint renderbuffer);
typedef GLvoid (GLAPI * PROC_glNamedFramebufferParameteri)(GLuint framebuffer, GLenum pname, GLint param);
typedef GLvoid (GLAPI * PROC_glNamedFramebufferTexture)(GLuint framebuffer, GLenum attachment, GLuint texture, GLint level);
typedef GLvoid (GLAPI * PROC_glNamedFramebufferTextureLayer)(GLuint framebuffer, GLenum attachment, GLuint texture, GLint level, GLint layer);
typedef GLvoid (GLAPI * PROC_glNamedFramebufferDrawBuffer)(GLuint framebuffer, GLenum buf);
typedef GLvoid (GLAPI * PROC_glNamedFramebufferDrawBuffers)(GLuint framebuffer, GLsizei n, const GLenum * bufs);
typedef GLvoid (GLAPI * PROC_glNamedFramebufferReadBuffer)(GLuint framebuffer, GLenum src);
typedef GLvoid (GLAPI * PROC_glInvalidateNamedFramebufferData)(GLuint framebuffer, GLsizei numAttachments, const GLenum * attachments);
typedef GLvoid (GLAPI * PROC_glInvalidateNamedFramebufferSubData)(GLuint framebuffer, GLsizei numAttachments, const GLenum * attachments, GLint x, GLint y, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glClearNamedFramebufferiv)(GLuint framebuffer, GLenum buffer, GLint drawbuffer, const GLint * value);
typedef GLvoid (GLAPI * PROC_glClearNamedFramebufferuiv)(GLuint framebuffer, GLenum buffer, GLint drawbuffer, const GLuint * value);
typedef GLvoid (GLAPI * PROC_glClearNamedFramebufferfv)(GLuint framebuffer, GLenum buffer, GLint drawbuffer, const GLfloat * value);
typedef GLvoid (GLAPI * PROC_glClearNamedFramebufferfi)(GLuint framebuffer, GLenum buffer, GLint drawbuffer, GLfloat depth, GLint stencil);
typedef GLvoid (GLAPI * PROC_glBlitNamedFramebuffer)(GLuint readFramebuffer, GLuint drawFramebuffer, GLint srcX0, GLint srcY0, GLint srcX1, GLint srcY1, GLint dstX0, GLint dstY0, GLint dstX1, GLint dstY1, GLbitfield mask, GLenum filter);
typedef GLenum (GLAPI * PROC_glCheckNamedFramebufferStatus)(GLuint framebuffer, GLenum target);
typedef GLvoid (GLAPI * PROC_glGetNamedFramebufferParameteriv)(GLuint framebuffer, GLenum pname, GLint * param);
typedef GLvoid (GLAPI * PROC_glGetNamedFramebufferAttachmentParameteriv)(GLuint framebuffer, GLenum attachment, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glCreateRenderbuffers)(GLsizei n, GLuint * renderbuffers);
typedef GLvoid (GLAPI * PROC_glNamedRenderbufferStorage)(GLuint renderbuffer, GLenum internalformat, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glNamedRenderbufferStorageMultisample)(GLuint renderbuffer, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glGetNamedRenderbufferParameteriv)(GLuint renderbuffer, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glCreateTextures)(GLenum target, GLsizei n, GLuint * textures);
typedef GLvoid (GLAPI * PROC_glTextureBuffer)(GLuint texture, GLenum internalformat, GLuint buffer);
typedef GLvoid (GLAPI * PROC_glTextureBufferRange)(GLuint texture, GLenum internalformat, GLuint buffer, GLintptr offset, GLsizeiptr size);
typedef GLvoid (GLAPI * PROC_glTextureStorage1D)(GLuint texture, GLsizei levels, GLenum internalformat, GLsizei width);
typedef GLvoid (GLAPI * PROC_glTextureStorage2D)(GLuint texture, GLsizei levels, GLenum internalformat, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glTextureStorage3D)(GLuint texture, GLsizei levels, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth);
typedef GLvoid (GLAPI * PROC_glTextureStorage2DMultisample)(GLuint texture, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height, GLboolean fixedsamplelocations);
typedef GLvoid (GLAPI * PROC_glTextureStorage3DMultisample)(GLuint texture, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth, GLboolean fixedsamplelocations);
typedef GLvoid (GLAPI * PROC_glTextureSubImage1D)(GLuint texture, GLint level, GLint xoffset, GLsizei width, GLenum format, GLenum type, const GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glTextureSubImage2D)(GLuint texture, GLint level, GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format, GLenum type, const GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glTextureSubImage3D)(GLuint texture, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLenum type, const GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glCompressedTextureSubImage1D)(GLuint texture, GLint level, GLint xoffset, GLsizei width, GLenum format, GLsizei imageSize, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glCompressedTextureSubImage2D)(GLuint texture, GLint level, GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format, GLsizei imageSize, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glCompressedTextureSubImage3D)(GLuint texture, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLsizei imageSize, const GLvoid * data);
typedef GLvoid (GLAPI * PROC_glCopyTextureSubImage1D)(GLuint texture, GLint level, GLint xoffset, GLint x, GLint y, GLsizei width);
typedef GLvoid (GLAPI * PROC_glCopyTextureSubImage2D)(GLuint texture, GLint level, GLint xoffset, GLint yoffset, GLint x, GLint y, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glCopyTextureSubImage3D)(GLuint texture, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLint x, GLint y, GLsizei width, GLsizei height);
typedef GLvoid (GLAPI * PROC_glTextureParameterf)(GLuint texture, GLenum pname, GLfloat param);
typedef GLvoid (GLAPI * PROC_glTextureParameterfv)(GLuint texture, GLenum pname, const GLfloat * param);
typedef GLvoid (GLAPI * PROC_glTextureParameteri)(GLuint texture, GLenum pname, GLint param);
typedef GLvoid (GLAPI * PROC_glTextureParameterIiv)(GLuint texture, GLenum pname, const GLint * params);
typedef GLvoid (GLAPI * PROC_glTextureParameterIuiv)(GLuint texture, GLenum pname, const GLuint * params);
typedef GLvoid (GLAPI * PROC_glTextureParameteriv)(GLuint texture, GLenum pname, const GLint * param);
typedef GLvoid (GLAPI * PROC_glGenerateTextureMipmap)(GLuint texture);
typedef GLvoid (GLAPI * PROC_glBindTextureUnit)(GLuint unit, GLuint texture);
typedef GLvoid (GLAPI * PROC_glGetTextureImage)(GLuint texture, GLint level, GLenum format, GLenum type, GLsizei bufSize, GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glGetCompressedTextureImage)(GLuint texture, GLint level, GLsizei bufSize, GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glGetTextureLevelParameterfv)(GLuint texture, GLint level, GLenum pname, GLfloat * params);
typedef GLvoid (GLAPI * PROC_glGetTextureLevelParameteriv)(GLuint texture, GLint level, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetTextureParameterfv)(GLuint texture, GLenum pname, GLfloat * params);
typedef GLvoid (GLAPI * PROC_glGetTextureParameterIiv)(GLuint texture, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetTextureParameterIuiv)(GLuint texture, GLenum pname, GLuint * params);
typedef GLvoid (GLAPI * PROC_glGetTextureParameteriv)(GLuint texture, GLenum pname, GLint * params);
typedef GLvoid (GLAPI * PROC_glCreateVertexArrays)(GLsizei n, GLuint * arrays);
typedef GLvoid (GLAPI * PROC_glDisableVertexArrayAttrib)(GLuint vaobj, GLuint index);
typedef GLvoid (GLAPI * PROC_glEnableVertexArrayAttrib)(GLuint vaobj, GLuint index);
typedef GLvoid (GLAPI * PROC_glVertexArrayElementBuffer)(GLuint vaobj, GLuint buffer);
typedef GLvoid (GLAPI * PROC_glVertexArrayVertexBuffer)(GLuint vaobj, GLuint bindingindex, GLuint buffer, GLintptr offset, GLsizei stride);
typedef GLvoid (GLAPI * PROC_glVertexArrayVertexBuffers)(GLuint vaobj, GLuint first, GLsizei count, const GLuint * buffers, const GLintptr * offsets, const GLsizei * strides);
typedef GLvoid (GLAPI * PROC_glVertexArrayAttribBinding)(GLuint vaobj, GLuint attribindex, GLuint bindingindex);
typedef GLvoid (GLAPI * PROC_glVertexArrayAttribFormat)(GLuint vaobj, GLuint attribindex, GLint size, GLenum type, GLboolean normalized, GLuint relativeoffset);
typedef GLvoid (GLAPI * PROC_glVertexArrayAttribIFormat)(GLuint vaobj, GLuint attribindex, GLint size, GLenum type, GLuint relativeoffset);
typedef GLvoid (GLAPI * PROC_glVertexArrayAttribLFormat)(GLuint vaobj, GLuint attribindex, GLint size, GLenum type, GLuint relativeoffset);
typedef GLvoid (GLAPI * PROC_glVertexArrayBindingDivisor)(GLuint vaobj, GLuint bindingindex, GLuint divisor);
typedef GLvoid (GLAPI * PROC_glGetVertexArrayiv)(GLuint vaobj, GLenum pname, GLint * param);
typedef GLvoid (GLAPI * PROC_glGetVertexArrayIndexediv)(GLuint vaobj, GLuint index, GLenum pname, GLint * param);
typedef GLvoid (GLAPI * PROC_glGetVertexArrayIndexed64iv)(GLuint vaobj, GLuint index, GLenum pname, GLint64 * param);
typedef GLvoid (GLAPI * PROC_glCreateSamplers)(GLsizei n, GLuint * samplers);
typedef GLvoid (GLAPI * PROC_glCreateProgramPipelines)(GLsizei n, GLuint * pipelines);
typedef GLvoid (GLAPI * PROC_glCreateQueries)(GLenum target, GLsizei n, GLuint * ids);
typedef GLvoid (GLAPI * PROC_glGetQueryBufferObjecti64v)(GLuint id, GLuint buffer, GLenum pname, GLintptr offset);
typedef GLvoid (GLAPI * PROC_glGetQueryBufferObjectiv)(GLuint id, GLuint buffer, GLenum pname, GLintptr offset);
typedef GLvoid (GLAPI * PROC_glGetQueryBufferObjectui64v)(GLuint id, GLuint buffer, GLenum pname, GLintptr offset);
typedef GLvoid (GLAPI * PROC_glGetQueryBufferObjectuiv)(GLuint id, GLuint buffer, GLenum pname, GLintptr offset);
typedef GLvoid (GLAPI * PROC_glMemoryBarrierByRegion)(GLbitfield barriers);
typedef GLvoid (GLAPI * PROC_glGetTextureSubImage)(GLuint texture, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLenum type, GLsizei bufSize, GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glGetCompressedTextureSubImage)(GLuint texture, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLsizei bufSize, GLvoid * pixels);
typedef GLenum (GLAPI * PROC_glGetGraphicsResetStatus)();
typedef GLvoid (GLAPI * PROC_glGetnCompressedTexImage)(GLenum target, GLint lod, GLsizei bufSize, GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glGetnTexImage)(GLenum target, GLint level, GLenum format, GLenum type, GLsizei bufSize, GLvoid * pixels);
typedef GLvoid (GLAPI * PROC_glGetnUniformdv)(GLuint program, GLint location, GLsizei bufSize, GLdouble * params);
typedef GLvoid (GLAPI * PROC_glGetnUniformfv)(GLuint program, GLint location, GLsizei bufSize, GLfloat * params);
typedef GLvoid (GLAPI * PROC_glGetnUniformiv)(GLuint program, GLint location, GLsizei bufSize, GLint * params);
typedef GLvoid (GLAPI * PROC_glGetnUniformuiv)(GLuint program, GLint location, GLsizei bufSize, GLuint * params);
typedef GLvoid (GLAPI * PROC_glReadnPixels)(GLint x, GLint y, GLsizei width, GLsizei height, GLenum format, GLenum type, GLsizei bufSize, GLvoid * data);
typedef GLvoid (GLAPI * PROC_glTextureBarrier)();

#define GL_DEPTH_BUFFER_BIT                                           0x0100
#define GL_STENCIL_BUFFER_BIT                                         0x0400
#define GL_COLOR_BUFFER_BIT                                           0x4000
#define GL_FALSE                                                      0x0000
#define GL_TRUE                                                       0x0001
#define GL_POINTS                                                     0x0000
#define GL_LINES                                                      0x0001
#define GL_LINE_LOOP                                                  0x0002
#define GL_LINE_STRIP                                                 0x0003
#define GL_TRIANGLES                                                  0x0004
#define GL_TRIANGLE_STRIP                                             0x0005
#define GL_TRIANGLE_FAN                                               0x0006
#define GL_QUADS                                                      0x0007
#define GL_NEVER                                                      0x0200
#define GL_LESS                                                       0x0201
#define GL_EQUAL                                                      0x0202
#define GL_LEQUAL                                                     0x0203
#define GL_GREATER                                                    0x0204
#define GL_NOTEQUAL                                                   0x0205
#define GL_GEQUAL                                                     0x0206
#define GL_ALWAYS                                                     0x0207
#define GL_ZERO                                                       0x0000
#define GL_ONE                                                        0x0001
#define GL_SRC_COLOR                                                  0x0300
#define GL_ONE_MINUS_SRC_COLOR                                        0x0301
#define GL_SRC_ALPHA                                                  0x0302
#define GL_ONE_MINUS_SRC_ALPHA                                        0x0303
#define GL_DST_ALPHA                                                  0x0304
#define GL_ONE_MINUS_DST_ALPHA                                        0x0305
#define GL_DST_COLOR                                                  0x0306
#define GL_ONE_MINUS_DST_COLOR                                        0x0307
#define GL_SRC_ALPHA_SATURATE                                         0x0308
#define GL_NONE                                                       0x0000
#define GL_FRONT_LEFT                                                 0x0400
#define GL_FRONT_RIGHT                                                0x0401
#define GL_BACK_LEFT                                                  0x0402
#define GL_BACK_RIGHT                                                 0x0403
#define GL_FRONT                                                      0x0404
#define GL_BACK                                                       0x0405
#define GL_LEFT                                                       0x0406
#define GL_RIGHT                                                      0x0407
#define GL_FRONT_AND_BACK                                             0x0408
#define GL_NO_ERROR                                                   0x0000
#define GL_INVALID_ENUM                                               0x0500
#define GL_INVALID_VALUE                                              0x0501
#define GL_INVALID_OPERATION                                          0x0502
#define GL_OUT_OF_MEMORY                                              0x0505
#define GL_CW                                                         0x0900
#define GL_CCW                                                        0x0901
#define GL_POINT_SIZE                                                 0x0B11
#define GL_POINT_SIZE_RANGE                                           0x0B12
#define GL_POINT_SIZE_GRANULARITY                                     0x0B13
#define GL_LINE_SMOOTH                                                0x0B20
#define GL_LINE_WIDTH                                                 0x0B21
#define GL_LINE_WIDTH_RANGE                                           0x0B22
#define GL_LINE_WIDTH_GRANULARITY                                     0x0B23
#define GL_POLYGON_MODE                                               0x0B40
#define GL_POLYGON_SMOOTH                                             0x0B41
#define GL_CULL_FACE                                                  0x0B44
#define GL_CULL_FACE_MODE                                             0x0B45
#define GL_FRONT_FACE                                                 0x0B46
#define GL_DEPTH_RANGE                                                0x0B70
#define GL_DEPTH_TEST                                                 0x0B71
#define GL_DEPTH_WRITEMASK                                            0x0B72
#define GL_DEPTH_CLEAR_VALUE                                          0x0B73
#define GL_DEPTH_FUNC                                                 0x0B74
#define GL_STENCIL_TEST                                               0x0B90
#define GL_STENCIL_CLEAR_VALUE                                        0x0B91
#define GL_STENCIL_FUNC                                               0x0B92
#define GL_STENCIL_VALUE_MASK                                         0x0B93
#define GL_STENCIL_FAIL                                               0x0B94
#define GL_STENCIL_PASS_DEPTH_FAIL                                    0x0B95
#define GL_STENCIL_PASS_DEPTH_PASS                                    0x0B96
#define GL_STENCIL_REF                                                0x0B97
#define GL_STENCIL_WRITEMASK                                          0x0B98
#define GL_VIEWPORT                                                   0x0BA2
#define GL_DITHER                                                     0x0BD0
#define GL_BLEND_DST                                                  0x0BE0
#define GL_BLEND_SRC                                                  0x0BE1
#define GL_BLEND                                                      0x0BE2
#define GL_LOGIC_OP_MODE                                              0x0BF0
#define GL_COLOR_LOGIC_OP                                             0x0BF2
#define GL_DRAW_BUFFER                                                0x0C01
#define GL_READ_BUFFER                                                0x0C02
#define GL_SCISSOR_BOX                                                0x0C10
#define GL_SCISSOR_TEST                                               0x0C11
#define GL_COLOR_CLEAR_VALUE                                          0x0C22
#define GL_COLOR_WRITEMASK                                            0x0C23
#define GL_DOUBLEBUFFER                                               0x0C32
#define GL_STEREO                                                     0x0C33
#define GL_LINE_SMOOTH_HINT                                           0x0C52
#define GL_POLYGON_SMOOTH_HINT                                        0x0C53
#define GL_UNPACK_SWAP_BYTES                                          0x0CF0
#define GL_UNPACK_LSB_FIRST                                           0x0CF1
#define GL_UNPACK_ROW_LENGTH                                          0x0CF2
#define GL_UNPACK_SKIP_ROWS                                           0x0CF3
#define GL_UNPACK_SKIP_PIXELS                                         0x0CF4
#define GL_UNPACK_ALIGNMENT                                           0x0CF5
#define GL_PACK_SWAP_BYTES                                            0x0D00
#define GL_PACK_LSB_FIRST                                             0x0D01
#define GL_PACK_ROW_LENGTH                                            0x0D02
#define GL_PACK_SKIP_ROWS                                             0x0D03
#define GL_PACK_SKIP_PIXELS                                           0x0D04
#define GL_PACK_ALIGNMENT                                             0x0D05
#define GL_MAX_TEXTURE_SIZE                                           0x0D33
#define GL_MAX_VIEWPORT_DIMS                                          0x0D3A
#define GL_SUBPIXEL_BITS                                              0x0D50
#define GL_TEXTURE_1D                                                 0x0DE0
#define GL_TEXTURE_2D                                                 0x0DE1
#define GL_POLYGON_OFFSET_UNITS                                       0x2A00
#define GL_POLYGON_OFFSET_POINT                                       0x2A01
#define GL_POLYGON_OFFSET_LINE                                        0x2A02
#define GL_POLYGON_OFFSET_FILL                                        0x8037
#define GL_POLYGON_OFFSET_FACTOR                                      0x8038
#define GL_TEXTURE_BINDING_1D                                         0x8068
#define GL_TEXTURE_BINDING_2D                                         0x8069
#define GL_TEXTURE_WIDTH                                              0x1000
#define GL_TEXTURE_HEIGHT                                             0x1001
#define GL_TEXTURE_INTERNAL_FORMAT                                    0x1003
#define GL_TEXTURE_BORDER_COLOR                                       0x1004
#define GL_TEXTURE_RED_SIZE                                           0x805C
#define GL_TEXTURE_GREEN_SIZE                                         0x805D
#define GL_TEXTURE_BLUE_SIZE                                          0x805E
#define GL_TEXTURE_ALPHA_SIZE                                         0x805F
#define GL_DONT_CARE                                                  0x1100
#define GL_FASTEST                                                    0x1101
#define GL_NICEST                                                     0x1102
#define GL_BYTE                                                       0x1400
#define GL_UNSIGNED_BYTE                                              0x1401
#define GL_SHORT                                                      0x1402
#define GL_UNSIGNED_SHORT                                             0x1403
#define GL_INT                                                        0x1404
#define GL_UNSIGNED_INT                                               0x1405
#define GL_FLOAT                                                      0x1406
#define GL_DOUBLE                                                     0x140A
#define GL_STACK_OVERFLOW                                             0x0503
#define GL_STACK_UNDERFLOW                                            0x0504
#define GL_CLEAR                                                      0x1500
#define GL_AND                                                        0x1501
#define GL_AND_REVERSE                                                0x1502
#define GL_COPY                                                       0x1503
#define GL_AND_INVERTED                                               0x1504
#define GL_NOOP                                                       0x1505
#define GL_XOR                                                        0x1506
#define GL_OR                                                         0x1507
#define GL_NOR                                                        0x1508
#define GL_EQUIV                                                      0x1509
#define GL_INVERT                                                     0x150A
#define GL_OR_REVERSE                                                 0x150B
#define GL_COPY_INVERTED                                              0x150C
#define GL_OR_INVERTED                                                0x150D
#define GL_NAND                                                       0x150E
#define GL_SET                                                        0x150F
#define GL_TEXTURE                                                    0x1702
#define GL_COLOR                                                      0x1800
#define GL_DEPTH                                                      0x1801
#define GL_STENCIL                                                    0x1802
#define GL_STENCIL_INDEX                                              0x1901
#define GL_DEPTH_COMPONENT                                            0x1902
#define GL_RED                                                        0x1903
#define GL_GREEN                                                      0x1904
#define GL_BLUE                                                       0x1905
#define GL_ALPHA                                                      0x1906
#define GL_RGB                                                        0x1907
#define GL_RGBA                                                       0x1908
#define GL_POINT                                                      0x1B00
#define GL_LINE                                                       0x1B01
#define GL_FILL                                                       0x1B02
#define GL_KEEP                                                       0x1E00
#define GL_REPLACE                                                    0x1E01
#define GL_INCR                                                       0x1E02
#define GL_DECR                                                       0x1E03
#define GL_VENDOR                                                     0x1F00
#define GL_RENDERER                                                   0x1F01
#define GL_VERSION                                                    0x1F02
#define GL_EXTENSIONS                                                 0x1F03
#define GL_NEAREST                                                    0x2600
#define GL_LINEAR                                                     0x2601
#define GL_NEAREST_MIPMAP_NEAREST                                     0x2700
#define GL_LINEAR_MIPMAP_NEAREST                                      0x2701
#define GL_NEAREST_MIPMAP_LINEAR                                      0x2702
#define GL_LINEAR_MIPMAP_LINEAR                                       0x2703
#define GL_TEXTURE_MAG_FILTER                                         0x2800
#define GL_TEXTURE_MIN_FILTER                                         0x2801
#define GL_TEXTURE_WRAP_S                                             0x2802
#define GL_TEXTURE_WRAP_T                                             0x2803
#define GL_PROXY_TEXTURE_1D                                           0x8063
#define GL_PROXY_TEXTURE_2D                                           0x8064
#define GL_REPEAT                                                     0x2901
#define GL_R3_G3_B2                                                   0x2A10
#define GL_RGB4                                                       0x804F
#define GL_RGB5                                                       0x8050
#define GL_RGB8                                                       0x8051
#define GL_RGB10                                                      0x8052
#define GL_RGB12                                                      0x8053
#define GL_RGB16                                                      0x8054
#define GL_RGBA2                                                      0x8055
#define GL_RGBA4                                                      0x8056
#define GL_RGB5_A1                                                    0x8057
#define GL_RGBA8                                                      0x8058
#define GL_RGB10_A2                                                   0x8059
#define GL_RGBA12                                                     0x805A
#define GL_RGBA16                                                     0x805B
#define GL_VERTEX_ARRAY                                               0x8074
#define GL_UNSIGNED_BYTE_3_3_2                                        0x8032
#define GL_UNSIGNED_SHORT_4_4_4_4                                     0x8033
#define GL_UNSIGNED_SHORT_5_5_5_1                                     0x8034
#define GL_UNSIGNED_INT_8_8_8_8                                       0x8035
#define GL_UNSIGNED_INT_10_10_10_2                                    0x8036
#define GL_TEXTURE_BINDING_3D                                         0x806A
#define GL_PACK_SKIP_IMAGES                                           0x806B
#define GL_PACK_IMAGE_HEIGHT                                          0x806C
#define GL_UNPACK_SKIP_IMAGES                                         0x806D
#define GL_UNPACK_IMAGE_HEIGHT                                        0x806E
#define GL_TEXTURE_3D                                                 0x806F
#define GL_PROXY_TEXTURE_3D                                           0x8070
#define GL_TEXTURE_DEPTH                                              0x8071
#define GL_TEXTURE_WRAP_R                                             0x8072
#define GL_MAX_3D_TEXTURE_SIZE                                        0x8073
#define GL_UNSIGNED_BYTE_2_3_3_REV                                    0x8362
#define GL_UNSIGNED_SHORT_5_6_5                                       0x8363
#define GL_UNSIGNED_SHORT_5_6_5_REV                                   0x8364
#define GL_UNSIGNED_SHORT_4_4_4_4_REV                                 0x8365
#define GL_UNSIGNED_SHORT_1_5_5_5_REV                                 0x8366
#define GL_UNSIGNED_INT_8_8_8_8_REV                                   0x8367
#define GL_UNSIGNED_INT_2_10_10_10_REV                                0x8368
#define GL_BGR                                                        0x80E0
#define GL_BGRA                                                       0x80E1
#define GL_MAX_ELEMENTS_VERTICES                                      0x80E8
#define GL_MAX_ELEMENTS_INDICES                                       0x80E9
#define GL_CLAMP_TO_EDGE                                              0x812F
#define GL_TEXTURE_MIN_LOD                                            0x813A
#define GL_TEXTURE_MAX_LOD                                            0x813B
#define GL_TEXTURE_BASE_LEVEL                                         0x813C
#define GL_TEXTURE_MAX_LEVEL                                          0x813D
#define GL_SMOOTH_POINT_SIZE_RANGE                                    0x0B12
#define GL_SMOOTH_POINT_SIZE_GRANULARITY                              0x0B13
#define GL_SMOOTH_LINE_WIDTH_RANGE                                    0x0B22
#define GL_SMOOTH_LINE_WIDTH_GRANULARITY                              0x0B23
#define GL_ALIASED_LINE_WIDTH_RANGE                                   0x846E
#define GL_TEXTURE0                                                   0x84C0
#define GL_TEXTURE1                                                   0x84C1
#define GL_TEXTURE2                                                   0x84C2
#define GL_TEXTURE3                                                   0x84C3
#define GL_TEXTURE4                                                   0x84C4
#define GL_TEXTURE5                                                   0x84C5
#define GL_TEXTURE6                                                   0x84C6
#define GL_TEXTURE7                                                   0x84C7
#define GL_TEXTURE8                                                   0x84C8
#define GL_TEXTURE9                                                   0x84C9
#define GL_TEXTURE10                                                  0x84CA
#define GL_TEXTURE11                                                  0x84CB
#define GL_TEXTURE12                                                  0x84CC
#define GL_TEXTURE13                                                  0x84CD
#define GL_TEXTURE14                                                  0x84CE
#define GL_TEXTURE15                                                  0x84CF
#define GL_TEXTURE16                                                  0x84D0
#define GL_TEXTURE17                                                  0x84D1
#define GL_TEXTURE18                                                  0x84D2
#define GL_TEXTURE19                                                  0x84D3
#define GL_TEXTURE20                                                  0x84D4
#define GL_TEXTURE21                                                  0x84D5
#define GL_TEXTURE22                                                  0x84D6
#define GL_TEXTURE23                                                  0x84D7
#define GL_TEXTURE24                                                  0x84D8
#define GL_TEXTURE25                                                  0x84D9
#define GL_TEXTURE26                                                  0x84DA
#define GL_TEXTURE27                                                  0x84DB
#define GL_TEXTURE28                                                  0x84DC
#define GL_TEXTURE29                                                  0x84DD
#define GL_TEXTURE30                                                  0x84DE
#define GL_TEXTURE31                                                  0x84DF
#define GL_ACTIVE_TEXTURE                                             0x84E0
#define GL_MULTISAMPLE                                                0x809D
#define GL_SAMPLE_ALPHA_TO_COVERAGE                                   0x809E
#define GL_SAMPLE_ALPHA_TO_ONE                                        0x809F
#define GL_SAMPLE_COVERAGE                                            0x80A0
#define GL_SAMPLE_BUFFERS                                             0x80A8
#define GL_SAMPLES                                                    0x80A9
#define GL_SAMPLE_COVERAGE_VALUE                                      0x80AA
#define GL_SAMPLE_COVERAGE_INVERT                                     0x80AB
#define GL_TEXTURE_CUBE_MAP                                           0x8513
#define GL_TEXTURE_BINDING_CUBE_MAP                                   0x8514
#define GL_TEXTURE_CUBE_MAP_POSITIVE_X                                0x8515
#define GL_TEXTURE_CUBE_MAP_NEGATIVE_X                                0x8516
#define GL_TEXTURE_CUBE_MAP_POSITIVE_Y                                0x8517
#define GL_TEXTURE_CUBE_MAP_NEGATIVE_Y                                0x8518
#define GL_TEXTURE_CUBE_MAP_POSITIVE_Z                                0x8519
#define GL_TEXTURE_CUBE_MAP_NEGATIVE_Z                                0x851A
#define GL_PROXY_TEXTURE_CUBE_MAP                                     0x851B
#define GL_MAX_CUBE_MAP_TEXTURE_SIZE                                  0x851C
#define GL_COMPRESSED_RGB                                             0x84ED
#define GL_COMPRESSED_RGBA                                            0x84EE
#define GL_TEXTURE_COMPRESSION_HINT                                   0x84EF
#define GL_TEXTURE_COMPRESSED_IMAGE_SIZE                              0x86A0
#define GL_TEXTURE_COMPRESSED                                         0x86A1
#define GL_NUM_COMPRESSED_TEXTURE_FORMATS                             0x86A2
#define GL_COMPRESSED_TEXTURE_FORMATS                                 0x86A3
#define GL_CLAMP_TO_BORDER                                            0x812D
#define GL_BLEND_DST_RGB                                              0x80C8
#define GL_BLEND_SRC_RGB                                              0x80C9
#define GL_BLEND_DST_ALPHA                                            0x80CA
#define GL_BLEND_SRC_ALPHA                                            0x80CB
#define GL_POINT_FADE_THRESHOLD_SIZE                                  0x8128
#define GL_DEPTH_COMPONENT16                                          0x81A5
#define GL_DEPTH_COMPONENT24                                          0x81A6
#define GL_DEPTH_COMPONENT32                                          0x81A7
#define GL_MIRRORED_REPEAT                                            0x8370
#define GL_MAX_TEXTURE_LOD_BIAS                                       0x84FD
#define GL_TEXTURE_LOD_BIAS                                           0x8501
#define GL_INCR_WRAP                                                  0x8507
#define GL_DECR_WRAP                                                  0x8508
#define GL_TEXTURE_DEPTH_SIZE                                         0x884A
#define GL_TEXTURE_COMPARE_MODE                                       0x884C
#define GL_TEXTURE_COMPARE_FUNC                                       0x884D
#define GL_FUNC_ADD                                                   0x8006
#define GL_FUNC_SUBTRACT                                              0x800A
#define GL_FUNC_REVERSE_SUBTRACT                                      0x800B
#define GL_MIN                                                        0x8007
#define GL_MAX                                                        0x8008
#define GL_CONSTANT_COLOR                                             0x8001
#define GL_ONE_MINUS_CONSTANT_COLOR                                   0x8002
#define GL_CONSTANT_ALPHA                                             0x8003
#define GL_ONE_MINUS_CONSTANT_ALPHA                                   0x8004
#define GL_BUFFER_SIZE                                                0x8764
#define GL_BUFFER_USAGE                                               0x8765
#define GL_QUERY_COUNTER_BITS                                         0x8864
#define GL_CURRENT_QUERY                                              0x8865
#define GL_QUERY_RESULT                                               0x8866
#define GL_QUERY_RESULT_AVAILABLE                                     0x8867
#define GL_ARRAY_BUFFER                                               0x8892
#define GL_ELEMENT_ARRAY_BUFFER                                       0x8893
#define GL_ARRAY_BUFFER_BINDING                                       0x8894
#define GL_ELEMENT_ARRAY_BUFFER_BINDING                               0x8895
#define GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING                         0x889F
#define GL_READ_ONLY                                                  0x88B8
#define GL_WRITE_ONLY                                                 0x88B9
#define GL_READ_WRITE                                                 0x88BA
#define GL_BUFFER_ACCESS                                              0x88BB
#define GL_BUFFER_MAPPED                                              0x88BC
#define GL_BUFFER_MAP_POINTER                                         0x88BD
#define GL_STREAM_DRAW                                                0x88E0
#define GL_STREAM_READ                                                0x88E1
#define GL_STREAM_COPY                                                0x88E2
#define GL_STATIC_DRAW                                                0x88E4
#define GL_STATIC_READ                                                0x88E5
#define GL_STATIC_COPY                                                0x88E6
#define GL_DYNAMIC_DRAW                                               0x88E8
#define GL_DYNAMIC_READ                                               0x88E9
#define GL_DYNAMIC_COPY                                               0x88EA
#define GL_SAMPLES_PASSED                                             0x8914
#define GL_SRC1_ALPHA                                                 0x8589
#define GL_BLEND_EQUATION_RGB                                         0x8009
#define GL_VERTEX_ATTRIB_ARRAY_ENABLED                                0x8622
#define GL_VERTEX_ATTRIB_ARRAY_SIZE                                   0x8623
#define GL_VERTEX_ATTRIB_ARRAY_STRIDE                                 0x8624
#define GL_VERTEX_ATTRIB_ARRAY_TYPE                                   0x8625
#define GL_CURRENT_VERTEX_ATTRIB                                      0x8626
#define GL_VERTEX_PROGRAM_POINT_SIZE                                  0x8642
#define GL_VERTEX_ATTRIB_ARRAY_POINTER                                0x8645
#define GL_STENCIL_BACK_FUNC                                          0x8800
#define GL_STENCIL_BACK_FAIL                                          0x8801
#define GL_STENCIL_BACK_PASS_DEPTH_FAIL                               0x8802
#define GL_STENCIL_BACK_PASS_DEPTH_PASS                               0x8803
#define GL_MAX_DRAW_BUFFERS                                           0x8824
#define GL_DRAW_BUFFER0                                               0x8825
#define GL_DRAW_BUFFER1                                               0x8826
#define GL_DRAW_BUFFER2                                               0x8827
#define GL_DRAW_BUFFER3                                               0x8828
#define GL_DRAW_BUFFER4                                               0x8829
#define GL_DRAW_BUFFER5                                               0x882A
#define GL_DRAW_BUFFER6                                               0x882B
#define GL_DRAW_BUFFER7                                               0x882C
#define GL_DRAW_BUFFER8                                               0x882D
#define GL_DRAW_BUFFER9                                               0x882E
#define GL_DRAW_BUFFER10                                              0x882F
#define GL_DRAW_BUFFER11                                              0x8830
#define GL_DRAW_BUFFER12                                              0x8831
#define GL_DRAW_BUFFER13                                              0x8832
#define GL_DRAW_BUFFER14                                              0x8833
#define GL_DRAW_BUFFER15                                              0x8834
#define GL_BLEND_EQUATION_ALPHA                                       0x883D
#define GL_MAX_VERTEX_ATTRIBS                                         0x8869
#define GL_VERTEX_ATTRIB_ARRAY_NORMALIZED                             0x886A
#define GL_MAX_TEXTURE_IMAGE_UNITS                                    0x8872
#define GL_FRAGMENT_SHADER                                            0x8B30
#define GL_VERTEX_SHADER                                              0x8B31
#define GL_MAX_FRAGMENT_UNIFORM_COMPONENTS                            0x8B49
#define GL_MAX_VERTEX_UNIFORM_COMPONENTS                              0x8B4A
#define GL_MAX_VARYING_FLOATS                                         0x8B4B
#define GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS                             0x8B4C
#define GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS                           0x8B4D
#define GL_SHADER_TYPE                                                0x8B4F
#define GL_FLOAT_VEC2                                                 0x8B50
#define GL_FLOAT_VEC3                                                 0x8B51
#define GL_FLOAT_VEC4                                                 0x8B52
#define GL_INT_VEC2                                                   0x8B53
#define GL_INT_VEC3                                                   0x8B54
#define GL_INT_VEC4                                                   0x8B55
#define GL_BOOL                                                       0x8B56
#define GL_BOOL_VEC2                                                  0x8B57
#define GL_BOOL_VEC3                                                  0x8B58
#define GL_BOOL_VEC4                                                  0x8B59
#define GL_FLOAT_MAT2                                                 0x8B5A
#define GL_FLOAT_MAT3                                                 0x8B5B
#define GL_FLOAT_MAT4                                                 0x8B5C
#define GL_SAMPLER_1D                                                 0x8B5D
#define GL_SAMPLER_2D                                                 0x8B5E
#define GL_SAMPLER_3D                                                 0x8B5F
#define GL_SAMPLER_CUBE                                               0x8B60
#define GL_SAMPLER_1D_SHADOW                                          0x8B61
#define GL_SAMPLER_2D_SHADOW                                          0x8B62
#define GL_DELETE_STATUS                                              0x8B80
#define GL_COMPILE_STATUS                                             0x8B81
#define GL_LINK_STATUS                                                0x8B82
#define GL_VALIDATE_STATUS                                            0x8B83
#define GL_INFO_LOG_LENGTH                                            0x8B84
#define GL_ATTACHED_SHADERS                                           0x8B85
#define GL_ACTIVE_UNIFORMS                                            0x8B86
#define GL_ACTIVE_UNIFORM_MAX_LENGTH                                  0x8B87
#define GL_SHADER_SOURCE_LENGTH                                       0x8B88
#define GL_ACTIVE_ATTRIBUTES                                          0x8B89
#define GL_ACTIVE_ATTRIBUTE_MAX_LENGTH                                0x8B8A
#define GL_FRAGMENT_SHADER_DERIVATIVE_HINT                            0x8B8B
#define GL_SHADING_LANGUAGE_VERSION                                   0x8B8C
#define GL_CURRENT_PROGRAM                                            0x8B8D
#define GL_POINT_SPRITE_COORD_ORIGIN                                  0x8CA0
#define GL_LOWER_LEFT                                                 0x8CA1
#define GL_UPPER_LEFT                                                 0x8CA2
#define GL_STENCIL_BACK_REF                                           0x8CA3
#define GL_STENCIL_BACK_VALUE_MASK                                    0x8CA4
#define GL_STENCIL_BACK_WRITEMASK                                     0x8CA5
#define GL_PIXEL_PACK_BUFFER                                          0x88EB
#define GL_PIXEL_UNPACK_BUFFER                                        0x88EC
#define GL_PIXEL_PACK_BUFFER_BINDING                                  0x88ED
#define GL_PIXEL_UNPACK_BUFFER_BINDING                                0x88EF
#define GL_FLOAT_MAT2x3                                               0x8B65
#define GL_FLOAT_MAT2x4                                               0x8B66
#define GL_FLOAT_MAT3x2                                               0x8B67
#define GL_FLOAT_MAT3x4                                               0x8B68
#define GL_FLOAT_MAT4x2                                               0x8B69
#define GL_FLOAT_MAT4x3                                               0x8B6A
#define GL_SRGB                                                       0x8C40
#define GL_SRGB8                                                      0x8C41
#define GL_SRGB_ALPHA                                                 0x8C42
#define GL_SRGB8_ALPHA8                                               0x8C43
#define GL_COMPRESSED_SRGB                                            0x8C48
#define GL_COMPRESSED_SRGB_ALPHA                                      0x8C49
#define GL_COMPARE_REF_TO_TEXTURE                                     0x884E
#define GL_CLIP_DISTANCE0                                             0x3000
#define GL_CLIP_DISTANCE1                                             0x3001
#define GL_CLIP_DISTANCE2                                             0x3002
#define GL_CLIP_DISTANCE3                                             0x3003
#define GL_CLIP_DISTANCE4                                             0x3004
#define GL_CLIP_DISTANCE5                                             0x3005
#define GL_CLIP_DISTANCE6                                             0x3006
#define GL_CLIP_DISTANCE7                                             0x3007
#define GL_MAX_CLIP_DISTANCES                                         0x0D32
#define GL_MAJOR_VERSION                                              0x821B
#define GL_MINOR_VERSION                                              0x821C
#define GL_NUM_EXTENSIONS                                             0x821D
#define GL_CONTEXT_FLAGS                                              0x821E
#define GL_COMPRESSED_RED                                             0x8225
#define GL_COMPRESSED_RG                                              0x8226
#define GL_CONTEXT_FLAG_FORWARD_COMPATIBLE_BIT                        0x0001
#define GL_RGBA32F                                                    0x8814
#define GL_RGB32F                                                     0x8815
#define GL_RGBA16F                                                    0x881A
#define GL_RGB16F                                                     0x881B
#define GL_VERTEX_ATTRIB_ARRAY_INTEGER                                0x88FD
#define GL_MAX_ARRAY_TEXTURE_LAYERS                                   0x88FF
#define GL_MIN_PROGRAM_TEXEL_OFFSET                                   0x8904
#define GL_MAX_PROGRAM_TEXEL_OFFSET                                   0x8905
#define GL_CLAMP_READ_COLOR                                           0x891C
#define GL_FIXED_ONLY                                                 0x891D
#define GL_MAX_VARYING_COMPONENTS                                     0x8B4B
#define GL_TEXTURE_1D_ARRAY                                           0x8C18
#define GL_PROXY_TEXTURE_1D_ARRAY                                     0x8C19
#define GL_TEXTURE_2D_ARRAY                                           0x8C1A
#define GL_PROXY_TEXTURE_2D_ARRAY                                     0x8C1B
#define GL_TEXTURE_BINDING_1D_ARRAY                                   0x8C1C
#define GL_TEXTURE_BINDING_2D_ARRAY                                   0x8C1D
#define GL_R11F_G11F_B10F                                             0x8C3A
#define GL_UNSIGNED_INT_10F_11F_11F_REV                               0x8C3B
#define GL_RGB9_E5                                                    0x8C3D
#define GL_UNSIGNED_INT_5_9_9_9_REV                                   0x8C3E
#define GL_TEXTURE_SHARED_SIZE                                        0x8C3F
#define GL_TRANSFORM_FEEDBACK_VARYING_MAX_LENGTH                      0x8C76
#define GL_TRANSFORM_FEEDBACK_BUFFER_MODE                             0x8C7F
#define GL_MAX_TRANSFORM_FEEDBACK_SEPARATE_COMPONENTS                 0x8C80
#define GL_TRANSFORM_FEEDBACK_VARYINGS                                0x8C83
#define GL_TRANSFORM_FEEDBACK_BUFFER_START                            0x8C84
#define GL_TRANSFORM_FEEDBACK_BUFFER_SIZE                             0x8C85
#define GL_PRIMITIVES_GENERATED                                       0x8C87
#define GL_TRANSFORM_FEEDBACK_PRIMITIVES_WRITTEN                      0x8C88
#define GL_RASTERIZER_DISCARD                                         0x8C89
#define GL_MAX_TRANSFORM_FEEDBACK_INTERLEAVED_COMPONENTS              0x8C8A
#define GL_MAX_TRANSFORM_FEEDBACK_SEPARATE_ATTRIBS                    0x8C8B
#define GL_INTERLEAVED_ATTRIBS                                        0x8C8C
#define GL_SEPARATE_ATTRIBS                                           0x8C8D
#define GL_TRANSFORM_FEEDBACK_BUFFER                                  0x8C8E
#define GL_TRANSFORM_FEEDBACK_BUFFER_BINDING                          0x8C8F
#define GL_RGBA32UI                                                   0x8D70
#define GL_RGB32UI                                                    0x8D71
#define GL_RGBA16UI                                                   0x8D76
#define GL_RGB16UI                                                    0x8D77
#define GL_RGBA8UI                                                    0x8D7C
#define GL_RGB8UI                                                     0x8D7D
#define GL_RGBA32I                                                    0x8D82
#define GL_RGB32I                                                     0x8D83
#define GL_RGBA16I                                                    0x8D88
#define GL_RGB16I                                                     0x8D89
#define GL_RGBA8I                                                     0x8D8E
#define GL_RGB8I                                                      0x8D8F
#define GL_RED_INTEGER                                                0x8D94
#define GL_GREEN_INTEGER                                              0x8D95
#define GL_BLUE_INTEGER                                               0x8D96
#define GL_RGB_INTEGER                                                0x8D98
#define GL_RGBA_INTEGER                                               0x8D99
#define GL_BGR_INTEGER                                                0x8D9A
#define GL_BGRA_INTEGER                                               0x8D9B
#define GL_SAMPLER_1D_ARRAY                                           0x8DC0
#define GL_SAMPLER_2D_ARRAY                                           0x8DC1
#define GL_SAMPLER_1D_ARRAY_SHADOW                                    0x8DC3
#define GL_SAMPLER_2D_ARRAY_SHADOW                                    0x8DC4
#define GL_SAMPLER_CUBE_SHADOW                                        0x8DC5
#define GL_UNSIGNED_INT_VEC2                                          0x8DC6
#define GL_UNSIGNED_INT_VEC3                                          0x8DC7
#define GL_UNSIGNED_INT_VEC4                                          0x8DC8
#define GL_INT_SAMPLER_1D                                             0x8DC9
#define GL_INT_SAMPLER_2D                                             0x8DCA
#define GL_INT_SAMPLER_3D                                             0x8DCB
#define GL_INT_SAMPLER_CUBE                                           0x8DCC
#define GL_INT_SAMPLER_1D_ARRAY                                       0x8DCE
#define GL_INT_SAMPLER_2D_ARRAY                                       0x8DCF
#define GL_UNSIGNED_INT_SAMPLER_1D                                    0x8DD1
#define GL_UNSIGNED_INT_SAMPLER_2D                                    0x8DD2
#define GL_UNSIGNED_INT_SAMPLER_3D                                    0x8DD3
#define GL_UNSIGNED_INT_SAMPLER_CUBE                                  0x8DD4
#define GL_UNSIGNED_INT_SAMPLER_1D_ARRAY                              0x8DD6
#define GL_UNSIGNED_INT_SAMPLER_2D_ARRAY                              0x8DD7
#define GL_QUERY_WAIT                                                 0x8E13
#define GL_QUERY_NO_WAIT                                              0x8E14
#define GL_QUERY_BY_REGION_WAIT                                       0x8E15
#define GL_QUERY_BY_REGION_NO_WAIT                                    0x8E16
#define GL_BUFFER_ACCESS_FLAGS                                        0x911F
#define GL_BUFFER_MAP_LENGTH                                          0x9120
#define GL_BUFFER_MAP_OFFSET                                          0x9121
#define GL_DEPTH_COMPONENT32F                                         0x8CAC
#define GL_DEPTH32F_STENCIL8                                          0x8CAD
#define GL_FLOAT_32_UNSIGNED_INT_24_8_REV                             0x8DAD
#define GL_INVALID_FRAMEBUFFER_OPERATION                              0x0506
#define GL_FRAMEBUFFER_ATTACHMENT_COLOR_ENCODING                      0x8210
#define GL_FRAMEBUFFER_ATTACHMENT_COMPONENT_TYPE                      0x8211
#define GL_FRAMEBUFFER_ATTACHMENT_RED_SIZE                            0x8212
#define GL_FRAMEBUFFER_ATTACHMENT_GREEN_SIZE                          0x8213
#define GL_FRAMEBUFFER_ATTACHMENT_BLUE_SIZE                           0x8214
#define GL_FRAMEBUFFER_ATTACHMENT_ALPHA_SIZE                          0x8215
#define GL_FRAMEBUFFER_ATTACHMENT_DEPTH_SIZE                          0x8216
#define GL_FRAMEBUFFER_ATTACHMENT_STENCIL_SIZE                        0x8217
#define GL_FRAMEBUFFER_DEFAULT                                        0x8218
#define GL_FRAMEBUFFER_UNDEFINED                                      0x8219
#define GL_DEPTH_STENCIL_ATTACHMENT                                   0x821A
#define GL_MAX_RENDERBUFFER_SIZE                                      0x84E8
#define GL_DEPTH_STENCIL                                              0x84F9
#define GL_UNSIGNED_INT_24_8                                          0x84FA
#define GL_DEPTH24_STENCIL8                                           0x88F0
#define GL_TEXTURE_STENCIL_SIZE                                       0x88F1
#define GL_TEXTURE_RED_TYPE                                           0x8C10
#define GL_TEXTURE_GREEN_TYPE                                         0x8C11
#define GL_TEXTURE_BLUE_TYPE                                          0x8C12
#define GL_TEXTURE_ALPHA_TYPE                                         0x8C13
#define GL_TEXTURE_DEPTH_TYPE                                         0x8C16
#define GL_UNSIGNED_NORMALIZED                                        0x8C17
#define GL_FRAMEBUFFER_BINDING                                        0x8CA6
#define GL_DRAW_FRAMEBUFFER_BINDING                                   0x8CA6
#define GL_RENDERBUFFER_BINDING                                       0x8CA7
#define GL_READ_FRAMEBUFFER                                           0x8CA8
#define GL_DRAW_FRAMEBUFFER                                           0x8CA9
#define GL_READ_FRAMEBUFFER_BINDING                                   0x8CAA
#define GL_RENDERBUFFER_SAMPLES                                       0x8CAB
#define GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE                         0x8CD0
#define GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME                         0x8CD1
#define GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LEVEL                       0x8CD2
#define GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_CUBE_MAP_FACE               0x8CD3
#define GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LAYER                       0x8CD4
#define GL_FRAMEBUFFER_COMPLETE                                       0x8CD5
#define GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT                          0x8CD6
#define GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT                  0x8CD7
#define GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER                         0x8CDB
#define GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER                         0x8CDC
#define GL_FRAMEBUFFER_UNSUPPORTED                                    0x8CDD
#define GL_MAX_COLOR_ATTACHMENTS                                      0x8CDF
#define GL_COLOR_ATTACHMENT0                                          0x8CE0
#define GL_COLOR_ATTACHMENT1                                          0x8CE1
#define GL_COLOR_ATTACHMENT2                                          0x8CE2
#define GL_COLOR_ATTACHMENT3                                          0x8CE3
#define GL_COLOR_ATTACHMENT4                                          0x8CE4
#define GL_COLOR_ATTACHMENT5                                          0x8CE5
#define GL_COLOR_ATTACHMENT6                                          0x8CE6
#define GL_COLOR_ATTACHMENT7                                          0x8CE7
#define GL_COLOR_ATTACHMENT8                                          0x8CE8
#define GL_COLOR_ATTACHMENT9                                          0x8CE9
#define GL_COLOR_ATTACHMENT10                                         0x8CEA
#define GL_COLOR_ATTACHMENT11                                         0x8CEB
#define GL_COLOR_ATTACHMENT12                                         0x8CEC
#define GL_COLOR_ATTACHMENT13                                         0x8CED
#define GL_COLOR_ATTACHMENT14                                         0x8CEE
#define GL_COLOR_ATTACHMENT15                                         0x8CEF
#define GL_COLOR_ATTACHMENT16                                         0x8CF0
#define GL_COLOR_ATTACHMENT17                                         0x8CF1
#define GL_COLOR_ATTACHMENT18                                         0x8CF2
#define GL_COLOR_ATTACHMENT19                                         0x8CF3
#define GL_COLOR_ATTACHMENT20                                         0x8CF4
#define GL_COLOR_ATTACHMENT21                                         0x8CF5
#define GL_COLOR_ATTACHMENT22                                         0x8CF6
#define GL_COLOR_ATTACHMENT23                                         0x8CF7
#define GL_COLOR_ATTACHMENT24                                         0x8CF8
#define GL_COLOR_ATTACHMENT25                                         0x8CF9
#define GL_COLOR_ATTACHMENT26                                         0x8CFA
#define GL_COLOR_ATTACHMENT27                                         0x8CFB
#define GL_COLOR_ATTACHMENT28                                         0x8CFC
#define GL_COLOR_ATTACHMENT29                                         0x8CFD
#define GL_COLOR_ATTACHMENT30                                         0x8CFE
#define GL_COLOR_ATTACHMENT31                                         0x8CFF
#define GL_DEPTH_ATTACHMENT                                           0x8D00
#define GL_STENCIL_ATTACHMENT                                         0x8D20
#define GL_FRAMEBUFFER                                                0x8D40
#define GL_RENDERBUFFER                                               0x8D41
#define GL_RENDERBUFFER_WIDTH                                         0x8D42
#define GL_RENDERBUFFER_HEIGHT                                        0x8D43
#define GL_RENDERBUFFER_INTERNAL_FORMAT                               0x8D44
#define GL_STENCIL_INDEX1                                             0x8D46
#define GL_STENCIL_INDEX4                                             0x8D47
#define GL_STENCIL_INDEX8                                             0x8D48
#define GL_STENCIL_INDEX16                                            0x8D49
#define GL_RENDERBUFFER_RED_SIZE                                      0x8D50
#define GL_RENDERBUFFER_GREEN_SIZE                                    0x8D51
#define GL_RENDERBUFFER_BLUE_SIZE                                     0x8D52
#define GL_RENDERBUFFER_ALPHA_SIZE                                    0x8D53
#define GL_RENDERBUFFER_DEPTH_SIZE                                    0x8D54
#define GL_RENDERBUFFER_STENCIL_SIZE                                  0x8D55
#define GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE                         0x8D56
#define GL_MAX_SAMPLES                                                0x8D57
#define GL_FRAMEBUFFER_SRGB                                           0x8DB9
#define GL_HALF_FLOAT                                                 0x140B
#define GL_MAP_READ_BIT                                               0x0001
#define GL_MAP_WRITE_BIT                                              0x0002
#define GL_MAP_INVALIDATE_RANGE_BIT                                   0x0004
#define GL_MAP_INVALIDATE_BUFFER_BIT                                  0x0008
#define GL_MAP_FLUSH_EXPLICIT_BIT                                     0x0010
#define GL_MAP_UNSYNCHRONIZED_BIT                                     0x0020
#define GL_COMPRESSED_RED_RGTC1                                       0x8DBB
#define GL_COMPRESSED_SIGNED_RED_RGTC1                                0x8DBC
#define GL_COMPRESSED_RG_RGTC2                                        0x8DBD
#define GL_COMPRESSED_SIGNED_RG_RGTC2                                 0x8DBE
#define GL_RG                                                         0x8227
#define GL_RG_INTEGER                                                 0x8228
#define GL_R8                                                         0x8229
#define GL_R16                                                        0x822A
#define GL_RG8                                                        0x822B
#define GL_RG16                                                       0x822C
#define GL_R16F                                                       0x822D
#define GL_R32F                                                       0x822E
#define GL_RG16F                                                      0x822F
#define GL_RG32F                                                      0x8230
#define GL_R8I                                                        0x8231
#define GL_R8UI                                                       0x8232
#define GL_R16I                                                       0x8233
#define GL_R16UI                                                      0x8234
#define GL_R32I                                                       0x8235
#define GL_R32UI                                                      0x8236
#define GL_RG8I                                                       0x8237
#define GL_RG8UI                                                      0x8238
#define GL_RG16I                                                      0x8239
#define GL_RG16UI                                                     0x823A
#define GL_RG32I                                                      0x823B
#define GL_RG32UI                                                     0x823C
#define GL_VERTEX_ARRAY_BINDING                                       0x85B5
#define GL_SAMPLER_2D_RECT                                            0x8B63
#define GL_SAMPLER_2D_RECT_SHADOW                                     0x8B64
#define GL_SAMPLER_BUFFER                                             0x8DC2
#define GL_INT_SAMPLER_2D_RECT                                        0x8DCD
#define GL_INT_SAMPLER_BUFFER                                         0x8DD0
#define GL_UNSIGNED_INT_SAMPLER_2D_RECT                               0x8DD5
#define GL_UNSIGNED_INT_SAMPLER_BUFFER                                0x8DD8
#define GL_TEXTURE_BUFFER                                             0x8C2A
#define GL_MAX_TEXTURE_BUFFER_SIZE                                    0x8C2B
#define GL_TEXTURE_BINDING_BUFFER                                     0x8C2C
#define GL_TEXTURE_BUFFER_DATA_STORE_BINDING                          0x8C2D
#define GL_TEXTURE_RECTANGLE                                          0x84F5
#define GL_TEXTURE_BINDING_RECTANGLE                                  0x84F6
#define GL_PROXY_TEXTURE_RECTANGLE                                    0x84F7
#define GL_MAX_RECTANGLE_TEXTURE_SIZE                                 0x84F8
#define GL_R8_SNORM                                                   0x8F94
#define GL_RG8_SNORM                                                  0x8F95
#define GL_RGB8_SNORM                                                 0x8F96
#define GL_RGBA8_SNORM                                                0x8F97
#define GL_R16_SNORM                                                  0x8F98
#define GL_RG16_SNORM                                                 0x8F99
#define GL_RGB16_SNORM                                                0x8F9A
#define GL_RGBA16_SNORM                                               0x8F9B
#define GL_SIGNED_NORMALIZED                                          0x8F9C
#define GL_PRIMITIVE_RESTART                                          0x8F9D
#define GL_PRIMITIVE_RESTART_INDEX                                    0x8F9E
#define GL_COPY_READ_BUFFER                                           0x8F36
#define GL_COPY_WRITE_BUFFER                                          0x8F37
#define GL_UNIFORM_BUFFER                                             0x8A11
#define GL_UNIFORM_BUFFER_BINDING                                     0x8A28
#define GL_UNIFORM_BUFFER_START                                       0x8A29
#define GL_UNIFORM_BUFFER_SIZE                                        0x8A2A
#define GL_MAX_VERTEX_UNIFORM_BLOCKS                                  0x8A2B
#define GL_MAX_GEOMETRY_UNIFORM_BLOCKS                                0x8A2C
#define GL_MAX_FRAGMENT_UNIFORM_BLOCKS                                0x8A2D
#define GL_MAX_COMBINED_UNIFORM_BLOCKS                                0x8A2E
#define GL_MAX_UNIFORM_BUFFER_BINDINGS                                0x8A2F
#define GL_MAX_UNIFORM_BLOCK_SIZE                                     0x8A30
#define GL_MAX_COMBINED_VERTEX_UNIFORM_COMPONENTS                     0x8A31
#define GL_MAX_COMBINED_GEOMETRY_UNIFORM_COMPONENTS                   0x8A32
#define GL_MAX_COMBINED_FRAGMENT_UNIFORM_COMPONENTS                   0x8A33
#define GL_UNIFORM_BUFFER_OFFSET_ALIGNMENT                            0x8A34
#define GL_ACTIVE_UNIFORM_BLOCK_MAX_NAME_LENGTH                       0x8A35
#define GL_ACTIVE_UNIFORM_BLOCKS                                      0x8A36
#define GL_UNIFORM_TYPE                                               0x8A37
#define GL_UNIFORM_SIZE                                               0x8A38
#define GL_UNIFORM_NAME_LENGTH                                        0x8A39
#define GL_UNIFORM_BLOCK_INDEX                                        0x8A3A
#define GL_UNIFORM_OFFSET                                             0x8A3B
#define GL_UNIFORM_ARRAY_STRIDE                                       0x8A3C
#define GL_UNIFORM_MATRIX_STRIDE                                      0x8A3D
#define GL_UNIFORM_IS_ROW_MAJOR                                       0x8A3E
#define GL_UNIFORM_BLOCK_BINDING                                      0x8A3F
#define GL_UNIFORM_BLOCK_DATA_SIZE                                    0x8A40
#define GL_UNIFORM_BLOCK_NAME_LENGTH                                  0x8A41
#define GL_UNIFORM_BLOCK_ACTIVE_UNIFORMS                              0x8A42
#define GL_UNIFORM_BLOCK_ACTIVE_UNIFORM_INDICES                       0x8A43
#define GL_UNIFORM_BLOCK_REFERENCED_BY_VERTEX_SHADER                  0x8A44
#define GL_UNIFORM_BLOCK_REFERENCED_BY_GEOMETRY_SHADER                0x8A45
#define GL_UNIFORM_BLOCK_REFERENCED_BY_FRAGMENT_SHADER                0x8A46
#define GL_CONTEXT_CORE_PROFILE_BIT                                   0x0001
#define GL_CONTEXT_COMPATIBILITY_PROFILE_BIT                          0x0002
#define GL_LINES_ADJACENCY                                            0x000A
#define GL_LINE_STRIP_ADJACENCY                                       0x000B
#define GL_TRIANGLES_ADJACENCY                                        0x000C
#define GL_TRIANGLE_STRIP_ADJACENCY                                   0x000D
#define GL_PROGRAM_POINT_SIZE                                         0x8642
#define GL_MAX_GEOMETRY_TEXTURE_IMAGE_UNITS                           0x8C29
#define GL_FRAMEBUFFER_ATTACHMENT_LAYERED                             0x8DA7
#define GL_FRAMEBUFFER_INCOMPLETE_LAYER_TARGETS                       0x8DA8
#define GL_GEOMETRY_SHADER                                            0x8DD9
#define GL_GEOMETRY_VERTICES_OUT                                      0x8916
#define GL_GEOMETRY_INPUT_TYPE                                        0x8917
#define GL_GEOMETRY_OUTPUT_TYPE                                       0x8918
#define GL_MAX_GEOMETRY_UNIFORM_COMPONENTS                            0x8DDF
#define GL_MAX_GEOMETRY_OUTPUT_VERTICES                               0x8DE0
#define GL_MAX_GEOMETRY_TOTAL_OUTPUT_COMPONENTS                       0x8DE1
#define GL_MAX_VERTEX_OUTPUT_COMPONENTS                               0x9122
#define GL_MAX_GEOMETRY_INPUT_COMPONENTS                              0x9123
#define GL_MAX_GEOMETRY_OUTPUT_COMPONENTS                             0x9124
#define GL_MAX_FRAGMENT_INPUT_COMPONENTS                              0x9125
#define GL_CONTEXT_PROFILE_MASK                                       0x9126
#define GL_DEPTH_CLAMP                                                0x864F
#define GL_QUADS_FOLLOW_PROVOKING_VERTEX_CONVENTION                   0x8E4C
#define GL_FIRST_VERTEX_CONVENTION                                    0x8E4D
#define GL_LAST_VERTEX_CONVENTION                                     0x8E4E
#define GL_PROVOKING_VERTEX                                           0x8E4F
#define GL_TEXTURE_CUBE_MAP_SEAMLESS                                  0x884F
#define GL_MAX_SERVER_WAIT_TIMEOUT                                    0x9111
#define GL_OBJECT_TYPE                                                0x9112
#define GL_SYNC_CONDITION                                             0x9113
#define GL_SYNC_STATUS                                                0x9114
#define GL_SYNC_FLAGS                                                 0x9115
#define GL_SYNC_FENCE                                                 0x9116
#define GL_SYNC_GPU_COMMANDS_COMPLETE                                 0x9117
#define GL_UNSIGNALED                                                 0x9118
#define GL_SIGNALED                                                   0x9119
#define GL_ALREADY_SIGNALED                                           0x911A
#define GL_TIMEOUT_EXPIRED                                            0x911B
#define GL_CONDITION_SATISFIED                                        0x911C
#define GL_WAIT_FAILED                                                0x911D
#define GL_SYNC_FLUSH_COMMANDS_BIT                                    0x0001
#define GL_SAMPLE_POSITION                                            0x8E50
#define GL_SAMPLE_MASK                                                0x8E51
#define GL_SAMPLE_MASK_VALUE                                          0x8E52
#define GL_MAX_SAMPLE_MASK_WORDS                                      0x8E59
#define GL_TEXTURE_2D_MULTISAMPLE                                     0x9100
#define GL_PROXY_TEXTURE_2D_MULTISAMPLE                               0x9101
#define GL_TEXTURE_2D_MULTISAMPLE_ARRAY                               0x9102
#define GL_PROXY_TEXTURE_2D_MULTISAMPLE_ARRAY                         0x9103
#define GL_TEXTURE_BINDING_2D_MULTISAMPLE                             0x9104
#define GL_TEXTURE_BINDING_2D_MULTISAMPLE_ARRAY                       0x9105
#define GL_TEXTURE_SAMPLES                                            0x9106
#define GL_TEXTURE_FIXED_SAMPLE_LOCATIONS                             0x9107
#define GL_SAMPLER_2D_MULTISAMPLE                                     0x9108
#define GL_INT_SAMPLER_2D_MULTISAMPLE                                 0x9109
#define GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE                        0x910A
#define GL_SAMPLER_2D_MULTISAMPLE_ARRAY                               0x910B
#define GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY                           0x910C
#define GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY                  0x910D
#define GL_MAX_COLOR_TEXTURE_SAMPLES                                  0x910E
#define GL_MAX_DEPTH_TEXTURE_SAMPLES                                  0x910F
#define GL_MAX_INTEGER_SAMPLES                                        0x9110
#define GL_VERTEX_ATTRIB_ARRAY_DIVISOR                                0x88FE
#define GL_SRC1_COLOR                                                 0x88F9
#define GL_ONE_MINUS_SRC1_COLOR                                       0x88FA
#define GL_ONE_MINUS_SRC1_ALPHA                                       0x88FB
#define GL_MAX_DUAL_SOURCE_DRAW_BUFFERS                               0x88FC
#define GL_ANY_SAMPLES_PASSED                                         0x8C2F
#define GL_SAMPLER_BINDING                                            0x8919
#define GL_RGB10_A2UI                                                 0x906F
#define GL_TEXTURE_SWIZZLE_R                                          0x8E42
#define GL_TEXTURE_SWIZZLE_G                                          0x8E43
#define GL_TEXTURE_SWIZZLE_B                                          0x8E44
#define GL_TEXTURE_SWIZZLE_A                                          0x8E45
#define GL_TEXTURE_SWIZZLE_RGBA                                       0x8E46
#define GL_TIME_ELAPSED                                               0x88BF
#define GL_TIMESTAMP                                                  0x8E28
#define GL_INT_2_10_10_10_REV                                         0x8D9F
#define GL_SAMPLE_SHADING                                             0x8C36
#define GL_MIN_SAMPLE_SHADING_VALUE                                   0x8C37
#define GL_MIN_PROGRAM_TEXTURE_GATHER_OFFSET                          0x8E5E
#define GL_MAX_PROGRAM_TEXTURE_GATHER_OFFSET                          0x8E5F
#define GL_TEXTURE_CUBE_MAP_ARRAY                                     0x9009
#define GL_TEXTURE_BINDING_CUBE_MAP_ARRAY                             0x900A
#define GL_PROXY_TEXTURE_CUBE_MAP_ARRAY                               0x900B
#define GL_SAMPLER_CUBE_MAP_ARRAY                                     0x900C
#define GL_SAMPLER_CUBE_MAP_ARRAY_SHADOW                              0x900D
#define GL_INT_SAMPLER_CUBE_MAP_ARRAY                                 0x900E
#define GL_UNSIGNED_INT_SAMPLER_CUBE_MAP_ARRAY                        0x900F
#define GL_DRAW_INDIRECT_BUFFER                                       0x8F3F
#define GL_DRAW_INDIRECT_BUFFER_BINDING                               0x8F43
#define GL_GEOMETRY_SHADER_INVOCATIONS                                0x887F
#define GL_MAX_GEOMETRY_SHADER_INVOCATIONS                            0x8E5A
#define GL_MIN_FRAGMENT_INTERPOLATION_OFFSET                          0x8E5B
#define GL_MAX_FRAGMENT_INTERPOLATION_OFFSET                          0x8E5C
#define GL_FRAGMENT_INTERPOLATION_OFFSET_BITS                         0x8E5D
#define GL_MAX_VERTEX_STREAMS                                         0x8E71
#define GL_DOUBLE_VEC2                                                0x8FFC
#define GL_DOUBLE_VEC3                                                0x8FFD
#define GL_DOUBLE_VEC4                                                0x8FFE
#define GL_DOUBLE_MAT2                                                0x8F46
#define GL_DOUBLE_MAT3                                                0x8F47
#define GL_DOUBLE_MAT4                                                0x8F48
#define GL_DOUBLE_MAT2x3                                              0x8F49
#define GL_DOUBLE_MAT2x4                                              0x8F4A
#define GL_DOUBLE_MAT3x2                                              0x8F4B
#define GL_DOUBLE_MAT3x4                                              0x8F4C
#define GL_DOUBLE_MAT4x2                                              0x8F4D
#define GL_DOUBLE_MAT4x3                                              0x8F4E
#define GL_ACTIVE_SUBROUTINES                                         0x8DE5
#define GL_ACTIVE_SUBROUTINE_UNIFORMS                                 0x8DE6
#define GL_ACTIVE_SUBROUTINE_UNIFORM_LOCATIONS                        0x8E47
#define GL_ACTIVE_SUBROUTINE_MAX_LENGTH                               0x8E48
#define GL_ACTIVE_SUBROUTINE_UNIFORM_MAX_LENGTH                       0x8E49
#define GL_MAX_SUBROUTINES                                            0x8DE7
#define GL_MAX_SUBROUTINE_UNIFORM_LOCATIONS                           0x8DE8
#define GL_NUM_COMPATIBLE_SUBROUTINES                                 0x8E4A
#define GL_COMPATIBLE_SUBROUTINES                                     0x8E4B
#define GL_PATCHES                                                    0x000E
#define GL_PATCH_VERTICES                                             0x8E72
#define GL_PATCH_DEFAULT_INNER_LEVEL                                  0x8E73
#define GL_PATCH_DEFAULT_OUTER_LEVEL                                  0x8E74
#define GL_TESS_CONTROL_OUTPUT_VERTICES                               0x8E75
#define GL_TESS_GEN_MODE                                              0x8E76
#define GL_TESS_GEN_SPACING                                           0x8E77
#define GL_TESS_GEN_VERTEX_ORDER                                      0x8E78
#define GL_TESS_GEN_POINT_MODE                                        0x8E79
#define GL_ISOLINES                                                   0x8E7A
#define GL_FRACTIONAL_ODD                                             0x8E7B
#define GL_FRACTIONAL_EVEN                                            0x8E7C
#define GL_MAX_PATCH_VERTICES                                         0x8E7D
#define GL_MAX_TESS_GEN_LEVEL                                         0x8E7E
#define GL_MAX_TESS_CONTROL_UNIFORM_COMPONENTS                        0x8E7F
#define GL_MAX_TESS_EVALUATION_UNIFORM_COMPONENTS                     0x8E80
#define GL_MAX_TESS_CONTROL_TEXTURE_IMAGE_UNITS                       0x8E81
#define GL_MAX_TESS_EVALUATION_TEXTURE_IMAGE_UNITS                    0x8E82
#define GL_MAX_TESS_CONTROL_OUTPUT_COMPONENTS                         0x8E83
#define GL_MAX_TESS_PATCH_COMPONENTS                                  0x8E84
#define GL_MAX_TESS_CONTROL_TOTAL_OUTPUT_COMPONENTS                   0x8E85
#define GL_MAX_TESS_EVALUATION_OUTPUT_COMPONENTS                      0x8E86
#define GL_MAX_TESS_CONTROL_UNIFORM_BLOCKS                            0x8E89
#define GL_MAX_TESS_EVALUATION_UNIFORM_BLOCKS                         0x8E8A
#define GL_MAX_TESS_CONTROL_INPUT_COMPONENTS                          0x886C
#define GL_MAX_TESS_EVALUATION_INPUT_COMPONENTS                       0x886D
#define GL_MAX_COMBINED_TESS_CONTROL_UNIFORM_COMPONENTS               0x8E1E
#define GL_MAX_COMBINED_TESS_EVALUATION_UNIFORM_COMPONENTS            0x8E1F
#define GL_UNIFORM_BLOCK_REFERENCED_BY_TESS_CONTROL_SHADER            0x84F0
#define GL_UNIFORM_BLOCK_REFERENCED_BY_TESS_EVALUATION_SHADER         0x84F1
#define GL_TESS_EVALUATION_SHADER                                     0x8E87
#define GL_TESS_CONTROL_SHADER                                        0x8E88
#define GL_TRANSFORM_FEEDBACK                                         0x8E22
#define GL_TRANSFORM_FEEDBACK_BUFFER_PAUSED                           0x8E23
#define GL_TRANSFORM_FEEDBACK_BUFFER_ACTIVE                           0x8E24
#define GL_TRANSFORM_FEEDBACK_BINDING                                 0x8E25
#define GL_MAX_TRANSFORM_FEEDBACK_BUFFERS                             0x8E70
#define GL_FIXED                                                      0x140C
#define GL_IMPLEMENTATION_COLOR_READ_TYPE                             0x8B9A
#define GL_IMPLEMENTATION_COLOR_READ_FORMAT                           0x8B9B
#define GL_LOW_FLOAT                                                  0x8DF0
#define GL_MEDIUM_FLOAT                                               0x8DF1
#define GL_HIGH_FLOAT                                                 0x8DF2
#define GL_LOW_INT                                                    0x8DF3
#define GL_MEDIUM_INT                                                 0x8DF4
#define GL_HIGH_INT                                                   0x8DF5
#define GL_SHADER_COMPILER                                            0x8DFA
#define GL_SHADER_BINARY_FORMATS                                      0x8DF8
#define GL_NUM_SHADER_BINARY_FORMATS                                  0x8DF9
#define GL_MAX_VERTEX_UNIFORM_VECTORS                                 0x8DFB
#define GL_MAX_VARYING_VECTORS                                        0x8DFC
#define GL_MAX_FRAGMENT_UNIFORM_VECTORS                               0x8DFD
#define GL_RGB565                                                     0x8D62
#define GL_PROGRAM_BINARY_RETRIEVABLE_HINT                            0x8257
#define GL_PROGRAM_BINARY_LENGTH                                      0x8741
#define GL_NUM_PROGRAM_BINARY_FORMATS                                 0x87FE
#define GL_PROGRAM_BINARY_FORMATS                                     0x87FF
#define GL_VERTEX_SHADER_BIT                                          0x0001
#define GL_FRAGMENT_SHADER_BIT                                        0x0002
#define GL_GEOMETRY_SHADER_BIT                                        0x0004
#define GL_TESS_CONTROL_SHADER_BIT                                    0x0008
#define GL_TESS_EVALUATION_SHADER_BIT                                 0x0010
#define GL_PROGRAM_SEPARABLE                                          0x8258
#define GL_ACTIVE_PROGRAM                                             0x8259
#define GL_PROGRAM_PIPELINE_BINDING                                   0x825A
#define GL_MAX_VIEWPORTS                                              0x825B
#define GL_VIEWPORT_SUBPIXEL_BITS                                     0x825C
#define GL_VIEWPORT_BOUNDS_RANGE                                      0x825D
#define GL_LAYER_PROVOKING_VERTEX                                     0x825E
#define GL_VIEWPORT_INDEX_PROVOKING_VERTEX                            0x825F
#define GL_UNDEFINED_VERTEX                                           0x8260
#define GL_COPY_READ_BUFFER_BINDING                                   0x8F36
#define GL_COPY_WRITE_BUFFER_BINDING                                  0x8F37
#define GL_TRANSFORM_FEEDBACK_ACTIVE                                  0x8E24
#define GL_TRANSFORM_FEEDBACK_PAUSED                                  0x8E23
#define GL_UNPACK_COMPRESSED_BLOCK_WIDTH                              0x9127
#define GL_UNPACK_COMPRESSED_BLOCK_HEIGHT                             0x9128
#define GL_UNPACK_COMPRESSED_BLOCK_DEPTH                              0x9129
#define GL_UNPACK_COMPRESSED_BLOCK_SIZE                               0x912A
#define GL_PACK_COMPRESSED_BLOCK_WIDTH                                0x912B
#define GL_PACK_COMPRESSED_BLOCK_HEIGHT                               0x912C
#define GL_PACK_COMPRESSED_BLOCK_DEPTH                                0x912D
#define GL_PACK_COMPRESSED_BLOCK_SIZE                                 0x912E
#define GL_NUM_SAMPLE_COUNTS                                          0x9380
#define GL_MIN_MAP_BUFFER_ALIGNMENT                                   0x90BC
#define GL_ATOMIC_COUNTER_BUFFER                                      0x92C0
#define GL_ATOMIC_COUNTER_BUFFER_BINDING                              0x92C1
#define GL_ATOMIC_COUNTER_BUFFER_START                                0x92C2
#define GL_ATOMIC_COUNTER_BUFFER_SIZE                                 0x92C3
#define GL_ATOMIC_COUNTER_BUFFER_DATA_SIZE                            0x92C4
#define GL_ATOMIC_COUNTER_BUFFER_ACTIVE_ATOMIC_COUNTERS               0x92C5
#define GL_ATOMIC_COUNTER_BUFFER_ACTIVE_ATOMIC_COUNTER_INDICES        0x92C6
#define GL_ATOMIC_COUNTER_BUFFER_REFERENCED_BY_VERTEX_SHADER          0x92C7
#define GL_ATOMIC_COUNTER_BUFFER_REFERENCED_BY_TESS_CONTROL_SHADER    0x92C8
#define GL_ATOMIC_COUNTER_BUFFER_REFERENCED_BY_TESS_EVALUATION_SHADER 0x92C9
#define GL_ATOMIC_COUNTER_BUFFER_REFERENCED_BY_GEOMETRY_SHADER        0x92CA
#define GL_ATOMIC_COUNTER_BUFFER_REFERENCED_BY_FRAGMENT_SHADER        0x92CB
#define GL_MAX_VERTEX_ATOMIC_COUNTER_BUFFERS                          0x92CC
#define GL_MAX_TESS_CONTROL_ATOMIC_COUNTER_BUFFERS                    0x92CD
#define GL_MAX_TESS_EVALUATION_ATOMIC_COUNTER_BUFFERS                 0x92CE
#define GL_MAX_GEOMETRY_ATOMIC_COUNTER_BUFFERS                        0x92CF
#define GL_MAX_FRAGMENT_ATOMIC_COUNTER_BUFFERS                        0x92D0
#define GL_MAX_COMBINED_ATOMIC_COUNTER_BUFFERS                        0x92D1
#define GL_MAX_VERTEX_ATOMIC_COUNTERS                                 0x92D2
#define GL_MAX_TESS_CONTROL_ATOMIC_COUNTERS                           0x92D3
#define GL_MAX_TESS_EVALUATION_ATOMIC_COUNTERS                        0x92D4
#define GL_MAX_GEOMETRY_ATOMIC_COUNTERS                               0x92D5
#define GL_MAX_FRAGMENT_ATOMIC_COUNTERS                               0x92D6
#define GL_MAX_COMBINED_ATOMIC_COUNTERS                               0x92D7
#define GL_MAX_ATOMIC_COUNTER_BUFFER_SIZE                             0x92D8
#define GL_MAX_ATOMIC_COUNTER_BUFFER_BINDINGS                         0x92DC
#define GL_ACTIVE_ATOMIC_COUNTER_BUFFERS                              0x92D9
#define GL_UNIFORM_ATOMIC_COUNTER_BUFFER_INDEX                        0x92DA
#define GL_UNSIGNED_INT_ATOMIC_COUNTER                                0x92DB
#define GL_VERTEX_ATTRIB_ARRAY_BARRIER_BIT                            0x0001
#define GL_ELEMENT_ARRAY_BARRIER_BIT                                  0x0002
#define GL_UNIFORM_BARRIER_BIT                                        0x0004
#define GL_TEXTURE_FETCH_BARRIER_BIT                                  0x0008
#define GL_SHADER_IMAGE_ACCESS_BARRIER_BIT                            0x0020
#define GL_COMMAND_BARRIER_BIT                                        0x0040
#define GL_PIXEL_BUFFER_BARRIER_BIT                                   0x0080
#define GL_TEXTURE_UPDATE_BARRIER_BIT                                 0x0100
#define GL_BUFFER_UPDATE_BARRIER_BIT                                  0x0200
#define GL_FRAMEBUFFER_BARRIER_BIT                                    0x0400
#define GL_TRANSFORM_FEEDBACK_BARRIER_BIT                             0x0800
#define GL_ATOMIC_COUNTER_BARRIER_BIT                                 0x1000
#define GL_MAX_IMAGE_UNITS                                            0x8F38
#define GL_MAX_COMBINED_IMAGE_UNITS_AND_FRAGMENT_OUTPUTS              0x8F39
#define GL_IMAGE_BINDING_NAME                                         0x8F3A
#define GL_IMAGE_BINDING_LEVEL                                        0x8F3B
#define GL_IMAGE_BINDING_LAYERED                                      0x8F3C
#define GL_IMAGE_BINDING_LAYER                                        0x8F3D
#define GL_IMAGE_BINDING_ACCESS                                       0x8F3E
#define GL_IMAGE_1D                                                   0x904C
#define GL_IMAGE_2D                                                   0x904D
#define GL_IMAGE_3D                                                   0x904E
#define GL_IMAGE_2D_RECT                                              0x904F
#define GL_IMAGE_CUBE                                                 0x9050
#define GL_IMAGE_BUFFER                                               0x9051
#define GL_IMAGE_1D_ARRAY                                             0x9052
#define GL_IMAGE_2D_ARRAY                                             0x9053
#define GL_IMAGE_CUBE_MAP_ARRAY                                       0x9054
#define GL_IMAGE_2D_MULTISAMPLE                                       0x9055
#define GL_IMAGE_2D_MULTISAMPLE_ARRAY                                 0x9056
#define GL_INT_IMAGE_1D                                               0x9057
#define GL_INT_IMAGE_2D                                               0x9058
#define GL_INT_IMAGE_3D                                               0x9059
#define GL_INT_IMAGE_2D_RECT                                          0x905A
#define GL_INT_IMAGE_CUBE                                             0x905B
#define GL_INT_IMAGE_BUFFER                                           0x905C
#define GL_INT_IMAGE_1D_ARRAY                                         0x905D
#define GL_INT_IMAGE_2D_ARRAY                                         0x905E
#define GL_INT_IMAGE_CUBE_MAP_ARRAY                                   0x905F
#define GL_INT_IMAGE_2D_MULTISAMPLE                                   0x9060
#define GL_INT_IMAGE_2D_MULTISAMPLE_ARRAY                             0x9061
#define GL_UNSIGNED_INT_IMAGE_1D                                      0x9062
#define GL_UNSIGNED_INT_IMAGE_2D                                      0x9063
#define GL_UNSIGNED_INT_IMAGE_3D                                      0x9064
#define GL_UNSIGNED_INT_IMAGE_2D_RECT                                 0x9065
#define GL_UNSIGNED_INT_IMAGE_CUBE                                    0x9066
#define GL_UNSIGNED_INT_IMAGE_BUFFER                                  0x9067
#define GL_UNSIGNED_INT_IMAGE_1D_ARRAY                                0x9068
#define GL_UNSIGNED_INT_IMAGE_2D_ARRAY                                0x9069
#define GL_UNSIGNED_INT_IMAGE_CUBE_MAP_ARRAY                          0x906A
#define GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE                          0x906B
#define GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE_ARRAY                    0x906C
#define GL_MAX_IMAGE_SAMPLES                                          0x906D
#define GL_IMAGE_BINDING_FORMAT                                       0x906E
#define GL_IMAGE_FORMAT_COMPATIBILITY_TYPE                            0x90C7
#define GL_IMAGE_FORMAT_COMPATIBILITY_BY_SIZE                         0x90C8
#define GL_IMAGE_FORMAT_COMPATIBILITY_BY_CLASS                        0x90C9
#define GL_MAX_VERTEX_IMAGE_UNIFORMS                                  0x90CA
#define GL_MAX_TESS_CONTROL_IMAGE_UNIFORMS                            0x90CB
#define GL_MAX_TESS_EVALUATION_IMAGE_UNIFORMS                         0x90CC
#define GL_MAX_GEOMETRY_IMAGE_UNIFORMS                                0x90CD
#define GL_MAX_FRAGMENT_IMAGE_UNIFORMS                                0x90CE
#define GL_MAX_COMBINED_IMAGE_UNIFORMS                                0x90CF
#define GL_COMPRESSED_RGBA_BPTC_UNORM                                 0x8E8C
#define GL_COMPRESSED_SRGB_ALPHA_BPTC_UNORM                           0x8E8D
#define GL_COMPRESSED_RGB_BPTC_SIGNED_FLOAT                           0x8E8E
#define GL_COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT                         0x8E8F
#define GL_TEXTURE_IMMUTABLE_FORMAT                                   0x912F
#define GL_NUM_SHADING_LANGUAGE_VERSIONS                              0x82E9
#define GL_VERTEX_ATTRIB_ARRAY_LONG                                   0x874E
#define GL_COMPRESSED_RGB8_ETC2                                       0x9274
#define GL_COMPRESSED_SRGB8_ETC2                                      0x9275
#define GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2                   0x9276
#define GL_COMPRESSED_SRGB8_PUNCHTHROUGH_ALPHA1_ETC2                  0x9277
#define GL_COMPRESSED_RGBA8_ETC2_EAC                                  0x9278
#define GL_COMPRESSED_SRGB8_ALPHA8_ETC2_EAC                           0x9279
#define GL_COMPRESSED_R11_EAC                                         0x9270
#define GL_COMPRESSED_SIGNED_R11_EAC                                  0x9271
#define GL_COMPRESSED_RG11_EAC                                        0x9272
#define GL_COMPRESSED_SIGNED_RG11_EAC                                 0x9273
#define GL_PRIMITIVE_RESTART_FIXED_INDEX                              0x8D69
#define GL_ANY_SAMPLES_PASSED_CONSERVATIVE                            0x8D6A
#define GL_MAX_ELEMENT_INDEX                                          0x8D6B
#define GL_COMPUTE_SHADER                                             0x91B9
#define GL_MAX_COMPUTE_UNIFORM_BLOCKS                                 0x91BB
#define GL_MAX_COMPUTE_TEXTURE_IMAGE_UNITS                            0x91BC
#define GL_MAX_COMPUTE_IMAGE_UNIFORMS                                 0x91BD
#define GL_MAX_COMPUTE_SHARED_MEMORY_SIZE                             0x8262
#define GL_MAX_COMPUTE_UNIFORM_COMPONENTS                             0x8263
#define GL_MAX_COMPUTE_ATOMIC_COUNTER_BUFFERS                         0x8264
#define GL_MAX_COMPUTE_ATOMIC_COUNTERS                                0x8265
#define GL_MAX_COMBINED_COMPUTE_UNIFORM_COMPONENTS                    0x8266
#define GL_MAX_COMPUTE_WORK_GROUP_INVOCATIONS                         0x90EB
#define GL_MAX_COMPUTE_WORK_GROUP_COUNT                               0x91BE
#define GL_MAX_COMPUTE_WORK_GROUP_SIZE                                0x91BF
#define GL_COMPUTE_WORK_GROUP_SIZE                                    0x8267
#define GL_UNIFORM_BLOCK_REFERENCED_BY_COMPUTE_SHADER                 0x90EC
#define GL_ATOMIC_COUNTER_BUFFER_REFERENCED_BY_COMPUTE_SHADER         0x90ED
#define GL_DISPATCH_INDIRECT_BUFFER                                   0x90EE
#define GL_DISPATCH_INDIRECT_BUFFER_BINDING                           0x90EF
#define GL_COMPUTE_SHADER_BIT                                         0x0020
#define GL_DEBUG_OUTPUT_SYNCHRONOUS                                   0x8242
#define GL_DEBUG_NEXT_LOGGED_MESSAGE_LENGTH                           0x8243
#define GL_DEBUG_CALLBACK_FUNCTION                                    0x8244
#define GL_DEBUG_CALLBACK_USER_PARAM                                  0x8245
#define GL_DEBUG_SOURCE_API                                           0x8246
#define GL_DEBUG_SOURCE_WINDOW_SYSTEM                                 0x8247
#define GL_DEBUG_SOURCE_SHADER_COMPILER                               0x8248
#define GL_DEBUG_SOURCE_THIRD_PARTY                                   0x8249
#define GL_DEBUG_SOURCE_APPLICATION                                   0x824A
#define GL_DEBUG_SOURCE_OTHER                                         0x824B
#define GL_DEBUG_TYPE_ERROR                                           0x824C
#define GL_DEBUG_TYPE_DEPRECATED_BEHAVIOR                             0x824D
#define GL_DEBUG_TYPE_UNDEFINED_BEHAVIOR                              0x824E
#define GL_DEBUG_TYPE_PORTABILITY                                     0x824F
#define GL_DEBUG_TYPE_PERFORMANCE                                     0x8250
#define GL_DEBUG_TYPE_OTHER                                           0x8251
#define GL_MAX_DEBUG_MESSAGE_LENGTH                                   0x9143
#define GL_MAX_DEBUG_LOGGED_MESSAGES                                  0x9144
#define GL_DEBUG_LOGGED_MESSAGES                                      0x9145
#define GL_DEBUG_SEVERITY_HIGH                                        0x9146
#define GL_DEBUG_SEVERITY_MEDIUM                                      0x9147
#define GL_DEBUG_SEVERITY_LOW                                         0x9148
#define GL_DEBUG_TYPE_MARKER                                          0x8268
#define GL_DEBUG_TYPE_PUSH_GROUP                                      0x8269
#define GL_DEBUG_TYPE_POP_GROUP                                       0x826A
#define GL_DEBUG_SEVERITY_NOTIFICATION                                0x826B
#define GL_MAX_DEBUG_GROUP_STACK_DEPTH                                0x826C
#define GL_DEBUG_GROUP_STACK_DEPTH                                    0x826D
#define GL_BUFFER                                                     0x82E0
#define GL_SHADER                                                     0x82E1
#define GL_PROGRAM                                                    0x82E2
#define GL_QUERY                                                      0x82E3
#define GL_PROGRAM_PIPELINE                                           0x82E4
#define GL_SAMPLER                                                    0x82E6
#define GL_MAX_LABEL_LENGTH                                           0x82E8
#define GL_DEBUG_OUTPUT                                               0x92E0
#define GL_CONTEXT_FLAG_DEBUG_BIT                                     0x0002
#define GL_MAX_UNIFORM_LOCATIONS                                      0x826E
#define GL_FRAMEBUFFER_DEFAULT_WIDTH                                  0x9310
#define GL_FRAMEBUFFER_DEFAULT_HEIGHT                                 0x9311
#define GL_FRAMEBUFFER_DEFAULT_LAYERS                                 0x9312
#define GL_FRAMEBUFFER_DEFAULT_SAMPLES                                0x9313
#define GL_FRAMEBUFFER_DEFAULT_FIXED_SAMPLE_LOCATIONS                 0x9314
#define GL_MAX_FRAMEBUFFER_WIDTH                                      0x9315
#define GL_MAX_FRAMEBUFFER_HEIGHT                                     0x9316
#define GL_MAX_FRAMEBUFFER_LAYERS                                     0x9317
#define GL_MAX_FRAMEBUFFER_SAMPLES                                    0x9318
#define GL_INTERNALFORMAT_SUPPORTED                                   0x826F
#define GL_INTERNALFORMAT_PREFERRED                                   0x8270
#define GL_INTERNALFORMAT_RED_SIZE                                    0x8271
#define GL_INTERNALFORMAT_GREEN_SIZE                                  0x8272
#define GL_INTERNALFORMAT_BLUE_SIZE                                   0x8273
#define GL_INTERNALFORMAT_ALPHA_SIZE                                  0x8274
#define GL_INTERNALFORMAT_DEPTH_SIZE                                  0x8275
#define GL_INTERNALFORMAT_STENCIL_SIZE                                0x8276
#define GL_INTERNALFORMAT_SHARED_SIZE                                 0x8277
#define GL_INTERNALFORMAT_RED_TYPE                                    0x8278
#define GL_INTERNALFORMAT_GREEN_TYPE                                  0x8279
#define GL_INTERNALFORMAT_BLUE_TYPE                                   0x827A
#define GL_INTERNALFORMAT_ALPHA_TYPE                                  0x827B
#define GL_INTERNALFORMAT_DEPTH_TYPE                                  0x827C
#define GL_INTERNALFORMAT_STENCIL_TYPE                                0x827D
#define GL_MAX_WIDTH                                                  0x827E
#define GL_MAX_HEIGHT                                                 0x827F
#define GL_MAX_DEPTH                                                  0x8280
#define GL_MAX_LAYERS                                                 0x8281
#define GL_MAX_COMBINED_DIMENSIONS                                    0x8282
#define GL_COLOR_COMPONENTS                                           0x8283
#define GL_DEPTH_COMPONENTS                                           0x8284
#define GL_STENCIL_COMPONENTS                                         0x8285
#define GL_COLOR_RENDERABLE                                           0x8286
#define GL_DEPTH_RENDERABLE                                           0x8287
#define GL_STENCIL_RENDERABLE                                         0x8288
#define GL_FRAMEBUFFER_RENDERABLE                                     0x8289
#define GL_FRAMEBUFFER_RENDERABLE_LAYERED                             0x828A
#define GL_FRAMEBUFFER_BLEND                                          0x828B
#define GL_READ_PIXELS                                                0x828C
#define GL_READ_PIXELS_FORMAT                                         0x828D
#define GL_READ_PIXELS_TYPE                                           0x828E
#define GL_TEXTURE_IMAGE_FORMAT                                       0x828F
#define GL_TEXTURE_IMAGE_TYPE                                         0x8290
#define GL_GET_TEXTURE_IMAGE_FORMAT                                   0x8291
#define GL_GET_TEXTURE_IMAGE_TYPE                                     0x8292
#define GL_MIPMAP                                                     0x8293
#define GL_MANUAL_GENERATE_MIPMAP                                     0x8294
#define GL_AUTO_GENERATE_MIPMAP                                       0x8295
#define GL_COLOR_ENCODING                                             0x8296
#define GL_SRGB_READ                                                  0x8297
#define GL_SRGB_WRITE                                                 0x8298
#define GL_FILTER                                                     0x829A
#define GL_VERTEX_TEXTURE                                             0x829B
#define GL_TESS_CONTROL_TEXTURE                                       0x829C
#define GL_TESS_EVALUATION_TEXTURE                                    0x829D
#define GL_GEOMETRY_TEXTURE                                           0x829E
#define GL_FRAGMENT_TEXTURE                                           0x829F
#define GL_COMPUTE_TEXTURE                                            0x82A0
#define GL_TEXTURE_SHADOW                                             0x82A1
#define GL_TEXTURE_GATHER                                             0x82A2
#define GL_TEXTURE_GATHER_SHADOW                                      0x82A3
#define GL_SHADER_IMAGE_LOAD                                          0x82A4
#define GL_SHADER_IMAGE_STORE                                         0x82A5
#define GL_SHADER_IMAGE_ATOMIC                                        0x82A6
#define GL_IMAGE_TEXEL_SIZE                                           0x82A7
#define GL_IMAGE_COMPATIBILITY_CLASS                                  0x82A8
#define GL_IMAGE_PIXEL_FORMAT                                         0x82A9
#define GL_IMAGE_PIXEL_TYPE                                           0x82AA
#define GL_SIMULTANEOUS_TEXTURE_AND_DEPTH_TEST                        0x82AC
#define GL_SIMULTANEOUS_TEXTURE_AND_STENCIL_TEST                      0x82AD
#define GL_SIMULTANEOUS_TEXTURE_AND_DEPTH_WRITE                       0x82AE
#define GL_SIMULTANEOUS_TEXTURE_AND_STENCIL_WRITE                     0x82AF
#define GL_TEXTURE_COMPRESSED_BLOCK_WIDTH                             0x82B1
#define GL_TEXTURE_COMPRESSED_BLOCK_HEIGHT                            0x82B2
#define GL_TEXTURE_COMPRESSED_BLOCK_SIZE                              0x82B3
#define GL_CLEAR_BUFFER                                               0x82B4
#define GL_TEXTURE_VIEW                                               0x82B5
#define GL_VIEW_COMPATIBILITY_CLASS                                   0x82B6
#define GL_FULL_SUPPORT                                               0x82B7
#define GL_CAVEAT_SUPPORT                                             0x82B8
#define GL_IMAGE_CLASS_4_X_32                                         0x82B9
#define GL_IMAGE_CLASS_2_X_32                                         0x82BA
#define GL_IMAGE_CLASS_1_X_32                                         0x82BB
#define GL_IMAGE_CLASS_4_X_16                                         0x82BC
#define GL_IMAGE_CLASS_2_X_16                                         0x82BD
#define GL_IMAGE_CLASS_1_X_16                                         0x82BE
#define GL_IMAGE_CLASS_4_X_8                                          0x82BF
#define GL_IMAGE_CLASS_2_X_8                                          0x82C0
#define GL_IMAGE_CLASS_1_X_8                                          0x82C1
#define GL_IMAGE_CLASS_11_11_10                                       0x82C2
#define GL_IMAGE_CLASS_10_10_10_2                                     0x82C3
#define GL_VIEW_CLASS_128_BITS                                        0x82C4
#define GL_VIEW_CLASS_96_BITS                                         0x82C5
#define GL_VIEW_CLASS_64_BITS                                         0x82C6
#define GL_VIEW_CLASS_48_BITS                                         0x82C7
#define GL_VIEW_CLASS_32_BITS                                         0x82C8
#define GL_VIEW_CLASS_24_BITS                                         0x82C9
#define GL_VIEW_CLASS_16_BITS                                         0x82CA
#define GL_VIEW_CLASS_8_BITS                                          0x82CB
#define GL_VIEW_CLASS_S3TC_DXT1_RGB                                   0x82CC
#define GL_VIEW_CLASS_S3TC_DXT1_RGBA                                  0x82CD
#define GL_VIEW_CLASS_S3TC_DXT3_RGBA                                  0x82CE
#define GL_VIEW_CLASS_S3TC_DXT5_RGBA                                  0x82CF
#define GL_VIEW_CLASS_RGTC1_RED                                       0x82D0
#define GL_VIEW_CLASS_RGTC2_RG                                        0x82D1
#define GL_VIEW_CLASS_BPTC_UNORM                                      0x82D2
#define GL_VIEW_CLASS_BPTC_FLOAT                                      0x82D3
#define GL_UNIFORM                                                    0x92E1
#define GL_UNIFORM_BLOCK                                              0x92E2
#define GL_PROGRAM_INPUT                                              0x92E3
#define GL_PROGRAM_OUTPUT                                             0x92E4
#define GL_BUFFER_VARIABLE                                            0x92E5
#define GL_SHADER_STORAGE_BLOCK                                       0x92E6
#define GL_VERTEX_SUBROUTINE                                          0x92E8
#define GL_TESS_CONTROL_SUBROUTINE                                    0x92E9
#define GL_TESS_EVALUATION_SUBROUTINE                                 0x92EA
#define GL_GEOMETRY_SUBROUTINE                                        0x92EB
#define GL_FRAGMENT_SUBROUTINE                                        0x92EC
#define GL_COMPUTE_SUBROUTINE                                         0x92ED
#define GL_VERTEX_SUBROUTINE_UNIFORM                                  0x92EE
#define GL_TESS_CONTROL_SUBROUTINE_UNIFORM                            0x92EF
#define GL_TESS_EVALUATION_SUBROUTINE_UNIFORM                         0x92F0
#define GL_GEOMETRY_SUBROUTINE_UNIFORM                                0x92F1
#define GL_FRAGMENT_SUBROUTINE_UNIFORM                                0x92F2
#define GL_COMPUTE_SUBROUTINE_UNIFORM                                 0x92F3
#define GL_TRANSFORM_FEEDBACK_VARYING                                 0x92F4
#define GL_ACTIVE_RESOURCES                                           0x92F5
#define GL_MAX_NAME_LENGTH                                            0x92F6
#define GL_MAX_NUM_ACTIVE_VARIABLES                                   0x92F7
#define GL_MAX_NUM_COMPATIBLE_SUBROUTINES                             0x92F8
#define GL_NAME_LENGTH                                                0x92F9
#define GL_TYPE                                                       0x92FA
#define GL_ARRAY_SIZE                                                 0x92FB
#define GL_OFFSET                                                     0x92FC
#define GL_BLOCK_INDEX                                                0x92FD
#define GL_ARRAY_STRIDE                                               0x92FE
#define GL_MATRIX_STRIDE                                              0x92FF
#define GL_IS_ROW_MAJOR                                               0x9300
#define GL_ATOMIC_COUNTER_BUFFER_INDEX                                0x9301
#define GL_BUFFER_BINDING                                             0x9302
#define GL_BUFFER_DATA_SIZE                                           0x9303
#define GL_NUM_ACTIVE_VARIABLES                                       0x9304
#define GL_ACTIVE_VARIABLES                                           0x9305
#define GL_REFERENCED_BY_VERTEX_SHADER                                0x9306
#define GL_REFERENCED_BY_TESS_CONTROL_SHADER                          0x9307
#define GL_REFERENCED_BY_TESS_EVALUATION_SHADER                       0x9308
#define GL_REFERENCED_BY_GEOMETRY_SHADER                              0x9309
#define GL_REFERENCED_BY_FRAGMENT_SHADER                              0x930A
#define GL_REFERENCED_BY_COMPUTE_SHADER                               0x930B
#define GL_TOP_LEVEL_ARRAY_SIZE                                       0x930C
#define GL_TOP_LEVEL_ARRAY_STRIDE                                     0x930D
#define GL_LOCATION                                                   0x930E
#define GL_LOCATION_INDEX                                             0x930F
#define GL_IS_PER_PATCH                                               0x92E7
#define GL_SHADER_STORAGE_BUFFER                                      0x90D2
#define GL_SHADER_STORAGE_BUFFER_BINDING                              0x90D3
#define GL_SHADER_STORAGE_BUFFER_START                                0x90D4
#define GL_SHADER_STORAGE_BUFFER_SIZE                                 0x90D5
#define GL_MAX_VERTEX_SHADER_STORAGE_BLOCKS                           0x90D6
#define GL_MAX_GEOMETRY_SHADER_STORAGE_BLOCKS                         0x90D7
#define GL_MAX_TESS_CONTROL_SHADER_STORAGE_BLOCKS                     0x90D8
#define GL_MAX_TESS_EVALUATION_SHADER_STORAGE_BLOCKS                  0x90D9
#define GL_MAX_FRAGMENT_SHADER_STORAGE_BLOCKS                         0x90DA
#define GL_MAX_COMPUTE_SHADER_STORAGE_BLOCKS                          0x90DB
#define GL_MAX_COMBINED_SHADER_STORAGE_BLOCKS                         0x90DC
#define GL_MAX_SHADER_STORAGE_BUFFER_BINDINGS                         0x90DD
#define GL_MAX_SHADER_STORAGE_BLOCK_SIZE                              0x90DE
#define GL_SHADER_STORAGE_BUFFER_OFFSET_ALIGNMENT                     0x90DF
#define GL_SHADER_STORAGE_BARRIER_BIT                                 0x2000
#define GL_MAX_COMBINED_SHADER_OUTPUT_RESOURCES                       0x8F39
#define GL_DEPTH_STENCIL_TEXTURE_MODE                                 0x90EA
#define GL_TEXTURE_BUFFER_OFFSET                                      0x919D
#define GL_TEXTURE_BUFFER_SIZE                                        0x919E
#define GL_TEXTURE_BUFFER_OFFSET_ALIGNMENT                            0x919F
#define GL_TEXTURE_VIEW_MIN_LEVEL                                     0x82DB
#define GL_TEXTURE_VIEW_NUM_LEVELS                                    0x82DC
#define GL_TEXTURE_VIEW_MIN_LAYER                                     0x82DD
#define GL_TEXTURE_VIEW_NUM_LAYERS                                    0x82DE
#define GL_TEXTURE_IMMUTABLE_LEVELS                                   0x82DF
#define GL_VERTEX_ATTRIB_BINDING                                      0x82D4
#define GL_VERTEX_ATTRIB_RELATIVE_OFFSET                              0x82D5
#define GL_VERTEX_BINDING_DIVISOR                                     0x82D6
#define GL_VERTEX_BINDING_OFFSET                                      0x82D7
#define GL_VERTEX_BINDING_STRIDE                                      0x82D8
#define GL_MAX_VERTEX_ATTRIB_RELATIVE_OFFSET                          0x82D9
#define GL_MAX_VERTEX_ATTRIB_BINDINGS                                 0x82DA
#define GL_VERTEX_BINDING_BUFFER                                      0x8F4F
#define GL_MAX_VERTEX_ATTRIB_STRIDE                                   0x82E5
#define GL_PRIMITIVE_RESTART_FOR_PATCHES_SUPPORTED                    0x8221
#define GL_TEXTURE_BUFFER_BINDING                                     0x8C2A
#define GL_MAP_PERSISTENT_BIT                                         0x0040
#define GL_MAP_COHERENT_BIT                                           0x0080
#define GL_DYNAMIC_STORAGE_BIT                                        0x0100
#define GL_CLIENT_STORAGE_BIT                                         0x0200
#define GL_CLIENT_MAPPED_BUFFER_BARRIER_BIT                           0x4000
#define GL_BUFFER_IMMUTABLE_STORAGE                                   0x821F
#define GL_BUFFER_STORAGE_FLAGS                                       0x8220
#define GL_CLEAR_TEXTURE                                              0x9365
#define GL_LOCATION_COMPONENT                                         0x934A
#define GL_TRANSFORM_FEEDBACK_BUFFER_INDEX                            0x934B
#define GL_TRANSFORM_FEEDBACK_BUFFER_STRIDE                           0x934C
#define GL_QUERY_BUFFER                                               0x9192
#define GL_QUERY_BUFFER_BARRIER_BIT                                   0x8000
#define GL_QUERY_BUFFER_BINDING                                       0x9193
#define GL_QUERY_RESULT_NO_WAIT                                       0x9194
#define GL_MIRROR_CLAMP_TO_EDGE                                       0x8743
#define GL_CONTEXT_LOST                                               0x0507
#define GL_NEGATIVE_ONE_TO_ONE                                        0x935E
#define GL_ZERO_TO_ONE                                                0x935F
#define GL_CLIP_ORIGIN                                                0x935C
#define GL_CLIP_DEPTH_MODE                                            0x935D
#define GL_QUERY_WAIT_INVERTED                                        0x8E17
#define GL_QUERY_NO_WAIT_INVERTED                                     0x8E18
#define GL_QUERY_BY_REGION_WAIT_INVERTED                              0x8E19
#define GL_QUERY_BY_REGION_NO_WAIT_INVERTED                           0x8E1A
#define GL_MAX_CULL_DISTANCES                                         0x82F9
#define GL_MAX_COMBINED_CLIP_AND_CULL_DISTANCES                       0x82FA
#define GL_TEXTURE_TARGET                                             0x1006
#define GL_QUERY_TARGET                                               0x82EA
#define GL_GUILTY_CONTEXT_RESET                                       0x8253
#define GL_INNOCENT_CONTEXT_RESET                                     0x8254
#define GL_UNKNOWN_CONTEXT_RESET                                      0x8255
#define GL_RESET_NOTIFICATION_STRATEGY                                0x8256
#define GL_LOSE_CONTEXT_ON_RESET                                      0x8252
#define GL_NO_RESET_NOTIFICATION                                      0x8261
#define GL_CONTEXT_FLAG_ROBUST_ACCESS_BIT                             0x0004
#define GL_CONTEXT_RELEASE_BEHAVIOR                                   0x82FB
#define GL_CONTEXT_RELEASE_BEHAVIOR_FLUSH                             0x82FC
#define GL_INVALID_INDEX                                              0xFFFFFFFF
#define GL_ALL_SHADER_BITS                                            0xFFFFFFFF
#define GL_ALL_BARRIER_BITS                                           0xFFFFFFFF
