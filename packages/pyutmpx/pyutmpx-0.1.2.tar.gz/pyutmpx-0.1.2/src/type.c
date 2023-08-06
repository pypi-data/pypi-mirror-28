/* ****************************************************************************
 * type.c -- get the utmpx entry type.
 * Copyright (C) 2017-2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */
#include <pyutmpx.h>
#include <utmpx.h>

/* Objects definition. */
PyObject* pyutmpx_boot_time;
PyObject* pyutmpx_old_time;
PyObject* pyutmpx_new_time;
PyObject* pyutmpx_user_process;
PyObject* pyutmpx_init_process;
PyObject* pyutmpx_login_process;
PyObject* pyutmpx_dead_process;

/* pyutmpx_prepare_types(): initialize the types and add them to the module. */

int pyutmpx_prepare_types(PyObject* m)
{
	/* Create the objects. */
	pyutmpx_boot_time = Py_BuildValue("i", 1);
	pyutmpx_old_time = Py_BuildValue("i", 2);
	pyutmpx_new_time = Py_BuildValue("i", 3);
	pyutmpx_user_process = Py_BuildValue("i", 4);
	pyutmpx_init_process = Py_BuildValue("i", 5);
	pyutmpx_login_process = Py_BuildValue("i", 6);
	pyutmpx_dead_process = Py_BuildValue("i", 7);

	/* Check that the creation went well. */
	if (!pyutmpx_boot_time || !pyutmpx_old_time || !pyutmpx_new_time
	 || !pyutmpx_user_process || !pyutmpx_init_process
	 || !pyutmpx_login_process || !pyutmpx_dead_process) {
		pyutmpx_destroy_types();
		return (1);
	}

	/* Add the objects to the module. */
	PyModule_AddObject(m, "BOOT_TIME", pyutmpx_boot_time);
	PyModule_AddObject(m, "OLD_TIME", pyutmpx_old_time);
	PyModule_AddObject(m, "NEW_TIME", pyutmpx_new_time);
	PyModule_AddObject(m, "USER_PROCESS", pyutmpx_user_process);
	PyModule_AddObject(m, "INIT_PROCESS", pyutmpx_init_process);
	PyModule_AddObject(m, "LOGIN_PROCESS", pyutmpx_login_process);
	PyModule_AddObject(m, "DEAD_PROCESS", pyutmpx_dead_process);

	return (0);
}

/* pyutmpx_destroy_types(): destroy the types.
 * Must be called after `pyutmpx_prepare_types()`. */

void pyutmpx_destroy_types(void)
{
	Py_XDECREF(pyutmpx_boot_time);
	Py_XDECREF(pyutmpx_old_time);
	Py_XDECREF(pyutmpx_new_time);
	Py_XDECREF(pyutmpx_user_process);
	Py_XDECREF(pyutmpx_init_process);
	Py_XDECREF(pyutmpx_login_process);
	Py_XDECREF(pyutmpx_dead_process);
}

/* pyutmpx_get_type: get the record type using a standard code. */

PyObject* pyutmpx_get_type(int ut_type)
{
	PyObject *type = NULL;

	switch (ut_type) {
	case BOOT_TIME:
		type = pyutmpx_boot_time;
		break;
	case OLD_TIME:
		type = pyutmpx_old_time;
		break;
	case NEW_TIME:
		type = pyutmpx_new_time;
		break;
	case USER_PROCESS:
		type = pyutmpx_user_process;
		break;
	case INIT_PROCESS:
		type = pyutmpx_init_process;
		break;
	case LOGIN_PROCESS:
		type = pyutmpx_login_process;
		break;
	case DEAD_PROCESS:
		type = pyutmpx_dead_process;
		break;
	default:
		/* EMPTY is managed here, with non-standard types. */
		return (NULL);
	}

	Py_INCREF(type);
	return (type);
}

/* pyutmpx_get_type_string: get the record type string for logging. */

const char* pyutmpx_get_type_string(PyObject* type)
{
	int val;

	if (PyArg_Parse(type, "i", &val) < 0)
		val = 0;

	switch (val) {
	case 1:
		return ("BOOT_TIME");
	case 2:
		return ("OLD_TIME");
	case 3:
		return ("NEW_TIME");
	case 4:
		return ("USER_PROCESS");
	case 5:
		return ("INIT_PROCESS");
	case 6:
		return ("LOGIN_PROCESS");
	case 7:
		return ("DEAD_PROCESS");
	}

	return "(unknown)";
}
