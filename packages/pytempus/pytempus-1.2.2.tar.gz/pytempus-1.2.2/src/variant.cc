#include "common.h"
#include <tempus/variant.hh>

namespace bp = boost::python;

void export_Variant() {
    // We don't expose a Variant python class: instead we transparently handle conversions
    // from python-types to C++ variant
    Variant_from_python();
    bp::to_python_converter<Tempus::Variant, Variant_to_python>();

    map_from_python<std::string, Tempus::Variant, Tempus::VariantMap>();
    bp::to_python_converter<Tempus::VariantMap, map_to_python<std::string, Tempus::Variant>>();

}
