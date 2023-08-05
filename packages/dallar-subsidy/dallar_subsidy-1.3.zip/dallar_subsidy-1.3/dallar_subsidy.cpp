#include <Python.h>

#ifdef _MSC_VER
    typedef __int64 int64_t;
#else
    #include <stdint.h>
#endif

static const int64_t COIN = 100000000;
static const int64_t minimumSubsidy = 8 * COIN;
static const int64_t nPremine = 200000 * COIN;

int64_t static GetBlockBaseValue(int nHeight)
{
    if (nHeight == 0)
	{
		return 1 * COIN;
	}

	if (nHeight == 1)
	{
		return nPremine;
	}

	int64_t nSubsidy = 256 * COIN;

	// Subsidy is reduced by 6% every 10080 blocks, which will occur approximately every 1 week
	int exponent = (nHeight / 10080);
	for (int i = 0; i < exponent; i++)
	{
		nSubsidy = nSubsidy * 47;
		nSubsidy = nSubsidy / 50;
	}
	if (nSubsidy < minimumSubsidy)
	{
		nSubsidy = minimumSubsidy;
	}
	return nSubsidy;
}

static PyObject *dallar_subsidy_getblockbasevalue(PyObject *self, PyObject *args)
{
    int input_height;
    if (!PyArg_ParseTuple(args, "i", &input_height))
        return NULL;
    long long output = GetBlockBaseValue(input_height);
    return Py_BuildValue("L", output);
}

static PyMethodDef dallar_subsidy_methods[] = {
    { "getBlockBaseValue", dallar_subsidy_getblockbasevalue, METH_VARARGS, "Returns the block value" },
    { NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC initdallar_subsidy(void) {
    (void) Py_InitModule("dallar_subsidy", dallar_subsidy_methods);
}
