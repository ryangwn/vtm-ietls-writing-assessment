from utils.pocketflow import Node
from utils.call_llm import call_llm
from utils.common import count_words, extract_json_from_llm_response, analyze_repetitive_words
from models import IELTSTask1Score, IELTSTask2Score, IELTSWritingSubmission
from prompts import TASK1_SCORING_PROMPT, TASK2_SCORING_PROMPT
import json

class GetIELTSSubmissionNode(Node):
    """Node to collect IELTS writing submission from the user."""
    def exec(self, _):
        task_type = input("Enter task type (1 or 2): ")
        while task_type not in ["1", "2"]:
            task_type = input("Enter task type (1 or 2): ")
        
        prompt = input("Enter the writing prompt: ")
        
        print("\nEnter your essay (type 'END' on a new line when finished):\n")
        essay_lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            essay_lines.append(line)
        
        essay = "\n".join(essay_lines)
        
        return {
            "task_type": "task1" if task_type == "1" else "task2",
            "prompt": prompt,
            "essay": essay
        }
    
    def post(self, shared, prep_res, exec_res):
        # Store the submission in shared
        submission = IELTSWritingSubmission(
            task_type=exec_res["task_type"],
            prompt=exec_res["prompt"],
            essay=exec_res["essay"],
            word_count=count_words(exec_res["essay"])
        )
        shared["submission"] = submission
        return "default"  # Go to the next node

class IELTSScoreNode(Node):
    """Node to score IELTS writing submission."""
    def prep(self, shared):
        # Read submission from shared
        return shared["submission"]
    
    def exec(self, submission):
        # Perform repetitive words analysis
        # repetitive_words = analyze_repetitive_words(submission.essay, top_n=10, min_word_length=3)
        
        # Convert to dictionary format for JSON
        # repetitive_words_dict = {word: count for word, count in repetitive_words}
        
        # Select the appropriate prompt based on task type
        if submission.task_type == "task1":
            prompt_template = TASK1_SCORING_PROMPT
        else:
            prompt_template = TASK2_SCORING_PROMPT
        
        # Format the prompt with the submission details
        formatted_prompt = prompt_template.format(
            prompt=submission.prompt,
            essay=submission.essay,
            word_count=submission.word_count
        )
        
        # Call LLM to get the score
        response = call_llm(formatted_prompt)
        
        # Extract and parse the JSON response
        score_data = extract_json_from_llm_response(response)
        
        if not score_data:
            raise ValueError("Failed to parse LLM response as JSON")
        
        # If the LLM didn't provide repetitive words analysis, add our own
        # if "repetitive_words" not in score_data or not score_data["repetitive_words"]:
        #     score_data["repetitive_words"] = {
        #         "words": repetitive_words_dict,
        #         "impact": "The essay shows some repetition of key terms which may affect the lexical resource score.",
        #         "suggestions": [
        #             "Use a wider range of vocabulary to express similar concepts",
        #             "Employ synonyms to avoid repetition of the same words",
        #             "Consider using more specific and precise terminology where appropriate"
        #         ]
        #     }
            
        # Return the score data
        return {
            "task_type": submission.task_type,
            "score_data": score_data,
            "raw_response": response
        }
    
    def post(self, shared, prep_res, exec_res):
        # Store the score in shared
        if exec_res["task_type"] == "task1":
            score = IELTSTask1Score(**exec_res["score_data"])
        else:
            score = IELTSTask2Score(**exec_res["score_data"])
        
        shared["score"] = score
        shared["raw_response"] = exec_res["raw_response"]
        return "default"

