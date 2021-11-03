#include "gillespieSEIR.hpp"
#include <iostream>
#include <functional>
#include <exception>
#include <random>
#include <math.h>
#include <iostream>

namespace py = boost::python;
namespace np = boost::python::numpy;

namespace seir
{

    GillespieSEIR::GillespieSEIR() : m_parameterNames({"S0", "E0", "I0", "R0", "beta", "kappa", "gamma"}),
                                     m_outputNames({"S", "E", "I", "R"})
    {
        m_nParameters = 7;
        m_nOutputs = 4;
    }

    void GillespieSEIR::solveGillespie(
        std::function<std::array<double, 16>(double, std::array<dtypeint, 4>&)> propensitiesFn,
        std::array<dtypeint, 4> state, std::array<double, 2> t_span,
        double max_t_step, std::vector<double>& times,
        std::vector<dtypeint>& out)
    {
        int outIndex = 0;
        double time = t_span[0];
        while (outIndex < times.size() && time == time)
        {
            if (time >= times[std::min((unsigned long)outIndex, times.size()-1)])
                std::copy(state.begin(), state.end(), out.begin()+(4*outIndex++));

            auto propensities = propensitiesFn(time, state);
            double s = 0;
            for (int i = 0; i < propensities.size(); i++) s+= propensities[i];
            if (s <= 0) s  = 1 / ((t_span[1] - t_span[0]) * max_t_step);
            double r1 = std::abs((double)std::rand() / RAND_MAX);
            if (r1 <= 0) r1 = 1.0;
            double time_step = std::log(1 / r1) / s;
            time += time_step;

            for (int i = 0; i < propensities.size(); i++) propensities[i] /= s;
            double r = std::abs((double)std::rand() / RAND_MAX);
            for (int i = 0; i < propensities.size(); i++)
            {
                r -= propensities[i];
                if (r <= 0)
                {
                    state[i/4]--;
                    state[i%4]++;
                    break;
                }
            }
        }
    }
    

    np::ndarray GillespieSEIR::simulate(
        np::ndarray parameters, np::ndarray times)
    {
        if (parameters.shape(0) != 7)
            throw std::runtime_error(std::string("Bad Parameters Input"));

        std::vector<double> vecTimes(times.shape(0));
        double* times_ptr = reinterpret_cast<double*>(times.get_data());
        for (int i = 0; i < vecTimes.size(); i++) vecTimes[i] = *(times_ptr + i);

        std::array<dtypeint, 4> initial;
        double* parameters_ptr = reinterpret_cast<double*>(parameters.get_data());
        for (int i = 0; i < 4; i++) initial[i] = (int)*(parameters_ptr + i);
        double beta = *(parameters_ptr + 4);
        double kappa = *(parameters_ptr + 5);
        double gamma = *(parameters_ptr + 6);

        //for (int i = 0; i < 7; i++) std::cout << *(parameters_ptr + i) << " ";
        //std::cout << std::endl;

        std::function<std::array<double, 16>(double, std::array<dtypeint, 4>&)> propensitiesFn =
        [&beta, &kappa, &gamma](double t, std::array<dtypeint, 4>& state)
        {
            std::array<double, 16> propensities = std::array<double, 16>();
            propensities.fill(0);

            propensities[1] = beta * (double)state[0] * (double)state[2];
            propensities[6] = kappa * (double)state[1];
            propensities[11] = gamma * (double)state[2];

            return propensities;
        };

        std::vector<dtypeint> data(times.shape(0) * 4, 0);

        solveGillespie(propensitiesFn, initial,
            {vecTimes[0], vecTimes[vecTimes.size()-1]}, 0.01,
            vecTimes,
            data);

        np::ndarray result = np::from_data(data.data(),
            np::dtype::get_builtin<dtypeint>(),
            py::make_tuple(data.size()/4, 4),
            py::make_tuple(4*sizeof(dtypeint), sizeof(dtypeint)),
            py::object());

        return result.copy();
    }

} // namespace seir
