// Generated code for Python source for module '__main__'
// created by Nuitka version 0.5.0.1

// This code is in part copyright 2013 Kay Hayen.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "nuitka/prelude.hpp"

#include "__modules.hpp"
#include "__constants.hpp"
#include "__helpers.hpp"

// The _module___main__ is a Python object pointer of module type.

// Note: For full compatability with CPython, every module variable access
// needs to go through it except for cases where the module cannot possibly
// have changed in the mean time.

PyObject *module___main__;
PyDictObject *moduledict___main__;

NUITKA_MAY_BE_UNUSED static PyObject *GET_MODULE_VALUE0( PyObject *var_name )
{
    // For module variable values, need to lookup in module dictionary or in
    // built-in dictionary.

    PyObject *result = GET_STRING_DICT_VALUE( moduledict___main__, (Nuitka_StringObject *)var_name );

    if (likely( result != NULL ))
    {
        assertObject( result );

        return result;
    }

    result = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)var_name );

    if (likely( result != NULL ))
    {
        assertObject( result );

        return result;
    }

    PyErr_Format( PyExc_NameError, "global name '%s' is not defined", Nuitka_String_AsString(var_name ));
    throw PythonException();
}

NUITKA_MAY_BE_UNUSED static PyObject *GET_MODULE_VALUE1( PyObject *var_name )
{
    return INCREASE_REFCOUNT( GET_MODULE_VALUE0( var_name ) );
}

NUITKA_MAY_BE_UNUSED void static DEL_MODULE_VALUE( PyObject *var_name, bool tolerant )
{
    int status = PyDict_DelItem( (PyObject *)moduledict___main__, var_name );

    if (unlikely( status == -1 && tolerant == false ))
    {
        PyErr_Format(
            PyExc_NameError,
            "global name '%s' is not defined",
            Nuitka_String_AsString( var_name )
        );

        throw PythonException();
    }
}

NUITKA_MAY_BE_UNUSED static PyObject *GET_LOCALS_OR_MODULE_VALUE0( PyObject *locals_dict, PyObject *var_name )
{
    PyObject *result = PyDict_GetItem( locals_dict, var_name );

    if ( result != NULL )
    {
        return result;
    }
    else
    {
        return GET_MODULE_VALUE0( var_name );
    }
}

NUITKA_MAY_BE_UNUSED static PyObject *GET_LOCALS_OR_MODULE_VALUE1( PyObject *locals_dict, PyObject *var_name )
{
    PyObject *result = PyDict_GetItem( locals_dict, var_name );

    if ( result != NULL )
    {
        return INCREASE_REFCOUNT( result );
    }
    else
    {
        return GET_MODULE_VALUE1( var_name );
    }
}

// The module function declarations.
static PyObject *MAKE_FUNCTION_function_1_logger_thread_worker_of_module___main__(  );


static PyObject *MAKE_FUNCTION_function_1_signal_handler_of_function_2_main_function_of_module___main__( PyObjectSharedLocalVariable &closure_aborted_list, PyObjectSharedLocalVariable &closure_cf, PyObjectSharedLocalVariable &closure_mc, PyObjectSharedLocalVariable &closure_scf );


// This structure is for attachment as self of function_1_signal_handler_of_function_2_main_function_of_module___main__.
// It is allocated at the time the function object is created.
struct _context_function_1_signal_handler_of_function_2_main_function_of_module___main___t
{
    // The function can access a read-only closure of the creator.
    PyObjectClosureVariable closure_aborted_list;
    PyObjectClosureVariable closure_cf;
    PyObjectClosureVariable closure_mc;
    PyObjectClosureVariable closure_scf;
};

static void _context_function_1_signal_handler_of_function_2_main_function_of_module___main___destructor( void *context_voidptr )
{
    _context_function_1_signal_handler_of_function_2_main_function_of_module___main___t *_python_context = (_context_function_1_signal_handler_of_function_2_main_function_of_module___main___t *)context_voidptr;



    delete _python_context;
}


static PyObject *MAKE_FUNCTION_function_2_main_function_of_module___main__(  );


// The module function definitions.
static PyObject *impl_function_1_logger_thread_worker_of_module___main__( Nuitka_FunctionObject *self, PyObject *_python_par_logger )
{
    // No context is used.

    // Local variable declarations.
    PyObjectLocalParameterVariableNoDel par_logger( const_str_plain_logger, _python_par_logger );
    PyObjectLocalVariable var_posfile( const_str_plain_posfile );
    PyObjectLocalVariable var_log_entry( const_str_plain_log_entry );
    PyObjectLocalVariable var_timestamp( const_str_plain_timestamp );
    PyObjectLocalVariable var_data( const_str_plain_data );
    PyObjectLocalVariable var_px( const_str_plain_px );
    PyObjectLocalVariable var_py( const_str_plain_py );
    PyObjectLocalVariable var_pz( const_str_plain_pz );
    PyObjectLocalVariable var_roll( const_str_plain_roll );
    PyObjectLocalVariable var_pitch( const_str_plain_pitch );
    PyObjectLocalVariable var_yaw( const_str_plain_yaw );
    PyObjectTempVariable tmp_for_loop_1__iter_value;

    // Actual function code.
    static PyFrameObject *frame_function_1_logger_thread_worker_of_module___main__ = NULL;

    if ( isFrameUnusable( frame_function_1_logger_thread_worker_of_module___main__ ) )
    {
        if ( frame_function_1_logger_thread_worker_of_module___main__ )
        {
#if _DEBUG_REFRAME
            puts( "reframe for function_1_logger_thread_worker_of_module___main__" );
#endif
            Py_DECREF( frame_function_1_logger_thread_worker_of_module___main__ );
        }

        frame_function_1_logger_thread_worker_of_module___main__ = MAKE_FRAME( codeobj_5ca39b17b9682cc8ca19997fc3ea65f4, module___main__ );
    }

    FrameGuard frame_guard( frame_function_1_logger_thread_worker_of_module___main__ );
    try
    {
        assert( Py_REFCNT( frame_function_1_logger_thread_worker_of_module___main__ ) == 2 ); // Frame stack
        frame_guard.setLineNumber( 22 );
        var_posfile.assign1( OPEN_FILE( const_str_plain_posfile, const_str_plain_w, NULL ) );
        while( true )
        {
            frame_guard.setLineNumber( 23 );
            if ( (!( (!( CHECK_IF_TRUE( PyObjectTemporary( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_logger_thread_stop ), const_str_plain_is_set ) ).asObject0() ) ).asObject0() ) )) )) )
            {
                break;
            }
            frame_guard.setLineNumber( 24 );
            PyObjectTemporaryWithDel tmp_for_loop_1__for_iterator( MAKE_ITERATOR( par_logger.asObject0() ) );
            PythonExceptionKeeper _caught_1;
#if PYTHON_VERSION < 300
            int _at_lineno_1 = 0;
