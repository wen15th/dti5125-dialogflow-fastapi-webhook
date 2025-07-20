# app/services/rag/rag_service.py
# SIMPLIFIED VERSION - No complex scoring, no strict filtering

from dotenv import load_dotenv
load_dotenv()

import os
import json
from typing import Dict, List, Optional
import logging
from pathlib import Path

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.schema import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PainCaretipManager:
    def __init__(self):
        self.pain_care_tips = {
            "educational": {
                "rating_range": [1, 2],
                "tip": "I'm glad you've been able to manage your pain. Exercising regularly and making sure to get adequate nutrition can go a long way when regulating pain.\n\nMeditating can be a good substitution if you are in too much pain to exercise.",
                "tone": "gentle_encouragement",
                "focus": "maintenance_and_prevention"
            },
            "basic_care": {
                "rating_range": [3],
                "tip": "Warm packs may help control your pain. However, avoid electric heating pads as they can cause burns with prolonged use.\n\nIf your pain is due to acute injury, consider using a cold pack instead to reduce pain and swelling. This should typically not be done for > 20 minutes.",
                "tone": "practical_supportive",
                "focus": "immediate_relief_strategies"
            },
            "advanced_care": {
                "rating_range": [4],
                "tip": "Try using the journal as a 'pain log' to note when the pain happens, where it is, and what it feels like. Also, write down what has or hasn't helped ease the pain. This can help you better understand what might be causing it.\n\nSharing this with your healthcare providers can help them identify and treat your pain more accurately.",
                "tone": "solution_focused",
                "focus": "tracking_and_healthcare_collaboration"
            },
            "escalation": {
                "rating_range": [5],
                "tip": "I recommend you speak to your doctor or your nurse about the pain you are experiencing.\n\nThey can help you find the underlying cause of your pain.",
                "tone": "calm_professional",
                "focus": "healthcare_provider_consultation"
            }
        }

    def get_pain_care_tip(self, rating: int) -> Dict:
        for care_level, care_data in self.pain_care_tips.items():
            if rating in care_data["rating_range"]:
                return {
                    "symptom": "pain",
                    "rating": rating,
                    "care_level": care_level,
                    "tip": care_data["tip"],
                    "tone": care_data["tone"],
                    "focus": care_data["focus"],
                    "source": f"predefined_{care_level}",
                    "escalation_needed": (care_level == "escalation")
                }
        
        return {
            "symptom": "pain",
            "rating": rating,
            "care_level": "general",
            "tip": f"For a pain severity rating of {rating}, please monitor your symptoms and consult with your healthcare provider for personalized advice.",
            "tone": "calm_professional",
            "focus": "general_monitoring",
            "source": "fallback",
            "escalation_needed": (rating == 5)
        }


