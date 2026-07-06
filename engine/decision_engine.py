class DecisionEngine:

    def decide(self, validation):

        if validation["passed"]:

            return "APPROVED"

        return "NEEDS REVIEW"