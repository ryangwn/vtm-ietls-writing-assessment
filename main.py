from dotenv import load_dotenv
load_dotenv()

from flow import create_ielts_scoring_flow

def main():
    """Main function to run the IELTS Writing Scoring system."""
    print("\n" + "=" * 50)
    print("IELTS WRITING SCORING SYSTEM")
    print("=" * 50)
    print("\nWelcome to the IELTS Writing Scoring System!")
    print("This system will evaluate your IELTS writing task and provide feedback.")
    print("\nInstructions:")
    print("1. Select the task type (Task 1 or Task 2)")
    print("2. Enter the writing prompt/question")
    print("3. Enter your essay (type 'END' on a new line when finished)")
    print("4. Wait for the system to evaluate your writing")
    print("\nLet's get started!\n")
    
    # Initialize shared data
    shared = {}
    
    # Create and run the IELTS scoring flow
    ielts_flow = create_ielts_scoring_flow()
    ielts_flow.run(shared)
    
    print(shared["display_output"])

if __name__ == "__main__":
    main()
