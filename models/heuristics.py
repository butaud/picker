class Heuristic:
    weight = 1

    def calc_score(self, data):
        return self._calc_unweighted_score(data) * self.weight

    def _calc_unweighted_score(self, data):
        pass