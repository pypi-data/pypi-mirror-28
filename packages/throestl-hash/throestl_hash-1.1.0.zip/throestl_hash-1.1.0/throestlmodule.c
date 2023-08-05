#include <Python.h>

#ifdef _MSC_VER
    typedef unsigned __int32 uint32_t;
    typedef __int32 int32_t;
    typedef __int64 int64_t;
#else
    #include <stdint.h>
#endif

#include "sph_groestl.h"

static void ThroestlHash(const char *input, int length, char *output)
{
    uint32_t hashA[16], hashB[16], hashC[16];
    
    sph_groestl512_context ctx_groestl[3];

    sph_groestl512_init(&ctx_groestl[0]);
    sph_groestl512 (&ctx_groestl[0], input, length); 
    sph_groestl512_close(&ctx_groestl[0], hashA);
    
    sph_groestl512_init(&ctx_groestl[1]);
    sph_groestl512 (&ctx_groestl[1], hashA, 64); 
    sph_groestl512_close(&ctx_groestl[1], hashB); 
    
    
    sph_groestl512_init(&ctx_groestl[2]);
    sph_groestl512 (&ctx_groestl[2], hashB, 64); 
    sph_groestl512_close(&ctx_groestl[2], hashC); 
    
    memcpy(output, hashC, 32);
}

static PyObject *throestl_gethash(PyObject *self, PyObject *args)
{
    char *output;
    PyObject *value;
#if PY_MAJOR_VERSION >= 3
    PyBytesObject *input;
#else
    PyStringObject *input;
#endif
    int length;
    if (!PyArg_ParseTuple(args, "Si", &input, &length))
        return NULL;
    Py_INCREF(input);
    output = PyMem_Malloc(32);

#if PY_MAJOR_VERSION >= 3
    ThroestlHash((char *)PyBytes_AsString((PyObject*) input), length, output);
#else
    ThroestlHash((char *)PyString_AsString((PyObject*) input), length, output);
#endif
    Py_DECREF(input);
#if PY_MAJOR_VERSION >= 3
    value = Py_BuildValue("y#", output, 32);
#else
    value = Py_BuildValue("s#", output, 32);
#endif
    PyMem_Free(output);
    return value;
}

static PyMethodDef ThroestlMethods[] = {
    { "getHash", throestl_gethash, METH_VARARGS, "Returns the throestl hash" },
    { NULL, NULL, 0, NULL }
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef ThroestlModule = {
    PyModuleDef_HEAD_INIT,
    "throestl_hash",
    "...",
    -1,
    ThroestlMethods
};

PyMODINIT_FUNC PyInit_throestl_hash(void) {
    return PyModule_Create(&ThroestlModule);
}

#else

PyMODINIT_FUNC initthroestl_hash(void) {
    (void) Py_InitModule("throestl_hash", ThroestlMethods);
}
#endif
