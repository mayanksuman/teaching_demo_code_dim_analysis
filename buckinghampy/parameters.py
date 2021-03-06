""" A set of common physical parameters and their SI units """

from .nondimensional import Parameter

# SI base parameters
mass = Parameter("M", {"kg": 1})
length = Parameter("L", {"m": 1})
temperature = Parameter("\\Theta", {"K": 1})
time = Parameter("T", {"s": 1})
electric_current = Parameter("I", {"A": 1})
luminous_intensity = Parameter("J", {"cd": 1})
amount_substance = Parameter("N", {"mol": 1})

# Some parameters used in physics
velocity = Parameter("V", {"m": 1, "s": -1})
acceleration = Parameter("a", {"m": 1, "s": -2})
density = Parameter(u"\\rho", {"kg": 1, "m": -3})
volume = Parameter(u'V\\llap{--}', {"m": 3})
area = Parameter('A', {"m": 2})
head = Parameter("h", {"m": 1})
angle = Parameter('\\theta', {})
surface_tension = Parameter("\\sigma", {"N":1, "m":-1})
stress = Parameter("\\sigma_s", {"N": 1, "m": -2})
viscosity = Parameter("\\mu", {"kg": 1, "m": -1, "s": -1})
kinematic_viscosity = Parameter("\\nu", {"m": 2, "s": -1})
thermal_expansivity = Parameter("\\alpha", {"K": -1})
thermal_conductivity = Parameter("k", {"kg": 1, "m": 1, "s": -3, "K": -1})
hydraulic_permeability = Parameter("\\kappa", {"m": 2})
hydraulic_conductivity = Parameter("K", {"m": 1, "s": -1})
thermal_diffusivity = Parameter("\\kappa", {"m": 2, "s": -1})
gravity_acceleration = acceleration.copy()
gravity_acceleration.symbol = 'g'
gravity = gravity_acceleration.copy()
rotation_rate = Parameter("\\Omega", {"s": -1})
specific_heat = Parameter("c", {"m": 2, "s": -2, "K": -1})
heat_capacity = specific_heat.copy()
pressure = stress.copy()
pressure.symbol = "P"
discharge = Parameter("Q", {"m": 3, "s": -1})
bulk_modulus = Parameter("K", {"kg": 1, "m": -1, "s": -2})
compressibility = Parameter("\\xi", {"kg": -1, "m": 1, "s": 2})
debye_temperature = Parameter("\\Theta_{D}", {"K": 1})
einstein_temperature = Parameter("\\Theta_{E}", {"K": 1})
decay_time = Parameter("\\tau", {"s": 1})
speed_of_light = Parameter("c", {"m": 1, "s": -1})
wavelength = Parameter("\\lambda", {"m": -1})
frequency = Parameter("\\nu", {"s": -1})
planck = Parameter("h", {"m": 2, "kg": 1, "s": -1})
boltzmann = Parameter("k_{B}", {"m": 2, "kg": 1, "K": -1, "s": -2})
current = electric_current.copy()
charge = Parameter("q", {"A": 1, "s": 1})
charge_density = Parameter("\\rho_c", {"A": 1, "s": -1, "m": -3})
electrical_conductivity = Parameter("C_e", {'S': 1})
electrical_resistivity = Parameter("R", {"\\ohm": 1})
voltage = Parameter("V", {"kg": 1, "m": 2, "s": -3, "A": -1})
magnetic_permeability = Parameter("\\mu", {"kg": 1, "m": 1, "s": -2, "A": -2})
magnetic_diffusivity = Parameter("\\eta_m", {"m": 2, "s": -1})
