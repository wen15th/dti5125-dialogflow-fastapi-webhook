# app/main.py
# ADAPTED VERSION - Enhanced RAG Integration While Preserving Colleague's Code

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import json
from pydantic import BaseModel, Field
from typing import Optional
import logging
import os
import sys
from pathlib import Path

# ENHANCED: Import for Enhanced RAG system
# Add the services directory to Python path for enhanced RAG import
current_dir = Path(__file__).parent
services_dir = current_dir / "services"
if services_dir.exists():
    sys.path.append(str(services_dir))
    try:
        # Import the ENHANCED RAG function (updated name)
        from rag.rag_service import get_refined_tip_with_rag
        RAG_AVAILABLE = True
        print("✅ Enhanced Pain RAG service loaded successfully")
    except ImportError as e:
        RAG_AVAILABLE = False
        print(f"⚠️  Enhanced Pain RAG service not available: {e}")
        print("   Please ensure the enhanced rag_service.py is in place")
else:
    RAG_AVAILABLE = False
    print(f"⚠️  Services directory not found: {services_dir}")

# ========== NO CHANGES BELOW THIS LINE ==========

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI backend service is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    logger.info("Request body: %s", json.dumps(body, ensure_ascii=False))

    intent = body["queryResult"]["intent"]["displayName"]

    # Intent Map
    handlers = {
        # "Default Welcome Intent": handle_welcome,
        # "Report_Movement_Issue": handle_report_movement,
        # "confirm_yes_movement": handle_symptom_education,
        "Report_Body_Reactions_And_Pain_Issue": handle_clarification,
        "Report_Body_Reactions_And_Pain_Issue - yes": handle_definition_and_goal,
        "Pain_Duration_Intent - custom": handle_submit, 
        # "Report_Sensory_Issue": handle_clarification,
        # "Report_Sensory_Issue - yes": handle_definition_and_goal
        "Default Fallback Intent": handle_fallback
    }

    try:
        handler = handlers.get(intent, handle_fallback)
        messages = handler(body)
    except Exception as e:
        logger.exception("Error occurred while handling request body: %s",str(e))
        messages = [f"Sorry, an error occurred, please try later."]

    text = ""
    message_list = []
    for message in messages:
        message_list.append({
            "text": {
                "text": [message]
            }
        })
        text = (text + "\n\n" + message).strip()

    output_contexts = []

    if intent == "Report_Body_Reactions_And_Pain_Issue - yes":
        consent_text = "To help me provide the best care tips, would you be okay to answer a few more questions?"
        text = (text + "\n\n" + consent_text).strip()
        message_list.append({
            "text": {
                "text": [consent_text]
            }
        })

        # Set output context for awaiting_consent
        session_path = body.get("session") or body.get("sessionInfo", {}).get("session")
        if not session_path:
            logger.error("No session path found in webhook request!")
            session_path = "projects/YOUR_PROJECT_ID/agent/sessions/placeholder"

        output_contexts = [{
            "name": f"{session_path}/contexts/awaiting_consent",
            "lifespanCount": 1
        }]


    response = {
        "fulfillmentText": text,
        "fulfillmentMessages": message_list,
    }
    if output_contexts:
        response["outputContexts"] = output_contexts

    return JSONResponse(content=response)
  
  # ========== NO CHANGES ABOVE THIS LINE ========== 

# app/main.py
# ADAPTED VERSION - Enhanced RAG Integration While Preserving Colleague's Code

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import json
from pydantic import BaseModel, Field
from typing import Optional
import logging
import os
import sys
from pathlib import Path

# ENHANCED: Import for Enhanced RAG system
# Add the services directory to Python path for enhanced RAG import
current_dir = Path(__file__).parent
services_dir = current_dir / "services"
if services_dir.exists():
    sys.path.append(str(services_dir))
    try:
        # Import the ENHANCED RAG function (updated name)
        from rag.rag_service import get_refined_tip_with_rag
        RAG_AVAILABLE = True
        print("✅ Enhanced Pain RAG service loaded successfully")
    except ImportError as e:
        RAG_AVAILABLE = False
        print(f"⚠️  Enhanced Pain RAG service not available: {e}")
        print("   Please ensure the enhanced rag_service.py is in place")
