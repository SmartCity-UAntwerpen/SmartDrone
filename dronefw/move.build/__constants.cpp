
#include "nuitka/prelude.hpp"

// Sentinel PyObject to be used for all our call iterator endings. It will
// become a PyCObject pointing to NULL. It's address is unique, and that's
// enough for us to use it as sentinel value.
PyObject *_sentinel_value = NULL;

PyObject *const_int_0;
PyObject *const_float_0_1;
PyObject *const_float_0_3;
PyObject *const_float_0_4;
PyObject *const_int_neg_1;
PyObject *const_int_pos_1;
PyObject *const_int_pos_3;
PyObject *const_int_pos_4;
PyObject *const_int_pos_5;
PyObject *const_str_empty;
PyObject *const_dict_empty;
PyObject *const_int_pos_90;
PyObject *const_int_pos_180;
PyObject *const_str_plain_0;
PyObject *const_str_plain_1;
PyObject *const_str_plain_2;
PyObject *const_str_plain_w;
PyObject *const_tuple_empty;
PyObject *const_str_plain_15;
PyObject *const_str_plain_20;
PyObject *const_str_plain_cf;
PyObject *const_str_plain_mc;
PyObject *const_str_plain_os;
PyObject *const_str_plain_px;
PyObject *const_str_plain_py;
PyObject *const_str_plain_pz;
PyObject *const_str_plain_up;
PyObject *const_str_plain_URI;
PyObject *const_str_plain_get;
PyObject *const_str_plain_int;
PyObject *const_str_plain_len;
PyObject *const_str_plain_scf;
PyObject *const_str_plain_set;
PyObject *const_str_plain_sys;
PyObject *const_str_plain_yaw;
PyObject *const_str_plain_args;
PyObject *const_str_plain_crtp;
PyObject *const_str_plain_data;
PyObject *const_str_plain_down;
PyObject *const_str_plain_iter;
PyObject *const_str_plain_join;
PyObject *const_str_plain_land;
PyObject *const_str_plain_long;
PyObject *const_str_plain_open;
PyObject *const_str_plain_read;
PyObject *const_str_plain_repr;
PyObject *const_str_plain_roll;
PyObject *const_str_plain_site;
PyObject *const_str_plain_stop;
PyObject *const_str_plain_time;
PyObject *const_str_plain_type;
PyObject *const_str_plain_20000;
PyObject *const_str_plain_ERROR;
PyObject *const_str_plain_Event;
PyObject *const_str_plain__exit;
PyObject *const_str_plain_cflib;
PyObject *const_str_plain_close;
PyObject *const_str_plain_float;
PyObject *const_str_plain_frame;
PyObject *const_str_plain_level;
PyObject *const_str_plain_param;
PyObject *const_str_plain_pitch;
PyObject *const_str_plain_range;
PyObject *const_str_plain_sleep;
PyObject *const_str_plain_start;
PyObject *const_str_plain_strip;
PyObject *const_str_plain_write;
PyObject *const_str_angle_module;
PyObject *const_str_plain_SIGINT;
PyObject *const_str_plain_Thread;
PyObject *const_str_plain_is_set;
PyObject *const_str_plain_logger;
PyObject *const_str_plain_signal;
PyObject *const_str_plain_target;
PyObject *const_str_plain_xrange;
PyObject *const_str_plain___all__;
PyObject *const_str_plain___cmp__;
PyObject *const_str_plain___doc__;
PyObject *const_str_plain_aborted;
PyObject *const_str_plain_compile;
PyObject *const_str_plain_connect;
PyObject *const_str_plain_forward;
PyObject *const_str_plain_inspect;
PyObject *const_str_plain_lg_stab;
PyObject *const_str_plain_logging;
PyObject *const_str_plain_posfile;
PyObject *const_str_plain___dict__;
PyObject *const_str_plain___exit__;
PyObject *const_str_plain___file__;
PyObject *const_str_plain___main__;
PyObject *const_str_plain___name__;
PyObject *const_str_plain_exc_type;
PyObject *const_str_plain_take_off;
PyObject *const_str_plain_Crazyflie;
PyObject *const_str_plain_LogConfig;
PyObject *const_str_plain___class__;
PyObject *const_str_plain___enter__;
PyObject *const_str_plain_commander;
PyObject *const_str_plain_exc_value;
PyObject *const_str_plain_log_entry;
PyObject *const_str_plain_open_link;
PyObject *const_str_plain_set_value;
PyObject *const_str_plain_threading;
PyObject *const_str_plain_timestamp;
PyObject *const_str_plain_turn_left;
PyObject *const_str_plain_SyncLogger;
PyObject *const_str_plain___import__;
PyObject *const_str_plain___module__;
PyObject *const_str_plain_close_link;
PyObject *const_str_plain_turn_right;
PyObject *const_str_plain___delattr__;
PyObject *const_str_plain___getattr__;
PyObject *const_str_plain___setattr__;
PyObject *const_str_plain_basicConfig;
PyObject *const_tuple_float_0_3_tuple;
PyObject *const_tuple_float_2_0_tuple;
PyObject *const_str_plain___builtins__;
PyObject *const_str_plain_aborted_list;
PyObject *const_str_plain_add_variable;
PyObject *const_str_plain_init_drivers;
PyObject *const_tuple_float_3_75_tuple;
PyObject *const_str_plain_SyncCrazyflie;
PyObject *const_str_plain___metaclass__;
PyObject *const_str_plain_exc_traceback;
PyObject *const_str_plain_logger_thread;
PyObject *const_str_plain_main_function;
PyObject *const_str_plain_send_setpoint;
PyObject *const_tuple_float_1_875_tuple;
PyObject *const_str_plain_signal_handler;
PyObject *const_str_plain_MotionCommander;
PyObject *const_list_str_plain_Thread_list;
PyObject *const_str_plain_logger_thread_stop;
PyObject *const_tuple_str_plain_logger_tuple;
PyObject *const_list_str_plain_Crazyflie_list;
PyObject *const_list_str_plain_LogConfig_list;
PyObject *const_list_str_plain_SyncLogger_list;
PyObject *const_str_plain_logger_thread_worker;
PyObject *const_list_str_plain_SyncCrazyflie_list;
PyObject *const_list_str_plain_MotionCommander_list;
PyObject *const_dict_243aa8eecd2da5a46892332cfdc4d450;
PyObject *const_dict_539d0a0b95c7f4877f43e57e4ab8d984;
PyObject *const_dict_62ee6ebcc3c4bc4b866e8cd064cf56b7;
PyObject *const_dict_aa4e253f8daa1e0b2cc0a262e29c3c19;
PyObject *const_dict_ce98f68090408fb17a6c2e7f34cf931d;
PyObject *const_dict_dc1a628231a099fc308313b6a124a2b1;
PyObject *const_str_digest_0345aa3382d9cabb03624fa419361084;
PyObject *const_str_digest_04817efd11c15364a6ec239780038862;
PyObject *const_str_digest_0c9434c1a2d38b03084e8af867a5a591;
PyObject *const_str_digest_145ace45251939555fbe881f24d19dc6;
PyObject *const_str_digest_187879fed30627459387957f2c0edddf;
PyObject *const_str_digest_1eb417079397bafee1de8a2307718a67;
PyObject *const_str_digest_245adc7cddbc80c6223f99aedd14303b;
PyObject *const_str_digest_24d1b912a24567d4b0f37e65866caec4;
PyObject *const_str_digest_2930a74bfe0dfc7d45d37b747109010a;
PyObject *const_str_digest_2d0bc760d21081fbbe357ac9bd3098d1;
PyObject *const_str_digest_2f68ad040984e87524a290e4cb58117f;
PyObject *const_str_digest_31d2b49447b7edba18cc9ff536133c53;
PyObject *const_str_digest_3bf51efc682f557ee837839a9da02b41;
PyObject *const_str_digest_44c948084dd4e5ab67b1ec497d101727;
PyObject *const_str_digest_4e2c018a5300351973557add0a24141a;
PyObject *const_str_digest_60a23ecc05ca99686bc518474cb1df7a;
PyObject *const_str_digest_68a9ac2f1f2f7e49c7bad57ba31976f6;
PyObject *const_str_digest_6cc08d0712c8d9467d68c797bc086fed;
PyObject *const_str_digest_6fae5998bcb63ea7f2ecb4f9dea2b2a7;
PyObject *const_str_digest_6fcf7cef0081a3be07ee72eeaf847b1f;
PyObject *const_str_digest_7390cc453f512da13f0d281a65059885;
PyObject *const_str_digest_77e23e10fe1b9556624317a002d8b1cc;
PyObject *const_str_digest_8c90b05af7802ee53561cbc1fa1ae964;
PyObject *const_str_digest_9f85aa3708239e0c778cb00a86748a3c;
PyObject *const_str_digest_a2c1833e0fd5389050407cccd2b5fa06;
PyObject *const_str_digest_a4d5e4010a0ee714d42205db4918cf2b;
PyObject *const_str_digest_b03c2e2c3dee02212866e618daae5997;
PyObject *const_str_digest_b064bc73fc5d82cb15ddbd6cb7eeb804;
PyObject *const_str_digest_bb098d44f0e169e5eb07c575224d8553;
PyObject *const_str_digest_bb9871a70568c3d29995e4ee517f0c1d;
PyObject *const_str_digest_bd56e81c8f1ef1514e78dc5e67b5b1a2;
PyObject *const_str_digest_c38568aedd7bb1c9232846890b69ebc7;
PyObject *const_str_digest_c42384e11d8039023cc63f738682e4b1;
PyObject *const_str_digest_cc876ca77c133b1ab9057ea27426e8d3;
PyObject *const_str_digest_d2f986057c6f7103b7ca87474919f5c2;
PyObject *const_str_digest_d4fc4410d79effb72c093ecd89b0a15d;
PyObject *const_str_digest_da28a3a52fef5cfcfe6516207c87623e;
PyObject *const_str_digest_e1b4f55ae195000b1f44d069fa0971fb;
PyObject *const_str_digest_e7511362545f1e8e4835d7768b8645c2;
PyObject *const_str_digest_e9fa29284a0eebe10618a41a87657254;
PyObject *const_str_digest_f0ea728aa6a36615358e93c174b00f87;
PyObject *const_str_digest_f991bf363475592a622e85cda89309dc;
PyObject *const_str_digest_fda94c46b142d763eef4593313ed7e9f;
PyObject *const_tuple_4827392191ca93bcc4094155298f412c_tuple;
PyObject *const_tuple_78f9ded54d9be9c5c92b9e64a92944b2_tuple;
PyObject *const_tuple_str_plain_signal_str_plain_frame_tuple;
PyCodeObject *codeobj_b7454df100b49567308905a916008142;
PyCodeObject *codeobj_5ca39b17b9682cc8ca19997fc3ea65f4;
PyCodeObject *codeobj_cd532aaf552b21af9328ca0de7c0f3dc;
PyCodeObject *codeobj_b6866d1d3dae1aec7ae569970b6db7dd;
PyCodeObject *codeobj_37a54b2662ac0a8cb93e5380370c546c;
PyCodeObject *codeobj_d04e0171ddf873f35efd2209c880fe9b;

