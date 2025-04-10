
class RankingAgent:
    def rank(self, ideas):
        return sorted(ideas, key=lambda x: len(x))
