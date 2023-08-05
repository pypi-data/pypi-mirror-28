#include <Python.h>

int _is_numeric(const char *str) {
	int str_len = strlen(str);
	int dot_flag = 0;
	int cursor;
	int ascii_value;
	
	if (*(str) == 0) {
	  return 0;
	}
	
	for (cursor = 0; cursor < str_len; cursor++) {
		ascii_value = (int)*(str + cursor);
		if (ascii_value == 46 && dot_flag == 1) {
			return 0;
		}
		if ((ascii_value == 46 && cursor == 0) || (ascii_value == 46 && cursor == str_len - 1)) {
			return 0;
		}
		if (ascii_value == 46 && dot_flag == 0) {
			dot_flag = 1;
			continue;
		}
		if (ascii_value < 48 || ascii_value > 57) {
			return 0;
		}
	}
	
	return 1;
}

static PyObject* is_numeric(PyObject* self, PyObject *args) {
   const char *str;
   
   if (!PyArg_ParseTuple(args, "s", &str)) {
      return Py_BuildValue("s", "is_numeric is expecting a single string argument");
   }

   return Py_BuildValue("i", _is_numeric(str));
}

static PyMethodDef strextnd_methods[] = {
   { "is_numeric", is_numeric, METH_VARARGS, "check if a string represents a number" },
   { NULL, NULL, 0, NULL }
};

static struct PyModuleDef is_numeric_definition = { 
    PyModuleDef_HEAD_INIT,
    "strextnd",
    "A Python module that adds funcionality to python3",
    -1, 
    strextnd_methods
};

PyMODINIT_FUNC PyInit_strextnd(void) {
   Py_Initialize();
   return PyModule_Create(&is_numeric_definition);
}