class SimplifiedPainFocusedRAGRetriever:
    """SIMPLIFIED: No complex scoring, minimal filtering"""

    def __init__(self, vector_store):
        self.vector_store = vector_store
        
        # Your improved severity-specific queries
        self.severity_queries = {
    1: [
        "pain", "ache", "discomfort", "soreness", "distress",
        "exercise", "physical activity", "workout", "training", "yoga","mindful", 
        "meditation", "mindfulness", "contemplation", "introspection", "concentration",
        "nutrition", "dietary habits", "nourishment", "healthy eating", "balanced diet"
    ],
    2: [
        "pain", "ache", "discomfort", "soreness", "distress",
        "exercise", "physical activity", "workout", "training", "exertion",
        "meditation", "mindfulness", "contemplation", "introspection", "concentration",
        "nutrition", "dietary habits", "nourishment", "healthy eating", "balanced diet"
    ],
    3: [
        "pain", "ache", "discomfort", "soreness", "distress",
        "pain relief", "pain alleviation", "analgesia", "soothing", "comfort",
        "pain therapy", "pain management", "therapeutic intervention", "pain treatment",
        "managing pain", "pain control", "pain coping strategies", "pain self-care",
        "pain treatment care tips", "pain care advice", "pain relief guidelines", "pain management tips"
    ],
    4: [
        "pain", "ache", "discomfort", "soreness", "distress",
        "chronic pain", "persistent pain", "long-term pain", "chronic pain syndrome",
        "tracking", "monitoring", "logging", "documenting", "recording", "pain medication",
        "healthcare collaboration", "clinical teamwork", "coordinated care", "multidisciplinary care",
        "pain treatment care tips", "pain care advice", "pain relief guidelines", "pain management tips"
    ],
    5: [
        "pain", "ache", "discomfort", "soreness", "distress",
        "severe pain", "intense pain", "acute pain", "excruciating pain", "pain medication",
        "pain medication", "pain relievers", "analgesics", "pharmacologic pain treatment", "pain meds",
        "urgent pain management", "emergency pain relief", "rapid analgesia", "immediate pain control",
        "healthcare pain consultation", "clinical pain evaluation", "pain specialist consultation"
    ]
}

    def _is_web_article(self, metadata) -> bool:
        """SIMPLIFIED: Basic web article check"""
        content_type = metadata.get('content_type', '')
        media_url = metadata.get('media_url', '')
        
        # Simple check: web_page type and no media URL
        return content_type == 'web_page' and not media_url

    def _is_media_content(self, metadata) -> bool:
        """Check if content is media"""
        content_type = metadata.get('content_type', '')
        media_url = metadata.get('media_url', '')
        return content_type in ['video', 'podcast'] or bool(media_url)

    def search_web_articles(self, severity: int, k: int = 2) -> List[Document]:
        """SIMPLIFIED: Web article search with minimal filtering"""
        try:
            queries = self.severity_queries.get(severity, ["pain"])
            all_articles = []
            seen_urls = set()
            
            logger.info(f"Searching web articles for severity {severity}")
            
            for query in queries:
                try:
                    # Get search results
                    results = self.vector_store.similarity_search(query, k=k*5)
                    
                    for doc in results:
                        url = doc.metadata.get('source_url', '')
                        if url in seen_urls:
                            continue
                        
                        # SIMPLIFIED: Only check if it's a web article
                        if self._is_web_article(doc.metadata):
                            doc.metadata['query_source'] = query
                            all_articles.append(doc)
                            seen_urls.add(url)
                            
                            title = doc.metadata.get('title', 'No title')
                            org = doc.metadata.get('organization', 'Unknown')
                            logger.info(f"Found article: [{org}] {title[:50]}...")
                            
                            if len(all_articles) >= k*3:
                                break
                    
                except Exception as e:
                    logger.warning(f"Query '{query}' failed: {e}")
                    continue
                
                if len(all_articles) >= k*3:
                    break
            
            # If no results with specific queries, try basic fallback
            if len(all_articles) == 0:
                logger.info("No articles found with specific queries, trying basic search...")
                try:
                    basic_results = self.vector_store.similarity_search("parkinson", k=k*10)
                    
                    for doc in basic_results:
                        url = doc.metadata.get('source_url', '')
                        if url in seen_urls:
                            continue
                        
                        if self._is_web_article(doc.metadata):
                            doc.metadata['query_source'] = "fallback_parkinson"
                            all_articles.append(doc)
                            seen_urls.add(url)
                            
                            if len(all_articles) >= k*2:
                                break
                                
                except Exception as e:
                    logger.warning(f"Fallback search failed: {e}")
            
            # Select diverse organizations
            final_articles = []
            used_orgs = set()
            
            # First pass: different organizations
            for doc in all_articles:
                org = doc.metadata.get('organization', 'Unknown')
                if org not in used_orgs and len(final_articles) < k:
                    final_articles.append(doc)
                    used_orgs.add(org)
                    logger.info(f"Selected article from {org}: {doc.metadata.get('title', 'No title')[:50]}")
            
            # Second pass: fill remaining slots
            for doc in all_articles:
                if len(final_articles) >= k:
                    break
                if doc not in final_articles:
                    final_articles.append(doc)
            
            logger.info(f"Final articles for severity {severity}: {len(final_articles)}")
            return final_articles[:k]
            
        except Exception as e:
            logger.error(f"Error searching web articles: {e}")
            return []

    def search_media_resources(self, severity: int, k: int = 2) -> List[Dict]:
        """SIMPLIFIED: Media search"""
        try:
            queries = self.severity_queries.get(severity, ["pain"])
            all_media = []
            seen_media_urls = set()
            
            logger.info(f"Searching media for severity {severity}")
            
            for query in queries:
                try:
                    # Add media-specific terms
                    media_query = f"{query} video podcast"
                    results = self.vector_store.similarity_search(media_query, k=k*5)
                    
                    for doc in results:
                        if not self._is_media_content(doc.metadata):
                            continue
                        
                        media_url = doc.metadata.get('media_url', '')
                        if not media_url or media_url in seen_media_urls:
                            continue
                        
                        media_info = {
                            'type': doc.metadata.get('content_type', 'video'),
                            'title': doc.metadata.get('title', 'Unknown'),
                            'organization': doc.metadata.get('organization', 'Unknown'),
                            'media_url': media_url,
                            'source_url': doc.metadata.get('source_url', ''),
                            'description': doc.metadata.get('description', ''),
                            'duration': doc.metadata.get('duration', ''),
                            'content_preview': doc.page_content[:200] + "..." if doc.page_content else ""
                        }
                        all_media.append(media_info)
                        seen_media_urls.add(media_url)
                        
                        logger.info(f"Found media: {media_info['title'][:40]} from {media_info['organization']}")
                        
                        if len(all_media) >= k*3:
                            break
                    
                except Exception as e:
                    logger.warning(f"Media query '{query}' failed: {e}")
                    continue
                
                if len(all_media) >= k*3:
                    break
            
            # Select diverse media
            final_media = []
            used_orgs = set()
            
            for media in all_media:
                org = media.get('organization', 'Unknown')
                if org not in used_orgs and len(final_media) < k:
                    final_media.append(media)
                    used_orgs.add(org)
                elif len(final_media) < k:
                    final_media.append(media)
            
            logger.info(f"Final media for severity {severity}: {len(final_media)}")
            return final_media[:k]
            
        except Exception as e:
            logger.error(f"Error searching media resources: {e}")
            return []


