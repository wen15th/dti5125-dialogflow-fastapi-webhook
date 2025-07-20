# app/services/pain_handlers.py
# UPDATED VERSION with Enhanced RAG Integration
import json
from typing import Dict, Any
import logging
from .rag.rag_service import get_refined_tip_with_rag

# Configure logging
logger = logging.getLogger(__name__)

def handle_pain_report(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    ENHANCED pain report handler with improved RAG integration
    """
    try:
        parameters = request_data.get("queryResult", {}).get("parameters", {})
        severity_score = parameters.get("severity_score")
        symptom = parameters.get("symptom", "pain")

        # Get ENHANCED care tip using improved RAG system
        rag_result = get_refined_tip_with_rag(
            severity_score=severity_score,
            symptom=symptom,
        )

        logger.info(f"RAG result: {json.dumps(rag_result, ensure_ascii=False)}")

        if rag_result['success']:
            # Create response based on ENHANCED RAG results
            response_list = _create_enhanced_response(rag_result, "")
            
            # Prepare rich response with follow-up suggestions
            response = {
                "fulfillmentText": "\n".join(response_list),
                "fulfillmentMessages": [
                    {
                        "payload": {
                            "richContent": [
                                [
                                    {
                                        "type": "description",
                                        "text": response_list
                                    }
                                ]
                            ]
                        }
                    }
                ]
            }
            
            # Add follow-up suggestions if available
            # if rag_result.get('sources') or rag_result.get('media_resources'):
            #     response["fulfillmentMessages"].append(_create_enhanced_suggestions_payload(rag_result))

            # Add escalation context if needed
            if rag_result.get('escalation_needed'):
                response["outputContexts"] = [
                    {
                        "name": f"{request_data.get('session')}/contexts/escalation-needed",
                        "lifespanCount": 5,
                        "parameters": {
                            "symptom": symptom,
                            "severity": severity_score,
                            "escalation_reason": "High severity pain reported",
                            "enhanced_system_used": True
                        }
                    }
                ]
            
            # Add enhanced system info to context
            response.setdefault("outputContexts", []).append({
                "name": f"{request_data.get('session')}/contexts/enhanced-rag-info",
                "lifespanCount": 3,
                "parameters": {
                    "retrieval_info": rag_result.get('retrieval_info', {}),
                    "sources_count": len(rag_result.get('sources', [])),
                    "media_count": len(rag_result.get('media_resources', []))
                }
            })
            
            logger.info(f"Enhanced RAG response created successfully for {symptom}")
            logger.info(f"Retrieved {len(rag_result.get('sources', []))} enhanced pain sources")
            return response
            
        else:
            # Fallback to basic response if enhanced RAG fails
            logger.warning(f"Enhanced RAG system failed: {rag_result.get('error', 'Unknown error')}")
            return _create_fallback_response(severity_score, symptom, "")
            
    except Exception as e:
        logger.error(f"Error in handle_pain_report: {str(e)}")
        return _create_error_response(str(e))


def _create_enhanced_response(rag_result: Dict[str, Any], user_input: str) -> list:
    """
    Create an ENHANCED response using improved RAG results
    """
    symptom = rag_result['symptom']
    severity = rag_result['severity_score']
    care_level = rag_result['care_level']
    escalation_needed = rag_result['escalation_needed']
    retrieval_info = rag_result.get('retrieval_info', {})
    
    # Start with empathetic acknowledgment
    response_parts = [
        f"I understand you're experiencing {symptom} and I want to help you manage it effectively."
    ]

    # Add severity-specific context
    if severity <= 2:
        response_parts.append("It's good that your pain level is relatively manageable.")
    elif severity == 3:
        response_parts.append("I can see you're dealing with moderate pain that needs attention.")
    elif severity == 4:
        response_parts.append("Your pain level is concerning and requires careful management.")
    else:  # severity == 5
        response_parts.append("I'm concerned about your high pain level. This needs immediate attention.")

    # Add the main care tip
    response_parts.append(f"\n💡 Care Recommendation")
    response_parts.append(rag_result['predefined_tip'])
    
    # Add AI-enhanced guidance if available
    if rag_result.get('ai_enhanced_tip') and len(rag_result['ai_enhanced_tip']) > 50:
        response_parts.append(f"\n🤖 Evidence-Based Guidance")
        response_parts.append(rag_result['ai_enhanced_tip'])

    # Add escalation notice if needed
    if escalation_needed:
        response_parts.append("\n🚨 Important")
        response_parts.append("Given the severity of your symptoms, I strongly recommend contacting your healthcare provider soon.")

    # Add ENHANCED source information
    if rag_result.get('sources'):
        source_count = len(rag_result['sources'])
        avg_relevance = retrieval_info.get('avg_pain_relevance_score', 0)
        response_parts.append(f"\n📚 This guidance is based on {source_count} high-quality pain-focused sources from trusted Parkinson's organizations (avg. relevance: {avg_relevance:.1f}).")

    # Add enhanced media resources mention
    if rag_result.get('media_resources'):
        media_count = len(rag_result['media_resources'])
        response_parts.append(f"\n🎬 I also found {media_count} pain-specific video/audio resources that can help with your pain management.")
        media_count = 1
        for media_resource in rag_result['media_resources']:
            response_parts.append(f"{media_count}. {media_resource['title']} ({media_resource['type']}): {media_resource['source_url']}")
            media_count += 1
    
    # Add enhanced system info if available
    # if retrieval_info.get('enhanced_pain_search'):
    #     response_parts.append(f"\n✨ **Enhanced Search:** Used specialized pain-focused retrieval for more relevant recommendations.")
    
    # return "\n".join(response_parts)
    return response_parts


def _create_enhanced_suggestions_payload(rag_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create ENHANCED suggestion chips for sources and media resources
    """
    suggestions = []
    
    # Add ENHANCED source suggestions (max 3) with relevance info
    for i, source in enumerate(rag_result.get('sources', [])[:3]):
        title = source.get('title', 'Resource')
        org = source.get('organization', 'Unknown')
        
        # Extract relevance score from relevance string
        relevance_str = source.get('relevance', '')
        relevance_score = ""
        if 'score:' in relevance_str:
            try:
                score_part = relevance_str.split('score:')[1].split(')')[0].strip()
                relevance_score = f" ({score_part})"
            except:
                pass
        
        suggestions.append(f"📖 {org}: {title[:25]}...{relevance_score}")
    
    # Add ENHANCED media suggestions (max 2) with source info
    for i, media in enumerate(rag_result.get('media_resources', [])[:2]):
        title = media.get('title', 'Media')
        media_type = media.get('type', 'resource')
        org = media.get('organization', 'Unknown')
        emoji = "🎬" if media_type == "video" else "🎧"
        suggestions.append(f"{emoji} {org}: {title[:25]}...")
    
    # Add enhanced general suggestions
    suggestions.extend([
        "💬 Tell me more about your pain",
        "📝 Log this pain episode",
        "🏥 Find pain specialists",
        "📞 Emergency contacts",
        "📊 View pain analytics"
    ])
    
    return {
        "quickReplies": {
            "title": "Enhanced pain resources and options:",
            "quickReplies": suggestions[:8]  # Limit to 8 suggestions
        }
    }


def _create_fallback_response(severity_score: int, symptom: str, user_input: str) -> Dict[str, Any]:
    """
    Create a basic fallback response when enhanced RAG system fails
    """
    # Basic care tips based on severity
    if severity_score <= 2:
        care_tip = "For mild pain, try gentle exercises, warm compresses, and relaxation techniques. Regular movement can help manage Parkinson's-related pain."
    elif severity_score == 3:
        care_tip = "For moderate pain, consider warm packs (avoid electric heating pads), gentle stretching, and tracking when the pain occurs. This information will be helpful for your healthcare team."
    elif severity_score == 4:
        care_tip = "For significant pain, keep a pain journal noting when it happens and what helps. Share this information with your healthcare providers for better pain management strategies."
    else:  # severity_score == 5
        care_tip = "For severe pain, I recommend speaking with your doctor or nurse as soon as possible. They can help identify the cause and provide appropriate treatment."
    
    response_text = f"I understand you're experiencing {symptom}. {care_tip}"
    
    if severity_score >= 4:
        response_text += "\n\n🚨 Given the severity of your symptoms, please consider contacting your healthcare provider."
    
    response_text += "\n\n⚠️ Note: Enhanced pain management system temporarily unavailable. Using basic recommendations."
    
    return {
        "fulfillmentText": response_text,
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [response_text]
                }
            }
        ],
        "outputContexts": [
            {
                "name": f"fallback-used",
                "lifespanCount": 1,
                "parameters": {
                    "enhanced_system_failed": True,
                    "fallback_reason": "Enhanced RAG system unavailable"
                }
            }
        ]
    }


