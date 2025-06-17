# IELTS Writing Scoring CREtical Agent

An AI-powered system for scoring and providing feedback on IELTS Writing Task 1 and Task 2 submissions.

## Overview

This system uses a flow-based architecture to process IELTS writing submissions, evaluate them according to official IELTS criteria, and provide detailed feedback to help test-takers improve their writing skills.

## Features

- Support for both Task 1 and Task 2 writing submissions
- Detailed scoring based on official IELTS criteria
- Comprehensive feedback including strengths, areas for improvement, and specific suggestions
- Word count calculation
- User-friendly command-line interface

## IELTS Scoring Criteria

### Task 1 Criteria
- Task Achievement (0-9)
- Coherence and Cohesion (0-9)
- Lexical Resource (0-9)
- Grammatical Range and Accuracy (0-9)

### Task 2 Criteria
- Task Response (0-9)
- Coherence and Cohesion (0-9)
- Lexical Resource (0-9)
- Grammatical Range and Accuracy (0-9)

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   cp .env.example .env
   ```
   ```
   LLM_TYPE=gemini
   GEMINI_API_KEY=your-api-key-here
   ```

## Usage

Run the main script to start the IELTS Writing Scoring system:

```
python main.py
```

Follow the on-screen instructions to:
1. Select the task type (Task 1 or Task 2)
2. Enter the writing prompt/question
3. Enter your essay (type 'END' on a new line when finished)
4. Receive detailed feedback and scoring

## System Architecture

The system uses a flow-based architecture with the following components:

```mermaid
flowchart LR
    submission[Get Submission] --> scoring[Score Essay]
    scoring --> display[Display Results]
```

### Nodes

1. **GetIELTSSubmissionNode**: Collects the task type, prompt, and essay from the user
2. **IELTSScoreNode**: Evaluates the submission using LLM-based scoring
3. **DisplayScoreNode**: Formats and displays the scoring results

## Dependencies

- openai>=1.0.0
- python-dotenv>=1.0.0
- pydantic>=2.0.0

## License

MIT
