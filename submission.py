class Submission(object):

    def __init__(self, submissionId, compiler, validator, sourceCodeFile,
            sourceCodeDirectory, inputDataFile, expectedOutputDataFile, timeLimit, memoryLimit, saveOutput):
        self.submissionId = submissionId
        self.compiler = compiler
        self.validator = validator
        self.sourceCodeFile = sourceCodeFile
        self.sourceCodeDirectory = sourceCodeDirectory
        self.inputDataFile = inputDataFile
        self.expectedOutputDataFile = expectedOutputDataFile
        self.timeLimit = timeLimit
        self.memoryLimit = memoryLimit
        self.saveOutput = saveOutput


