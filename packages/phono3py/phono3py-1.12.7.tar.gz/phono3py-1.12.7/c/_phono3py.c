/* Copyright (C) 2015 Atsushi Togo */
/* All rights reserved. */

/* This file is part of phonopy. */

/* Redistribution and use in source and binary forms, with or without */
/* modification, are permitted provided that the following conditions */
/* are met: */

/* * Redistributions of source code must retain the above copyright */
/*   notice, this list of conditions and the following disclaimer. */

/* * Redistributions in binary form must reproduce the above copyright */
/*   notice, this list of conditions and the following disclaimer in */
/*   the documentation and/or other materials provided with the */
/*   distribution. */

/* * Neither the name of the phonopy project nor the names of its */
/*   contributors may be used to endorse or promote products derived */
/*   from this software without specific prior written permission. */

/* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS */
/* "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT */
/* LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS */
/* FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE */
/* COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, */
/* INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, */
/* BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; */
/* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER */
/* CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT */
/* LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN */
/* ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE */
/* POSSIBILITY OF SUCH DAMAGE. */

#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <numpy/arrayobject.h>
#include <lapack_wrapper.h>
#include <phonoc_array.h>
#include <phonoc_const.h>
#include <phonon3_h/fc3.h>
#include <phonon3_h/frequency_shift.h>
#include <phonon3_h/interaction.h>
#include <phonon3_h/imag_self_energy_with_g.h>
#include <phonon3_h/pp_collision.h>
#include <phonon3_h/collision_matrix.h>
#include <other_h/isotope.h>
#include <triplet_h/triplet.h>
#include <tetrahedron_method.h>

/* #define LIBFLAME */
#ifdef LIBFLAME
#include <flame_wrapper.h>
#endif

static PyObject * py_get_interaction(PyObject *self, PyObject *args);
static PyObject * py_get_pp_collision(PyObject *self, PyObject *args);
static PyObject *
py_get_pp_collision_with_sigma(PyObject *self, PyObject *args);
static PyObject *
py_get_imag_self_energy_with_g(PyObject *self, PyObject *args);
static PyObject *
py_get_detailed_imag_self_energy_with_g(PyObject *self, PyObject *args);
static PyObject * py_get_frequency_shift_at_bands(PyObject *self,
                                                  PyObject *args);
static PyObject * py_get_collision_matrix(PyObject *self, PyObject *args);
static PyObject * py_get_reducible_collision_matrix(PyObject *self,
                                                    PyObject *args);
static PyObject * py_symmetrize_collision_matrix(PyObject *self,
                                                 PyObject *args);
static PyObject * py_distribute_fc3(PyObject *self, PyObject *args);
static PyObject * py_get_isotope_strength(PyObject *self, PyObject *args);
static PyObject * py_get_thm_isotope_strength(PyObject *self, PyObject *args);
static PyObject * py_set_permutation_symmetry_fc3(PyObject *self,
                                                  PyObject *args);
static PyObject * py_get_neighboring_gird_points(PyObject *self, PyObject *args);
static PyObject * py_set_integration_weights(PyObject *self, PyObject *args);
static PyObject *
py_tpl_get_triplets_reciprocal_mesh_at_q(PyObject *self, PyObject *args);
static PyObject * py_tpl_get_BZ_triplets_at_q(PyObject *self, PyObject *args);
static PyObject *
py_set_triplets_integration_weights(PyObject *self, PyObject *args);
static PyObject *
py_set_triplets_integration_weights_with_sigma(PyObject *self, PyObject *args);
static PyObject *
py_diagonalize_collision_matrix(PyObject *self, PyObject *args);
static PyObject * py_pinv_from_eigensolution(PyObject *self, PyObject *args);

#ifdef LIBFLAME
static PyObject * py_inverse_collision_matrix_libflame(PyObject *self, PyObject *args);
#endif

static void pinv_from_eigensolution(double *data,
                                    const double *eigvals,
                                    const int size,
                                    const double cutoff,
                                    const int pinv_method);
static void show_colmat_info(const PyArrayObject *collision_matrix_py,
                             const int i_sigma,
                             const int i_temp,
                             const int adrs_shift);

