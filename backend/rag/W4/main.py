from Crew import legal_crew

def main():
    print("=" * 60)
    print("        JuristiQ - AI Legal Assistant")
    print("=" * 60)

    while True:
        question = input("\nAsk your legal question (or type 'exit' to quit):\n> ")

        if question.lower() in ["exit", "quit"]:
            print("\nThank you for using JuristiQ!")
            break

        print("\nAnalyzing your query...\n")

        try:
            result = legal_crew.kickoff(
                inputs={
                    "question": question
                }
            )

            print("\n" + "=" * 60)
            print("FINAL LEGAL RESPONSE")
            print("=" * 60)
            print(result)

        except Exception as e:
            print("\nAn error occurred:")
            print(e)


if __name__ == "__main__":
    main()