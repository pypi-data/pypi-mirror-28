#include "common.h"
#include <tempus/request.hh>

namespace bp = boost::python;

static void request_set_destination_step( Tempus::Request& self, const Tempus::Request::Step& step )
{
    self.set_destination( step );
}

void export_Request() {
    GET_NON_CONST_SET(Tempus::Request, Tempus::db_id_t, origin)
    GET_NON_CONST_SET(Tempus::Request, Tempus::db_id_t, destination)
    GET(Tempus::Request, Tempus::Request::StepList, steps)
    GET(Tempus::Request, std::vector<Tempus::db_id_t>, allowed_modes)
    GET(Tempus::Request, std::vector<Tempus::CostId>, optimizing_criteria)

    bp::scope request = bp::class_<Tempus::Request>("Request")
        .add_property("origin", origin_get, origin_set)
        .add_property("destination", destination_get, destination_set)
        .def("set_destination_step", &request_set_destination_step)
        .add_property("steps", steps_get)
        .add_property("allowed_modes", allowed_modes_get)
        .def("add_allowed_mode", &Tempus::Request::add_allowed_mode)
        .def("optimizing_criteria", &Tempus::Request::optimizing_criteria, bp::return_value_policy<bp::copy_const_reference>())
        .def("add_intermediary_step", &Tempus::Request::add_intermediary_step)
        .def("set_optimizing_criterion", static_cast<void(Tempus::Request::*)(unsigned, const Tempus::CostId&)>(&Tempus::Request::set_optimizing_criterion))
        .def("add_criterion", &Tempus::Request::add_criterion)
    ;

    {
        bp::enum_<Tempus::Request::TimeConstraint::TimeConstraintType>("TimeConstraintType")
            .value("NoConstraint", Tempus::Request::TimeConstraint::NoConstraint)
            .value("ConstraintBefore", Tempus::Request::TimeConstraint::ConstraintBefore)
            .value("ConstraintAfter", Tempus::Request::TimeConstraint::ConstraintAfter)
        ;

        GET_SET(Tempus::Request::TimeConstraint, Tempus::Request::TimeConstraint::TimeConstraintType, type)
        GET_SET(Tempus::Request::TimeConstraint, Tempus::DateTime, date_time)
            bp::class_<Tempus::Request::TimeConstraint>("TimeConstraint")
            .def(bp::init<Tempus::Request::TimeConstraint::TimeConstraintType, Tempus::DateTime>(
                                                                                                 (bp::arg("type")=0, bp::arg("date_time")=bp::object())))
            .add_property("type", type_get, type_set)
            .add_property("date_time", date_time_get, date_time_set)
        ;
    }

    {
        GET_SET(Tempus::Request::Step, Tempus::db_id_t, location)
        GET_SET(Tempus::Request::Step, Tempus::Request::TimeConstraint, constraint)
        GET_SET(Tempus::Request::Step, bool, private_vehicule_at_destination)

            bp::class_<Tempus::Request::Step>("Step")
            .def(bp::init<Tempus::db_id_t, Tempus::Request::TimeConstraint, bool>(
                                                       (bp::arg("location")=0,
                                                        bp::arg("constraint")=Tempus::Request::TimeConstraint(),
                                                        bp::arg("private_vehicule_at_destination")=true)))
            .add_property("location",
                location_get,
                location_set)
            .add_property("constraint",
                constraint_get,
                constraint_set)
            .add_property("private_vehicule_at_destination",
                private_vehicule_at_destination_get,
                private_vehicule_at_destination_set)
        ;

    }
}