class EnhancedPainFocusedCareRAG:
    """RAG system with simplified filtering"""

    def __init__(self, chromadb_path: str, google_api_key: str):
        self.chromadb_path = chromadb_path
        self.google_api_key = google_api_key
        self.pain_care_manager = PainCaretipManager()
        self._initialize_system()

    def _initialize_system(self):
        try:
            os.environ["GOOGLE_API_KEY"] = self.google_api_key
            
            embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            self.vector_store = Chroma(
                collection_name="parkinsons_complete_kb",
                embedding_function=embedding_function,
                persist_directory=self.chromadb_path
            )
            
            # Use SIMPLIFIED retriever
            self.retriever = SimplifiedPainFocusedRAGRetriever(self.vector_store)
            
            self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
            self.prompt_template = self._create_enhanced_pain_prompt_template()
            
            logger.info("Enhanced pain-focused RAG system initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize enhanced pain-focused RAG system: {str(e)}")
            raise

    def _create_enhanced_pain_prompt_template(self):
        system_template = """You are a specialized Parkinson's disease pain management assistant. Provide additional guidance that complements the predefined pain care tip.

Use the pain-specific knowledge base context to add NEW information not already mentioned in the predefined tip.

TONE MATCHING - Match the exact tone:
- gentle_encouragement: "Research shows gentle approaches...", "Studies indicate..."
- practical_supportive: "Pain specialists recommend...", "Evidence-based techniques include..."
- solution_focused: "Pain management research suggests...", "Clinical studies show..."
- calm_professional: "Medical literature indicates...", "Pain experts advise..."

FOCUS: {focus_area}

Pain-Specific Knowledge Base Context:
{context}

Predefined Pain Care Tip:
{care_tip}"""

        human_template = """I have pain severity {rating}/5. Add evidence-based guidance from the knowledge base that complements the predefined tip without repeating it."""

        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template(human_template)
        ])

    def get_refined_tip_with_rag(self, severity_score: int, symptom: str, user_id: str = "default") -> Dict:
        """Main function with simplified filtering"""
        try:
            logger.info(f"Processing {symptom} with severity {severity_score}")
            
            if symptom != "pain":
                return self._fallback_for_non_pain(severity_score, symptom, user_id)
            
            # Get predefined tip
            care_tip_data = self.pain_care_manager.get_pain_care_tip(severity_score)

            # Get SEPARATE web articles and media
            # web_articles = self.retriever.search_web_articles(severity_score, k=3)
            web_articles = []
            media_resources = self.retriever.search_media_resources(severity_score, k=2)

            logger.info(f"Retrieved {len(web_articles)} articles, {len(media_resources)} media for severity {severity_score}")

            # Create context from articles only
            if web_articles:
                context_parts = []
                for doc in web_articles:
                    org = doc.metadata.get('organization', 'Unknown')
                    title = doc.metadata.get('title', 'Unknown')
                    
                    content_preview = doc.page_content[:600]
                    context_parts.append(f"Source: {org} - {title}\n{content_preview}...")
                
                context = "\n\n".join(context_parts)
            else:
                context = "Limited pain-specific information available."

            # Generate AI response
            formatted_prompt = self.prompt_template.format_messages(
                context=context,
                care_tip=care_tip_data['tip'],
                rating=severity_score,
                focus_area=care_tip_data.get('focus', 'pain_management')
            )

            ai_response = self.llm.invoke(formatted_prompt)

            # Format sources (articles only)
            sources = []
            for doc in web_articles:
                sources.append({
                    'organization': doc.metadata.get('organization', 'Unknown'),
                    'title': doc.metadata.get('title', 'No title'),
                    'url': doc.metadata.get('source_url', ''),
                    'content_type': 'web_page',
                    'description': doc.metadata.get('description', ''),
                    'query_source': doc.metadata.get('query_source', 'search')
                })

            return {
                'symptom': 'pain',
                'severity_score': severity_score,
                'care_level': care_tip_data['care_level'],
                'escalation_needed': care_tip_data['escalation_needed'],
                'predefined_tip': care_tip_data['tip'],
                'ai_enhanced_tip': ai_response.content,
                'sources': sources,  # WEB ARTICLES ONLY
                'media_resources': media_resources,  # MEDIA ONLY
                'tone_info': {
                    'tone_style': care_tip_data.get('tone', 'supportive'),
                    'focus_area': care_tip_data.get('focus', 'pain_management')
                },
                'retrieval_info': {
                    'enhanced_pain_search': True,
                    'simplified_filtering': True,
                    'total_pain_docs_found': len(web_articles),
                    'total_pain_media_found': len(media_resources)
                },
                'success': True
            }

        except Exception as e:
            logger.error(f"Error in enhanced pain RAG: {str(e)}")
            return {
                'symptom': symptom,
                'severity_score': severity_score,
                'care_level': 'error',
                'escalation_needed': (severity_score == 5),
                'predefined_tip': f"System error: {str(e)}",
                'ai_enhanced_tip': "Error retrieving pain information. Please consult your healthcare provider.",
                'sources': [],
                'media_resources': [],
                'tone_info': {},
                'retrieval_info': {'error': str(e)},
                'error': str(e),
                'success': False
            }

    def _fallback_for_non_pain(self, severity_score: int, symptom: str, user_id: str) -> Dict:
        return {
            'symptom': symptom,
            'severity_score': severity_score,
            'care_level': 'basic_care',
            'escalation_needed': (severity_score == 5),
            'predefined_tip': f"For {symptom} symptoms, monitor and consult healthcare provider if persistent.",
            'ai_enhanced_tip': f"Enhanced support for {symptom} is being developed. Track symptoms and discuss with healthcare team.",
            'sources': [],
            'media_resources': [],
            'tone_info': {'tone_style': 'supportive', 'focus_area': 'general_monitoring'},
            'retrieval_info': {'enhanced_system': False, 'fallback_used': True},
            'success': True
        }


