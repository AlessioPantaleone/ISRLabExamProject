import Agent
import Body
import Controller
from CsimApi.pycsim import CSim, common


def create_pioneer(api: CSim) -> Agent:
    actuators = [api.joint.with_velocity_control("Pioneer_p3dx_leftMotor"),
                 api.joint.with_velocity_control("Pioneer_p3dx_rightMotor")]
    sensors = [api.sensor.proximity("Pioneer_p3dx_ultrasonicSensor3"),
               api.sensor.proximity("Pioneer_p3dx_ultrasonicSensor6")]
    pioneer_real_body = Body.Body(sensors, actuators)

    pioneer_first_controller = Controller.Controller(pioneer_real_body)
    pioAge = Agent.Agent(pioneer_real_body, pioneer_first_controller)
    return pioAge


if __name__ == "__main__":
    with CSim.connect("127.0.0.1", 19997) as api:
        try:
            pioneer = create_pioneer(api)
        except common.NotFoundComponentError as e:
            print(e)
            print("Have you opened the right scene inside Coppelia SIM?")
            exit(-1)
