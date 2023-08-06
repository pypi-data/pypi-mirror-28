#include "common.h"
#include <tempus/road_graph.hh>

namespace bp = boost::python;

static Tempus::Road::Node f_road_graph_get_item_vertex_(Tempus::Road::Graph* g, Tempus::Road::Vertex v) { return (*g)[v]; }
static Tempus::Road::Section f_road_graph_get_item_edge_(Tempus::Road::Graph* g, Tempus::Road::Edge e) { return (*g)[e]; }
static Tempus::Road::Vertex f_road_graph_vertex(Tempus::Road::Graph* g, Tempus::Road::Graph::vertices_size_type i) { return vertex(i, *g); }
static size_t f_road_graph_num_egdes(Tempus::Road::Graph* g) { return num_edges(*g); }
static Tempus::Road::Edge f_road_graph_edge_from_index(Tempus::Road::Graph* g, Tempus::Road::Graph::edges_size_type i) { return edge_from_index(i, *g); }
static Tempus::Road::Section f_road_graph_edge(Tempus::Road::Graph* g, Tempus::Road::Graph::edge_descriptor e) { return (*g)[e];}
static Tempus::Road::Vertex f_road_graph_source(Tempus::Road::Graph* g, Tempus::Road::Graph::edge_descriptor e) { return source(e, *g);}
static Tempus::Road::Vertex f_road_graph_target(Tempus::Road::Graph* g, Tempus::Road::Graph::edge_descriptor e) { return target(e, *g);}
static size_t f_road_graph_num_vertices(Tempus::Road::Graph* g) { return num_vertices(*g); }

void export_RoadGraph() {
    bp::object roadModule(bp::handle<>(bp::borrowed(PyImport_AddModule("tempus.Road"))));
    bp::scope().attr("Road") = roadModule;
    bp::scope roadScope = roadModule;

    {
        bp::scope s = bp::class_<Tempus::Road::Graph>("Graph", bp::no_init)
        //                       ^
        // boost python can't wrap lambda, but can wrap func pointers...
        // (see http://stackoverflow.com/questions/18889028/a-positive-lambda-what-sorcery-is-this)
            .def("__getitem__", f_road_graph_get_item_vertex_)
            .def("__getitem__", f_road_graph_get_item_edge_)
            .def("vertex", f_road_graph_vertex)
            .def("num_edges", f_road_graph_num_egdes)
            .def("edge_from_index", f_road_graph_edge_from_index)
            .def("edge", f_road_graph_edge)

            .def("source", f_road_graph_source)
            .def("target", f_road_graph_target)
        ;


        bp::def("num_vertices", f_road_graph_num_vertices);
        // size_t (*nv)(const Tempus::Road::Graph&) = &boost::graph::num_vertices;
        // bp::def("num_vertices", nv);
    }


    bp::class_<Tempus::Road::Graph::edge_descriptor>("edge_descriptor", bp::no_init)
    ;

    bp::enum_<Tempus::Road::RoadType>("RoadType")
        .value("RoadMotorway", Tempus::Road::RoadType::RoadMotorway)
        .value("RoadPrimary", Tempus::Road::RoadType::RoadPrimary)
        .value("RoadSecondary", Tempus::Road::RoadType::RoadSecondary)
        .value("RoadStreet", Tempus::Road::RoadType::RoadStreet)
        .value("RoadOther", Tempus::Road::RoadType::RoadOther)
        .value("RoadCycleWay", Tempus::Road::RoadType::RoadCycleWay)
        .value("RoadPedestrianOnly", Tempus::Road::RoadType::RoadPedestrianOnly)
    ;

    GET_SET(Tempus::Road::Node, bool, is_bifurcation)
    GET_SET(Tempus::Road::Node, Tempus::Point3D, coordinates)
    bp::class_<Tempus::Road::Node, bp::bases<Tempus::Base>>("Node")
        .add_property("is_bifurcation", is_bifurcation_get, is_bifurcation_set)
        .add_property("coordinates", coordinates_get, coordinates_set)
    ;

    GET_SET(Tempus::Road::Section, float, length)
    GET_SET(Tempus::Road::Section, float, car_speed_limit)
    GET_SET(Tempus::Road::Section, uint16_t, traffic_rules)
    GET_SET(Tempus::Road::Section, uint16_t, parking_traffic_rules)
    GET_SET(Tempus::Road::Section, uint8_t, lane)
    GET_SET(Tempus::Road::Section, Tempus::Road::RoadType, road_type)
    bp::class_<Tempus::Road::Section, bp::bases<Tempus::Base>>("Section")
        .add_property("length", length_get, length_set)
        .add_property("car_speed_limit", car_speed_limit_get, car_speed_limit_set)
        .add_property("traffic_rules", traffic_rules_get, traffic_rules_set)
        .add_property("parking_traffic_rules", parking_traffic_rules_get, parking_traffic_rules_set)
        .add_property("lane", lane_get, lane_set)
        .add_property("road_type", road_type_get, road_type_set)
        .add_property("is_roundabout", &Tempus::Road::Section::is_roundabout, &Tempus::Road::Section::set_is_roundabout)
        .add_property("is_bridge", &Tempus::Road::Section::is_bridge, &Tempus::Road::Section::set_is_bridge)
        .add_property("is_tunnel", &Tempus::Road::Section::is_tunnel, &Tempus::Road::Section::set_is_tunnel)
        .add_property("is_ramp", &Tempus::Road::Section::is_ramp, &Tempus::Road::Section::set_is_ramp)
        .add_property("is_tollway", &Tempus::Road::Section::is_tollway, &Tempus::Road::Section::set_is_tollway)
    ;

    GET(Tempus::Road::Restriction, Tempus::Road::Restriction::EdgeSequence, road_edges)
    GET_SET(Tempus::Road::Restriction, Tempus::Road::Restriction::CostPerTransport, cost_per_transport)
    bp::class_<Tempus::Road::Restriction, bp::bases<Tempus::Base>>("Restriction", bp::no_init)
        .add_property("road_edges", road_edges_get)
        .add_property("cost_per_transport", cost_per_transport_get, cost_per_transport_set)
    ;
}
