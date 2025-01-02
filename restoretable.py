import os
import utils


def process_sql_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".sql"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                for line in file:
                    if line.lower().startswith("insert"):
                        utils.sqlInsert(line.strip())
                        print(line.strip())
                        break

if __name__ == "__main__":
    # directory = r"K:\Quality - Records\7130 - Infrastructure\ciqms\Dump20241229-2\Dump20241229-2"
    process_sql_files(directory)