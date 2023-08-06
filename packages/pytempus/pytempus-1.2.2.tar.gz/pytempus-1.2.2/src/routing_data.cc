#include "common.h"
#include <tempus/routing_data.hh>

namespace bp = boost::python;

void export_RoutingData() {
    {
        GET(Tempus::MMVertex, Tempus::MMVertex::Type, type)
        GET(Tempus::MMVertex, Tempus::db_id_t, id)

        bp::scope s = bp::class_<Tempus::MMVertex>("MMVertex", bp::init<Tempus::MMVertex::Type, Tempus::db_id_t>())
            .def(bp::init<Tempus::db_id_t, Tempus::db_id_t>())
            .add_property("type", type_get)
            .add_property("id", id_get)
            .def("network_id", &Tempus::MMVertex::network_id, bp::return_value_policy<return_optional>())
        ;

        bp::enum_<Tempus::MMVertex::Type>("Type")
            .value("Road", Tempus::MMVertex::Road)
            .value("Transport", Tempus::MMVertex::Transport)
            .value("Poi", Tempus::MMVertex::Poi)
        ;
    }

    {
        GET(Tempus::MMEdge, Tempus::MMVertex, source)
        GET(Tempus::MMEdge, Tempus::MMVertex, target)
        bp::class_<Tempus::MMEdge>("MMEdge", bp::init<const Tempus::MMVertex&, const Tempus::MMVertex&>())
            .add_property("source", source_get)
            .add_property("target", target_get)
        ;
    }

    bp::class_<Tempus::RoutingData>("RoutingData", bp::init<const std::string&>())
        .def("name", &Tempus::RoutingData::name)
        .def("transport_mode", static_cast<boost::optional<Tempus::TransportMode> (Tempus::RoutingData::*)(Tempus::db_id_t) const>(&Tempus::RoutingData::transport_mode), bp::return_value_policy<return_optional>())
        .def("transport_mode", static_cast<boost::optional<Tempus::TransportMode> (Tempus::RoutingData::*)(const std::string&) const>(&Tempus::RoutingData::transport_mode), bp::return_value_policy<return_optional>())
        .def("metadata", static_cast<std::string (Tempus::RoutingData::*)(const std::string&) const>(&Tempus::RoutingData::metadata))
        .def("set_metadata", &Tempus::RoutingData::set_metadata)

    ;
}

