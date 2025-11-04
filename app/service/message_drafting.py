import os
from typing import Dict, List, Optional
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from fastapi import HTTPException
import json

# Import existing query functions
from .query import query_message, get_doctor_info, get_practice_detail

# Initialize LLMs with fallback
def get_cerebras_llm():
    """Get Cerebras LLM - TODO: Implement when cerebras-cloud-sdk LangChain integration is available"""
    # For now, we'll use Gemini as primary since Cerebras LangChain integration may need custom setup
    pass

def get_gemini_llm():
    """Get Gemini LLM"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not found in environment")
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        temperature=0.7,
        google_api_key=api_key
    )

def get_primary_llm():
    """Get primary LLM (Cerebras) with Gemini fallback"""
    try:
        # Try Cerebras first
        # cerebras_llm = get_cerebras_llm()
        # return cerebras_llm
        # For now, use Gemini as primary until Cerebras integration is set up
        return get_gemini_llm()
    except Exception as e:
        # Fallback to Gemini
        print(f"Cerebras failed, using Gemini: {e}")
        return get_gemini_llm()

def get_fallback_llm():
    """Get fallback LLM (Gemini)"""
    return get_gemini_llm()

# Template definitions
DEFAULT_TEMPLATE = """{session_id}
{date_formatted}
{practice_name}, {practice_postcode}

Hi

Thank you for your request. If the terms are acceptable, please feel free to request Dr.

Start time: {start_time}
End time: {end_time}
Rate: £{pricing} per hr

Remote only

Dr. {doctor_last_name} is one of the most requested doctors on Lantum, having worked in over 300 practices. Please see Dr's profile for further details and the glowing testimonials.

Remote service is great for last-minute coverage or enhancing access. Dr can see many patients remotely, freeing up on-site partners.

Services include triage, advice, prescriptions, medication reviews, weaning controlled meds, admin sessions, MED3 reviews, mental health & dermatology appts, prescription queries, referrals, and extended access.

Please ignore our applications if terms don't suit you -with bulk bookings, is difficult to filter practices on Lantum.

For last-minute bookings, call/text 07515393107 or 07842557072, as we may miss Lantum notifications.

Thanks,

