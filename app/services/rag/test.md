# Adapted Enhanced Testing Guide

## 🚀 Quick Start (Preserving Colleague's Code)

```bash
# Start the enhanced API server
python app/main.py
```

## 🧪 Available Enhanced Test Endpoints

### 1. Enhanced Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

**Expected Response:**

```json
{
	"status": "healthy",
	"service": "Enhanced Parkinson's Care Assistant API",
	"version": "2.0.0",
	"enhanced_rag_available": true,
	"features": [
		"Enhanced pain-focused RAG retrieval",
		"Strict content filtering",
		"High-relevance source selection",
		"Evidence-based pain management guidance"
	]
}
```

### 2. Enhanced Pain Care Tips (Same URLs, Better Results)

Test different severity levels (1-5):

```bash
# Test mild pain (severity 1) - ENHANCED
curl -X GET "http://localhost:8000/api/pain/care-tip/1"

# Test moderate pain (severity 3) - ENHANCED
curl -X GET "http://localhost:8000/api/pain/care-tip/3"

# Test severe pain (severity 5) - ENHANCED
curl -X GET "http://localhost:8000/api/pain/care-tip/5"
```

**Enhanced Features to Look For:**

- ✅ `"enhanced_pain_search": true` in retrieval_info
- ✅ `"enhanced_filtering": true` in retrieval_info
- ✅ High relevance scores (20+) vs old system (5)
- ✅ Pain-focused source titles instead of "10 Early Signs"
- ✅ Evidence-based AI responses

### 3. Enhanced Comprehensive Validation

```bash
curl -X GET "http://localhost:8000/api/pain/validate"
```

**Enhanced Metrics:**

- `validation_score`: Should be >70% (excellent if >85%)
- `enhanced_search_active`: Should be `true`
- `pain_focused_sources`: Should be high
- `general_sources`: Should be 0 (filtered out)
- `avg_relevance_score`: Should be >15 (preferably >20)

### 4. Enhanced System Testing

```bash
curl -X GET "http://localhost:8000/api/pain/test-all-severities"
```

**Enhanced Quality Indicators:**

- `enhanced_system_usage`: Should be 100%
- `average_relevance_score`: Should be >15
- `system_quality`: Should show "excellent" or "good"

### 5. Enhanced System Info

```bash
curl -X GET "http://localhost:8000/api/info"
```

## 📊 Testing with FastAPI Docs (Same URL, Enhanced Features)

Visit: **http://localhost:8000/docs**

Interactive testing interface with enhanced endpoints while preserving your colleague's webhook functionality.

## 🔍 Enhanced Quality Validation Steps

### Step 1: Basic Enhanced Functionality Test

```bash
# Should return enhanced pain guidance with better sources
curl -X GET "http://localhost:8000/api/pain/care-tip/3" | jq '.success, .retrieval_info.enhanced_pain_search'
# Expected: true, true
```

### Step 2: Enhanced Source Quality Check

```bash
# Check for pain-focused source titles (NOT general PD content)
curl -X GET "http://localhost:8000/api/pain/care-tip/3" | jq '.sources[].title'
```

**Enhanced Results (What You Should See):**

- "Pain Management Strategies for Parkinson's Disease"
- "Chronic Pain Treatment in Movement Disorders"
- "Physical Therapy for Parkinson's Pain Relief"

**Old Results (What Should Be Filtered Out):**

- ❌ "10 Early Signs | Parkinson's Foundation"
- ❌ "Getting Diagnosed | Parkinson's Foundation"
- ❌ "Homepage | Parkinson's Foundation"

### Step 3: Enhanced System Features Check

```bash
# Look for enhanced system indicators
curl -X GET "http://localhost:8000/api/pain/care-tip/3" | jq '.retrieval_info'
```

**Enhanced Response Should Show:**

```json
{
	"enhanced_pain_search": true,
	"enhanced_filtering": true,
	"total_pain_docs_found": 4,
	"total_pain_media_found": 3,
	"avg_pain_relevance_score": 23.5
}
```

### Step 4: Enhanced Relevance Score Validation

```bash
# Check individual source relevance (should be much higher)
curl -X GET "http://localhost:8000/api/pain/care-tip/3" | jq '.sources[].relevance'
```

**Enhanced Scores Should Show:**

- "High - Enhanced pain-focused content (score: 25.3)"
- "High - Enhanced pain-focused content (score: 22.1)"

**Not the old low scores like:**

- ❌ "High - pain-specific content (score: 5.2)"

## 🔄 Colleague's Webhook Code (Preserved & Working)

Your colleague's webhook code at `POST /webhook` remains exactly as they wrote it:

