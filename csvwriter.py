import csv, time, sys

FILE_WRITE_BUFFER = 3000  # Specifies the number of bytes buffered before writing to
# the CSV file. This should be used to reduce write operations
# to the SD memory card.
#
# The script uses approximately 25 chars per line and 1 line
# per sec, so a value of 3000 equals one write operation
# per 2 to 4 minutes

outputPath = "./output"
csv_writers = {}
csv_filehandle = {}

# Flags
createdNewCSVs = False

def createFile(mac):
    global outputPath

    #ex createOutputFiles
    if len(csv_writers) != 0:
        for key in csv_writers.keys():
            csv_filehandle[key].close()

    if not outputPath.endswith('/'):
        outputPath = outputPath + "/"
    today = time.strftime("%d.%m.%Y")
    filename ="%d#%s.csv" % (mac + 7000, today)

    obj = open(outputPath + filename, 'ab', FILE_WRITE_BUFFER)
    csv_filehandle[mac] = obj
    csv_writers[mac] = csv.writer(obj, delimiter=';', quotechar='"')


def writeToCSV(mac, row):
    global createdNewCSVs, csv_writers
    checkTime = time.strftime("%H")

    # If we are at midnight, we need to create new files
    if (checkTime == "00" and createdNewCSVs == False):
        createFile(mac)
        createdNewCSVs = True

    # Reset flag after one hour
    if (checkTime != "00" and createdNewCSVs == True):
        createdNewCSVs = False

    csv_writers[mac].writerow(row)


def terminate():
    if len(csv_writers) != 0:
        for key in csv_writers.keys():
            csv_filehandle[key].close()