Juliana (Dr's PA)

On Behalf of:"""

RAPPORT_TEMPLATE = """NOTE: This application is being submitted by Gibril, Dr. {doctor_last_name}'s assistant. Dr. {doctor_last_name} only provides remote GP services via secure NHS N3 connection. She is one of the most requested and recognized doctors on Lantum with extensive experience in remote consultations. Dr. {doctor_last_name} offers efficient patient triage and remote care to help manage your list. If this remote arrangement works for your practice needs, please go ahead and accept. However, if on-site presence is essential, we completely understand that I won't be suitable on this occasion. Please review her profile for more information about her excellent track record. For questions: 07515393107 - Gibril (Assistant to Dr. {doctor_last_name})."""

# Agent Tools
def create_tools():
    """Create LangChain tools for the agent"""
    
    def analyze_sentiment(messages: str) -> str:
        """Analyze message history to determine sentiment and rapport level.
        
        Args:
            messages: JSON string of message history
            
        Returns:
            JSON string with sentiment analysis
        """
        try:
            msg_data = json.loads(messages)
            messages_list = msg_data.get('messages', [])
            summary = msg_data.get('summary', {})
            
            # Check if practice replied
            has_reply = summary.get('messages_received', 0) > 0
            
            # Analyze last practice reply if exists
            sentiment = "none"
            rapport_level = "low"
            
            if has_reply:
                # Find last practice reply (where user_id != doctor_id)
                practice_replies = [
                    msg for msg in messages_list 
                    if msg.get('user_id') != msg.get('doctor_id')
                ]
                
                if practice_replies:
                    last_reply = practice_replies[-1].get('body', '').lower()
                    
                    # Simple sentiment analysis
                    positive_words = ['thanks', 'thank you', 'accepted', 'great', 'excellent', 'perfect', 'yes', 'interested']
                    negative_words = ['no', 'not interested', 'decline', 'reject', 'unavailable', 'sorry']
                    
                    if any(word in last_reply for word in positive_words):
                        sentiment = "positive"
                        rapport_level = "high"
                    elif any(word in last_reply for word in negative_words):
                        sentiment = "negative"
                        rapport_level = "low"
                    else:
                        sentiment = "neutral"
                        rapport_level = "medium"
            
            result = {
                "has_reply": has_reply,
                "sentiment": sentiment,
                "rapport_level": rapport_level,
                "messages_sent": summary.get('messages_sent', 0),
                "messages_received": summary.get('messages_received', 0)
            }
            
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e), "sentiment": "unknown", "rapport_level": "low"})
    
    def select_template(analysis: str) -> str:
        """Select appropriate template based on sentiment analysis.
        
        Args:
            analysis: JSON string from analyze_sentiment
            
        Returns:
            Template type: 'rapport' or 'default'
        """
        try:
            analysis_data = json.loads(analysis)
            sentiment = analysis_data.get('sentiment', 'none')
            rapport_level = analysis_data.get('rapport_level', 'low')
            
            if sentiment == "positive" and rapport_level in ["high", "medium"]:
                return "rapport"
            else:
                return "default"
        except Exception as e:
            return "default"
    
    def draft_message(template_type: str, job_details: str) -> str:
        """Draft message using selected template.
        
        Args:
            template_type: 'rapport' or 'default'
            job_details: JSON string with job information
            
        Returns:
            Drafted message string
        """
        try:
            details = json.loads(job_details)
            template = RAPPORT_TEMPLATE if template_type == "rapport" else DEFAULT_TEMPLATE
            
            # Format date
            from datetime import datetime
            date_obj = datetime.strptime(details.get('date', ''), '%Y-%m-%d')
            date_formatted = date_obj.strftime('%a %d, %b')
            
            # Get doctor last name
            doctor_last_name = details.get('doctor_last_name', 'Doctor')
            
            # Format message
            message = template.format(
                session_id=details.get('session_id', ''),
                date_formatted=date_formatted,
                practice_name=details.get('practice_name', ''),
                practice_postcode=details.get('practice_postcode', ''),
                start_time=details.get('start_time', ''),
                end_time=details.get('end_time', ''),
                pricing=details.get('pricing', ''),
                doctor_last_name=doctor_last_name
            )
            
            return message
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error drafting message: {e}")
    
    return [
        Tool(
            name="analyze_sentiment",
            func=analyze_sentiment,
            description="Analyze message history to determine sentiment (positive/negative/none) and rapport level (high/medium/low). Input: JSON string of messages with summary."
        ),
        Tool(
            name="select_template",
            func=select_template,
            description="Select template type based on sentiment analysis. Returns 'rapport' for positive sentiment with good rapport, 'default' otherwise. Input: JSON string from analyze_sentiment."
        ),
        Tool(
            name="draft_message",
            func=draft_message,
            description="Draft message using selected template. Input: template_type ('rapport' or 'default') and job_details JSON string with session_id, date, practice_name, practice_postcode, start_time, end_time, pricing, doctor_last_name."
        )
    ]

async def run_agent_workflow(llm, messages_json: str, job_details_json: str) -> str:
    """
    Run agent workflow using LLM with tools.
    Since Gemini doesn't support function calling like OpenAI, we'll use a simpler approach.
    """
    
    tools = create_tools()
    
    # Step 1: Analyze sentiment
    sentiment_result = tools[0].func(messages_json)
    
    # Step 2: Select template
    template_type = tools[1].func(sentiment_result)
    
    # Step 3: Draft message
    draft = tools[2].func(template_type, job_details_json)
    
    # Step 4: Use LLM to refine/improve the draft if needed
    # Parse message history to include actual messages for context
    message_history_data = json.loads(messages_json)
    messages_list = message_history_data.get('messages', [])
    
    # Format message history for LLM context
    # Get doctor_id from job details to determine sender
    job_data = json.loads(job_details_json)
    doctor_id_from_job = job_data.get('doctor_id', None)
    
    message_context = ""
    if messages_list:
        message_context = "\n\nPrevious Message History (for context):\n"
        for msg in messages_list[-5:]:  # Include last 5 messages for context
            # Determine sender based on user_id matching doctor_id
            sender = "Doctor" if msg.get('user_id') == doctor_id_from_job else "Practice"
            body = msg.get('body', '')
            # Truncate long messages for context
            if len(body) > 200:
                body = body[:200] + "..."
            message_context += f"\n{sender}: {body}\n"
    else:
        message_context = "\n\nThis is a first-time application (no previous message history)."
    
    system_prompt = """You are an AI assistant helping refine professional messages for doctors applying to medical practices.

The message should:
- Be professional and clear
- Clearly indicate it's written "on behalf of" the doctor
- Match the tone based on previous interactions (rapport vs formal)
- Learn from successful past messages and adapt tone accordingly
- Include all necessary details (session ID, date, times, pricing)

Refine the draft message to ensure it's polished and professional, using the message history context to match the appropriate tone."""
    
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""Please review and refine this draft message. Only make minor improvements - don't change the structure or key information:

Template used: {template_type}
Sentiment analysis: {sentiment_result}
{message_context}

Draft message:
{draft}

Return only the refined message, nothing else.""")
    ])
    
    try:
        chain = prompt | llm
        result = await chain.ainvoke({})
        refined_message = result.content if hasattr(result, 'content') else str(result)
        return refined_message
    except Exception as e:
        # If LLM refinement fails, return original draft
        print(f"LLM refinement failed: {e}, returning original draft")
        return draft

async def draft_message_service(
    doctor_id: int,
    practice_id: int,
    session_id: int,
    job_description: str,
    pricing: float,
    start_time: str,
    end_time: str,
    date: str,
    practice_name: str,
    practice_postcode: str
) -> Dict:
    """
    Main service function to draft message using LangChain agent.
    
    Returns:
        Dictionary with draft_message, strategy_used, and analysis
    """
    try:
        # Get message history - handle case where no thread exists (first-time application)
        try:
            message_history = await query_message(practice_id, doctor_id)
        except HTTPException as e:
            # Check if it's a 404 (thread not found) or if detail contains "Thread not found"
            if e.status_code == 404 or "Thread not found" in str(e.detail):
                # No thread exists - this is a first-time application
                # Create empty message history structure
                message_history = {
                    "summary": {
                        "messages_sent": 0,
                        "messages_received": 0,
                        "total_messages": 0
                    },
                    "messages": []
                }
            else:
                # Re-raise other HTTP exceptions
                raise
        except Exception as e:
            # Catch any other exceptions and check for thread not found
            error_str = str(e)
            if "Thread not found" in error_str or "404" in error_str:
                # No thread exists - this is a first-time application
                message_history = {
                    "summary": {
                        "messages_sent": 0,
                        "messages_received": 0,
                        "total_messages": 0
                    },
                    "messages": []
                }
            else:
                # Re-raise other exceptions
                raise
        
        # Get doctor info
        doctor_info = await get_doctor_info(doctor_id)
        doctor_last_name = doctor_info.get('display_name', '').split()[-1] if doctor_info.get('display_name') else 'Doctor'
        
        # Get practice info (already have name and postcode, but verify)
        practice_info = await get_practice_detail(practice_id)
        
        # Prepare job details for agent
        job_details = {
            "doctor_id": doctor_id,  # Include doctor_id for message context
            "session_id": session_id,
            "date": date,
            "practice_name": practice_name or practice_info.get('name', ''),
            "practice_postcode": practice_postcode,
            "start_time": start_time,
            "end_time": end_time,
            "pricing": pricing,
            "doctor_last_name": doctor_last_name,
            "job_description": job_description
        }
        
        # Prepare data for agent
        messages_json = json.dumps(message_history)
        job_details_json = json.dumps(job_details)
        
        # Get primary LLM and run workflow
        try:
            llm = get_primary_llm()
            draft_message = await run_agent_workflow(llm, messages_json, job_details_json)
        except Exception as e:
            # Fallback to secondary LLM
            print(f"Primary LLM failed: {e}, trying fallback...")
            try:
                fallback_llm = get_fallback_llm()
                draft_message = await run_agent_workflow(fallback_llm, messages_json, job_details_json)
            except Exception as fallback_error:
                # If both fail, use tool directly without LLM refinement
                print(f"Both LLMs failed, using direct tool output: {fallback_error}")
                tools = create_tools()
                sentiment_result = tools[0].func(messages_json)
                template_type = tools[1].func(sentiment_result)
                draft_message = tools[2].func(template_type, job_details_json)
        
        # Analyze sentiment separately for response
        sentiment_result = json.loads(create_tools()[0].func(messages_json))
        template_type = create_tools()[1].func(json.dumps(sentiment_result))
        
        return {
            "draft_message": draft_message,
            "strategy_used": template_type,
            "analysis": sentiment_result,
            "session_id": session_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error drafting message: {e}")

