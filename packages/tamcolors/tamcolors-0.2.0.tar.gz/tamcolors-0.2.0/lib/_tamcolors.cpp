/*
#_tamcolors - Part of tamcolors
#Copyright (C) 2018  Charles McMarrow

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <Python.h>
#include <Windows.h>

HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
CONSOLE_SCREEN_BUFFER_INFO consoleInfo;
WORD saved_attributes;

static PyObject* _setColor(PyObject *self, PyObject *args) {
	int foreground;
	int background;

	if (!PyArg_ParseTuple(args, "ii", &foreground, &background)) {
		return NULL;
	}

	GetConsoleScreenBufferInfo(hConsole, &consoleInfo);
	saved_attributes = consoleInfo.wAttributes;

	int foregroundSave = saved_attributes%16;
	int backgroundSave = (saved_attributes - foregroundSave)/16;

	if (foreground == -1) {
		foreground = foregroundSave;
	}

	if (background == -1) {
	
		background = backgroundSave;
	}

	SetConsoleTextAttribute(hConsole, foreground + background*16);

	Py_RETURN_NONE;
}

static PyObject* _goToDefault(PyObject *self, PyObject *args) {

	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}

	SetConsoleTextAttribute(hConsole, saved_attributes);
	Py_RETURN_NONE;
}

static PyMethodDef _tamcolors_methods[] = {
	{
		"_setColor", _setColor, METH_VARARGS,
		"Set terminal color."
	},
	{
		"_goToDefault", _goToDefault, METH_VARARGS,
		"Go to default color."
	},

{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef _tamcolors_definition = {
	PyModuleDef_HEAD_INIT,
	"_tamcolors",
	"Can set Windows terminal color",
	-1,
	_tamcolors_methods
};

PyMODINIT_FUNC PyInit__tamcolors(void) {
	Py_Initialize();
	return PyModule_Create(&_tamcolors_definition);
}