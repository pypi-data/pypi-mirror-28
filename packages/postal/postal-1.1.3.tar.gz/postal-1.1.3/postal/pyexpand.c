#include <Python.h>
#include <libpostal/libpostal.h>
#include "pyutils.h"

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#endif

struct module_state {
    PyObject *error;
};


#ifdef IS_PY3K
    #define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
    #define GETSTATE(m) (&_state)
    static struct module_state _state;
#endif


static PyObject *py_expand(PyObject *self, PyObject *args, PyObject *keywords) {
    PyObject *arg_input;
    PyObject *arg_languages = Py_None;
    libpostal_normalize_options_t options = libpostal_get_default_options();

    PyObject *result = NULL;

    static char *kwlist[] = {"address",
                             "languages",
                             "address_components",
                             "latin_ascii",
                             "transliterate",
                             "strip_accents",
                             "decompose",
                             "lowercase",
                             "trim_string",
                             "replace_word_hyphens",
                             "delete_word_hyphens",
                             "replace_numeric_hyphens",
                             "delete_numeric_hyphens",
                             "split_alpha_from_numeric",
                             "delete_final_periods",
                             "delete_acronym_periods",
                             "drop_english_possessives",
                             "delete_apostrophes",
                             "expand_numex",
                             "roman_numerals",
                             NULL
                            };

    uint32_t address_components = options.address_components;
    uint32_t latin_ascii = options.latin_ascii;
    uint32_t transliterate = options.transliterate;
    uint32_t strip_accents = options.strip_accents;
    uint32_t decompose = options.decompose;
    uint32_t lowercase = options.lowercase;
    uint32_t trim_string = options.trim_string;
    uint32_t replace_word_hyphens = options.replace_word_hyphens;
    uint32_t delete_word_hyphens = options.delete_word_hyphens;
    uint32_t replace_numeric_hyphens = options.replace_numeric_hyphens;
    uint32_t delete_numeric_hyphens = options.delete_numeric_hyphens;
    uint32_t split_alpha_from_numeric = options.split_alpha_from_numeric;
    uint32_t delete_final_periods = options.delete_final_periods;
    uint32_t delete_acronym_periods = options.delete_acronym_periods;
    uint32_t drop_english_possessives = options.drop_english_possessives;
    uint32_t delete_apostrophes = options.delete_apostrophes;
    uint32_t expand_numex = options.expand_numex;
    uint32_t roman_numerals = options.roman_numerals;

    if (!PyArg_ParseTupleAndKeywords(args, keywords, 
                                     "O|OHIIIIIIIIIIIIIIIII:pyexpand", kwlist,
                                     &arg_input, &arg_languages,
                                     &address_components,
                                     &latin_ascii,
                                     &transliterate,
                                     &strip_accents,
                                     &decompose,
                                     &lowercase,
                                     &trim_string,
                                     &replace_word_hyphens,
                                     &delete_word_hyphens,
                                     &replace_numeric_hyphens,
                                     &delete_numeric_hyphens,
                                     &split_alpha_from_numeric,
                                     &delete_final_periods,
                                     &delete_acronym_periods,
                                     &drop_english_possessives,
                                     &delete_apostrophes,
                                     &expand_numex,
                                     &roman_numerals
                                     )) {
        return 0;
    }


    options.address_components = address_components;
    options.latin_ascii = latin_ascii;
    options.transliterate = transliterate;
    options.strip_accents = strip_accents;
    options.decompose = decompose;
    options.lowercase = lowercase;
    options.trim_string = trim_string;
    options.replace_word_hyphens = replace_word_hyphens;
    options.delete_word_hyphens = delete_word_hyphens;
    options.replace_numeric_hyphens = replace_numeric_hyphens;
    options.delete_numeric_hyphens = delete_numeric_hyphens;
    options.split_alpha_from_numeric = split_alpha_from_numeric;
    options.delete_final_periods = delete_final_periods;
    options.delete_acronym_periods = delete_acronym_periods;
    options.drop_english_possessives = drop_english_possessives;
    options.delete_apostrophes = delete_apostrophes;
    options.expand_numex = expand_numex;
    options.roman_numerals = roman_numerals;


    char *input = PyObject_to_string(arg_input);

    if (input == NULL) {
        return NULL;
    }

    size_t num_languages = 0;
    char **languages = NULL;

    if (PySequence_Check(arg_languages)) {
        languages = PyObject_to_strings_max_len(arg_languages, LIBPOSTAL_MAX_LANGUAGE_LEN, &num_languages);
    }

    if (num_languages > 0 && languages != NULL) {
        options.num_languages = num_languages;
        options.languages = languages;
    }

    size_t num_expansions = 0;
    char **expansions = libpostal_expand_address(input, options, &num_expansions);

    if (languages != NULL) {
        for (int i = 0; i < num_languages; i++) {
            free(languages[i]);
        }
        free(languages);
    }

    if (expansions != NULL) {
        result = PyObject_from_strings(expansions, num_expansions);
        libpostal_expansion_array_destroy(expansions, num_expansions);
    }

    return result;
}

