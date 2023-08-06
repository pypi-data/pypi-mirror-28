#include "common.h"
#include <tempus/public_transport.hh>
#include <tempus/public_transport_graph.hh>

    static void f_pt_network_add_agency(Tempus::PublicTransport::Network* n, const Tempus::PublicTransport::Agency& agency) { n->add_agency(agency); }
    static void f_pt_service_map_add(Tempus::PublicTransport::ServiceMap* sm, const std::string& id, const Tempus::Date& date ) { sm->add(id, date); }
    static bool f_pt_service_map_is_available_on(Tempus::PublicTransport::ServiceMap* sm, const std::string& id, const Tempus::Date& date ) { return sm->is_available_on( id, date ); }

    static Tempus::PublicTransport::Stop f_pt_graph_get_item_vertex_(Tempus::PublicTransport::Graph* g, Tempus::PublicTransport::Vertex v) { return (*g)[v]; }
    static Tempus::PublicTransport::Section f_pt_graph_get_item_edge_(Tempus::PublicTransport::Graph* g, Tempus::PublicTransport::Edge e) { return (*g)[e]; }
    static Tempus::PublicTransport::Vertex f_pt_graph_vertex(Tempus::PublicTransport::Graph* g, Tempus::PublicTransport::Graph::vertices_size_type i) { return vertex(i, *g); }
    static size_t f_pt_graph_num_egdes(Tempus::PublicTransport::Graph* g) { return num_edges(*g); }
    //static Tempus::PublicTransport::Edge f_pt_graph_edge_from_index(Tempus::PublicTransport::Graph* g, Tempus::PublicTransport::Graph::edges_size_type i) { return edge_from_index(i, *g); }
    static Tempus::PublicTransport::Section f_pt_graph_edge(Tempus::PublicTransport::Graph* g, Tempus::PublicTransport::Graph::edge_descriptor e) { return (*g)[e];}
    static Tempus::PublicTransport::Vertex f_pt_graph_source(Tempus::PublicTransport::Graph* g, Tempus::PublicTransport::Graph::edge_descriptor e) { return source(e, *g);}
    static Tempus::PublicTransport::Vertex f_pt_graph_target(Tempus::PublicTransport::Graph* g, Tempus::PublicTransport::Graph::edge_descriptor e) { return target(e, *g);}
    static size_t f_pt_graph_num_vertices(Tempus::PublicTransport::Graph* g) { return num_vertices(*g); }
    static size_t f_pt_graph_num_edges(Tempus::PublicTransport::Graph* g) { return num_edges(*g); }
    static std::pair<Tempus::PublicTransport::VertexIterator, Tempus::PublicTransport::VertexIterator> f_pt_graph_vertices( Tempus::PublicTransport::Graph* g ) { return vertices(*g); }
    static std::pair<Tempus::PublicTransport::EdgeIterator, Tempus::PublicTransport::EdgeIterator> f_pt_graph_edges( Tempus::PublicTransport::Graph* g ) { return edges(*g); }
    static std::vector<Tempus::PublicTransport::Timetable::TripTime> f_time_table_next_departures( Tempus::PublicTransport::Timetable* tt, float t )
    {
        std::vector<Tempus::PublicTransport::Timetable::TripTime> v;
        auto pit = tt->next_departures(t);
        for ( auto itt = pit.first; itt != pit.second; itt++ ) {
            v.push_back(*itt);
        }
        return v;
    }
    static std::vector<Tempus::PublicTransport::Timetable::TripTime> f_time_table_previous_arrivals( Tempus::PublicTransport::Timetable* tt, float t )
    {
        std::vector<Tempus::PublicTransport::Timetable::TripTime> v;
        auto pit = tt->previous_arrivals(t);
        for ( auto itt = pit.first; itt != pit.second; itt++ ) {
            v.push_back(*itt);
        }
        return v;
    }

