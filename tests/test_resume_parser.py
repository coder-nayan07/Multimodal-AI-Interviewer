import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.parsers.resume_parser import ResumeParser


def main():
    parser = ResumeParser()

    resume = parser.parse("data/NAYAN_.pdf")

    print("=" * 80)
    print("FILE:", resume.file_name)

    print("\nDetected Sections:\n")

    for section in resume.sections.keys():
        print(section)

    print("\n" + "=" * 80)

    for section, content in resume.sections.items():
        print(f"\n[{section.upper()}]\n")
        print(content)


if __name__ == "__main__":
    main()