# Singleton pattern
_enhanced_pain_rag_instance = None

def get_enhanced_pain_rag_instance(chromadb_path: str = None, google_api_key: str = None) -> EnhancedPainFocusedCareRAG:
    global _enhanced_pain_rag_instance
    if _enhanced_pain_rag_instance is None:
        if not chromadb_path or not google_api_key:
            raise ValueError("ChromaDB path and Google API key required")
        _enhanced_pain_rag_instance = EnhancedPainFocusedCareRAG(chromadb_path, google_api_key)
    return _enhanced_pain_rag_instance


def get_refined_tip_with_rag(severity_score: int, symptom: str, user_id: str = "default") -> Dict:
    """Simplified convenience function"""
    try:
        load_dotenv()
        
        current_dir = Path(__file__).parent
        chromadb_path = current_dir / "ChromaDB_Parkinson_Data"
        google_api_key = os.getenv("GOOGLE_API_KEY")
        
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        rag_system = get_enhanced_pain_rag_instance(str(chromadb_path), google_api_key)
        return rag_system.get_refined_tip_with_rag(severity_score, symptom, user_id)
        
    except Exception as e:
        logger.error(f"Error in convenience function: {str(e)}")
        return {
            'symptom': symptom,
            'severity_score': severity_score,
            'care_level': 'error',
            'escalation_needed': (severity_score == 5),
            'predefined_tip': f"System error: {str(e)}",
            'ai_enhanced_tip': "Error retrieving information. Consult healthcare provider.",
            'sources': [],
            'media_resources': [],
            'tone_info': {},
            'retrieval_info': {'error': str(e)},
            'error': str(e),
            'success': False
        }