struct module_state {
  PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct module_state _state;
#endif

static PyObject *
error_out(PyObject *m) {
  struct module_state *st = GETSTATE(m);
  PyErr_SetString(st->error, "something bad happened");
  return NULL;
}

static PyMethodDef _phono3py_methods[] = {
  {"error_out", (PyCFunction)error_out, METH_NOARGS, NULL},
  {"interaction",
   (PyCFunction)py_get_interaction,
   METH_VARARGS,
   "Interaction of triplets"},
  {"pp_collision",
   (PyCFunction)py_get_pp_collision,
   METH_VARARGS,
   "Collision and ph-ph calculation"},
  {"pp_collision_with_sigma",
   (PyCFunction)py_get_pp_collision_with_sigma,
   METH_VARARGS,
   "Collision and ph-ph calculation for smearing method"},
  {"imag_self_energy_with_g",
   (PyCFunction)py_get_imag_self_energy_with_g,
   METH_VARARGS,
   "Imaginary part of self energy at frequency points with g"},
  {"detailed_imag_self_energy_with_g",
   (PyCFunction)py_get_detailed_imag_self_energy_with_g,
   METH_VARARGS,
   "Detailed contribution to imaginary part of self energy at frequency points with g"},
  {"frequency_shift_at_bands",
   (PyCFunction)py_get_frequency_shift_at_bands,
   METH_VARARGS,
   "Phonon frequency shift from third order force constants"},
  {"collision_matrix",
   (PyCFunction)py_get_collision_matrix,
   METH_VARARGS,
   "Collision matrix with g"},
  {"reducible_collision_matrix",
   (PyCFunction)py_get_reducible_collision_matrix,
   METH_VARARGS,
   "Collision matrix with g for reducible grid points"},
  {"symmetrize_collision_matrix",
   (PyCFunction)py_symmetrize_collision_matrix,
   METH_VARARGS,
   "Symmetrize collision matrix"},
  {"distribute_fc3",
   (PyCFunction)py_distribute_fc3,
   METH_VARARGS,
   "Distribute least fc3 to full fc3"},
  {"isotope_strength",
   (PyCFunction)py_get_isotope_strength,
   METH_VARARGS,
   "Isotope scattering strength"},
  {"thm_isotope_strength",
   (PyCFunction)py_get_thm_isotope_strength,
   METH_VARARGS,
   "Isotope scattering strength for tetrahedron_method"},
  {"permutation_symmetry_fc3",
   (PyCFunction)py_set_permutation_symmetry_fc3,
   METH_VARARGS,
   "Set permutation symmetry for fc3"},
  {"neighboring_grid_points",
   (PyCFunction)py_get_neighboring_gird_points,
   METH_VARARGS,
   "Neighboring grid points by relative grid addresses"},
  {"integration_weights",
   (PyCFunction)py_set_integration_weights,
   METH_VARARGS,
   "Integration weights of tetrahedron method"},
  {"triplets_reciprocal_mesh_at_q",
   (PyCFunction)py_tpl_get_triplets_reciprocal_mesh_at_q,
   METH_VARARGS,
   "Triplets on reciprocal mesh points at a specific q-point"},
  {"BZ_triplets_at_q",
   (PyCFunction)py_tpl_get_BZ_triplets_at_q,
   METH_VARARGS,
   "Triplets in reciprocal primitive lattice are transformed to those in BZ."},
  {"triplets_integration_weights",
   (PyCFunction)py_set_triplets_integration_weights,
   METH_VARARGS,
   "Integration weights of tetrahedron method for triplets"},
  {"triplets_integration_weights_with_sigma",
   (PyCFunction)py_set_triplets_integration_weights_with_sigma,
   METH_VARARGS,
   "Integration weights of smearing method for triplets"},
  {"diagonalize_collision_matrix",
   (PyCFunction)py_diagonalize_collision_matrix,
   METH_VARARGS,
   "Diagonalize and optionally pseudo-inverse using Lapack dsyev(d)"},
  {"pinv_from_eigensolution",
   (PyCFunction)py_pinv_from_eigensolution,
   METH_VARARGS,
   "Pseudo-inverse from eigensolution"},
#ifdef LIBFLAME
  {"inverse_collision_matrix_libflame",
   (PyCFunction)py_inverse_collision_matrix_libflame,
   METH_VARARGS,
   "Pseudo-inverse using libflame hevd"},
#endif
  {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int _phono3py_traverse(PyObject *m, visitproc visit, void *arg) {
  Py_VISIT(GETSTATE(m)->error);
  return 0;
}

static int _phono3py_clear(PyObject *m) {
  Py_CLEAR(GETSTATE(m)->error);
  return 0;
}

static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
  "_phono3py",
  NULL,
  sizeof(struct module_state),
  _phono3py_methods,
  NULL,
  _phono3py_traverse,
  _phono3py_clear,
  NULL
};

#define INITERROR return NULL

PyObject *
PyInit__phono3py(void)

#else
#define INITERROR return

  void
  init_phono3py(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
  PyObject *module = PyModule_Create(&moduledef);
#else
  PyObject *module = Py_InitModule("_phono3py", _phono3py_methods);
#endif
  struct module_state *st;

  if (module == NULL)
    INITERROR;
  st = GETSTATE(module);

  st->error = PyErr_NewException("_phono3py.Error", NULL, NULL);
  if (st->error == NULL) {
    Py_DECREF(module);
    INITERROR;
  }

#if PY_MAJOR_VERSION >= 3
  return module;
#endif
}

static PyObject * py_get_interaction(PyObject *self, PyObject *args)
{
  PyArrayObject *fc3_normal_squared_py;
  PyArrayObject *g_zero_py;
  PyArrayObject *frequencies;
  PyArrayObject *eigenvectors;
  PyArrayObject *grid_point_triplets;
  PyArrayObject *grid_address_py;
  PyArrayObject *mesh_py;
  PyArrayObject *shortest_vectors;
  PyArrayObject *multiplicity;
  PyArrayObject *fc3_py;
  PyArrayObject *atomic_masses;
  PyArrayObject *p2s_map;
  PyArrayObject *s2p_map;
  PyArrayObject *band_indices_py;
  double cutoff_frequency;
  int symmetrize_fc3_q;

  Darray *fc3_normal_squared;
  Darray *freqs;
  Carray *eigvecs;
  Iarray *triplets;
  char* g_zero;
  int *grid_address;
  int *mesh;
  Darray *fc3;
  Darray *svecs;
  Iarray *multi;
  double *masses;
  int *p2s;
  int *s2p;
  int *band_indices;

  if (!PyArg_ParseTuple(args, "OOOOOOOOOOOOOOid",
                        &fc3_normal_squared_py,
                        &g_zero_py,
                        &frequencies,
                        &eigenvectors,
                        &grid_point_triplets,
                        &grid_address_py,
                        &mesh_py,
                        &fc3_py,
                        &shortest_vectors,
                        &multiplicity,
                        &atomic_masses,
                        &p2s_map,
                        &s2p_map,
                        &band_indices_py,
                        &symmetrize_fc3_q,
                        &cutoff_frequency)) {
    return NULL;
  }


  fc3_normal_squared = convert_to_darray(fc3_normal_squared_py);
  freqs = convert_to_darray(frequencies);
  /* npy_cdouble and lapack_complex_double may not be compatible. */
  /* So eigenvectors should not be used in Python side */
  eigvecs = convert_to_carray(eigenvectors);
  triplets = convert_to_iarray(grid_point_triplets);
  g_zero = (char*)PyArray_DATA(g_zero_py);
  grid_address = (int*)PyArray_DATA(grid_address_py);
  mesh = (int*)PyArray_DATA(mesh_py);
  fc3 = convert_to_darray(fc3_py);
  svecs = convert_to_darray(shortest_vectors);
  multi = convert_to_iarray(multiplicity);
  masses = (double*)PyArray_DATA(atomic_masses);
  p2s = (int*)PyArray_DATA(p2s_map);
  s2p = (int*)PyArray_DATA(s2p_map);
  band_indices = (int*)PyArray_DATA(band_indices_py);

  get_interaction(fc3_normal_squared,
                  g_zero,
                  freqs,
                  eigvecs,
                  triplets,
                  grid_address,
                  mesh,
                  fc3,
                  svecs,
                  multi,
                  masses,
                  p2s,
                  s2p,
                  band_indices,
                  symmetrize_fc3_q,
                  cutoff_frequency);

  free(fc3_normal_squared);
  free(freqs);
  free(eigvecs);
  free(triplets);
  free(fc3);
  free(svecs);
  free(multi);

  Py_RETURN_NONE;
}

static PyObject * py_get_pp_collision(PyObject *self, PyObject *args)
{
  PyArrayObject *gamma_py;
  PyArrayObject *relative_grid_address_py;
  PyArrayObject *frequencies_py;
  PyArrayObject *eigenvectors_py;
  PyArrayObject *triplets_py;
  PyArrayObject *triplet_weights_py;
  PyArrayObject *grid_address_py;
  PyArrayObject *bz_map_py;
  PyArrayObject *mesh_py;
  PyArrayObject *fc3_py;
  PyArrayObject *shortest_vectors_py;
  PyArrayObject *multiplicity_py;
  PyArrayObject *atomic_masses_py;
  PyArrayObject *p2s_map_py;
  PyArrayObject *s2p_map_py;
  PyArrayObject *band_indices_py;
  PyArrayObject *temperatures_py;
  double cutoff_frequency;
  int is_NU;
  int symmetrize_fc3_q;

  double *gamma;
  int (*relative_grid_address)[4][3];
  double *frequencies;
  lapack_complex_double *eigenvectors;
  Iarray *triplets;
  int *triplet_weights;
  int *grid_address;
  int *bz_map;
  int *mesh;
  double *fc3;
  Darray *svecs;
  int *multi;
  double *masses;
  int *p2s;
  int *s2p;
  Iarray *band_indices;
  Darray *temperatures;

  if (!PyArg_ParseTuple(args, "OOOOOOOOOOOOOOOOOiid",
                        &gamma_py,
                        &relative_grid_address_py,
                        &frequencies_py,
                        &eigenvectors_py,
                        &triplets_py,
                        &triplet_weights_py,
                        &grid_address_py,
                        &bz_map_py,
                        &mesh_py,
                        &fc3_py,
                        &shortest_vectors_py,
                        &multiplicity_py,
                        &atomic_masses_py,
                        &p2s_map_py,
                        &s2p_map_py,
                        &band_indices_py,
                        &temperatures_py,
                        &is_NU,
                        &symmetrize_fc3_q,
                        &cutoff_frequency)) {
    return NULL;
  }

  gamma = (double*)PyArray_DATA(gamma_py);
  relative_grid_address = (int(*)[4][3])PyArray_DATA(relative_grid_address_py);
  frequencies = (double*)PyArray_DATA(frequencies_py);
  eigenvectors = (lapack_complex_double*)PyArray_DATA(eigenvectors_py);
  triplets = convert_to_iarray(triplets_py);
  triplet_weights = (int*)PyArray_DATA(triplet_weights_py);
  grid_address = (int*)PyArray_DATA(grid_address_py);
  bz_map = (int*)PyArray_DATA(bz_map_py);
  mesh = (int*)PyArray_DATA(mesh_py);
  fc3 = (double*)PyArray_DATA(fc3_py);
  svecs = convert_to_darray(shortest_vectors_py);
  multi = (int*)PyArray_DATA(multiplicity_py);
  masses = (double*)PyArray_DATA(atomic_masses_py);
  p2s = (int*)PyArray_DATA(p2s_map_py);
  s2p = (int*)PyArray_DATA(s2p_map_py);
  band_indices = convert_to_iarray(band_indices_py);
  temperatures = convert_to_darray(temperatures_py);

  ppc_get_pp_collision(gamma,
                       relative_grid_address,
                       frequencies,
                       eigenvectors,
                       triplets,
                       triplet_weights,
                       grid_address,
                       bz_map,
                       mesh,
                       fc3,
                       svecs,
                       multi,
                       masses,
                       p2s,
                       s2p,
                       band_indices,
                       temperatures,
                       is_NU,
                       symmetrize_fc3_q,
                       cutoff_frequency);

  free(triplets);
  triplets = NULL;
  free(svecs);
  svecs = NULL;
  free(band_indices);
  band_indices = NULL;
  free(temperatures);
  temperatures = NULL;

  Py_RETURN_NONE;
}

static PyObject * py_get_pp_collision_with_sigma(PyObject *self, PyObject *args)
{
  PyArrayObject *gamma_py;
  PyArrayObject *frequencies_py;
  PyArrayObject *eigenvectors_py;
  PyArrayObject *triplets_py;
  PyArrayObject *triplet_weights_py;
  PyArrayObject *grid_address_py;
  PyArrayObject *mesh_py;
  PyArrayObject *fc3_py;
  PyArrayObject *shortest_vectors_py;
  PyArrayObject *multiplicity_py;
  PyArrayObject *atomic_masses_py;
  PyArrayObject *p2s_map_py;
  PyArrayObject *s2p_map_py;
  PyArrayObject *band_indices_py;
  PyArrayObject *temperatures_py;
  int is_NU;
  int symmetrize_fc3_q;
  double sigma;
  double sigma_cutoff;
  double cutoff_frequency;

  double *gamma;
  double *frequencies;
  lapack_complex_double *eigenvectors;
  Iarray *triplets;
  int *triplet_weights;
  int *grid_address;
  int *mesh;
  double *fc3;
  Darray *svecs;
  int *multi;
  double *masses;
  int *p2s;
  int *s2p;
  Iarray *band_indices;
  Darray *temperatures;

  if (!PyArg_ParseTuple(args, "OddOOOOOOOOOOOOOOiid",
                        &gamma_py,
                        &sigma,
                        &sigma_cutoff,
                        &frequencies_py,
                        &eigenvectors_py,
                        &triplets_py,
                        &triplet_weights_py,
                        &grid_address_py,
                        &mesh_py,
                        &fc3_py,
                        &shortest_vectors_py,
                        &multiplicity_py,
                        &atomic_masses_py,
                        &p2s_map_py,
                        &s2p_map_py,
                        &band_indices_py,
                        &temperatures_py,
                        &is_NU,
                        &symmetrize_fc3_q,
                        &cutoff_frequency)) {
    return NULL;
  }

  gamma = (double*)PyArray_DATA(gamma_py);
  frequencies = (double*)PyArray_DATA(frequencies_py);
  eigenvectors = (lapack_complex_double*)PyArray_DATA(eigenvectors_py);
  triplets = convert_to_iarray(triplets_py);
  triplet_weights = (int*)PyArray_DATA(triplet_weights_py);
  grid_address = (int*)PyArray_DATA(grid_address_py);
  mesh = (int*)PyArray_DATA(mesh_py);
  fc3 = (double*)PyArray_DATA(fc3_py);
  svecs = convert_to_darray(shortest_vectors_py);
  multi = (int*)PyArray_DATA(multiplicity_py);
  masses = (double*)PyArray_DATA(atomic_masses_py);
  p2s = (int*)PyArray_DATA(p2s_map_py);
  s2p = (int*)PyArray_DATA(s2p_map_py);
  band_indices = convert_to_iarray(band_indices_py);
  temperatures = convert_to_darray(temperatures_py);

  ppc_get_pp_collision_with_sigma(gamma,
                                  sigma,
                                  sigma_cutoff,
                                  frequencies,
                                  eigenvectors,
                                  triplets,
                                  triplet_weights,
                                  grid_address,
                                  mesh,
                                  fc3,
                                  svecs,
                                  multi,
                                  masses,
                                  p2s,
                                  s2p,
                                  band_indices,
                                  temperatures,
                                  is_NU,
                                  symmetrize_fc3_q,
                                  cutoff_frequency);

  free(triplets);
  triplets = NULL;
  free(svecs);
  svecs = NULL;
  free(band_indices);
  band_indices = NULL;
  free(temperatures);
  temperatures = NULL;

  Py_RETURN_NONE;
}

static PyObject * py_get_imag_self_energy_with_g(PyObject *self, PyObject *args)
{
  PyArrayObject *gamma_py;
  PyArrayObject *fc3_normal_squared_py;
  PyArrayObject *frequencies_py;
  PyArrayObject *grid_point_triplets_py;
  PyArrayObject *triplet_weights_py;
  PyArrayObject *g_py;
  PyArrayObject *g_zero_py;
  double cutoff_frequency, temperature;

  Darray *fc3_normal_squared;
  double *gamma;
  double *g;
  char* g_zero;
  double *frequencies;
  int *grid_point_triplets;
  int *triplet_weights;

  if (!PyArg_ParseTuple(args, "OOOOOdOOd",
                        &gamma_py,
                        &fc3_normal_squared_py,
                        &grid_point_triplets_py,
                        &triplet_weights_py,
                        &frequencies_py,
                        &temperature,
                        &g_py,
                        &g_zero_py,
                        &cutoff_frequency)) {
    return NULL;
  }

  fc3_normal_squared = convert_to_darray(fc3_normal_squared_py);
  gamma = (double*)PyArray_DATA(gamma_py);
  g = (double*)PyArray_DATA(g_py);
  g_zero = (char*)PyArray_DATA(g_zero_py);
  frequencies = (double*)PyArray_DATA(frequencies_py);
  grid_point_triplets = (int*)PyArray_DATA(grid_point_triplets_py);
  triplet_weights = (int*)PyArray_DATA(triplet_weights_py);

  ise_get_imag_self_energy_at_bands_with_g(gamma,
                                           fc3_normal_squared,
                                           frequencies,
                                           grid_point_triplets,
                                           triplet_weights,
                                           g,
                                           g_zero,
                                           temperature,
                                           cutoff_frequency);

  free(fc3_normal_squared);
  fc3_normal_squared = NULL;

  Py_RETURN_NONE;
}

static PyObject *
py_get_detailed_imag_self_energy_with_g(PyObject *self, PyObject *args)
{
  PyArrayObject *gamma_detail_py;
  PyArrayObject *gamma_N_py;
  PyArrayObject *gamma_U_py;
  PyArrayObject *fc3_normal_squared_py;
  PyArrayObject *frequencies_py;
  PyArrayObject *grid_point_triplets_py;
  PyArrayObject *triplet_weights_py;
  PyArrayObject *grid_address_py;
  PyArrayObject *g_py;
  PyArrayObject *g_zero_py;
  double cutoff_frequency, temperature;

  Darray *fc3_normal_squared;
  double *gamma_detail;
  double *gamma_N;
  double *gamma_U;
  double *g;
  char* g_zero;
  double *frequencies;
  int *grid_point_triplets;
  int *triplet_weights;
  int *grid_address;

  if (!PyArg_ParseTuple(args, "OOOOOOOOdOOd",
                        &gamma_detail_py,
                        &gamma_N_py,
                        &gamma_U_py,
                        &fc3_normal_squared_py,
                        &grid_point_triplets_py,
                        &triplet_weights_py,
                        &grid_address_py,
                        &frequencies_py,
                        &temperature,
                        &g_py,
                        &g_zero_py,
                        &cutoff_frequency)) {
    return NULL;
  }

  fc3_normal_squared = convert_to_darray(fc3_normal_squared_py);
  gamma_detail = (double*)PyArray_DATA(gamma_detail_py);
  gamma_N = (double*)PyArray_DATA(gamma_N_py);
  gamma_U = (double*)PyArray_DATA(gamma_U_py);
  g = (double*)PyArray_DATA(g_py);
  g_zero = (char*)PyArray_DATA(g_zero_py);
  frequencies = (double*)PyArray_DATA(frequencies_py);
  grid_point_triplets = (int*)PyArray_DATA(grid_point_triplets_py);
  triplet_weights = (int*)PyArray_DATA(triplet_weights_py);
  grid_address = (int*)PyArray_DATA(grid_address_py);

  ise_get_detailed_imag_self_energy_at_bands_with_g(gamma_detail,
                                                    gamma_N,
                                                    gamma_U,
                                                    fc3_normal_squared,
                                                    frequencies,
                                                    grid_point_triplets,
                                                    triplet_weights,
                                                    grid_address,
                                                    g,
                                                    g_zero,
                                                    temperature,
                                                    cutoff_frequency);

  free(fc3_normal_squared);

  Py_RETURN_NONE;
}

static PyObject * py_get_frequency_shift_at_bands(PyObject *self,
                                                  PyObject *args)
{
  PyArrayObject *shift_py;
  PyArrayObject *fc3_normal_squared_py;
  PyArrayObject *frequencies_py;
  PyArrayObject *grid_point_triplets_py;
  PyArrayObject *triplet_weights_py;
  PyArrayObject *band_indices_py;
  double epsilon, unit_conversion_factor, cutoff_frequency, temperature;

  Darray *fc3_normal_squared;
  double *shift;
  double *frequencies;
  int *band_indices;
  int *grid_point_triplets;
  int *triplet_weights;

  if (!PyArg_ParseTuple(args, "OOOOOOdddd",
                        &shift_py,
                        &fc3_normal_squared_py,
                        &grid_point_triplets_py,
                        &triplet_weights_py,
                        &frequencies_py,
                        &band_indices_py,
                        &temperature,
                        &epsilon,
                        &unit_conversion_factor,
                        &cutoff_frequency)) {
    return NULL;
  }


  fc3_normal_squared = convert_to_darray(fc3_normal_squared_py);
  shift = (double*)PyArray_DATA(shift_py);
  frequencies = (double*)PyArray_DATA(frequencies_py);
  band_indices = (int*)PyArray_DATA(band_indices_py);
  grid_point_triplets = (int*)PyArray_DATA(grid_point_triplets_py);
  triplet_weights = (int*)PyArray_DATA(triplet_weights_py);

  get_frequency_shift_at_bands(shift,
                               fc3_normal_squared,
                               band_indices,
                               frequencies,
                               grid_point_triplets,
                               triplet_weights,
                               epsilon,
                               temperature,
                               unit_conversion_factor,
                               cutoff_frequency);

  free(fc3_normal_squared);

  Py_RETURN_NONE;
}

static PyObject * py_get_collision_matrix(PyObject *self, PyObject *args)
{
  PyArrayObject *collision_matrix_py;
  PyArrayObject *fc3_normal_squared_py;
  PyArrayObject *frequencies_py;
  PyArrayObject *triplets_py;
  PyArrayObject *triplets_map_py;
  PyArrayObject *stabilized_gp_map_py;
  PyArrayObject *g_py;
  PyArrayObject *rotated_grid_points_py;
  PyArrayObject *rotations_cartesian_py;
  double temperature, unit_conversion_factor, cutoff_frequency;

  Darray *fc3_normal_squared;
  double *collision_matrix;
  double *g;
  double *frequencies;
  int *triplets;
  Iarray *triplets_map;
  int *stabilized_gp_map;
  Iarray *rotated_grid_points;
  double *rotations_cartesian;

  if (!PyArg_ParseTuple(args, "OOOOOOOOOddd",
                        &collision_matrix_py,
                        &fc3_normal_squared_py,
                        &frequencies_py,
                        &g_py,
                        &triplets_py,
                        &triplets_map_py,
                        &stabilized_gp_map_py,
                        &rotated_grid_points_py,
                        &rotations_cartesian_py,
                        &temperature,
                        &unit_conversion_factor,
                        &cutoff_frequency)) {
    return NULL;
  }

  fc3_normal_squared = convert_to_darray(fc3_normal_squared_py);
  collision_matrix = (double*)PyArray_DATA(collision_matrix_py);
  g = (double*)PyArray_DATA(g_py);
  frequencies = (double*)PyArray_DATA(frequencies_py);
  triplets = (int*)PyArray_DATA(triplets_py);
  triplets_map = convert_to_iarray(triplets_map_py);
  stabilized_gp_map = (int*)PyArray_DATA(stabilized_gp_map_py);
  rotated_grid_points = convert_to_iarray(rotated_grid_points_py);
  rotations_cartesian = (double*)PyArray_DATA(rotations_cartesian_py);

  col_get_collision_matrix(collision_matrix,
                           fc3_normal_squared,
                           frequencies,
                           triplets,
                           triplets_map,
                           stabilized_gp_map,
                           rotated_grid_points,
                           rotations_cartesian,
                           g,
                           temperature,
                           unit_conversion_factor,
                           cutoff_frequency);

  free(fc3_normal_squared);
  free(triplets_map);
  free(rotated_grid_points);

  Py_RETURN_NONE;
}

static PyObject * py_get_reducible_collision_matrix(PyObject *self, PyObject *args)
{
  PyArrayObject *collision_matrix_py;
  PyArrayObject *fc3_normal_squared_py;
  PyArrayObject *frequencies_py;
  PyArrayObject *triplets_py;
  PyArrayObject *triplets_map_py;
  PyArrayObject *stabilized_gp_map_py;
  PyArrayObject *g_py;
  double temperature, unit_conversion_factor, cutoff_frequency;

  Darray *fc3_normal_squared;
  double *collision_matrix;
  double *g;
  double *frequencies;
  int *triplets;
  Iarray *triplets_map;
  int *stabilized_gp_map;

  if (!PyArg_ParseTuple(args, "OOOOOOOddd",
                        &collision_matrix_py,
                        &fc3_normal_squared_py,
                        &frequencies_py,
                        &g_py,
                        &triplets_py,
                        &triplets_map_py,
                        &stabilized_gp_map_py,
                        &temperature,
                        &unit_conversion_factor,
                        &cutoff_frequency)) {
    return NULL;
  }

  fc3_normal_squared = convert_to_darray(fc3_normal_squared_py);
  collision_matrix = (double*)PyArray_DATA(collision_matrix_py);
  g = (double*)PyArray_DATA(g_py);
  frequencies = (double*)PyArray_DATA(frequencies_py);
  triplets = (int*)PyArray_DATA(triplets_py);
  triplets_map = convert_to_iarray(triplets_map_py);
  stabilized_gp_map = (int*)PyArray_DATA(stabilized_gp_map_py);

  col_get_reducible_collision_matrix(collision_matrix,
                                     fc3_normal_squared,
                                     frequencies,
                                     triplets,
                                     triplets_map,
                                     stabilized_gp_map,
                                     g,
                                     temperature,
                                     unit_conversion_factor,
                                     cutoff_frequency);

  free(fc3_normal_squared);
  free(triplets_map);

  Py_RETURN_NONE;
}

static PyObject * py_symmetrize_collision_matrix(PyObject *self, PyObject *args)
{
  PyArrayObject *collision_matrix_py;

  double *collision_matrix;
  int num_sigma;
  int num_temp;
  int num_grid_points;
  int num_band;
  int i, j, k, l, num_column, adrs_shift;
  double val;

  if (!PyArg_ParseTuple(args, "O",
                        &collision_matrix_py)) {
    return NULL;
  }

  collision_matrix = (double*)PyArray_DATA(collision_matrix_py);
  num_sigma = PyArray_DIMS(collision_matrix_py)[0];
  num_temp = PyArray_DIMS(collision_matrix_py)[1];
  num_grid_points = PyArray_DIMS(collision_matrix_py)[2];
  num_band = PyArray_DIMS(collision_matrix_py)[3];

  if (PyArray_NDIM(collision_matrix_py) == 8) {
    num_column = num_grid_points * num_band * 3;
  } else {
    num_column = num_grid_points * num_band;
  }

  for (i = 0; i < num_sigma; i++) {
    for (j = 0; j < num_temp; j++) {
      adrs_shift = (i * num_column * num_column * num_temp +
                    j * num_column * num_column);
      show_colmat_info(collision_matrix_py, i, j, adrs_shift);
#pragma omp parallel for private(l, val)
      for (k = 0; k < num_column; k++) {
        for (l = k + 1; l < num_column; l++) {
          val = (collision_matrix[adrs_shift + k * num_column + l] +
                 collision_matrix[adrs_shift + l * num_column + k]) / 2;
          collision_matrix[adrs_shift + k * num_column + l] = val;
          collision_matrix[adrs_shift + l * num_column + k] = val;
        }
      }
    }
  }

  Py_RETURN_NONE;
}

static PyObject * py_get_isotope_strength(PyObject *self, PyObject *args)
{
  PyArrayObject *gamma_py;
  PyArrayObject *frequencies_py;
  PyArrayObject *eigenvectors_py;
  PyArrayObject *band_indices_py;
  PyArrayObject *mass_variances_py;
  int grid_point;
  int num_grid_points;
  double cutoff_frequency;
  double sigma;

  double *gamma;
  double *frequencies;
  lapack_complex_double *eigenvectors;
  int *band_indices;
  double *mass_variances;
  int num_band;
  int num_band0;

  if (!PyArg_ParseTuple(args, "OiOOOOidd",
                        &gamma_py,
                        &grid_point,
                        &mass_variances_py,
                        &frequencies_py,
                        &eigenvectors_py,
                        &band_indices_py,
                        &num_grid_points,
                        &sigma,
                        &cutoff_frequency)) {
    return NULL;
  }


  gamma = (double*)PyArray_DATA(gamma_py);
  frequencies = (double*)PyArray_DATA(frequencies_py);
  eigenvectors = (lapack_complex_double*)PyArray_DATA(eigenvectors_py);
  band_indices = (int*)PyArray_DATA(band_indices_py);
  mass_variances = (double*)PyArray_DATA(mass_variances_py);
  num_band = PyArray_DIMS(frequencies_py)[1];
  num_band0 = PyArray_DIMS(band_indices_py)[0];

  /* int i, j, k; */
  /* double f, f0; */
  /* int *weights, *ir_grid_points; */
  /* double *integration_weights; */

  /* ir_grid_points = (int*)malloc(sizeof(int) * num_grid_points); */
  /* weights = (int*)malloc(sizeof(int) * num_grid_points); */
  /* integration_weights = (double*)malloc(sizeof(double) * */
  /*                                    num_grid_points * num_band0 * num_band); */

  /* for (i = 0; i < num_grid_points; i++) { */
  /*   ir_grid_points[i] = i; */
  /*   weights[i] = 1; */
  /*   for (j = 0; j < num_band0; j++) { */
  /*     f0 = frequencies[grid_point * num_band + band_indices[j]]; */
  /*     for (k = 0; k < num_band; k++) { */
  /*    f = frequencies[i * num_band + k]; */
  /*    integration_weights[i * num_band0 * num_band + */
  /*                        j * num_band + k] = gaussian(f - f0, sigma); */
  /*     } */
  /*   } */
  /* } */

  /* get_thm_isotope_scattering_strength(gamma, */
  /*                                  grid_point, */
  /*                                  ir_grid_points, */
  /*                                  weights, */
  /*                                  mass_variances, */
  /*                                  frequencies, */
  /*                                  eigenvectors, */
  /*                                  num_grid_points, */
  /*                                  band_indices, */
  /*                                  num_band, */
  /*                                  num_band0, */
  /*                                  integration_weights, */
  /*                                  cutoff_frequency); */

  /* free(ir_grid_points); */
  /* free(weights); */
  /* free(integration_weights); */

  get_isotope_scattering_strength(gamma,
                                  grid_point,
                                  mass_variances,
                                  frequencies,
                                  eigenvectors,
                                  num_grid_points,
                                  band_indices,
                                  num_band,
                                  num_band0,
                                  sigma,
                                  cutoff_frequency);

  Py_RETURN_NONE;
}

static PyObject * py_get_thm_isotope_strength(PyObject *self, PyObject *args)
{
  PyArrayObject *gamma_py;
  PyArrayObject *frequencies_py;
  PyArrayObject *eigenvectors_py;
  PyArrayObject *band_indices_py;
  PyArrayObject *mass_variances_py;
  PyArrayObject *ir_grid_points_py;
  PyArrayObject *weights_py;
  int grid_point;
  double cutoff_frequency;
  PyArrayObject *integration_weights_py;

  double *gamma;
  double *frequencies;
  int *ir_grid_points;
  int *weights;
  lapack_complex_double *eigenvectors;
  int *band_indices;
  double *mass_variances;
  int num_band;
  int num_band0;
  double *integration_weights;
  int num_ir_grid_points;

  if (!PyArg_ParseTuple(args, "OiOOOOOOOd",
                        &gamma_py,
                        &grid_point,
                        &ir_grid_points_py,
                        &weights_py,
                        &mass_variances_py,
                        &frequencies_py,
                        &eigenvectors_py,
                        &band_indices_py,
                        &integration_weights_py,
                        &cutoff_frequency)) {
    return NULL;
  }


  gamma = (double*)PyArray_DATA(gamma_py);
  frequencies = (double*)PyArray_DATA(frequencies_py);
  ir_grid_points = (int*)PyArray_DATA(ir_grid_points_py);
  weights = (int*)PyArray_DATA(weights_py);
  eigenvectors = (lapack_complex_double*)PyArray_DATA(eigenvectors_py);
  band_indices = (int*)PyArray_DATA(band_indices_py);
  mass_variances = (double*)PyArray_DATA(mass_variances_py);
  num_band = PyArray_DIMS(frequencies_py)[1];
  num_band0 = PyArray_DIMS(band_indices_py)[0];
  integration_weights = (double*)PyArray_DATA(integration_weights_py);
  num_ir_grid_points = PyArray_DIMS(ir_grid_points_py)[0];

  get_thm_isotope_scattering_strength(gamma,
                                      grid_point,
                                      ir_grid_points,
                                      weights,
                                      mass_variances,
                                      frequencies,
                                      eigenvectors,
                                      num_ir_grid_points,
                                      band_indices,
                                      num_band,
                                      num_band0,
                                      integration_weights,
                                      cutoff_frequency);

  Py_RETURN_NONE;
}

static PyObject * py_distribute_fc3(PyObject *self, PyObject *args)
{
  PyArrayObject *force_constants_third_copy;
  PyArrayObject *force_constants_third;
  int third_atom;
  PyArrayObject *rotation_cart_inv;
  PyArrayObject *atom_mapping_py;

  double *fc3_copy;
  double *fc3;
  double *rot_cart_inv;
  int *atom_mapping;
  int num_atom;

  if (!PyArg_ParseTuple(args, "OOiOO",
                        &force_constants_third_copy,
                        &force_constants_third,
                        &third_atom,
                        &atom_mapping_py,
                        &rotation_cart_inv)) {
    return NULL;
  }

  fc3_copy = (double*)PyArray_DATA(force_constants_third_copy);
  fc3 = (double*)PyArray_DATA(force_constants_third);
  rot_cart_inv = (double*)PyArray_DATA(rotation_cart_inv);
  atom_mapping = (int*)PyArray_DATA(atom_mapping_py);
  num_atom = PyArray_DIMS(atom_mapping_py)[0];

  distribute_fc3(fc3_copy,
                 fc3,
                 third_atom,
                 atom_mapping,
                 num_atom,
                 rot_cart_inv);

  Py_RETURN_NONE;
}

static PyObject * py_set_permutation_symmetry_fc3(PyObject *self, PyObject *args)
{
  PyArrayObject *fc3_py;

  double *fc3;
  int num_atom;

  if (!PyArg_ParseTuple(args, "O",
                        &fc3_py)) {
    return NULL;
  }

  fc3 = (double*)PyArray_DATA(fc3_py);
  num_atom = PyArray_DIMS(fc3_py)[0];

  set_permutation_symmetry_fc3(fc3, num_atom);

  Py_RETURN_NONE;
}

static PyObject * py_get_neighboring_gird_points(PyObject *self, PyObject *args)
{
  PyArrayObject *relative_grid_points_py;
  PyArrayObject *grid_points_py;
  PyArrayObject *relative_grid_address_py;
  PyArrayObject *mesh_py;
  PyArrayObject *bz_grid_address_py;
  PyArrayObject *bz_map_py;

  int *relative_grid_points;
  int *grid_points;
  int num_grid_points;
  int (*relative_grid_address)[3];
  int num_relative_grid_address;
  int *mesh;
  int (*bz_grid_address)[3];
  int *bz_map;
  int i;

  if (!PyArg_ParseTuple(args, "OOOOOO",
                        &relative_grid_points_py,
                        &grid_points_py,
                        &relative_grid_address_py,
                        &mesh_py,
                        &bz_grid_address_py,
                        &bz_map_py)) {
    return NULL;
  }

  relative_grid_points = (int*)PyArray_DATA(relative_grid_points_py);
  grid_points = (int*)PyArray_DATA(grid_points_py);
  num_grid_points = PyArray_DIMS(grid_points_py)[0];
  relative_grid_address = (int(*)[3])PyArray_DATA(relative_grid_address_py);
  num_relative_grid_address = PyArray_DIMS(relative_grid_address_py)[0];
  mesh = (int*)PyArray_DATA(mesh_py);
  bz_grid_address = (int(*)[3])PyArray_DATA(bz_grid_address_py);
  bz_map = (int*)PyArray_DATA(bz_map_py);

#pragma omp parallel for
  for (i = 0; i < num_grid_points; i++) {
    thm_get_neighboring_grid_points
      (relative_grid_points + i * num_relative_grid_address,
       grid_points[i],
       relative_grid_address,
       num_relative_grid_address,
       mesh,
       bz_grid_address,
       bz_map);
  }

  Py_RETURN_NONE;
}

static PyObject * py_set_integration_weights(PyObject *self, PyObject *args)
{
  PyArrayObject *iw_py;
  PyArrayObject *frequency_points_py;
  PyArrayObject *relative_grid_address_py;
  PyArrayObject *mesh_py;
  PyArrayObject *grid_points_py;
  PyArrayObject *frequencies_py;
  PyArrayObject *bz_grid_address_py;
  PyArrayObject *bz_map_py;

  double *iw;
  double *frequency_points;
  int num_band0;
  int (*relative_grid_address)[4][3];
  int *mesh;
  int *grid_points;
  int num_gp;
  int (*bz_grid_address)[3];
  int *bz_map;
  double *frequencies;
  int num_band;
  int i, j, k, bi;
  int vertices[24][4];
  double freq_vertices[24][4];

  if (!PyArg_ParseTuple(args, "OOOOOOOO",
                        &iw_py,
                        &frequency_points_py,
                        &relative_grid_address_py,
                        &mesh_py,
                        &grid_points_py,
                        &frequencies_py,
                        &bz_grid_address_py,
                        &bz_map_py)) {
    return NULL;
  }

  iw = (double*)PyArray_DATA(iw_py);
  frequency_points = (double*)PyArray_DATA(frequency_points_py);
  num_band0 = PyArray_DIMS(frequency_points_py)[0];
  relative_grid_address = (int(*)[4][3])PyArray_DATA(relative_grid_address_py);
  mesh = (int*)PyArray_DATA(mesh_py);
  grid_points = (int*)PyArray_DATA(grid_points_py);
  num_gp = PyArray_DIMS(grid_points_py)[0];
  bz_grid_address = (int(*)[3])PyArray_DATA(bz_grid_address_py);
  bz_map = (int*)PyArray_DATA(bz_map_py);
  frequencies = (double*)PyArray_DATA(frequencies_py);
  num_band = PyArray_DIMS(frequencies_py)[1];

#pragma omp parallel for private(j, k, bi, vertices, freq_vertices)
  for (i = 0; i < num_gp; i++) {
    for (j = 0; j < 24; j++) {
      thm_get_neighboring_grid_points(vertices[j],
                                      grid_points[i],
                                      relative_grid_address[j],
                                      4,
                                      mesh,
                                      bz_grid_address,
                                      bz_map);
    }
    for (bi = 0; bi < num_band; bi++) {
      for (j = 0; j < 24; j++) {
        for (k = 0; k < 4; k++) {
          freq_vertices[j][k] = frequencies[vertices[j][k] * num_band + bi];
        }
      }
      for (j = 0; j < num_band0; j++) {
        iw[i * num_band0 * num_band + j * num_band + bi] =
          thm_get_integration_weight(frequency_points[j], freq_vertices, 'I');
      }
    }
  }

  Py_RETURN_NONE;
}

static PyObject *
py_tpl_get_triplets_reciprocal_mesh_at_q(PyObject *self, PyObject *args)
{
  PyArrayObject *map_triplets;
  PyArrayObject *grid_address_py;
  PyArrayObject *map_q;
  int fixed_grid_number;
  PyArrayObject *mesh;
  int is_time_reversal;
  PyArrayObject *rotations;

  int (*grid_address)[3];
  int *map_triplets_int;
  int *map_q_int;
  int *mesh_int;
  int (*rot)[3][3];
  int num_rot;
  int num_ir;

  if (!PyArg_ParseTuple(args, "OOOiOiO",
                        &map_triplets,
                        &map_q,
                        &grid_address_py,
                        &fixed_grid_number,
                        &mesh,
                        &is_time_reversal,
                        &rotations)) {
    return NULL;
  }

  grid_address = (int(*)[3])PyArray_DATA(grid_address_py);
  map_triplets_int = (int*)PyArray_DATA(map_triplets);
  map_q_int = (int*)PyArray_DATA(map_q);
  mesh_int = (int*)PyArray_DATA(mesh);
  rot = (int(*)[3][3])PyArray_DATA(rotations);
  num_rot = PyArray_DIMS(rotations)[0];
  num_ir = tpl_get_triplets_reciprocal_mesh_at_q(map_triplets_int,
                                                 map_q_int,
                                                 grid_address,
                                                 fixed_grid_number,
                                                 mesh_int,
                                                 is_time_reversal,
                                                 num_rot,
                                                 rot);

  return PyLong_FromLong((long) num_ir);
}


static PyObject * py_tpl_get_BZ_triplets_at_q(PyObject *self, PyObject *args)
{
  PyArrayObject *triplets_py;
  PyArrayObject *bz_grid_address_py;
  PyArrayObject *bz_map_py;
  PyArrayObject *map_triplets_py;
  PyArrayObject *mesh_py;
  int grid_point;

  int (*triplets)[3];
  int (*bz_grid_address)[3];
  int *bz_map;
  int *map_triplets;
  int num_map_triplets;
  int *mesh;
  int num_ir;

  if (!PyArg_ParseTuple(args, "OiOOOO",
                        &triplets_py,
                        &grid_point,
                        &bz_grid_address_py,
                        &bz_map_py,
                        &map_triplets_py,
                        &mesh_py)) {
    return NULL;
  }

  triplets = (int(*)[3])PyArray_DATA(triplets_py);
  bz_grid_address = (int(*)[3])PyArray_DATA(bz_grid_address_py);
  bz_map = (int*)PyArray_DATA(bz_map_py);
  map_triplets = (int*)PyArray_DATA(map_triplets_py);
  num_map_triplets = PyArray_DIMS(map_triplets_py)[0];
  mesh = (int*)PyArray_DATA(mesh_py);

  num_ir = tpl_get_BZ_triplets_at_q(triplets,
                                    grid_point,
                                    bz_grid_address,
                                    bz_map,
                                    map_triplets,
                                    num_map_triplets,
                                    mesh);

  return PyLong_FromLong((long) num_ir);
}

static PyObject *
py_set_triplets_integration_weights(PyObject *self, PyObject *args)
{
  PyArrayObject *iw_py;
  PyArrayObject *iw_zero_py;
  PyArrayObject *frequency_points_py;
  PyArrayObject *relative_grid_address_py;
  PyArrayObject *mesh_py;
  PyArrayObject *triplets_py;
  PyArrayObject *frequencies_py;
  PyArrayObject *bz_grid_address_py;
  PyArrayObject *bz_map_py;

  double *iw;
  char *iw_zero;
  double *frequency_points;
  int num_band0;
  int (*relative_grid_address)[4][3];
  int *mesh;
  int (*triplets)[3];
  int num_triplets;
  int (*bz_grid_address)[3];
  int *bz_map;
  double *frequencies;
  int num_band;
  int num_iw;

  if (!PyArg_ParseTuple(args, "OOOOOOOOO",
                        &iw_py,
                        &iw_zero_py,
                        &frequency_points_py,
                        &relative_grid_address_py,
                        &mesh_py,
                        &triplets_py,
                        &frequencies_py,
                        &bz_grid_address_py,
                        &bz_map_py)) {
    return NULL;
  }

  iw = (double*)PyArray_DATA(iw_py);
  iw_zero = (char*)PyArray_DATA(iw_zero_py);
  frequency_points = (double*)PyArray_DATA(frequency_points_py);
  num_band0 = PyArray_DIMS(frequency_points_py)[0];
  relative_grid_address = (int(*)[4][3])PyArray_DATA(relative_grid_address_py);
  mesh = (int*)PyArray_DATA(mesh_py);
  triplets = (int(*)[3])PyArray_DATA(triplets_py);
  num_triplets = PyArray_DIMS(triplets_py)[0];
  bz_grid_address = (int(*)[3])PyArray_DATA(bz_grid_address_py);
  bz_map = (int*)PyArray_DATA(bz_map_py);
  frequencies = (double*)PyArray_DATA(frequencies_py);
  num_band = PyArray_DIMS(frequencies_py)[1];
  num_iw = PyArray_DIMS(iw_py)[0];

  tpl_get_integration_weight(iw,
                             iw_zero,
                             frequency_points,
                             num_band0,
                             relative_grid_address,
                             mesh,
                             triplets,
                             num_triplets,
                             bz_grid_address,
                             bz_map,
                             frequencies,
                             num_band,
                             num_iw,
                             1,
                             0);

  Py_RETURN_NONE;
}

static PyObject *
py_set_triplets_integration_weights_with_sigma(PyObject *self, PyObject *args)
{
  PyArrayObject *iw_py;
  PyArrayObject *iw_zero_py;
  PyArrayObject *frequency_points_py;
  PyArrayObject *triplets_py;
  PyArrayObject *frequencies_py;
  double sigma, sigma_cutoff;

  double *iw;
  char *iw_zero;
  double *frequency_points;
  int num_band0;
  int (*triplets)[3];
  int num_triplets;
  double *frequencies;
  int num_band;
  int num_iw;

  if (!PyArg_ParseTuple(args, "OOOOOdd",
                        &iw_py,
                        &iw_zero_py,
                        &frequency_points_py,
                        &triplets_py,
                        &frequencies_py,
                        &sigma,
                        &sigma_cutoff)) {
    return NULL;
  }

  iw = (double*)PyArray_DATA(iw_py);
  iw_zero = (char*)PyArray_DATA(iw_zero_py);
  frequency_points = (double*)PyArray_DATA(frequency_points_py);
  num_band0 = PyArray_DIMS(frequency_points_py)[0];
  triplets = (int(*)[3])PyArray_DATA(triplets_py);
  num_triplets = PyArray_DIMS(triplets_py)[0];
  frequencies = (double*)PyArray_DATA(frequencies_py);
  num_band = PyArray_DIMS(frequencies_py)[1];
  num_iw = PyArray_DIMS(iw_py)[0];

  tpl_get_integration_weight_with_sigma(iw,
                                        iw_zero,
                                        sigma,
                                        sigma_cutoff,
                                        frequency_points,
                                        num_band0,
                                        triplets,
                                        num_triplets,
                                        frequencies,
                                        num_band,
                                        num_iw);

  Py_RETURN_NONE;
}

#ifdef LIBFLAME
static PyObject * py_inverse_collision_matrix_libflame(PyObject *self, PyObject *args)
{
  PyArrayObject *collision_matrix_py;
  PyArrayObject *eigenvalues_py;
  int i_sigma, i_temp;
  double cutoff;
  double *collision_matrix;
  double *eigvals;
  int num_temp;
  int num_ir_grid_points;
  int num_band;
  int num_column, adrs_shift;

  if (!PyArg_ParseTuple(args, "OOiid",
                        &collision_matrix_py,
                        &eigenvalues_py,
                        &i_sigma,
                        &i_temp,
                        &cutoff)) {
    return NULL;
  }


  collision_matrix = (double*)PyArray_DATA(collision_matrix_py);
  eigvals = (double*)PyArray_DATA(eigenvalues_py);
  num_temp = PyArray_DIMS(collision_matrix_py)[1];
  num_ir_grid_points = PyArray_DIMS(collision_matrix_py)[2];
  num_band = PyArray_DIMS(collision_matrix_py)[3];

  num_column = num_ir_grid_points * num_band * 3;

  adrs_shift = (i_sigma * num_column * num_column * num_temp +
                i_temp * num_column * num_column);

  phonopy_pinv_libflame(collision_matrix + adrs_shift,
                        eigvals, num_column, cutoff);

  Py_RETURN_NONE;
}
#endif

static PyObject *
py_diagonalize_collision_matrix(PyObject *self, PyObject *args)
{
  PyArrayObject *collision_matrix_py;
  PyArrayObject *eigenvalues_py;
  double cutoff;
  int i_sigma, i_temp, is_pinv, solver;

  double *collision_matrix;
  double *eigvals;
  int num_temp;
  int num_grid_point;
  int num_band;
  int num_column, adrs_shift, info;

  if (!PyArg_ParseTuple(args, "OOiidii",
                        &collision_matrix_py,
                        &eigenvalues_py,
                        &i_sigma,
                        &i_temp,
                        &cutoff,
                        &solver,
                        &is_pinv)) {
    return NULL;
  }

  collision_matrix = (double*)PyArray_DATA(collision_matrix_py);
  eigvals = (double*)PyArray_DATA(eigenvalues_py);
  num_temp = PyArray_DIM(collision_matrix_py, 1);
  num_grid_point = PyArray_DIM(collision_matrix_py, 2);
  num_band = PyArray_DIM(collision_matrix_py, 3);

  if (PyArray_NDIM(collision_matrix_py) == 8) {
    num_column = num_grid_point * num_band * 3;
  } else {
    num_column = num_grid_point * num_band;
  }
  adrs_shift = (i_sigma * num_column * num_column * num_temp +
                i_temp * num_column * num_column);

  show_colmat_info(collision_matrix_py, i_sigma, i_temp, adrs_shift);
  info = phonopy_dsyev(collision_matrix + adrs_shift,
                       eigvals, num_column, solver);
  if (is_pinv) {
    pinv_from_eigensolution(collision_matrix + adrs_shift,
                            eigvals, num_column, cutoff, 0);
  }

  return PyLong_FromLong((long) info);
}

static PyObject * py_pinv_from_eigensolution(PyObject *self, PyObject *args)
{
  PyArrayObject *collision_matrix_py;
  PyArrayObject *eigenvalues_py;
  double cutoff;
  int i_sigma, i_temp, pinv_method;

  double *collision_matrix;
  double *eigvals;
  int num_temp;
  int num_grid_point;
  int num_band;
  int num_column, adrs_shift;

  if (!PyArg_ParseTuple(args, "OOiidi",
                        &collision_matrix_py,
                        &eigenvalues_py,
                        &i_sigma,
                        &i_temp,
                        &cutoff,
                        &pinv_method)) {
    return NULL;
  }

  collision_matrix = (double*)PyArray_DATA(collision_matrix_py);
  eigvals = (double*)PyArray_DATA(eigenvalues_py);
  num_temp = PyArray_DIMS(collision_matrix_py)[1];
  num_grid_point = PyArray_DIMS(collision_matrix_py)[2];
  num_band = PyArray_DIMS(collision_matrix_py)[3];

  if (PyArray_NDIM(collision_matrix_py) == 8) {
    num_column = num_grid_point * num_band * 3;
  } else {
    num_column = num_grid_point * num_band;
  }
  adrs_shift = (i_sigma * num_column * num_column * num_temp +
                i_temp * num_column * num_column);

  show_colmat_info(collision_matrix_py, i_sigma, i_temp, adrs_shift);

  pinv_from_eigensolution(collision_matrix + adrs_shift,
                          eigvals, num_column, cutoff, pinv_method);

  Py_RETURN_NONE;
}

static void pinv_from_eigensolution(double *data,
                                    const double *eigvals,
                                    const int size,
                                    const double cutoff,
                                    const int pinv_method)
{
  int i, ib, j, k, max_l, i_s, j_s;
  double *tmp_data;
  double e, sum;
  int *l;

  l = NULL;
  tmp_data = NULL;

  tmp_data = (double*)malloc(sizeof(double) * size * size);

#pragma omp parallel for
  for (i = 0; i < size * size; i++) {
    tmp_data[i] = data[i];
  }

  l = (int*)malloc(sizeof(int) * size);
  max_l = 0;
  for (i = 0; i < size; i++) {
    if (pinv_method == 0) {
      e = fabs(eigvals[i]);
    } else {
      e = eigvals[i];
    }
    if (e > cutoff) {
      l[max_l] = i;
      max_l++;
    }
  }

#pragma omp parallel for private(ib, j, k, i_s, j_s, sum)
  for (i = 0; i < size / 2; i++) {
    /* from front */
    i_s = i * size;
    for (j = i; j < size; j++) {
      j_s = j * size;
      sum = 0;
      for (k = 0; k < max_l; k++) {
        sum += tmp_data[i_s + l[k]] * tmp_data[j_s + l[k]] / eigvals[l[k]];
      }
      data[i_s + j] = sum;
      data[j_s + i] = sum;
    }
    /* from back */
    ib = size - i - 1;
    i_s = ib * size;
    for (j = ib; j < size; j++) {
      j_s = j * size;
      sum = 0;
      for (k = 0; k < max_l; k++) {
        sum += tmp_data[i_s + l[k]] * tmp_data[j_s + l[k]] / eigvals[l[k]];
      }
      data[i_s + j] = sum;
      data[j_s + ib] = sum;
    }
  }

  /* when size is odd */
  if ((size % 2) == 1) {
    i = (size - 1) / 2;
    i_s = i * size;
    for (j = i; j < size; j++) {
      j_s = j * size;
      sum = 0;
      for (k = 0; k < max_l; k++) {
        sum += tmp_data[i_s + l[k]] * tmp_data[j_s + l[k]] / eigvals[l[k]];
      }
      data[i_s + j] = sum;
      data[j_s + i] = sum;
    }
  }

  free(l);
  l = NULL;

  free(tmp_data);
  tmp_data = NULL;
}

static void show_colmat_info(const PyArrayObject *collision_matrix_py,
                             const int i_sigma,
                             const int i_temp,
                             const int adrs_shift)
{
  int i;

  printf(" Array_shape:(");
  for (i = 0; i < PyArray_NDIM(collision_matrix_py); i++) {
    printf("%d", (int)PyArray_DIM(collision_matrix_py, i));
    if (i < PyArray_NDIM(collision_matrix_py) - 1) {
      printf(",");
    } else {
      printf("), ");
    }
  }
  printf("Data shift:%d [%d, %d]\n", adrs_shift, i_sigma, i_temp);
}
