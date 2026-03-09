"""
Educational Video Generator
Creates animated explainer videos from text prompts using LLMs, Manim, and TTS.
"""

import sys
import os

from dotenv import load_dotenv
load_dotenv()
print("DEBUG LLM_PROVIDER:", os.getenv("LLM_PROVIDER"))

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline import VideoPipeline

def main():
    # Load environment variables only from .env file
    load_dotenv(override=True)
    
    print("\n" + "="*70)
    print(" EDUCATIONAL VIDEO GENERATOR")
    print("="*70 + "\n")
    
    # Get topic from user
    topic = input("📝 Enter the topic for your video: ").strip()
    if not topic:
        print("❌ No topic provided. Exiting.")
        return 1
    
    # Get number of sections
    while True:
        try:
            num_sections_input = input("📊 How many sections? (default: 3): ").strip()
            if not num_sections_input:
                num_sections = 3
                break
            num_sections = int(num_sections_input)
            if num_sections < 1:
                print("⚠️  Please enter a number greater than 0")
                continue
            if num_sections > 10:
                print("⚠️  Warning: More than 10 sections may take a very long time!")
                confirm = input("Continue anyway? (y/n): ").strip().lower()
                if confirm != 'y':
                    continue
            break
        except ValueError:
            print("⚠️  Please enter a valid number")
    
    # Confirm settings
    print("\n" + "="*70)
    print("📋 CONFIGURATION SUMMARY")
    print("="*70)
    print(f"Topic: {topic}")
    print(f"Sections: {num_sections}")
    print("="*70)
    
    confirm = input("\n▶️  Start video generation? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled.")
        return 0
    
    # Run the pipeline
    print("\n🚀 Starting pipeline...\n")
    pipeline = VideoPipeline()
    result = pipeline.run(
        topic=topic,
        num_sections=num_sections
    )
    
       # Print results
    print("\n" + "="*70)
    print("🎯 FINAL RESULT")
    print("="*70)

    if result.get("success"):
        print("✅ Success! Video created at:")
        print(f"   📁 {result['final_video']}")
    else:
        print("❌ Failed to create video")
        print(f"   Error: {result.get('error')}")

    print("="*70 + "\n")

    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
