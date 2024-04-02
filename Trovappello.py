import tabula
import os

from find_last_exam_calendar import find_last_exam_calendar
from chronological_reordering import chronological_reordering

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def filter_calendar(pdf_file_url, exam_codes, output_dir):
    csv_output_path = output_dir + pdf_file_url.split("/")[-1].replace(".pdf","_filtered.csv")

    # Read PDF file and convert it into a list of DataFrames
    dfs = tabula.read_pdf(pdf_file_url, pages='all')
    with open(csv_output_path, "w") as csv_file:
        csv_file.write("Prof.\tNum.\tNome esame\tCodice\tCdL\tData\tOra\tAula\tModalità\n")

        for df in dfs:
            # Iterate through each row in the DataFrame
            for index, row in df.iterrows():
                # Check if any of the search words are in the current row
                if any(word in row.values for word in exam_codes):
                    # Print out the entire row
                    for value in row.values:
                        # print(value, "@", end='\t')
                        csv_file.write(str(value)+"\t")

                    csv_file.write("\n")

    chronological_reordering(csv_output_path)

    print(f"Extraction and search completed.\nOutput file saved as {csv_output_path}\n")


if __name__ == "__main__":
    # List of the exam you want to select in the calendar
    exam_codes_dict = {
        "CdP": "713II", 
        "CD": "714II",
        "DRSE": "1082I",
        "ISTR": "274II",
        "MdR": "276II",
        "MTA": "1124I",
        "PPS": "455AA",
        "SEAR": "279II",
        "TdSC": "281II",
        "CF": "260II",
        "CISI": "263II",
        "DV": "271II",
        "LVM": "1123I",
        "MSPPD": "849II",
        "ROB": "277II",
        "RA": "712II",
        "SGN": "278II",
        "SS": "280II"
    }

    exam_codes = [
        exam_codes_dict["CdP"],
        exam_codes_dict["ISTR"],
        exam_codes_dict["MdR"],
        exam_codes_dict["PPS"],
        exam_codes_dict["CF"],
        exam_codes_dict["SGN"],
        exam_codes_dict["MSPPD"],
        exam_codes_dict["ROB"]
        ]
    
    output_dir = os.getcwd() + "/" 

    mode = "3"

    while mode not in "12":
        mode = input("Select mode:\n\t1) Online (automatic find the newest calendar and search on it)\n\t2) Offline (you give the calendar pdf file path)\n")

        if int(mode) == 1:
            url = 'https://www.ing.unipi.it/it/studenti/calendario-esami'
            pdf_files_url = find_last_exam_calendar(url)

            for pdf_file in pdf_files_url:
                filter_calendar(pdf_file, exam_codes, output_dir)
            break

        if int(mode) == 2:
            pdf_file = input("Insert pdf file path without \"\":\n")
            filter_calendar(pdf_file, exam_codes, output_dir)
            break
        
        print("Input a valid mode selection\n\n")

