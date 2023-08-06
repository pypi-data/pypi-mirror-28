#include <Python.h>

int _is_numeric(char *str) {
	int dot_flag = 0;
	int all_zeros = 1;
	int leading_minus = 0;
	int cursor;
	int ascii_value;
	
	if (((int)*(str) < 48 || (int)*(str) > 57) && *(str) != 45) {
	  return 0;
	}
	
	if ((int)*(str) == 45 && (int)*(str + 1) == 48 && *(str + 2) == 0) {
	  return 0;
	}
	
	if ((int)*(str) == 45) {
	  leading_minus = 1;
	}
	
	for (cursor = 1; *(str + cursor) != 0; cursor++) {
		ascii_value = (int)*(str + cursor);
		if (ascii_value == 46 && dot_flag == 1) {
			return 0;
		}
		if (ascii_value == 46 && *(str + cursor + 1) == 0) {
			return 0;
		}
		if (ascii_value == 46 && dot_flag == 0) {
			dot_flag = 1;
			continue;
		}
		if (ascii_value < 48 || ascii_value > 57) {
			return 0;
		}
		
		if (ascii_value != 48) {
		  all_zeros = 0;
		}
	}
	
	if (all_zeros == 1 && leading_minus == 1) {
	  return 0;
	}
	
	return 1;
}

static PyObject* is_numeric(PyObject* self, PyObject *args) {
   const char *str;
   
   if (!PyArg_ParseTuple(args, "s", &str)) {
      return Py_BuildValue("s", "is_numeric is expecting a single string argument");
   }

   if(_is_numeric(str)) {
	   return Py_True;
   }
   else {
	   return Py_False;
   }
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