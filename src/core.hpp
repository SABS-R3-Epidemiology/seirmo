#ifndef _CORE_HPP
#define _CORE_HPP

#include <vector>
#include <boost/python/numpy.hpp>
#include <iostream>

namespace seir
{

namespace py = boost::python;
namespace np = boost::python::numpy;

class SEIRModel
{
public:
    SEIRModel():
        m_nParameters(0), m_nOutputs(0) {}

    const int nParameters() const { return m_nParameters; };
    const int nOutputs() const { return m_nOutputs; };

    virtual np::ndarray simulate(
        np::ndarray parameters,
        np::ndarray times) {
            return np::zeros(py::make_tuple(1), np::dtype::get_builtin<int>());
        }

protected:
    int m_nParameters;
    int m_nOutputs;
};

class SEIRModelFactory
{
public:
    SEIRModel* gillespieSEIR();
};

} // namespace seir

#endif // _CORE_HPP