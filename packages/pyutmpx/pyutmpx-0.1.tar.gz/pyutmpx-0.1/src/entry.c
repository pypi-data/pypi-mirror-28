/* ****************************************************************************
 * entry.c -- manage a utmpx entry.
 * Copyright (C) 2017-2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */
#include "main.h"
#include <string.h>

/* pyutmpx_ent_t: object structure.
 * Contains all the data that a utmpx entry contains. */

typedef struct {
	PyObject_HEAD

	PyObject* id;
	PyObject* type;
	PyObject* user;
	PyObject* line;
	PyObject* time;
	PyObject* pid;
} pyutmpx_ent_t;

/* ************************************************************************* */
/*  Constructor, destructor                                                  */
/* ************************************************************************* */
/* pyutmpx_create_ent: create the Python object. */

static PyObject* pyutmpx_create_ent(PyTypeObject* type, PyObject* args,
	PyObject* kw)
{
	pyutmpx_ent_t* self;

	self = (pyutmpx_ent_t*)type->tp_alloc(type, 0);
	if (self) {
		self->id = NULL;
		self->type = NULL;
		self->user = NULL;
		self->line = NULL;
		self->time = NULL;
		self->pid = NULL;
	}

	return ((PyObject*)self);
}

/* pyutmpx_init_ent: initialize the Python object.
 * Looks for the file, check if it has the rights to open it, and stuff. */

static int pyutmpx_init_ent(pyutmpx_ent_t* self, PyObject* args, PyObject* kw)
{
	char *keywords[] = {"id", "type", "user", "line", "time",
		"pid", NULL};

	if (!PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO", keywords,
		&self->id, &self->type, &self->user, &self->line, &self->time,
		&self->pid))
		return (-1);

	/* TODO: check the argument types */

	Py_INCREF(self->id);
	Py_INCREF(self->type);
	Py_INCREF(self->user);
	Py_INCREF(self->line);
	Py_INCREF(self->time);
	Py_INCREF(self->pid);

	/* Everything went well! */
	return (0);
}

/* pyutmpx_exit_ent: destroy the Python object.
 * Deinitializes everything it can. */

static void pyutmpx_exit_ent(pyutmpx_ent_t* self)
{
	if (!self) return;

	/* Free the members. */
	Py_XDECREF(self->id);
	Py_XDECREF(self->type);
	Py_XDECREF(self->user);
	Py_XDECREF(self->line);
	Py_XDECREF(self->time);
	Py_XDECREF(self->pid);

	/* Free the Python object. */
	Py_TYPE(self)->tp_free((PyObject*)self);
}

/* ************************************************************************* */
/*  Representation                                                           */
/* ************************************************************************* */
/* pyutmpx_repr_ent: represent the Python object.
 * This is useful for debugging. */

static void put_str(char **ps, size_t *n, const char *s)
{
	size_t len;

	strncpy(*ps, s, *n);
	len = strlen(*ps);
	*ps += len;
	*n -= len;
}

static void put_repr(char **ps, size_t *n, PyObject *o)
{
	PyObject *repr, *repr_utf8;
	const char *r; int has_failed = 1;

	/* Get the representation. */
	repr = PyObject_Repr(o);
	if (!repr)
		goto fail;

	/* Encode the representation as UTF-8 */
	repr_utf8 = PyUnicode_AsEncodedString(repr, "utf-8", "~E~");
	Py_DECREF(repr);
	if (!repr_utf8)
		goto fail;

	/* Get a C string from the Python encoded string. */
	r = PyBytes_AS_STRING(repr_utf8);
	Py_DECREF(repr_utf8);

	/* Get a default string if has failed. */
	has_failed = 0;
fail:
	if (has_failed)
		r = "(unknown)";

	/* Copy into the final buffer. */
	put_str(ps, n, r);
}

static PyObject* pyutmpx_repr_ent(pyutmpx_ent_t* self)
{
	char buf[1024], *s = buf;
	size_t len = 1024;

	put_str(&s, &len, "utmp_entry(type=");
	put_str(&s, &len, pyutmpx_get_type_string(self->type));
	put_str(&s, &len, ", time=");
	put_repr(&s, &len, self->time);
	put_str(&s, &len, ", user=");
	put_repr(&s, &len, self->user);
	put_str(&s, &len, ", line=");
	put_repr(&s, &len, self->line);
	put_str(&s, &len, ", pid=");
	put_repr(&s, &len, self->pid);
	put_str(&s, &len, ")");

	return (Py_BuildValue("s", buf));
}

/* ************************************************************************* */
/*  Class definition                                                         */
/* ************************************************************************* */
static PyMethodDef pyutmpx_ent_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyMemberDef pyutmpx_ent_members[] = {
	{"id", T_OBJECT, offsetof(pyutmpx_ent_t, id),
		READONLY, "Unspecified initialization process identifier."},
	{"type", T_OBJECT, offsetof(pyutmpx_ent_t, type),
		READONLY, "Type of entry."},
	{"user", T_OBJECT, offsetof(pyutmpx_ent_t, user),
		READONLY, "User login name."},
	{"line", T_OBJECT, offsetof(pyutmpx_ent_t, line),
		READONLY, "Device name."},
	{"time", T_OBJECT, offsetof(pyutmpx_ent_t, time),
		READONLY, "Time entry was made."},
	{"pid", T_OBJECT, offsetof(pyutmpx_ent_t, pid),
		READONLY, "Process ID."},

	{NULL}
};

PyTypeObject pyutmpx_entry = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */
	.tp_name = "pyutmpx.utmp_entry",
	.tp_doc = "utmp entry",
	.tp_basicsize = sizeof(pyutmpx_ent_t),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */
	.tp_new = pyutmpx_create_ent,
	.tp_init = (initproc)pyutmpx_init_ent,
	.tp_dealloc = (destructor)pyutmpx_exit_ent,
	.tp_repr = (reprfunc)pyutmpx_repr_ent,
	.tp_methods = pyutmpx_ent_methods,

	/* Members. */
	.tp_members = pyutmpx_ent_members
};
