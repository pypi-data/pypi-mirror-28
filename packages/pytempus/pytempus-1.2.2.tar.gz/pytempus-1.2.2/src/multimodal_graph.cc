#include "common.h"
#include <tempus/multimodal_graph.hh>

namespace bp = boost::python;

using PublicTransportGraphWithId = std::pair<Tempus::db_id_t, const Tempus::PublicTransport::Graph*>;
static std::vector<PublicTransportGraphWithId> f_m_graph_public_transports(Tempus::Multimodal::Graph* g)
{
    std::vector<PublicTransportGraphWithId> pt_graphs;
    for ( auto pt_i : g->public_transports() ) {
        pt_graphs.push_back(pt_i);
    }
    return pt_graphs;
}

void export_Graph() {
    {
        bp::object modalModule(bp::handle<>(bp::borrowed(PyImport_AddModule("tempus.Multimodal"))));
        bp::scope().attr("Multimodal") = modalModule;
        bp::scope modalScope = modalModule;

        {
            bp::scope s = bp::class_<Tempus::Multimodal::Vertex>("Vertex")
                .def(bp::init<const Tempus::Multimodal::Graph&, Tempus::Road::Vertex, Tempus::Multimodal::Vertex::road_t>())
                .def(bp::init<const Tempus::Multimodal::Graph&, Tempus::PublicTransportGraphIndex, Tempus::PublicTransport::Vertex, Tempus::Multimodal::Vertex::pt_t>())
                .def(bp::init<const Tempus::Multimodal::Graph&, const Tempus::POIIndex, Tempus::Multimodal::Vertex::poi_t>())
                .add_property("type", &Tempus::Multimodal::Vertex::type)
                .def("is_null", &Tempus::Multimodal::Vertex::is_null)
                .add_property("road_vertex", &Tempus::Multimodal::Vertex::road_vertex)
                .add_property("pt_graph_idx", &Tempus::Multimodal::Vertex::pt_graph_idx)
                .add_property("pt_vertex", &Tempus::Multimodal::Vertex::pt_vertex)
                .add_property("poi_idx", &Tempus::Multimodal::Vertex::poi_idx)
                .add_property("hash", &Tempus::Multimodal::Vertex::hash)
                // .def("vertex", +[](Tempus::Multimodal::Graph* g, Tempus::Multimodal::Graph::vertices_size_type i) { return vertex(i, *g); })

                // .add_property("graph", &Tempus::Multimodal::Vertex::graph)
                // .add_property("road_graph", &Tempus::Multimodal::Vertex::road_graph)
            ;

            bp::enum_<Tempus::Multimodal::Vertex::VertexType>("VertexType")
                .value("Null", Tempus::Multimodal::Vertex::VertexType::Null)
                .value("Road", Tempus::Multimodal::Vertex::VertexType::Road)
                .value("PublicTransport", Tempus::Multimodal::Vertex::VertexType::PublicTransport)
                .value("Poi", Tempus::Multimodal::Vertex::VertexType::Poi)
            ;
        }

        bp::def("get_road_node", &Tempus::Multimodal::get_road_node);
        bp::def("get_pt_stop", &Tempus::Multimodal::get_pt_stop);
        bp::def("get_mm_vertex", &Tempus::Multimodal::get_mm_vertex);
        bp::def("num_vertices", &Tempus::Multimodal::num_vertices);
        bp::def("num_edges", &Tempus::Multimodal::num_edges);
        bp::def("source", &Tempus::Multimodal::source);
        bp::def("target", &Tempus::Multimodal::target);
        bp::def("vertices", &Tempus::Multimodal::vertices);
        bp::def("edges", &Tempus::Multimodal::edges);
        bp::def("out_edges", &Tempus::Multimodal::out_edges);
        bp::def("in_edges", &Tempus::Multimodal::in_edges);
        bp::def("out_degree", &Tempus::Multimodal::out_degree);
        bp::def("in_degree", &Tempus::Multimodal::in_degree);
        bp::def("degree", &Tempus::Multimodal::degree);
        bp::def("edge", &Tempus::Multimodal::edge);


        {
            GET(Tempus::Multimodal::Edge, Tempus::Multimodal::Vertex, source)
            GET(Tempus::Multimodal::Edge, Tempus::Multimodal::Vertex, target)
            GET(Tempus::Multimodal::Edge, Tempus::Road::Edge, road_edge)
            bp::scope s = bp::class_<Tempus::Multimodal::Edge>("Edge")
                .add_property("source", source_get)
                .add_property("target", target_get)
                .add_property("road_edge", road_edge_get)
                .add_property("connection_type", &Tempus::Multimodal::Edge::connection_type)
                .add_property("traffic_rules", &Tempus::Multimodal::Edge::traffic_rules)
            ;

            bp::enum_<Tempus::Multimodal::Edge::ConnectionType>("ConnectionType")
                .value("UnknownConnection", Tempus::Multimodal::Edge::ConnectionType::UnknownConnection)
                .value("Road2Road", Tempus::Multimodal::Edge::ConnectionType::Road2Road)
                .value("Road2Transport", Tempus::Multimodal::Edge::ConnectionType::Road2Transport)
                .value("Transport2Road", Tempus::Multimodal::Edge::ConnectionType::Transport2Road)
                .value("Transport2Transport", Tempus::Multimodal::Edge::ConnectionType::Transport2Transport)
                .value("Road2Poi", Tempus::Multimodal::Edge::ConnectionType::Road2Poi)
                .value("Poi2Road", Tempus::Multimodal::Edge::ConnectionType::Poi2Road)
            ;
        }


        {
            using namespace Tempus::Multimodal;
            using namespace Tempus;
            const Road::Graph& (Graph::*roadl_get)() const = &Graph::road;
            auto road_get = bp::make_function(roadl_get, bp::return_value_policy<bp::copy_const_reference>());

            bp::scope s = bp::class_<Graph, bp::bases<RoutingData>, boost::noncopyable>("Graph", bp::no_init)
                .def("road", road_get)
                .def("pois", &Graph::pois)
                .def("road_vertex_from_id", &Graph::road_vertex_from_id, bp::return_value_policy<return_optional>())
                .def("road_edge_from_id", &Graph::road_edge_from_id, bp::return_value_policy<return_optional>())
                .def("public_transport_index", &Graph::public_transport_index)
                .def("public_transport_rindex", &Graph::public_transport_rindex)
                .def("public_transport", &Graph::public_transport, bp::return_value_policy<bp::copy_const_reference>())
                .def("public_transports", f_m_graph_public_transports)
            ;
        }
    }

    BIND_ITERATOR(Tempus::Multimodal::VertexIterator, "t_m_vi")
    BIND_ITERATOR(Tempus::Multimodal::OutEdgeIterator, "t_m_oei")
    BIND_ITERATOR(Tempus::Multimodal::InEdgeIterator, "t_m_iei")
    BIND_ITERATOR(Tempus::Multimodal::EdgeIterator, "t_m_ei")
}
