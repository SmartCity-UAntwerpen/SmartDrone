#ifndef __NUITKA_TUPLES_H__
#define __NUITKA_TUPLES_H__

NUITKA_MAY_BE_UNUSED static PyObject *MAKE_TUPLE1( PyObject *element0 )
{
    PyObject *result = PyTuple_New( 1 );

    if (unlikely( result == NULL ))
    {
        throw PythonException();
    }

    assertObject( element0 );
    PyTuple_SET_ITEM( result, 0, INCREASE_REFCOUNT( element0 ) );

    assert( Py_REFCNT( result ) == 1 );

    return result;
}

NUITKA_MAY_BE_UNUSED static PyObject *MAKE_TUPLE2( PyObject *element0, PyObject *element1 )
{
    PyObject *result = PyTuple_New( 2 );

    if (unlikely( result == NULL ))
    {
        throw PythonException();
    }

    assertObject( element0 );
    PyTuple_SET_ITEM( result, 0, INCREASE_REFCOUNT( element0 ) );
    assertObject( element1 );
    PyTuple_SET_ITEM( result, 1, INCREASE_REFCOUNT( element1 ) );

    assert( Py_REFCNT( result ) == 1 );

    return result;
}

NUITKA_MAY_BE_UNUSED static PyObject *MAKE_TUPLE3( PyObject *element0, PyObject *element1, PyObject *element2 )
{
    PyObject *result = PyTuple_New( 3 );

    if (unlikely( result == NULL ))
    {
        throw PythonException();
    }

    assertObject( element0 );
    PyTuple_SET_ITEM( result, 0, INCREASE_REFCOUNT( element0 ) );
    assertObject( element1 );
    PyTuple_SET_ITEM( result, 1, INCREASE_REFCOUNT( element1 ) );
    assertObject( element2 );
    PyTuple_SET_ITEM( result, 2, INCREASE_REFCOUNT( element2 ) );

    assert( Py_REFCNT( result ) == 1 );

    return result;
}

NUITKA_MAY_BE_UNUSED static PyObject *MAKE_TUPLE4( PyObject *element0, PyObject *element1, PyObject *element2, PyObject *element3 )
{
    PyObject *result = PyTuple_New( 4 );

    if (unlikely( result == NULL ))
    {
        throw PythonException();
    }

    assertObject( element0 );
    PyTuple_SET_ITEM( result, 0, INCREASE_REFCOUNT( element0 ) );
    assertObject( element1 );
    PyTuple_SET_ITEM( result, 1, INCREASE_REFCOUNT( element1 ) );
    assertObject( element2 );
    PyTuple_SET_ITEM( result, 2, INCREASE_REFCOUNT( element2 ) );
    assertObject( element3 );
    PyTuple_SET_ITEM( result, 3, INCREASE_REFCOUNT( element3 ) );

    assert( Py_REFCNT( result ) == 1 );

    return result;
}

NUITKA_MAY_BE_UNUSED static PyObject *MAKE_TUPLE5( PyObject *element0, PyObject *element1, PyObject *element2, PyObject *element3, PyObject *element4 )
{
    PyObject *result = PyTuple_New( 5 );

    if (unlikely( result == NULL ))
    {
        throw PythonException();
    }

    assertObject( element0 );
    PyTuple_SET_ITEM( result, 0, INCREASE_REFCOUNT( element0 ) );
    assertObject( element1 );
    PyTuple_SET_ITEM( result, 1, INCREASE_REFCOUNT( element1 ) );
    assertObject( element2 );
    PyTuple_SET_ITEM( result, 2, INCREASE_REFCOUNT( element2 ) );
    assertObject( element3 );
    PyTuple_SET_ITEM( result, 3, INCREASE_REFCOUNT( element3 ) );
    assertObject( element4 );
    PyTuple_SET_ITEM( result, 4, INCREASE_REFCOUNT( element4 ) );

    assert( Py_REFCNT( result ) == 1 );

    return result;
}