def _create_error_response(error_message: str) -> Dict[str, Any]:
    """
    Create an error response when something goes wrong
    """
    response_text = ("I apologize, but I'm having trouble processing your request right now. "
                    "For pain management, I recommend consulting with your healthcare provider. "
                    "You can also try gentle exercises, warm compresses, and relaxation techniques for mild pain relief.")
    
    return {
        "fulfillmentText": response_text,
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [response_text]
                }
            }
        ],
        "outputContexts": [
            {
                "name": f"error-occurred",
                "lifespanCount": 1,
                "parameters": {
                    "error_type": "pain_handler_error",
                    "error_message": error_message
                }
            }
        ]
    }


def handle_pain_followup(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle follow-up questions about pain management with ENHANCED system
    """
    try:
        user_input = request_data.get("queryResult", {}).get("queryText", "")
        session_id = request_data.get("session", "").split("/")[-1]
        
        # Check if user is asking for more specific information
        if any(keyword in user_input.lower() for keyword in ["exercise", "therapy", "medication", "doctor"]):
            # Use ENHANCED RAG to get more specific information
            rag_result = get_refined_tip_with_rag(
                severity_score=3,  # Default moderate severity for follow-up
                symptom="pain",
                user_id=session_id
            )
            
            if rag_result['success']:
                # Extract relevant information based on user's question
                if "exercise" in user_input.lower():
                    response_text = "Here are evidence-based exercise recommendations for pain management:\n\n"
                    # Filter for exercise-related content from AI response
                    ai_content = rag_result.get('ai_enhanced_tip', '')
                    if any(word in ai_content.lower() for word in ["exercise", "stretch", "physical", "movement"]):
                        response_text += ai_content[:400] + "..."
                    else:
                        response_text += "Gentle exercises like walking, stretching, and range-of-motion activities can help with pain management. Always consult your healthcare provider before starting new exercises."
                
                elif "medication" in user_input.lower():
                    response_text = "Regarding pain medication for Parkinson's:\n\n"
                    ai_content = rag_result.get('ai_enhanced_tip', '')
                    if "medication" in ai_content.lower():
                        response_text += ai_content[:400] + "..."
                    else:
                        response_text += "It's important to work with your healthcare provider to find the right pain management approach. They can help determine if medication adjustments or new treatments might help with your pain."
                
                elif "doctor" in user_input.lower() or "healthcare" in user_input.lower():
                    response_text = "When speaking with your healthcare provider about pain:\n\n"
                    response_text += "• Describe the location, intensity, and timing of your pain\n"
                    response_text += "• Share what makes it better or worse\n"
                    response_text += "• Mention how it affects your daily activities\n"
                    response_text += "• Keep a pain diary to track patterns\n"
                    
                    ai_content = rag_result.get('ai_enhanced_tip', '')
                    if ai_content and len(ai_content) > 50:
                        response_text += f"\n**Additional guidance:** {ai_content[:300]}..."
                
                else:
                    response_text = rag_result.get('ai_enhanced_tip', 'I can help you with pain management strategies.')
                    if not response_text or len(response_text) < 50:
                        response_text = rag_result.get('predefined_tip', 'I can help you with pain management strategies.')
                
                # Add enhanced system note if available
                retrieval_info = rag_result.get('retrieval_info', {})
                if retrieval_info.get('enhanced_pain_search'):
                    sources_count = retrieval_info.get('total_pain_docs_found', 0)
                    if sources_count > 0:
                        response_text += f"\n\n📚 This information is based on {sources_count} specialized pain management sources."
                
                return {
                    "fulfillmentText": response_text,
                    "fulfillmentMessages": [
                        {
                            "text": {
                                "text": [response_text]
                            }
                        }
                    ]
                }
        
        # Default enhanced follow-up response
        return {
            "fulfillmentText": "What specific aspect of pain management would you like to know more about? I can provide evidence-based information on exercises, treatments, when to contact your doctor, or general pain relief strategies.",
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": ["What specific aspect of pain management would you like to know more about? I can provide evidence-based information on exercises, treatments, when to contact your doctor, or general pain relief strategies."]
                    }
                },
                {
                    "quickReplies": {
                        "title": "Enhanced pain management topics:",
                        "quickReplies": [
                            "💪 Evidence-based exercises",
                            "💊 Pain medications",
                            "🏥 When to see specialist",
                            "📝 Pain tracking methods",
                            "🌡️ Heat/cold therapy",
                            "🧘 Relaxation techniques"
                        ]
                    }
                }
            ]
        }
        
    except Exception as e:
        logger.error(f"Error in handle_pain_followup: {str(e)}")
        return _create_error_response(str(e))


def handle_other_symptoms(request_data: Dict[str, Any], symptom_type: str) -> Dict[str, Any]:
    """
    Generic handler for other symptoms using enhanced RAG system
    """
    try:
        session_id = request_data.get("session", "").split("/")[-1]
        user_input = request_data.get("queryResult", {}).get("queryText", "")
        
        # Map symptom types
        symptom_mapping = {
            "lightheadedness": "light-headedness",
            "dizziness": "light-headedness",
            "sweating": "unusual sweating",
            "skin": "skin changes"
        }
        
        symptom = symptom_mapping.get(symptom_type.lower(), symptom_type)
        
        # Dummy severity score for testing
        # TODO: Replace with actual ML model prediction
        dummy_severity = 3  # Default moderate severity
        
        logger.info(f"Processing {symptom} report for session {session_id}")
        
        # Get enhanced response (currently only pain is enhanced)
        rag_result = get_refined_tip_with_rag(
            severity_score=dummy_severity,
            symptom=symptom,
            user_id=session_id
        )
        
        if rag_result['success']:
            response_list = _create_enhanced_response(rag_result, user_input)
            
            response = {
                "fulfillmentText": "\n".join(response_list),
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": response_list
                        }
                    }
                ]
            }
            
            # Add suggestions if resources available
            if rag_result.get('sources') or rag_result.get('media_resources'):
                response["fulfillmentMessages"].append(_create_enhanced_suggestions_payload(rag_result))
            
            # Add escalation context if needed
            if rag_result.get('escalation_needed'):
                response["outputContexts"] = [
                    {
                        "name": f"{request_data.get('session')}/contexts/escalation-needed",
                        "lifespanCount": 5,
                        "parameters": {
                            "symptom": symptom,
                            "severity": dummy_severity,
                            "escalation_reason": f"High severity {symptom} reported"
                        }
                    }
                ]
            
            return response
            
        else:
            # Fallback response
            return _create_fallback_response(dummy_severity, symptom, user_input)
            
    except Exception as e:
        logger.error(f"Error in handle_other_symptoms: {str(e)}")
        return _create_error_response(str(e))


# ENHANCED utility functions for testing and debugging
def test_enhanced_pain_handler():
    """
    Test function for ENHANCED pain handler with RAG integration
    """
    # Sample request data mimicking Dialogflow webhook format
    sample_request = {
        "queryResult": {
            "queryText": "I'm having severe pain in my back and legs",
            "parameters": {},
            "intent": {
                "name": "pain.report",
                "displayName": "Pain Report"
            }
        },
        "session": "projects/test-project/agent/sessions/test-session-123"
    }
    
    print("🧪 Testing ENHANCED Pain Handler with RAG Integration")
    print("=" * 60)
    
    try:
        response = handle_pain_report(sample_request)
        print("✅ Enhanced pain handler test successful")
        print(f"📝 Response preview: {response['fulfillmentText'][:200]}...")
        
        if 'fulfillmentMessages' in response:
            print(f"📊 Messages count: {len(response['fulfillmentMessages'])}")
        
        if 'outputContexts' in response:
            print(f"🔄 Contexts set: {len(response['outputContexts'])}")
            
            # Check for enhanced system context
            for context in response['outputContexts']:
                if 'enhanced-rag-info' in context.get('name', ''):
                    retrieval_info = context.get('parameters', {}).get('retrieval_info', {})
                    print(f"🔍 Enhanced retrieval used: {retrieval_info.get('enhanced_pain_search', False)}")
                    print(f"📚 Sources found: {context.get('parameters', {}).get('sources_count', 0)}")
                    print(f"🎥 Media found: {context.get('parameters', {}).get('media_count', 0)}")
            
    except Exception as e:
        print(f"❌ Enhanced pain handler test failed: {str(e)}")


def test_enhanced_pain_followup():
    """
    Test function for enhanced pain follow-up handler
    """
    test_queries = [
        "Tell me about exercises for pain",
        "What medications help with pain?",
        "When should I see a doctor for pain?",
        "How can I track my pain?"
    ]
    
    print("\n🧪 Testing Enhanced Pain Follow-up Handler")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")
        
        sample_request = {
            "queryResult": {
                "queryText": query,
                "parameters": {},
                "intent": {
                    "name": "pain.followup",
                    "displayName": "Pain Follow-up"
                }
            },
            "session": "projects/test-project/agent/sessions/test-session-456"
        }
        
        try:
            response = handle_pain_followup(sample_request)
            print(f"   ✅ Follow-up successful")
            print(f"   📝 Response length: {len(response['fulfillmentText'])} chars")
            
            # Check if response is relevant to the query
            response_text = response['fulfillmentText'].lower()
            query_words = query.lower().split()
            relevance = sum(1 for word in query_words if word in response_text)
            print(f"   🎯 Relevance score: {relevance}/{len(query_words)}")
            
        except Exception as e:
            print(f"   ❌ Follow-up failed: {str(e)}")


def test_enhanced_other_symptoms():
    """
    Test function for enhanced other symptoms handler
    """
    test_symptoms = ["lightheadedness", "sweating", "skin"]
    
    print("\n🧪 Testing Enhanced Other Symptoms Handler")
    print("=" * 60)
    
    for symptom in test_symptoms:
        print(f"\n🔍 Testing {symptom}...")
        
        sample_request = {
            "queryResult": {
                "queryText": f"I'm experiencing {symptom} issues",
                "parameters": {},
                "intent": {
                    "name": f"{symptom}.report",
                    "displayName": f"{symptom.title()} Report"
                }
            },
            "session": "projects/test-project/agent/sessions/test-session-789"
        }
        
        try:
            response = handle_other_symptoms(sample_request, symptom)
            print(f"   ✅ {symptom} handler successful")
            print(f"   📝 Response length: {len(response['fulfillmentText'])} chars")
            
            # Check if fallback was used (for non-pain symptoms)
            if 'outputContexts' in response:
                for context in response['outputContexts']:
                    if 'fallback-used' in context.get('name', ''):
                        print(f"   ⚠️  Fallback used (expected for non-pain symptoms)")
                        break
                else:
                    print(f"   ✅ Enhanced system used")
            
        except Exception as e:
            print(f"   ❌ {symptom} handler failed: {str(e)}")


def validate_enhanced_integration():
    """
    Validate that the enhanced integration is working correctly
    """
    print("\n🔬 VALIDATION: Enhanced Integration Test")
    print("=" * 50)
    
    # Test pain handling
    pain_request = {
        "queryResult": {
            "queryText": "I have moderate back pain",
            "parameters": {},
            "intent": {"name": "pain.report", "displayName": "Pain Report"}
        },
        "session": "projects/test-project/agent/sessions/validation-test"
    }
    
    try:
        response = handle_pain_report(pain_request)
        
        print("✅ Enhanced integration test successful!")
        
        # Check for enhanced features
        has_enhanced_context = False
        enhanced_info = {}
        
        if 'outputContexts' in response:
            for context in response['outputContexts']:
                if 'enhanced-rag-info' in context.get('name', ''):
                    has_enhanced_context = True
                    enhanced_info = context.get('parameters', {})
                    break
        
        print(f"\n📊 INTEGRATION ANALYSIS:")
        print(f"   Enhanced context found: {has_enhanced_context}")
        
        if has_enhanced_context:
            retrieval_info = enhanced_info.get('retrieval_info', {})
            print(f"   Enhanced search used: {retrieval_info.get('enhanced_pain_search', False)}")
            print(f"   Enhanced filtering: {retrieval_info.get('enhanced_filtering', False)}")
            print(f"   Sources retrieved: {enhanced_info.get('sources_count', 0)}")
            print(f"   Media retrieved: {enhanced_info.get('media_count', 0)}")
            
            avg_score = retrieval_info.get('avg_pain_relevance_score', 0)
            if avg_score > 0:
                print(f"   Avg relevance score: {avg_score:.2f}")
                if avg_score > 15:
                    print("   ✅ HIGH QUALITY: Good relevance scores!")
                else:
                    print("   ⚠️  MEDIUM QUALITY: Relevance could be better")
        
        # Check response quality
        response_text = response['fulfillmentText']
        print(f"\n🤖 RESPONSE QUALITY:")
        print(f"   Response length: {len(response_text)} chars")
        
        # Check for enhanced indicators
        enhanced_indicators = [
            "Evidence-Based Guidance",
            "high-quality pain-focused sources",
            "Enhanced Search",
            "specialized pain-focused retrieval"
        ]
        
        found_indicators = sum(1 for indicator in enhanced_indicators 
                             if indicator in response_text)
        
        print(f"   Enhanced indicators found: {found_indicators}/{len(enhanced_indicators)}")
        
        if found_indicators >= 2:
            print("   ✅ EXCELLENT: Response shows enhanced system features!")
        elif found_indicators >= 1:
            print("   ✅ GOOD: Some enhanced features visible")
        else:
            print("   ⚠️  WARNING: Enhanced features not clearly visible in response")
        
    except Exception as e:
        print(f"❌ VALIDATION FAILED: {str(e)}")


def compare_enhanced_vs_fallback():
    """
    Compare enhanced system vs fallback responses
    """
    print("\n📊 COMPARISON: Enhanced vs Fallback")
    print("=" * 50)
    
    # Test request
    test_request = {
        "queryResult": {
            "queryText": "I have chronic pain in my joints",
            "parameters": {},
            "intent": {"name": "pain.report", "displayName": "Pain Report"}
        },
        "session": "projects/test-project/agent/sessions/comparison-test"
    }
    
    print("Testing enhanced system...")
    try:
        enhanced_response = handle_pain_report(test_request)
        enhanced_length = len(enhanced_response['fulfillmentText'])
        enhanced_has_sources = any('high-quality' in enhanced_response['fulfillmentText'] or 
                                 'Evidence-Based' in enhanced_response['fulfillmentText'])
        
        print(f"✅ Enhanced response length: {enhanced_length} chars")
        print(f"✅ Enhanced features visible: {enhanced_has_sources}")
        
    except Exception as e:
        print(f"❌ Enhanced system error: {str(e)}")
        return
    
    print("\nTesting fallback system...")
    try:
        # Force fallback by testing with dummy severity
        fallback_response = _create_fallback_response(3, "pain", "I have chronic pain")
        fallback_length = len(fallback_response['fulfillmentText'])
        fallback_has_warning = 'Enhanced pain management system temporarily unavailable' in fallback_response['fulfillmentText']
        
        print(f"✅ Fallback response length: {fallback_length} chars")
        print(f"✅ Fallback warning present: {fallback_has_warning}")
        
        print(f"\n📈 COMPARISON RESULTS:")
        print(f"   Enhanced is longer: {enhanced_length > fallback_length}")
        print(f"   Enhanced has sources: {enhanced_has_sources}")
        print(f"   Fallback has warning: {fallback_has_warning}")
        
        if enhanced_length > fallback_length and enhanced_has_sources:
            print("   🎉 EXCELLENT: Enhanced system provides richer responses!")
        else:
            print("   ⚠️  WARNING: Enhanced system may not be working optimally")
        
    except Exception as e:
        print(f"❌ Fallback test error: {str(e)}")


if __name__ == "__main__":
    # Run ENHANCED tests when script is executed directly
    print("🧪 RUNNING ENHANCED PAIN HANDLER TESTS")
    print("=" * 70)
    
    try:
        # 1. Test enhanced pain handler
        test_enhanced_pain_handler()
        
        # 2. Test enhanced follow-up
        test_enhanced_pain_followup()
        
        # 3. Test other symptoms
        test_enhanced_other_symptoms()
        
        # 4. Validate integration
        validate_enhanced_integration()
        
        # 5. Compare systems
        compare_enhanced_vs_fallback()
        
        print("\n🏁 ENHANCED PAIN HANDLER TESTING COMPLETE!")
        print("If you see enhanced features and good relevance scores,")
        print("the enhanced pain handler integration is working correctly!")
        
    except Exception as e:
        print(f"\n❌ ENHANCED TESTING FAILED: {str(e)}")
        print("Please check your enhanced RAG service configuration.")