else:
    RAG_AVAILABLE = False
    print(f"⚠️  Services directory not found: {services_dir}")

# ========== NO CHANGES BELOW THIS LINE ========== 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI backend service is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    logger.info("Request body: %s", json.dumps(body, ensure_ascii=False))

    intent = body["queryResult"]["intent"]["displayName"]

    # Intent Map
    handlers = {
        # "Default Welcome Intent": handle_welcome,
        # "Report_Movement_Issue": handle_report_movement,
        # "confirm_yes_movement": handle_symptom_education,
        "Report_Body_Reactions_And_Pain_Issue": handle_clarification,
        "Report_Body_Reactions_And_Pain_Issue - yes": handle_definition_and_goal,
        "Pain_Duration_Intent - custom": handle_submit, 
        # "Report_Sensory_Issue": handle_clarification,
        # "Report_Sensory_Issue - yes": handle_definition_and_goal
        "Default Fallback Intent": handle_fallback
    }

    try:
        handler = handlers.get(intent, handle_fallback)
        messages = handler(body)
    except Exception as e:
        logger.exception("Error occurred while handling request body: %s",str(e))
        messages = [f"Sorry, an error occurred, please try later."]

    text = ""
    message_list = []
    for message in messages:
        message_list.append({
            "text": {
                "text": [message]
            }
        })
        text = (text + "\n\n" + message).strip()

    output_contexts = []

    if intent == "Report_Body_Reactions_And_Pain_Issue - yes":
        consent_text = "To help me provide the best care tips, would you be okay to answer a few more questions?"
        text = (text + "\n\n" + consent_text).strip()
        message_list.append({
            "text": {
                "text": [consent_text]
            }
        })

        # Set output context for awaiting_consent
        session_path = body.get("session") or body.get("sessionInfo", {}).get("session")
        if not session_path:
            logger.error("No session path found in webhook request!")
            session_path = "projects/YOUR_PROJECT_ID/agent/sessions/placeholder"

        output_contexts = [{
            "name": f"{session_path}/contexts/awaiting_consent",
            "lifespanCount": 1
        }]


    response = {
        "fulfillmentText": text,
        "fulfillmentMessages": message_list,
    }
    if output_contexts:
        response["outputContexts"] = output_contexts

    return JSONResponse(content=response)

# ========== NO CHANGES ABOVE THIS LINE ==========

# ===== ENHANCED RAG TESTING ENDPOINTS (NEW) =====

# Enhanced Pydantic Models for RAG
class EnhancedPainCareRequest(BaseModel):
    severity_score: int = Field(..., ge=1, le=5, description="Pain severity score from 1 to 5")
    user_id: Optional[str] = Field(default="default", description="Optional user identifier")

class EnhancedPainCareResponse(BaseModel):
    symptom: str
    severity_score: int
    care_level: str
    escalation_needed: bool
    predefined_tip: str
    ai_enhanced_tip: str
    sources: list
    media_resources: list
    tone_info: dict
    retrieval_info: dict  # NEW: Enhanced retrieval information
    success: bool
    error: Optional[str] = None

# Enhanced Health Check
@app.get("/health")
def enhanced_health_check():
    """Enhanced health check endpoint"""
    return {
        "status": "healthy",
        "service": "Enhanced Parkinson's Care Assistant API",
        "version": "2.0.0",
        "enhanced_rag_available": RAG_AVAILABLE,
        "features": [
            "Enhanced pain-focused RAG retrieval",
            "Strict content filtering", 
            "High-relevance source selection",
            "Evidence-based pain management guidance"
        ] if RAG_AVAILABLE else ["Basic API functionality"]
    }

