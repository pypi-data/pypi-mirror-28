#include "common.h"
#include <tempus/plugin_factory.hh>

namespace bp = boost::python;

void register_plugin_fn(
    Tempus::PluginFactory* plugin_factory,
    bp::object create,
    bp::object options,
    bp::object caps,
    bp::object name)
{
    auto
    create_fn = [create](Tempus::ProgressionCallback& p, const Tempus::VariantMap& opt) -> Tempus::Plugin* {
        bp::object do_not_delete_me_please (create(p, opt));
        bp::incref(do_not_delete_me_please.ptr());
        return bp::extract<Tempus::Plugin*>(do_not_delete_me_please);
    };

    auto
     options_fn = [options]() {
        bp::object do_not_delete_me_please (options());
        bp::incref(do_not_delete_me_please.ptr());

        // Aha, nice try. We can't use this ...
        // return bp::extract<Tempus::Plugin::Capabilities*>(do_not_delete_me_please);

        // because there's a of a subtle difference: extract<> needs a bp::class_<> declaration
        // to be able to use python->c++ converters we registered.
        // As OptionDescriptionList is a simple typedef to std::map<> + specific converters we need to
        // hack a bit to get boost|python to play nice with us...

        // So let's try to explicitely use the converter
        typedef map_from_python<std::string, Tempus::Plugin::OptionDescription, Tempus::Plugin::OptionDescriptionList> Conv;
        if (Conv::convertible(do_not_delete_me_please.ptr())) {
            Tempus::Plugin::OptionDescriptionList* result = new Tempus::Plugin::OptionDescriptionList();
            Conv::construct_in_object(do_not_delete_me_please.ptr(), result);
            return result;
        } else {
            throw std::runtime_error( "Cannot convert to C++ OptionDescriptionList" );
        }
    };

    auto
     caps_fn = [caps]() {
        bp::object do_not_delete_me_please (caps());
        bp::incref(do_not_delete_me_please.ptr());
        return bp::extract<Tempus::Plugin::Capabilities*>(do_not_delete_me_please);
    };

    auto
     name_fn = [name]() { return bp::extract<const char*>(name()); };


    plugin_factory->register_plugin_fn(create_fn, options_fn, caps_fn, name_fn);
}

void export_PluginFactory() {
    bp::class_<Tempus::PluginFactory, boost::noncopyable>("PluginFactory", bp::no_init)
        .def("plugin_list", &Tempus::PluginFactory::plugin_list)
        .def("create_plugin", &Tempus::PluginFactory::create_plugin, bp::return_value_policy<bp::reference_existing_object>())
        .def("register_plugin_fn", &register_plugin_fn)
        .def("plugin_capabilities", &Tempus::PluginFactory::plugin_capabilities)
        .def("option_descriptions", &Tempus::PluginFactory::option_descriptions)
        .def("instance", &Tempus::PluginFactory::instance, bp::return_value_policy<bp::reference_existing_object>()).staticmethod("instance")
    ;
    // .def("create_plugin_from_fn", &Tempus::PluginFactory::create_plugin_from_fn, bp::return_value_policy<bp::reference_existing_object>())
    // bp::
}

