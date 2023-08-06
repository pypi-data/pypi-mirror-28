/* ****************************************************************************
 * main.h -- pyutmpx module header.
 * Copyright (C) 2017-2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */
#ifndef  MAIN_H
# define MAIN_H 2018020601
# include <Python.h>
# include <structmember.h>

extern PyTypeObject pyutmpx_utmp;
extern PyTypeObject pyutmpx_entry;

extern int pyutmpx_prepare_types(PyObject* module);
extern void pyutmpx_destroy_types(void);
extern PyObject* pyutmpx_get_type(int ut_type);
extern const char* pyutmpx_get_type_string(PyObject* type);

extern PyObject* pyutmpx_get_datetime(const struct timeval* tv);

#endif /* MAIN_H */
