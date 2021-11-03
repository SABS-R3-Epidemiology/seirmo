#include "core.hpp"
#include "gillespieSEIR.hpp"

namespace seir
{

SEIRModel* SEIRModelFactory::gillespieSEIR()
{
    return new GillespieSEIR();
}

} // namespace seir
