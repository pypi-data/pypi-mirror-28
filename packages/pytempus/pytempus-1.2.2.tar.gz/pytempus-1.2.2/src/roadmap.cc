#include "common.h"
#include <tempus/roadmap.hh>

namespace bp = boost::python;

void add_step_wrapper(Tempus::Roadmap* roadmap, Tempus::Roadmap::RoadStep& obj)
{
    roadmap->add_step( obj.clone() );
}

struct RoadmapIterator
{
    RoadmapIterator(Tempus::Roadmap::StepConstIterator it, Tempus::Roadmap::StepConstIterator it_end) : it_(it), it_end_(it_end) {}
    const Tempus::Roadmap::Step& next()
    {
        if ( it_ == it_end_ ) {
            PyErr_SetString(PyExc_StopIteration, "No more data.");
            bp::throw_error_already_set();
        }
        const Tempus::Roadmap::Step& s = *it_;
        it_++;
        return s;
    }
    Tempus::Roadmap::StepConstIterator it_, it_end_;
};

static const Tempus::Roadmap::Step& roadmap_it_next( RoadmapIterator& it )
{
    return it.next();
}
static RoadmapIterator roadmap_iter( const Tempus::Roadmap* rm )
{
    return RoadmapIterator( rm->begin(), rm->end() );
}