#endif


            try
            {
                // Tried block:
                while( true )
                {
                    frame_guard.setLineNumber( 24 );
                    PyObject *_tmp_unpack_2 = ITERATOR_NEXT( tmp_for_loop_1__for_iterator.asObject0() );

                    if ( _tmp_unpack_2 == NULL )
                    {
                        break;
                    }
                    tmp_for_loop_1__iter_value.assign1( _tmp_unpack_2 );
                    var_log_entry.assign0( tmp_for_loop_1__iter_value.asObject0() );
                    frame_guard.setLineNumber( 25 );
                    var_timestamp.assign1( LOOKUP_SUBSCRIPT_CONST( var_log_entry.asObject0(), const_int_0, 0 ) );
                    frame_guard.setLineNumber( 26 );
                    var_data.assign1( LOOKUP_SUBSCRIPT_CONST( var_log_entry.asObject0(), const_int_pos_1, 1 ) );
                    frame_guard.setLineNumber( 28 );
                    var_px.assign1( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_data.asObject0(), const_str_plain_get ) ).asObject0(), const_str_digest_6cc08d0712c8d9467d68c797bc086fed ) );
                    frame_guard.setLineNumber( 29 );
                    var_py.assign1( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_data.asObject0(), const_str_plain_get ) ).asObject0(), const_str_digest_f991bf363475592a622e85cda89309dc ) );
                    frame_guard.setLineNumber( 30 );
                    var_pz.assign1( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_data.asObject0(), const_str_plain_get ) ).asObject0(), const_str_digest_bb098d44f0e169e5eb07c575224d8553 ) );
                    frame_guard.setLineNumber( 31 );
                    var_roll.assign1( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_data.asObject0(), const_str_plain_get ) ).asObject0(), const_str_digest_a4d5e4010a0ee714d42205db4918cf2b ) );
                    frame_guard.setLineNumber( 32 );
                    var_pitch.assign1( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_data.asObject0(), const_str_plain_get ) ).asObject0(), const_str_digest_7390cc453f512da13f0d281a65059885 ) );
                    frame_guard.setLineNumber( 33 );
                    var_yaw.assign1( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_data.asObject0(), const_str_plain_get ) ).asObject0(), const_str_digest_d2f986057c6f7103b7ca87474919f5c2 ) );
                    frame_guard.setLineNumber( 35 );
                    {
                        PyObjectTempKeeper1 call1;
                        PyObjectTempKeeper0 make_tuple1;
                        PyObjectTempKeeper0 make_tuple2;
                        PyObjectTempKeeper0 make_tuple3;
                        DECREASE_REFCOUNT( ( call1.assign( LOOKUP_ATTRIBUTE( var_posfile.asObject0(), const_str_plain_write ) ), CALL_FUNCTION_WITH_ARGS1( call1.asObject0(), PyObjectTemporary( BINARY_OPERATION_REMAINDER( const_str_digest_0c9434c1a2d38b03084e8af867a5a591, PyObjectTemporary( ( make_tuple1.assign( var_px.asObject0() ), make_tuple2.assign( var_py.asObject0() ), make_tuple3.assign( var_pz.asObject0() ), MAKE_TUPLE4( make_tuple1.asObject0(), make_tuple2.asObject0(), make_tuple3.asObject0(), var_yaw.asObject0() ) ) ).asObject0() ) ).asObject0() ) ) );
                    }
                    frame_guard.setLineNumber( 36 );
                    {
                        PyObjectTempKeeper0 make_tuple1;
                        PyObjectTempKeeper0 make_tuple2;
                        PyObjectTempKeeper0 make_tuple3;
                        PyObjectTempKeeper0 make_tuple4;
                        PyObjectTempKeeper0 make_tuple5;
                        PRINT_ITEM_TO( NULL, PyObjectTemporary( TO_STR( PyObjectTemporary( BINARY_OPERATION_REMAINDER( const_str_digest_145ace45251939555fbe881f24d19dc6, PyObjectTemporary( ( make_tuple1.assign( var_px.asObject0() ), make_tuple2.assign( var_py.asObject0() ), make_tuple3.assign( var_pz.asObject0() ), make_tuple4.assign( var_roll.asObject0() ), make_tuple5.assign( var_pitch.asObject0() ), MAKE_TUPLE6( make_tuple1.asObject0(), make_tuple2.asObject0(), make_tuple3.asObject0(), make_tuple4.asObject0(), make_tuple5.asObject0(), var_yaw.asObject0() ) ) ).asObject0() ) ).asObject0() ) ).asObject0() );
                        PRINT_NEW_LINE_TO( NULL );
                    }
                    frame_guard.setLineNumber( 37 );
                    break;

                    CONSIDER_THREADING();
                }
            }
            catch ( PythonException &_exception )
            {
#if PYTHON_VERSION >= 300
                if ( !_exception.hasTraceback() )
                {
                    _exception.setTraceback( MAKE_TRACEBACK( frame_guard.getFrame() ) );
                }
                else
                {
                    _exception.addTraceback( frame_guard.getFrame0() );
                }
#else
                _at_lineno_1 = frame_guard.getLineNumber();
#endif

                _caught_1.save( _exception );

#if PYTHON_VERSION >= 300
                frame_guard.preserveExistingException();

                _exception.toExceptionHandler();
#endif
            }

            // Final block:
            tmp_for_loop_1__iter_value.del( true );
            tmp_for_loop_1__for_iterator.del( false );
#if PYTHON_VERSION < 300
            if ( _at_lineno_1 != 0 )
            {
               frame_guard.setLineNumber( _at_lineno_1 );
            }
#endif
            _caught_1.rethrow();
            // Final end
            frame_guard.setLineNumber( 38 );
            DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_time ), const_str_plain_sleep ) ).asObject0(), const_float_0_1 ) );

            CONSIDER_THREADING();
        }
        frame_guard.setLineNumber( 39 );
        DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_posfile.asObject0(), const_str_plain_close ) ).asObject0() ) );
    }
    catch ( PythonException &_exception )
    {
        if ( !_exception.hasTraceback() )
        {
            _exception.setTraceback( MAKE_TRACEBACK( frame_guard.getFrame() ) );
        }
        else
        {
            _exception.addTraceback( frame_guard.getFrame0() );
        }

        Py_XDECREF( frame_guard.getFrame0()->f_locals );
        frame_guard.getFrame0()->f_locals = par_logger.updateLocalsDict( var_yaw.updateLocalsDict( var_pitch.updateLocalsDict( var_roll.updateLocalsDict( var_pz.updateLocalsDict( var_py.updateLocalsDict( var_px.updateLocalsDict( var_data.updateLocalsDict( var_timestamp.updateLocalsDict( var_log_entry.updateLocalsDict( var_posfile.updateLocalsDict( PyDict_New() ) ) ) ) ) ) ) ) ) ) );

        if ( frame_guard.getFrame0() == frame_function_1_logger_thread_worker_of_module___main__ )
        {
           Py_DECREF( frame_function_1_logger_thread_worker_of_module___main__ );
           frame_function_1_logger_thread_worker_of_module___main__ = NULL;
        }

        _exception.toPython();
        return NULL;
    }
    return INCREASE_REFCOUNT( Py_None );
}
static PyObject *fparse_function_1_logger_thread_worker_of_module___main__( Nuitka_FunctionObject *self, PyObject **args, Py_ssize_t args_size, PyObject *kw )
{
    assert( kw == NULL || PyDict_Check( kw ) );

    NUITKA_MAY_BE_UNUSED Py_ssize_t kw_size = kw ? PyDict_Size( kw ) : 0;
    NUITKA_MAY_BE_UNUSED Py_ssize_t kw_found = 0;
    NUITKA_MAY_BE_UNUSED Py_ssize_t kw_only_found = 0;
    Py_ssize_t args_given = args_size;
    PyObject *_python_par_logger = NULL;
    // Copy given dictionary values to the the respective variables:
    if ( kw_size > 0 )
    {
        Py_ssize_t ppos = 0;
        PyObject *key, *value;

        while( PyDict_Next( kw, &ppos, &key, &value ) )
        {
#if PYTHON_VERSION < 300
            if (unlikely( !PyString_Check( key ) && !PyUnicode_Check( key ) ))
#else
            if (unlikely( !PyUnicode_Check( key ) ))
#endif
            {
                PyErr_Format( PyExc_TypeError, "logger_thread_worker() keywords must be strings" );
                goto error_exit;
            }

            NUITKA_MAY_BE_UNUSED bool found = false;

            Py_INCREF( key );
            Py_INCREF( value );

            // Quick path, could be our value.
            if ( found == false && const_str_plain_logger == key )
            {
                assert( _python_par_logger == NULL );
                _python_par_logger = value;

                found = true;
                kw_found += 1;
            }

            // Slow path, compare against all parameter names.
            if ( found == false && RICH_COMPARE_BOOL_EQ_PARAMETERS( const_str_plain_logger, key ) )
            {
                assert( _python_par_logger == NULL );
                _python_par_logger = value;

                found = true;
                kw_found += 1;
            }


            Py_DECREF( key );

            if ( found == false )
            {
               Py_DECREF( value );

               PyErr_Format(
                   PyExc_TypeError,
                   "logger_thread_worker() got an unexpected keyword argument '%s'",
                   Nuitka_String_Check( key ) ? Nuitka_String_AsString( key ) : "<non-string>"
               );

               goto error_exit;
            }
        }

#if PYTHON_VERSION < 300
        assert( kw_found == kw_size );
        assert( kw_only_found == 0 );
#endif
    }

    // Check if too many arguments were given in case of non star args
    if (unlikely( args_given > 1 ))
    {
#if PYTHON_VERSION < 270
        ERROR_TOO_MANY_ARGUMENTS( self, args_given, kw_size );
#elif PYTHON_VERSION < 330
        ERROR_TOO_MANY_ARGUMENTS( self, args_given + kw_found );
#else
        ERROR_TOO_MANY_ARGUMENTS( self, args_given, kw_only_found );
#endif
        goto error_exit;
    }


    // Copy normal parameter values given as part of the args list to the respective variables:

    if (likely( 0 < args_given ))
    {
         if (unlikely( _python_par_logger != NULL ))
         {
             ERROR_MULTIPLE_VALUES( self, 0 );
             goto error_exit;
         }

        _python_par_logger = INCREASE_REFCOUNT( args[ 0 ] );
    }
    else if ( _python_par_logger == NULL )
    {
        if ( 0 + self->m_defaults_given >= 1  )
        {
            _python_par_logger = INCREASE_REFCOUNT( PyTuple_GET_ITEM( self->m_defaults, self->m_defaults_given + 0 - 1 ) );
        }
#if PYTHON_VERSION < 330
        else
        {
#if PYTHON_VERSION < 270
            ERROR_TOO_FEW_ARGUMENTS( self, kw_size, args_given + kw_found );
#elif PYTHON_VERSION < 300
            ERROR_TOO_FEW_ARGUMENTS( self, args_given + kw_found );
#else
            ERROR_TOO_FEW_ARGUMENTS( self, args_given + kw_found - kw_only_found );
#endif

            goto error_exit;
        }
#endif
    }

#if PYTHON_VERSION >= 330
    if (unlikely( _python_par_logger == NULL ))
    {
        PyObject *values[] = { _python_par_logger };
        ERROR_TOO_FEW_ARGUMENTS( self, values );

        goto error_exit;
    }
#endif


    return impl_function_1_logger_thread_worker_of_module___main__( self, _python_par_logger );

error_exit:;

    Py_XDECREF( _python_par_logger );

    return NULL;
}

