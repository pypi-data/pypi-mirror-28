#include "common.h"
#include <tempus/plugin.hh>

namespace bp = boost::python;

class PluginWrapper : public Tempus::Plugin, public bp::wrapper<Tempus::Plugin> {
    public:
        PluginWrapper(const std::string& name /*, const Tempus::VariantMap& opt= Tempus::VariantMap()*/) : Tempus::Plugin(name /*, opt*/) {}

        virtual std::unique_ptr<Tempus::PluginRequest> request( const Tempus::VariantMap&) const {
            std::cerr << "Do not call me" << std::endl;
            return std::unique_ptr<Tempus::PluginRequest>(nullptr);
        }

        Tempus::PluginRequest* request2(const Tempus::VariantMap& options = Tempus::VariantMap() ) const {
            // see return policy
            return request(options).release();
        }

        const Tempus::RoutingData* routing_data() const {
            return this->get_override("routing_data")();
        }
};

static auto f_option_description_default_value_get(Tempus::Plugin::OptionDescription* o) -> decltype(Variant_to_python::convert(o->default_value))
    { return Variant_to_python::convert(o->default_value); }
		
static void f_option_description_default_value_set(Tempus::Plugin::OptionDescription* o, bp::object a)
    { o->default_value = Variant_from_python::construct(a.ptr()); }

void export_Plugin() {
    bp::class_<Tempus::PluginRequest>("PluginRequest", bp::init<const Tempus::Plugin*, const Tempus::VariantMap&>())
        .def("process", adapt_unique_by_value(&Tempus::PluginRequest::process))
        .def("metrics", &Tempus::PluginRequest::metrics, bp::return_value_policy<bp::copy_non_const_reference>());
    ;


    {
        bp::scope s = bp::class_<PluginWrapper, boost::noncopyable>("Plugin", bp::init<const std::string& /*, const Tempus::VariantMap&*/>())
            .def("request", &PluginWrapper::request2, bp::return_value_policy<bp::manage_new_object>()) // for python plugin
            .def("request", adapt_unique_const(&Tempus::Plugin::request)) // for C++ plugin called from py
            .def("routing_data", bp::pure_virtual(&Tempus::Plugin::routing_data), bp::return_internal_reference<>())
            .add_property("name", &Tempus::Plugin::name)
            .def("declare_option", &Tempus::Plugin::declare_option).staticmethod("declare_option")
        ;

        GET_SET(Tempus::Plugin::Capabilities, bool, intermediate_steps)
        GET_SET(Tempus::Plugin::Capabilities, bool, depart_after)
        GET_SET(Tempus::Plugin::Capabilities, bool, arrive_before)
        GET(Tempus::Plugin::Capabilities, std::vector<Tempus::CostId>, optimization_criteria)
        bp::class_<Tempus::Plugin::Capabilities>("Capabilities")
            .add_property("intermediate_steps", intermediate_steps_get, intermediate_steps_set)
            .add_property("depart_after", depart_after_get, depart_after_set)
            .add_property("arrive_before", arrive_before_get, arrive_before_set)
            .add_property("optimization_criteria", optimization_criteria_get)
        ;
		

        bp::class_<Tempus::Plugin::OptionDescription>("OptionDescription")
            .def_readwrite("description", &Tempus::Plugin::OptionDescription::description)
            .add_property("default_value",
                // We don't want to expose Variant to python, so we instead use convertors here.
                // This allows to keep implicit conversion between VariantMap and dict.
                f_option_description_default_value_get,
				f_option_description_default_value_set)
            .def_readwrite("visible", &Tempus::Plugin::OptionDescription::visible)
        ;


    }
    map_from_python<std::string, Tempus::Plugin::OptionDescription, Tempus::Plugin::OptionDescriptionList>();
    bp::to_python_converter<Tempus::Plugin::OptionDescriptionList, map_to_python<std::string, Tempus::Plugin::OptionDescription> >();

    bp::def("load_routing_data", &Tempus::load_routing_data, bp::return_internal_reference<>());
}
