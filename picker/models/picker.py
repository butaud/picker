import time

class Picker:
    def __init__(self, generator, constraints, heuristics):
        self.generator = generator
        self.constraints = constraints
        self.heuristics = heuristics

        self.output_func = None
        self.max_time_to_search_millis = 10000
        self.choices_to_compare = 5 * len(self.heuristics)
        self.start = 0.0
    
    def pick(self):
        self.start = time.time()
        choices = []

        self._output("Searching for up to " + str(self.choices_to_compare) + " possibilities")
        while self._should_keep_going(choices):
            possibility = self.generator.generate()
            
            if self._meets_constraints(possibility):
                choices.append(possibility)
                self._output("Found possibility #" + str(len(choices)))
        
        if len(choices) == 0:
            self._output("Could not find any choices within the time limit.")
            return None
        
        return sorted(choices, key=self._score_possibility, reverse=True)[0]
    
    def _output(self, message):
        if self.output_func is not None:
            self.output_func(message)

    def _should_keep_going(self, choices):
        return (len(choices) < self.choices_to_compare) and (time.time() - self.start < self.max_time_to_search_millis)
    
    def _meets_constraints(self, possibility):
        for constraint in self.constraints:
            if not constraint.is_met(possibility):
                return False
        return True
    
    def _score_possibility(self, possibility):
        score = 0
        for heuristic in self.heuristics:
            score += heuristic.calc_score(possibility)
        return score
    
    def _swallow(self, message):
        pass