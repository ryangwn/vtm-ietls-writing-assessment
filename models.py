from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict

class IELTSTask1Criteria(BaseModel):
    task_achievement: float = Field(..., ge=0, le=9, description="Score for Task Achievement (0-9)")
    coherence_cohesion: float = Field(..., ge=0, le=9, description="Score for Coherence and Cohesion (0-9)")
    lexical_resource: float = Field(..., ge=0, le=9, description="Score for Lexical Resource (0-9)")
    grammatical_range: float = Field(..., ge=0, le=9, description="Score for Grammatical Range and Accuracy (0-9)")
    
    def overall_score(self) -> float:
        """Calculate the overall band score as the average of the four criteria."""
        return round((self.task_achievement + self.coherence_cohesion + 
                     self.lexical_resource + self.grammatical_range) / 4, 1)

class IELTSTask2Criteria(BaseModel):
    task_achievement: float = Field(..., ge=0, le=9, description="Score for Task Achievement (0-9)")
    coherence_cohesion: float = Field(..., ge=0, le=9, description="Score for Coherence and Cohesion (0-9)")
    lexical_resource: float = Field(..., ge=0, le=9, description="Score for Lexical Resource (0-9)")
    grammatical_range: float = Field(..., ge=0, le=9, description="Score for Grammatical Range and Accuracy (0-9)")
    
    def overall_score(self) -> float:
        """Calculate the overall band score as the average of the four criteria."""
        return round((self.task_achievement + self.coherence_cohesion + 
                     self.lexical_resource + self.grammatical_range) / 4, 1)

class RepetitiveWordsAnalysis(BaseModel):
    words: Dict[str, int] = Field(..., description="Dictionary of most frequently used words and their counts")
    impact: str = Field(..., description="Analysis of how word repetition impacts the essay quality")
    suggestions: List[str] = Field(..., description="Suggestions to improve vocabulary variety")

class DetailedAnalysis(BaseModel):
    summary: str = Field(..., description="Overall analysis summary of the essay")
    task_achievement_analysis: Optional[str] = Field(None, description="Detailed analysis of task achievement (Task 1)")
    task_achievement_analysis: Optional[str] = Field(None, description="Detailed analysis of task achievement (Task 2)")
    coherence_cohesion_analysis: str = Field(..., description="Detailed analysis of coherence and cohesion")
    lexical_resource_analysis: str = Field(..., description="Detailed analysis of lexical resource")
    grammatical_range_analysis: str = Field(..., description="Detailed analysis of grammatical range and accuracy")

class IELTSFeedback(BaseModel):
    strengths: List[str] = Field(..., description="List of strengths in the writing")
    areas_for_improvement: List[str] = Field(..., description="List of areas that need improvement")
    suggestions: List[str] = Field(..., description="Suggestions for improvement")

class IELTSTask1Score(BaseModel):
    criteria: IELTSTask1Criteria
    feedback: IELTSFeedback
    # repetitive_words: Optional[RepetitiveWordsAnalysis] = None
    detailed_analysis: Optional[DetailedAnalysis] = None
    overall_band: float = Field(..., ge=0, le=9, description="Overall band score (0-9)")

class IELTSTask2Score(BaseModel):
    criteria: IELTSTask2Criteria
    feedback: IELTSFeedback
    # repetitive_words: Optional[RepetitiveWordsAnalysis] = None
    detailed_analysis: Optional[DetailedAnalysis] = None
    overall_band: float = Field(..., ge=0, le=9, description="Overall band score (0-9)")

class IELTSWritingSubmission(BaseModel):
    task_type: Literal["task1", "task2"]
    prompt: str
    essay: str
    word_count: Optional[int] = None
