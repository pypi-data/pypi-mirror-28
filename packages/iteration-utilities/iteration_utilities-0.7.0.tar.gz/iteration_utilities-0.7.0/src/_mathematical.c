/******************************************************************************
 * Licensed under Apache License Version 2.0 - see LICENSE
 *****************************************************************************/

/******************************************************************************
 * partial-like functions:
 *
 * square     : lambda value: value ** 2
 * double     : lambda value: value * 2
 * reciprocal : lambda value: 1 / value
 *****************************************************************************/

static PyObject *
PyIU_MathSquare(PyObject *m,
                PyObject *o)
{
    return PyNumber_Power(o, PyIU_global_two, Py_None);
}

static PyObject *
PyIU_MathDouble(PyObject *m,
                PyObject *o)
{
    return PyNumber_Multiply(o, PyIU_global_two);
}

static PyObject *
PyIU_MathReciprocal(PyObject *m,
                    PyObject *o)
{
    return PyNumber_TrueDivide(PyIU_global_one, o);
}

/******************************************************************************
 * Reverse arithmetic operators:
 *
 * radd  : lambda o1, o2: o2 + o1
 * rsub  : lambda o1, o2: o2 - o1
 * rmul  : lambda o1, o2: o2 * o1
 * rdiv  : lambda o1, o2: o2 / o1
 * rfdiv : lambda o1, o2: o2 // o1
 * rpow  : lambda o1, o2: o2 ** o1
 * rmod  : lambda o1, o2: o2 % o1
 *****************************************************************************/

static PyObject *
PyIU_MathRadd(PyObject *m,
              PyObject *args)
{
    PyObject *op1, *op2;
    if (PyArg_UnpackTuple(args, "radd", 2, 2, &op1, &op2)) {
        return PyNumber_Add(op2, op1);
    } else {
        return NULL;
    }
}

static PyObject *
PyIU_MathRsub(PyObject *m,
              PyObject *args)
{
    PyObject *op1, *op2;
    if (PyArg_UnpackTuple(args, "rsub", 2, 2, &op1, &op2)) {
        return PyNumber_Subtract(op2, op1);
    } else {
        return NULL;
    }
}

static PyObject *
PyIU_MathRmul(PyObject *m,
              PyObject *args)
{
    PyObject *op1, *op2;
    if (PyArg_UnpackTuple(args, "rmul", 2, 2, &op1, &op2)) {
        return PyNumber_Multiply(op2, op1);
    } else {
        return NULL;
    }
}

static PyObject *
PyIU_MathRdiv(PyObject *m,
              PyObject *args)
{
    PyObject *op1, *op2;
    if (PyArg_UnpackTuple(args, "rdiv", 2, 2, &op1, &op2)) {
        return PyNumber_TrueDivide(op2, op1);
    } else {
        return NULL;
    }
}

static PyObject *
PyIU_MathRfdiv(PyObject *m,
               PyObject *args)
{
    PyObject *op1, *op2;
    if (PyArg_UnpackTuple(args, "rfdiv", 2, 2, &op1, &op2)) {
        return PyNumber_FloorDivide(op2, op1);
    } else {
        return NULL;
    }
}

static PyObject *
PyIU_MathRpow(PyObject *m,
              PyObject *args)
{
    PyObject *op1, *op2;
    if (PyArg_UnpackTuple(args, "rpow", 2, 2, &op1, &op2)) {
        return PyNumber_Power(op2, op1, Py_None);
    } else {
        return NULL;
    }
}

static PyObject *
PyIU_MathRmod(PyObject *m,
              PyObject *args)
{
    PyObject *op1, *op2;
    if (PyArg_UnpackTuple(args, "rmod", 2, 2, &op1, &op2)) {
        return PyNumber_Remainder(op2, op1);
    } else {
        return NULL;
    }
}
