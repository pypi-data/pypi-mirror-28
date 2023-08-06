/* ****************************************************************************
 * main.c -- pyutmpx module definition.
 * Copyright (C) 2017-2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */
#include "main.h"
# include <datetime.h>

/* Utility to get a datetime from a timeval. */

PyObject *pyutmpx_get_datetime(const struct timeval *tv)
{
	PyObject *result = NULL;
	PyObject *epoch = NULL, *date_delta = NULL;

	epoch = PyDateTime_FromDateAndTime(1970, 1, 1, 0, 0, 0, 0);
	date_delta = PyDelta_FromDSU(0, tv->tv_sec, tv->tv_usec);
	if (!epoch || !date_delta)
		goto fail;

	result = PyNumber_Add(epoch, date_delta);

fail:
	Py_XDECREF(epoch);
	Py_XDECREF(date_delta);

	return (result);
}

/* Module methods. */

static PyMethodDef module_methods[] = {
	{NULL, NULL, 0, NULL}
};

/* Module definition. */

static struct PyModuleDef module = {
	PyModuleDef_HEAD_INIT,

	/* General information. */
	.m_name = "pyutmpx",
	.m_doc = "This module provides a utmp reader.",
	.m_methods = module_methods,

	/* Keep state in global variables. */
	.m_size = -1,
};

/* Module initialization. */

PyMODINIT_FUNC PyInit_pyutmpx(void)
{
	PyObject *m;

	/* Initialize the module. */
	m = PyModule_Create(&module);
	if (!m)
		goto fail;

	/* Import the datetime module. */
	PyDateTime_IMPORT;

	/* Add the utmp iterator type to the module. */
	if (PyType_Ready(&pyutmpx_utmp) < 0)
		goto fail;
	Py_INCREF(&pyutmpx_utmp);
	PyModule_AddObject(m, "utmp", (PyObject*)&pyutmpx_utmp);

	/* Add the utmp entry type to the module. */
	if (PyType_Ready(&pyutmpx_entry) < 0)
		goto fail;
	Py_INCREF(&pyutmpx_entry);
	PyModule_AddObject(m, "utmp_entry", (PyObject*)&pyutmpx_entry);

	/* Make the constants and add them to the module. */
	if (pyutmpx_prepare_types(m))
		goto fail;

	/* Everything went well in the end :) */
	return (m);
fail:
	pyutmpx_destroy_types();
	Py_XDECREF(&pyutmpx_utmp);
	Py_XDECREF(&pyutmpx_entry);
	Py_XDECREF(m);
	return (NULL);
}
