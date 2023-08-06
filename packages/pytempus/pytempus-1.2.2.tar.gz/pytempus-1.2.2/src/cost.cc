#include "common.h"
#include <tempus/cost.hh>

namespace bp = boost::python;

void export_Cost() {
    bp::enum_<Tempus::CostId>("Cost")
        .value("Distance", Tempus::CostId::CostDistance)
        .value("Duration", Tempus::CostId::CostDuration)
        .value("Price", Tempus::CostId::CostPrice)
        .value("Carbon", Tempus::CostId::CostCarbon)
        .value("Calories", Tempus::CostId::CostCalories)
        .value("NumberOfChanges", Tempus::CostId::CostNumberOfChanges)
        .value("Variability", Tempus::CostId::CostVariability)
        .value("PathComplexity", Tempus::CostId::CostPathComplexity)
        .value("Elevation", Tempus::CostId::CostElevation)
        .value("Security", Tempus::CostId::CostSecurity)
        .value("Landmark", Tempus::CostId::CostLandmark)
    ;

    bp::def("cost_name", &Tempus::cost_name);
    bp::def("cost_unit", &Tempus::cost_unit);

    map_from_python<Tempus::CostId, double, Tempus::Costs>();
    bp::to_python_converter<Tempus::Costs, map_to_python<Tempus::CostId, double>>();
}
