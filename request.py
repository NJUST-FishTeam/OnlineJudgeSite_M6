#Protocol-----request

class GetSubmissionRequest(object):

	def __init__(self, siteId, availableCompiler, availableValidator, dateTime):
		self.siteId = siteId
		self.dateTime = dateTime
		self.availableCompiler = availableCompiler
		self.availableValidator = availableValidator


class OnlineRequest(object):

	def __init__(self, siteId, secret, key, dateTime):
		self.siteId = siteId
		self.secret = secret
		self.key = key
		self.dateTime = dateTime


class OfflineRequest(object):

	def __init__(self, siteId, key, secret, dateTime):
		self.siteId = siteId
		self.key = key
		self.secret = secret
		self.dateTime = dateTime


class HeartbeatRequest(object):

	def __init__(
		self, siteId, cpuUsage, totalMemory, freeMemory, totalDiskSpace,
		freeDiskSpace, currentState, currentSubmissionId, dateTime):
		self.siteId = siteId
		self.cpuUsage = cpuUsage
		self.totalMemory = totalMemory
		self.freeMemory = freeMemory
		self.totalDiskSpace = totalDiskSpace
		self.freeDiskSpace = freeDiskSpace
		self.currentState = currentState
		self.currentSubmissonId = currentSubmissionId
		self.dateTime = dateTime


class UpdateResultRequest(object):

	def __init__(
		self, siteId, submissionId, judgeResult, runTime, runMemory,
		compilerOutput, coreOutput, validatorOutput, programOutput, dateTime):
		self.siteId = siteId
		self.submissionId = submissionId
		self.judgeResult = judgeResult
		self.runTime = runTime
		self.runMemory = runMemory
		self.compilerOutput = compilerOutput
		self.coreOutput = coreOutput
		self.validatorOutput = validatorOutput
		self.programOutput = programOutput
		self.dateTime =dateTime


class UpdateStateRequest(object):

	def __init__(self, siteId, submissionId, newState, dateTime):
		self.siteId = siteId
		self.submissionId = submissionId
		self.newState = newState
		self.dateTime = dateTime