extern "C" const unsigned char constant_bin[];
#define stream_data constant_bin

static void __initConstants( void )
{
    PyObject *const_float_0_5;
    PyObject *const_float_2_0;
    PyObject *const_float_3_75;
    PyObject *const_float_1_875;
    PyObject *const_int_pos_100;
    PyObject *const_str_plain_ro;
    PyObject *const_str_plain_rw;
    PyObject *const_str_plain_name;
    PyObject *const_str_plain_Position;
    PyObject *const_str_plain_ro_cache;
    PyObject *const_str_plain_rw_cache;
    PyObject *const_str_plain_velocity;
    PyObject *const_str_plain_period_in_ms;
    PyObject *const_str_plain_enable_debug_driver;
    const_int_0 = PyInt_FromLong( 0l );
    const_float_0_1 = UNSTREAM_FLOAT( &stream_data[ 0 ] );
    const_float_0_3 = UNSTREAM_FLOAT( &stream_data[ 8 ] );
    const_float_0_4 = UNSTREAM_FLOAT( &stream_data[ 16 ] );
    const_int_neg_1 = PyInt_FromLong( -1l );
    const_int_pos_1 = PyInt_FromLong( 1l );
    const_int_pos_3 = PyInt_FromLong( 3l );
    const_int_pos_4 = PyInt_FromLong( 4l );
    const_int_pos_5 = PyInt_FromLong( 5l );
    const_str_empty = UNSTREAM_STRING( &stream_data[ 0 ], 0, 0 );
    const_dict_empty = PyDict_New();
    const_int_pos_90 = PyInt_FromLong( 90l );
    const_int_pos_180 = PyInt_FromLong( 180l );
    const_str_plain_0 = UNSTREAM_CHAR( 48, 0 );
    const_str_plain_1 = UNSTREAM_CHAR( 49, 0 );
    const_str_plain_2 = UNSTREAM_CHAR( 50, 0 );
    const_str_plain_w = UNSTREAM_CHAR( 119, 1 );
    const_tuple_empty = PyTuple_New( 0 );
    const_str_plain_15 = UNSTREAM_STRING( &stream_data[ 24 ], 2, 0 );
    const_str_plain_20 = UNSTREAM_STRING( &stream_data[ 26 ], 2, 0 );
    const_str_plain_cf = UNSTREAM_STRING( &stream_data[ 28 ], 2, 1 );
    const_str_plain_mc = UNSTREAM_STRING( &stream_data[ 30 ], 2, 1 );
    const_str_plain_os = UNSTREAM_STRING( &stream_data[ 32 ], 2, 1 );
    const_str_plain_px = UNSTREAM_STRING( &stream_data[ 34 ], 2, 1 );
    const_str_plain_py = UNSTREAM_STRING( &stream_data[ 36 ], 2, 1 );
    const_str_plain_pz = UNSTREAM_STRING( &stream_data[ 38 ], 2, 1 );
    const_str_plain_up = UNSTREAM_STRING( &stream_data[ 40 ], 2, 1 );
    const_str_plain_URI = UNSTREAM_STRING( &stream_data[ 42 ], 3, 1 );
    const_str_plain_get = UNSTREAM_STRING( &stream_data[ 45 ], 3, 1 );
    const_str_plain_int = UNSTREAM_STRING( &stream_data[ 48 ], 3, 1 );
    const_str_plain_len = UNSTREAM_STRING( &stream_data[ 51 ], 3, 1 );
    const_str_plain_scf = UNSTREAM_STRING( &stream_data[ 54 ], 3, 1 );
    const_str_plain_set = UNSTREAM_STRING( &stream_data[ 57 ], 3, 1 );
    const_str_plain_sys = UNSTREAM_STRING( &stream_data[ 60 ], 3, 1 );
    const_str_plain_yaw = UNSTREAM_STRING( &stream_data[ 63 ], 3, 1 );
    const_str_plain_args = UNSTREAM_STRING( &stream_data[ 66 ], 4, 1 );
    const_str_plain_crtp = UNSTREAM_STRING( &stream_data[ 70 ], 4, 1 );
    const_str_plain_data = UNSTREAM_STRING( &stream_data[ 74 ], 4, 1 );
    const_str_plain_down = UNSTREAM_STRING( &stream_data[ 78 ], 4, 1 );
    const_str_plain_iter = UNSTREAM_STRING( &stream_data[ 82 ], 4, 1 );
    const_str_plain_join = UNSTREAM_STRING( &stream_data[ 86 ], 4, 1 );
    const_str_plain_land = UNSTREAM_STRING( &stream_data[ 90 ], 4, 1 );
    const_str_plain_long = UNSTREAM_STRING( &stream_data[ 94 ], 4, 1 );
    const_str_plain_open = UNSTREAM_STRING( &stream_data[ 98 ], 4, 1 );
    const_str_plain_read = UNSTREAM_STRING( &stream_data[ 102 ], 4, 1 );
    const_str_plain_repr = UNSTREAM_STRING( &stream_data[ 106 ], 4, 1 );
    const_str_plain_roll = UNSTREAM_STRING( &stream_data[ 110 ], 4, 1 );
    const_str_plain_site = UNSTREAM_STRING( &stream_data[ 114 ], 4, 1 );
    const_str_plain_stop = UNSTREAM_STRING( &stream_data[ 118 ], 4, 1 );
    const_str_plain_time = UNSTREAM_STRING( &stream_data[ 122 ], 4, 1 );
    const_str_plain_type = UNSTREAM_STRING( &stream_data[ 126 ], 4, 1 );
    const_str_plain_20000 = UNSTREAM_STRING( &stream_data[ 130 ], 5, 0 );
    const_str_plain_ERROR = UNSTREAM_STRING( &stream_data[ 135 ], 5, 1 );
    const_str_plain_Event = UNSTREAM_STRING( &stream_data[ 140 ], 5, 1 );
    const_str_plain__exit = UNSTREAM_STRING( &stream_data[ 145 ], 5, 1 );
    const_str_plain_cflib = UNSTREAM_STRING( &stream_data[ 150 ], 5, 1 );
    const_str_plain_close = UNSTREAM_STRING( &stream_data[ 155 ], 5, 1 );
    const_str_plain_float = UNSTREAM_STRING( &stream_data[ 160 ], 5, 1 );
    const_str_plain_frame = UNSTREAM_STRING( &stream_data[ 165 ], 5, 1 );
    const_str_plain_level = UNSTREAM_STRING( &stream_data[ 170 ], 5, 1 );
    const_str_plain_param = UNSTREAM_STRING( &stream_data[ 175 ], 5, 1 );
    const_str_plain_pitch = UNSTREAM_STRING( &stream_data[ 180 ], 5, 1 );
    const_str_plain_range = UNSTREAM_STRING( &stream_data[ 185 ], 5, 1 );
    const_str_plain_sleep = UNSTREAM_STRING( &stream_data[ 190 ], 5, 1 );
    const_str_plain_start = UNSTREAM_STRING( &stream_data[ 195 ], 5, 1 );
    const_str_plain_strip = UNSTREAM_STRING( &stream_data[ 200 ], 5, 1 );
    const_str_plain_write = UNSTREAM_STRING( &stream_data[ 205 ], 5, 1 );
    const_str_angle_module = UNSTREAM_STRING( &stream_data[ 210 ], 8, 0 );
    const_str_plain_SIGINT = UNSTREAM_STRING( &stream_data[ 218 ], 6, 1 );
    const_str_plain_Thread = UNSTREAM_STRING( &stream_data[ 224 ], 6, 1 );
    const_str_plain_is_set = UNSTREAM_STRING( &stream_data[ 230 ], 6, 1 );
    const_str_plain_logger = UNSTREAM_STRING( &stream_data[ 236 ], 6, 1 );
    const_str_plain_signal = UNSTREAM_STRING( &stream_data[ 242 ], 6, 1 );
    const_str_plain_target = UNSTREAM_STRING( &stream_data[ 248 ], 6, 1 );
    const_str_plain_xrange = UNSTREAM_STRING( &stream_data[ 254 ], 6, 1 );
    const_str_plain___all__ = UNSTREAM_STRING( &stream_data[ 260 ], 7, 1 );
    const_str_plain___cmp__ = UNSTREAM_STRING( &stream_data[ 267 ], 7, 1 );
    const_str_plain___doc__ = UNSTREAM_STRING( &stream_data[ 274 ], 7, 1 );
    const_str_plain_aborted = UNSTREAM_STRING( &stream_data[ 281 ], 7, 1 );
    const_str_plain_compile = UNSTREAM_STRING( &stream_data[ 288 ], 7, 1 );
    const_str_plain_connect = UNSTREAM_STRING( &stream_data[ 295 ], 7, 1 );
    const_str_plain_forward = UNSTREAM_STRING( &stream_data[ 302 ], 7, 1 );
    const_str_plain_inspect = UNSTREAM_STRING( &stream_data[ 309 ], 7, 1 );
    const_str_plain_lg_stab = UNSTREAM_STRING( &stream_data[ 316 ], 7, 1 );
    const_str_plain_logging = UNSTREAM_STRING( &stream_data[ 323 ], 7, 1 );
    const_str_plain_posfile = UNSTREAM_STRING( &stream_data[ 330 ], 7, 1 );
    const_str_plain___dict__ = UNSTREAM_STRING( &stream_data[ 337 ], 8, 1 );
    const_str_plain___exit__ = UNSTREAM_STRING( &stream_data[ 345 ], 8, 1 );
    const_str_plain___file__ = UNSTREAM_STRING( &stream_data[ 353 ], 8, 1 );
    const_str_plain___main__ = UNSTREAM_STRING( &stream_data[ 361 ], 8, 1 );
    const_str_plain___name__ = UNSTREAM_STRING( &stream_data[ 369 ], 8, 1 );
    const_str_plain_exc_type = UNSTREAM_STRING( &stream_data[ 377 ], 8, 1 );
    const_str_plain_take_off = UNSTREAM_STRING( &stream_data[ 385 ], 8, 1 );
    const_str_plain_Crazyflie = UNSTREAM_STRING( &stream_data[ 393 ], 9, 1 );
    const_str_plain_LogConfig = UNSTREAM_STRING( &stream_data[ 402 ], 9, 1 );
    const_str_plain___class__ = UNSTREAM_STRING( &stream_data[ 411 ], 9, 1 );
    const_str_plain___enter__ = UNSTREAM_STRING( &stream_data[ 420 ], 9, 1 );
    const_str_plain_commander = UNSTREAM_STRING( &stream_data[ 429 ], 9, 1 );
    const_str_plain_exc_value = UNSTREAM_STRING( &stream_data[ 438 ], 9, 1 );
    const_str_plain_log_entry = UNSTREAM_STRING( &stream_data[ 447 ], 9, 1 );
    const_str_plain_open_link = UNSTREAM_STRING( &stream_data[ 456 ], 9, 1 );
    const_str_plain_set_value = UNSTREAM_STRING( &stream_data[ 465 ], 9, 1 );
    const_str_plain_threading = UNSTREAM_STRING( &stream_data[ 474 ], 9, 1 );
    const_str_plain_timestamp = UNSTREAM_STRING( &stream_data[ 483 ], 9, 1 );
    const_str_plain_turn_left = UNSTREAM_STRING( &stream_data[ 492 ], 9, 1 );
    const_str_plain_SyncLogger = UNSTREAM_STRING( &stream_data[ 501 ], 10, 1 );
    const_str_plain___import__ = UNSTREAM_STRING( &stream_data[ 511 ], 10, 1 );
    const_str_plain___module__ = UNSTREAM_STRING( &stream_data[ 521 ], 10, 1 );
    const_str_plain_close_link = UNSTREAM_STRING( &stream_data[ 531 ], 10, 1 );
    const_str_plain_turn_right = UNSTREAM_STRING( &stream_data[ 541 ], 10, 1 );
    const_str_plain___delattr__ = UNSTREAM_STRING( &stream_data[ 551 ], 11, 1 );
    const_str_plain___getattr__ = UNSTREAM_STRING( &stream_data[ 562 ], 11, 1 );
    const_str_plain___setattr__ = UNSTREAM_STRING( &stream_data[ 573 ], 11, 1 );
    const_str_plain_basicConfig = UNSTREAM_STRING( &stream_data[ 584 ], 11, 1 );
    const_tuple_float_0_3_tuple = MAKE_TUPLE1( const_float_0_3 );
    const_float_2_0 = UNSTREAM_FLOAT( &stream_data[ 595 ] );
    const_tuple_float_2_0_tuple = MAKE_TUPLE1( const_float_2_0 );
    const_str_plain___builtins__ = UNSTREAM_STRING( &stream_data[ 603 ], 12, 1 );
    const_str_plain_aborted_list = UNSTREAM_STRING( &stream_data[ 615 ], 12, 1 );
    const_str_plain_add_variable = UNSTREAM_STRING( &stream_data[ 627 ], 12, 1 );
    const_str_plain_init_drivers = UNSTREAM_STRING( &stream_data[ 639 ], 12, 1 );
    const_float_3_75 = UNSTREAM_FLOAT( &stream_data[ 651 ] );
    const_tuple_float_3_75_tuple = MAKE_TUPLE1( const_float_3_75 );
    const_str_plain_SyncCrazyflie = UNSTREAM_STRING( &stream_data[ 659 ], 13, 1 );
    const_str_plain___metaclass__ = UNSTREAM_STRING( &stream_data[ 672 ], 13, 1 );
    const_str_plain_exc_traceback = UNSTREAM_STRING( &stream_data[ 685 ], 13, 1 );
    const_str_plain_logger_thread = UNSTREAM_STRING( &stream_data[ 698 ], 13, 1 );
    const_str_plain_main_function = UNSTREAM_STRING( &stream_data[ 711 ], 13, 1 );
    const_str_plain_send_setpoint = UNSTREAM_STRING( &stream_data[ 724 ], 13, 1 );
    const_float_1_875 = UNSTREAM_FLOAT( &stream_data[ 737 ] );
    const_tuple_float_1_875_tuple = MAKE_TUPLE1( const_float_1_875 );
    const_str_plain_signal_handler = UNSTREAM_STRING( &stream_data[ 745 ], 14, 1 );
    const_str_plain_MotionCommander = UNSTREAM_STRING( &stream_data[ 759 ], 15, 1 );
    const_list_str_plain_Thread_list = MAKE_LIST1( const_str_plain_Thread );
    const_str_plain_logger_thread_stop = UNSTREAM_STRING( &stream_data[ 774 ], 18, 1 );
    const_tuple_str_plain_logger_tuple = MAKE_TUPLE1( const_str_plain_logger );
    const_list_str_plain_Crazyflie_list = MAKE_LIST1( const_str_plain_Crazyflie );
    const_list_str_plain_LogConfig_list = MAKE_LIST1( const_str_plain_LogConfig );
    const_list_str_plain_SyncLogger_list = MAKE_LIST1( const_str_plain_SyncLogger );
    const_str_plain_logger_thread_worker = UNSTREAM_STRING( &stream_data[ 792 ], 20, 1 );
    const_list_str_plain_SyncCrazyflie_list = MAKE_LIST1( const_str_plain_SyncCrazyflie );
    const_list_str_plain_MotionCommander_list = MAKE_LIST1( const_str_plain_MotionCommander );
    const_str_plain_ro_cache = UNSTREAM_STRING( &stream_data[ 812 ], 8, 1 );
    const_str_plain_ro = UNSTREAM_STRING( &stream_data[ 110 ], 2, 1 );
    const_str_plain_rw_cache = UNSTREAM_STRING( &stream_data[ 820 ], 8, 1 );
    const_str_plain_rw = UNSTREAM_STRING( &stream_data[ 304 ], 2, 1 );
    const_dict_243aa8eecd2da5a46892332cfdc4d450 = MAKE_DICT2( const_str_plain_ro, const_str_plain_ro_cache, const_str_plain_rw, const_str_plain_rw_cache );
    const_str_plain_enable_debug_driver = UNSTREAM_STRING( &stream_data[ 828 ], 19, 1 );
    const_dict_539d0a0b95c7f4877f43e57e4ab8d984 = MAKE_DICT1( Py_False, const_str_plain_enable_debug_driver );
    const_dict_62ee6ebcc3c4bc4b866e8cd064cf56b7 = MAKE_DICT1( const_int_0, const_str_plain_aborted );
    const_str_plain_velocity = UNSTREAM_STRING( &stream_data[ 847 ], 8, 1 );
    const_float_0_5 = UNSTREAM_FLOAT( &stream_data[ 855 ] );
    const_dict_aa4e253f8daa1e0b2cc0a262e29c3c19 = MAKE_DICT1( const_float_0_5, const_str_plain_velocity );
    const_str_plain_name = UNSTREAM_STRING( &stream_data[ 371 ], 4, 1 );
    const_str_plain_Position = UNSTREAM_STRING( &stream_data[ 863 ], 8, 1 );
    const_str_plain_period_in_ms = UNSTREAM_STRING( &stream_data[ 871 ], 12, 1 );
    const_int_pos_100 = PyInt_FromLong( 100l );
    const_dict_ce98f68090408fb17a6c2e7f34cf931d = MAKE_DICT2( const_str_plain_Position, const_str_plain_name, const_int_pos_100, const_str_plain_period_in_ms );
    const_dict_dc1a628231a099fc308313b6a124a2b1 = MAKE_DICT1( const_float_0_4, const_str_plain_velocity );
    const_str_digest_0345aa3382d9cabb03624fa419361084 = UNSTREAM_STRING( &stream_data[ 883 ], 29, 0 );
    const_str_digest_04817efd11c15364a6ec239780038862 = UNSTREAM_STRING( &stream_data[ 912 ], 4, 0 );
    const_str_digest_0c9434c1a2d38b03084e8af867a5a591 = UNSTREAM_STRING( &stream_data[ 916 ], 12, 0 );
    const_str_digest_145ace45251939555fbe881f24d19dc6 = UNSTREAM_STRING( &stream_data[ 928 ], 53, 0 );
    const_str_digest_187879fed30627459387957f2c0edddf = UNSTREAM_STRING( &stream_data[ 981 ], 26, 0 );
    const_str_digest_1eb417079397bafee1de8a2307718a67 = UNSTREAM_STRING( &stream_data[ 1007 ], 29, 0 );
    const_str_digest_245adc7cddbc80c6223f99aedd14303b = UNSTREAM_STRING( &stream_data[ 1036 ], 16, 0 );
    const_str_digest_24d1b912a24567d4b0f37e65866caec4 = UNSTREAM_STRING( &stream_data[ 1052 ], 20, 0 );
    const_str_digest_2930a74bfe0dfc7d45d37b747109010a = UNSTREAM_STRING( &stream_data[ 1072 ], 19, 0 );
    const_str_digest_2d0bc760d21081fbbe357ac9bd3098d1 = UNSTREAM_STRING( &stream_data[ 1091 ], 20, 0 );
    const_str_digest_2f68ad040984e87524a290e4cb58117f = UNSTREAM_STRING( &stream_data[ 1111 ], 4, 0 );
    const_str_digest_31d2b49447b7edba18cc9ff536133c53 = UNSTREAM_STRING( &stream_data[ 1115 ], 10, 0 );
    const_str_digest_3bf51efc682f557ee837839a9da02b41 = UNSTREAM_STRING( &stream_data[ 1125 ], 34, 0 );
    const_str_digest_44c948084dd4e5ab67b1ec497d101727 = UNSTREAM_STRING( &stream_data[ 1159 ], 6, 0 );
    const_str_digest_4e2c018a5300351973557add0a24141a = UNSTREAM_STRING( &stream_data[ 1165 ], 14, 0 );
    const_str_digest_60a23ecc05ca99686bc518474cb1df7a = UNSTREAM_STRING( &stream_data[ 1179 ], 20, 0 );
    const_str_digest_68a9ac2f1f2f7e49c7bad57ba31976f6 = UNSTREAM_STRING( &stream_data[ 1199 ], 12, 0 );
    const_str_digest_6cc08d0712c8d9467d68c797bc086fed = UNSTREAM_STRING( &stream_data[ 1211 ], 13, 0 );
    const_str_digest_6fae5998bcb63ea7f2ecb4f9dea2b2a7 = UNSTREAM_STRING( &stream_data[ 1224 ], 10, 0 );
    const_str_digest_6fcf7cef0081a3be07ee72eeaf847b1f = UNSTREAM_STRING( &stream_data[ 1234 ], 20, 0 );
    const_str_digest_7390cc453f512da13f0d281a65059885 = UNSTREAM_STRING( &stream_data[ 1254 ], 16, 0 );
    const_str_digest_77e23e10fe1b9556624317a002d8b1cc = UNSTREAM_STRING( &stream_data[ 1270 ], 4, 0 );
    const_str_digest_8c90b05af7802ee53561cbc1fa1ae964 = UNSTREAM_STRING( &stream_data[ 1274 ], 19, 0 );
    const_str_digest_9f85aa3708239e0c778cb00a86748a3c = UNSTREAM_STRING( &stream_data[ 1293 ], 7, 0 );
    const_str_digest_a2c1833e0fd5389050407cccd2b5fa06 = UNSTREAM_STRING( &stream_data[ 1300 ], 16, 0 );
    const_str_digest_a4d5e4010a0ee714d42205db4918cf2b = UNSTREAM_STRING( &stream_data[ 1316 ], 15, 0 );
    const_str_digest_b03c2e2c3dee02212866e618daae5997 = UNSTREAM_STRING( &stream_data[ 1331 ], 17, 0 );
    const_str_digest_b064bc73fc5d82cb15ddbd6cb7eeb804 = UNSTREAM_STRING( &stream_data[ 1348 ], 14, 0 );
    const_str_digest_bb098d44f0e169e5eb07c575224d8553 = UNSTREAM_STRING( &stream_data[ 1362 ], 13, 0 );
    const_str_digest_bb9871a70568c3d29995e4ee517f0c1d = UNSTREAM_STRING( &stream_data[ 1375 ], 14, 0 );
    const_str_digest_bd56e81c8f1ef1514e78dc5e67b5b1a2 = UNSTREAM_STRING( &stream_data[ 1389 ], 16, 0 );
    const_str_digest_c38568aedd7bb1c9232846890b69ebc7 = UNSTREAM_STRING( &stream_data[ 1405 ], 21, 0 );
    const_str_digest_c42384e11d8039023cc63f738682e4b1 = UNSTREAM_STRING( &stream_data[ 1426 ], 15, 0 );
    const_str_digest_cc876ca77c133b1ab9057ea27426e8d3 = UNSTREAM_STRING( &stream_data[ 1441 ], 14, 0 );
    const_str_digest_d2f986057c6f7103b7ca87474919f5c2 = UNSTREAM_STRING( &stream_data[ 1455 ], 14, 0 );
    const_str_digest_d4fc4410d79effb72c093ecd89b0a15d = UNSTREAM_STRING( &stream_data[ 1469 ], 18, 0 );
    const_str_digest_da28a3a52fef5cfcfe6516207c87623e = UNSTREAM_STRING( &stream_data[ 1487 ], 21, 0 );
    const_str_digest_e1b4f55ae195000b1f44d069fa0971fb = UNSTREAM_STRING( &stream_data[ 1508 ], 19, 0 );
    const_str_digest_e7511362545f1e8e4835d7768b8645c2 = UNSTREAM_STRING( &stream_data[ 1527 ], 21, 0 );
    const_str_digest_e9fa29284a0eebe10618a41a87657254 = UNSTREAM_STRING( &stream_data[ 1548 ], 14, 0 );
    const_str_digest_f0ea728aa6a36615358e93c174b00f87 = UNSTREAM_STRING( &stream_data[ 981 ], 15, 0 );
    const_str_digest_f991bf363475592a622e85cda89309dc = UNSTREAM_STRING( &stream_data[ 1562 ], 13, 0 );
    const_str_digest_fda94c46b142d763eef4593313ed7e9f = UNSTREAM_STRING( &stream_data[ 1575 ], 5, 0 );
    const_tuple_4827392191ca93bcc4094155298f412c_tuple = MAKE_TUPLE11( const_str_plain_logger, const_str_plain_posfile, const_str_plain_log_entry, const_str_plain_timestamp, const_str_plain_data, const_str_plain_px, const_str_plain_py, const_str_plain_pz, const_str_plain_roll, const_str_plain_pitch, const_str_plain_yaw );
    const_tuple_78f9ded54d9be9c5c92b9e64a92944b2_tuple = MAKE_TUPLE9( const_str_plain_URI, const_str_plain_lg_stab, const_str_plain_cf, const_str_plain_scf, const_str_plain_mc, const_str_plain_logger, const_str_plain_logger_thread, const_str_plain_aborted_list, const_str_plain_signal_handler );
    const_tuple_str_plain_signal_str_plain_frame_tuple = MAKE_TUPLE2( const_str_plain_signal, const_str_plain_frame );
    codeobj_b7454df100b49567308905a916008142 = MAKE_CODEOBJ( const_str_digest_9f85aa3708239e0c778cb00a86748a3c, const_str_angle_module, 0, const_tuple_empty, 0, 0 );
    codeobj_5ca39b17b9682cc8ca19997fc3ea65f4 = MAKE_CODEOBJ( const_str_digest_9f85aa3708239e0c778cb00a86748a3c, const_str_plain_logger_thread_worker, 21, const_tuple_str_plain_logger_tuple, 1, CO_NEWLOCALS | CO_OPTIMIZED );
    codeobj_cd532aaf552b21af9328ca0de7c0f3dc = MAKE_CODEOBJ( const_str_digest_9f85aa3708239e0c778cb00a86748a3c, const_str_plain_logger_thread_worker, 21, const_tuple_4827392191ca93bcc4094155298f412c_tuple, 1, CO_NEWLOCALS | CO_OPTIMIZED );
    codeobj_b6866d1d3dae1aec7ae569970b6db7dd = MAKE_CODEOBJ( const_str_digest_9f85aa3708239e0c778cb00a86748a3c, const_str_plain_main_function, 45, const_tuple_empty, 0, CO_NEWLOCALS | CO_OPTIMIZED );
    codeobj_37a54b2662ac0a8cb93e5380370c546c = MAKE_CODEOBJ( const_str_digest_9f85aa3708239e0c778cb00a86748a3c, const_str_plain_main_function, 45, const_tuple_78f9ded54d9be9c5c92b9e64a92944b2_tuple, 0, CO_NEWLOCALS | CO_OPTIMIZED );
    codeobj_d04e0171ddf873f35efd2209c880fe9b = MAKE_CODEOBJ( const_str_digest_9f85aa3708239e0c778cb00a86748a3c, const_str_plain_signal_handler, 106, const_tuple_str_plain_signal_str_plain_frame_tuple, 2, CO_NEWLOCALS | CO_OPTIMIZED );
}

void _initConstants( void )
{
    if ( _sentinel_value == NULL )
    {
#if PYTHON_VERSION < 300
        _sentinel_value = PyCObject_FromVoidPtr( NULL, NULL );
#else
        // The NULL value is not allowed for a capsule, so use something else.
        _sentinel_value = PyCapsule_New( (void *)27, "sentinel", NULL );
#endif
        assert( _sentinel_value );

        __initConstants();
    }
}
