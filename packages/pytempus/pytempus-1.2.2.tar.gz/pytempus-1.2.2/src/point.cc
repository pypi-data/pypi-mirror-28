#include "common.h"
#include <tempus/point.hh>

namespace bp = boost::python;

void export_Point() {
    {
        GET_SET(Tempus::Point2D, float, x)
        GET_SET(Tempus::Point2D, float, y)
        bp::class_<Tempus::Point2D>("Point2D")
            .def(bp::init<float, float>())
            .add_property("x",x_get, x_set)
            .add_property("y",y_get, y_set)
        ;
    }
    {
        GET_SET(Tempus::Point3D, float, x)
        GET_SET(Tempus::Point3D, float, y)
        GET_SET(Tempus::Point3D, float, z)
        bp::class_<Tempus::Point3D>("Point3D")
            .def(bp::init<float, float, float>())
            .add_property("x",x_get, x_set)
            .add_property("y",y_get, y_set)
            .add_property("z",z_get, z_set)
        ;
    }

    float (*dist_2d)(const Tempus::Point2D&, const Tempus::Point2D&) = &Tempus::distance;
    float (*dist_3d)(const Tempus::Point3D&, const Tempus::Point3D&) = &Tempus::distance;
    float (*dist2_2d)(const Tempus::Point2D&, const Tempus::Point2D&) = &Tempus::distance2;
    float (*dist2_3d)(const Tempus::Point3D&, const Tempus::Point3D&) = &Tempus::distance2;

    bp::def("distance", dist_2d);
    bp::def("distance", dist_3d);
    bp::def("distance2", dist2_2d);
    bp::def("distance2", dist2_3d);
}
