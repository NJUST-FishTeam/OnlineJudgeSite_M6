class Result(object):

    def __init__(
            self, submissionId, runTime, runMemory, programFile, programDirectory,
            actualOutputDataFile, compilerOutput, coreOutput, validatorOutput, status, result, saveOutput):
        self.submissionId = submissionId
        self.runTime = runTime
        self.runMemory = runMemory
        self.programFile = programFile
        self.programDirectory = programDirectory
        self.actualOutputDataFile = actualOutputDataFile
        self.compilerOutput = compilerOutput
        self.coreOutput = coreOutput
        self.validatotOutput = validatorOutput
        self.status = status
        self.result = result
        self.saveOutput = saveOutput


