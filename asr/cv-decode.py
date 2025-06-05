import argparse
import os
import time
from typing import List

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def process_files_batch(file_paths: List[str]) -> List[dict]:
    """Process a batch of audio files using the ASR API.

    Args:
        file_paths (List[str]): List of paths to audio files to be processed

    Returns:
        List[dict]: List of dictionaries containing transcription results.
                   Each dictionary has keys:
                   - 'transcription': The transcribed text (str)
                   - 'duration': The duration of the audio (str)
                   If processing fails, returns empty strings for both fields.
    """
    try:
        files_list = []
        for file_path in file_paths:
            with open(file_path, "rb") as f:
                file_content = f.read()
                files_list.append(
                    ("files", (os.path.basename(file_path), file_content, "audio/mpeg"))
                )

        response = requests.post(
            "http://localhost:8001/asr", files=files_list, timeout=60
        )

        if response.status_code == 200:
            results = response.json()
            return results

        else:
            print(f"Error processing batch: {response.status_code}")
            return [{"transcription": "", "duration": ""} for _ in file_paths]

    except requests.exceptions.Timeout:
        print("Timeout error processing batch after 60s")
        return [{"transcription": "", "duration": ""} for _ in file_paths]


def decode_audio_files(path: str, save_csv_file_name: str) -> None:
    """Process audio files in a directory and save transcription results to CSV.

    Args:
        path (str): Path to directory containing audio files to transcribe
        save_csv_file_name (str): Path to CSV file to save transcription results.
            The CSV file should already exist and contain a 'filename' column.
            Results will be added in 'generated_text' and 'duration' columns.

    Returns:
        None: Results are saved directly to the CSV file.

    Note:
        Successfully transcribed audio files will be deleted after processing.
    """

    results_dict = {}
    batch_size = int(os.getenv("BATCH_SIZE", 20))

    existing_df = pd.read_csv(save_csv_file_name)
    if "filename" not in existing_df.columns:
        print("Column 'filename' is not present in target csv file")

    else:
        if not os.path.isdir(path):
            print(f"Path not found: {path}")

        else:
            audio_files = [os.path.join(path, f) for f in os.listdir(path)]
            total_files = len(audio_files)
            total_batches = (total_files + batch_size - 1) // batch_size
            print(
                f"Found {total_files} audio files to process in {total_batches} batches."
            )

            for i in range(0, len(audio_files), batch_size):
                batch_num = (i // batch_size) + 1
                batch_files = audio_files[i : i + batch_size]
                print(f"Processing batch {batch_num}/{total_batches}...\n")

                batch_results = process_files_batch(batch_files)

                for j, filename in enumerate(batch_files):
                    transcription = batch_results[j]["transcription"]
                    duration = batch_results[j]["duration"]
                    if transcription != "" and duration != "":
                        os.remove(
                            filename
                        )  # deleting the file if transcription is successful (text generated with duration)

                    results_dict[filename] = {
                        "generated_text": transcription,
                        "duration": duration,
                    }

            time.sleep(0.1)

            # Updating existing df with generated texts and durations
            for index, row in existing_df.iterrows():
                filename = row["filename"]
                if filename in results_dict:
                    existing_df.at[index, "generated_text"] = results_dict[filename][
                        "generated_text"
                    ]
                    existing_df.at[index, "duration"] = results_dict[filename][
                        "duration"
                    ]

            existing_df.to_csv(save_csv_file_name, index=False)

            print(
                f"CSV file {save_csv_file_name} updated with generated text and durations."
            )


if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str, help="Path to directory containing audio files to transcribe"
    )
    parser.add_argument(
        "save_csv_file_name",
        type=str,
        help="Path to CSV file to save transcription results",
    )
    args = parser.parse_args()
    decode_audio_files(path=args.path, save_csv_file_name=args.save_csv_file_name)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTotal time elapsed: {elapsed_time:.2f} seconds")
