
from .generation_agent import GenerationAgent
from .reflection_agent import ReflectionAgent
from .ranking_agent import RankingAgent
from .evolution_agent import EvolutionAgent
from .proximity_agent import ProximityAgent
from .meta_review_agent import MetaReviewAgent

class SupervisorAgent:
    def __init__(self):
        self.gen = GenerationAgent()
        self.ref = ReflectionAgent()
        self.rank = RankingAgent()
        self.evo = EvolutionAgent()
        self.prox = ProximityAgent()
        self.meta = MetaReviewAgent()

    def handle_query(self, query):
        ideas = self.gen.generate_ideas(query)
        refined = self.ref.reflect(ideas)
        ranked = self.rank.rank(refined)
        evolved = self.evo.evolve(ranked)
        related = [self.prox.find_related(i) for i in evolved]
        meta_review = self.meta.review(evolved)
        return {
            "original_ideas": ideas,
            "refined": refined,
            "ranked": ranked,
            "evolved": evolved,
            "related": related,
            "review": meta_review
        }