def debug_web_page_search():
    """Debug web page search"""
    print("🔍 DEBUGGING WEB PAGE SEARCH")
    print("=" * 50)
    
    try:
        load_dotenv()
        current_dir = Path(__file__).parent
        chromadb_path = current_dir / "ChromaDB_Parkinson_Data"
        google_api_key = os.getenv("GOOGLE_API_KEY")
        
        if not google_api_key:
            print("❌ GOOGLE_API_KEY not found")
            return
        
        # Initialize vector store
        embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = Chroma(
            collection_name="parkinsons_complete_kb",
            embedding_function=embedding_function,
            persist_directory=str(chromadb_path)
        )
        
        # Test searches
        test_queries = [
            "exercise",
            "meditation", 
            "pain",
            "parkinson"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing query: '{query}'")
            results = vector_store.similarity_search(query, k=10)
            
            web_pages = []
            videos = []
            
            for doc in results:
                content_type = doc.metadata.get('content_type', 'unknown')
                title = doc.metadata.get('title', 'No title')
                org = doc.metadata.get('organization', 'Unknown')
                
                if content_type == 'web_page':
                    web_pages.append((org, title))
                elif content_type in ['video', 'podcast']:
                    videos.append((org, title))
            
            print(f"   📄 Web Pages: {len(web_pages)}")
            for org, title in web_pages[:3]:
                print(f"      [{org}] {title[:60]}...")
            
            print(f"   🎬 Videos: {len(videos)}")
            
    except Exception as e:
        print(f"❌ Error in debug: {e}")


def test_simplified_system():
    """Test the simplified system"""
    print("🧪 Testing SIMPLIFIED System")
    print("=" * 50)
    
    for severity in [1, 2, 3, 4, 5]:
        print(f"\n🔍 Testing Severity {severity}:")
        result = get_refined_tip_with_rag(severity, "pain")
        
        if result['success']:
            sources = result.get('sources', [])
            media = result.get('media_resources', [])
            
            print(f"   ✅ Articles Found: {len(sources)}")
            for i, source in enumerate(sources, 1):
                print(f"      {i}. [{source['organization']}] {source['title'][:50]}...")
            
            print(f"   ✅ Media Found: {len(media)}")
            for i, m in enumerate(media, 1):
                print(f"      {i}. [{m['organization']}] {m['title'][:50]}...")
            
        else:
            print(f"   ❌ Failed: {result.get('error', 'Unknown')}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        debug_web_page_search()
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        test_simplified_system()
    else:
        test_simplified_system()