void export_Roadmap() {
    {
        GET_SET(Tempus::Roadmap, Tempus::DateTime, starting_date_time);
        // manually wrap Roadmap iterators, for some odd reason, bp::range looses type information of derived classes (RoadStep, etc.)
        bp::class_<RoadmapIterator>("RoadmapIterator", bp::no_init)
            .def("__next__", roadmap_it_next, bp::return_value_policy<bp::reference_existing_object>())
            ;
        bp::scope s = bp::class_<Tempus::Roadmap>("Roadmap")
            // with_custodian_and_ward_postcall<0,1> is used to tie the lifetime of the result (0-th argument)
            // == the newly created RoadmapIterator
            // to the lifetime of the first argument (== this == the Roadmap)
            .def("__iter__", &roadmap_iter, bp::with_custodian_and_ward_postcall<0,1>())
            .def("add_step", &add_step_wrapper) // Tempus::Roadmap::add_step)
            .add_property("starting_date_time", starting_date_time_get, starting_date_time_set)
        ;

        {
            GET_SET(Tempus::Roadmap::Step, Tempus::Roadmap::Step::StepType, step_type)
            GET_SET(Tempus::Roadmap::Step, Tempus::db_id_t, transport_mode)
            GET_SET(Tempus::Roadmap::Step, std::string, geometry_wkb)


            bp::scope t = bp::class_<Tempus::Roadmap::Step>("Step", bp::init<Tempus::Roadmap::Step::StepType>())
                .add_property("step_type", step_type_get, step_type_set)
                .add_property("transport_mode", transport_mode_get, transport_mode_set)
                .add_property("geometry_wkb", geometry_wkb_get, geometry_wkb_set)
                .def("cost", &Tempus::Roadmap::Step::cost)
                .def("set_cost", &Tempus::Roadmap::Step::set_cost)
                .def("costs", &Tempus::Roadmap::Step::costs, bp::return_value_policy<bp::return_by_value>())
            ;

            bp::enum_<Tempus::Roadmap::Step::StepType>("StepType")
                .value("RoadStep", Tempus::Roadmap::Step::RoadStep)
                .value("PublicTransportStep", Tempus::Roadmap::Step::PublicTransportStep)
                .value("RoadStepTransferStep", Tempus::Roadmap::Step::TransferStep)
            ;

        }


        {
            GET_SET(Tempus::Roadmap::RoadStep, Tempus::db_id_t, road_edge_id)
            GET_SET(Tempus::Roadmap::RoadStep, std::string, road_name)
            GET_SET(Tempus::Roadmap::RoadStep, double, distance_km)
            GET_SET(Tempus::Roadmap::RoadStep, Tempus::Roadmap::RoadStep::EndMovement, end_movement)

            bp::scope t = bp::class_<Tempus::Roadmap::RoadStep, bp::bases<Tempus::Roadmap::Step>>("RoadStep")
                .add_property("road_edge_id", road_edge_id_get, road_edge_id_set)
                .add_property("road_name", road_name_get, road_name_set)
                .add_property("distance_km", distance_km_get, distance_km_set)
                .add_property("end_movement", end_movement_get, end_movement_set)
            ;

            bp::enum_<Tempus::Roadmap::RoadStep::EndMovement>("EndMovement")
                .value("GoAhead", Tempus::Roadmap::RoadStep::GoAhead)
                .value("TurnLeft", Tempus::Roadmap::RoadStep::TurnLeft)
                .value("TurnRight", Tempus::Roadmap::RoadStep::TurnRight)
                .value("UTurn", Tempus::Roadmap::RoadStep::UTurn)
                .value("RoundAboutEnter", Tempus::Roadmap::RoadStep::RoundAboutEnter)
                .value("FirstExit", Tempus::Roadmap::RoadStep::FirstExit)
                .value("SecondExit", Tempus::Roadmap::RoadStep::SecondExit)
                .value("ThirdExit", Tempus::Roadmap::RoadStep::ThirdExit)
                .value("FourthExit", Tempus::Roadmap::RoadStep::FourthExit)
                .value("FifthExit", Tempus::Roadmap::RoadStep::FifthExit)
                .value("SixthExit", Tempus::Roadmap::RoadStep::SixthExit)
                .value("YouAreArrived", Tempus::Roadmap::RoadStep::YouAreArrived)
            ;
        }

        {
            GET_SET(Tempus::Roadmap::PublicTransportStep, Tempus::db_id_t, network_id)
            GET_SET(Tempus::Roadmap::PublicTransportStep, double, wait)
            GET_SET(Tempus::Roadmap::PublicTransportStep, double, departure_time)
            GET_SET(Tempus::Roadmap::PublicTransportStep, double, arrival_time)
            GET_SET(Tempus::Roadmap::PublicTransportStep, Tempus::db_id_t, trip_id)
            GET_SET(Tempus::Roadmap::PublicTransportStep, Tempus::db_id_t, departure_stop)
            GET_SET(Tempus::Roadmap::PublicTransportStep, std::string, departure_name)
            GET_SET(Tempus::Roadmap::PublicTransportStep, Tempus::db_id_t, arrival_stop)
            GET_SET(Tempus::Roadmap::PublicTransportStep, std::string, arrival_name)
            GET_SET(Tempus::Roadmap::PublicTransportStep, std::string, route)

            bp::class_<Tempus::Roadmap::PublicTransportStep, bp::bases<Tempus::Roadmap::Step>>("PublicTransportStep")
                .add_property("network_id", network_id_get, network_id_set)
                .add_property("wait", wait_get, wait_set)
                .add_property("departure_time", departure_time_get, departure_time_set)
                .add_property("arrival_time", arrival_time_get, arrival_time_set)
                .add_property("trip_id", trip_id_get, trip_id_set)
                .add_property("departure_stop", departure_stop_get, departure_stop_set)
                .add_property("departure_name", departure_name_get, departure_name_set)
                .add_property("arrival_stop", arrival_stop_get, arrival_stop_set)
                .add_property("arrival_name", arrival_name_get, arrival_name_set)
                .add_property("route", route_get, route_set)
            ;
        }

        {
            GET_SET(Tempus::Roadmap::TransferStep, Tempus::db_id_t, final_mode)
            GET_SET(Tempus::Roadmap::TransferStep, std::string, initial_name)
            GET_SET(Tempus::Roadmap::TransferStep, std::string, final_name)
            bp::class_<Tempus::Roadmap::TransferStep, bp::bases<Tempus::Roadmap::Step, Tempus::MMEdge>>("TransferStep", bp::init<const Tempus::MMVertex&, const Tempus::MMVertex&>())
                .add_property("final_mode", final_mode_get, final_mode_set)
                .add_property("initial_name", initial_name_get, initial_name_set)
                .add_property("final_name", final_name_get, final_name_set)
            ;
        }
    }


    {
        GET(Tempus::ResultElement, Tempus::Roadmap, roadmap)
        GET(Tempus::ResultElement, Tempus::Isochrone, isochrone)

        bp::class_<Tempus::ResultElement>("ResultElement")
            .def(bp::init<const Tempus::Isochrone&>())
            .def(bp::init<const Tempus::Roadmap&>())
            .def("is_roadmap", &Tempus::ResultElement::is_roadmap)
            .def("is_isochrone", &Tempus::ResultElement::is_isochrone)
            .def("roadmap", roadmap_get)
            .def("isochrone", isochrone_get)
        ;
    }

    bp::def("get_total_costs", &Tempus::get_total_costs);

    {
        GET_SET(Tempus::IsochroneValue, float, x)
        GET_SET(Tempus::IsochroneValue, float, y)
        GET_SET(Tempus::IsochroneValue, int, mode)
        GET_SET(Tempus::IsochroneValue, int, mode_changes)
        GET_SET(Tempus::IsochroneValue, int, pt_changes)
        GET_SET(Tempus::IsochroneValue, float, cost)
        GET_SET(Tempus::IsochroneValue, uint32_t, uid)
        GET_SET(Tempus::IsochroneValue, uint32_t, predecessor)
        GET_SET(Tempus::IsochroneValue, float, wait_time)
            bp::class_<Tempus::IsochroneValue>("IsochroneValue", bp::init<float, float, int, int, int, float, uint32_t, uint32_t, float>())
            .add_property("x", x_get, x_set)
            .add_property("y", y_get, y_set)
            .add_property("mode", mode_get, mode_set)
            .add_property("mode_changes", mode_changes_get, mode_changes_set)
            .add_property("pt_changes", pt_changes_get, pt_changes_set)
            .add_property("cost", cost_get, cost_set)
            .add_property("uid", uid_get, uid_set)
            .add_property("predecessor", predecessor_get, predecessor_set)
            .add_property("wait_time", wait_time_get, wait_time_set)
        ;
    }
}