# Enhanced Pain Care Tip Endpoint (POST)
@app.post("/api/pain/care-tip", response_model=EnhancedPainCareResponse)
async def get_enhanced_pain_care_tip(request: EnhancedPainCareRequest):
    """
    Get enhanced pain care tip with improved RAG system
    
    Request body:
    {
        "severity_score": 3,
        "user_id": "optional_user_id"
    }
    """
    if not RAG_AVAILABLE:
        raise HTTPException(
            status_code=503, 
            detail="Enhanced Pain RAG service is not available. Please check server configuration and ensure enhanced rag_service.py is properly installed."
        )
    
    try:
        logger.info(f"Processing ENHANCED pain care tip request: severity={request.severity_score}, user_id={request.user_id}")
        
        # Call the ENHANCED RAG system
        result = get_refined_tip_with_rag(request.severity_score, "pain", request.user_id)
        
        if result['success']:
            logger.info(f"Successfully generated ENHANCED pain care tip for severity {request.severity_score}")
            logger.info(f"Enhanced system used: {result.get('retrieval_info', {}).get('enhanced_pain_search', False)}")
            logger.info(f"Sources found: {len(result.get('sources', []))}, Media found: {len(result.get('media_resources', []))}")
            return result
        else:
            logger.error(f"Failed to generate enhanced pain care tip: {result.get('error', 'Unknown error')}")
            raise HTTPException(status_code=500, detail=result.get('error', 'Unknown error'))
            
    except Exception as e:
        logger.error(f"Unexpected error in get_enhanced_pain_care_tip: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Enhanced Pain Care Tip Endpoint (GET)
@app.get("/api/pain/care-tip/{severity_score}")
async def get_enhanced_pain_care_tip_get(severity_score: int, user_id: Optional[str] = "default"):
    """
    Enhanced GET endpoint for pain care tip
    
    URL: /api/pain/care-tip/3?user_id=optional_user_id
    """
    if not RAG_AVAILABLE:
        raise HTTPException(
            status_code=503, 
            detail="Enhanced Pain RAG service is not available. Please check server configuration and ensure enhanced rag_service.py is properly installed."
        )
    
    if severity_score < 1 or severity_score > 5:
        raise HTTPException(
            status_code=400, 
            detail="severity_score must be between 1 and 5"
        )
    
    try:
        logger.info(f"Processing ENHANCED GET pain care tip request: severity={severity_score}, user_id={user_id}")
        
        # Call the ENHANCED RAG system
        result = get_refined_tip_with_rag(severity_score, "pain", user_id)
        
        if result['success']:
            logger.info(f"Successfully generated ENHANCED pain care tip for severity {severity_score}")
            retrieval_info = result.get('retrieval_info', {})
            logger.info(f"Enhanced features: search={retrieval_info.get('enhanced_pain_search', False)}, "
                       f"filtering={retrieval_info.get('enhanced_filtering', False)}, "
                       f"avg_relevance={retrieval_info.get('avg_pain_relevance_score', 0):.1f}")
            return result
        else:
            logger.error(f"Failed to generate enhanced pain care tip: {result.get('error', 'Unknown error')}")
            raise HTTPException(status_code=500, detail=result.get('error', 'Unknown error'))
            
    except Exception as e:
        logger.error(f"Unexpected error in get_enhanced_pain_care_tip_get: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Enhanced Comprehensive Testing
@app.get("/api/pain/test-all-severities")
async def test_all_enhanced_pain_severities(user_id: Optional[str] = "test_user"):
    """
    Test endpoint to get ENHANCED care tips for all pain severity levels
    Includes enhanced system metrics and quality assessment
    """
    if not RAG_AVAILABLE:
        raise HTTPException(
            status_code=503, 
            detail="Enhanced Pain RAG service is not available. Please check server configuration."
        )
    
    try:
        results = {}
        logger.info("Testing all pain severity levels with ENHANCED system")
        
        total_sources = 0
        total_media = 0
        total_relevance_score = 0
        enhanced_searches = 0
        
        for severity in range(1, 6):
            try:
                result = get_refined_tip_with_rag(severity, "pain", user_id)
                results[f"severity_{severity}"] = result
                
                # Collect enhanced metrics
                if result['success']:
                    retrieval_info = result.get('retrieval_info', {})
                    sources_count = len(result.get('sources', []))
                    media_count = len(result.get('media_resources', []))
                    
                    total_sources += sources_count
                    total_media += media_count
                    
                    if retrieval_info.get('enhanced_pain_search', False):
                        enhanced_searches += 1
                    
                    avg_relevance = retrieval_info.get('avg_pain_relevance_score', 0)
                    total_relevance_score += avg_relevance
                    
                    logger.info(f"Enhanced test severity {severity}: Success - "
                               f"sources={sources_count}, media={media_count}, "
                               f"relevance={avg_relevance:.1f}, enhanced={retrieval_info.get('enhanced_pain_search', False)}")
                else:
                    logger.error(f"Enhanced test severity {severity}: Failed")
                    
            except Exception as e:
                results[f"severity_{severity}"] = {
                    'error': str(e),
                    'success': False,
                    'severity_score': severity
                }
                logger.error(f"Failed to test enhanced severity {severity}: {str(e)}")
        
        # Calculate enhanced summary
        successful_tests = sum(1 for result in results.values() if result.get('success', False))
        avg_overall_relevance = total_relevance_score / 5 if successful_tests > 0 else 0
        
        enhanced_summary = {
            'total_tests': 5,
            'successful_tests': successful_tests,
            'success_rate': f"{successful_tests/5*100:.1f}%",
            'enhanced_searches_used': enhanced_searches,
            'enhanced_system_usage': f"{enhanced_searches/5*100:.1f}%",
            'total_sources_found': total_sources,
            'total_media_found': total_media,
            'average_sources_per_test': f"{total_sources/5:.1f}",
            'average_media_per_test': f"{total_media/5:.1f}",
            'average_relevance_score': f"{avg_overall_relevance:.2f}",
            'system_quality': "excellent" if avg_overall_relevance > 20 else "good" if avg_overall_relevance > 15 else "needs_improvement"
        }
        
        return {
            'enhanced_summary': enhanced_summary,
            'results': results,
            'success': True,
            'system_version': '2.0.0 - Enhanced'
        }
        
    except Exception as e:
        logger.error(f"Unexpected error in test_all_enhanced_pain_severities: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Enhanced Validation Endpoint
@app.get("/api/pain/validate")
async def validate_enhanced_pain_system():
    """
    ENHANCED validation endpoint to check if the pain-focused system is working correctly
    Includes detailed quality metrics and recommendations
    """
    if not RAG_AVAILABLE:
        raise HTTPException(
            status_code=503, 
            detail="Enhanced Pain RAG service is not available. Please check server configuration."
        )
    
    try:
        logger.info("Running ENHANCED pain system validation")
        
        # Test moderate pain (most common case)
        test_result = get_refined_tip_with_rag(3, "pain", 'enhanced_validation_user')
        
        if not test_result['success']:
            return {
                'validation_passed': False,
                'error': test_result.get('error', 'Unknown error'),
                'system_status': 'FAILED',
                'recommendations': ['Check enhanced RAG system configuration', 'Verify ChromaDB path', 'Check Google API key']
            }
        
        retrieval_info = test_result.get('retrieval_info', {})
        sources = test_result.get('sources', [])
        media_resources = test_result.get('media_resources', [])
        
        # Enhanced validation checks
        enhanced_validation = {
            'system_responsive': test_result['success'],
            'enhanced_search_active': retrieval_info.get('enhanced_pain_search', False),
            'enhanced_filtering_active': retrieval_info.get('enhanced_filtering', False),
            'pain_sources_found': len(sources),
            'pain_media_found': len(media_resources),
            'ai_response_generated': bool(test_result.get('ai_enhanced_tip', '')),
            'proper_care_level': test_result.get('care_level') == 'basic_care',
            'high_relevance_scores': retrieval_info.get('avg_pain_relevance_score', 0) > 15
        }
        
        # Check source quality (enhanced)
        pain_focused_sources = 0
        general_sources = 0
        high_relevance_sources = 0
        
        for source in sources:
            title = source.get('title', '').lower()
            relevance_str = source.get('relevance', '')
            
            # Check if source is pain-focused
            if any(keyword in title for keyword in ['pain', 'relief', 'treatment', 'therapy', 'management']):
                pain_focused_sources += 1
            
            # Check if source is general content (should be filtered out)
            if any(keyword in title for keyword in ['early signs', 'getting diagnosed', 'about us', 'career', 'homepage']):
                general_sources += 1
            
            # Check relevance score
            if 'score:' in relevance_str:
                try:
                    score_part = relevance_str.split('score:')[1].split(')')[0].strip()
                    score = float(score_part)
                    if score > 15:
                        high_relevance_sources += 1
                except:
                    pass
        
        enhanced_validation.update({
            'pain_focused_sources': pain_focused_sources,
            'general_sources_filtered': general_sources == 0,
            'high_relevance_sources': high_relevance_sources,
            'source_quality_excellent': pain_focused_sources == len(sources) and general_sources == 0
        })
        
        # Check AI response quality
        ai_response = test_result.get('ai_enhanced_tip', '').lower()
        pain_keywords = ['pain', 'relief', 'therapy', 'treatment', 'management', 'exercise', 'evidence', 'research']
        pain_keywords_found = [kw for kw in pain_keywords if kw in ai_response]
        
        enhanced_validation.update({
            'pain_keywords_in_response': pain_keywords_found,
            'pain_focused_ai': len(pain_keywords_found) >= 2,
            'evidence_based_language': any(word in ai_response for word in ['evidence', 'research', 'studies', 'clinical'])
        })
        
        # Overall validation score
        validations_passed = sum(1 for v in enhanced_validation.values() if v is True)
        total_validations = len([v for v in enhanced_validation.values() if isinstance(v, bool)])
        validation_score = validations_passed / total_validations * 100
        
        # Generate recommendations
        recommendations = []
        if validation_score >= 85:
            recommendations.append("✅ EXCELLENT: Enhanced system is working optimally!")
        elif validation_score >= 70:
            recommendations.append("✅ GOOD: Enhanced system is working well with minor room for improvement")
        else:
            recommendations.append("⚠️ NEEDS IMPROVEMENT: Enhanced system needs attention")
        
        if not enhanced_validation['enhanced_search_active']:
            recommendations.append("❌ Enhanced search not active - check enhanced rag_service.py installation")
        
        if general_sources > 0:
            recommendations.append(f"⚠️ Found {general_sources} general sources - enhanced filtering may need improvement")
        
        if enhanced_validation['pain_focused_sources'] == len(sources) and len(sources) > 0:
            recommendations.append("✅ All sources are pain-focused - excellent enhanced filtering!")
        
        if retrieval_info.get('avg_pain_relevance_score', 0) < 15:
            recommendations.append("⚠️ Consider increasing relevance thresholds for better quality")
        
        response = {
            'validation_passed': validation_score >= 70,
            'validation_score': f"{validation_score:.1f}%",
            'system_status': 'EXCELLENT' if validation_score >= 85 else 'GOOD' if validation_score >= 70 else 'NEEDS_IMPROVEMENT',
            'enhanced_validation_details': enhanced_validation,
            'source_quality_metrics': {
                'total_sources': len(sources),
                'pain_focused_sources': pain_focused_sources,
                'general_sources': general_sources,
                'high_relevance_sources': high_relevance_sources,
                'avg_relevance_score': retrieval_info.get('avg_pain_relevance_score', 0)
            },
            'recommendations': recommendations,
            'test_result_summary': {
                'care_level': test_result.get('care_level'),
                'escalation_needed': test_result.get('escalation_needed'),
                'ai_response_length': len(test_result.get('ai_enhanced_tip', '')),
                'enhanced_features_used': retrieval_info.get('enhanced_pain_search', False)
            },
            'success': True
        }
        
        logger.info(f"Enhanced validation completed: {validation_score:.1f}% score")
        return response
        
    except Exception as e:
        logger.error(f"Enhanced validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Enhanced validation failed: {str(e)}")

# Enhanced Information Endpoint
@app.get("/api/info")
def get_enhanced_api_info():
    """Get information about available enhanced API endpoints"""
    return {
        "service": "Enhanced Parkinson's Care Assistant API",
        "version": "2.0.0",
        "enhanced_rag_available": RAG_AVAILABLE,
        "enhanced_features": [
            "Pain-focused content retrieval with 20+ relevance threshold",
            "Strict filtering to exclude general PD content", 
            "Targeted pain queries for better source quality",
            "Enhanced relevance scoring with penalties for general content",
            "Evidence-based AI response generation",
            "Comprehensive quality metrics and validation"
        ] if RAG_AVAILABLE else ["Basic API functionality"],
        "endpoints": {
            "webhook": "POST /webhook - Dialogflow webhook integration (colleague's code)",
            "health": "GET /health - Enhanced health check",
            "pain_care_post": "POST /api/pain/care-tip - Get enhanced pain care tip (POST)",
            "pain_care_get": "GET /api/pain/care-tip/{severity} - Get enhanced pain care tip (GET)",
            "test_all": "GET /api/pain/test-all-severities - Test all pain severities with enhanced metrics",
            "validate": "GET /api/pain/validate - Validate enhanced RAG system",
            "info": "GET /api/info - This endpoint",
            "docs": "GET /docs - FastAPI interactive documentation"
        },
        "pain_severity_levels": {
            "1-2": "Educational/gentle encouragement",
            "3": "Basic care/practical support", 
            "4": "Advanced care/solution focused",
            "5": "Escalation/professional consultation"
        },
        "enhanced_quality_metrics": {
            "relevance_threshold": "20+ (vs 5 in basic system)",
            "content_filtering": "Strict pain-focus validation",
            "source_penalties": "-10 points for general content",
            "target_quality": "Pain-specific sources only"
        }
    }

# Colleague's handler functions - EXACTLY as provided, no changes
def handle_clarification(body):
    """Handler for clarification intent - implemented by colleague"""
    return ["I understand you're experiencing pain. Let me help you with that."]

def handle_definition_and_goal(body):
    """Handler for definition and goal intent - implemented by colleague"""
    return ["Let me help you understand and manage your pain better."]

def handle_submit(body):
    """Handler for submit intent - implemented by colleague"""
    return ["Thank you for providing the information. I'll help you with pain management."]

def handle_fallback(body):
    """Handler for fallback intent - implemented by colleague"""
    return ["I'm sorry, I didn't understand. Could you please rephrase?"]

if __name__ == "__main__":
    import uvicorn
    
    # Enhanced startup checks
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        if not os.getenv("GOOGLE_API_KEY"):
            print("⚠️  WARNING: GOOGLE_API_KEY not found in environment variables")
            print("Please ensure your .env file is configured correctly for enhanced RAG")
        else:
            print("✅ Environment variables loaded successfully")
        
        print("🚀 Starting Enhanced Parkinson's Care Assistant API...")
        print("📋 Available endpoints:")
        print("   POST /webhook (Dialogflow integration - colleague's code)")
        print("   GET  /health (enhanced)")
        print("   POST /api/pain/care-tip (enhanced)")
        print("   GET  /api/pain/care-tip/<severity_score> (enhanced)")
        print("   GET  /api/pain/test-all-severities (enhanced)")
        print("   GET  /api/pain/validate (enhanced)")
        print("   GET  /api/info (enhanced)")
        
        print(f"\n🔗 Enhanced Test URLs (will be available at):")
        print("   http://localhost:8000/health")
        print("   http://localhost:8000/api/pain/care-tip/3")
        print("   http://localhost:8000/api/pain/validate")
        print("   http://localhost:8000/docs (FastAPI interactive docs)")
        
        if RAG_AVAILABLE:
            print(f"\n✨ Enhanced Features Active:")
            print("   🎯 Pain-focused content retrieval")
            print("   🔍 Strict quality filtering")
            print("   📊 High relevance scoring (20+ threshold)")
            print("   🚫 General content penalties")
        else:
            print(f"\n⚠️  Enhanced RAG features not available")
            print("   Please ensure enhanced rag_service.py is properly installed")
        
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except Exception as e:
        print(f"❌ Failed to start enhanced server: {str(e)}")
        print("Please check your dependencies and enhanced configuration")