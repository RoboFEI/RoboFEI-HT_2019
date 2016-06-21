#The recipe gives simple implementation of a Discrete Proportional-Integral-Derivative (PID) controller. PID controller gives output value for error between desired reference input and measurement feedback to minimize error value.
#More information: http://en.wikipedia.org/wiki/PID_controller
#
#cnr437@gmail.com
#
#######	Example	#########
#
#p=PID(3.0,0.4,1.2)
#p.setPoint(5.0)
#while True:
#     pid = p.update(measurement_value)
#
#

""" Describes the PID class - A discrete PID control for object tracking (Following Object)"""

class PID:

	"""Initial conditions for PID"""
	def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):
		""" Initial Porportional Gain = 2"""	
		self.Kp=P
		""" Initial Integrative Gain = 0.0"""			
		self.Ki=I
		""" Initial Derivative Gain = 1.0"""			
		self.Kd=D
		"""	Initial Derivator = 0"""
		self.Derivator=Derivator
		"""	Initial Integrator = 0"""
		self.Integrator=Integrator
		"""	Initial maximum value fpr integrator = 500"""
		self.Integrator_max=Integrator_max
		"""	Initial minimum value fpr integrator = -500"""
		self.Integrator_min=Integrator_min
		"""	Defines Set_Point to 0.0"""
		self.set_point=0.0
		"""	Defines Goal Error to 0.0"""
		self.error=0.0

		""" Calculate PID output value for given reference input and feedback"""
	def update(self,current_value):

		"""	Current error is Set_Point minus the current error position"""
		self.error = self.set_point - current_value
		""" Update the proportional value. Proportional Gain times current error"""
		self.P_value = self.Kp * self.error
		""" Update the derivator value. Derivative Gain times current error minus derivator"""
		self.D_value = self.Kd * ( self.error - self.Derivator)
		""" Update the derivator. Derivator gets error"""
		self.Derivator = self.error
		""" Update the integrator, Current Integrator plus current error"""
		self.Integrator = self.Integrator + self.error

		""" Checks if the integrator exceeds maximum value"""
		if self.Integrator > self.Integrator_max:
			""" If exceeds integrator gets maximum value"""
			self.Integrator = self.Integrator_max
			""" Checks if the integrator exceeds minimum value"""
		elif self.Integrator < self.Integrator_min:
			""" If exceeds integrator gets minimum value"""
			self.Integrator = self.Integrator_min
			
		""" I_value gets current integrator times Integrative Gain"""
		self.I_value = self.Integrator * self.Ki
		""" PID error gets the sum of all errors (Proportional, Derivative and Integrative)"""
		PID = self.P_value + self.I_value + self.D_value
		"""Return Error"""
		return PID

	"""	Initilize the setpoint of PID """
	def setPoint(self,set_point):
		""" Defines SetPoint"""
		self.set_point = set_point
		"""	Defines Integrator = 0"""
		self.Integrator=0
		"""	Defines Derivator = 0"""
		self.Derivator=0
		
		"""	Set integrator """
	def setIntegrator(self, Integrator):
		"""	Defines Integrator"""
		self.Integrator = Integrator
	"""	Set Derivator """
	def setDerivator(self, Derivator):
		"""	Defines Derivator"""
		self.Derivator = Derivator
	""" Set Proportional Gain Kp"""
	def setKp(self,P):
		"""	Defines Kp"""
		self.Kp=P
	""" Set Integrative Gain Ki"""
	def setKi(self,I):
		"""	Defines Ki"""
		self.Ki=I
	""" Set Derivative Gain Kd"""
	def setKd(self,D):
		"""	Defines Kd"""
		self.Kd=D
	""" Get goal point"""
	def getPoint(self):
		""" Returns Set Point """
		return self.set_point
	""" Gets error """
	def getError(self):
		""" Returns Error"""
		return self.error
	""" Get integrator """
	def getIntegrator(self):
		""" Returns Integrator """
		return self.Integrator
	""" Get derivator """
	def getDerivator(self):
		""" Returns Derivator """
		return self.Derivator

