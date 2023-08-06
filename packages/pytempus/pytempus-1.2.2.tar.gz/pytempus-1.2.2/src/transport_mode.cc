#include "common.h"
#include <tempus/transport_modes.hh>

namespace bp = boost::python;

void export_TransportMode() {
    bp::enum_<Tempus::TransportModeEngine>("TransportModeEngine")
        .value("EnginePetrol", Tempus::TransportModeEngine::EnginePetrol)
        .value("EngineGasoil", Tempus::TransportModeEngine::EngineGasoil)
        .value("EngineLPG", Tempus::TransportModeEngine::EngineLPG)
        .value("EngineElectricCar", Tempus::TransportModeEngine::EngineElectricCar)
        .value("EngineElectricCycle", Tempus::TransportModeEngine::EngineElectricCycle)
    ;

    bp::enum_<Tempus::TransportModeId>("TransportModeId")
        .value("TransportModeWalking", Tempus::TransportModeId::TransportModeWalking)
        .value("TransportModePrivateBicycle", Tempus::TransportModeId::TransportModePrivateBicycle)
        .value("TransportModePrivateCar", Tempus::TransportModeId::TransportModePrivateCar)
        .value("TransportModeTaxi", Tempus::TransportModeId::TransportModeTaxi)
    ;

    bp::enum_<Tempus::TransportModeTrafficRule>("TransportModeTrafficRule")
        .value("TrafficRulePedestrian", Tempus::TransportModeTrafficRule::TrafficRulePedestrian)
        .value("TrafficRuleBicycle", Tempus::TransportModeTrafficRule::TrafficRuleBicycle)
        .value("TrafficRuleCar", Tempus::TransportModeTrafficRule::TrafficRuleCar)
        .value("TrafficRuleTaxi", Tempus::TransportModeTrafficRule::TrafficRuleTaxi)
        .value("TrafficRuleCarPool", Tempus::TransportModeTrafficRule::TrafficRuleCarPool)
        .value("TrafficRuleTruck", Tempus::TransportModeTrafficRule::TrafficRuleTruck)
        .value("TrafficRuleCoach", Tempus::TransportModeTrafficRule::TrafficRuleCoach)
        .value("TrafficRulePublicTransport", Tempus::TransportModeTrafficRule::TrafficRulePublicTransport)
    ;

    bp::enum_<Tempus::TransportModeSpeedRule>("TransportModeSpeedRule")
        .value("SpeedRulePedestrian", Tempus::TransportModeSpeedRule::SpeedRulePedestrian)
        .value("SpeedRuleBicycle", Tempus::TransportModeSpeedRule::SpeedRuleBicycle)
        .value("SpeedRuleElectricCycle", Tempus::TransportModeSpeedRule::SpeedRuleElectricCycle)
        .value("SpeedRuleRollerSkate", Tempus::TransportModeSpeedRule::SpeedRuleRollerSkate)
        .value("SpeedRuleCar", Tempus::TransportModeSpeedRule::SpeedRuleCar)
        .value("SpeedRuleTruck", Tempus::TransportModeSpeedRule::SpeedRuleTruck)
    ;

    bp::enum_<Tempus::TransportModeTollRule>("TransportModeTollRule")
        .value("TollRuleLightVehicule", Tempus::TransportModeTollRule::TollRuleLightVehicule)
        .value("TollRuleIntermediateVehicule", Tempus::TransportModeTollRule::TollRuleIntermediateVehicule)
        .value("TollRule2Axles", Tempus::TransportModeTollRule::TollRule2Axles)
        .value("TollRule3Axles", Tempus::TransportModeTollRule::TollRule3Axles)
        .value("TollRuleMotorcycles", Tempus::TransportModeTollRule::TollRuleMotorcycles)
    ;

    bp::enum_<Tempus::TransportModeRouteType>("TransportModeRouteType")
        .value("RouteTypeTram", Tempus::TransportModeRouteType::RouteTypeTram)
        .value("RouteTypeSubway", Tempus::TransportModeRouteType::RouteTypeSubway)
        .value("RouteTypeRail", Tempus::TransportModeRouteType::RouteTypeRail)
        .value("RouteTypeBus", Tempus::TransportModeRouteType::RouteTypeBus)
        .value("RouteTypeFerry", Tempus::TransportModeRouteType::RouteTypeFerry)
        .value("RouteTypeCableCar", Tempus::TransportModeRouteType::RouteTypeCableCar)
        .value("RouteTypeSuspendedCar", Tempus::TransportModeRouteType::RouteTypeSuspendedCar)
        .value("RouteTypeFunicular", Tempus::TransportModeRouteType::RouteTypeFunicular)
    ;

    GET_SET(Tempus::TransportMode, std::string, name)
    GET_SET(Tempus::TransportMode, bool, is_public_transport)
    GET_SET(Tempus::TransportMode, Tempus::TransportModeSpeedRule, speed_rule);
    GET_SET(Tempus::TransportMode, unsigned, toll_rules);
    GET_SET(Tempus::TransportMode, Tempus::TransportModeEngine, engine_type);
    GET_SET(Tempus::TransportMode, Tempus::TransportModeRouteType, route_type);
    bp::class_<Tempus::TransportMode, bp::bases<Tempus::Base>>("TransportMode")
        .add_property("name", name_get, name_set)
        .add_property("is_public_transport", is_public_transport_get, is_public_transport_set)
        .add_property("speed_rule", speed_rule_get, speed_rule_set)
        .add_property("toll_rules", toll_rules_get, toll_rules_set)
        .add_property("engine_type", engine_type_get, engine_type_set)
        .add_property("route_type", route_type_get, route_type_set)
        .add_property("need_parking", &Tempus::TransportMode::need_parking, static_cast<void (Tempus::TransportMode::*)(const bool&)>(&Tempus::TransportMode::set_need_parking))
        .add_property("is_shared", &Tempus::TransportMode::is_shared, static_cast<void (Tempus::TransportMode::*)(const bool&)>(&Tempus::TransportMode::set_is_shared))
        .add_property("must_be_returned", &Tempus::TransportMode::must_be_returned, static_cast<void (Tempus::TransportMode::*)(const bool&)>(&Tempus::TransportMode::set_must_be_returned))
        .add_property("traffic_rules", &Tempus::TransportMode::traffic_rules, &Tempus::TransportMode::set_traffic_rules)
    ;
}
