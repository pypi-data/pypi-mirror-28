/**
 *   Copyright (C) 2012-2017 Oslandia <infos@oslandia.com>
 *
 *   This library is free software; you can redistribute it and/or
 *   modify it under the terms of the GNU Library General Public
 *   License as published by the Free Software Foundation; either
 *   version 2 of the License, or (at your option) any later version.
 *
 *   This library is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *   Library General Public License for more details.
 *   You should have received a copy of the GNU Library General Public
 *   License along with this library; if not, see <http://www.gnu.org/licenses/>.
 */

#include <list>
#include <vector>

#include "common.h"

#include <tempus/road_graph.hh>
#include <tempus/public_transport_graph.hh>
#include <tempus/multimodal_graph.hh>
#include <tempus/request.hh>
#include <tempus/roadmap.hh>
#include <tempus/poi.hh>
#include <tempus/plugin.hh>

void export_PluginFactory();
void export_ProgressionCallback();
void export_Variant();
void export_Request();
void export_Plugin();
void export_TransportMode();
void export_RoutingData();
void export_Roadmap();
void export_Graph();
void export_RoadGraph();
void export_Pt();
void export_POI();
void export_Point();
void export_Cost();

namespace bp = boost::python;

using PublicTransportGraphWithId = std::pair<Tempus::db_id_t, const Tempus::PublicTransport::Graph*>;
#if 0
static std::vector<PublicTransportGraphWithId> f_m_graph_public_transports(Tempus::Multimodal::Graph* g)
{
    std::vector<PublicTransportGraphWithId> pt_graphs;
    for ( auto pt_i : g->public_transports() ) {
        pt_graphs.push_back(pt_i);
    }
    return pt_graphs;
}
#endif



boost::optional<Tempus::Road::Edge> edge_wrapper(Tempus::Road::Vertex v1, Tempus::Road::Vertex v2, const Tempus::Road::Graph& road_graph) {
    Tempus::Road::Edge e;
    bool found = false;
    boost::tie( e, found ) = boost::edge( v1, v2, road_graph );
    if (found) {
        return e;
    } else {
        return boost::optional<Tempus::Road::Edge>();
    }
}

BOOST_PYTHON_MODULE(pytempus)
{
    bp::object package = bp::scope();
    package.attr("__path__") = "pytempus";

    bp::to_python_converter<PublicTransportGraphWithId, pair_to_python<Tempus::db_id_t, const Tempus::PublicTransport::Graph*>>();

    date_from_python_converter();
    bp::to_python_converter<Tempus::DateTime, date_to_python_converter>();

    #define VECTOR_SEQ_CONV(Type) custom_vector_from_seq<Type>();  bp::to_python_converter<std::vector<Type>, custom_vector_to_list<Type> >();
    #define LIST_SEQ_CONV(Type) custom_list_from_seq<Type>();  bp::to_python_converter<std::list<Type>, custom_list_to_list<Type> >();

    VECTOR_SEQ_CONV(std::string)
    VECTOR_SEQ_CONV(Tempus::Road::Edge)
    VECTOR_SEQ_CONV(Tempus::Request::Step)
    VECTOR_SEQ_CONV(Tempus::db_id_t)
    VECTOR_SEQ_CONV(Tempus::CostId)
    VECTOR_SEQ_CONV(Tempus::IsochroneValue)
    VECTOR_SEQ_CONV(Tempus::POI)
    VECTOR_SEQ_CONV(PublicTransportGraphWithId)
    VECTOR_SEQ_CONV(Tempus::PublicTransport::Timetable::TripTime)
    LIST_SEQ_CONV(Tempus::ResultElement)

    bp::class_<Tempus::Base>("Base")
        .add_property("db_id", &Tempus::Base::db_id, &Tempus::Base::set_db_id)
    ;

    bp::def("edge", &edge_wrapper, bp::return_value_policy<return_optional>());

    export_PluginFactory();
    export_ProgressionCallback();
    export_Variant();
    export_Request();
    export_Plugin();
    export_TransportMode();
    export_RoutingData();
    export_Roadmap();
    export_Graph();
    export_RoadGraph();
    export_Pt();
    export_POI();
    export_Point();
    export_Cost();

    // tempus_init()
    bp::def("init", &tempus_init);
}

// Apparently we hit here a strange bug in Visual Studio 2015 Update 3
// http://stackoverflow.com/questions/38261530/unresolved-external-symbols-since-visual-studio-2015-update-3-boost-python-link
// that requires to explicitly instanciate get_pointer on "const volatile" pointers
    
namespace boost
{
template <>
Tempus::RoutingData const volatile * get_pointer<class Tempus::RoutingData const volatile >
(class Tempus::RoutingData const volatile *c)
{
    return c;
}
// this is needed too ...
template <>
class optional<Tempus::Plugin const volatile>
{
    using pointer_type = Tempus::Plugin const volatile *;
};
template <>
Tempus::Plugin const volatile * get_pointer<class Tempus::Plugin const volatile >
(class Tempus::Plugin const volatile *c)
{
    return c;
}
template <>
Tempus::PluginRequest const volatile * get_pointer<class Tempus::PluginRequest const volatile >
(class Tempus::PluginRequest const volatile *c)
{
    return c;
}
template <>
Tempus::Roadmap::RoadStep const volatile * get_pointer<class Tempus::Roadmap::RoadStep const volatile >
(class Tempus::Roadmap::RoadStep const volatile *c)
{
    return c;
}
template <>
Tempus::Roadmap::Step const volatile * get_pointer<class Tempus::Roadmap::Step const volatile >
(class Tempus::Roadmap::Step const volatile *c)
{
    return c;
}
}
