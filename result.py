class Result(object):

    def __init__(self, submissionId, runTime, runMemory, compilerOutput, status, result):
        self.submissionId = submissionId
        self.runTime = runTime
        self.runMemory = runMemory
        self.compilerOutput = compilerOutput
        self.status = status
        self.result = result