class DisplayScoreNode(Node):
    """Node to display IELTS writing score."""
    def prep(self, shared):
        # Read score from shared
        return {
            "submission": shared["submission"],
            "score": shared["score"]
        }
    
    def exec(self, data):
        submission = data["submission"]
        score = data["score"]
        
        # Prepare the display output
        output = []
        output.append("\n" + "=" * 50)
        output.append("IELTS WRITING SCORE REPORT")
        output.append("=" * 50)
        
        output.append(f"\nTask Type: {'Task 1' if submission.task_type == 'task1' else 'Task 2'}")
        output.append(f"Word Count: {submission.word_count}")
        output.append(f"\nOverall Band Score: {score.overall_band}")
        
        output.append("\nDetailed Criteria Scores and Comments:")
        
        # Task Achievement/Response
        output.append(f"\n  Task Achievement: {score.criteria.task_achievement}")

        # if submission.task_type == "task1":
        #     output.append("  " + "-" * 50)
        #     output.append("  • Addresses the requirements of the task")
        #     output.append("  • Presents and highlights key features")
        #     output.append("  • Presents a clear overview of trends/differences")
        #     if score.criteria.task_achievement >= 7.0:
        #         output.append("  ✓ Covers all requirements with relevant, accurate content")
        #     elif score.criteria.task_achievement >= 6.0:
        #         output.append("  ⚠ Some irrelevant/inaccurate information or missing details")
        #     else:
        #         output.append("  ✗ Limited coverage of key features with inaccuracies")
        # else:  # task2
        #     output.append(f"\n  Task Achievement: {score.criteria.task_achievement}")
        #     output.append("  " + "-" * 50)
        #     output.append("  • Addresses all parts of the task")
        #     output.append("  • Presents a clear position/argument")
        #     output.append("  • Develops ideas with relevant examples")
        #     if score.criteria.task_achievement >= 7.0:
        #         output.append("  ✓ Addresses all parts with relevant, extended ideas")
        #     elif score.criteria.task_achievement >= 6.0:
        #         output.append("  ⚠ Addresses main parts but with some irrelevant/underdeveloped points")
        #     else:
        #         output.append("  ✗ Limited response with inadequate development of ideas")
        
        # Coherence & Cohesion
        output.append(f"\n  Coherence & Cohesion: {score.criteria.coherence_cohesion}")

        # output.append("  " + "-" * 50)
        # output.append("  • Logical organization and progression")
        # output.append("  • Appropriate use of cohesive devices")
        # output.append("  • Effective paragraphing")
        # if score.criteria.coherence_cohesion >= 7.0:
        #     output.append("  ✓ Logically organized with good use of cohesive devices")
        # elif score.criteria.coherence_cohesion >= 6.0:
        #     output.append("  ⚠ Generally coherent but with some mechanical/faulty cohesion")
        # else:
        #     output.append("  ✗ Lacks clear progression with inadequate cohesive devices")
        
        # Lexical Resource
        output.append(f"\n  Lexical Resource: {score.criteria.lexical_resource}")
        # output.append("  " + "-" * 50)
        # output.append("  • Range and accuracy of vocabulary")
        # output.append("  • Use of less common and idiomatic vocabulary")
        # output.append("  • Spelling and word formation")
        # if score.criteria.lexical_resource >= 7.0:
        #     output.append("  ✓ Good range of vocabulary with flexibility and precision")
        # elif score.criteria.lexical_resource >= 6.0:
        #     output.append("  ⚠ Adequate vocabulary but limited range or precision")
        # else:
        #     output.append("  ✗ Limited vocabulary with frequent errors in word choice/spelling")
        
        # Grammatical Range & Accuracy
        output.append(f"\n  Grammatical Range & Accuracy: {score.criteria.grammatical_range}")
        
        # output.append("  " + "-" * 50)
        # output.append("  • Range and accuracy of grammatical structures")
        # output.append("  • Sentence variety and complexity")
        # output.append("  • Punctuation")
        # if score.criteria.grammatical_range >= 7.0:
        #     output.append("  ✓ Good range of structures with accuracy and flexibility")
        # elif score.criteria.grammatical_range >= 6.0:
        #     output.append("  ⚠ Mix of simple and complex structures with some errors")
        # else:
        #     output.append("  ✗ Limited range of structures with frequent errors")      
        
        output.append("\nStrengths:")
        for i, strength in enumerate(score.feedback.strengths, 1):
            output.append(f"  {i}. {strength}")
        
        output.append("\nAreas for Improvement:")
        for i, area in enumerate(score.feedback.areas_for_improvement, 1):
            output.append(f"  {i}. {area}")
        
        output.append("\nSuggestions:")
        for i, suggestion in enumerate(score.feedback.suggestions, 1):
            output.append(f"  {i}. {suggestion}")
        
        # Display repetitive words analysis if available
        # if score.repetitive_words:
        #     output.append("\n" + "=" * 50)
        #     output.append("REPETITIVE WORDS ANALYSIS")
        #     output.append("=" * 50)
            
        #     # Display most frequent words and their counts
        #     output.append("\nMost Frequently Used Words:")
        #     for word, count in score.repetitive_words.words.items():
        #         output.append(f"  • '{word}': {count} times")
            
        #     # Display impact analysis
        #     output.append("\nImpact on Essay Quality:")
        #     output.append(f"  {score.repetitive_words.impact}")
            
        #     # Display suggestions for vocabulary improvement
        #     output.append("\nSuggestions for Vocabulary Improvement:")
        #     for i, suggestion in enumerate(score.repetitive_words.suggestions, 1):
        #         output.append(f"  {i}. {suggestion}")
        
        # Display detailed analysis if available
        if score.detailed_analysis:
            output.append("\n" + "=" * 50)
            output.append("DETAILED ANALYSIS")
            output.append("=" * 50)
            
            # Display overall summary
            output.append("\nOverall Summary:")
            output.append(f"  {score.detailed_analysis.summary}")
            
            # Display task achievement/response analysis
            if submission.task_type == "task1":
                output.append("\nTask Achievement Analysis:")
                output.append(f"  {score.detailed_analysis.task_achievement_analysis}")
            else:  # task2
                output.append("\nTask Achievement Analysis:")
                output.append(f"  {score.detailed_analysis.task_achievement_analysis}")
            
            # Display coherence and cohesion analysis
            output.append("\nCoherence & Cohesion Analysis:")
            output.append(f"  {score.detailed_analysis.coherence_cohesion_analysis}")
            
            # Display lexical resource analysis
            output.append("\nLexical Resource Analysis:")
            output.append(f"  {score.detailed_analysis.lexical_resource_analysis}")
            
            # Display grammatical range analysis
            output.append("\nGrammatical Range & Accuracy Analysis:")
            output.append(f"  {score.detailed_analysis.grammatical_range_analysis}")
        
        output.append("\n" + "=" * 50)
        
        return "\n".join(output)
    
    def post(self, shared, prep_res, exec_res):
        # Store the display output in shared
        shared["display_output"] = exec_res
        return "default"  # Go to the next node
