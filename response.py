# Protocol-------response

class OnlineResponse(object):

    def __init__(self, siteId, accepted, dateTime):
        self.siteId = siteId
        self.accepted = accepted
        self.dateTime = dateTime


class OfflineResponse(object):

    def __init__(self, siteId, accepted, dateTime):
        self.siteId = siteId
        self.accepted = accepted
        self.dateTime = dateTime


class GetSubmissionResponse(object):

    def __init__(
            self, siteId, valid, submissionId, sourceCode, validator,
            compiler, testDataId, inputMd5, outputMd5, timeLimit,
            memoryLimit, keepOutput, dateTime, spjMd5, spj_type):
        self.siteId = siteId
        self.valid = valid
        self.submissionId = submissionId
        self.sourceCode = sourceCode
        self.compiler = compiler
        self.validator = validator
        self.testDataId = testDataId
        self.inputMd5 = inputMd5
        self.outputMd5 = outputMd5
        self.timeLimit = timeLimit
        self.memoryLimit = memoryLimit
        self.keepOutput = keepOutput
        self.dateTime = dateTime
        self.spjMd5 = spjMd5
        self.spj_type = spj_type


class HeartbeatResponse(object):

    def __init__(self, siteId, accepted, dateTime):
        self.siteId = siteId
        self.accepted = accepted
        self, dateTime = dateTime


class UpdateResultResponse(object):

    def __init__(self, siteId, submissionId, accepted, dateTime):
        self.siteId = siteId
        self.submissonId = submissionId
        self.accepted = accepted
        self.dateTime = dateTime


class UpdateStateResponse(object):

    def __init__(self, siteId, submissionId, accepted, dateTime):
        self.siteId = siteId
        self.submissionId = submissionId
        self.accepted = accepted
        self.dateTime = dateTime
