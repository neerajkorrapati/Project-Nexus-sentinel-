class DecisionEngine:

    def decide(self, validation):

        """
        Decide whether invoice is approved.

        """

        if validation["passed"]:

            return "APPROVED"

        return "NEEDS_REVIEW"