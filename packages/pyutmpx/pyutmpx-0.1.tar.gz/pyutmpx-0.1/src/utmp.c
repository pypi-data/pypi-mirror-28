/* ****************************************************************************
 * utmp.c -- utmpx file iterator definition.
 * Copyright (C) 2017-2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */
#include "main.h"
#include <errno.h>
#include <utmpx.h>

/* pyutmpx_utmp_t: object structure.
 * As this module uses the POSIX interface to utmp, using a global cursor,
 * this structure does not require any auxiliary data for now.
 * More data will be required if the module allows more interactions with
 * its environment, such as direct utmp/wtmp/btmp file reading, or
 * interaction with a utmp-managing daemon such as utmps. */

typedef struct {
	PyObject_HEAD
} pyutmpx_utmp_t;

/* ************************************************************************* */
/*  Constructor, destructor                                                  */
/* ************************************************************************* */
/* pyutmpx_create_utmp: create the Python object.
 * It does not initialize the connexion to the file,
 * see `pyutmpx_init_utmp()`. */

static PyObject* pyutmpx_create_utmp(PyTypeObject* type, PyObject* args,
	PyObject* kw)
{
	pyutmpx_utmp_t *self;

	self = (pyutmpx_utmp_t*)type->tp_alloc(type, 0);
	return ((PyObject*)self);
}

/* pyutmpx_init_utmp: initialize the Python object.
 * Looks for the file, check if it has the rights to open it, and stuff. */

static int pyutmpx_init_utmp(pyutmpx_utmp_t* self, PyObject* args,
	PyObject* kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	/* Reset the thing. */
	setutxent();

	/* Everything went well! */
	return (0);
}

/* pyutmpx_exit_utmp: destroy the Python object.
 * Deinitializes everything it can. */

static void pyutmpx_exit_utmp(pyutmpx_utmp_t* self)
{
	if (!self) return;

	/* Free the Python object. */
	Py_TYPE(self)->tp_free((PyObject*)self);
}

/* ************************************************************************* */
/*  Iterator-related methods                                                 */
/* ************************************************************************* */
/* pyutmpx_iter_utmp: return self because we are iterable. */

static PyObject* pyutmpx_iter_utmp(pyutmpx_utmp_t* self)
{
	Py_INCREF(self);
	return ((PyObject*)self);
}

/* pyutmpx_next_utmp: return next element in self. */

static PyObject* pyutmpx_next_utmp(pyutmpx_utmp_t* self)
{
	PyObject *id = NULL, *user = NULL, *line = NULL, *pid = NULL,
		*type = NULL, *date = NULL;
	PyObject *arglist = NULL, *entry = NULL;
	struct utmpx* ent;
	int failed = 1;

	/* Get the entry and iterate using the POSIX utmpx interface. */
	do {
		ent = getutxent();
		if (!ent) {
			PyErr_SetNone(PyExc_StopIteration);
			return (NULL);
		}
	} while (!(type = pyutmpx_get_type(ent->ut_type)));

	/* Get the date. */
	date = pyutmpx_get_datetime(&ent->ut_tv);
	if (!date)
		goto fail;

	/* Get the miscallaneous ID. */
	id = Py_BuildValue("s", ent->ut_id);
	if (!id)
		goto fail;

	/* Get the user. */
	user = Py_BuildValue("s", ent->ut_user);
	if (!user)
		goto fail;

	/* Get the device (line). */
	line = Py_BuildValue("s", ent->ut_line);
	if (!line)
		goto fail;

	/* Get the PID. */
	pid = Py_BuildValue("k", ent->ut_pid);
	if (!pid)
		goto fail;

	/* Create the argument list and call the object to create it. */
	arglist = Py_BuildValue("OOOOOO", id, type, user, line, date, pid);
	if (!arglist)
		goto fail;

	entry = PyObject_CallObject((PyObject*)&pyutmpx_entry, arglist);
	if (!entry)
		goto fail;

	/* End. */
	Py_INCREF(entry);
	failed = 0;
fail:
	Py_XDECREF(arglist);

	/* Even in the case where everything went okay, the object will have
	 * incremented the reference count to these objects, so this should
	 * be okay. */

	Py_XDECREF(id);
	Py_XDECREF(user);
	Py_XDECREF(line);
	Py_XDECREF(pid);
	Py_XDECREF(type);
	Py_XDECREF(date);
	Py_XDECREF(entry);

	/* Go, go, go! */

	if (failed)
		PyErr_SetString(PyExc_Exception, "");
	return (entry);
}

/* ************************************************************************* */
/*  Class definition                                                         */
/* ************************************************************************* */
static PyMethodDef pyutmpx_utmp_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyMemberDef pyutmpx_utmp_members[] = {
	{NULL}
};

PyTypeObject pyutmpx_utmp = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */
	.tp_name = "pyutmpx.utmp",
	.tp_doc = "utmp entries iterator",
	.tp_basicsize = sizeof(pyutmpx_utmp_t),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */
	.tp_new = pyutmpx_create_utmp,
	.tp_init = (initproc)pyutmpx_init_utmp,
	.tp_dealloc = (destructor)pyutmpx_exit_utmp,
	.tp_methods = pyutmpx_utmp_methods,
	.tp_iter = (getiterfunc)pyutmpx_iter_utmp,
	.tp_iternext = (iternextfunc)pyutmpx_next_utmp,

	/* Members. */
	.tp_members = pyutmpx_utmp_members
};