```bash
# Test colleague's webhook (unchanged)
curl -X POST "http://localhost:8000/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "queryResult": {
      "intent": {
        "displayName": "Report_Body_Reactions_And_Pain_Issue"
      },
      "queryText": "I have pain"
    },
    "session": "projects/test/agent/sessions/123"
  }'
```

## 🚨 Troubleshooting Enhanced System

### If You Get 503 Service Unavailable:

1. **Check Enhanced RAG Installation:**

   ```bash
   # Verify enhanced rag_service.py exists
   ls app/services/rag/rag_service.py

   # Check if enhanced function exists
   python -c "from app.services.rag.rag_service import get_refined_tip_with_rag; print('✅ Enhanced RAG loaded')"
   ```

2. **Check Environment Variables:**

   ```bash
   echo $GOOGLE_API_KEY
   # Should not be empty
   ```

3. **Check ChromaDB Path:**
   ```bash
   ls app/services/rag/ChromaDB_Parkinson_Data/
   # Should show chroma.sqlite3 and other files
   ```

### If Sources Are Still Generic:

1. **Check Enhanced System Status:**

   ```bash
   curl -X GET "http://localhost:8000/api/pain/care-tip/3" | jq '.retrieval_info.enhanced_pain_search'
   # Should be true
   ```

2. **Verify Enhanced Filtering:**

   ```bash
   curl -X GET "http://localhost:8000/api/pain/validate" | jq '.enhanced_validation_details.enhanced_filtering_active'
   # Should be true
   ```

3. **Check Source Quality:**
   ```bash
   curl -X GET "http://localhost:8000/api/pain/validate" | jq '.source_quality_metrics'
   ```

### If Relevance Scores Are Still Low:

1. **Check Average Scores:**

   ```bash
   curl -X GET "http://localhost:8000/api/pain/care-tip/3" | jq '.retrieval_info.avg_pain_relevance_score'
   # Should be >15, preferably >20
   ```

2. **Run Enhanced Validation:**
   ```bash
   curl -X GET "http://localhost:8000/api/pain/validate" | jq '.validation_score'
   # Should be >70%
   ```

## 📈 Enhanced Success Criteria

### ✅ **Excellent (85+ Quality Score)**

- All sources are pain-focused
- Relevance scores >20
- No general content retrieved
- Enhanced features fully active

### ✅ **Good (70-85 Quality Score)**

- Most sources are pain-focused
- Relevance scores >15
- Minimal general content
- Enhanced system mostly active

### ⚠️ **Needs Improvement (<70 Quality Score)**

- Mixed source quality
- Low relevance scores
- General content still appearing
- Check enhanced configuration

## 🧪 Advanced Enhanced Testing

### Test Enhanced vs Original Comparison:

```bash
# Check if enhanced system is actually being used
curl -s "http://localhost:8000/api/pain/care-tip/3" | jq '.retrieval_info.enhanced_pain_search, .retrieval_info.avg_pain_relevance_score'
```

### Enhanced Performance Testing:

```bash
# Test response times for enhanced system
time curl -s "http://localhost:8000/api/pain/care-tip/3" > /dev/null
```

### Enhanced Batch Validation:

```bash
# Run comprehensive enhanced validation
curl -X GET "http://localhost:8000/api/pain/validate" | jq '.recommendations[]'
```

### Test Enhanced Quality Across All Severities:

```bash
for i in {1..5}; do
  echo "Testing enhanced severity $i:"
  curl -s "http://localhost:8000/api/pain/care-tip/$i" | jq '.retrieval_info.avg_pain_relevance_score'
done
```

## 🔍 What Changed vs Original

### Enhanced Improvements:

- **Source Quality**: Pain-specific instead of general PD content
- **Relevance Scores**: 20+ instead of 5
- **Content Filtering**: Strict pain-focus validation
- **AI Responses**: Evidence-based language
- **Quality Metrics**: Comprehensive validation

### What Stayed the Same:

- **Colleague's Webhook**: Exactly preserved, no changes
- **API URLs**: Same endpoints, enhanced functionality
- **FastAPI Docs**: Same location, enhanced endpoints
- **Basic Structure**: Your colleague's code untouched

## 📞 Getting Enhanced Help

If enhanced tests fail:

1. **Check the enhanced validation endpoint** for specific recommendations
2. **Compare with original system** using validation metrics
3. **Verify enhanced rag_service.py** is properly installed
4. **Check logs** for enhanced system initialization

## 🎯 Quick Enhanced Validation

```bash
# One-command enhanced system check
curl -s "http://localhost:8000/api/pain/validate" | jq '.validation_passed, .validation_score, .system_status'
```

**Expected Enhanced Result:**

```json
true
"85.2%"
"EXCELLENT"
```

Your enhanced system should now provide significantly better pain-focused results while keeping your colleague's webhook code exactly as they wrote it!
