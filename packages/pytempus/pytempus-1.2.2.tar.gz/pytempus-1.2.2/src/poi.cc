#include "common.h"
#include <tempus/poi.hh>

namespace bp = boost::python;

void export_POI() {
    GET_SET(Tempus::POI, Tempus::POI::PoiType, poi_type)
    GET_SET(Tempus::POI, std::string, name)
    GET_SET(Tempus::POI, std::vector<Tempus::db_id_t>, parking_transport_modes)
    GET_SET(Tempus::POI, Tempus::Road::Edge, road_edge)
    GET_SET(Tempus::POI, Tempus::Point3D, coordinates)

    bp::scope s = bp::class_<Tempus::POI, bp::bases<Tempus::Base>>("POI")
        .add_property("poi_type", poi_type_get, poi_type_set)
        .add_property("name", name_get, name_set)
        .add_property("parking_transport_modes", parking_transport_modes_get, parking_transport_modes_set)
        .add_property("road_edge", road_edge_get, road_edge_set)
        .add_property("coordinates", coordinates_get, coordinates_set)
    ;

    bp::enum_<Tempus::POI::PoiType>("PoiType")
        .value("TypeCarPark", Tempus::POI::PoiType::TypeCarPark)
        .value("TypeSharedCarPoint", Tempus::POI::PoiType::TypeSharedCarPoint)
        .value("TypeCyclePark", Tempus::POI::PoiType::TypeCyclePark)
        .value("TypeSharedCyclePoint", Tempus::POI::PoiType::TypeSharedCyclePoint)
        .value("TypeUserPOI", Tempus::POI::PoiType::TypeUserPOI)
    ;
}