static PyMethodDef expand_methods[] = {
    {"expand_address", (PyCFunction)py_expand, METH_VARARGS | METH_KEYWORDS, "expand_address(text, **kw)"},
    {NULL, NULL},
};



#ifdef IS_PY3K

static int expand_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int expand_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    libpostal_teardown_language_classifier();
    libpostal_teardown();
    return 0;
}

static struct PyModuleDef module_def = {
        PyModuleDef_HEAD_INIT,
        "_expand",
        NULL,
        sizeof(struct module_state),
        expand_methods,
        NULL,
        expand_traverse,
        expand_clear,
        NULL
};

#define INITERROR return NULL

PyObject *
PyInit__expand(void) {

#else

#define INITERROR return

void cleanup_libpostal(void) {
    libpostal_teardown();
    libpostal_teardown_language_classifier();
}

void
init_expand(void) {

#endif

#ifdef IS_PY3K
    PyObject *module = PyModule_Create(&module_def);
#else
    PyObject *module = Py_InitModule("_expand", expand_methods);
#endif

    if (module == NULL) {
        INITERROR;
    }
    struct module_state *st = GETSTATE(module);

    st->error = PyErr_NewException("_expand.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

    if (!libpostal_setup() || !libpostal_setup_language_classifier()) {
        PyErr_SetString(PyExc_TypeError,
                        "Error loading libpostal");
    }

    PyModule_AddIntConstant(module, "ADDRESS_NONE", LIBPOSTAL_ADDRESS_NONE);
    PyModule_AddIntConstant(module, "ADDRESS_ANY", LIBPOSTAL_ADDRESS_ANY);
    PyModule_AddIntConstant(module, "ADDRESS_NAME", LIBPOSTAL_ADDRESS_NAME);
    PyModule_AddIntConstant(module, "ADDRESS_HOUSE_NUMBER", LIBPOSTAL_ADDRESS_HOUSE_NUMBER);
    PyModule_AddIntConstant(module, "ADDRESS_STREET", LIBPOSTAL_ADDRESS_STREET);
    PyModule_AddIntConstant(module, "ADDRESS_UNIT", LIBPOSTAL_ADDRESS_UNIT);
    PyModule_AddIntConstant(module, "ADDRESS_LEVEL", LIBPOSTAL_ADDRESS_LEVEL);
    PyModule_AddIntConstant(module, "ADDRESS_STAIRCASE", LIBPOSTAL_ADDRESS_STAIRCASE);
    PyModule_AddIntConstant(module, "ADDRESS_ENTRANCE", LIBPOSTAL_ADDRESS_ENTRANCE);

    PyModule_AddIntConstant(module, "ADDRESS_CATEGORY", LIBPOSTAL_ADDRESS_CATEGORY);
    PyModule_AddIntConstant(module, "ADDRESS_NEAR", LIBPOSTAL_ADDRESS_NEAR);

    PyModule_AddIntConstant(module, "ADDRESS_TOPONYM", LIBPOSTAL_ADDRESS_TOPONYM);
    PyModule_AddIntConstant(module, "ADDRESS_POSTAL_CODE", LIBPOSTAL_ADDRESS_POSTAL_CODE);
    PyModule_AddIntConstant(module, "ADDRESS_PO_BOX", LIBPOSTAL_ADDRESS_PO_BOX);
    PyModule_AddIntConstant(module, "ADDRESS_ALL", LIBPOSTAL_ADDRESS_ALL);

#ifndef IS_PY3K
    Py_AtExit(&cleanup_libpostal);
#endif

#ifdef IS_PY3K
    return module;
#endif
}