static PyObject *dparse_function_1_logger_thread_worker_of_module___main__( Nuitka_FunctionObject *self, PyObject **args, int size )
{
    if ( size == 1 )
    {
        return impl_function_1_logger_thread_worker_of_module___main__( self, INCREASE_REFCOUNT( args[ 0 ] ) );
    }
    else
    {
        PyObject *result = fparse_function_1_logger_thread_worker_of_module___main__( self, args, size, NULL );
        return result;
    }

}



static PyObject *impl_function_2_main_function_of_module___main__( Nuitka_FunctionObject *self )
{
    // No context is used.

    // Local variable declarations.
    PyObjectLocalVariable var_URI( const_str_plain_URI );
    PyObjectLocalVariable var_lg_stab( const_str_plain_lg_stab );
    PyObjectSharedLocalVariable var_cf( const_str_plain_cf );
    PyObjectSharedLocalVariable var_scf( const_str_plain_scf );
    PyObjectSharedLocalVariable var_mc( const_str_plain_mc );
    PyObjectLocalVariable var_logger( const_str_plain_logger );
    PyObjectLocalVariable var_logger_thread( const_str_plain_logger_thread );
    PyObjectSharedLocalVariable var_aborted_list( const_str_plain_aborted_list );
    PyObjectLocalVariable var_signal_handler( const_str_plain_signal_handler );

    // Actual function code.
    var_URI.assign0( const_str_digest_e9fa29284a0eebe10618a41a87657254 );
    static PyFrameObject *frame_function_2_main_function_of_module___main__ = NULL;

    if ( isFrameUnusable( frame_function_2_main_function_of_module___main__ ) )
    {
        if ( frame_function_2_main_function_of_module___main__ )
        {
#if _DEBUG_REFRAME
            puts( "reframe for function_2_main_function_of_module___main__" );
#endif
            Py_DECREF( frame_function_2_main_function_of_module___main__ );
        }

        frame_function_2_main_function_of_module___main__ = MAKE_FRAME( codeobj_b6866d1d3dae1aec7ae569970b6db7dd, module___main__ );
    }

    FrameGuard frame_guard( frame_function_2_main_function_of_module___main__ );
    try
    {
        assert( Py_REFCNT( frame_function_2_main_function_of_module___main__ ) == 2 ); // Frame stack
        frame_guard.setLineNumber( 52 );
        {
            PyObjectTempKeeper1 call1;
            DECREASE_REFCOUNT( ( call1.assign( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_logging ), const_str_plain_basicConfig ) ), CALL_FUNCTION( call1.asObject0(), const_tuple_empty, PyObjectTemporary( MAKE_DICT1( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_logging ), const_str_plain_ERROR ) ).asObject0(), const_str_plain_level ) ).asObject0() ) ) );
        }
        frame_guard.setLineNumber( 56 );
        DECREASE_REFCOUNT( CALL_FUNCTION( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_cflib ), const_str_plain_crtp ) ).asObject0(), const_str_plain_init_drivers ) ).asObject0(), const_tuple_empty, PyObjectTemporary( PyDict_Copy( const_dict_539d0a0b95c7f4877f43e57e4ab8d984 ) ).asObject0() ) );
        frame_guard.setLineNumber( 57 );
        PRINT_ITEM_TO( NULL, const_str_digest_60a23ecc05ca99686bc518474cb1df7a );
        PRINT_NEW_LINE_TO( NULL );
        frame_guard.setLineNumber( 58 );
        var_lg_stab.assign1( CALL_FUNCTION( GET_MODULE_VALUE0( const_str_plain_LogConfig ), const_tuple_empty, PyObjectTemporary( PyDict_Copy( const_dict_ce98f68090408fb17a6c2e7f34cf931d ) ).asObject0() ) );
        frame_guard.setLineNumber( 59 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_lg_stab.asObject0(), const_str_plain_add_variable ) ).asObject0(), const_str_digest_6cc08d0712c8d9467d68c797bc086fed, const_str_plain_float ) );
        frame_guard.setLineNumber( 60 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_lg_stab.asObject0(), const_str_plain_add_variable ) ).asObject0(), const_str_digest_f991bf363475592a622e85cda89309dc, const_str_plain_float ) );
        frame_guard.setLineNumber( 61 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_lg_stab.asObject0(), const_str_plain_add_variable ) ).asObject0(), const_str_digest_bb098d44f0e169e5eb07c575224d8553, const_str_plain_float ) );
        frame_guard.setLineNumber( 62 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_lg_stab.asObject0(), const_str_plain_add_variable ) ).asObject0(), const_str_digest_a4d5e4010a0ee714d42205db4918cf2b, const_str_plain_float ) );
        frame_guard.setLineNumber( 63 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_lg_stab.asObject0(), const_str_plain_add_variable ) ).asObject0(), const_str_digest_7390cc453f512da13f0d281a65059885, const_str_plain_float ) );
        frame_guard.setLineNumber( 64 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_lg_stab.asObject0(), const_str_plain_add_variable ) ).asObject0(), const_str_digest_d2f986057c6f7103b7ca87474919f5c2, const_str_plain_float ) );
        frame_guard.setLineNumber( 67 );
        var_cf.assign1( CALL_FUNCTION( GET_MODULE_VALUE0( const_str_plain_Crazyflie ), const_tuple_empty, PyObjectTemporary( PyDict_Copy( const_dict_243aa8eecd2da5a46892332cfdc4d450 ) ).asObject0() ) );
        frame_guard.setLineNumber( 68 );
        {
            PyObjectTempKeeper0 call1;
            PyObjectTempKeeper1 call2;
            var_scf.assign1( ( call1.assign( GET_MODULE_VALUE0( const_str_plain_SyncCrazyflie ) ), call2.assign( MAKE_TUPLE1( var_URI.asObject0() ) ), CALL_FUNCTION( call1.asObject0(), call2.asObject0(), PyObjectTemporary( MAKE_DICT1( var_cf.asObject0(), const_str_plain_cf ) ).asObject0() ) ) );
        }
        frame_guard.setLineNumber( 69 );
        DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_scf.asObject0(), const_str_plain_open_link ) ).asObject0() ) );
        frame_guard.setLineNumber( 70 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_time ), const_str_plain_sleep ) ).asObject0(), const_int_pos_5 ) );
        frame_guard.setLineNumber( 71 );
        PRINT_ITEM_TO( NULL, const_str_digest_a2c1833e0fd5389050407cccd2b5fa06 );
        PRINT_NEW_LINE_TO( NULL );
        frame_guard.setLineNumber( 72 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_68a9ac2f1f2f7e49c7bad57ba31976f6, const_str_plain_0 ) );
        frame_guard.setLineNumber( 73 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_b064bc73fc5d82cb15ddbd6cb7eeb804, const_str_plain_15 ) );
        frame_guard.setLineNumber( 74 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_bb9871a70568c3d29995e4ee517f0c1d, const_str_plain_15 ) );
        frame_guard.setLineNumber( 75 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_2930a74bfe0dfc7d45d37b747109010a, const_str_plain_20000 ) );
        frame_guard.setLineNumber( 78 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_4e2c018a5300351973557add0a24141a, const_str_plain_20 ) );
        frame_guard.setLineNumber( 79 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_cc876ca77c133b1ab9057ea27426e8d3, const_str_plain_20 ) );
        frame_guard.setLineNumber( 80 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_da28a3a52fef5cfcfe6516207c87623e, const_str_digest_04817efd11c15364a6ec239780038862 ) );
        frame_guard.setLineNumber( 81 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_e7511362545f1e8e4835d7768b8645c2, const_str_digest_77e23e10fe1b9556624317a002d8b1cc ) );
        frame_guard.setLineNumber( 82 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_c38568aedd7bb1c9232846890b69ebc7, const_str_digest_2f68ad040984e87524a290e4cb58117f ) );
        frame_guard.setLineNumber( 83 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_24d1b912a24567d4b0f37e65866caec4, const_str_digest_04817efd11c15364a6ec239780038862 ) );
        frame_guard.setLineNumber( 84 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_2d0bc760d21081fbbe357ac9bd3098d1, const_str_digest_77e23e10fe1b9556624317a002d8b1cc ) );
        frame_guard.setLineNumber( 85 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_6fcf7cef0081a3be07ee72eeaf847b1f, const_str_digest_2f68ad040984e87524a290e4cb58117f ) );
        frame_guard.setLineNumber( 86 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_b03c2e2c3dee02212866e618daae5997, const_str_digest_44c948084dd4e5ab67b1ec497d101727 ) );
        frame_guard.setLineNumber( 87 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_bd56e81c8f1ef1514e78dc5e67b5b1a2, const_str_digest_44c948084dd4e5ab67b1ec497d101727 ) );
        frame_guard.setLineNumber( 89 );
        PRINT_ITEM_TO( NULL, const_str_digest_6fae5998bcb63ea7f2ecb4f9dea2b2a7 );
        PRINT_NEW_LINE_TO( NULL );
        frame_guard.setLineNumber( 94 );
        {
            PyObjectTempKeeper0 call1;
            var_mc.assign1( ( call1.assign( GET_MODULE_VALUE0( const_str_plain_MotionCommander ) ), CALL_FUNCTION_WITH_ARGS1( call1.asObject0(), var_scf.asObject0() ) ) );
        }
        frame_guard.setLineNumber( 95 );
        PRINT_ITEM_TO( NULL, const_str_digest_0345aa3382d9cabb03624fa419361084 );
        PRINT_NEW_LINE_TO( NULL );
        frame_guard.setLineNumber( 98 );
        {
            PyObjectTempKeeper0 call1;
            PyObjectTempKeeper0 call2;
            var_logger.assign1( ( call1.assign( GET_MODULE_VALUE0( const_str_plain_SyncLogger ) ), call2.assign( var_scf.asObject0() ), CALL_FUNCTION_WITH_ARGS2( call1.asObject0(), call2.asObject0(), var_lg_stab.asObject0() ) ) );
        }
        frame_guard.setLineNumber( 99 );
        DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_logger.asObject0(), const_str_plain_connect ) ).asObject0() ) );
        frame_guard.setLineNumber( 100 );
        {
            PyObjectTempKeeper0 call1;
            PyObjectTempKeeper0 make_dict1;
            var_logger_thread.assign1( ( call1.assign( GET_MODULE_VALUE0( const_str_plain_Thread ) ), CALL_FUNCTION( call1.asObject0(), const_tuple_empty, PyObjectTemporary( ( make_dict1.assign( GET_MODULE_VALUE0( const_str_plain_logger_thread_worker ) ), MAKE_DICT2( make_dict1.asObject0(), const_str_plain_target, PyObjectTemporary( MAKE_LIST1( var_logger.asObject1() ) ).asObject0(), const_str_plain_args ) ) ).asObject0() ) ) );
        }
        frame_guard.setLineNumber( 102 );
        DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_logger_thread.asObject0(), const_str_plain_start ) ).asObject0() ) );
        var_aborted_list.assign1( PyDict_Copy( const_dict_62ee6ebcc3c4bc4b866e8cd064cf56b7 ) );
        var_signal_handler.assign1( MAKE_FUNCTION_function_1_signal_handler_of_function_2_main_function_of_module___main__( var_aborted_list, var_cf, var_mc, var_scf ) );
        frame_guard.setLineNumber( 127 );
        {
            PyObjectTempKeeper1 call1;
            PyObjectTempKeeper1 call2;
            DECREASE_REFCOUNT( ( call1.assign( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_signal ), const_str_plain_signal ) ), call2.assign( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_signal ), const_str_plain_SIGINT ) ), CALL_FUNCTION_WITH_ARGS2( call1.asObject0(), call2.asObject0(), var_signal_handler.asObject0() ) ) );
        }
        frame_guard.setLineNumber( 131 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_mc.asObject0(), const_str_plain_take_off ) ).asObject0(), const_float_0_3, const_float_0_4 ) );
        frame_guard.setLineNumber( 132 );
        PRINT_ITEM_TO( NULL, const_str_digest_245adc7cddbc80c6223f99aedd14303b );
        PRINT_NEW_LINE_TO( NULL );
        frame_guard.setLineNumber( 135 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_time ), const_str_plain_sleep ) ).asObject0(), const_int_pos_3 ) );
        frame_guard.setLineNumber( 136 );
        DECREASE_REFCOUNT( CALL_FUNCTION( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_mc.asObject0(), const_str_plain_up ) ).asObject0(), const_tuple_float_0_3_tuple, PyObjectTemporary( PyDict_Copy( const_dict_aa4e253f8daa1e0b2cc0a262e29c3c19 ) ).asObject0() ) );
        frame_guard.setLineNumber( 137 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_time ), const_str_plain_sleep ) ).asObject0(), const_int_pos_1 ) );
        frame_guard.setLineNumber( 138 );
        PRINT_ITEM_TO( NULL, const_str_digest_fda94c46b142d763eef4593313ed7e9f );
        PRINT_NEW_LINE_TO( NULL );
        frame_guard.setLineNumber( 147 );
        DECREASE_REFCOUNT( CALL_FUNCTION( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_mc.asObject0(), const_str_plain_forward ) ).asObject0(), const_tuple_float_3_75_tuple, PyObjectTemporary( PyDict_Copy( const_dict_aa4e253f8daa1e0b2cc0a262e29c3c19 ) ).asObject0() ) );
        frame_guard.setLineNumber( 148 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_mc.asObject0(), const_str_plain_turn_left ) ).asObject0(), const_int_pos_90, const_int_pos_90 ) );
        frame_guard.setLineNumber( 149 );
        DECREASE_REFCOUNT( CALL_FUNCTION( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_mc.asObject0(), const_str_plain_forward ) ).asObject0(), const_tuple_float_1_875_tuple, PyObjectTemporary( PyDict_Copy( const_dict_aa4e253f8daa1e0b2cc0a262e29c3c19 ) ).asObject0() ) );
        frame_guard.setLineNumber( 151 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_mc.asObject0(), const_str_plain_turn_left ) ).asObject0(), const_int_pos_180, const_int_pos_90 ) );
        frame_guard.setLineNumber( 153 );
        DECREASE_REFCOUNT( CALL_FUNCTION( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_mc.asObject0(), const_str_plain_forward ) ).asObject0(), const_tuple_float_1_875_tuple, PyObjectTemporary( PyDict_Copy( const_dict_aa4e253f8daa1e0b2cc0a262e29c3c19 ) ).asObject0() ) );
        frame_guard.setLineNumber( 154 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_mc.asObject0(), const_str_plain_turn_right ) ).asObject0(), const_int_pos_90, const_int_pos_90 ) );
        frame_guard.setLineNumber( 155 );
        DECREASE_REFCOUNT( CALL_FUNCTION( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_mc.asObject0(), const_str_plain_forward ) ).asObject0(), const_tuple_float_3_75_tuple, PyObjectTemporary( PyDict_Copy( const_dict_aa4e253f8daa1e0b2cc0a262e29c3c19 ) ).asObject0() ) );
        frame_guard.setLineNumber( 160 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_mc.asObject0(), const_str_plain_turn_left ) ).asObject0(), const_int_pos_180, const_int_pos_90 ) );
        frame_guard.setLineNumber( 162 );
        DECREASE_REFCOUNT( CALL_FUNCTION( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_mc.asObject0(), const_str_plain_down ) ).asObject0(), const_tuple_float_2_0_tuple, PyObjectTemporary( PyDict_Copy( const_dict_dc1a628231a099fc308313b6a124a2b1 ) ).asObject0() ) );
        frame_guard.setLineNumber( 163 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_mc.asObject0(), const_str_plain_land ) ).asObject0(), const_float_0_4 ) );
        frame_guard.setLineNumber( 164 );
        DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_time ), const_str_plain_sleep ) ).asObject0(), const_int_pos_3 ) );
        frame_guard.setLineNumber( 165 );
        DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_scf.asObject0(), const_str_plain_close_link ) ).asObject0() ) );
        frame_guard.setLineNumber( 168 );
        DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_logger_thread_stop ), const_str_plain_set ) ).asObject0() ) );
        frame_guard.setLineNumber( 169 );
        DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( var_logger_thread.asObject0(), const_str_plain_join ) ).asObject0() ) );
    }
    catch ( PythonException &_exception )
    {
        if ( !_exception.hasTraceback() )
        {
            _exception.setTraceback( MAKE_TRACEBACK( frame_guard.getFrame() ) );
        }
        else
        {
            _exception.addTraceback( frame_guard.getFrame0() );
        }

        Py_XDECREF( frame_guard.getFrame0()->f_locals );
        frame_guard.getFrame0()->f_locals = var_signal_handler.updateLocalsDict( var_aborted_list.updateLocalsDict( var_logger_thread.updateLocalsDict( var_logger.updateLocalsDict( var_mc.updateLocalsDict( var_scf.updateLocalsDict( var_cf.updateLocalsDict( var_lg_stab.updateLocalsDict( var_URI.updateLocalsDict( PyDict_New() ) ) ) ) ) ) ) ) );

        if ( frame_guard.getFrame0() == frame_function_2_main_function_of_module___main__ )
        {
           Py_DECREF( frame_function_2_main_function_of_module___main__ );
           frame_function_2_main_function_of_module___main__ = NULL;
        }

        _exception.toPython();
        return NULL;
    }
    return INCREASE_REFCOUNT( Py_None );
}
static PyObject *fparse_function_2_main_function_of_module___main__( Nuitka_FunctionObject *self, PyObject **args, Py_ssize_t args_size, PyObject *kw )
{
    assert( kw == NULL || PyDict_Check( kw ) );

    NUITKA_MAY_BE_UNUSED Py_ssize_t kw_size = kw ? PyDict_Size( kw ) : 0;
    NUITKA_MAY_BE_UNUSED Py_ssize_t kw_found = 0;
    NUITKA_MAY_BE_UNUSED Py_ssize_t kw_only_found = 0;
    Py_ssize_t args_given = args_size;

    if (unlikely( args_given + kw_size > 0 ))
    {
#if PYTHON_VERSION < 330
        ERROR_NO_ARGUMENTS_ALLOWED(
           self,
           args_given + kw_size
        );
#else
        ERROR_NO_ARGUMENTS_ALLOWED(
           self,
           kw_size > 0 ? kw : NULL,
           args_given
        );
#endif

        goto error_exit;
    }


    return impl_function_2_main_function_of_module___main__( self );

error_exit:;


    return NULL;
}

