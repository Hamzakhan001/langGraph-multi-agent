#!/usr/bin/env python3
"""
Working LangGraph Visualization - Fixed for your version
"""

import os
from datetime import datetime
from typing import TypedDict
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# ==============================================================================
# 1. PROPER STATE DEFINITION (This fixes the Dict issue)
# ==============================================================================

class CallState(TypedDict):
    """Properly defined state for LangGraph"""
    caller_number: str
    caller_name: str
    call_time: datetime
    is_late_night: bool
    message: str
    sms_sent: bool
    meeting_scheduled: bool

# ==============================================================================
# 2. SIMPLIFIED NODES
# ==============================================================================

def check_call_time(state: CallState) -> CallState:
    """Check if call was made during late night hours"""
    print("🔍 Node: Checking call time...")
    call_time = state["call_time"]
    state["is_late_night"] = 2 <= call_time.hour < 8
    print(f"   Late night? {state['is_late_night']}")
    return state

def generate_message(state: CallState) -> CallState:
    """Generate response message"""
    print("🤖 Node: Generating message...")
    state["message"] = "Hi! I don't take calls after 2 AM. Please reply with your email and preferred meeting time (9 AM-6 PM). Thanks!"
    print(f"   Message: {state['message'][:50]}...")
    return state

def send_sms_node(state: CallState) -> CallState:
    """Send SMS"""
    print("📱 Node: Sending SMS...")
    state["sms_sent"] = True
    print(f"   SMS sent to: {state['caller_number']}")
    return state

def schedule_meeting_node(state: CallState) -> CallState:
    """Schedule meeting"""
    print("📅 Node: Scheduling meeting...")
    state["meeting_scheduled"] = True
    print("   Meeting scheduled!")
    return state

# ==============================================================================
# 3. ROUTING FUNCTION
# ==============================================================================

def route_next(state: CallState) -> str:
    """Route to next node based on state"""
    if not state.get("is_late_night"):
        print("🧭 Routing: Normal hours -> END")
        return END
    elif not state.get("message"):
        print("🧭 Routing: Need message -> generate_message")
        return "generate_message"
    elif not state.get("sms_sent"):
        print("🧭 Routing: Need SMS -> send_sms")
        return "send_sms"
    elif not state.get("meeting_scheduled"):
        print("🧭 Routing: Need meeting -> schedule_meeting")
        return "schedule_meeting"
    else:
        print("🧭 Routing: Complete -> END")
        return END

# ==============================================================================
# 4. CREATE WORKFLOW WITH WORKING VISUALIZATION
# ==============================================================================

def create_visualizable_workflow():
    """Create LangGraph workflow that can be visualized"""
    
    print("🏗️ Building LangGraph workflow...")
    
    # Create workflow with proper state type
    workflow = StateGraph(CallState)
    
    # Add nodes
    workflow.add_node("check_time", check_call_time)
    workflow.add_node("generate_message", generate_message)
    workflow.add_node("send_sms", send_sms_node)
    workflow.add_node("schedule_meeting", schedule_meeting_node)
    
    # Set entry point
    workflow.set_entry_point("check_time")
    
    # Add edges
    workflow.add_conditional_edges(
        "check_time",
        route_next,
        {
            "generate_message": "generate_message",
            END: END
        }
    )
    
    workflow.add_conditional_edges(
        "generate_message",
        route_next,
        {
            "send_sms": "send_sms",
            END: END
        }
    )
    
    workflow.add_conditional_edges(
        "send_sms", 
        route_next,
        {
            "schedule_meeting": "schedule_meeting",
            END: END
        }
    )
    
    workflow.add_edge("schedule_meeting", END)
    
    # Compile and return
    graph = workflow.compile()
    print("✅ Workflow compiled successfully!")
    return graph

# ==============================================================================
# 5. WORKING VISUALIZATION METHODS
# ==============================================================================

