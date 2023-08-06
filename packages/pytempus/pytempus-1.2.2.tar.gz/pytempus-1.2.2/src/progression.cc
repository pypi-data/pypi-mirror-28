#include "common.h"
#include <tempus/progression.hh>

namespace bp = boost::python;

void export_ProgressionCallback() {
    bp::class_<Tempus::ProgressionCallback>("ProgressionCallback")
        .def("__call__", &Tempus::ProgressionCallback::operator())
    ;

    bp::class_<Tempus::TextProgression, bp::bases<Tempus::ProgressionCallback>>("TextProgression", bp::init<int>())
    ;
}