static PyObject *dparse_function_2_main_function_of_module___main__( Nuitka_FunctionObject *self, PyObject **args, int size )
{
    if ( size == 0 )
    {
        return impl_function_2_main_function_of_module___main__( self );
    }
    else
    {
        PyObject *result = fparse_function_2_main_function_of_module___main__( self, args, size, NULL );
        return result;
    }

}



static PyObject *impl_function_1_signal_handler_of_function_2_main_function_of_module___main__( Nuitka_FunctionObject *self, PyObject *_python_par_signal, PyObject *_python_par_frame )
{
    // The context of the function.
    struct _context_function_1_signal_handler_of_function_2_main_function_of_module___main___t *_python_context = (struct _context_function_1_signal_handler_of_function_2_main_function_of_module___main___t *)self->m_context;

    // Local variable declarations.
    PyObjectLocalParameterVariableNoDel par_signal( const_str_plain_signal, _python_par_signal );
    PyObjectLocalParameterVariableNoDel par_frame( const_str_plain_frame, _python_par_frame );

    // Actual function code.
    static PyFrameObject *frame_function_1_signal_handler_of_function_2_main_function_of_module___main__ = NULL;

    if ( isFrameUnusable( frame_function_1_signal_handler_of_function_2_main_function_of_module___main__ ) )
    {
        if ( frame_function_1_signal_handler_of_function_2_main_function_of_module___main__ )
        {
#if _DEBUG_REFRAME
            puts( "reframe for function_1_signal_handler_of_function_2_main_function_of_module___main__" );
#endif
            Py_DECREF( frame_function_1_signal_handler_of_function_2_main_function_of_module___main__ );
        }

        frame_function_1_signal_handler_of_function_2_main_function_of_module___main__ = MAKE_FRAME( codeobj_d04e0171ddf873f35efd2209c880fe9b, module___main__ );
    }

    FrameGuard frame_guard( frame_function_1_signal_handler_of_function_2_main_function_of_module___main__ );
    try
    {
        assert( Py_REFCNT( frame_function_1_signal_handler_of_function_2_main_function_of_module___main__ ) == 2 ); // Frame stack
        frame_guard.setLineNumber( 107 );
        if ( RICH_COMPARE_BOOL_EQ( PyObjectTemporary( LOOKUP_SUBSCRIPT( _python_context->closure_aborted_list.asObject0(), const_str_plain_aborted ) ).asObject0(), const_int_0 ) )
        {
            frame_guard.setLineNumber( 108 );
            SET_SUBSCRIPT( const_int_pos_1, _python_context->closure_aborted_list.asObject0(), const_str_plain_aborted );
            frame_guard.setLineNumber( 109 );
            PRINT_ITEM_TO( NULL, const_str_digest_d4fc4410d79effb72c093ecd89b0a15d );
            PRINT_NEW_LINE_TO( NULL );
            frame_guard.setLineNumber( 110 );
            DECREASE_REFCOUNT( CALL_FUNCTION( PyObjectTemporary( LOOKUP_ATTRIBUTE( _python_context->closure_mc.asObject0(), const_str_plain_down ) ).asObject0(), const_tuple_float_2_0_tuple, PyObjectTemporary( PyDict_Copy( const_dict_dc1a628231a099fc308313b6a124a2b1 ) ).asObject0() ) );
            frame_guard.setLineNumber( 111 );
            DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( _python_context->closure_mc.asObject0(), const_str_plain_stop ) ).asObject0() ) );
            frame_guard.setLineNumber( 112 );
            DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_time ), const_str_plain_sleep ) ).asObject0(), const_int_pos_4 ) );
            frame_guard.setLineNumber( 113 );
            DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( _python_context->closure_scf.asObject0(), const_str_plain_close_link ) ).asObject0() ) );
            frame_guard.setLineNumber( 114 );
            DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( _python_context->closure_cf.asObject0(), const_str_plain_close_link ) ).asObject0() ) );
            frame_guard.setLineNumber( 115 );
            PRINT_ITEM_TO( NULL, const_str_plain_2 );
            PRINT_NEW_LINE_TO( NULL );
            frame_guard.setLineNumber( 116 );
            DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_os ), const_str_plain__exit ) ).asObject0(), const_int_0 ) );
        }
        frame_guard.setLineNumber( 117 );
        if ( RICH_COMPARE_BOOL_EQ( PyObjectTemporary( LOOKUP_SUBSCRIPT( _python_context->closure_aborted_list.asObject0(), const_str_plain_aborted ) ).asObject0(), const_int_pos_1 ) )
        {
            frame_guard.setLineNumber( 118 );
            PRINT_ITEM_TO( NULL, const_str_digest_e1b4f55ae195000b1f44d069fa0971fb );
            PRINT_NEW_LINE_TO( NULL );
            frame_guard.setLineNumber( 119 );
            DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS4( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( _python_context->closure_cf.asObject0(), const_str_plain_commander ) ).asObject0(), const_str_plain_send_setpoint ) ).asObject0(), const_int_0, const_int_0, const_int_0, const_int_0 ) );
            frame_guard.setLineNumber( 120 );
            DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS2( PyObjectTemporary( LOOKUP_ATTRIBUTE( PyObjectTemporary( LOOKUP_ATTRIBUTE( _python_context->closure_cf.asObject0(), const_str_plain_param ) ).asObject0(), const_str_plain_set_value ) ).asObject0(), const_str_digest_68a9ac2f1f2f7e49c7bad57ba31976f6, const_str_plain_1 ) );
            frame_guard.setLineNumber( 121 );
            DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_time ), const_str_plain_sleep ) ).asObject0(), const_int_pos_1 ) );
            frame_guard.setLineNumber( 122 );
            DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( _python_context->closure_mc.asObject0(), const_str_plain_stop ) ).asObject0() ) );
            frame_guard.setLineNumber( 123 );
            DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( _python_context->closure_scf.asObject0(), const_str_plain_close_link ) ).asObject0() ) );
            frame_guard.setLineNumber( 124 );
            DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( _python_context->closure_cf.asObject0(), const_str_plain_close_link ) ).asObject0() ) );
            frame_guard.setLineNumber( 125 );
            PRINT_ITEM_TO( NULL, const_str_plain_1 );
            PRINT_NEW_LINE_TO( NULL );
            frame_guard.setLineNumber( 126 );
            DECREASE_REFCOUNT( CALL_FUNCTION_WITH_ARGS1( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_os ), const_str_plain__exit ) ).asObject0(), const_int_0 ) );
        }
    }
    catch ( PythonException &_exception )
    {
        if ( !_exception.hasTraceback() )
        {
            _exception.setTraceback( MAKE_TRACEBACK( frame_guard.getFrame() ) );
        }
        else
        {
            _exception.addTraceback( frame_guard.getFrame0() );
        }

        Py_XDECREF( frame_guard.getFrame0()->f_locals );
        frame_guard.getFrame0()->f_locals = par_frame.updateLocalsDict( par_signal.updateLocalsDict( _python_context->closure_cf.updateLocalsDict( _python_context->closure_scf.updateLocalsDict( _python_context->closure_mc.updateLocalsDict( _python_context->closure_aborted_list.updateLocalsDict( PyDict_New() ) ) ) ) ) );

        if ( frame_guard.getFrame0() == frame_function_1_signal_handler_of_function_2_main_function_of_module___main__ )
        {
           Py_DECREF( frame_function_1_signal_handler_of_function_2_main_function_of_module___main__ );
           frame_function_1_signal_handler_of_function_2_main_function_of_module___main__ = NULL;
        }

        _exception.toPython();
        return NULL;
    }
    return INCREASE_REFCOUNT( Py_None );
}
static PyObject *fparse_function_1_signal_handler_of_function_2_main_function_of_module___main__( Nuitka_FunctionObject *self, PyObject **args, Py_ssize_t args_size, PyObject *kw )
{
    assert( kw == NULL || PyDict_Check( kw ) );

    NUITKA_MAY_BE_UNUSED Py_ssize_t kw_size = kw ? PyDict_Size( kw ) : 0;
    NUITKA_MAY_BE_UNUSED Py_ssize_t kw_found = 0;
    NUITKA_MAY_BE_UNUSED Py_ssize_t kw_only_found = 0;
    Py_ssize_t args_given = args_size;
    PyObject *_python_par_signal = NULL;
    PyObject *_python_par_frame = NULL;
    // Copy given dictionary values to the the respective variables:
    if ( kw_size > 0 )
    {
        Py_ssize_t ppos = 0;
        PyObject *key, *value;

        while( PyDict_Next( kw, &ppos, &key, &value ) )
        {
#if PYTHON_VERSION < 300
            if (unlikely( !PyString_Check( key ) && !PyUnicode_Check( key ) ))
#else
            if (unlikely( !PyUnicode_Check( key ) ))
#endif
            {
                PyErr_Format( PyExc_TypeError, "signal_handler() keywords must be strings" );
                goto error_exit;
            }

            NUITKA_MAY_BE_UNUSED bool found = false;

            Py_INCREF( key );
            Py_INCREF( value );

            // Quick path, could be our value.
            if ( found == false && const_str_plain_signal == key )
            {
                assert( _python_par_signal == NULL );
                _python_par_signal = value;

                found = true;
                kw_found += 1;
            }
            if ( found == false && const_str_plain_frame == key )
            {
                assert( _python_par_frame == NULL );
                _python_par_frame = value;

                found = true;
                kw_found += 1;
            }

            // Slow path, compare against all parameter names.
            if ( found == false && RICH_COMPARE_BOOL_EQ_PARAMETERS( const_str_plain_signal, key ) )
            {
                assert( _python_par_signal == NULL );
                _python_par_signal = value;

                found = true;
                kw_found += 1;
            }
            if ( found == false && RICH_COMPARE_BOOL_EQ_PARAMETERS( const_str_plain_frame, key ) )
            {
                assert( _python_par_frame == NULL );
                _python_par_frame = value;

                found = true;
                kw_found += 1;
            }


            Py_DECREF( key );

            if ( found == false )
            {
               Py_DECREF( value );

               PyErr_Format(
                   PyExc_TypeError,
                   "signal_handler() got an unexpected keyword argument '%s'",
                   Nuitka_String_Check( key ) ? Nuitka_String_AsString( key ) : "<non-string>"
               );

               goto error_exit;
            }
        }

#if PYTHON_VERSION < 300
        assert( kw_found == kw_size );
        assert( kw_only_found == 0 );
#endif
    }

    // Check if too many arguments were given in case of non star args
    if (unlikely( args_given > 2 ))
    {
#if PYTHON_VERSION < 270
        ERROR_TOO_MANY_ARGUMENTS( self, args_given, kw_size );
#elif PYTHON_VERSION < 330
        ERROR_TOO_MANY_ARGUMENTS( self, args_given + kw_found );
#else
        ERROR_TOO_MANY_ARGUMENTS( self, args_given, kw_only_found );
#endif
        goto error_exit;
    }


    // Copy normal parameter values given as part of the args list to the respective variables:

    if (likely( 0 < args_given ))
    {
         if (unlikely( _python_par_signal != NULL ))
         {
             ERROR_MULTIPLE_VALUES( self, 0 );
             goto error_exit;
         }

        _python_par_signal = INCREASE_REFCOUNT( args[ 0 ] );
    }
    else if ( _python_par_signal == NULL )
    {
        if ( 0 + self->m_defaults_given >= 2  )
        {
            _python_par_signal = INCREASE_REFCOUNT( PyTuple_GET_ITEM( self->m_defaults, self->m_defaults_given + 0 - 2 ) );
        }
#if PYTHON_VERSION < 330
        else
        {
#if PYTHON_VERSION < 270
            ERROR_TOO_FEW_ARGUMENTS( self, kw_size, args_given + kw_found );
#elif PYTHON_VERSION < 300
            ERROR_TOO_FEW_ARGUMENTS( self, args_given + kw_found );
#else
            ERROR_TOO_FEW_ARGUMENTS( self, args_given + kw_found - kw_only_found );
#endif

            goto error_exit;
        }
#endif
    }
    if (likely( 1 < args_given ))
    {
         if (unlikely( _python_par_frame != NULL ))
         {
             ERROR_MULTIPLE_VALUES( self, 1 );
             goto error_exit;
         }

        _python_par_frame = INCREASE_REFCOUNT( args[ 1 ] );
    }
    else if ( _python_par_frame == NULL )
    {
        if ( 1 + self->m_defaults_given >= 2  )
        {
            _python_par_frame = INCREASE_REFCOUNT( PyTuple_GET_ITEM( self->m_defaults, self->m_defaults_given + 1 - 2 ) );
        }
#if PYTHON_VERSION < 330
        else
        {
#if PYTHON_VERSION < 270
            ERROR_TOO_FEW_ARGUMENTS( self, kw_size, args_given + kw_found );
#elif PYTHON_VERSION < 300
            ERROR_TOO_FEW_ARGUMENTS( self, args_given + kw_found );
#else
            ERROR_TOO_FEW_ARGUMENTS( self, args_given + kw_found - kw_only_found );
#endif

            goto error_exit;
        }
#endif
    }

#if PYTHON_VERSION >= 330
    if (unlikely( _python_par_signal == NULL || _python_par_frame == NULL ))
    {
        PyObject *values[] = { _python_par_signal, _python_par_frame };
        ERROR_TOO_FEW_ARGUMENTS( self, values );

        goto error_exit;
    }
#endif


    return impl_function_1_signal_handler_of_function_2_main_function_of_module___main__( self, _python_par_signal, _python_par_frame );

error_exit:;

    Py_XDECREF( _python_par_signal );
    Py_XDECREF( _python_par_frame );

    return NULL;
}

