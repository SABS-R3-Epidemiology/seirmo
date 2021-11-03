#define PI_SSIZE_T_CLEAN
#include <python3.8/Python.h>

double square(double x) { return x*x; }

static PyObject* method_square(PyObject* self, PyObject* args)
{
    double x;
    if (!PyArg_ParseTuple(args, "d", &x)) return NULL;

    return PyFloat_FromDouble(x * x);
}


static PyMethodDef PySquareMethods[] = {
    {"square", method_square, METH_VARARGS, "Python interface for square C++ library function"},
};

static struct PyModuleDef squaremodule = {
    PyModuleDef_HEAD_INIT,
    "square",
    "Python interface for the square C++ library function",
    -1,
    PySquareMethods
};

PyMODINIT_FUNC PyInit_square(void){
    return PyModule_Create(&squaremodule);
}
