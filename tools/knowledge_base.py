import json, os
class KnowledgeBaseTool:
    def __init__(self):
        p = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge_base.json')
        with open(p, 'r', encoding='utf-8') as f:
            self.articles = json.load(f).get('articles', [])
    def search(self, query, category=''):
        res = []
        q = query.lower()
        for a in self.articles:
            score = 0
            if category and a.get('category','').lower() == category.lower(): score += 10
            for tag in a.get('tags', []):
                if tag.lower() in q: score += 5
            if score > 0: res.append({**a, 'relevance_score': score})
        res.sort(key=lambda x: x['relevance_score'], reverse=True)
        return res[:3]