static PyObject *dparse_function_1_signal_handler_of_function_2_main_function_of_module___main__( Nuitka_FunctionObject *self, PyObject **args, int size )
{
    if ( size == 2 )
    {
        return impl_function_1_signal_handler_of_function_2_main_function_of_module___main__( self, INCREASE_REFCOUNT( args[ 0 ] ), INCREASE_REFCOUNT( args[ 1 ] ) );
    }
    else
    {
        PyObject *result = fparse_function_1_signal_handler_of_function_2_main_function_of_module___main__( self, args, size, NULL );
        return result;
    }

}




static PyObject *MAKE_FUNCTION_function_1_logger_thread_worker_of_module___main__(  )
{
    PyObject *result = Nuitka_Function_New(
        fparse_function_1_logger_thread_worker_of_module___main__,
        dparse_function_1_logger_thread_worker_of_module___main__,
        const_str_plain_logger_thread_worker,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_cd532aaf552b21af9328ca0de7c0f3dc,
        INCREASE_REFCOUNT( Py_None ),
#if PYTHON_VERSION >= 300
        INCREASE_REFCOUNT( Py_None ),
        NULL,
#endif
        module___main__,
        Py_None
    );

    return result;
}



static PyObject *MAKE_FUNCTION_function_1_signal_handler_of_function_2_main_function_of_module___main__( PyObjectSharedLocalVariable &closure_aborted_list, PyObjectSharedLocalVariable &closure_cf, PyObjectSharedLocalVariable &closure_mc, PyObjectSharedLocalVariable &closure_scf )
{
    struct _context_function_1_signal_handler_of_function_2_main_function_of_module___main___t *_python_context = new _context_function_1_signal_handler_of_function_2_main_function_of_module___main___t;

    // Copy the parameter default values and closure values over.
    _python_context->closure_aborted_list.shareWith( closure_aborted_list );
    _python_context->closure_cf.shareWith( closure_cf );
    _python_context->closure_mc.shareWith( closure_mc );
    _python_context->closure_scf.shareWith( closure_scf );

    PyObject *result = Nuitka_Function_New(
        fparse_function_1_signal_handler_of_function_2_main_function_of_module___main__,
        dparse_function_1_signal_handler_of_function_2_main_function_of_module___main__,
        const_str_plain_signal_handler,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_d04e0171ddf873f35efd2209c880fe9b,
        INCREASE_REFCOUNT( Py_None ),
#if PYTHON_VERSION >= 300
        INCREASE_REFCOUNT( Py_None ),
        NULL,
#endif
        module___main__,
        Py_None,
        _python_context,
        _context_function_1_signal_handler_of_function_2_main_function_of_module___main___destructor
    );

    return result;
}