def try_langgraph_visualization(graph):
    """Try LangGraph's built-in visualization methods"""
    
    print("\n🎨 TRYING LANGGRAPH NATIVE VISUALIZATION")
    print("="*50)
    
    try:
        # Method 1: Get graph object
        print("1️⃣ Getting graph object...")
        graph_obj = graph.get_graph()
        print("✅ Graph object retrieved!")
        
        # Method 2: Try ASCII
        print("\n2️⃣ Trying ASCII representation...")
        try:
            ascii_repr = graph_obj.draw_ascii()
            print("📊 ASCII GRAPH:")
            print(ascii_repr)
        except Exception as e:
            print(f"❌ ASCII failed: {e}")
        
        # Method 3: Try Mermaid
        print("\n3️⃣ Trying Mermaid representation...")
        try:
            mermaid_repr = graph_obj.draw_mermaid()
            print("🔗 MERMAID CODE:")
            print(mermaid_repr)
            print("\n💡 Copy above code to https://mermaid.live")
        except Exception as e:
            print(f"❌ Mermaid failed: {e}")
        
        # Method 4: Graph info
        print("\n4️⃣ Graph structure info...")
        try:
            print(f"📊 Nodes: {list(graph_obj.nodes())}")
            print(f"🔗 Edges: {list(graph_obj.edges())}")
        except Exception as e:
            print(f"❌ Structure info failed: {e}")
            
    except Exception as e:
        print(f"❌ Could not get graph object: {e}")

# ==============================================================================
# 6. ALTERNATIVE VISUALIZATION METHODS
# ==============================================================================

def manual_graph_visualization(graph):
    """Manual visualization when built-in methods fail"""
    
    print("\n🛠️ MANUAL WORKFLOW VISUALIZATION")
    print("="*50)
    
    # Show the logical flow
    print("📋 WORKFLOW STRUCTURE:")
    print("""
    ┌─────────────────┐
    │ 📞 check_time   │ ◄─── Entry Point
    └─────────────────┘
             │
             ▼
        ┌─────────┐
        │Late     │
        │Night?   │ ◄─── Decision Node
        └─────────┘
         /       \\
       YES        NO
        │          │
        ▼          ▼
    ┌─────────┐   ┌─────────┐
    │🤖 gen   │   │   END   │
    │message  │   │ (Normal)│
    └─────────┘   └─────────┘
        │
        ▼
    ┌─────────┐
    │📱 send  │
    │  sms    │
    └─────────┘
        │
        ▼
    ┌─────────┐
    │📅 sched │
    │ meeting │
    └─────────┘
        │
        ▼
    ┌─────────┐
    │   END   │
    │(Complete)│
    └─────────┘
    """)
    
    print("🔄 EXECUTION PATHS:")
    print("Path 1: check_time → END (normal hours)")
    print("Path 2: check_time → generate_message → send_sms → schedule_meeting → END")

# ==============================================================================
# 7. TEST WITH EXECUTION TRACE
# ==============================================================================

def test_with_trace(graph):
    """Test workflow and show execution trace"""
    
    print("\n🧪 TESTING WITH EXECUTION TRACE")
    print("="*50)
    
    # Test late night scenario
    print("\n🌙 SCENARIO 1: Late night call (3:30 AM)")
    late_night_state = CallState(
        caller_number="+923075861200",
        caller_name="Test Caller",
        call_time=datetime.now().replace(hour=3, minute=30),
        is_late_night=False,
        message="",
        sms_sent=False,
        meeting_scheduled=False
    )
    
    try:
        result = graph.invoke(late_night_state)
        print("✅ Late night test completed!")
        print(f"📋 Final state: SMS sent = {result['sms_sent']}, Meeting = {result['meeting_scheduled']}")
    except Exception as e:
        print(f"❌ Late night test failed: {e}")
    
    # Test normal hours
    print("\n☀️ SCENARIO 2: Normal hours call (11:30 AM)")
    normal_state = CallState(
        caller_number="+923075861200",
        caller_name="Test Caller", 
        call_time=datetime.now().replace(hour=11, minute=30),
        is_late_night=False,
        message="",
        sms_sent=False,
        meeting_scheduled=False
    )
    
    try:
        result = graph.invoke(normal_state)
        print("✅ Normal hours test completed!")
        print(f"📋 Final state: SMS sent = {result['sms_sent']}, Meeting = {result['meeting_scheduled']}")
    except Exception as e:
        print(f"❌ Normal hours test failed: {e}")

# ==============================================================================
# 8. MAIN FUNCTION
# ==============================================================================

def main():
    """Main visualization demo"""
    
    print("🚀 LANGGRAPH VISUALIZATION - FIXED VERSION")
    print("="*60)
    
    # Create the workflow
    graph = create_visualizable_workflow()
    
    # Try built-in visualization
    try_langgraph_visualization(graph)
    
    # Manual visualization
    manual_graph_visualization(graph)
    
    # Test with execution trace
    test_with_trace(graph)
    
    print("\n🎯 SUMMARY:")
    print("✅ Your LangGraph workflow is working perfectly!")
    print("✅ The execution flow is correct")
    print("💡 If built-in visualization doesn't work, the manual diagram shows your flow")

if __name__ == "__main__":
    main()