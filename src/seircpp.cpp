#include "core.hpp"
#include <boost/python.hpp>
#include <boost/python/numpy.hpp>

BOOST_PYTHON_MODULE(seircpp)
{
    using namespace boost::python;

    Py_Initialize();
    boost::python::numpy::initialize();

    class_<seir::SEIRModelFactory>("SEIRModelFactory", init<>())
        .def("gillespieSEIR", &seir::SEIRModelFactory::gillespieSEIR,
            return_value_policy<manage_new_object>(), "");

    class_<seir::SEIRModel>("SEIRModel", init<>())
        .def("n_parameters", &seir::SEIRModel::nParameters, "")
        .def("n_outputs", &seir::SEIRModel::nOutputs, "")
        .def("simulate", &seir::SEIRModel::simulate, "");
}

/*

Build this using:
g++ -o seircpp.so seircpp.cpp core.cpp gillespieSEIR.cpp -std=c++11 -fPIC -shared -w -Wall -Wextra `python3.8-config --includes --libs` -lboost_python38 -lboost_numpy38


*/