static PyObject *MAKE_FUNCTION_function_2_main_function_of_module___main__(  )
{
    PyObject *result = Nuitka_Function_New(
        fparse_function_2_main_function_of_module___main__,
        dparse_function_2_main_function_of_module___main__,
        const_str_plain_main_function,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_37a54b2662ac0a8cb93e5380370c546c,
        INCREASE_REFCOUNT( Py_None ),
#if PYTHON_VERSION >= 300
        INCREASE_REFCOUNT( Py_None ),
        NULL,
#endif
        module___main__,
        Py_None
    );

    return result;
}


#if PYTHON_VERSION >= 300
static struct PyModuleDef mdef___main__ =
{
    PyModuleDef_HEAD_INIT,
    "__main__",   /* m_name */
    NULL,                /* m_doc */
    -1,                  /* m_size */
    NULL,                /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#endif

#define _MODULE_UNFREEZER 0

#if _MODULE_UNFREEZER

#include "nuitka/unfreezing.hpp"

// Table for lookup to find "frozen" modules or DLLs, i.e. the ones included in
// or along this binary.
static struct Nuitka_MetaPathBasedLoaderEntry meta_path_loader_entries[] =
{

    { NULL, NULL, 0 }
};

#endif

// The exported interface to CPython. On import of the module, this function
// gets called. It has to have an exact function name, in cases it's a shared
// library export. This is hidden behind the MOD_INIT_DECL.

MOD_INIT_DECL( __main__ )
{

#if defined(_NUITKA_EXE) || PYTHON_VERSION >= 300
    static bool _init_done = false;

    // Packages can be imported recursively in deep executables.
    if ( _init_done )
    {
        return MOD_RETURN_VALUE( module___main__ );
    }
    else
    {
        _init_done = true;
    }
#endif

#ifdef _NUITKA_MODULE
    // In case of a stand alone extension module, need to call initialization
    // the init here because that's the first and only time we are going to get
    // called here.

    // Initialize the constant values used.
    _initBuiltinModule();
    _initConstants();

    // Initialize the compiled types of Nuitka.
    PyType_Ready( &Nuitka_Generator_Type );
    PyType_Ready( &Nuitka_Function_Type );
    PyType_Ready( &Nuitka_Method_Type );
    PyType_Ready( &Nuitka_Frame_Type );
#if PYTHON_VERSION < 300
    initSlotCompare();
#endif

    patchBuiltinModule();
    patchTypeComparison();

#endif

#if _MODULE_UNFREEZER
    registerMetaPathBasedUnfreezer( meta_path_loader_entries );
#endif

    // puts( "in init__main__" );

    // Create the module object first. There are no methods initially, all are
    // added dynamically in actual code only.  Also no "__doc__" is initially
    // set at this time, as it could not contain NUL characters this way, they
    // are instead set in early module code.  No "self" for modules, we have no
    // use for it.
#if PYTHON_VERSION < 300
    module___main__ = Py_InitModule4(
        "__main__",       // Module Name
        NULL,                    // No methods initially, all are added
                                 // dynamically in actual module code only.
        NULL,                    // No __doc__ is initially set, as it could
                                 // not contain NUL this way, added early in
                                 // actual code.
        NULL,                    // No self for modules, we don't use it.
        PYTHON_API_VERSION
    );
#else
    module___main__ = PyModule_Create( &mdef___main__ );
#endif

    moduledict___main__ = (PyDictObject *)((PyModuleObject *)module___main__)->md_dict;

    assertObject( module___main__ );

// Seems to work for Python2.7 out of the box, but for Python3, the module
// doesn't automatically enter "sys.modules", so do it manually.
#if PYTHON_VERSION >= 300
    {
        int r = PyObject_SetItem( PySys_GetObject( (char *)"modules" ), const_str_plain___main__, module___main__ );

        assert( r != -1 );
    }
#endif

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    PyObject *module_dict = PyModule_GetDict( module___main__ );

    if ( PyDict_GetItem( module_dict, const_str_plain___builtins__ ) == NULL )
    {
        PyObject *value = ( PyObject *)module_builtin;

#ifdef _NUITKA_EXE
        if ( module___main__ != module___main__ )
        {
#endif
            value = PyModule_GetDict( value );
#ifdef _NUITKA_EXE
        }
#endif

#ifndef __NUITKA_NO_ASSERT__
        int res =
#endif
            PyDict_SetItem( module_dict, const_str_plain___builtins__, value );

        assert( res == 0 );
    }

#if PYTHON_VERSION >= 330
#if _MODULE_UNFREEZER
    PyDict_SetItem( module_dict, const_str_plain___loader__, metapath_based_loader );
#else
    PyDict_SetItem( module_dict, const_str_plain___loader__, Py_None );
#endif
#endif

    // Temp variables if any


    // Module code
    PyFrameObject *frame_module___main__ = MAKE_FRAME( codeobj_b7454df100b49567308905a916008142, module___main__ );

    FrameGuard frame_guard( frame_module___main__ );
    try
    {
        assert( Py_REFCNT( frame_module___main__ ) == 2 ); // Frame stack
        frame_guard.setLineNumber( 1 );
        DECREASE_REFCOUNT( IMPORT_MODULE( const_str_plain_site, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, const_tuple_empty, const_int_neg_1 ) );
        UPDATE_STRING_DICT0( moduledict___main__, (Nuitka_StringObject *)const_str_plain___doc__, Py_None );
        UPDATE_STRING_DICT0( moduledict___main__, (Nuitka_StringObject *)const_str_plain___file__, const_str_digest_9f85aa3708239e0c778cb00a86748a3c );
        frame_guard.setLineNumber( 3 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_logging, IMPORT_MODULE( const_str_plain_logging, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, Py_None, const_int_neg_1 ) );
        frame_guard.setLineNumber( 4 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_time, IMPORT_MODULE( const_str_plain_time, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, Py_None, const_int_neg_1 ) );
        frame_guard.setLineNumber( 5 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_sys, IMPORT_MODULE( const_str_plain_sys, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, Py_None, const_int_neg_1 ) );
        frame_guard.setLineNumber( 6 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_os, IMPORT_MODULE( const_str_plain_os, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, Py_None, const_int_neg_1 ) );
        frame_guard.setLineNumber( 7 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_signal, IMPORT_MODULE( const_str_plain_signal, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, Py_None, const_int_neg_1 ) );
        frame_guard.setLineNumber( 9 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_cflib, IMPORT_MODULE( const_str_digest_31d2b49447b7edba18cc9ff536133c53, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, Py_None, const_int_neg_1 ) );
        frame_guard.setLineNumber( 10 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_threading, IMPORT_MODULE( const_str_plain_threading, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, Py_None, const_int_neg_1 ) );
        frame_guard.setLineNumber( 11 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_Crazyflie, IMPORT_NAME( PyObjectTemporary( IMPORT_MODULE( const_str_digest_f0ea728aa6a36615358e93c174b00f87, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, const_list_str_plain_Crazyflie_list, const_int_neg_1 ) ).asObject0(), const_str_plain_Crazyflie ) );
        frame_guard.setLineNumber( 12 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_SyncCrazyflie, IMPORT_NAME( PyObjectTemporary( IMPORT_MODULE( const_str_digest_1eb417079397bafee1de8a2307718a67, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, const_list_str_plain_SyncCrazyflie_list, const_int_neg_1 ) ).asObject0(), const_str_plain_SyncCrazyflie ) );
        frame_guard.setLineNumber( 13 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_MotionCommander, IMPORT_NAME( PyObjectTemporary( IMPORT_MODULE( const_str_digest_3bf51efc682f557ee837839a9da02b41, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, const_list_str_plain_MotionCommander_list, const_int_neg_1 ) ).asObject0(), const_str_plain_MotionCommander ) );
        frame_guard.setLineNumber( 14 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_SyncLogger, IMPORT_NAME( PyObjectTemporary( IMPORT_MODULE( const_str_digest_187879fed30627459387957f2c0edddf, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, const_list_str_plain_SyncLogger_list, const_int_neg_1 ) ).asObject0(), const_str_plain_SyncLogger ) );
        frame_guard.setLineNumber( 15 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_LogConfig, IMPORT_NAME( PyObjectTemporary( IMPORT_MODULE( const_str_digest_8c90b05af7802ee53561cbc1fa1ae964, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, const_list_str_plain_LogConfig_list, const_int_neg_1 ) ).asObject0(), const_str_plain_LogConfig ) );
        frame_guard.setLineNumber( 16 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_Thread, IMPORT_NAME( PyObjectTemporary( IMPORT_MODULE( const_str_plain_threading, ((PyModuleObject *)module___main__)->md_dict, ((PyModuleObject *)module___main__)->md_dict, const_list_str_plain_Thread_list, const_int_neg_1 ) ).asObject0(), const_str_plain_Thread ) );
        frame_guard.setLineNumber( 20 );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_logger_thread_stop, CALL_FUNCTION_NO_ARGS( PyObjectTemporary( LOOKUP_ATTRIBUTE( GET_MODULE_VALUE0( const_str_plain_threading ), const_str_plain_Event ) ).asObject0() ) );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_logger_thread_worker, MAKE_FUNCTION_function_1_logger_thread_worker_of_module___main__(  ) );
        UPDATE_STRING_DICT1( moduledict___main__, (Nuitka_StringObject *)const_str_plain_main_function, MAKE_FUNCTION_function_2_main_function_of_module___main__(  ) );
        frame_guard.setLineNumber( 173 );
        DECREASE_REFCOUNT( CALL_FUNCTION_NO_ARGS( GET_MODULE_VALUE0( const_str_plain_main_function ) ) );
    }
    catch ( PythonException &_exception )
    {
        if ( !_exception.hasTraceback() )
        {
            _exception.setTraceback( MAKE_TRACEBACK( frame_guard.getFrame() ) );
        }
        else
        {
            _exception.addTraceback( frame_guard.getFrame0() );
        }

#if 0
    // TODO: Recognize the need for it
        Py_XDECREF( frame_guard.getFrame0()->f_locals );
        frame_guard.getFrame0()->f_locals = INCREASE_REFCOUNT( ((PyModuleObject *)module___main__)->md_dict );
#endif

        // Return the error.
        _exception.toPython();
        return MOD_RETURN_VALUE( NULL );
    }

   return MOD_RETURN_VALUE( module___main__ );
}
// The main program for C++. It needs to prepare the interpreter and then
// calls the initialization code of the __main__ module.

