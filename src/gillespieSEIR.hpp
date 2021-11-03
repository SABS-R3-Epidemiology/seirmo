#ifndef _GILLESPIE_SEIR_HPP
#define _GILLESPIE_SEIR_HPP

#include "core.hpp"
#include <vector>
#include <string>
#include <functional>

namespace seir
{

class GillespieSEIR: public SEIRModel
{
typedef int dtypeint;

public:
    GillespieSEIR();

    boost::python::numpy::ndarray simulate(
        boost::python::numpy::ndarray parameters,
        boost::python::numpy::ndarray times) override;

private:
    void solveGillespie(
        std::function<std::array<double, 16>(double, std::array<dtypeint, 4>&)> propensitiesFn,
        std::array<dtypeint, 4> state, std::array<double, 2> t_span,
        double max_t_step, std::vector<double>& times,
        std::vector<dtypeint> &out);

private:
    std::vector<std::string> m_parameterNames;
    std::vector<std::string> m_outputNames;
};


} // namespace seir

#endif // _GILLESPIE_SEIR_HPP
