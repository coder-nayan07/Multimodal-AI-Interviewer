import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.parsers.jd_parser import JobDescriptionParser


def main():
    parser = JobDescriptionParser()

    jd = parser.parse("data/JD.txt")

    print("=" * 80)
    print("FILE:", jd.file_name)

    print("\nFIRST 1000 CHARACTERS\n")
    print(jd.cleaned_text[:1000])

    print("\n")
    print("=" * 80)
    print(f"Total Length: {len(jd.cleaned_text)} characters")


if __name__ == "__main__":
    main()