#include "structseq.h"
#ifdef _NUITKA_WINMAIN_ENTRY_POINT
int __stdcall WinMain( HINSTANCE hInstance, HINSTANCE hPrevInstance, char* lpCmdLine, int nCmdShow )
{
    int argc = __argc;
    char** argv = __argv;
#else
int main( int argc, char *argv[] )
{
#endif
#ifdef _NUITKA_STANDALONE
    prepareStandaloneEnvironment();
#endif

    // Initialize Python environment.
    Py_DebugFlag = 0;
#if 0
    Py_Py3kWarningFlag = 0;
#endif
#if 0
    Py_DivisionWarningFlag =
#if 0
        Py_Py3kWarningFlag ||
#endif
        0;
#endif
    Py_InspectFlag = 0;
    Py_InteractiveFlag = 0;
    Py_OptimizeFlag = 0;
    Py_DontWriteBytecodeFlag = 0;
    Py_NoUserSiteDirectory = 0;
    Py_IgnoreEnvironmentFlag = 0;
#if 0
    Py_TabcheckFlag = 0;
#endif
    Py_VerboseFlag = 0;
#if 0
    Py_UnicodeFlag = 0;
#endif
    Py_BytesWarningFlag = 0;
#if 1
    Py_HashRandomizationFlag = 1;
#endif

    // We want to import the site module, but only after we finished our own
    // setup. The site module import will be the first thing, the main module
    // does.
    Py_NoSiteFlag = 1;

    // Initialize the embedded CPython interpreter.
    setCommandLineParameters( argc, argv, true );
    Py_Initialize();

    // Lie about it, believe it or not, there are "site" files, that check
    // against later imports, see below.
    Py_NoSiteFlag = 0;

    // Set the command line parameters for run time usage.
    setCommandLineParameters( argc, argv, false );

    // Initialize the constant values used.
    _initBuiltinModule();
    _initConstants();
    _initBuiltinOriginalValues();

    // Revert the wrong sys.flags value, it's used by "site" on at least Debian
    // for Python3.3, more uses may exist.
#if 0 == 0
#if PYTHON_VERSION >= 330
    PyStructSequence_SetItem( PySys_GetObject( "flags" ), 6, const_int_0 );
#elif PYTHON_VERSION >= 320
    PyStructSequence_SetItem( PySys_GetObject( "flags" ), 7, const_int_0 );
#elif PYTHON_VERSION >= 260
    PyStructSequence_SET_ITEM( PySys_GetObject( (char *)"flags" ), 9, const_int_0 );
#endif
#endif

    // Initialize the compiled types of Nuitka.
    PyType_Ready( &Nuitka_Generator_Type );
    PyType_Ready( &Nuitka_Function_Type );
    PyType_Ready( &Nuitka_Method_Type );
    PyType_Ready( &Nuitka_Frame_Type );
#if PYTHON_VERSION < 300
    initSlotCompare();
#endif

    enhancePythonTypes();

    // Set the sys.executable path to the original Python executable on Linux
    // or to python.exe on Windows.
    PySys_SetObject(
        (char *)"executable",
        const_str_digest_c42384e11d8039023cc63f738682e4b1
    );

    patchBuiltinModule();
    patchTypeComparison();

    // Allow to override the ticker value, to remove checks for threads in
    // CPython core from impact on benchmarks.
    char const *ticker_value = getenv( "NUITKA_TICKER" );
    if ( ticker_value != NULL )
    {
        _Py_Ticker = atoi( ticker_value );
        assert ( _Py_Ticker >= 20 );
    }

#if _NUITKA_STANDALONE
    setEarlyFrozenModulesFileAttribute();
#endif

    // Execute the "__main__" module init function.
    MOD_INIT_NAME( __main__ )();

    if ( ERROR_OCCURED() )
    {
        // Cleanup code may need a frame, so put one back.
        PyThreadState_GET()->frame = MAKE_FRAME( codeobj_b7454df100b49567308905a916008142, module___main__ );

        PyErr_PrintEx( 0 );
        Py_Exit( 1 );
    }
    else
    {
        Py_Exit( 0 );
    }
}