NUITKA_MAY_BE_UNUSED static PyObject *MAKE_TUPLE6( PyObject *element0, PyObject *element1, PyObject *element2, PyObject *element3, PyObject *element4, PyObject *element5 )
{
    PyObject *result = PyTuple_New( 6 );

    if (unlikely( result == NULL ))
    {
        throw PythonException();
    }

    assertObject( element0 );
    PyTuple_SET_ITEM( result, 0, INCREASE_REFCOUNT( element0 ) );
    assertObject( element1 );
    PyTuple_SET_ITEM( result, 1, INCREASE_REFCOUNT( element1 ) );
    assertObject( element2 );
    PyTuple_SET_ITEM( result, 2, INCREASE_REFCOUNT( element2 ) );
    assertObject( element3 );
    PyTuple_SET_ITEM( result, 3, INCREASE_REFCOUNT( element3 ) );
    assertObject( element4 );
    PyTuple_SET_ITEM( result, 4, INCREASE_REFCOUNT( element4 ) );
    assertObject( element5 );
    PyTuple_SET_ITEM( result, 5, INCREASE_REFCOUNT( element5 ) );

    assert( Py_REFCNT( result ) == 1 );

    return result;
}

NUITKA_MAY_BE_UNUSED static PyObject *MAKE_TUPLE9( PyObject *element0, PyObject *element1, PyObject *element2, PyObject *element3, PyObject *element4, PyObject *element5, PyObject *element6, PyObject *element7, PyObject *element8 )
{
    PyObject *result = PyTuple_New( 9 );

    if (unlikely( result == NULL ))
    {
        throw PythonException();
    }

    assertObject( element0 );
    PyTuple_SET_ITEM( result, 0, INCREASE_REFCOUNT( element0 ) );
    assertObject( element1 );
    PyTuple_SET_ITEM( result, 1, INCREASE_REFCOUNT( element1 ) );
    assertObject( element2 );
    PyTuple_SET_ITEM( result, 2, INCREASE_REFCOUNT( element2 ) );
    assertObject( element3 );
    PyTuple_SET_ITEM( result, 3, INCREASE_REFCOUNT( element3 ) );
    assertObject( element4 );
    PyTuple_SET_ITEM( result, 4, INCREASE_REFCOUNT( element4 ) );
    assertObject( element5 );
    PyTuple_SET_ITEM( result, 5, INCREASE_REFCOUNT( element5 ) );
    assertObject( element6 );
    PyTuple_SET_ITEM( result, 6, INCREASE_REFCOUNT( element6 ) );
    assertObject( element7 );
    PyTuple_SET_ITEM( result, 7, INCREASE_REFCOUNT( element7 ) );
    assertObject( element8 );
    PyTuple_SET_ITEM( result, 8, INCREASE_REFCOUNT( element8 ) );

    assert( Py_REFCNT( result ) == 1 );

    return result;
}

NUITKA_MAY_BE_UNUSED static PyObject *MAKE_TUPLE11( PyObject *element0, PyObject *element1, PyObject *element2, PyObject *element3, PyObject *element4, PyObject *element5, PyObject *element6, PyObject *element7, PyObject *element8, PyObject *element9, PyObject *element10 )
{
    PyObject *result = PyTuple_New( 11 );

    if (unlikely( result == NULL ))
    {
        throw PythonException();
    }

    assertObject( element0 );
    PyTuple_SET_ITEM( result, 0, INCREASE_REFCOUNT( element0 ) );
    assertObject( element1 );
    PyTuple_SET_ITEM( result, 1, INCREASE_REFCOUNT( element1 ) );
    assertObject( element2 );
    PyTuple_SET_ITEM( result, 2, INCREASE_REFCOUNT( element2 ) );
    assertObject( element3 );
    PyTuple_SET_ITEM( result, 3, INCREASE_REFCOUNT( element3 ) );
    assertObject( element4 );
    PyTuple_SET_ITEM( result, 4, INCREASE_REFCOUNT( element4 ) );
    assertObject( element5 );
    PyTuple_SET_ITEM( result, 5, INCREASE_REFCOUNT( element5 ) );
    assertObject( element6 );
    PyTuple_SET_ITEM( result, 6, INCREASE_REFCOUNT( element6 ) );
    assertObject( element7 );
    PyTuple_SET_ITEM( result, 7, INCREASE_REFCOUNT( element7 ) );
    assertObject( element8 );
    PyTuple_SET_ITEM( result, 8, INCREASE_REFCOUNT( element8 ) );
    assertObject( element9 );
    PyTuple_SET_ITEM( result, 9, INCREASE_REFCOUNT( element9 ) );
    assertObject( element10 );
    PyTuple_SET_ITEM( result, 10, INCREASE_REFCOUNT( element10 ) );

    assert( Py_REFCNT( result ) == 1 );

    return result;
}

