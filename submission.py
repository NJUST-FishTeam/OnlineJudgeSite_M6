class Submission(object):

    def __init__(self, submissionId, compiler, validator, timeLimit, memoryLimit, saveOutput):
        self.submissionId = submissionId
        self.compiler = compiler
        self.validator = validator
        self.timeLimit = timeLimit
        self.memoryLimit = memoryLimit
        self.saveOutput = saveOutput


