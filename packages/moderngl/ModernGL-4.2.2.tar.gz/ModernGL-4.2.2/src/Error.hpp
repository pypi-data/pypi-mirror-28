#pragma once

#include "Python.hpp"

struct MGLError {
	PyException_HEAD

	const char * filename;
	const char * function;
	int line;
};

extern PyTypeObject MGLError_Type;

void MGLError_SetTrace(const char * filename, const char * function, int line, const char * format, ...);
void MGLError_SetTrace(const char * filename, const char * function, int line, PyObject * message);

#define MGLError_Set(...) MGLError_SetTrace(__FILE__, __FUNCTION__, __LINE__, __VA_ARGS__)
