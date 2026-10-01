import json
import os
from typing import List, Dict
from duckduckgo_search import DDGS

class KnowledgeBaseTool:
    """
    ENTERPRISE HYBRID KNOWLEDGE BASE TOOL
    - Searches Local Corporate KB for internal SOPs.
    - Automatically falls back to Live Internet Web Search for unlimited IT troubleshooting.
    """
    def __init__(self):
        self.articles = self._load_kb()
        
    def _load_kb(self) -> List[Dict]:
        kb_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge_base.json')
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                return json.load(f).get("articles", [])
        except Exception:
            return []

    def search(self, query: str, category: str = "") -> List[Dict]:
        """
        Step 1: Search Local KB.
        Step 2: If no strong match, search Live Internet via DuckDuckGo.
        """
        results = []
        q_lower = query.lower()
        q_words = [w for w in q_lower.split() if len(w) > 3]

        # 1. Local KB Matching
        for article in self.articles:
            score = 0
            if category and article.get("category", "").lower() == category.lower():
                score += 8
            for tag in article.get("tags", []):
                if tag.lower() in q_lower:
                    score += 4
            for word in q_words:
                if word in article.get("title", "").lower():
                    score += 3
                if word in article.get("problem", "").lower():
                    score += 2
                    
            if score >= 6: # Strong local match threshold
                results.append({
                    **article,
                    "source": "Internal Corporate KB",
                    "relevance_score": score
                })

        # Sort local results
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

        # 2. Live Web Search Fallback (If local results are weak or empty)
        if len(results) == 0 or results[0].get("relevance_score", 0) < 10:
            web_results = self._live_web_search(query)
            results.extend(web_results)

        return results[:3]

    def _live_web_search(self, query: str) -> List[Dict]:
        """Searches live technical documentation and IT forums on the web"""
        try:
            search_query = f"{query} IT troubleshooting fix guide"
            ddgs = DDGS()
            raw_results = list(ddgs.text(search_query, max_results=3))
            
            web_articles = []
            for i, r in enumerate(raw_results):
                web_articles.append({
                    "article_id": f"WEB-SRC-{i+1}",
                    "title": r.get("title", "Online Technical Advisory"),
                    "category": "web_intelligence",
                    "problem": query,
                    "solution": r.get("body", "Follow the latest vendor troubleshooting documentation."),
                    "steps": [
                        f"Review live advisory from {r.get('href', 'source')}",
                        "Apply recommended configuration patch or parameter update.",
                        "Verify service functionality after patch."
                    ],
                    "tags": ["web_search", "live_data", "vendor_docs"],
                    "source": f"Live Web ({r.get('href', 'Internet')})",
                    "relevance_score": 9.5
                })
            return web_articles
        except Exception as e:
            # Fallback if network issue
            return [{
                "article_id": "WEB-FALLBACK",
                "title": "General System Remediation",
                "category": "general",
                "problem": query,
                "solution": "Standard diagnostic isolation and service restart procedure.",
                "steps": ["Inspect system error logs.", "Verify network endpoints.", "Restart relevant daemon."],
                "tags": ["fallback"],
                "source": "Heuristic Engine",
                "relevance_score": 5.0
            }]