#endif
#ifndef __NUITKA_LISTS_H__
#define __NUITKA_LISTS_H__

NUITKA_MAY_BE_UNUSED static PyObject *MAKE_LIST0(  )
{
    PyObject *result = PyList_New( 0 );

    if (unlikely( result == NULL ))
    {
        throw PythonException();
    }



    assert( Py_REFCNT( result ) == 1 );

    return result;
}

NUITKA_MAY_BE_UNUSED static PyObject *MAKE_LIST1( PyObject *element0 )
{
    PyObject *result = PyList_New( 1 );

    if (unlikely( result == NULL ))
    {
        throw PythonException();
    }

    assertObject( element0 );
    PyList_SET_ITEM( result, 0, element0 );

    assert( Py_REFCNT( result ) == 1 );

    return result;
}

#endif
#ifndef __NUITKA_DICTS_H__
#define __NUITKA_DICTS_H__

NUITKA_MAY_BE_UNUSED static PyObject *MAKE_DICT0(  )
{
    PyObject *result = _PyDict_NewPresized( 0 );

    if (unlikely( result == NULL ))
    {
        throw PythonException();
    }



    assert( Py_REFCNT( result ) == 1 );

    return result;
}

NUITKA_MAY_BE_UNUSED static PyObject *MAKE_DICT1( PyObject *value1, PyObject *key1 )
{
    PyObject *result = _PyDict_NewPresized( 1 );

    if (unlikely( result == NULL ))
    {
        throw PythonException();
    }

    assertObject( key1 );
    assertObject( value1 );

    {
        int status = PyDict_SetItem( result, key1, value1 );

        if (unlikely( status == -1 ))
        {
            throw PythonException();
        }
    }

    assert( Py_REFCNT( result ) == 1 );

    return result;
}

NUITKA_MAY_BE_UNUSED static PyObject *MAKE_DICT2( PyObject *value1, PyObject *key1, PyObject *value2, PyObject *key2 )
{
    PyObject *result = _PyDict_NewPresized( 2 );

    if (unlikely( result == NULL ))
    {
        throw PythonException();
    }

    assertObject( key1 );
    assertObject( value1 );

    {
        int status = PyDict_SetItem( result, key1, value1 );

        if (unlikely( status == -1 ))
        {
            throw PythonException();
        }
    }
    assertObject( key2 );
    assertObject( value2 );

    {
        int status = PyDict_SetItem( result, key2, value2 );

        if (unlikely( status == -1 ))
        {
            throw PythonException();
        }
    }

    assert( Py_REFCNT( result ) == 1 );

    return result;
}

#endif
#ifndef __NUITKA_SETS_H__
#define __NUITKA_SETS_H__


#endif
#ifndef __NUITKA_CALLS_H__
#define __NUITKA_CALLS_H__

extern PyObject *CALL_FUNCTION_WITH_ARGS1( PyObject *called, PyObject *arg0 );
extern PyObject *CALL_FUNCTION_WITH_ARGS2( PyObject *called, PyObject *arg0, PyObject *arg1 );
extern PyObject *CALL_FUNCTION_WITH_ARGS3( PyObject *called, PyObject *arg0, PyObject *arg1, PyObject *arg2 );
extern PyObject *CALL_FUNCTION_WITH_ARGS4( PyObject *called, PyObject *arg0, PyObject *arg1, PyObject *arg2, PyObject *arg3 );
#endif