void export_Pt() {
    bp::object ptModule(bp::handle<>(bp::borrowed(PyImport_AddModule("tempus.PublicTransport"))));
    bp::scope().attr("PublicTransport") = ptModule;
    bp::scope ptScope = ptModule;

    // public_transport.hh
    {
        GET_SET(Tempus::PublicTransport::Agency, std::string, name);
        bp::class_<Tempus::PublicTransport::Agency, bp::bases<Tempus::Base>>("Agency")
            .add_property("name", name_get, name_set)
            ;
    }

    {
        GET_SET(Tempus::PublicTransport::Network, std::string, name);
        GET(Tempus::PublicTransport::Network, std::vector<Tempus::PublicTransport::Agency>, agencies);
        bp::class_<Tempus::PublicTransport::Network, bp::bases<Tempus::Base>>("Network")
            .add_property("name", name_get, name_set)
            .add_property("agencies", agencies_get)
            .def("add_agency", f_pt_network_add_agency)
            ;
    }

    // public_transport_graph.hh
    {
        bp::class_<Tempus::PublicTransport::ServiceMap>("ServiceMap")
            .def("add", f_pt_service_map_add)
            .def("is_available_on", f_pt_service_map_is_available_on)
            ;        
    }
    {
        GET(Tempus::PublicTransport::GraphProperties, Tempus::PublicTransport::ServiceMap, service_map);
        bp::class_<Tempus::PublicTransport::GraphProperties>("GraphProperties")
            .add_property("service_map", service_map_get)
            ;        
    }

    {
        bp::scope s = bp::class_<Tempus::PublicTransport::Graph>("Graph", bp::no_init)
            .def("__getitem__", f_pt_graph_get_item_vertex_)
            .def("__getitem__", f_pt_graph_get_item_edge_)
            .def("vertex", f_pt_graph_vertex)
            .def("num_edges", f_pt_graph_num_egdes)
            //.def("edge_from_index", f_pt_graph_edge_from_index)
            .def("edge", f_pt_graph_edge)
            .def("source", f_pt_graph_source)
            .def("target", f_pt_graph_target)
        ;

        bp::def("num_vertices", f_pt_graph_num_vertices);
        bp::def("num_edges", f_pt_graph_num_edges);
        bp::def("vertices", f_pt_graph_vertices);
        bp::def("edges", f_pt_graph_edges);
    }

    BIND_ITERATOR(Tempus::PublicTransport::VertexIterator, "pt_vi")
    BIND_ITERATOR(Tempus::PublicTransport::OutEdgeIterator, "pt_oei")
    BIND_ITERATOR(Tempus::PublicTransport::InEdgeIterator, "pt_iei")
    BIND_ITERATOR(Tempus::PublicTransport::EdgeIterator, "pt_ei")


    {
        bp::class_<Tempus::PublicTransport::Graph::edge_descriptor>("edge_descriptor", bp::no_init)
            ;
    }

    {
        using namespace Tempus::PublicTransport;
        using namespace Tempus;
        GET_SET(Stop, std::string, name);
        GET_SET(Stop, bool, is_station);
        GET_SET(Stop, Optional<Vertex>, parent_station);
        GET_SET(Stop, Optional<uint16_t>, graph);
        GET_SET(Stop, Optional<Vertex>, vertex);
        GET_SET(Stop, Road::Edge, road_edge);
        GET_SET(Stop, boost::optional<Road::Edge>, opposite_road_edge);
        GET_SET(Stop, Abscissa, abscissa_road_section );
        GET_SET(Stop, uint16_t, zone_id );
        GET_SET(Stop, Point3D, coordinates );
        bp::class_<Stop, bp::bases<Tempus::Base>>("Stop")
            .add_property("graph", graph_get, graph_set)
            .add_property("vertex", vertex_get, vertex_set)
            .add_property("name", name_get, name_set)
            .add_property("is_station", is_station_get, is_station_set)
            .add_property("parent_station", parent_station_get, parent_station_set)
            .add_property("road_edge", road_edge_get, road_edge_set)
            .add_property("opposite_road_edge", opposite_road_edge_get, opposite_road_edge_set)
            .add_property("abscissa_road_section", abscissa_road_section_get, abscissa_road_section_set)
            .add_property("zone_id", zone_id_get, zone_id_set)
            .add_property("coordinates", coordinates_get, coordinates_set)
            ;
    }

    {
        using namespace Tempus::PublicTransport;
        using namespace Tempus;
        bp::scope s = bp::class_<Timetable>("Timetable");

        bp::def("next_departures", f_time_table_next_departures);
        bp::def("previous_arrivals", f_time_table_previous_arrivals);

        GET_SET(Timetable::TripTime, float, departure_time );
        GET_SET(Timetable::TripTime, float, arrival_time );
        GET_SET(Timetable::TripTime, db_id_t, trip_id );
        GET_SET(Timetable::TripTime, std::string, service_id );
        bp::class_<Timetable::TripTime>("TripTime")
            .add_property("departure_time", departure_time_get, departure_time_set)
            .add_property("arrival_time", arrival_time_get, arrival_time_set)
            .add_property("trip_id", trip_id_get, trip_id_set)
            .add_property("service_id", service_id_get, service_id_set)
            ;
    }

    {
        using namespace Tempus::PublicTransport;
        using namespace Tempus;
        GET_SET(Section, db_id_t, network_id);
        GET(Section, Timetable, time_table);
        bp::class_<Section>("Section")
            .add_property("network_id", network_id_get, network_id_set)
            .add_property("time_table", time_table_get)
            ;
    }

    bp::def("next_departure", &Tempus::PublicTransport::next_departure);
    bp::def("previous_arrival", &Tempus::PublicTransport::previous_arrival);
}
