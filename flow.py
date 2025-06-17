from utils.pocketflow import Flow
from nodes import GetIELTSSubmissionNode, IELTSScoreNode, DisplayScoreNode

def create_ielts_scoring_flow():
    """Create and return an IELTS writing scoring flow."""
    # Create nodes
    get_submission_node = GetIELTSSubmissionNode()
    score_node = IELTSScoreNode()
    display_node = DisplayScoreNode()
    
    # Connect nodes in sequence
    get_submission_node >> score_node >> display_node
    
    # Create flow starting with input node
    return Flow(start=get_submission_node)

ielts_scoring_flow = create_ielts_scoring_flow()
